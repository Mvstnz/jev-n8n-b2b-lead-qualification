# Business test cases: B2B lead qualification

All companies, messages, budgets and deadlines below are synthetic. The commercial rules belong to a fictional process-automation provider. Expected outcomes are policy targets, not observed JEV results.

## The business in one paragraph

ClearFlow Automation connects existing business systems to reduce repetitive office work: reports, quotation follow-ups, order updates, document handovers and approvals. Its demo offer includes paid discovery from EUR 3,000, a narrowly scoped pilot from EUR 5,000 and a departmental rollout from EUR 15,000. These are invented thresholds, not market-price claims. Enterprise programmes and unresolved technical dependencies require a person to review feasibility.

## What makes these tests commercially meaningful

A small approved pilot can be a better immediate opportunity than a large unfunded programme. An urgent request is not proof that a company can buy. Funding for a previous pilot does not approve the next rollout. A live customer incident can be urgent but still should not enter the sales pipeline.

## Development examples

### DEV-01 - Funded reporting rollout

**Company:** Alder Manufacturing (fictional)  
**Current-phase budget field:** EUR 30,000  
**Requested completion:** 60 days from the test reference date

> Our operations team spends 12 hours each week combining production and order reports from existing systems. We need automatic collection, an exception list and a daily management report for one department. EUR 30,000 is approved for this rollout and the operations director has authorised procurement. Please prepare a proposal for delivery in 60 days.

**Expected outcome:** `HOT`  
**Why:** Defined supported rollout, explicitly approved current-phase funding and a concrete proposal request.  
**What this tests:** Can the workflow recognise an actionable business opportunity rather than just the word AI?

### DEV-02 - Small paid pilot, real buying intent

**Company:** Beacon Services (fictional)  
**Current-phase budget field:** EUR 6,000  
**Requested completion:** 30 days from the test reference date

> We are a 12-person service company and sometimes forget to follow up quotations. We want one pilot: connect our existing CRM to email reminders for one sales team. EUR 6,000 has been approved for this pilot, to be delivered in 30 days. Please quote the paid pilot; a wider rollout is not part of this purchase.

**Expected outcome:** `HOT`  
**Why:** The current pilot meets the pilot policy; small company size is not a reason to reject it.  
**What this tests:** Does a realistic small pilot receive fair treatment?

### DEV-03 - Urgent, but not authorised

**Company:** Cedar Distribution (fictional)  
**Current-phase budget field:** EUR 40,000  
**Requested completion:** 60 days from the test reference date

> Missed order-status updates are causing complaints. We would like an automated update and escalation workflow for customer service in 60 days. EUR 40,000 is our planning estimate, not an approved budget. The board has not approved this project; its funding meeting is in 45 days. Can you draft a proposal for that decision?

**Expected outcome:** `WARM`  
**Why:** The need is genuine, but current-phase authorisation is explicitly pending. Urgency alone must not create a HOT lead.  
**What this tests:** Can the model separate operational pain from buying readiness?

### DEV-04 - Large budget, no buying initiative

**Company:** Delta Retail Group (fictional)  
**Current-phase budget field:** EUR 250,000  
**Requested completion:** 270 days from the test reference date

> Our strategy team is researching ways to automate weekly stock reporting. EUR 250,000 is an early planning envelope, not approved funding. We are collecting examples for next year, not requesting a quotation or selecting a supplier. Any departmental rollout would be at least 270 days away.

**Expected outcome:** `WARM`  
**Why:** A large planning number is not approved spending or a current buying step.  
**What this tests:** Does the system understand not requesting a quotation?

### DEV-05 - High value, wrong service

**Company:** Elm Logistics (fictional)  
**Current-phase budget field:** EUR 200,000  
**Requested completion:** 90 days from the test reference date

> We have approved EUR 200,000 to replace our entire ERP system and supply warehouse robots. We need a supplier to deliver that replacement in 90 days. Please send a full quotation; connecting or automating our existing software is not the requirement.

**Expected outcome:** `COLD`  
**Why:** The primary requested deliverables are explicitly outside the demo service offering.  
**What this tests:** Can the workflow resist a high-budget opportunity that is not a fit?

### DEV-06 - Rollout budget disguised as a pilot

**Company:** Field Wholesale (fictional)  
**Current-phase budget field:** EUR 7,000  
**Requested completion:** 60 days from the test reference date

> We call this a pilot, but we need order intake, stock checks, dispatch notifications and exception reporting deployed for the whole sales department. Our full budget of EUR 7,000 is approved; there is no separate implementation budget. Please quote delivery of all four workflows in 60 days.

**Expected outcome:** `COLD`  
**Why:** The actual requested deliverable is a rollout; the word pilot does not change its budget threshold.  
**What this tests:** Does the model assess actual scope rather than copy the customer label?

### DEV-07 - Promising multi-country programme

**Company:** Grove Industrial Group (fictional)  
**Current-phase budget field:** EUR 120,000  
**Requested completion:** 90 days from the test reference date

> Funding of EUR 120,000 is approved to automate quotation approvals across nine country offices. The current purchase includes all nine offices, different approval matrices and central reporting. Please propose a complete rollout in 90 days. We need your team to assess the architecture before committing.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** The current commitment is enterprise-wide; human feasibility review takes precedence over budget and intent.  
**What this tests:** Can commercial attractiveness be separated from delivery confidence?

### DEV-08 - Contradictory current budgets

**Company:** Harbour Components (fictional)  
**Current-phase budget field:** EUR 3,000  
**Requested completion:** 60 days from the test reference date

> We need a departmental order-reporting rollout in 60 days. The approved budget for this exact rollout is EUR 25,000, not EUR 3,000. Please prepare the implementation proposal.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** The form and message disagree about the same current-phase budget. Neither amount should be silently selected.  
**What this tests:** Are material contradictions surfaced?

### DEV-09 - Urgent existing-customer incident

**Company:** Ivy Parts (fictional)  
**Current-phase budget field:** Not stated  
**Requested completion:** Not stated

> Your order-notification workflow stopped this morning and our dispatch team cannot see new orders. This is support for the existing EUR 40,000 project, not a new purchase. Please investigate under our current service agreement.

**Expected outcome:** `NOT_A_SALES_LEAD`  
**Why:** Route to the support owner with no sales score; the historical contract value is not a new budget.  
**What this tests:** Is an urgent support issue kept out of the sales queue without being ignored?

### DEV-10 - A vendor selling to us

**Company:** Juniper Software (fictional)  
**Current-phase budget field:** EUR 20,000  
**Requested completion:** 60 days from the test reference date

> We sell a reporting platform and would like ClearFlow Automation to buy an annual licence for EUR 20,000. Can your purchasing team review our offer within 60 days? We are not seeking a process-automation supplier.

**Expected outcome:** `NOT_A_SALES_LEAD`  
**Why:** The direction of the transaction is reversed: this is a supplier offer, not customer demand.  
**What this tests:** Can the system tell a buyer from a seller?

## Development-separated evaluation cases

### EVAL-01 - Approved order-update rollout

**Company:** Kestrel Supply (fictional)  
**Current-phase budget field:** EUR 22,000  
**Requested completion:** 75 days from the test reference date

> Customer service retypes order updates from our inventory system into emails. We want status collection, outbound templates and an exception queue for this department. Procurement has approval to spend EUR 22,000 on this scope. Please send an implementation proposal for delivery in 75 days.

**Expected outcome:** `HOT`  
**Why:** A supported departmental rollout with approved funds and a proposal request.  
**What this tests:** Identify a funded operational improvement.

### EVAL-02 - Budget is still a business case

**Company:** Larch Trading (fictional)  
**Current-phase budget field:** EUR 28,000  
**Requested completion:** 90 days from the test reference date

> Late quotation follow-ups cost us opportunities. Please provide a proposal for CRM follow-up and exception reporting in 90 days. EUR 28,000 is the amount I will request from finance; no funds have been approved yet. I need the proposal to support that request.

**Expected outcome:** `WARM`  
**Why:** A proposal is requested, but approval for this scope is still pending.  
**What this tests:** Distinguish a serious evaluation from approved buying readiness.

### EVAL-03 - Website and ad campaign only

**Company:** Maple Packaging (fictional)  
**Current-phase budget field:** EUR 50,000  
**Requested completion:** 60 days from the test reference date

> We have EUR 50,000 approved for a new marketing website and a social advertising campaign, to be delivered in 60 days. Please quote this work. We do not require system integrations, reporting automation or operational workflows.

**Expected outcome:** `COLD`  
**Why:** The primary service requested is outside the provider offer despite good budget and intent.  
**What this tests:** Prioritise service fit over commercial size.

### EVAL-04 - Request with no current budget

**Company:** Northline Services (fictional)  
**Current-phase budget field:** Not stated  
**Requested completion:** 75 days from the test reference date

> We want a rollout that moves approved requests into our scheduling system and sends customer updates. Delivery in 75 days would help. Please prepare a proposal, but we cannot state a current budget or whether funding will be approved until we understand the scope.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** Current funding is unknown, not zero and not a reason for an automatic rejection.  
**What this tests:** Handle missing commercial information honestly.

### EVAL-05 - Paid discovery before a large possible programme

**Company:** Oakline Logistics (fictional)  
**Current-phase budget field:** EUR 4,000  
**Requested completion:** 21 days from the test reference date

> Our eventual automation programme could cost EUR 150,000, but that programme is not approved and is NOT the current purchase. We have authorised EUR 4,000 for paid process mapping and a written recommendation, due in 21 days. No live deployment is included. Please quote only this discovery engagement.

**Expected outcome:** `HOT`  
**Why:** Only the approved discovery phase is being bought now; a hypothetical large programme must not distort qualification.  
**What this tests:** Separate current paid scope from hypothetical future value.

### EVAL-06 - Existing-customer outage, not a new order

**Company:** Pine Distribution (fictional)  
**Current-phase budget field:** Not stated  
**Requested completion:** Not stated

> The workflow you delivered under our existing EUR 60,000 contract is failing and our sales team is missing new orders. Please restore the existing service under our support agreement. We are not asking for a new project or an expansion.

**Expected outcome:** `NOT_A_SALES_LEAD`  
**Why:** Support needs an owner, but the historical contract price is not new opportunity value.  
**What this tests:** Avoid treating urgency and a large historical amount as a hot lead.

### EVAL-07 - Small team, funded reminders pilot

**Company:** Quartz Consulting (fictional)  
**Current-phase budget field:** EUR 5,000  
**Requested completion:** 28 days from the test reference date

> Our eight-person firm loses track of sent proposals. We have approved exactly EUR 5,000 for one CRM-to-email follow-up workflow for our sales team, with delivery in 28 days. Please send the paid pilot proposal. No other workflows are part of this purchase.

**Expected outcome:** `HOT`  
**Why:** Exactly meets the pilot budget floor; company size carries no penalty.  
**What this tests:** Use scope-relative budget fit rather than a universal large-deal rule.

### EVAL-08 - Executive title without funding

**Company:** Ridge Manufacturing (fictional)  
**Current-phase budget field:** EUR 45,000  
**Requested completion:** 80 days from the test reference date

> I am the managing director and need automated stock exception and order reporting for one department. We would like the rollout in 80 days. EUR 45,000 is my planning allowance, but finance has not approved it and procurement cannot contract yet. Please prepare a proposal for our approval meeting.

**Expected outcome:** `WARM`  
**Why:** The title is not a substitute for explicit funding approval.  
**What this tests:** Avoid inferring buying authority from job title.

### EVAL-09 - Delivery in one week

**Company:** Stonefield Wholesale (fictional)  
**Current-phase budget field:** EUR 30,000  
**Requested completion:** 7 days from the test reference date

> EUR 30,000 is approved for order intake, inventory checks, shipping updates and departmental reporting. Please quote delivery of the whole rollout in seven days. This deadline cannot be moved without speaking to our operations director.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** The requested date is inside the minimum standard lead time. It requires feasibility discussion, not a HOT label or delivery promise.  
**What this tests:** Distinguish urgency from feasible delivery.

### EVAL-10 - Research wording includes a negated quote request

**Company:** Tern Retail (fictional)  
**Current-phase budget field:** EUR 80,000  
**Requested completion:** 150 days from the test reference date

> We are gathering examples of customer-service automation for a strategy paper. EUR 80,000 is a possible budget envelope and a rollout might happen in 150 days, but there is no approved initiative. Please do NOT send a quotation or arrange a supplier-selection call at this stage.

**Expected outcome:** `WARM`  
**Why:** The message explicitly denies a current quote or selection step.  
**What this tests:** Understand negation rather than triggering on quotation.

### EVAL-11 - Approved expansion, not support

**Company:** Umber Components (fictional)  
**Current-phase budget field:** EUR 18,000  
**Requested completion:** 60 days from the test reference date

> You already support our quotation workflow. We now want a separate paid rollout for order-status updates and dispatch exceptions in the same department. EUR 18,000 has been approved specifically for this new scope, for delivery in 60 days. Please prepare a proposal; this is not a support fix.

**Expected outcome:** `HOT`  
**Why:** A separately approved new purchase from an existing customer is a sales opportunity.  
**What this tests:** Separate expansion revenue from routine support.

### EVAL-12 - Unfunded rollout after funded pilot

**Company:** Vale Group (fictional)  
**Current-phase budget field:** EUR 70,000  
**Requested completion:** 120 days from the test reference date

> Our EUR 6,000 trial was approved last month. We are now requesting a proposal for a departmental rollout costing around EUR 70,000 in 120 days. The EUR 70,000 rollout budget has not been approved; the pilot approval does not cover it.

**Expected outcome:** `WARM`  
**Why:** Approval for a previous phase is not approval for the current requested rollout.  
**What this tests:** Track what funding applies to.

### EVAL-13 - Large programme needing feasibility review

**Company:** Willow Group (fictional)  
**Current-phase budget field:** EUR 180,000  
**Requested completion:** 120 days from the test reference date

> The board approved EUR 180,000 to automate approval processes in six country offices in the current engagement. Please propose the rollout for all offices in 120 days, including country-specific access controls and a shared audit trail.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** A multi-country current commitment is an enterprise scope requiring assessment.  
**What this tests:** Keep large complex deals visible without auto-qualifying them.

### EVAL-14 - Paid analysis, not free consulting

**Company:** Yarrow Services (fictional)  
**Current-phase budget field:** EUR 3,000  
**Requested completion:** 14 days from the test reference date

> We do not yet know which manual process to automate. We have approved EUR 3,000 for a paid process workshop and a written prioritisation report, completed in 14 days. Please quote that discovery work only; an implementation project would be a separate decision.

**Expected outcome:** `HOT`  
**Why:** An explicit paid discovery purchase is valid even before an implementation is chosen.  
**What this tests:** Recognise paid analysis as a real product, not weak intent.

### EVAL-15 - Too little money for the requested pilot

**Company:** Zephyr Parts (fictional)  
**Current-phase budget field:** EUR 2,500  
**Requested completion:** 35 days from the test reference date

> We have approved EUR 2,500 total for one CRM-to-email reminders pilot, to be delivered in 35 days. Please quote implementation, not a workshop. We cannot increase the budget and there is no separate technical budget.

**Expected outcome:** `COLD`  
**Why:** The current pilot is below the fictional EUR 5,000 pilot floor; do not silently relabel it discovery.  
**What this tests:** Compare money to the actual deliverable.

### EVAL-16 - Application-access dependency

**Company:** Aster Distribution (fictional)  
**Current-phase budget field:** EUR 26,000  
**Requested completion:** 75 days from the test reference date

> EUR 26,000 is approved for order intake, status emails and reporting in 75 days. Please propose the rollout. However, our ERP supplier has not allowed API or export access and we do not know whether any data connection is permitted. Delivery depends on resolving that access issue.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** An explicit unresolved source-data dependency prevents a normal qualification decision.  
**What this tests:** Do not turn a budget into evidence of technical feasibility.

### EVAL-17 - Legitimate vendor offer

**Company:** Birch Systems (fictional)  
**Current-phase budget field:** EUR 35,000  
**Requested completion:** 45 days from the test reference date

> Our company sells workflow software. We are offering ClearFlow Automation a EUR 35,000 annual reseller package and would like your purchasing decision in 45 days. We are not requesting that your company automate our processes.

**Expected outcome:** `NOT_A_SALES_LEAD`  
**Why:** The sender wants us to buy their software.  
**What this tests:** Detect the direction of a commercial proposal.

### EVAL-18 - Narrow funded pilot at a large group

**Company:** Cobalt Industrial (fictional)  
**Current-phase budget field:** EUR 7,000  
**Requested completion:** 35 days from the test reference date

> We are a group of 4,000 employees, but this request is only for one stock-alert workflow between our inventory system and email for one local team. EUR 7,000 is approved for that pilot, delivered in 35 days. Please quote it. A group rollout is only a future possibility, not part of this purchase.

**Expected outcome:** `HOT`  
**Why:** The actual paid scope is a local pilot, not an enterprise rollout just because the buyer is large.  
**What this tests:** Avoid using company size as a scope proxy.

### EVAL-19 - Approved initiative paused by management

**Company:** Dune Wholesale (fictional)  
**Current-phase budget field:** EUR 50,000  
**Requested completion:** 100 days from the test reference date

> We had EUR 50,000 approved for departmental reporting automation and expected delivery in 100 days. Management has now frozen new projects during restructuring. Do not prepare a proposal or start supplier selection until we explicitly reopen this initiative.

**Expected outcome:** `WARM`  
**Why:** The opportunity is on hold; the historical approval cannot make it actionable now.  
**What this tests:** Recognise that a hold overrides prior approval.

### EVAL-20 - Current budget mismatch

**Company:** Evergreen Supply (fictional)  
**Current-phase budget field:** EUR 5,000  
**Requested completion:** 70 days from the test reference date

> Please propose the departmental order-status and reporting rollout for delivery in 70 days. EUR 25,000 has been approved for this exact scope; that is the current implementation budget, not a later phase.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** The message says EUR 25,000 for the current phase while the form says EUR 5,000.  
**What this tests:** Raise a concrete discrepancy instead of choosing the convenient amount.

### EVAL-21 - Whole software product outside the offer

**Company:** Fjord Software (fictional)  
**Current-phase budget field:** EUR 300,000  
**Requested completion:** 120 days from the test reference date

> We have EUR 300,000 approved to build a new commercial SaaS product from scratch, including its own core application and subscription billing. Please quote delivery in 120 days. We are not looking to connect existing office systems or improve an internal workflow.

**Expected outcome:** `COLD`  
**Why:** A new software product is outside this fictional provider service offering.  
**What this tests:** Reject scope mismatch even when the potential contract is large.

### EVAL-22 - On-premises requirement not validated

**Company:** Granite Services (fictional)  
**Current-phase budget field:** EUR 32,000  
**Requested completion:** 90 days from the test reference date

> EUR 32,000 is approved for document routing, approvals and status reporting in 90 days. Please propose the project, but all processing must remain on our isolated network with no external API calls. Our security team has not reviewed any architecture or approved your proposed hosting.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** The hosting restriction needs technical assessment; the demo cannot assume its cloud design is acceptable.  
**What this tests:** Treat material delivery restrictions as review triggers.

### EVAL-23 - Coordinator with an approved sponsor

**Company:** Hazel Manufacturing (fictional)  
**Current-phase budget field:** EUR 24,000  
**Requested completion:** 85 days from the test reference date

> I coordinate the project for our operations director. She has approved EUR 24,000 for automated report collection, validation and exception emails for our department. Delivery is needed in 85 days. Please send the proposal; she will join the scope call and handle contract approval.

**Expected outcome:** `HOT`  
**Why:** A coordinating contact can progress a funded purchase; seniority of the sender is not a gating rule.  
**What this tests:** Do not reject a lead just because the contact is not the final signatory.

### EVAL-24 - Funded project scheduled next year

**Company:** Indigo Trading (fictional)  
**Current-phase budget field:** EUR 35,000  
**Requested completion:** 300 days from the test reference date

> EUR 35,000 is approved for a departmental quotation-follow-up and reporting rollout. We want delivery in 300 days, after our system upgrade. Please provide a proposal, but there is no near-term implementation or accelerated timetable.

**Expected outcome:** `WARM`  
**Why:** The current funding is real as stated, but the requested phase is outside the demo active-sales horizon.  
**What this tests:** Separate genuine intent from near-term priority.

### EVAL-25 - Vague AI request with money attached

**Company:** Jade Commerce (fictional)  
**Current-phase budget field:** EUR 40,000  
**Requested completion:** 90 days from the test reference date

> We have an approved EUR 40,000 digital-improvement envelope and want something useful in 90 days. Please send a proposal for AI that improves everything across our business. We cannot yet name a process, the systems involved or what success would look like.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** A price and date do not establish a defined deliverable. Clarify the current scope before scoring it.  
**What this tests:** Do not invent a project to match an attractive budget.

### EVAL-26 - Free deployment only

**Company:** Kelp Retail (fictional)  
**Current-phase budget field:** EUR 0  
**Requested completion:** 60 days from the test reference date

> We need order intake, dispatch updates and reporting implemented for one department in 60 days. We will not pay for implementation: the total current budget is EUR 0 and there is no later paid commitment. Please provide the complete rollout for free.

**Expected outcome:** `COLD`  
**Why:** An explicitly zero current budget is different from an unknown budget and fails the offer floor.  
**What this tests:** Keep missing and zero funding distinct.

### EVAL-27 - Focused approval-notification pilot

**Company:** Lumen Services (fictional)  
**Current-phase budget field:** EUR 8,000  
**Requested completion:** 40 days from the test reference date

> We have approved EUR 8,000 for one purchase-request notification workflow connecting our existing form system to email for one office team. Please quote the paid pilot for delivery in 40 days. It will not make purchase decisions or place orders automatically.

**Expected outcome:** `HOT`  
**Why:** One bounded workflow, sufficient pilot budget and a concrete paid proposal request.  
**What this tests:** Recognise a safe narrow first phase without inventing extra scope.

### EVAL-28 - Active vendor comparison, no proposal yet

**Company:** Meadow Logistics (fictional)  
**Current-phase budget field:** EUR 25,000  
**Requested completion:** 100 days from the test reference date

> EUR 25,000 is approved for a departmental order-update and reporting project, potentially delivered in 100 days. We are comparing approaches and would like examples of how you work. We are not asking for a paid proposal or choosing a supplier yet.

**Expected outcome:** `WARM`  
**Why:** The contact is comparing approaches, not taking a concrete contracting step.  
**What this tests:** Keep approval and buying intent as separate dimensions.

### EVAL-29 - Support incident and upsell in one message

**Company:** Noble Components (fictional)  
**Current-phase budget field:** EUR 20,000  
**Requested completion:** 80 days from the test reference date

> First, our existing quotation workflow is broken and needs repair under support. Separately, we have approved EUR 20,000 for new order-status workflows delivered in 80 days and want a proposal. Please do not let the expansion request delay the current incident.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** Two work items need different owners: support for the incident and sales for the expansion.  
**What this tests:** Do not bury support inside a promising sales lead.

### EVAL-30 - No approval statement despite a concrete request

**Company:** Orchard Supply (fictional)  
**Current-phase budget field:** EUR 27,000  
**Requested completion:** 75 days from the test reference date

> We need automatic collection of order information, customer updates and exception reporting for our service department. The budget field is EUR 27,000 and our target is delivery in 75 days. Please send a proposal. I have not provided any information about funding approval or who can authorise this phase.

**Expected outcome:** `NEEDS_REVIEW`  
**Why:** An amount and proposal request do not establish authorisation; ask for the missing readiness fact.  
**What this tests:** Avoid interpreting a number as approved purchasing power.

## Technical tests

These are implementation requirements. They have not been run against the target n8n instance. Offline assertions in the package cover only selected rule/schema behaviours.

### TECH-01 - Double submission

**Test:** Send the same authenticated request twice with one idempotency key and identical content.

**Expected:** One lead record and no duplicate notification; return the prior recorded result without another JEV call.

**Type:** Workflow integration

### TECH-02 - Reused key, changed request

**Test:** Reuse an idempotency key while changing the current budget.

**Expected:** Return an explicit conflict; do not overwrite the original lead or recycle its score.

**Type:** Workflow integration

### TECH-03 - Lost response after save

**Test:** Simulate the client losing the response after the lead is saved, then retry.

**Expected:** Find the stored record and return it. Do not re-evaluate the lead or send Slack twice.

**Type:** Fault injection

### TECH-04 - JEV is unavailable

**Test:** Simulate timeout and 503 in the private provider adapter.

**Expected:** At most one bounded retry when appropriate; record a technical review, not a HOT result and not silent mock fallback. Count every attempt.

**Type:** Fault injection

### TECH-05 - Invalid provider authentication

**Test:** Simulate 401 or 403.

**Expected:** No repeated chargeable retries; keep the integration unverified and report the authentication failure without logging the key.

**Type:** Fault injection

### TECH-06 - Malformed typed answer

**Test:** Supply missing question answers, impossible score ranges, NaN, unknown choices and invalid probability maps.

**Expected:** NEEDS_REVIEW for a model/schema error with no displayed score. Schema errors never count as correct semantic decisions.

**Type:** Unit and workflow integration

### TECH-07 - Google Sheets write failure

**Test:** Simulate a failed lead write after successful qualification.

**Expected:** Do not claim the lead was saved and do not send a success notification. Preserve retry context without re-calling JEV where supported.

**Type:** Fault injection

### TECH-08 - Slack delivery status unknown

**Test:** Simulate a timeout after a Slack send may already have been accepted.

**Expected:** Record UNKNOWN; do not blindly resend. A Slack failure never changes the commercial category.

**Type:** Fault injection

### TECH-09 - Spreadsheet and message injection

**Test:** Use an otherwise valid message beginning with = and containing <script> and Slack mention syntax.

**Expected:** Keep text inert in Sheets and UI, escape Slack text and suppress channel mentions. Do not open links or execute formulas.

**Type:** Unit and workflow integration

### TECH-10 - Customer attempts to change configuration

**Test:** Submit model, policy, run_mode, slack_url, expected_route or budget_limit as extra API fields; also test an instruction override in message text.

**Expected:** Reject unauthorised control fields. The message cannot change credentials, limits or destinations even if the model misses an attack flag.

**Type:** Security boundary test

### TECH-11 - Unknown, zero and invalid budget

**Test:** Test null, 0, -1, true, NaN and ambiguous formatted amounts.

**Expected:** Unknown remains unknown; zero is a real amount; invalid types and negative values are rejected before JEV. Never silently convert currency.

**Type:** Unit and workflow integration

### TECH-12 - Phase-specific price boundaries

**Test:** For each supported phase use floor minus EUR 0.01, exact floor and 1.5 times floor.

**Expected:** Use the actual current phase. EUR 5,000 can qualify a pilot but not a rollout; never adjust the phase to fit the price.

**Type:** Unit test

### TECH-13 - Delivery-date boundaries

**Test:** Test one day below the phase minimum, exactly the minimum, 180 and 181 days; also a past or invalid date.

**Expected:** Too-short valid dates require review; invalid dates fail validation; 181 days is future planning. Use the trusted reference date.

**Type:** Unit test

### TECH-14 - Uncertain categorical decision

**Test:** Provide well-formed choice distributions just below 0.75 probability or below the 0.20 margin.

**Expected:** Apply review thresholds to relevant sales decisions. Do not sell these initial thresholds as calibrated confidence.

**Type:** Unit test

### TECH-15 - Company size and role do not buy priority

**Test:** Change only the company-size field and contact title while keeping the message and model answers identical.

**Expected:** Fixed-policy score and route remain identical; the state allowlist excludes these fields. This is not evidence of live-model invariance.

**Type:** Unit test

### TECH-16 - Mixed support and expansion

**Test:** Run a message asking both to repair a live incident and propose a new purchase.

**Expected:** NEEDS_REVIEW with support_and_sales ownership; preserve the incident rather than bury it in a HOT sales message.

**Type:** Workflow integration

### TECH-17 - Concurrent duplicate requests

**Test:** Launch two identical submissions at the same time in a controlled test.

**Expected:** Record whether duplicate prevention really works. A Sheets lookup-then-append is not a proven atomic guarantee; disclose the boundary or add supported serialisation.

**Type:** Diagnostic integration

### TECH-18 - Cost guard and call cap

**Test:** Simulate a nonzero price with paid budget 0, unknown pricing and the 121st planned call.

**Expected:** Block the external call. Include retries/probes in the 120-call cap; continue offline tasks. No automatic credit purchase.

**Type:** Unit and workflow integration

### TECH-19 - No evaluation-label leakage

**Test:** Inspect a captured outbound model request and hashes of frozen fixtures.

**Expected:** Only allowlisted customer content and trusted business policy are present. No case IDs, titles, expected labels, mock data or contact details.

**Type:** Audit

### TECH-20 - Export and screenshot secret scan

**Test:** Inspect redacted exports recursively, including URLs, pinned data, execution errors and node parameters.

**Expected:** No API keys, JWTs, real Slack webhook paths, authorisation headers or personal account details in sharing assets. Private operational files stay separate.

**Type:** Release check
