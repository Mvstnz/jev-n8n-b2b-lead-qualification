# Integration evidence

| Check | Result | Evidence boundary |
|---|---|---|
| n8n MCP initialize/tools | PASS | Actual remote management connection |
| n8n mock showcase validation and run | PASS, five outputs | MOCK only; no external side effects |
| Protected form preview | PASS | One synthetic valid form input |
| Protected Intake pipeline validation | PASS, 13 nodes | Private IDs bound in n8n; public source has placeholders |
| Intake invalid-input branch | PASS | Negative budget returned `INVALID_INPUT` and `invalid_budget`; no provider/storage node ran |
| Intake valid-input run | PASS, five distinct inputs | DEV-01, DEV-02, DEV-03, DEV-07 and DEV-09 completed fingerprint, empty lookup, JEV, fixed gates, Sheets append, preview and receipt |
| 24-hour duplicate replay | PASS, two serial replays | Stored receipt returned; neither JEV nor append node ran; row count stayed at two |
| n8n mock Test Runner | PASS, 90/90 authored routes | Stored hand-authored answers, not model quality |
| n8n Evaluation Core | PASS | Native `POST /v1/evaluate` returned typed answers; private runtime key header, workflow inactive |
| Google Sheet creation | PASS | Private four-tab Sheet created through Codex Google connector |
| Google Sheets n8n append | PASS | Five synthetic leads appended by n8n action node: HOT 2, NEEDS_REVIEW 2, NOT_A_SALES_LEAD 1 |
| Google Sheets persisted read-back | PASS | All five rows and their actual categories read independently through Codex Google connector |
| `TestRuns` and `Summary` population | PASS, plugin action | 90 live result/error rows and updated summary written through Codex Google connector, not n8n Test Runner |
| JEV native HTTP adapter | PASS | Second smoke returned validated response; fake-transport tests also pass |
| Vercel free-credit control | PASS for this run | USD 5 starting credits, USD 1 lifetime key budget, model cost USD 0; no purchase |
| Slack private sender gate | PASS | Gate emitted zero items; HTTP send node did not run |
| Slack webhook delivery | PASS, six MOCK messages | One approved private n8n sender execution delivered five MOCK lead notifications and one MOCK summary; Slack channel read-back confirmed six, then sender gate was relocked |
| Live JEV evaluation | PARTIAL | 90 planned slots attempted; 28 valid replies, 62 provider errors; see [evaluation](evaluation.md) |

The Sheet has `Leads`, `TestRuns`, `Summary` and `Config` tabs. `Leads` has 44 named columns. Its five n8n-written synthetic rows include two `HOT` with scores `97.8` and `93.02`, two `NEEDS_REVIEW`, and one `NOT_A_SALES_LEAD`. All used model `typesafe-ai/jev` and retained `slack_status = PREVIEW_ONLY`. The second row has a SHA-256 payload fingerprint and form idempotency key; the first row was backfilled privately for duplicate testing. `TestRuns` contains 90 plugin-written rows with 28 valid responses and 62 explicit provider errors. Raw responses stay outside the Sheet and public repository.

The mock showcase returned HOT for DEV-01 (100), HOT for DEV-02 (95), WARM for DEV-03, NEEDS_REVIEW for DEV-07 and NOT_A_SALES_LEAD/support for DEV-09. Those use hand-authored answers and were the source of the approved Slack messages. Live JEV intake returned HOT for DEV-01 and DEV-02 (97.8 and 93.02), NEEDS_REVIEW for DEV-03 and DEV-07, and NOT_A_SALES_LEAD/support for DEV-09. The DEV-03 difference from the authored WARM expectation reflects a model-assessed `paid_discovery` scope and an `uncertain_scope` gate; development showcase route agreement was 4/5. No failed JEV call was replaced by a mock answer.
