# Slack MOCK demo: six messages sent

These five texts were produced by an actual n8n MOCK execution and delivered in one approved private sender run on 24 September 2026. `MOCK` means hand-authored typed answers; none is a live JEV result. Names and messages are synthetic. A read-back of the private Slack demo channel confirmed all six messages. The sender's gate was relocked after delivery and the workflow remains inactive.

```text
B2B ENQUIRY | DEMO | MOCK
Company: Alder Manufacturing
Current phase: standard_rollout
Budget EUR: 30000
Requested completion: 2026-11-30
Category: HOT
Priority: 100
Reason: qualified_current_phase
Next action: Recommend personal sales follow-up.
Owner: sales
```

```text
B2B ENQUIRY | DEMO | MOCK
Company: Beacon Services
Current phase: focused_pilot
Budget EUR: 6000
Requested completion: 2026-10-31
Category: HOT
Priority: 95
Reason: qualified_current_phase
Next action: Recommend personal sales follow-up.
Owner: sales
```

```text
B2B ENQUIRY | DEMO | MOCK
Company: Cedar Distribution
Current phase: standard_rollout
Budget EUR: 40000
Requested completion: 2026-11-30
Category: WARM
Priority: Not scored
Reason: approval_pending
Next action: Support the approval process.
Owner: sales
```

```text
B2B ENQUIRY | DEMO | MOCK
Company: Grove Industrial Group
Current phase: enterprise_rollout
Budget EUR: 120000
Requested completion: 2026-12-30
Category: NEEDS_REVIEW
Priority: Not scored
Reason: enterprise_feasibility
Next action: Assign solution review.
Owner: solution_review
```

```text
B2B ENQUIRY | DEMO | MOCK
Company: Ivy Parts
Current phase: not_applicable
Budget EUR: Not stated
Requested completion: Not stated
Category: NOT_A_SALES_LEAD
Priority: Not scored
Reason: existing_customer_support
Next action: Route for support triage; do not discard or sales-score.
Owner: support
```

Sixth sent message, a summary prepared from that same run:

```text
B2B DEMO SUMMARY | MOCK | PREVIEW ONLY
Five synthetic showcase enquiries processed in n8n.
Routes: HOT 2, WARM 1, NEEDS_REVIEW 1, NOT_A_SALES_LEAD 1.
Live JEV evaluations: 0. Google Sheets runtime writes: 0.
This six-message batch is an internal mock demonstration.
These are policy/mock checks, not model performance or sales outcomes.
```

This six-message batch was the only approved send. The summary text retains `PREVIEW ONLY` because it describes the MOCK preview outputs; its delivery does not make those outputs live JEV results. The private webhook and Slack channel identifiers are intentionally absent from this public report. No development or evaluation loop sent messages.
