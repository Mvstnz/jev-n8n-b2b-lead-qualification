"""Offline tests for the native request shape and fail-closed budget gate."""
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import json

from jev_adapter import (CostGate, JEVAdapterError, evaluate_live,
                         load_public_configuration, parse_response, prepare_request)
from policy_reference import materialize_fixture


def expect_error(action, reason: str) -> None:
    try:
        action()
    except JEVAdapterError as error:
        assert str(error) == reason, (str(error), reason)
    else:
        raise AssertionError("expected " + reason)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    policy, questions = load_public_configuration(root)
    fixtures = json.loads((root / "fixtures/development_inputs.json").read_text(encoding="utf-8"))
    lead = materialize_fixture(fixtures[0], "2026-09-24")
    body = prepare_request(lead, policy, questions, "2026-09-24")
    request = json.loads(body)
    assert request["model"] == "typesafe-ai/jev"
    assert len(request["questions"]) == 9
    assert set(request["state"]["lead"]) == {
        "message", "budget_eur", "currency", "target_delivery_date", "days_until_delivery"
    }
    assert "contact_email" not in body.decode("utf-8")
    gate = CostGate(Decimal("0.000000042"))
    expect_error(lambda: evaluate_live(body, "fake-test-key", policy, gate),
                 "positive_price_with_zero_budget")
    assert gate.attempts == 0
    answers = json.loads((root / "fixtures/mock_answers.json").read_text(encoding="utf-8"))
    synthetic = {"model": "typesafe-ai/jev", "answers": answers["DEV-01"]["answers"]}
    parsed = parse_response(json.dumps(synthetic).encode(), policy)
    assert parsed["answers"] == answers["DEV-01"]["answers"]
    wrong = deepcopy(synthetic)
    wrong["model"] = "another-model"
    expect_error(lambda: parse_response(json.dumps(wrong).encode(), policy), "unexpected_model")
    calls = []
    def fake_transport(_url, _headers, _body, timeout):
        calls.append(timeout)
        if len(calls) == 1:
            return 503, {}, b""
        return 200, {}, json.dumps(synthetic).encode()
    free_gate = CostGate(Decimal("0"))
    assert evaluate_live(body, "fake-test-key", policy, free_gate, fake_transport)["model"] == "typesafe-ai/jev"
    assert free_gate.attempts == 2 and calls == [15, 15]
    blocked = CostGate(Decimal("0"), max_attempts=1)
    expect_error(lambda: evaluate_live(body, "fake-test-key", policy, blocked,
                 lambda *_: (503, {}, b"")), "attempt_cap_exhausted")
    assert blocked.attempts == 1
    auth_calls = []
    def denied(*_):
        auth_calls.append(1)
        return 403, {}, b""
    expect_error(lambda: evaluate_live(body, "fake-test-key", policy,
                 CostGate(Decimal("0")), denied), "http_status:403")
    assert auth_calls == [1]
    print("JEV adapter offline checks passed. Live calls: 0.")


if __name__ == "__main__":
    main()
