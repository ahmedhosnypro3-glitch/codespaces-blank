# Slide 049 — BUILD READINESS (prephase pack S20e)

Feeds the next attempt on `slide_049_recreated.pptx` (current build:
`build/slide_049.js`, 251 lines; gen_status='building'; the lane that held it parked on a
2026-10-24 vision-leg wedge that has since cleared — heavy 65536-token legs ran fine on
2026-10-25). Rows reference `delta_vs_related.md` (vs certified 046) and the ground-truth
transcripts in `orig_judges/`.

## A. Certified components available for reuse (do NOT re-derive)

| # | Component | Where | Reuse action |
|---|---|---|---|
| A1 | House chrome | `drawHouseChrome(pptx, s, {numeral: "49"})` | keep |
| A2 | d(x) 2-row bracketed matrix PNGs | `build/assets/slide_049_matrix_1..6.png` (w 0.79167in each) | REUSE — 2-D law compliant |
| A3 | W column PNGs | `build/assets/slide_049_wcol_1..6.png` + `eq_slide049_wcol.json` sidecar (175×379px, 12pt) | REUSE; note the v2 attempt-9 geometry (rows 4-6 shifted +11px) |
| A4 | 046's certified stop-text idiom | `build/slide_046.js:262-274` | REFERENCE for text runs; 049 differs (bare lines, no pink box) |

## B. Delta-row → build-action checklist

| Delta ref | Build action |
|---|---|
| C2 badge | keep "49" |
| T1 container | GROUND-TRUTH: `orig_topband.txt` §1 decides full violet box vs 046-style rules+left stroke; build currently draws full violet 1.5pt box — adjust border color/hue per §6 census |
| T2 7th column "Initial W = [4, -2]" | verify form in `orig_topband.txt` §3: inline-linear (keep) vs stacked 2×1 (re-render via `scripts/render_eq.py`, no asset exists) |
| T3 class hues | verify C1 red / C2 blue order from `orig_aug_stop.txt` §4 |
| T5 REPEAT line | keep red bold; check whether frame shows "η = 1" fully |
| T7 Z grid | build draws 3×3 parenthesized grid; verify values (0 7 3)/(0 6 2) and delimiter style vs `orig_topband.txt` §4 |
| T9 top-right weight box | GROUND-TRUTH: if `orig_full.txt` region map shows a yellow/pink box x~738..828, ADD it (046 idiom with 049's values); if absent keep |
| A1 augmented container | GROUND-TRUTH: box vs open rules vs bare; adjust strokes |
| A2 "Ugmented" title | keep verbatim spelling; color per census (violet vs navy vs black) |
| A3 data rows | GROUND-TRUTH: 3+bias rows (045 family) vs 4 data rows (spec); fix table to frame |
| A4 Iteration 2 box | keep; size per measured white-text band |
| A5 stop block | GROUND-TRUTH: bare 20pt lines (current build) vs a filled box (046-style); spec says RED-FILLED box with white text, build says bare black/red — frame decides |
| R2/R3/R4 calc rows | keep 6 ruled rows + PNGs; verify rule y-bands 140/205/271/337/403/469/527 and per-row x anchors vs `orig_calc_r12.txt`/`orig_calc_r56.txt` |

## C. Lane context (READ-ONLY)

- Worker `fix-judge-049g` parked 2026-10-24 with the wedge record (5 full-slide + 1 callout
  attempts hung at 630s client abort). Gateway healthy again 2026-10-25 — the resume path
  is the lane's own `legA_dispatch_049d.sh`/`legB_dispatch_049d.sh`, not mine to run.
- The build already carries two certified-shape fixes (2D matrix PNGs; W-column v2).
- Do not touch `qa/slide049/` outside `prephase/`; do not write the DB.

## D. Verification order

1. `orig_judges/orig_full.txt` — region map (T9 + any missed region).
2. `orig_topband.txt` — T1..T8.
3. `orig_aug_stop.txt` — A1..A5.
4. `orig_calc_r12.txt` + `orig_calc_r56.txt` — R2..R4.
5. Apply §B → rebuild → house_chrome_check.py → judge (both legs now feasible).

## E. OMML inventory (post-certification step, deck law)

- `slide_049_recreated.pptx` currently carries NO `mc:AlternateContent` wrap — and
  neither do certified siblings 045/046/047 (deck-wide OMML pass not yet run).
- After visual_check=PASS, wrap the **12 matrix-class PNGs** (`slide_049_matrix_1..6`
  2-row bracketed d(x) matrices + `slide_049_wcol_1..6` [5;−1;−1] columns; per-row
  geometry in `eq_slide049_wcol.json`) via `scripts/18_omml_wrapper.py` — manifest
  values re-derived from the CURRENT pptx, never assumed from a prior build.
- Wrap the slide's own plain-named pptx only; never LO-resave a wrapped deck.
