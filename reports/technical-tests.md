# Technical case status

The 20 scenarios are defined in [`fixtures/technical_tests.json`](../fixtures/technical_tests.json). “Offline checked” means a deterministic unit/reference assertion or a fake transport; it does not prove n8n side effects. The n8n tests below ran on an inactive demo workflow with synthetic data.

| Case | Status on 24 September 2026 | Evidence boundary |
|---|---|---|
| TECH-01 Double submission | Serial n8n checked | Two identical replays within 24 hours returned stored receipts; no JEV or append node ran |
| TECH-02 Reused key, changed request | Not run | Conflict handling not implemented |
| TECH-03 Lost response after save | Partially checked | A serial replay after successful save returned the stored receipt; an actual lost network response was not injected |
| TECH-04 JEV unavailable | Partially checked | Native adapter handled provider 429/503 during campaign; n8n outage branch was not injected |
| TECH-05 Invalid provider authentication | Partially checked | Initial 403 was recorded; no deliberate n8n credential failure was injected |
| TECH-06 Malformed typed answer | Offline checked | Reference policy routes malformed scores/probabilities to technical review; n8n malformed-response run not performed |
| TECH-07 Sheets write failure | Not run | Successful n8n append/read-back proven; failure behavior remains untested |
| TECH-08 Unknown Slack delivery | Not run | No webhook sends; private sender gate correctly emitted zero send items |
| TECH-09 Spreadsheet/message injection | Partially checked | Slack preview source escapes markup and suppresses ASCII `@`; no adversarial n8n/Sheets run |
| TECH-10 Customer configuration override | Partially checked | Model-state allowlist checked offline; 28 live replies were parsed, but no adversarial n8n form run |
| TECH-11 Unknown, zero and invalid budget | Offline and n8n checked | Reference null/zero/negative cases pass; protected Intake returned `INVALID_INPUT` for a negative budget without external calls |
| TECH-12 Phase price boundaries | Offline checked | Discovery, pilot and rollout floors tested in reference policy |
| TECH-13 Delivery date boundaries | Offline checked | Phase minimum notice and long horizon tested in reference policy |
| TECH-14 Uncertain categorical decision | Offline checked | Low choice probability routes to review |
| TECH-15 Size and role invariance | Offline checked | Deterministic route unchanged when size, role or company name changes; live model invariance not measured |
| TECH-16 Mixed support and expansion | Partially checked | Synthetic mocks pass; a subset received valid live JEV replies, but provider limits prevented full-set assessment |
| TECH-17 Concurrent duplicates | Not run | Sheets lookup plus append is not atomic; parallel submissions remain unsafe |
| TECH-18 Cost guard/call cap | Offline and runtime checked | Zero paid budget blocks locally; dedicated key has USD 1 non-resetting Gateway budget inside USD 5 free credits. Private campaign stopped below 120 attempts; n8n cross-execution cap is not implemented |
| TECH-19 Label leakage | Offline and runtime checked | All 40 fixture states use the five-field lead allowlist and exclude authored labels; successful native requests use that builder |
| TECH-20 Export/secret scan | Release checked | Exact supplied-value, staged/history and forbidden-file scans passed; no screenshots were submitted for visual review |

The first Gateway smoke returned 403. A subsequent smoke, two distinct n8n end-to-end executions and 28 evaluation replies succeeded. Two serial n8n duplicate replays returned stored receipts. Provider rate limits interrupted the rest of the evaluation; see [evaluation](evaluation.md). Technical statuses distinguish a successful path from concurrent or failure recovery behavior.
