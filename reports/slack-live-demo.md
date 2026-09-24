# Slack showcase from saved LIVE JEV results

On 24 September 2026, five fictional enquiries had been evaluated through the inactive n8n intake, live `typesafe-ai/jev` via Vercel AI Gateway, fixed rules and Google Sheets. A **separate manual n8n sender** read the five saved rows, checked their `LIVE JEV` provenance, formatted five concise business cases and a recap, and produced a zero-send preview with its Slack approval gate closed. Following explicit send approval, one execution delivered exactly six messages through a **private Slack Incoming Webhook**. The n8n execution reported six successful send items; a separate channel read-back confirmed the six messages. The gate was immediately relocked and the sender remains inactive.

| Synthetic case | Saved decision | Plain-English Slack message |
|---|---|---|
| Alder Manufacturing: EUR 30,000 department reporting | HOT, priority 97.8/100 | Current request, customer-reported funding, recommended Sales follow-up and next action. |
| Beacon Services: EUR 6,000 one-team CRM reminder pilot | HOT, priority 93.02/100 | A narrow pilot is qualified by fixed budget, fit and timing rules; Sales confirms scope and quote. |
| Cedar Distribution: EUR 40,000 estimate with approval pending | NEEDS_REVIEW, not scored | JEV could not classify the exact paid scope confidently; a person clarifies scope and funding. |
| Grove Industrial Group: EUR 120,000 nine-office quotation approvals | NEEDS_REVIEW, not scored | The exact scope is uncertain; Sales review and a solution specialist check deliverables before a quote. The larger stated budget does not override the review gate. |
| Ivy Parts: broken existing order notification under service agreement | NOT_A_SALES_LEAD, not scored | The issue belongs to Support; it is not discarded. |

The recap counted **Sales follow-up 2, human review 2, Support 1**, and said explicitly that only the two Sales cases receive business-priority scores. “Not scored” is intentional for review and support routes, not a missing value. The [pilot screenshot](../assets/screenshots/slack-live-hot.png), [review and support screenshot](../assets/screenshots/slack-live-review.png), [recap screenshot](../assets/screenshots/slack-live-recap.png), and [annotated carousel](../assets/linkedin/) show the real private Slack UI with synthetic data. A customer statement that budget was approved was not independently verified; no customer was contacted.

The current sender canvas has a connected native n8n Slack node after the approval gate. Its OAuth credential passed a **read-only channel lookup** in a temporary test configuration. The send operation and closed gate were restored afterwards. That native node has **not** posted a message. The six messages above came from the earlier webhook delivery path, as the n8n execution and Slack read-back show. This distinction matters when interpreting the native-node screenshot.

An earlier [six-message MOCK policy batch](slack-previews.md) used hand-authored typed answers, not live model output. An intermediate four-message narrative based on three saved live JEV cases was also delivered before the user requested the clearer five-case format. Neither batch was sent automatically by the intake. Private webhook, channel, Sheet and execution identifiers are omitted from this public report.
