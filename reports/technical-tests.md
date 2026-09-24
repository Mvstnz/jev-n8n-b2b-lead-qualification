# Technical case status

The 20 scenarios are defined in [`fixtures/technical_tests.json`](../fixtures/technical_tests.json). “Offline checked” means a deterministic unit/reference assertion or a fake transport; it does not prove n8n side effects. The n8n tests below ran on an inactive demo workflow with synthetic data.

| Case | Status on 24 September 2026 | Evidence boundary |
|---|---|---|
| TECH-01 Double submission | Not run | Intake has no durable idempotency key or dedupe path |
| TECH-02 Reused key, changed request | Not run | Conflict handling not implemented |
| TECH-03 Lost response after save | Not run | n8n Sheets write blocked by OAuth |
| TECH-04 JEV unavailable | Not run | No injected outage; real gateway rejected account verification |
| TECH-05 Invalid provider authentication | Not run | No deliberate credential failure; runtime JEV credential unbound |
| TECH-06 Malformed typed answer | Offline checked | Reference policy routes malformed scores/probabilities to technical review; n8n malformed-response run not performed |
| TECH-07 Sheets write failure | Not run | No n8n Sheets write/read yet |
| TECH-08 Unknown Slack delivery | Not run | No webhook sends; private sender gate correctly emitted zero send items |
| TECH-09 Spreadsheet/message injection | Partially checked | Slack preview source escapes markup and suppresses ASCII `@`; no adversarial n8n/Sheets run |
| TECH-10 Customer configuration override | Partially checked | Model-state allowlist and attack-probability gate checked offline; no live model answer |
| TECH-11 Unknown, zero and invalid budget | Offline and n8n checked | Reference null/zero/negative cases pass; protected Intake returned `INVALID_INPUT` for a negative budget without external calls |
| TECH-12 Phase price boundaries | Offline checked | Discovery, pilot and rollout floors tested in reference policy |
| TECH-13 Delivery date boundaries | Offline checked | Phase minimum notice and long horizon tested in reference policy |
| TECH-14 Uncertain categorical decision | Offline checked | Low choice probability routes to review |
| TECH-15 Size and role invariance | Offline checked | Deterministic route unchanged when size, role or company name changes; live model invariance not measured |
| TECH-16 Mixed support and expansion | Fixture policy checked | Synthetic cases route under authored typed mocks; live interpretation unmeasured |
| TECH-17 Concurrent duplicates | Not run | Append-based Intake draft has no serialisation or atomic protection |
| TECH-18 Cost guard/call cap | Offline checked | Positive price plus zero budget blocks before transport; a one-attempt fake cap stops retry; fake 403 is never retried. n8n cross-execution cap is not implemented |
| TECH-19 Label leakage | Offline checked | All 40 fixture states use the five-field lead allowlist and exclude expected-route labels; no successful provider request |
| TECH-20 Export/secret scan | Release checked | Exact supplied-value, staged/history and forbidden-file scans passed; no screenshots were submitted for visual review |

The native Gateway smoke test made one authorised request and received HTTP 403 `customer_verification_required`. It is not evidence for a typed answer, semantic quality or any of the 90 planned evaluation repetitions.
