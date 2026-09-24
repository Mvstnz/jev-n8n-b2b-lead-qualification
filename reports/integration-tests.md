# Integration evidence

| Check | Result | Evidence boundary |
|---|---|---|
| n8n MCP initialize/tools | PASS | Actual remote management connection |
| n8n mock showcase validation | PASS, 5 nodes | Workflow SDK validation |
| n8n mock showcase manual run | PASS, five outputs | MOCK only; no external side effects |
| n8n protected form validation | PASS, one synthetic DEV-01 input | Inactive form-trigger manual execution |
| Google Sheet creation/read | PASS, four tabs and Summary values | Codex Google connector action, not n8n runtime |
| Google Sheets n8n write/read | NOT RUN | Action OAuth still needs Google authorization |
| JEV native HTTP from n8n | NOT RUN | Positive catalog price conflicts with zero paid budget; credential unbound |
| JEV native HTTP adapter offline | PASS | Request allowlist, typed-response checks, cost gate and transient retry tested with fake transport; no provider request |
| Slack private sender gate | PASS | Inactive three-node workflow validated; manual execution succeeded and only the approval-gate node ran, emitting zero items |
| Slack webhook send | NOT RUN | Preview-only gate; user approval still required |
| 30×3 live evaluation | NOT RUN | 0 of 90 main calls |

The Google sheet has `Leads`, `TestRuns`, `Summary` and `Config` tabs. Leads has 44 named columns covering the business view, idempotency, policy/model provenance, timing, cost and notification status. TestRuns has 23 named columns. Header rows are frozen, and Leads/TestRuns have filters. The sheet uses UTC. No lead or TestRuns row is claimed to have been written by n8n.

The n8n mock execution yielded HOT (DEV-01, score 100), HOT (DEV-02, score 95), WARM (DEV-03, Not scored), NEEDS_REVIEW (DEV-07, Not scored) and NOT_A_SALES_LEAD/support (DEV-09, Not scored). These came from hand-authored answers and fixed policy, not JEV. The form execution accepted a valid synthetic record; no claim is made for an invalid-input integration run.
