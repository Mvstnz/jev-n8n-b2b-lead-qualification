# n8n workflow sources

`mock-showcase.sdk.js` and `intake-preview.sdk.js` are portable n8n Workflow SDK source, built by the scripts in `tools/`. They contain no runtime credential IDs or secrets. On the target n8n instance (24 September 2026), both passed MCP validation and were created as **inactive** workflows.

The mock showcase was executed manually. It processed DEV-01, DEV-02, DEV-03, DEV-07 and DEV-09 with hand-authored typed answers and produced five `PREVIEW_ONLY` Slack texts. It makes no HTTP, Sheets or Slack requests. The intake preview uses n8n user authentication and rejects unauthorized fields and malformed form values. One valid synthetic form-trigger execution succeeded. It does not yet invoke JEV or save a lead.

These sources are not raw n8n exports and cannot alone demonstrate a completed end-to-end pipeline. The operational workflow IDs and links are intentionally kept out of the public repository. The separate Python [native HTTP adapter](../reference/jev_adapter.py) is offline tested but is not wired into the n8n workflows. The Google Sheets action OAuth credential still needs its Google authorization step; JEV runtime credential binding and the account pricing decision remain open. See `reports/integration-tests.md`.
