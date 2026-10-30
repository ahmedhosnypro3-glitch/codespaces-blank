# Worker report — slide 036 (deck 03_ridger_regression_gradient_descent)

- Worker: w036 (pool run 859463) · Slide: **036 "Problem Formulation"**
- Deck DB: `VIDEO=machine-learning/03_ridger_regression_gradient_descent`
- Final status: **CERTIFIED** — visual_check=PASS, gen_status=passed, visual_attempts=8
- Judge method: **direct harness image reads** (owner directive 2026-10-24; no vision
  gateway, no `scripts/16_vision_gate.sh`, no `analyze_image.py`)

## 1. Resume state (what was banked when this worker started)
- Build `recreated_pptx/build/slide_036.js` (== `build_attempt_5.js`), pptx
  `slide_036_recreated.pptx` (05:01:32), render `render_7.png` (05:01:36, current bytes).
- Full-slide gateway transcript `judge_attempt_7.txt` (attempt 7, PASS) — kept as banked
  evidence; its body has no md5 header and does not satisfy this run's transcript format,
  so attempt 8 was judged in full with the direct-read template.
- Crop leg missing: `crop_7_eq_stack_judge.txt` was a 115-byte header-only stub (no verdict).
  `crop_7_{eq_stack,delta_lines}` pairs existed but were never judged.
- No `worker_report.md` existed.

## 2. What the crop leg found on render_7 (all real, measured)
Reading the original and fresh render_7 crops directly (comparison order per protocol):
1. **Unmatched opening parenthesis** on the first equation term: render emitted `(W` at
   frame x304 while the original has W at x304 with NO parentheses on that term
   (`eq036_v4.py` had dropped only the closing paren).
2. **Literal `_i` subscript** — the equation printed `X` + `_` + baseline `i` instead of a
   lowered subscript (violates the founder 2D-math rule: never caret/underscore text).
3. **`)take` with no gap** — second group's `)` at 499 and the phrase ink at 502; the original
   has `)` 496..498 and the phrase starting at 507.
4. **Summation limit uncoloured** — the original's limit is italic with "misclassified" and
   "(i)" in red; render was black upright.
5. **Two verbatim case errors** — box 2 line 3 and box 4 line 2 printed lowercase
   `class I` where the frame and the analysis spec both have capital `Class I`.

## 3. Fixes applied (attempt 8)
- New equation asset renderer `qa/slide036/eq036_v5.py` → `build/assets/eq_036_error.png`
  (5409x377 px @600 dpi). PIL composite, pieces pinned to measured frame ink:
  `Error =` 84..150, Sigma 220..240, italic limit 162..297 with red "misclassified"/"(i)",
  term1 `W^T X_i` with NO parens and a true lowered i, `⇒` 396..411, term2 `(W^T X_i)`
  443..499, italic phrase 507..732 (7.7 px gap after `)`). Sidecar
  `eq_036_error.json` re-emitted; attempt-7 asset + sidecar preserved as
  `qa/slide036/assets_eq_036_error_attempt7.{png,json}`.
- `build/slide_036.js`: EQ_W/EQ_H updated to the new asset (9.015 x 0.62833 in, same
  EQ_X/EQ_Y); box2-L3 and box4-L2 target tokens `class` → `Class`. Everything else untouched.
- Banked `build_attempt_8.js` (md5 1b5c330b73a9be8ae8d47f0ea6f6be6e; identical to the live
  script).
- Rebuild: pptx md5 **ad2a07ddd2e688b40d57d20e5c6ea701**; rendered at 150 dpi with a private
  LibreOffice profile (`$RUNDIR/lo/036`) → `render_8.png` md5
  **ad8676e60fbd305096dce60dc0b16c5a** (2001x1125).

## 4. Pre-judge selfcheck (mandatory) and chrome
- `selfcheck_attempt_8.py` / `.txt` on render_8 (150 dpi, scale 2.0833): **RESULT: PASS**
  — frame containment 4/4 boxes, equation ink present, delimiter spans, no wrap, explicit
  line spacing, baseline deltas 0-2 px, colour coding, equation ink-band dx0 dy-1 dw-1 dh1,
  red X present, raised W^T.
- `shared_patterns/house_chrome_check.py render_8.png 36` → **PASS** (`house_chrome_8.txt`).

## 5. Judging (attempt 8 — both legs, direct reads)
| leg | transcript | verdict |
|---|---|---|
| full slide | `judge_attempt_8.txt` | **PASS** (5 MINORs, all adjudicated) |
| crop eq_stack (x60..890 y320..430) | `crop_8_eq_stack_judge.txt` | **PASS** |
| crop delta_lines (x60..880 y433..539) | `crop_8_delta_lines_judge.txt` | **PASS** |
| crop class_lines (x60..880 y90..318) | `crop_8_class_lines_judge.txt` | **PASS** |

- Crop pairs cut from render_8 at matched effective scale (`cut_crops_8.py` / `.txt`):
  eq_stack 1730x229, delta_lines 1709x221, class_lines 1709x474 — orig LANCZOS-upscaled to the
  render crop's exact size, effective px/frame-px identical per axis on both sides.
- Measurements backing the verdicts: `audit_8.txt` (per-line ink spans/ratios, collision gaps,
  equation piece bboxes, delimiter spans, limit red-part check, containment), `measure_eq_7.txt`
  (original/render ink-run census), zooms `zoom_8_*.png`.
- MINORs (documented, not fix triggers; `adjudication_attempt_8.txt`): serif-bold-italic source
  medium vs the deck's Arial (per-line width ratios 0.907-1.021), vector underlines and italic
  class tokens not drawn, title ink 16 px narrower, implication-arrow glyph/whitespace
  substitution. These are the deck's ratified typographic substitution (same treatment as
  certified siblings 012/035) — **open deck-level debt**, not slide-036 content/geometry
  defects.

## 6. Evidence index (md5)
- unique_slides/slide_036.jpg · a75911bb68fa4865ded5cd329891f76e
- recreated_pptx/slide_036_recreated.pptx · ad2a07ddd2e688b40d57d20e5c6ea701
- recreated_pptx/build/slide_036.js · 1b5c330b73a9be8ae8d47f0ea6f6be6e
- qa/slide036/render_8.png · ad8676e60fbd305096dce60dc0b16c5a
- qa/slide036/crop_8_eq_stack_orig.png · 441376694dd8b7ef8e4af2e3dcc4ea41
- qa/slide036/crop_8_eq_stack_render.png · 5b80d5d6d3e5b95bb3b17c2fbc62668b
- qa/slide036/crop_8_delta_lines_orig.png · b28e95abe75c143ae0f0da519bdb27d5
- qa/slide036/crop_8_delta_lines_render.png · f0ad9b921531d83c6b647b8e6f702f51
- qa/slide036/crop_8_class_lines_orig.png · 0e26e68784e3a05df1845d33c6f3fba7
- qa/slide036/crop_8_class_lines_render.png · b93f601da97dc532150494548c1e6ea7
- Equation asset (attempt 8) · build/assets/eq_036_error.png (5409x377 @600 dpi),
  attempt-7 asset preserved as qa/slide036/assets_eq_036_error_attempt7.png

## 7. Evidence handling notes (nothing deleted)
- The unjudged attempt-7 crop pairs were re-cut from the SAME current render bytes and
  replaced at the canonical `crop_7_*` names (they carried no verdict). Superseded md5s:
  crop_7_eq_stack_orig bd55d177…, crop_7_eq_stack_render 49b1c05f…, crop_7_delta_lines_orig
  8c04dc0d…, crop_7_delta_lines_render af462957…. Their source (render_7.png) is unchanged and
  still banked; the re-cuts are reproducible with `cut_crops_5.py`-style geometry.
- The header-only `crop_7_eq_stack_judge.txt` stub is preserved verbatim as
  `crop_7_eq_stack_judge.gateway_stub.txt`; new crops are banked under `crop_8_*`.
- All earlier renders (1/2/3/5/6/7), transcripts, prompts and build copies are untouched.

## 8. Resume point
None — slide certified. Component export not required (slide 036 has no dependents in
`slide_dependencies.json`; it is neither a parent nor a child).
