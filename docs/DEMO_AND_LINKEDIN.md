# Demo and LinkedIn package

## Evidence boundary

ClearFlow Automation and every lead are fictional. Screenshots are real captures of the n8n, Google Sheets and Slack applications. The five `Leads` rows came from distinct **live JEV** calls through the inactive n8n intake workflow. The six Slack notifications came from a separate, approved **MOCK** showcase using hand-authored answers. No real prospect was contacted. The n8n sender is inactive and its send gate is relocked.

## Suggested post images

1. [Workflow overview](../assets/screenshots/workflow.png): validation, 24-hour duplicate check, JEV evaluation, Sheets storage and Slack preview. The private subworkflow ID was obscured.
2. [Five live synthetic leads](../assets/screenshots/sheets-leads.png): two HOT, two NEEDS_REVIEW and one NOT_A_SALES_LEAD. DEV-03 differed from its authored WARM expectation.
3. [Actual Slack messages](../assets/screenshots/slack-mock-demo.png): approved and delivered MOCK notifications, clearly labelled as such.
4. Optional [evaluation summary](../assets/screenshots/sheets-summary.png): precise result denominators and provider failures.

All four images were cropped, metadata stripped and visually reviewed. The public images contain no credentials, private resource IDs or real lead data. Capture dates and hashes are recorded in `checks/media_review.json`.

## Two-to-three-minute demo script

1. Open the workflow screenshot or the private inactive n8n canvas. Explain: `Enquiry → Validate → De-duplicate → JEV → Policy gates → Sheets → Slack preview`.
2. Show five synthetic rows in Sheets. DEV-01 and DEV-02 are HOT, including a small EUR 6,000 pilot; DEV-07 is flagged for enterprise review; DEV-09 goes to support. DEV-03 is a real disagreement: JEV assessed `paid_discovery`, and the final gate routed to NEEDS_REVIEW instead of the authored WARM expectation.
3. Show the Slack channel. Explain that the six delivered messages are a separate MOCK demonstration of the notification format. Never describe them as messages sent by the live JEV intake.
4. Show the summary: 28 of 90 planned evaluation attempts returned valid typed results, 23 of those 28 matched authored routes, and there were no false HOT classifications. The other 62 attempts failed at the provider boundary. This does not establish full-set quality or stability.
5. Close with the production gates: migrate the private inline gateway key into an n8n credential, make duplicate handling atomic, add partial-failure recovery and re-run provider-limited cases before activating the workflow.

## Copy-ready LinkedIn post (English)

> I built an AI-powered B2B lead qualification workflow with n8n and JEV. 🔧
>
> The goal: turn a new enquiry into a useful next action, instead of treating a big budget or an urgent message as an automatic sales opportunity.
>
> The flow is simple: **Enquiry → Validate → Check duplicates → Ask JEV → Apply business gates → Save to Sheets → Prepare a Slack notification.**
>
> It asks nine structured questions about the *current paid phase*. Fixed rules then decide whether to follow up, help with funding approval, request a feasibility review, or route an existing customer to support. The score appears only when the gates pass.
>
> I ran five synthetic enquiries through the connected n8n → JEV → Google Sheets path. Two became HOT, two needed review, and one went to support. One case disagreed with my authored expected route; I kept that result visible. I also sent six clearly labelled MOCK messages to a private Slack demo channel to show the notification experience.
>
> In a separate 30-case evaluation, 23 of 28 valid responses matched my authored routes and none produced a false HOT. Provider limits blocked the other 62 planned attempts, so this remains a portfolio demo rather than a production claim.
>
> The workflow, tests, limitations and real screenshots are on GitHub: https://github.com/Mvstnz/jev-n8n-b2b-lead-qualification
>
> #n8n #AIAutomation #JEV #BusinessAutomation #RevOps

The user publishes this post personally. Do not publish, schedule, or send it automatically. If the user posts fewer than four images, use the first three and retain the MOCK/LIVE distinction in the caption.
