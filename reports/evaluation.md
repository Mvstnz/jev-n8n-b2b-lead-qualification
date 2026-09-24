# Evaluation status

The authored set contains 30 synthetic cases: HOT 8, WARM 7, COLD 4, NEEDS_REVIEW 9 and NOT_A_SALES_LEAD 2. These are policy targets, not real sales outcomes. Each case had three planned JEV runs.

| Source | Development agreement | Evaluation agreement | Meaning |
|---|---:|---:|---|
| HAND-AUTHORED MOCK | 10/10 | 30/30 | Typed-answer and fixed-gate regression only |
| n8n MOCK_REPEAT | — | 90/90 | Repeated stored answers, not model repeatability |
| RULES ONLY | 8/10 | 24/30 | Deterministic baseline over all synthetic cases |
| LIVE JEV | 1/1 n8n integration case | 23/28 valid replies | 90 slots attempted; 62 yielded no valid model answer |

The native JEV campaign attempted all 90 case/repetition slots. **28** produced valid typed responses; **62** did not: 59 were stopped because `Retry-After` exceeded the adapter's two-second bound, two ended HTTP 503 and one ended HTTP 429. The 28 valid outputs agreed with authored routes **23/28**. The first repetition yielded 24 valid answers and 20 agreements. Five valid disagreements were all authored `WARM` cases routed to `NEEDS_REVIEW` by uncertainty or unclear-scope gates; there were **zero false HOT** outcomes among valid replies. Only two cases received at least two valid repetitions, and both retained the same route. Full three-run stability cannot be estimated.

Among the 28 valid replies, agreement with authored typed semantics was `inquiry_type` 27/28, `engagement_scope` 24/28, `buying_readiness` 22/28, and `delivery_risk` 25/28. Binary flag agreement at the policy threshold was contradiction 27/28, instruction attack 28/28 and semantic ambiguity 28/28. These comparisons are against self-authored labels and include repeated cases; they are not independent accuracy estimates. Every valid reply reported gateway cost **USD 0** during the promotion. The authenticated credit balance remained USD 5 at periodic checks. Provider latency was not captured.

The baseline was implemented before labels were joined by its runner, with no case-ID branches. Its 24/30 covers all 30 cases, while JEV's 23/28 excludes provider failures, so a direct win/loss claim is unjustified. Provider errors were retained as errors and never replaced with mocks. The run stopped with 100 counted live attempts, below the 120-attempt campaign ceiling; retries need a later rate-limit window and fresh credit checks.
