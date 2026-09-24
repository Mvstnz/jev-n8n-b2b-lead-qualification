"""Offline reference policy for a fictional B2B automation provider.

No HTTP, n8n, Google or Slack operations. Input answers are already-decoded
JEV-shaped data or explicitly labelled hand-authored mocks. Passing these tests
validates business rules, NOT model quality or external integrations.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import date, timedelta
from math import isfinite
import re
from typing import Any

CHOICES = ('inquiry_type', 'engagement_scope', 'buying_readiness', 'delivery_risk')
SCORES = ('service_fit', 'buying_intent')
FLAGS = ('contradiction', 'instruction_attack', 'semantic_ambiguity')


def is_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and isfinite(value)


def materialize_fixture(item: dict[str, Any], reference_date: str) -> dict[str, Any]:
    """Resolve the fixture's relative delivery date using trusted runner config."""
    lead = deepcopy(item['input'])
    offset = lead.pop('target_delivery_days_from_reference')
    lead['target_delivery_date'] = (
        None if offset is None else
        (date.fromisoformat(reference_date) + timedelta(days=offset)).isoformat()
    )
    return lead


def validate_input(lead: dict[str, Any], policy: dict[str, Any]) -> str | None:
    """Validate normalized input. HTTP allowlisting/byte limits happen upstream."""
    for field in ('company_name', 'contact_name'):
        if not isinstance(lead.get(field), str) or not lead[field].strip() or len(lead[field]) > 200:
            return 'invalid_' + field
    email = lead.get('contact_email')
    if not isinstance(email, str) or len(email) > 254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
        return 'invalid_contact_email'
    msg = lead.get('message')
    if not isinstance(msg, str) or not 1 <= len(msg.strip()) <= policy['defaults']['max_message_characters']:
        return 'invalid_message'
    budget = lead.get('budget_eur')
    if budget is not None and (not is_number(budget) or budget < 0):
        return 'invalid_budget'
    if lead.get('currency') != 'EUR':
        return 'unsupported_currency'
    size = lead.get('company_size')
    if size is not None and (not isinstance(size, int) or isinstance(size, bool) or size < 1):
        return 'invalid_company_size'
    delivery = lead.get('target_delivery_date')
    if delivery is not None:
        if not isinstance(delivery, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', delivery):
            return 'invalid_delivery_date'
        try:
            date.fromisoformat(delivery)
        except ValueError:
            return 'invalid_delivery_date'
    return None


def validate_answers(answers: Any, policy: dict[str, Any]) -> str | None:
    """Strict native-answer validation; never invent missing model results."""
    if not isinstance(answers, dict):
        return 'answers_not_object'
    for key in CHOICES:
        a = answers.get(key)
        options = policy['choice_options'][key]
        if not isinstance(a, dict) or a.get('type') != 'choice' or a.get('choice') not in options:
            return 'invalid_' + key
        p = a.get('probabilities')
        if not isinstance(p, dict) or set(p) != set(options):
            return 'invalid_' + key + '_probability_keys'
        if any(not is_number(v) or not 0 <= v <= 1 for v in p.values()):
            return 'invalid_' + key + '_probabilities'
        if abs(sum(p.values()) - 1.0) > 0.02:
            return 'invalid_' + key + '_probability_sum'
        if p[a['choice']] + 1e-9 < max(p.values()):
            return 'invalid_' + key + '_selected_choice'
    for key in SCORES:
        a = answers.get(key)
        if not isinstance(a, dict) or a.get('type') != 'score' or not is_number(a.get('score')) or not 0 <= a['score'] <= 3:
            return 'invalid_' + key
        p = a.get('probabilities')
        if not isinstance(p, dict) or set(p) != {'0', '1', '2', '3'}:
            return 'invalid_' + key + '_probability_keys'
        if any(not is_number(v) or not 0 <= v <= 1 for v in p.values()) or abs(sum(p.values()) - 1) > 0.02:
            return 'invalid_' + key + '_probabilities'
    for key in FLAGS:
        a = answers.get(key)
        if not isinstance(a, dict) or a.get('type') != 'boolean' or not is_number(a.get('probability')) or not 0 <= a['probability'] <= 1:
            return 'invalid_' + key
    return None


def build_state(lead: dict[str, Any], policy: dict[str, Any], reference_date: str) -> dict[str, Any]:
    """The model never receives names, contact details, test IDs or expected labels."""
    days = None if lead.get('target_delivery_date') is None else (
        date.fromisoformat(lead['target_delivery_date']) - date.fromisoformat(reference_date)
    ).days
    return {
        'business': deepcopy(policy['business']),
        'lead': {
            'message': lead['message'], 'budget_eur': lead.get('budget_eur'),
            'currency': lead['currency'], 'target_delivery_date': lead.get('target_delivery_date'),
            'days_until_delivery': days,
        },
    }


def decide(lead: dict[str, Any], answers: dict[str, Any] | None,
           policy: dict[str, Any], reference_date: str,
           provider_error: str | None = None) -> dict[str, Any]:
    """Business routing after normalization, using explicit priority gates.

    Does not implement input transport auth, I/O, side effects or deduplication.
    Date and policy are trusted server inputs, never customer override fields.
    """
    def out(route: str, reason: str, action: str, owner: str = 'sales',
            score: float | None = None, breakdown: dict[str, float] | None = None) -> dict[str, Any]:
        return {
            'route': route, 'priority_score': score, 'reason_code': reason,
            'next_action': action, 'owner_queue': owner,
            'review_required': route == 'NEEDS_REVIEW',
            'breakdown': breakdown, 'policy_version': policy['policy_version'],
        }
    def review(reason: str, action: str = 'A person must clarify this point before sales prioritisation.',
               owner: str = 'sales_review') -> dict[str, Any]:
        return out('NEEDS_REVIEW', reason, action, owner)
    invalid = validate_input(lead, policy)
    if invalid:
        return out('INVALID_INPUT', invalid, 'Correct the submitted information; no model call is needed.', 'intake')
    if provider_error:
        return review('provider_error', 'Review the technical error; do not substitute mock decisions.', 'technical_review')
    error = validate_answers(answers, policy)
    if error:
        return review('malformed_model_response', 'Inspect the invalid model response: ' + error, 'technical_review')
    assert answers is not None
    thresholds = policy['review_thresholds']
    if answers['instruction_attack']['probability'] >= thresholds['instruction_attack_probability']:
        return review('instruction_attack', 'Review the untrusted instruction attempt; keep configuration unchanged.', 'technical_review')
    if answers['contradiction']['probability'] >= thresholds['contradiction_probability']:
        return review('conflicting_information', 'Clarify the conflicting facts for the current paid phase.')

    def choice_uncertain(key: str) -> bool:
        a = answers[key]
        ordered = sorted(a['probabilities'].values(), reverse=True)
        return (a['probabilities'][a['choice']] < thresholds['minimum_choice_probability']
                or ordered[0] - ordered[1] < thresholds['minimum_choice_margin'])

    kind = answers['inquiry_type']['choice']
    if choice_uncertain('inquiry_type') or kind == 'unclear':
        return review('unclear_inquiry_type', 'Clarify who is buying what and whether this is a new request.')
    if kind == 'existing_customer_support':
        return out('NOT_A_SALES_LEAD', 'existing_customer_support',
                   'Route to the support owner for incident triage; do not discard or sales-score the message.', 'support')
    if kind == 'supplier_pitch':
        return out('NOT_A_SALES_LEAD', 'supplier_pitch', 'Route to the vendor-review owner, not the sales queue.', 'vendor_review')
    if kind == 'careers':
        return out('NOT_A_SALES_LEAD', 'careers', 'Route to the people/contractor inbox, without candidate scoring.', 'people')
    if kind == 'mixed_support_and_sales':
        return review('mixed_support_and_sales', 'Split the existing support issue and proposed new scope; preserve both owners.', 'support_and_sales')
    if answers['semantic_ambiguity']['probability'] >= thresholds['semantic_ambiguity_probability']:
        return review('ambiguous_request', 'Clarify the current deliverable; do not invent a scope from the budget.')
    if choice_uncertain('engagement_scope'):
        return review('uncertain_scope')
    scope = answers['engagement_scope']['choice']
    fit = answers['service_fit']['score']
    intent = answers['buying_intent']['score']
    if scope == 'unsupported' or fit <= policy['routing']['clear_mismatch_max_fit']:
        return out('COLD', 'outside_service_offer', 'Record the mismatch; a person may discuss alternatives. Do not auto-reject.')
    if scope in ('unclear', 'not_applicable') or fit < policy['routing']['minimum_clear_fit']:
        return review('scope_needs_clarification', 'Clarify the mixed or weakly defined service requirement.')
    if scope == 'enterprise_rollout':
        return review('enterprise_feasibility', 'Assign solution review for the current enterprise-wide commitment.', 'solution_review')
    if choice_uncertain('delivery_risk') or answers['delivery_risk']['choice'] != 'none_stated':
        return review('delivery_dependency', 'Check stated access, integration or hosting dependencies before qualification.', 'solution_review')
    if lead.get('budget_eur') is None or lead.get('target_delivery_date') is None:
        return review('missing_commercial_fields', 'Ask for the budget and requested completion date of the current paid phase.')
    phase = policy['business']['phases'][scope]
    days = (date.fromisoformat(lead['target_delivery_date']) - date.fromisoformat(reference_date)).days
    if days < phase['minimum_notice_days']:
        return review('delivery_too_soon', 'Discuss the requested date with a delivery owner; no capacity promise.', 'solution_review')
    if lead['budget_eur'] < phase['minimum_budget_eur']:
        return out('COLD', 'budget_below_current_scope', 'Record the budget-to-scope gap; do not relabel the scope to make it fit.')
    if choice_uncertain('buying_readiness'):
        return review('uncertain_approval')
    ready = answers['buying_readiness']['choice']
    if ready in ('unknown', 'not_applicable'):
        return review('approval_not_stated', 'Ask whether funding for this specific paid phase is approved.')
    if ready == 'on_hold':
        return out('WARM', 'project_on_hold', 'Retain the opportunity on hold; resume only after an explicit restart.')
    if ready == 'approval_pending':
        return out('WARM', 'approval_pending', 'Support the stated approval process; do not treat estimated funds as authorised.')
    if ready == 'exploration_only':
        return out('WARM', 'research_stage', 'Keep in a research-stage queue; no unsolicited outreach in this demo.')
    if days > policy['routing']['long_horizon_days']:
        return out('WARM', 'future_delivery_horizon', 'Keep a later follow-up recommendation without starting an automatic campaign.')
    ratio = lead['budget_eur'] / phase['minimum_budget_eur']
    budget_points = next(row['points'] for row in policy['budget_points'] if ratio >= row['minimum_ratio'])
    timing_points = next(row['points'] for row in policy['timing_points'] if days <= row['maximum_days'])
    parts = {
        'service_fit': fit / 3 * policy['weights']['service_fit'],
        'buying_intent': intent / 3 * policy['weights']['buying_intent'],
        'budget_fit': budget_points, 'timing': timing_points,
    }
    raw = sum(parts.values())
    r = policy['routing']
    if raw >= r['hot_min_score'] and fit >= r['hot_min_service_fit'] and intent >= r['hot_min_buying_intent']:
        return out('HOT', 'qualified_current_phase', 'Recommend a personal sales follow-up for the defined paid phase.',
                   score=round(raw, 2), breakdown={k:round(v,2) for k,v in parts.items()})
    if raw >= r['warm_min_score']:
        return out('WARM', 'not_yet_concrete_buying_step', 'Record fit and interest; clarify the next buying step.',
                   score=round(raw, 2), breakdown={k:round(v,2) for k,v in parts.items()})
    return out('COLD', 'low_policy_priority', 'Keep the record with its explanation; no automatic rejection.',
               score=round(raw, 2), breakdown={k:round(v,2) for k,v in parts.items()})
