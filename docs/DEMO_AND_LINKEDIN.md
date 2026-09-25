# Demo and LinkedIn package

## The story in one sentence

JEV interprets a synthetic B2B request; fixed rules choose Sales, human review or Support; Google Sheets records the reason; a separately approved n8n sender explains saved decisions in a private Slack channel.

## Eight individual, annotated Roboto PNG slides

The red arrows point to cropped **real application screenshots** captured on 24 September 2026. The 1200 × 1500 portrait slides use Roboto for added titles and explanations, preserve the screenshots' aspect ratios and include enlarged decision details. All companies and requests are fictional. Use these PNGs in order:

1. [The business contrast](../assets/linkedin-roboto/01-business-contrast.png): why a smaller, clear pilot can go to Sales while a larger, unclear rollout needs review.
2. [The n8n intake](../assets/linkedin-roboto/02-intake-validation.png): form, validation and duplicate check before JEV runs.
3. [Where JEV runs](../assets/linkedin-roboto/03-jev-and-policy.png): Vercel AI Gateway request inside the Evaluation Core, then answer validation and fixed policy.
4. [The saved results](../assets/linkedin-roboto/04-google-sheets.png): five synthetic live JEV intake rows; two sales scores, two review cases and one support case.
5. [The visible Slack step](../assets/linkedin-roboto/05-slack-workflow.png): a separate inactive sender reads Sheets, formats cases and has a native n8n Slack node behind a closed approval gate. Its OAuth channel access passed a **read-only** test. The six delivered messages pictured next used the earlier approved private webhook path; native posting has not been send-tested.
6. [A small pilot in Slack](../assets/linkedin-roboto/06-slack-sales-message.png): Beacon Services, a customer-reported approved EUR 6,000 pilot, receives a Sales follow-up with 93.02/100 business priority.
7. [An unclear rollout in Slack](../assets/linkedin-roboto/07-slack-review-message.png): a EUR 120,000 nine-office request remains unscored because its scope is uncertain.
8. [A support case in Slack](../assets/linkedin-roboto/08-slack-support-message.png): an existing-customer incident is handled by Support and receives no sales score.

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

JEV was chosen for its [typed decision interface](https://vercel.com/ai-gateway/models/jev): it evaluates a supplied state against focused questions and returns machine-readable choices and uncertainty. [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) is an affordable general-purpose model that also supports structured outputs. Luna was not run on this lead set, so the post explains a workload-fit decision rather than claiming superior accuracy, latency or end-to-end cost.

## Copy-ready LinkedIn post (English)

> Built an AI-assisted B2B Lead Qualification Workflow in n8n 🤖
>
> I've been working on another automation project. This one turns an incoming B2B enquiry into a clear next action for the right internal team.
>
> The workflow handles the process from request to internal notification:
>
> 🔹 Receive and validate an enquiry in n8n
> 🔹 Check for an existing record in Google Sheets
> 🔹 Use JEV through Vercel AI Gateway to understand the work requested **now**
> 🔹 Apply explicit business rules to choose Sales, human review or Support
> 🔹 Save the result and prepare an internal Slack summary
> 🔹 Send selected saved demo results through a separate approval-gated n8n sender
>
> The process is basically:
> **Request → Understand → Check → Route → Store → Notify**
>
> 🛠️ Tech stack:
> • n8n
> • JEV via Vercel AI Gateway
> • Google Sheets
> • Slack
>
> Why JEV instead of a low-cost general model like GPT-6 Luna? Luna can return structured output too. But this step needs nine focused judgements about the current request, not generated sales copy. JEV is built to return typed answers and uncertainty for that kind of decision. My code validates those answers; fixed business rules decide the route and priority. I chose JEV for that fit, not because I proved it more accurate than Luna on these leads.
>
> What I like about this project is that the AI helps **interpret** a messy request, while clear rules decide what happens next. A fictional EUR 6,000 pilot received a Sales follow-up and a 93.02/100 **business-priority** score. A EUR 120,000 nine-office rollout needed human scope review and no score yet. An existing customer issue went to Support.
>
> I tested five synthetic live JEV enquiries through n8n and Sheets, then sent five case summaries plus a recap to a private Slack demo channel after manual approval. Four of the five intake routes matched the predefined expectations. The screenshots show real app screens with fictional companies; this is a portfolio demo, and the workflows remain inactive.
>
> Code, tests and the limits of the live evaluation: https://github.com/Mvstnz/jev-n8n-b2b-lead-qualification
>
> More automation projects coming soon.
>
> #n8n #JEV #AIAutomation #WorkflowAutomation #BusinessAutomation

Post this personally after checking the carousel order and wording. No LinkedIn publishing or customer communication was automated. The private Slack webhook and operational IDs are intentionally absent from the public repository.
