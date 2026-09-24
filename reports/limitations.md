# Limitations and next gates

1. The deployed mock showcase and intake preview are separate inactive workflows. They do not yet form a persisted JEV-to-Sheets pipeline. The supplied workflow sources are valid for the target n8n SDK, but no credential-bearing raw export is public.
2. The Google Sheets action credential is present but not authorized. The existing trigger credentials are a different type. n8n must complete Google authorization, then write and read a labelled setup row in the private demo sheet before storage can be marked tested.
3. JEV requests are blocked by the zero-paid-budget guard: authenticated model metadata lists a positive input-token price despite the public promotional Free label. No live JEV performance, usage or cost can be claimed.
4. Five MOCK Slack previews exist, but no webhook message was sent. A private sender must be verified after one combined approval for five messages plus one summary.
5. Idempotency, concurrent duplicate prevention, lost-response recovery, Sheets write failure and unknown Slack delivery have not been proven end to end. A Sheets lookup followed by append is not atomic under concurrent requests.
6. The dataset and policy were authored for this fictional portfolio use. Labels are not sales-team validated, scores are not win probabilities, and no real ROI or production readiness is implied.
