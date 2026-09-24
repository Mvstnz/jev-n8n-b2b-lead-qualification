# Local release guard

`release_guard.py` checks a candidate public tree for the supplied private values
and common encodings, selected token patterns, forbidden files and unreviewed media.
It prints finding names/paths, not matching secret contents. It also checks staged
blobs and reachable Git history when `--git-history` is passed. Run it BEFORE a
public connector write/commit/push, not just after uploading.

From the private outer workspace:

```sh
python project/tools/test_release_guard.py
python project/tools/release_guard.py --root project --credentials PRIVATE_CREDENTIALS.txt --require-credentials
```

After initialising Git ONLY in project/ and staging reviewed files:

```sh
python project/tools/release_guard.py --root project --credentials PRIVATE_CREDENTIALS.txt --require-credentials --git-history
```

From a public clone without private access, pattern-only checks can run with
`python tools/release_guard.py --root .`. Do not place actual secrets in CI just
to enable the optional exact-value comparison.

## Screenshots

The tool cannot inspect text in pixels. After ACTUAL visual review and redaction,
record the final file hash in `checks/media_review.json`:

```json
{
  "files": {
    "assets/screenshots/workflow.png": {
      "sha256": "REPLACE_WITH_SHA256_OF_VISUALLY_REVIEWED_FILE",
      "reviewed_for_secrets": true,
      "reviewer": "REPLACE_WITH_ACTUAL_REVIEW_DESCRIPTION"
    }
  }
}
```

This is an example, not an approved screenshot. Do not automatically mark assets
reviewed just to pass the gate. Changing bytes invalidates the recorded review.
Other binary types, archives and unsupported file formats require a separate
review path; do not weaken the guard to silently permit them.

## Limitations

This is a supplementary scanner, not a complete DLP system or proof of safety.
It does not recognise every credential format, split/obfuscated secret, private
identifier or personal data. It does not inspect pixels and excludes local tool
caches. Review the exact staged/plugin-upload file list and actual public content.
Never bypass GitHub push protection. A .gitignore rule does not remove tracked
files or a secret from old commits.
