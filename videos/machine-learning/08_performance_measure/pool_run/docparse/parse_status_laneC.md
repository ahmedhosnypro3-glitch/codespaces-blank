# doc-parse crop-cascade register — lane C, 08_performance_measure slides 020–028

Date: 2026-10-31. Namespace: `videos/machine-learning/08_performance_measure/`.
Mandate: namespace AGENTS.md "Doc-parse crop-cascade mandate (dense slides)" — ROC /
threshold / sigmoid slides are dense math+diagram frames. Parsed markdown is DATA for
verbatim-text checks; it never overrides the house frame rule.

## Route probe (probe-first gate)

- Probe: `pool_run/docparse/_probe_laneC/out/` — 480×270 crop of `slide_020.jpg`,
  `--max-output-tokens 600 --timeout 90`.
- Result: exit 0 · `finish_reason=stop` · 234 content chars · 0.7 s · non-degenerate → GREEN.
- Route (config IS the route; values never read/printed): parse = nemotron-3.5-parse
  (NVIDIA-direct), chat adjudicator = docparsechat via localhost:17844.

## Run method

- Driver: `pool_run/docparse/_laneC_driver.sh` (bg task, log `_laneC_run.log`).
- Per slide: `crop_cascade.py unique_slides/slide_0NN*.jpg
  --prompt-file ~/.agents/skills/doc-parse/references/prompts/crop_decision.md
  --out pool_run/docparse/slide0NN/ --max-crops 16 --max-parse-calls 24 --max-depth 6
  --max-retries 6 --max-parallel 2 --parse-timeout 150 --chat-timeout 60`.
- One cascade at a time, 60–90 s pacing between slides, ≤2 concurrent parse calls
  (script-internal pool). Wrapper retried failed runs up to 6× with 120–300 s sleeps —
  no wrapper-level retry was needed; every slide passed on attempt 1 (exit 0).
- Frames are 960×540 native, under the 1664×2048 parser ceiling — no downscale applied.
- Pre-existing 2026-10-27 cascade dirs for slide020–028 were moved (not deleted) to
  `pool_run/docparse/_archive/laneC_20261031/` before the fresh runs.

## Per-slide status

| slide | source frame | exit | parse calls | crops | non-stop/empty parses | chat degraded | composed transcript |
|---|---|---|---|---|---|---|---|
| 020 | slide_020.jpg | 0 | 2 | 1 | 0 | no | composed/slide_020_composed.md |
| 021 | slide_021.jpg | 0 | 5 | 4 | 0 | yes (chat probe failed → deterministic-conservative decisions, flagged in manifest) | composed/slide_021_composed.md |
| 022 | slide_022.jpg | 0 | 3 | 2 | 0 | no | composed/slide_022_composed.md |
| 023 | slide_023.jpg | 0 | 2 | 1 | 0 | no | composed/slide_023_composed.md |
| 024 | slide_024.jpg | 0 | 2 | 1 | 0 | no | composed/slide_024_composed.md |
| 025 | slide_025.jpg | 0 | 1 | 0 | 0 | no | composed/slide_025_composed.md |
| 026 | slide_026.jpg | 0 | 1 | 0 | 0 | no | composed/slide_026_composed.md |
| 027 | slide_027.jpg | 0 | 1 | 0 | 0 | no | composed/slide_027_composed.md |
| 028 | slide_028-.jpg | 0 | 4 | 3 | 0 | no | composed/slide_028-_composed.md |

Budgets: caps 16 crops / 24 parse calls per slide; spent ≤5 calls and ≤4 crops each.
Every `.parse.json` was read: all `finish_reason=stop`, non-empty content. Done counter:
9/9 slides have a valid composed transcript. Failed calls: 0. No wrapper retries fired.

Not touched: `recreated_pptx/`, `mission.db` / `slides_progress.db`.
