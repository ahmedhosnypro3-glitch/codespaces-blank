# Worker report — slide 008 "[1] Ridge Regularizer to Minimize Overfitting"

Deck: `machine-learning/03_ridger_regression_gradient_descent`
Worker: `worker-008-pickup`
Date: 2026-10-23

## Deliverable

- `recreated_pptx/slide_008_recreated.pptx` — single plain-named version (no suffix).
- Build script: `recreated_pptx/build/slide_008.js` (pre-existing, measured geometry).
- Render: `recreated_pptx/qa/slide008/render_1.png` — 2000×1125 px = exactly 150 dpi
  for a 13.333×7.5 in slide (native LibreOffice PNG export at
  `PixelWidth=2000 / PixelHeight=1125`, no upscale resampling).

## Content

The original frame is a **title-only slide**: a red bold title and a blue
bold-italic subtitle, plus the house badge. No bullets, equations, imagery,
tables, or charts (confirmed against `analysis/slide_008_final.json`:
`verbatim_text.bullets`, `.equations`, `imagery` all empty; the recreation brief
explicitly excludes the white mouse-pointer as a video-capture artifact).

- Title: `[1] Ridge Regularizer to Minimize Overfitting`, Arial bold 34 pt, C00000.
- Subtitle: `(Also Known as L2 regularizer)`, Arial bold-italic 27.75 pt, 0000CC.
- No equation media in the pptx, therefore no `eq_*.json` sidecars — the
  matplotlib-mathtext rule applies only to slides that actually carry equations.
- No graph/curve assets — this slide has no plots, so the smooth-curve /
  analytic-curve rule does not apply here.

## House chrome (per deck AGENTS.md, verified by the checker)

`shared_patterns/house_chrome_check.py render_1.png 8` → **PASS**:
panel x 112–1882 render-px (=54–903 frame px), y 94–bottom (=45–540), strokes
L/R/bottom present, **top bare**, badge center (1825,152) d=69 render-px
(=(876,73) d≈35 frame px). All within tolerance 8 render-px.

## Pre-judge self-check (`selfcheck_attempt_2.py`)

Closed-loop pixel comparison of the 150 dpi render against
`unique_slides/slide_008.jpg` (chrome excluded, frame-px coordinates):

| band | ORIGINAL | RENDER | Δ |
|---|---|---|---|
| title rows | 231..263 | 232.3..263.5 | ≤ 1.3 px |
| title cols | 107..817 | 107.0..817.0 | 0 px |
| subtitle rows | 302..328 | 302.4..327.4 | ≤ 0.6 px |
| subtitle cols | 261..664 | 260.6..664.8 | ≤ 0.4 px |
| inter-band gap | 39 px | 38.9 px | 0.1 px |

Also verified: 0 red px in the top band (no top stroke), 0 content ink px outside
the panel (frame containment), content ink density ratio 0.891 (JPEG-thin
original — expected).

**SELF-CHECK: ALL PASS**

## Judge legs (protocol `shared_patterns/judge_protocol_03.md`)

### Leg 1 — Template A full-slide comparison

- Probe/retry history: attempts hit the upstream storm (504/502/429 /
  read-timeout / connection errors / HangError) before a valid body opened the
  window. Two hard-wall HangError aborts and one "Response ended prematurely"
  were protocol wall events, not judge attempts.
- Judge: `qa/slide008/judge_attempt_1.txt`
- Result: **FINAL VERDICT: PASS** — "Discrepancies vs. Original: None
  identified." All element-by-element checks (verbatim text, layout, colors,
  missing elements, frame containment, video artifacts) PASS; no visual-quality
  defects.

### Leg 2 — Procedure B zoomed crop-pair certificates

Slide 008 has two dense text regions (two isolated type blocks on an otherwise
empty panel). Both were certified.

Regions (frame px, ~8 px padding):

- `title` — (99, 223, 825, 271): red bold title line.
- `subtitle` — (253, 294, 672, 336): blue bold-italic subtitle line.

Both crops banked under `qa/slide008/` as
`crop_1_<name>_render.png` + `crop_1_<name>_orig.png`. Both images are
**exactly equal in pixel dimensions and effective scale per axis**
(render 2000×1125 = 2.08333 px/frame-px; original crop LANCZOS-upscaled by the
same factor), so no scale-mismatch drift is fabricated:

| region | render crop | orig crop | frame px | effective scale |
|---|---|---|---|---|
| title | 1512×100 | 1512×100 | 726×48 | 2.0826 / 2.0833 |
| subtitle | 873×88 | 873×88 | 419×42 | 2.0835 / 2.0952 |

- `crop_1_title_judge.txt` → **FINAL VERDICT: PASS** — "Discrepancies: none
  found in this region", nothing at BLOCKER/MAJOR/MINOR level.
- `crop_1_subtitle_judge.txt` → **FINAL VERDICT: PASS** — verbatim text
  `(Also Known as L2 regularizer)` matches exactly; no missing/wrong/garbled
  glyphs, "L2" uses the numeral 2 in both, parentheses intact, stroke continuity
  good. The only raised item is a **MINOR "typed strokes heavier than the
  upscaled video capture" note, explicitly "artifact only" / "None" severity** —
  it is a medium difference in the ORIGINAL's capture, not a defect in the
  recreation, and is covered by ground rules (c)/(e). No fix required.

## Certification

Full-slide PASS (Leg 1) + both crop-pair certificates clean (Leg 2) →
`visual_check=PASS`, `visual_transcript=<full-slide transcript path>`,
`gen_status=passed`. No fix/re-render needed.

## Attempt accounting

Per protocol, judge attempts are shared across both legs (6 max per slide, 3
garbage re-invokes, W4 one hard-wall retry). Counting only coherent/failed judge
invocations that produced or attempted a body: the full-slide judge consumed 1
(coherent, PASS), the title crop leg consumed 1 (coherent, PASS), the subtitle
crop leg consumes 1. All well within budget. The remaining dispatches were
upstream wall events (abort/timeout) which the protocol explicitly does not
count as attempts.

## S19 payload-exact confirmation addendum (2026-10-25)

Confirmation crop legs re-ran on the certified deliverable under the
pool-299640 amendment (no rebuild): frozen tplB payload byte-exact (payload
banked as payload_B_N008_confirm.txt, md5 d137335f924c3d7e8ff77bdcc68e8c6e),
PIL-verified matched-scale crop pairs.

- Title crop: crop_1_title_judge_confirm.txt — FINAL VERDICT: PASS + 4 MINORs,
  adjudicated PIL-first in adjudication_title_1_confirm.txt (notably the
  judge's "IMG2 narrower" claim inverted under measurement: render ink w1480
  vs original w1489; remaining MINORs noise-floor/weight class).
- Subtitle crop: crop_1_subtitle_judge_confirm.txt — FINAL VERDICT: PASS,
  zero findings.
- DB: last_error note written; gen_status/visual_check untouched.
- No build, render, or banked evidence was modified.
