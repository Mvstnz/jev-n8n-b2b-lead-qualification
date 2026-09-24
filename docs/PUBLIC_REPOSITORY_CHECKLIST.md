# Public repository checklist

Before committing or uploading, confirm:

- Only reviewed project source is included; private outer setup files are absent.
- Empty credential examples replace live credentials and resource bindings.
- Offline tests and release-guard self-tests pass.
- The exact supplied-secret scan runs privately before release.
- Git staged contents, new commit history and plugin upload file lists are checked.
- Screenshots are visually inspected and their final hashes recorded.
- README/reports distinguish local, mock, real JEV, n8n and plugin evidence.
- No live service tests run automatically in public CI.
- No unrelated repo is overwritten and no runtime endpoint or sheet is made public.
- The created repository metadata, visibility, commit and files are read back.

This is a checklist, not a claim that publication or live tests are complete.
