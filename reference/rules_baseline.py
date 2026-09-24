"""Conservative RULES ONLY comparator for synthetic B2B enquiries.

It reads customer input and the same fixed policy as JEV. The probability-shaped
adapter values below are deterministic interface markers, not model confidence.
"""
from __future__ import annotations

import re
from typing import Any

from policy_reference import decide, validate_input


def _has(text: str, *patterns: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def _choice(value: str, options: list[str]) -> dict[str, Any]:
    rest = .02 / (len(options) - 1)
    return {"type": "choice", "choice": value,
            "probabilities": {option: .98 if option == value else rest for option in options}}


def _score(value: int) -> dict[str, Any]:
    return {"type": "score", "score": value,
            "probabilities": {str(i): .97 if i == value else .01 for i in range(4)}}


def _flag(value: bool) -> dict[str, Any]:
    return {"type": "boolean", "probability": .98 if value else .02}


def infer_answers(lead: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Infer only explicit statements; unknown meaning remains reviewable."""
    text = lead["message"].lower()
    support = _has(text, r"\b(existing|current) (service|contract|agreement)\b", r"\b(stopped|broken|failing|restore|repair|incident|support fix)\b")
    expansion = _has(text, r"\b(separate|new) (paid )?(scope|rollout|project|purchase)\b", r"\bexpansion\b")
    vendor = _has(text, r"\bwe (sell|are offering)\b", r"\bbuy (our|an annual)\b", r"\breseller package\b") and not _has(text, r"\bwe are not offering\b")
    careers = _has(text, r"\b(job|career|employment|contractor placement)\b") and not _has(text, r"\bautomate\b")
    if vendor:
        kind = "supplier_pitch"
    elif careers:
        kind = "careers"
    elif support and expansion:
        kind = "mixed_support_and_sales"
    elif support and _has(text, r"\bnot (a |asking for a )?(new|separate) (purchase|project|expansion)\b", r"\bunder (our|the) (current|existing)\b"):
        kind = "existing_customer_support"
    elif expansion:
        kind = "customer_expansion"
    else:
        kind = "new_project"

    unsupported = _has(text, r"\breplace (our|the|an) entire erp\b", r"\b(warehouse|industrial) robots\b", r"\bnew (commercial )?saas product from scratch\b", r"\bmarketing website\b", r"\bsocial advertising campaign\b")
    discovery = _has(text, r"\bpaid (process )?(discovery|workshop|mapping|assessment)\b", r"\bwritten (recommendation|prioritisation report)\b") and _has(text, r"\b(no live deployment|discovery work only|quote only this discovery|written report)\b")
    enterprise = _has(text, r"\b(multi[- ]country|nine country|six country|all (nine|six) offices|enterprise[- ]wide)\b")
    pilot = _has(text, r"\b(one|single) (narrow |focused |paid )?(workflow|pilot|trial)\b", r"\bpilot\b")
    rollout = _has(text, r"\b(whole|entire|departmental|several|multiple|four)\b.{0,45}\b(workflows|rollout|process|reporting)\b", r"\brollout\b")
    if kind in ("existing_customer_support", "supplier_pitch", "careers"):
        scope = "not_applicable"
    elif unsupported:
        scope = "unsupported"
    elif enterprise:
        scope = "enterprise_rollout"
    elif discovery:
        scope = "paid_discovery"
    elif rollout and _has(text, r"\b(whole|entire|departmental|all four|four workflows|several)\b"):
        scope = "standard_rollout"
    elif pilot:
        scope = "focused_pilot"
    elif rollout:
        scope = "standard_rollout"
    elif _has(text, r"\b(workflow|automation|report|order|approval|process)\b"):
        scope = "unclear"
    else:
        scope = "unclear"

    risk = "feasibility_review" if _has(text, r"\bnot allowed api or export access\b", r"\bno external api calls\b", r"\bisolated network\b", r"\bhosting.*not.*approved\b", r"\baccess issue\b") else "none_stated"
    if kind in ("existing_customer_support", "supplier_pitch", "careers") or unsupported:
        risk = "not_applicable"
    if _has(text, r"\b(frozen|on hold|paused|cancelled|do not prepare a proposal until)\b"):
        readiness = "on_hold"
    elif _has(text, r"\b(not|has not|have not|no funds have been) approved\b", r"\bapproval.*pending\b", r"\bboard has not approved\b", r"\brequest from finance\b"):
        readiness = "approval_pending"
    elif _has(text, r"\b(researching|gathering examples|early planning|possible budget envelope)\b", r"\bno approved initiative\b"):
        readiness = "exploration_only"
    elif _has(text, r"\b(approved|authorised|authorized)\b"):
        readiness = "approved_current_phase"
    else:
        readiness = "unknown"
    if kind in ("existing_customer_support", "supplier_pitch", "careers"):
        readiness = "not_applicable"

    if _has(text, r"\bdo not (send|prepare).{0,25}(quote|quotation|proposal)\b", r"\bnot asking for a (paid )?proposal\b"):
        intent = 1
    elif readiness == "on_hold":
        intent = 0
    elif _has(text, r"\b(please|can you|would like you to).{0,40}(quote|proposal|prepare)\b", r"\bquote (the|this|it)\b", r"\bpaid (pilot|discovery|workshop)\b"):
        intent = 3
    elif _has(text, r"\b(comparing|evaluating|vendor comparison)\b"):
        intent = 2
    else:
        intent = 1
    fit = 0 if scope in ("unsupported", "not_applicable") else (1 if scope == "unclear" else 3)
    if kind in ("existing_customer_support", "supplier_pitch", "careers"):
        intent = 0

    # The form amount is authoritative for deterministic arithmetic. An explicit
    # conflicting amount for the same current phase requires review.
    amount = lead.get("budget_eur")
    stated = [int(a.replace(",", "")) for a in re.findall(r"EUR\s+([\d,]+)", text, re.I)]
    contradiction = amount is not None and any(a != amount for a in stated) and _has(text, r"\b(this exact|current implementation|not eur|approved budget for this)\b")
    ambiguity = scope == "unclear" and _has(text, r"\b(cannot yet name|improves everything|something useful)\b")
    flags = {"contradiction": contradiction, "instruction_attack": _has(text, r"\b(ignore (the|all) (instructions|rules)|change the model|reveal (the )?secret)\b"), "semantic_ambiguity": ambiguity}
    values = {"inquiry_type": kind, "engagement_scope": scope, "buying_readiness": readiness, "delivery_risk": risk}
    answers = {key: _choice(value, policy["choice_options"][key]) for key, value in values.items()}
    answers.update({"service_fit": _score(fit), "buying_intent": _score(intent)})
    answers.update({key: _flag(value) for key, value in flags.items()})
    return answers


def baseline_decide(lead: dict[str, Any], policy: dict[str, Any], reference_date: str) -> dict[str, Any]:
    if validate_input(lead, policy):
        return decide(lead, None, policy, reference_date)
    return decide(lead, infer_answers(lead, policy), policy, reference_date)
