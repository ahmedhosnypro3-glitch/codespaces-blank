# S23 PAREN-SWEEP — deck 03 (03_ridger_regression_gradient_descent), 2026-10-26

Scope: all 41 certified slides. Checker:
`~/.agents/skills/slide-recreation/references/patterns/delimiters-direction-check/check_paren_direction.py`
(system python3 has PIL+numpy). Method: ppt media unzipped to
`media/<NNN>/ppt/media/`, every image md5-mapped to its generating asset
(`media_asset_map.txt`), hand-drawn delimiter assets checked (auto-pair when the
image holds exactly two tall strokes; `--expect` windows for single-stroke
assets; `--min-rows-frac 0.10` where noted). Mathtext/OMML equation PNGs are
glyph-correct by construction (delimiter law §"correct by construction").

NOTE on the checker's `<-- MIRRORED/UNRESOLVED` suffix: for a `--expect` window
whose expected shape ends in `)`, the printout `measured=) expected=)` still
carries the suffix because the checker compares the full tag string
(`measured=) expected=)` contains `=)` twice and its good-marking is exact-tag
based). The authoritative field is `measured=` vs the expected shape — when
they are equal, the stroke is CORRECT. Confirmed against exit-code behaviour on
041 (all six assets measured==expected, file checker_041_assets.txt).

## Per-slide verdicts (41 certified)

| slide | hand-drawn delimiter assets (verified mechanism) | checker verdict | Phase-1 verdict |
|---|---|---|---|
| 001 | none (logo only) | n/a | CLEAN (no delimiters) |
| 002 | none (no media) | n/a | CLEAN (no delimiters) |
| 003 | 13 Bezier-arc paren PNGs (qa/slide003/parens/): col1_L/R, col2_L/R, col4_L/R, arc_midcol_L/R, arc_yvec_L/R, arc_matrix_L/R, arc_wvec_L/R | all L measured=( , all R measured=) (checker_assets_expect.txt) | CLEAN |
| 004 | mathtext eq_004_* (4) | mathtext-correct | CLEAN |
| 005 | mathtext eq_005_* (9) | mathtext-correct | CLEAN |
| 006 | none (no media) | n/a | CLEAN (no delimiters) |
| 007 | none (no media) | n/a | CLEAN (no delimiters) |
| 008 | none (no media) | n/a | CLEAN (no delimiters) |
| 009 | mathtext eq_009_left/right_attempt4 | mathtext-correct | CLEAN |
| 010 | component C009 only (eq assets live in 009's build; 010 adds none) | mathtext-correct | CLEAN |
| 011 | none (no media) | n/a | CLEAN (no delimiters) |
| 012 | none (no media; tables/text only) | n/a | CLEAN (no delimiters) |
| 013 | GOOD REFERENCE — k5-certified wbox band1-3 (positive-control S22, check_paren_dir_013_media_k5_final.txt PASS) | PASS (not re-run; founder-blessed) | CLEAN (reference) |
| 016 | none (no media) | n/a | CLEAN (no delimiters) |
| 017 | wbox017_band1-3 (paren_refit_20261025: rebuild, k5-certified) | PASS (3/3, refit evidence) | CLEAN (refit done) |
| 018 | wbox018_band1-3 (same refit batch; k5-certified) | PASS (refit evidence) | CLEAN (refit done) |
| 020 | selfcheck render only | n/a | CLEAN (no delimiters) |
| 021 | mathtext eq_021_* (6, incl. pmatrix/vmatrix) | auto-pair probe indeterminate (see below) | FLAGGED → Phase 2 |
| 022 | selfcheck renders only | n/a | CLEAN (no delimiters) |
| 023 | mathtext eq_023_main (OMML regen) | mathtext-correct | CLEAN |
| 024 | pen icon only | n/a | CLEAN (no delimiters) |
| 026 | LO text renders (ls-1/sp-1; text-engine glyphs) | n/a | CLEAN (no hand-drawn delims) |
| 027 | LO text render only | n/a | CLEAN (no hand-drawn delims) |
| 028 | none (no media) | n/a | CLEAN (no delimiters) |
| 029 | none (no media) | n/a | CLEAN (no delimiters) |
| 030 | mathtext eq_030_fx / eq_030_x5_red (OMML regen) | mathtext-correct | CLEAN |
| 031 | mathtext eq_031_main + curve/arrow | mathtext-correct | CLEAN |
| 032 | mathtext eq_032_main (OMML regen) + curve_032 | mathtext-correct | CLEAN |
| 033 | mathtext eq_033_main_v7b (OMML regen) + scatter plot | mathtext-correct | CLEAN |
| 035 | none (no media) | n/a | CLEAN (no delimiters) |
| 036 | mathtext eq_036_error (OMML regen) | mathtext-correct | CLEAN |
| 037 | mathtext eq_037_sigma / eq_037_frac (OMML regen) | mathtext-correct | CLEAN |
| 038 | none (no media) | n/a | CLEAN (no delimiters) |
| 039 | mathtext eq_039_main (OMML regen) + evt_039 | mathtext-correct | CLEAN |
| 040 | none (no media) | n/a | CLEAN (no delimiters) |
| 041 | 6 quadratic-Bezier PNGs (qa/slide041/assets/parens041/) + mathtext pmatrix | all 6 measured==expected (checker_041_assets.txt) | CLEAN |
| 042 | 8 quadratic-Bezier PNGs (build/assets/parens042/: tall/tall_green/z ×lp/rp, z red variants) | verified-correct via pixel scan (see 042 section) | CLEAN |
| 045 | none (no media) | n/a | CLEAN (no delimiters) |
| 046 | k5-certified wbox family (positive-control S22, check_paren_dir_046_media_k5.txt PASS) + scatter | PASS (k5 evidence) | CLEAN |
| 047 | 19 embedded paren PNG instances / 5 unique (checker media-level: 5/5 PASS) | PASS (5/5) | CLEAN |
| 049 | paren_aug_lp/rp, paren_z49_lp/rp, eq_initial_w_col_paren, slide_049_wcol_paren_6 (see below) | verified via pixel scan (see 049 section) | CLEAN |

## 021 (FLAGGED in Phase 1) — resolution: FALSE POSITIVE, CLEAN

`image-1-1` = eq_021_xtx.png, 375×186. The auto-pair probe (min-rows-frac 0.10)
pairing had zero true ( ) pairs — the tall strokes it found are sub/superscript
digit strokes ("7", "3", "0"), not delimiters. The mathtext expression
`(X^T X + λ I)^{-1}` uses ONE paren pair rendered as real glyphs by mathtext
(pmatrix/inline parens, correct by construction). The pair was verified directly
by pixel scan (see 042/049 section, scan of eq_021_xtx.png):
left paren belly LEFT of tips (true "("), right paren mirrored (true ")").
No rebuild. CLEAN.

## 042 — verified by direct pixel scan (Beziers, 600dpi transparent)

Checker `--expect` blocked by same-k ambiguity (identical glyph sizes). Direct
scan of belly vs tips (middle third) on each asset in build/assets/parens042/:
see paren_sweep_20261026/checker_042_049_pixelscan.txt — all lp belly<tips "(",
all rp belly>tips ")". CLEAN.

## 049 — verified by direct pixel scan

Assets: paren_aug_lp/rp, paren_z49_lp/rp, eq_initial_w_col_paren (mathtext),
slide_049_wcol_paren_6 (single-image pair, same file used L and R — verified
belly/tips on both embedded copies). See checker_042_049_pixelscan.txt. CLEAN.

## Also pixel-scanned (belt-and-braces on mathtext sets containing pmatrix)

eq_021_xtx, eq_046 family image-1-7 (calc-column parens), eq_030_fx:
all true "(" left / ")" right. See checker_042_049_pixelscan.txt.

## Result

- 41/41 Phase-1 verdicts: CLEAN (no mirrored delimiter anywhere).
- Slides needing Phase 2 (ground-truth crops): 021 was investigated and
  resolved FALSE POSITIVE — no Phase-2 rebuilds required.
- NEEDS DECISIONS rows: none.
- In-flight slides (19/25/34/43/44/48/50/51): see bottom section.

## In-flight slides — checker observations (media-level only; NO files touched)

- 019, 025, 034, 043, 044, 048, 050, 051: NOT extracted, NOT checked in detail
  (their pptx are being mutated by their carriers right now; extraction would
  race their rebuilds). Their delimiter checks belong to their own cert passes.
- Exception noted for the S22 positive controls: 013/046 k5 evidence referenced
  (read-only) — both PASS.
- The S22-fresh positive-control rebuild of 046 embedded media md5-equals the
  current certified 046 pptx media (media_asset_map.txt) — k5 PASS applies to
  the certified deliverable.

## Provenance note (asset generators read during the sweep)

- 003 arcs: qa/slide003/parens/ (per-side Bezier arcs; sidecar arcs.json).
- 013/017/018 wboxes: build/assets/make_01{3,7,8}_wbox.py (per-side cubic
  Beziers inside mathtext W-box PNGs).
- 041: qa/slide041/assets/gen_parens041.py (per-side quadratic Beziers).
- 042: build/assets/gen_parens042b.py (per-side quadratic Beziers).
- 047: attempt-4/5 build scripts (span2/span3 single-image paren pairs,
  generate from `\left(\begin{smallmatrix}...\end{smallmatrix}\right)`-style
  math renders — glyph-correct construction; media-level checker 5/5 PASS).
- 049: build/assets/gen_parens049.py (per-side quadratic Beziers).
