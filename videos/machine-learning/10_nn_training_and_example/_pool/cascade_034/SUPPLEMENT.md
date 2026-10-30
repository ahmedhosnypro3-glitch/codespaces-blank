# scope_d2 doc-parse supplement — slides 24–34

Lane: doc-parse (advisory). Partition D2 = slides 24,25,26,27,28,29,30,31,32,33,34.
All final transcripts: `analysis/parse/slide_NNN.parse.md` + `.parse.json`.

## Fresh parses (parse_document.py, --timeout 180, bounded 4-way fan)

| slide | exit | out_tokens | md_chars | finish_reason |
|---|---|---|---|---|
| 024 | 0 | 243 | 1358 | stop |
| 025 | 0 | 415 | 1018 | stop |
| 026 | 0 | 47 | 284 | stop |
| 027 | 0 | 363 | 464 | stop |
| 028 | 0 | 481 | 598 | stop |
| 029 | 0 | 139 | 455 | stop |
| 030 | 0 | 540 | 656 | stop |
| 033 | 0 | 291 | 754 | stop |
| 034 | 0 | 199 | 412 | stop |

## Repaired outputs (no re-parse, no overwrite)

A prior worker had passed the output dir as `analysis/parse/slide_031.parse.md`
and `analysis/parse/slide_032.parse.md`, so the pairs landed one level down. The
inner pairs were promoted to the canonical paths and verified:
`finish_reason=stop`, `.parse.md` bytes == the json `content` field. The empty
stray directories were removed; no transcript was modified or deleted.

| slide | finish_reason | out_tokens | md_chars |
|---|---|---|---|
| 031 | stop | 123 | 193 |
| 032 | stop | 260 | 708 |

## Dense-content cross-check vs analysis finals

Cross-checked with `analysis/slide_0NN_final.json` verbatim_text (slides 24, 25, 34
have finals; 28 has a raw analysis used instead).

| slide | verdict |
|---|---|
| 024 | complete — every bullet and label present |
| 027, 029, 030, 032, 033 | complete — dense formula/chart slides fully captured |
| 026 | complete — sparse slide, all visible text captured |
| 028 | omitted the top-left red-bordered formula box (δ_j, Δ_ji) — escalated |
| 025 | omitted the diagram labels (Class 1/2/m, Error, Output 1/2/m) and the chart titles/captions ("Exploding Gradients", "Sigmoid vs Tanh", axis ticks) — escalated |
| 034 | omitted the entire top band: "Forward Calculations" title plus the network diagram — escalated |

## Crop cascade runs

`crop_cascade.py` (max-crops 16, max-parse-calls 24, max-depth 6, parse-timeout 180)
for the three escalated pages. The chat lane was degraded on every run — the
`docparsechat` model answers HTTP 404 `model_not_found` on
`http://17844/v1/chat/completions` — so decisions ran on the
deterministic-conservative tiers (no CROP-vs-STOP adjudication available).

| run dir | crops | parse calls | elements | outcome |
|---|---|---|---|---|
| `_pool/cascade_025` | 8 | 9 | 22 | recovered Class 1/2/m, "Error Error Error", "Exploding Gradients", "Sigmoid vs Tanh", axis ticks (-10,-5,0,5,10) |
| `_pool/cascade_028` | 2 | 3 | 2 | recovered δ_j / Δ_ji box plus δ6, δ7 and the W6/W7 rows the full read dropped |
| `_pool/cascade_034` | 0 | 1 | 1 | stopped at root (`too-small`): the full read classed the whole 960x540 frame as one `<class_Chart>`, so no region was cut |

## Slide 34 — manual region reads (chat-lane substitute)

The cascade's deterministic fallback could not crop slide 34, so four regions were
cut directly (PIL, no scaling — crops read at their own native pixels) and parsed
one call each into `_pool/cascade_034/manual_crops/`. Transform: scale 1.0, so
crop pixels == frame pixels; boxes are `(x0, y0, x1, y1)` of `slide_034.jpg`
(960x540). All reads `finish_reason=stop`.

| crop file | frame box | recovered content |
|---|---|---|
| s34_diag_out.png | 660,25 → 905,235 | "34" badge, "Output", "Target", node 6 / O 0 / t₆, node 7 / O 1 / t₇, η= 5 |
| s34_diag_in.png | 320,20 → 680,180 | "Input", x₁ (1), x₂ (5), node 3, edge weights 0.1 / 0.5 / 0.1, "Bias" |
| s34_title4.png | 0,0 → 190,200 | title box: "Forwa[rward] [Calcu]lator[s]" — the box sits at x<190, so the 20px cut clips the right edge |
| s34_diag_full.png | 230,12 → 900,235 | "Input 0.1 / Output 0.2 / Target 0.3 / Bias 0.4 / Bias 0.5", η=5 |

Reads that returned only a bare `<class_Picture>` with no text (no usable
transcript, not failures): s34_title, s34_title2, s34_title3, s34_diag_mid,
s34_diagram. Remaining unread on slide 34: the small numeric weight labels on the
diagram edges — the vision analysis records them as "[?] / values not captured"
too, and the source is 960x540, so the parse lane cannot do better without an
upscale (which the lane forbids).

## Storm / reliability log

No timeouts, 502s or 504s occurred. Incident: the crop cascade runs printed
`chat lane probe failed — HTTP 404 model_not_found` and continued degraded;
this is an operator config matter for the chat model (never touched by this
lane) and does not affect the parse reads, all of which succeeded.
