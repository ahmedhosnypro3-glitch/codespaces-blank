# Worker report — slide 039 (deck 03: machine-learning/03_ridger_regression_gradient_descent)

Slide title: "Gradient Descent (GD) – Stochastic Gradient Descent SGD) and Mini-Batch
Gradient Descent" (the unbalanced `SGD)` is the ORIGINAL's own typo, reproduced
verbatim per the output contract).
Worker: `slide039-worker`
Dependency: none (root slide; not in any pattern group).

## Deliverable

`recreated_pptx/slide_039_recreated.pptx` — single plain-named version (law), built by
`recreated_pptx/build/slide_039.js`, banked at `qa/slide039/build_attempt_2.js`.

- Layout: `LAYOUT_WIDE` 13.33 x 7.5 in, canvas FFFFFF.
- House chrome via `shared_patterns/house_chrome.js`: gray E9E9E7 panel x54..903 y45..540;
  C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 only — **no top stroke**
  (measured, deck-specific); badge d35 at (876,73), fill FDFD96, purple ring 6A5ACD,
  bold 18pt Arial #333333, numeral `39`.
- Font: Times New Roman throughout (serif, per `typography_notes`). TITLE 28pt bold,
  BODY 19pt regular, WHY_SIZE 18pt bold, ANN_SIZE 15pt regular, CAP_SIZE 19pt bold.
- Equation: matplotlib mathtext -> 600dpi transparent PNG (`build/assets/eq_039_main.png`,
  1676x179 px) placed at x366.04, y274.1 in (= px/600). Mathtext
  `W^{(updated)}=W^{old}-\eta\,\delta_{i}\,X_{i}`, 17pt, colour 000000. Sidecar at
  `build/assets/eq_039_main.json` (for the orchestrator's post-certification OMML wrap —
  NOT applied by this worker).
- Chevron bullet markers: 600dpi triangle PNG `build/assets/evt_039.png` (Arial has no
  U+25B6 glyph; a PNG marker was the measured, safe choice).
- Verified in the delivered file: 16/16 required text lines verbatim (unzipped the XML),
  media = equation PNG + arrow PNG with valid rels, fonts = {Times New Roman, Arial}.

## Render / gates

- `qa/slide039/render_2.png` — 2001x1125, 150 dpi, LibreOffice (`-env:UserInstallation=
  file://$TMPDIR/lo_slide039`) -> pdftoppm. Cut from the delivered build (build 23:42,
  render 23:43).
- **`shared_patterns/house_chrome_check.py render_2.png 39` = PASS** (panel x112-1882,
  y94-bottom; strokes L/R/bottom present, top bare; badge center (1824,152) d=68;
  all within tol 8).
- **Self-check `selfcheck_attempt_2.py` = PASS** (all 19 elements within tolerance;
  no wrapped lines; equation ink present and inside the green callout; caption centres
  y419/443/469 vs measured 417/441/467; caption pitch 23.3px vs measured 24px).

Attempt history (judge attempts are shared across both legs; budget 6):

| # | leg | target | result |
|---|---|---|---|
| 1 | Template A | render_1.png | HangError at the gateway's 630s wall (queue-induced), no transcript — **not an attempt** per W4 |
| 2 | Template A | render_2.png | **FINAL VERDICT: PASS** + 1 borderline MINOR -> `adjudication_1.txt` |
| 3 | Template B eq_stack | crop_2 pair | coherent, no FINAL VERDICT line -> `adjudication_2.txt` |
| 4 | Template B eq_stack | crop_2 pair | re-roll (identical findings) -> same adjudication |
| 5 | Template B title_lines | crop_2 pair | coherent, no FINAL VERDICT line -> `adjudication_3.txt` |
| 6 | Template B notes_bullets | crop_2 pair | coherent, no FINAL VERDICT line -> `adjudication_4.txt` |

The earlier `render_1.png`/`build_attempt_1.js`/`selfcheck_attempt_1.*` evidence is kept
(never delete banked evidence); it describes the pre-caption-fix build.

Why render_2: the bottom caption was re-measured and found to be **three colour runs**
(red for the first nine words, black for the remainder; then a black line; then the
blue emphasis line), not the single all-red box in attempt 1. Implemented as three
boxes pinned to the measured ink centres (y417/441/467) — see `build_attempt_2.js`.

## Judge legs — verdicts

### Leg 1 (Template A, full-slide) — PASS
Transcript: `qa/slide039/judge_attempt_2.txt` (contains `FINAL VERDICT: PASS — faithful,
usable recreation`).
- BLOCKER: none. MAJOR: none.
- One MINOR (borderline, medium confidence): the blue caption line reads as a
  violet/indigo ≈ the house 6A5ACD-family purple vs the original's slightly more
  saturated blue.
- The judge explicitly verified as NOT defects: house chrome (incl. no top stroke),
  title verbatim + line-broken identically with the same colour runs, bullets 1-3 with
  the same wrap point, the equation (same content and variable order, 2D form), the red
  annotation, "Why using SGD" + its two bullets, the lower caption block with its colour
  runs, regions/ordering, containment, missing elements, delimiter geometry, and the
  correctly-omitted mouse-cursor artifact.

### Leg 2 (Template B, crop pairs) — clean by PIL adjudication
Procedure B requires a crop-pair over each dense region. All three dense regions of this
slide were cut at matched effective scale (LANCZOS x2.083 of the same slide-space region;
both crops byte-identical in size so slide-space coordinates map 1:1):

| region | frame px bbox | transcript | outcome |
|---|---|---|---|
| eq_stack | x339..863, y251..311 | `crop_2_eq_stack_judge.txt` | clean — adjudicated (`adjudication_2.txt`) |
| title_lines | x114..842, y71..136 | `crop_2_title_lines_judge.txt` | clean — adjudicated (`adjudication_3.txt`) |
| notes_bullets | x76..403, y300..378 | `crop_2_notes_bullets_judge.txt` | clean — adjudicated (`adjudication_4.txt`) |

Note on transcript form: all three crop bodies came back **without a `FINAL VERDICT:`
line**, so under the standing law they are not evidence on their own. Each was re-rolled
once on unchanged bytes (eq_stack) and every raised finding was PIL-refuted against both
images, with the refutation record banked — which is exactly the "clean" condition in the
protocol (`FINAL VERDICT: PASS` **or** every finding PIL-refuted + banked refutation).

## Adjudications (PIL-first, against both images)

1. `adjudication_1.txt` — blue caption colour (full-slide MINOR).
   **No fix.** The ORIGINAL frame contains no single blue: its own title "Mini-Batch"
   and caption blue differ from each other by 79.3 RGB units, more than the recreation's
   uniform #584CA8 differs from either (45.8 / 36.2). The residual is brightness, not
   hue — blue-lead agrees within 6 units. #584CA8 is the measured median of the deck's
   blue ink and reproduces the original's own title blue to 8.5 units.
2. `adjudication_2.txt` — equation "bold/underlined vectors, red η, green δ_i, red X_i,
   missing pen scribble" (eq_stack).
   **No fix.** A JPEG-response control (the known-red annotation shifts +104 G / +107 B
   through IMG2's codec) predicts black ink would show g-lead 86; the observed equation
   ink shows g-lead 41 — *less* saturated than neutral black. So there is **no colour
   coding** in the equation zone. The red in that zone clusters as solid blobs
   (density 0.67-0.90, frame x493..566, y280..295) — over η/δ_i/X_i — which is exactly
   the "red mouse-pointer arrow over the equation" the analysis record identifies as a
   screen-cursor artifact (correctly omitted per ground rule c). Ink density 12.5% vs
   12.2% refutes any bold-weight difference. The validated analysis (`PASS_WITH_FIXES`)
   itself specifies the equation as plain text with no per-symbol colours, and the
   full-slide judge independently confirmed the equation content.
3. `adjudication_3.txt` — title "extra `)` after (GD)" + "collapsed space between the
   blue and red runs" (title_lines).
   **No fix.** The render has four clean glyphs `(` x338..345, `G` x347..366,
   `D` x368..386, `)` x388..395. The original's line-1 ink is blurred into one blob
   x337..386, which is why it "looks like" there is no closing paren — but measuring the
   original at the exact columns of the render's `)` gives red pixel counts
   54 / 49 / 42 (x388/390/392) then a clean stop at x394: a closing parenthesis is
   present in both. On line 2 all three runs match within 1-2px (render "and" 280..323,
   "Gradient" 478..586, "Descent" 593..686 vs orig 279..324, 476..582, 588..687); the
   render's blue run has 7 internal letter gaps (properly separated letters) vs the
   original's 2 blurred ones — the words are *more* separated in the render, not less.
4. `adjudication_4.txt` — "solid vs open/outlined arrowhead", "wider spacing after
   'efficient'", "sharpness" (notes_bullets).
   **No fix.** Both markers are solid filled triangles: fill 0.51 vs 0.49 (marker 1) and
   0.51 vs 0.46 (marker 2), same 22x19 px bbox, same position, ink counts 215 vs 217.
   An outlined glyph would fill ~0.15-0.25. Bullet-1 line extents are IDENTICAL
   (x105..392 both) and word-space widths match (11-12px vs 13-15px, blur-spread only).
   The sharpness difference is the expected outcome of rendering a PPTX against an
   upscaled video frame (ground rules d/e).

## DB state (final)

```
gen_status   = passed
visual_check = PASS
visual_attempts = 2
visual_transcript = videos/.../recreated_pptx/qa/slide039/judge_attempt_2.txt
pptx_path = videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_039_recreated.pptx
build_script = .../recreated_pptx/build/slide_039.js
worker_id = slide039-worker, heartbeat current
last_error = null
```

## Banked evidence (`qa/slide039/`)

`render_1.png`, `render_2.png`, `build_attempt_1.js`, `build_attempt_2.js`,
`selfcheck_attempt_1.py` + `_output.txt`, `selfcheck_attempt_2.py` + `_output.txt`,
`judge_prompt_1.txt`, `judge_attempt_2.txt`,
`crop_2_{eq_stack,title_lines,notes_bullets}_{render,orig}.png`,
`crop_prompt_2_{eq_stack,title_lines,notes_bullets}.txt`,
`crop_2_{eq_stack,title_lines,notes_bullets}_judge.txt`,
`adjudication_1.txt`, `adjudication_2.txt`, `adjudication_3.txt`, `adjudication_4.txt`,
`worker_report.md` (this file), plus the attempt-1 crop set.

Measurement scripts: `selfcheck_attempt_1.py`, `selfcheck_attempt_2.py` (both re-runnable
against any render of this slide).

## Open / follow-up

- OMML wrap: not applied here (post-certification step owned by the orchestrator) —
  re-derive the manifest rel-ids from the CURRENT pptx before wrapping.
- The crop judge in this fleet is currently not emitting the mandated `FINAL VERDICT:`
  line (all three legs returned prose bodies). That is a model-behaviour issue worth
  reporting upstream; adjudication is the protocol's sanctioned fallback and was used.
