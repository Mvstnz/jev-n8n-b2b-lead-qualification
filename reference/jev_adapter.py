"""Native JEV HTTP adapter. No request occurs without an explicit cost gate.

This module is deliberately independent of n8n credentials and side effects.
The transport can be injected for offline failure tests. A successful native
JEV response shape was confirmed with a live smoke test on 24 September 2026.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import json
from pathlib import Path
import time
from typing import Any, Callable
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from policy_reference import build_state, validate_answers, validate_input

ENDPOINT = "https://ai-gateway.vercel.sh/v1/evaluate"
MODEL = "typesafe-ai/jev"
MAX_ATTEMPTS = 120
Transport = Callable[[str, dict[str, str], bytes, int], tuple[int, dict[str, str], bytes]]


class JEVAdapterError(RuntimeError):
    """Safe error without a token, request body, or customer text."""


def default_transport(url: str, headers: dict[str, str], body: bytes,
                      timeout: int) -> tuple[int, dict[str, str], bytes]:
    request = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers), response.read(1_000_001)
    except HTTPError as error:
        return error.code, dict(error.headers), error.read(1_000_001)


def prepare_request(lead: dict[str, Any], policy: dict[str, Any],
                    questions: dict[str, Any], reference_date: str) -> bytes:
    invalid = validate_input(lead, policy)
    if invalid:
        raise JEVAdapterError("invalid_input:" + invalid)
    if len(questions) != 9 or set(questions) != {
        "inquiry_type", "engagement_scope", "service_fit", "buying_intent",
        "buying_readiness", "delivery_risk", "contradiction",
        "instruction_attack", "semantic_ambiguity",
    }:
        raise JEVAdapterError("invalid_questions")
    body = {"model": MODEL, "state": build_state(lead, policy, reference_date),
            "questions": questions}
    return json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def parse_response(payload: bytes, policy: dict[str, Any]) -> dict[str, Any]:
    if len(payload) > 1_000_000:
        raise JEVAdapterError("response_too_large")
    try:
        data = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise JEVAdapterError("invalid_response_json") from error
    if not isinstance(data, dict) or data.get("model") != MODEL:
        raise JEVAdapterError("unexpected_model")
    invalid = validate_answers(data.get("answers"), policy)
    if invalid:
        raise JEVAdapterError("invalid_answers:" + invalid)
    return {
        "model": data["model"], "answers": data["answers"],
        "request_id": data.get("id"), "created": data.get("created"),
        "usage": data.get("usage"), "provider_metadata": data.get("providerMetadata"),
    }


@dataclass
class CostGate:
    """Fails closed when catalogue price is positive and no spend is authorised.

    A positive allowance is a spending permission, not a hard billing cap. The
    provider may charge for timeouts and hidden request overhead. An operator
    must monitor actual usage separately before enabling such an allowance.
    """

    input_price_usd_per_token: Decimal
    paid_budget_usd: Decimal = Decimal("0")
    max_attempts: int = MAX_ATTEMPTS
    attempts: int = 0

    def before_attempt(self) -> None:
        if self.attempts >= self.max_attempts:
            raise JEVAdapterError("attempt_cap_exhausted")
        if self.input_price_usd_per_token < 0 or self.paid_budget_usd < 0:
            raise JEVAdapterError("invalid_cost_configuration")
        if self.input_price_usd_per_token > 0 and self.paid_budget_usd == 0:
            raise JEVAdapterError("positive_price_with_zero_budget")
        self.attempts += 1  # Timeouts may be billable, so count before transport.


def evaluate_live(body: bytes, key: str, policy: dict[str, Any], gate: CostGate,
                  transport: Transport = default_transport) -> dict[str, Any]:
    """Send one native evaluation with at most one transient retry.

    Do not call from untrusted form fields. Key, gate and policy are trusted
    runtime configuration. The caller must persist attempt/cost accounting.
    """
    if not key or "\n" in key or "\r" in key:
        raise JEVAdapterError("missing_or_invalid_runtime_key")
    for retry in range(2):
        gate.before_attempt()
        try:
            status, headers, response_body = transport(
                ENDPOINT,
                {"Authorization": "Bearer " + key, "Content-Type": "application/json"},
                body, 15,
            )
        except (TimeoutError, OSError) as error:
            if retry == 0:
                continue
            raise JEVAdapterError("transport_failure") from error
        if status == 200:
            return parse_response(response_body, policy)
        if status in (408, 429, 500, 502, 503, 504) and retry == 0:
            value = headers.get("Retry-After", headers.get("retry-after", "0"))
            try:
                delay = max(0.0, float(value))
            except ValueError:
                delay = 0.0
            if delay > 2:
                raise JEVAdapterError("retry_after_exceeds_bound")
            if delay:
                time.sleep(delay)
            continue
        raise JEVAdapterError("http_status:" + str(status))
    raise JEVAdapterError("retry_exhausted")


def load_public_configuration(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        json.loads((root / "config/policy.json").read_text(encoding="utf-8")),
        json.loads((root / "config/jev-questions.json").read_text(encoding="utf-8")),
    )
