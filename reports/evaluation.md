# Evaluation status

The authored evaluation set contains 30 synthetic cases: HOT 8, WARM 7, COLD 4, NEEDS_REVIEW 9 and NOT_A_SALES_LEAD 2. These are policy targets, not observed model predictions.

| Source | Development route agreement | Evaluation route agreement | Meaning |
|---|---:|---:|---|
| HAND-AUTHORED MOCK | 10/10 | 30/30 | Exercises typed-answer validation and fixed business gates only |
| n8n MOCK_REPEAT | — | 90/90 repeated authored routes | n8n policy regression using stored mock answers, not provider repeatability |
| RULES ONLY | 8/10 | 24/30 | Deterministic baseline on the same synthetic inputs |
| LIVE JEV | 0/10 run | 0/90 repetitions run | No semantic or repeatability metric available |

The baseline was implemented before evaluation labels were joined by the runner. It uses explicit phrase and negation rules and the same policy gates; it contains no case-ID branches. Its 24/30 agreement is a small self-authored synthetic-policy measure. It is not a sales prediction or an independent benchmark.

Primary JEV first-run agreement: **Not measured (0/30 planned)**. False HOT, HOT precision/recall, question-level agreement, review share, all-three-repeat consistency, provider latency and provider-reported costs: **Not measured**. No failed JEV call was silently replaced by mocks. One authorised native smoke attempt returned HTTP 403 `customer_verification_required`; it produced no model answer and was not retried. The Gateway account must be verified before the campaign can proceed.
