# doc-parse crop-cascade register — 08_performance_measure slides 014–026

Lane: doc-parse crop-cascade over the ORIGINAL lecture frames.
Namespace: `videos/machine-learning/08_performance_measure/`
Frames: `unique_slides/slide_0NN.jpg`, all **960×540** (native) — under the
1664×2048 parser ceiling, so **no lane-side downscale was applied** to any frame.
All calls share the configured route (config IS the route; its values were never read or printed).

## Route probe (probe-first gate, binding)

- Probe: `pool_run/docparse/_probe_14_26/` — 480×270 crop of `slide_014.jpg`,
  `--max-output-tokens 600 --timeout 90`.
- Result: exit 0 · `finish_reason=stop` · 187 content chars · 2.6 s · non-degenerate → **probe GREEN**.
- The green probe proves the route was alive in this serving window; it is not a guarantee for heavy calls
  (each heavy call was still checked against its own `finish_reason`).

## Run method

- Full-frame parse first: `parse_document.py <original frame> -o pool_run/docparse/slideNNN/fullframe/`
  at native resolution (explicit `--timeout 150`). Eight slides (014–019, 024, 026) were parsed by this worker
  in a bounded parallel fan (4 in flight, slots refilled): batch wall **8 s** vs ~21 s summed call latency
  ≈ **2.6× measured speedup**, no fidelity loss.
- Then the automated cascade per slide:
  `crop_cascade.py <original frame> --prompt-file references/prompts/crop_decision.md --out pool_run/docparse/slideNNN/`
  with budgets `--max-crops 16 --max-parse-calls 24 --max-depth 6 --max-retries 3 --max-parallel 4
  --parse-timeout 150 --chat-timeout 60`. Cascades were run **sequentially** (one cascade at a time;
  each fans internally at 4) — cross-worker fan-out against the shared upstream was not used.
- Every `.parse.json` was read for `finish_reason` before counting a page done.

## DEGRADED FLAG — chat adjudicator lane down

The chat lane probe fails on every run with `HTTP 404 model_not_found` on the configured chat
model. Per the skill's chat-advisor law the runs completed **degraded**, on deterministic-conservative
CROP decisions, flagged in each `manifest.json` as
`degraded: {chat: true, reason: "chat probe failed — decisions use the deterministic-conservative fallback"}`.
This affects **all 13 slides** (8 run by this worker, 5 validated from sibling-worker runs).
Crop-decision source in the manifests is `fallback`/`deterministic`, never a chat verdict.
Consequence for the build: the transcripts are plain parse data with no LLM adjudication layer behind them.

## Per-slide register

| slide | full-frame | finish_reason | crops | parse calls | composed transcript | truncated / empty regions |
|---|---|---|---|---|---|---|
| 014 | ok | stop | 5 | 6 | `pool_run/docparse/slide014/composed/slide_014_composed.md` | none |
| 015 | ok | stop | 4 | 5 | `pool_run/docparse/slide015/composed/slide_015_composed.md` | none |
| 016 | ok | stop | 3 | 4 | `pool_run/docparse/slide016/composed/slide_016_composed.md` | none |
| 017 | ok | stop | 1 | 2 | `pool_run/docparse/slide017/composed/slide_017_composed.md` | none |
| 018 | ok | stop | 5 | 6 | `pool_run/docparse/slide018/composed/slide_018_composed.md` | none |
| 019 | ok | stop | 2 | 3 | `pool_run/docparse/slide019/composed/slide_019_composed.md` | none |
| 020 | ok | stop | 4 | 5 | `pool_run/docparse/slide020/composed/slide_020_composed.md` | none |
| 021 | ok | stop | 4 | 5 | `pool_run/docparse/slide021/composed/slide_021_composed.md` | none |
| 022 | ok | stop | 2 | 3 | `pool_run/docparse/slide022/composed/slide_022_composed.md` | none |
| 023 | ok | stop | 1 | 2 | `pool_run/docparse/slide023/composed/slide_023_composed.md` | none |
| 024 | ok | stop | 1 | 2 | `pool_run/docparse/slide024/composed/slide_024_composed.md` | none |
| 025 | ok | stop | 2 | 3 | `pool_run/docparse/slide025/composed/slide_025_composed.md` | none |
| 026 | ok | stop | 2 | 3 | `pool_run/docparse/slide026/composed/slide_026_composed.md` | none |

**Done counter: 13/13 slides have a valid transcript. Failed calls: 0.** No call returned a non-`stop`
finish reason and no call returned empty content; every composed transcript's `## Failed calls` section
reads `- (none)`. No crop returned a faithful-empty region shell, so no region was left unread for
structural reasons.

### Provenance of each row

- **014–019, 024, 026 — run by this worker** at the budgets above. Each has the standalone
  full-frame artifact in `slideNNN/fullframe/slide_NNN.parse.{md,json}` plus the cascade's own
  full-frame read in `slideNNN/full/slide_NNN.parse.{md,json}` (the two are byte-equivalent reads).
- **020–023, 025 — banked earlier by sibling workers** (`worker-20-23`, `worker-08-24-27-236944`)
  and **validated, not overwritten**, so no banked evidence was destroyed. Their caps were lower than
  this worker's spec (020–023: 12 crops / 18 calls / parallel 2; 025: 10 crops / 14 calls) and they
  carry no standalone `fullframe/` artifact — the cascade's `full/` read is their full-frame parse.
  Health was confirmed per-call: every `.parse.json` is `finish_reason=stop` with non-empty content,
  and every composed file exists with `- (none)` under `## Failed calls`.

### Slide content carried by the transcripts (for the build's verbatim-text check)

- 014 — "Combine Precision and Recall in one number" (lollipop chart; Positive/Negative, TN/FP/TP/FN).
- 015 — "Required to PENALIZE small values of Precision and Recall" (line chart, x/y table).
- 016 — "Combine Precision and Recall in one number" (lollipop chart; TP/FN/TN/FP grid).
- 017 — "F-Score for different Precision and Recall values" (multi-line chart; full precision×recall→F1 table).
- 018 — "Precision and Recall of Multi-class classification" (ranked table; columns incl. Docg/Cat/Fish rows).
- 019 — "Training Samples with Labels (Two Classes)" (perceptron diagram; activation function, threshold, labels).
- 020 — "Training Samples with Labels (Two Classes)" (diagram-as-chart; initial sample, model, LOSS, evaluation).
- 021–026 — "Effect of Selecting Threshold Value on Model Performance" (confusion-matrix flows;
  Predicted-as P/N × Actual P/N, TP/FN/FP/TN).

### Stop reasons reached (deterministic tiers; chat lane was unavailable)

`no-new-information` (child read added nothing over its parent), `too-small` (slide 017 — chart region
already too small at source scale for a further crop), and `no-internal-structure`/`leaf` on simple
regions. `backstop` was never reached; no slide exhausted its 16-crop / 24-call budget.
