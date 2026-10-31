# OMML_INVENTORY_r4 — deck 03 eq-pic wrap state (READ-ONLY scan, 2026-10-31)

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
Method: for each of the 51 CURRENT `recreated_pptx/slide_NNN_recreated.pptx`, unzipped
`ppt/slides/slide1.xml` and classified every `p:pic` as **wrapped** (ancestor
`mc:AlternateContent`) or **remaining** (plain pic). Pics were matched to eq sidecars by
pic `descr` basename (exact for all slides with eq pics, incl. 005/030 whose media bytes
were re-encoded) with md5/IHDR-dims fallback for multi-rel matches. Sidecars scanned:
all 184 `recreated_pptx/build/assets/eq_*.json` (plus the odd-named ones:
`eq_r*_l`/`eq_r_kw`/`eq_initial_w_col` -> slide 048 per `build/gen_assets_048.py`;
`eq_slide048_*` -> 048; `eq_slide049_*` -> 049; `eq_index_014`/`eq_index_042` are
matrix-bracket assets, NOT equations). A descr sweep for `eq_` in pic names found three
more embedded eq PNGs whose sidecars live outside `build/assets/` (slides 014, 033, 034
— r3 missed these; they are real remaining work).

Supersedes r2/r3 wrap-state columns (agent-391 shard 004/005/015/021/030 now partially
wrapped per `OMML_WRAP_LOG.md`; 009/036/039 fully wrapped earlier).

## Summary

- Eq pics total in current pptx files: **122** across 19 slides; **wrapped 21**, **remaining 101**.
- Fully wrapped (done): **009 (2/2), 030 (2/2), 036 (1/1), 039 (1/1)**.
- Partially wrapped: **004 (1/4), 005 (8/9), 015 (1/9), 021 (5/6)**.
- Unwrapped with eq pics: **014 (0/3), 023 (0/1), 031 (0/1), 032 (0/1), 033 (0/1), 034 (0/1),
  037 (0/5), 044 (0/54), 048 (0/6), 050 (0/4), 051 (0/11)**.
- Sidecars exist but NO eq pic embedded in the current pptx (skip, unchanged): 003, 043,
  046, 047, 049.

## Per-slide table

| slide | total eq pics | wrapped | remaining | remaining sidecars (rel ids) | remaining mathtext features | status |
|---|---|---|---|---|---|---|
| 004 | 4 | 1 | 3 | rId1 eq_004_Yvec, rId2 eq_004_Yhatvec, rId4 eq_004_formula | `\underline` + `\mathbf` (COMPOSED entries), `\mathbf{\hat{Y}}`; mixed color (black/red) | partial — remaining blocked on `\underline` / `\mathbf{\hat{Y}}` |
| 005 | 9 | 8 | 1 | rId7 eq_005_deriv2 | `\underline`, `\partial`, `\dfrac`, `\left\right` | partial — deriv2 blocked on `\underline` |
| 009 | 2 | 2 | 0 | — | — | DONE (manifests qa/slide009/) |
| 014 | 3 | 0 | 3 | rId1 eq_014_Yvec, rId2 eq_014_Yhatvec, rId3 eq_014_final | no sidecars in build/assets (PNGs in qa/slide014/assets_backup_att10/); mathtext must be re-banked from build/slide_014.js | remaining (NEW vs r3) — geometry-only |
| 015 | 9 | 1 | 8 | rId1 eq1_l1, rId2 eq1_l2, rId3 eq1_l3, rId4 redbox_eq, rId6 deriv_l1, rId7 deriv_l2, rId8 normal, rId9 solution | all 8 use `\underline` (+ `\frac`, `\lambda`, `\partial`) | partial — all remaining blocked on `\underline` |
| 021 | 6 | 5 | 1 | rId6 eq_021_invexpr | `\underline`, `\lambda`; color=multi | partial — invexpr blocked on `\underline` |
| 023 | 1 | 0 | 1 | rId1 eq_023_main | `\underline`, `\lambda`, `\left\right` | remaining — wrapper previously FAIL-LOUD here (qa/slide023/omml_prepass_note.md); manifest banked qa/slide023/omml_manifest.json |
| 030 | 2 | 2 | 0 | — | — | DONE |
| 031 | 1 | 0 | 1 | rId1 eq_031_main | GEOMETRY-ONLY (no mathtext) — re-bank from build/slide_031.js | remaining |
| 032 | 1 | 0 | 1 | rId2 eq_032_main | GEOMETRY-ONLY — re-bank from build/slide_032.js / render_curve_032.py | remaining |
| 033 | 1 | 0 | 1 | rId1 eq_033_main_v7b | sidecar geometry-only (qa/slide033/eq_033_main_v7b.json) — re-bank from build/slide_033.js | remaining (NEW vs r3) |
| 034 | 1 | 0 | 1 | rId1 eq_034_main | mathtext recoverable from build/gen_eq_034.py: `f(x) = \frac{x^2 \cos(x) - x}{10}` | remaining (NEW vs r3) |
| 036 | 1 | 1 | 0 | — | — | DONE (qa/slide036/) |
| 037 | 5 | 0 | 5 | rId1/rId4/rId5 eq_037_sigma; rId2/rId3 eq_037_frac | GEOMETRY-ONLY — re-bank; anisotropic rescale + per-instance fontsize re-derivation needed (qa/slide037/omml_prepass_note.md) | remaining |
| 039 | 1 | 1 | 0 | — | — | DONE (qa/slide039/) |
| 044 | 54 | 0 | 54 | 48 distinct sidecars: eq_044_dx1_a..dx6_d, w1_a..w6_a, arrD/arrL/arrDk (multi-rel each) | GEOMETRY-ONLY, per-piece colors (000000/C00000/009A4A/0000C8) — re-bank per piece from build/gen_eq_044.py + slide_044.js | remaining — biggest shard |
| 048 | 6 | 0 | 6 | rId1..rId6 eq_r1_l..eq_r6_l | GEOMETRY-ONLY — re-bank from build/gen_assets_048.py | remaining |
| 050 | 4 | 0 | 4 | rId15 eq_050_Z1, rId16 eq_050_Z2, rId17 eq_050_Z3, rId18 eq_050_finalW | finalW has mathtext with `\underline` + `\substack` + `\phantom`; Z1-Z3 GEOMETRY-ONLY | remaining |
| 051 | 11 | 0 | 11 | rId13 initw, rId14 step, rId33 dzlabel_1, rId34 rowvec_1, rId35/38/41 wcol_green, rId36 dzlabel_2, rId37 rowvec_2, rId39 dzlabel_3, rId40 rowvec_3 | step/dzlabel_1/rowvec_1-3 parseable (`\;` spacing; colors #A1232A/#000000/#0F0087); initw/dzlabel_2-3/wcol_green GEOMETRY-ONLY | remaining |

## Notes

- rel_id lists for multi-rel sidecars (037, 044, 051 wcol_green) come from IHDR-dims
  fallback and are supersets; re-derive exactly from `ppt/slides/_rels/slide1.xml.rels`
  at wrap time per the wrapper contract.
- Deck `03_ridger_regression_gradient_descent_final.pptx` currently has
  mc:AlternateContent on pages **9, 36, 39 only** (verified by unzip); pages for the
  2026-10-31 shard wraps (4, 5, 15, 21, 30) are stale in the deck — see
  OMML_WRAP_PLAN_r4.md restage list.
- PREP ONLY: no wrapper run, no pptx modified, no git touched, no evidence deleted.
