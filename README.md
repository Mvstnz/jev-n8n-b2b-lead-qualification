# B2B Lead Qualification with n8n + JEV

This is a synthetic portfolio demo for ClearFlow Automation, a fictional company that connects existing business software. It shows how current scope, funding and delivery gates can matter more than a large stated budget. An approved EUR 6,000 focused pilot can be HOT while an urgent EUR 40,000 rollout awaiting funding remains WARM. A broken existing workflow goes to support without a sales score.

## Verified status (24 September 2026)

| Component | Evidence |
|---|---|
| LOCAL POLICY TESTED | 292/292 supplied offline assertions passed |
| MOCK WORKFLOW TESTED | n8n manual execution succeeded; five synthetic cases produced the expected routes and Slack previews |
| FORM VALIDATION TESTED | n8n preview accepted a valid synthetic enquiry; gated Intake draft rejected a negative budget and stopped a valid enquiry at the closed JEV gate, before HTTP or Sheets |
| LIVE JEV TESTED | One native HTTP attempt reached the gateway but returned 403 `customer_verification_required`; zero valid JEV answers. The account requires a credit card even to unlock free credits |
| SHEETS TESTED | One native Google Sheet created and read through the Codex Google connector; n8n write/read is not verified |
| SLACK PREVIEW/SENT | Five n8n MOCK previews prepared; private six-message sender validated with approval gate closed; zero messages sent |
| EVALUATION COMPLETE | No: 0/90 planned live evaluations; n8n MOCK_REPEAT policy regression 90/90; RULES ONLY baseline 24/30 on authored synthetic labels |

The [integration report](reports/integration-tests.md), [evaluation report](reports/evaluation.md) and [technical-case status](reports/technical-tests.md) identify exactly what ran. Mock answers are hand-authored test fixtures, not JEV output. No real customers or sales outcomes are represented.

## Architecture and business policy

The intended production path is `authenticated intake → input allowlist → JEV native evaluate → typed-answer validation → fixed commercial gates → Google Sheets → Slack preview/approved send`. The deployed mock showcase runs the middle policy and preview path without side effects. A separate protected Intake Preview validates form data. An inactive [Intake pipeline draft](workflows/intake-pipeline.template.sdk.js) connects a protected form, the internal Evaluation Core, a private Sheets append node and a Slack preview branch. Its published source uses inert placeholders for private resource IDs. The Evaluation Core's credential is unbound and live gate closed; the separate inactive Test Runner exercises the 30 mock cases three times each. [Workflow sources](workflows/README.md) are portable Workflow SDK definitions, not credential-bearing raw exports.

JEV uses the [nine typed questions](config/jev-questions.json) against only the customer message, current-phase budget, currency, requested completion and derived days, plus the trusted fictional [policy](config/policy.json). The model must not receive names, roles, case IDs, authored labels or mock answers. [Reference code](reference/policy_reference.py) validates answer shapes and applies gates in order. The [rules-only baseline](reference/rules_baseline.py) uses fixed phrase and negation rules as a transparent comparator.

Current paid-phase floors are EUR 3,000 for discovery, EUR 5,000 for a narrow pilot and EUR 15,000 for a departmental rollout. Multi-country scope and unresolved access/hosting dependencies require review. These are invented demo rules, not market prices or delivery promises. A score is shown only after the relevant gates pass; it is not a purchase probability.

## Run local checks

From this repository root with Python 3.10+:

```sh
python reference/check_offline.py
python tools/test_release_guard.py
python reference/test_jev_adapter.py
python reference/run_local.py
python tools/release_guard.py --root .
```

`run_local.py` computes routes before it joins authored labels. It reports MOCK and RULES ONLY separately. Do not interpret their agreement as live-model quality.

## Import and finish runtime setup

1. Import/build [the mock showcase](workflows/mock-showcase.sdk.js), [intake preview](workflows/intake-preview.sdk.js), [mock Test Runner](workflows/test-runner.sdk.js), [native Evaluation Core](workflows/evaluation-core.sdk.js) and [gated Intake template](workflows/intake-pipeline.template.sdk.js) using an n8n Workflow SDK capable instance. Builders are in `tools/`. Supply private core/sheet IDs to the intake builder outside the public tree. Keep forms inactive until the end-to-end path and access protection are verified. The forms use n8n user authentication.
2. Create a private Google Sheet with `Leads`, `TestRuns`, `Summary` and `Config` tabs; the required columns are in [the integration report](reports/integration-tests.md). Bind a **Google Sheets action OAuth** credential in n8n. A Codex Google connector or a Google Sheets Trigger credential does not prove an n8n write.
3. Vercel returned `customer_verification_required` on the first authorised native request, so the account holder must unlock Gateway access. Bind the key through a supported n8n HTTP credential. The [Evaluation Core source](workflows/evaluation-core.sdk.js) targets `POST https://ai-gateway.vercel.sh/v1/evaluate` with `model: typesafe-ai/jev`, one shared allowlisted state and all nine questions. Its live gate and public default paid budget remain closed. The [offline HTTP adapter](reference/jev_adapter.py) builds the request and validates typed answers; the actual response contract still needs a successful live smoke test.
4. Keep the Slack Incoming Webhook in a private sender only. The current private n8n sender is inactive and its approval gate emits zero items; the public repository contains no webhook URL or secret-bearing sender export. Review [five previews and the proposed summary](reports/slack-previews.md), then obtain one combined send approval before enabling it. No development or evaluation loop may send Slack messages.
5. Run one n8n Sheets setup write/read, one JEV smoke test if authorised, then ten development cases. Freeze policy/questions/evaluation fixtures and run 30 evaluation cases three times each within the 120-attempt cap. Record errors, usage, cost, latency, question-level outputs and a fair baseline comparison.

## Limitations and security

The current n8n mock runs do not persist leads, call JEV or send Slack. The Intake pipeline draft is incomplete: its invalid-input branch ran, while a valid enquiry stopped at the closed internal JEV gate. No n8n HTTP or Sheets write was attempted in that run. The Evaluation Core is inactive: no HTTP credential is bound and it has not processed a real JEV response. The Google Sheet exists through a plugin action. A Google Sheets action credential was created in n8n and linked to the Intake draft but still needs Google OAuth authorization; no n8n write/read has succeeded. Idempotent storage and concurrent duplicate protection are not implemented. No public webhook, prospect email, automatic LinkedIn post or production sales processing is enabled.

Only synthetic fixtures and redacted source belong here. Do not commit credentials, private workflow exports, account URLs or raw executions. See [limitations](reports/limitations.md), [release checks](docs/PUBLIC_REPOSITORY_CHECKLIST.md) and [official references](docs/OFFICIAL_REFERENCES.md). No licence has been selected.
