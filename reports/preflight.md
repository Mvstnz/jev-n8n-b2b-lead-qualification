# Preflight (redacted)

Checked 24 September 2026. The supplied n8n Streamable HTTP MCP endpoint responded to `initialize` and `tools/list`. The server reported protocol `2025-03-26` and exposed workflow search, SDK reference/schema lookup, validation, creation, execution, update, publish/unpublish and credential listing. The instance UI reported n8n 2.41.2. The two new demo workflows are inactive; no public trigger was enabled.

Credential listing found four `googleSheetsTriggerOAuth2Api` entries and no `googleSheetsOAuth2Api` action credential at discovery time. An action credential was subsequently created in n8n UI but remains **Needs first setup** because Google authorization did not complete. No Vercel AI Gateway runtime credential was verified. The Codex Google connector successfully created one native private sheet and read its Summary tab; that is not an n8n write/read test. GitHub plugin identity resolved a personal account; local `gh` authentication was separately verified. The Slack webhook is present privately but has not been called.

The public JEV page displays “Free” with a promotion ending 25 September 2026, while the authenticated AI Gateway model catalogue returned input pricing `0.000000042 USD/token` and output pricing `0`. The account-applicable bill for a JEV request has therefore not been established as zero. With paid budget USD 0, live attempts remain blocked. The planned campaign is 90 evaluation calls plus development, smoke, showcase and retries, capped at 120 total attempts. No model attempt has been made.

Private operational URLs, account details, credential IDs and raw replies are not included here.
