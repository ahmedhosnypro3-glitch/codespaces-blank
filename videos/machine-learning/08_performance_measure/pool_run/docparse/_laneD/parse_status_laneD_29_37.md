# doc-parse crop-cascade lane D — 08_performance_measure slides 029–037 (2026-10-31)

Namespace: `videos/machine-learning/08_performance_measure/`. Per the namespace AGENTS.md
doc-parse crop-cascade mandate (dense ROC/AUC slides), each ORIGINAL frame
`unique_slides/slide_0NN.jpg` (960×540) got a fresh crop cascade:

```
python3 ~/.agents/skills/doc-parse/scripts/crop_cascade.py unique_slides/slide_0NN.jpg \
  --prompt-file ~/.agents/skills/doc-parse/references/prompts/crop_decision.md \
  --out pool_run/docparse/slide0NN/ \
  --max-crops 16 --max-parse-calls 24 --max-depth 6 --max-retries 6 \
  --max-parallel 2 --parse-timeout 150 --chat-timeout 60
```

Driver: `pool_run/docparse/_laneD/run_laneD.sh` (per-slide logs `_laneD/slide0NN.cascade.log`).
Route probe first: `pool_run/docparse/_probe_laneD/` — 480×270 crop of slide_029, exit 0,
`finish_reason=stop`, 310 chars, 1.8 s → probe GREEN.
Prior 2026-10-30 runs were archived, not deleted: `pool_run/docparse/_archive/slide0NN_laneD_*`.
Pacing laws kept: 60–90 s between slides, max 2 concurrent parse calls, 120–300 s backoff on
timeout/429/5xx (retry ladder up to 6). Parsed markdown is DATA for verbatim-text checks only;
it never overrides the house frame rule. `recreated_pptx/` and `mission.db` untouched.

## Per-slide register (all runs 2026-10-31)

| slide | parse calls | crops | chat-degraded | all parse.json finish=stop, non-empty | composed transcript | notes |
|---|---|---|---|---|---|---|
| 029 | 1 | 0 | no | yes (1/1) | `slide029/composed/slide_029_composed.md` (1197 B) | chat advised STOP at root; full-frame read carried the whole confusion-matrix/ROC table |
| 030 | 1 | 0 | yes (chat probe timed out) | yes (1/1) | `slide030/composed/slide_030_composed.md` (619 B) | DEGENERATE full-frame read (54-char picture-only token, same as archived run); supplemented with manual 1664 px upscale crop parses under `slide030/manual/out/` which recovered the threshold table, TPR/FPR formulas, ROC labels |
| 031 | 5 | 4 | no | yes (5/5) | `slide031/composed/slide_031_composed.md` (1970 B) | thresholds 0.0/0.1/0.3 sweep values captured |
| 032 | 2 | 1 | no | yes (2/2) | `slide032/composed/slide_032_composed.md` (1077 B) | adds Threshold=0.4 row |
| 033 | 4 | 3 | no | yes (4/4) | `slide033/composed/slide_033_composed.md` (1696 B) | adds Threshold=0.6 row |
| 034 | 3 | 2 | no | yes (3/3) | `slide034/composed/slide_034_composed.md` (1590 B) | adds Threshold=0.7 "Best (FPR)" |
| 035 | 4 | 3 | no | yes (4/4) | `slide035/composed/slide_035_composed.md` (2534 B) | adds Threshold=1, FPR=1.0 point |
| 036 | 3 | 2 | no | yes (3/3) | `slide036/composed/slide_036_composed.md` (1534 B) | "The Best (TPR)" annotation |
| 037 | 2 | 1 | no | yes (2/2) | `slide037/composed/slide_037_composed.md` (2158 B) | AUC slide: title "Area Under the Curve (AUC)", chart crop with Best/Worst model callouts |

Done counter: 9/9 slides have a banked cascade run; every `.parse.json` is `finish_reason=stop`
with non-empty content; every composed transcript's `## Failed calls` reads `- (none)`.
Chat adjudicator lane was intermittently timing out during the window (slides 030 degraded;
031/033/035/036 completed with per-node fallback decisions after retries) — flagged per
manifest; parse lane itself had zero failed calls.
