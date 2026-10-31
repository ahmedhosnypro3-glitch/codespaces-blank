# Doc-parse lane STATUS — 08_performance_measure slides 020-028

Lane root: `pool_run/docparse_j/` (isolated; no other lane shares this root).
Parse script: `~/.agents/skills/doc-parse/scripts/parse_document.py` (config resolved by the script itself, never read here).
Full-frame command per slide: `python3 parse_document.py <ns>/unique_slides/slide_NNN.jpg -o pool_run/docparse_j/slideNNN --timeout 300`.
Done criteria: `finish_reason=stop` AND non-empty `content` in the `.parse.json`. Non-stop/empty = failed call, re-run fresh (max 5 attempts, 60s sleep between).
Probe before batch: slide_020, attempt 1, finish=stop, 367 chars, 100 out tokens, exit 0 — PASS.
Run finished: 2026-10-31 ~04:12Z. All 9 full-frame + all 9 cascades green.

## Full-frame parses (pool_run/docparse_j/slideNNN/) — ALL OK, attempt 1, no retries

| Slide | Image file | finish_reason | content chars | out tokens | Transcripts |
|---|---|---|---|---|---|
| 020 | slide_020.jpg | stop | 367 | 100 | slide020/slide_020.parse.{md,json} |
| 021 | slide_021.jpg | stop | 254 | 59 | slide021/slide_021.parse.{md,json} |
| 022 | slide_022.jpg | stop | 258 | 66 | slide022/slide_022.parse.{md,json} |
| 023 | slide_023.jpg | stop | 234 | 58 | slide023/slide_023.parse.{md,json} |
| 024 | slide_024.jpg | stop | 234 | 58 | slide024/slide_024.parse.{md,json} |
| 025 | slide_025.jpg | stop | 234 | 58 | slide025/slide_025.parse.{md,json} |
| 026 | slide_026.jpg | stop | 233 | 58 | slide026/slide_026.parse.{md,json} |
| 027 | slide_027.jpg | stop | 752 | 125 | slide027/slide_027.parse.{md,json} |
| 028 | slide_028-.jpg | stop | 1467 | 257 | slide028/slide_028-.parse.{md,json} |

## Crop cascades (pool_run/docparse_j/cascade_slideNNN/) — dense slides — ALL rc=0

Command: `python3 crop_cascade.py <image> --prompt-file ~/.agents/skills/doc-parse/references/prompts/crop_decision.md --out pool_run/docparse_j/cascade_slideNNN --parse-timeout 300`
Every cascade: manifest.json + prompt_used.md + run.log + composed/<stem>_composed.md present; zero non-stop or empty transcripts among full/ and crops/ parse JSONs.

| Slide | rc | parse_calls | chat_calls | elements | composed bytes | chat degraded | Status |
|---|---|---|---|---|---|---|---|
| 020 | 0 | 3 | 3 | 3 | 1562 | no | OK |
| 021 | 0 | 3 | 3 | 3 | 1303 | no | OK |
| 022 | 0 | 3 | 0 | 2 | 992 | YES (chat probe timed out; deterministic-conservative fallback, flagged in manifest) | OK (degraded) |
| 023 | 0 | 1 | 1 | 1 | 723 | no | OK |
| 024 | 0 | 1 | 1 | 1 | 723 | no | OK |
| 025 | 0 | 3 | 2 | 2 | 1010 | no | OK |
| 026 | 0 | 3 | 2 | 2 | 1045 | no | OK |
| 027 | 0 | 1 | 0 | 7 | 1472 | no | OK |
| 028 | 0 | 4 | 1 | 16 | 2896 | no | OK |

Notes:
- slide_028's source file is `unique_slides/slide_028-.jpg` (dash suffix in the deck's naming); its full-frame transcripts are keyed `slide_028-.parse.*` inside `slide028/`.
- The chat adjudicator lane (localhost gateway) intermittently timed out at 60s during the run; affected cascades completed in the sanctioned degraded/deterministic mode where the probe failed (only slide 022), others recovered on retry.
- Parsed markdown is DATA for verbatim-text checks; it does not override the house frame rule (namespace AGENTS.md).
