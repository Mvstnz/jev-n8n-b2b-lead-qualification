# Demo and LinkedIn package

## The story in one sentence

JEV interprets a synthetic B2B request; fixed rules choose Sales, human review or Support; Google Sheets records the reason; a separately approved n8n sender explains saved decisions in a private Slack channel.

## Six-slide annotated carousel

The red arrows are annotations over cropped **real application screenshots** captured on 24 September 2026. All companies and requests are fictional. Download these PNGs in order:

1. [The n8n intake](../assets/linkedin/01-workflow-overview.png): form, duplicate check, JEV, Sheets and a Slack text preview.
2. [Where JEV runs](../assets/linkedin/02-jev-and-rules.png): a native Vercel AI Gateway request inside the Evaluation Core, then answer validation and fixed policy.
3. [The native Slack step](../assets/linkedin/03-native-slack-step.png): a separate inactive sender reads Sheets, formats five cases, holds a closed approval gate and has a connected n8n Slack node. Its OAuth channel access passed a **read-only** test. The six delivered messages pictured later used the earlier approved private webhook path; native posting has not been send-tested.
4. [The saved results](../assets/linkedin/04-sheets-results.png): five synthetic live JEV intake rows; two sales scores, two review cases and one support case.
5. [A small pilot in Slack](../assets/linkedin/05-slack-sales-cases.png): Beacon Services, a customer-reported approved EUR 6,000 pilot, receives a Sales follow-up with 93.02/100 business priority.
6. [Review and Support in Slack](../assets/linkedin/06-slack-review-support.png): a EUR 120,000 multi-country request remains unscored because its scope is uncertain; an existing-customer incident goes to Support.

The original redacted evidence crops are in [assets/screenshots](../assets/screenshots/). The arrows and captions were added for explanation; no application UI or decision result was invented. The final images are visually reviewed and hashed in `checks/media_review.json`.

## What actually ran

- Five distinct synthetic enquiries completed the inactive n8n form → live `typesafe-ai/jev` through Vercel AI Gateway → fixed rules → Google Sheets append → Slack preview path. Four of the five final routes matched the authored case expectations. Two serial duplicate replays returned stored receipts without additional writes.
- The final **six-message** Slack showcase read all five saved live JEV rows and produced five case messages plus a recap. A closed-gate preview sent zero messages. After the explicit send approval, one private webhook execution delivered six messages, the Slack channel was read back, and the gate was closed again. The intake itself did not send Slack messages.
- An earlier six-message MOCK policy batch used hand-authored typed answers. An intermediate four-message LIVE JEV narrative was sent before the user requested shorter, clearer business-case text. These are separate runs.
- The native n8n Slack node and connected OAuth credential are present on the current sender canvas. A temporary read-only `get channel` operation succeeded, then the node was restored to `post message` and the gate to closed. **No native-node message send is claimed.**
- The broader live evaluation planned 90 slots. Provider limits and errors left 28 valid typed replies; 23 of those 28 matched authored routes, with zero false HOT among valid replies. This is a partial test, not a production accuracy estimate.

## Two-minute walkthrough

1. **Business problem:** Inbound requests mix potential purchases, early ideas, unclear rollouts and existing-customer incidents. Budget alone does not tell the team what to do next.
2. **JEV's role:** The intake sends allowlisted facts about the *current requested work* to nine typed JEV questions. They cover request type, current scope, service fit, buying intent, funding readiness, delivery risk, contradictions, instruction attacks and genuine ambiguity.
3. **Where human judgment and rules enter:** Code validates JEV's response shape and confidence, then applies explicit gates. Unclear or complex scope goes to human review. Existing-contract incidents go to Support. Qualified sales cases alone receive a business-priority score. That number is **not** a purchase probability.
4. **Business contrast:** Beacon's narrow EUR 6,000 pilot receives Sales follow-up. Grove's customer-stated EUR 120,000 nine-office rollout needs scope clarification before any sales score. Ivy's broken order notification is a Support issue.
5. **Delivery:** Google Sheets stores each synthetic result. The intake only prepares Slack text. A separate, manually approved sender posts selected saved results to a private channel and closes again.

`Current paid phase` means the work and budget requested **now**, such as a pilot rather than a hypothetical later company-wide rollout. Customer-reported approval has not been independently verified. The business thresholds are fictional demo policy, not market prices or delivery commitments.

## Copy-ready LinkedIn post (English)

> **The EUR 120,000 request got no score. The EUR 6,000 pilot went to Sales.**
>
> I built this B2B lead qualification demo to answer a simple question: **Who should handle an enquiry next, and why?**
>
> The n8n flow is: **enquiry → JEV through Vercel AI Gateway → explicit business rules → Google Sheets → approved Slack notification.**
>
> JEV interprets the work requested *now* through nine structured questions. Is it a new purchase or an existing service issue? A narrow pilot or a multi-country rollout? Is funding for this exact phase reported as approved? Code validates the answers; fixed rules choose the next team and decide whether a priority score is appropriate.
>
> Three synthetic cases show why that split matters:
> - A EUR 6,000 pilot with customer-reported funding approval → personal Sales follow-up, priority 93.02/100.
> - A EUR 120,000 rollout across nine offices → human scope review, **no score yet**.
> - A broken workflow under an existing service agreement → Support, **not a sales lead**.
>
> I ran five fictional enquiries through the connected n8n/JEV/Sheets path. A separate, approval-gated n8n sender delivered five readable case summaries and a recap to a private Slack demo channel. The intake itself stays preview-only, and the workflow remains inactive.
>
> The screenshots are from the real tools; the lead data is synthetic. The score is a business priority, not a prediction that someone will buy. The tests, partial live evaluation and remaining operational limits are documented here: https://github.com/Mvstnz/jev-n8n-b2b-lead-qualification
>
> #n8n #JEV #AIAutomation #BusinessAutomation #RevOps

Post this personally after checking the carousel order and wording. No LinkedIn publishing or customer communication was automated. The private Slack webhook and operational IDs are intentionally absent from the public repository.
