# Screenshots: real evidence only

The PNGs here are real UI captures from 24 September 2026. `workflow-explained.png` shows
the inactive n8n intake with a labelled JEV step, Sheets append and Slack
preview; its private subworkflow ID is obscured. `jev-core.png` shows the
actual JEV Gateway request within the Evaluation Core. `slack-sender.png`
shows the separate Sheets-backed sender, closed approval gate and native Slack
node. The connected native Slack credential passed a read-only channel check;
the pictured delivered messages used the earlier private webhook path.
`sheets-leads.png` shows five synthetic live JEV intake rows,
and `sheets-summary.png` shows their summary and separate evaluation.
`slack-live-hot.png`, `slack-live-review.png` and `slack-live-recap.png` show
the delivered five-case-plus-recap showcase based on saved live JEV decisions.
The older
`slack-mock-demo.png` shows a different, clearly labelled MOCK policy batch.

The final images were cropped, visually reviewed, converted to metadata-free RGB
PNGs and hashed in `checks/media_review.json`. The release scanner verifies those
hashes, not pixels. Do not add fabricated evidence, account details, browser
runtime URLs, secrets or the private setup ZIP. The red-arrow versions for
LinkedIn are in `assets/linkedin-roboto/`; earlier sets remain in `assets/linkedin-v2/` and `assets/linkedin/`. See `tools/README.md`.
