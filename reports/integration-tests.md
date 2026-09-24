# Integration evidence

| Check | Result | Evidence boundary |
|---|---|---|
| n8n MCP initialize/tools | PASS | Actual remote management connection |
| n8n mock showcase validation and run | PASS, five outputs | MOCK only; no external side effects |
| Protected form preview | PASS | One synthetic valid form input |
| Protected Intake pipeline validation | PASS, eight nodes | Private IDs bound in n8n; public source has placeholders |
| Intake invalid-input branch | PASS | Negative budget returned `INVALID_INPUT` and `invalid_budget`; no provider/storage node ran |
| Intake valid-input run | PASS | Synthetic DEV-01 completed JEV, fixed gates, Sheets append, Slack preview and receipt |
| n8n mock Test Runner | PASS, 90/90 authored routes | Stored hand-authored answers, not model quality |
| n8n Evaluation Core | PASS | Native `POST /v1/evaluate` returned typed answers; private runtime key header, workflow inactive |
| Google Sheet creation | PASS | Private four-tab Sheet created through Codex Google connector |
| Google Sheets n8n append | PASS | Synthetic `HOT` lead appended by n8n action node |
| Google Sheets persisted read-back | PASS | Same row and model ID read independently through Codex Google connector |
| JEV native HTTP adapter | PASS | Second smoke returned validated response; fake-transport tests also pass |
| Vercel free-credit control | PASS for this run | USD 5 starting credits, USD 1 lifetime key budget, model cost USD 0; no purchase |
| Slack private sender gate | PASS | Gate emitted zero items; HTTP send node did not run |
| Slack webhook delivery | NOT RUN | Combined send approval remains outstanding |
| Live JEV evaluation | PARTIAL | 90 planned slots attempted; 28 valid replies, 62 provider errors; see [evaluation](evaluation.md) |

The Sheet has `Leads`, `TestRuns`, `Summary` and `Config` tabs. `Leads` has 44 named columns for business view, idempotency, provenance, cost and notification status. The one n8n-written row is synthetic: category `HOT`, score `97.8`, model `typesafe-ai/jev`, and `slack_status = PREVIEW_ONLY`. `TestRuns` was not populated by n8n; live evaluation and raw responses remain private.

The mock showcase returned HOT for DEV-01 (100), HOT for DEV-02 (95), WARM for DEV-03, NEEDS_REVIEW for DEV-07 and NOT_A_SALES_LEAD/support for DEV-09. Those use hand-authored answers. The live DEV-01 route was HOT (97.8), a distinct model-derived result. No failed JEV call was replaced by a mock answer.
