# Official references

Public documentation checked during preparation on **24 September 2026**.
Account access, current plan entitlements and runtime behaviour remain unverified.
Recheck relevant documentation during implementation.

| Topic | Official source |
|---|---|
| Codex project instructions | https://developers.openai.com/codex/guides/agents-md |
| Codex MCP | https://developers.openai.com/codex/mcp |
| Codex plugins | https://developers.openai.com/codex/plugins |
| n8n MCP tools | https://docs.n8n.io/connect/connect-to-n8n-mcp-server/mcp-server-tools-reference |
| Google OAuth in n8n Cloud | https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/ |
| n8n form trigger | https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.formtrigger/ |
| Vercel native JEV evaluation | https://vercel.com/docs/ai-gateway/modalities/evaluation |
| JEV current rate listing | https://vercel.com/ai-gateway/models/jev |
| Slack Incoming Webhooks | https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/ |
| Slack rate limits | https://docs.slack.dev/apis/web-api/rate-limits/ |
| Google Sheets RAW input option | https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueInputOption |
| n8n HTTP credentials | https://docs.n8n.io/integrations/builtin/credentials/httprequest/ |
| GitHub repository creation | https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository |
| Git ignore behaviour | https://docs.github.com/en/get-started/git-basics/ignoring-files |
| Removing sensitive GitHub data | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository |

The checked Vercel listing says Free with promotional pricing ending on
25 September 2026. This is not a guarantee of free requests after that date or
proof of the supplied account's billing. Unknown/positive prices block live
requests with the default zero paid budget, including small probes.

The documented JEV HTTP route is /v1/evaluate, not Chat Completions. Model fields,
response shapes and actual available n8n/plugin actions must still be verified
in the implementing environment. No Codex plugin session is assumed transferable
to n8n, a CLI or another service.
