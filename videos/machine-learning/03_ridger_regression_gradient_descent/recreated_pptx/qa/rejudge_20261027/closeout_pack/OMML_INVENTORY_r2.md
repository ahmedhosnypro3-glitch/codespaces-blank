# OMML_INVENTORY_r2 — S9 equation-wrap closeout prep (deck 03_ridger_regression_gradient_descent)

Generated 2026-10-31 by a read-only inventory pass (PREP ONLY — nothing wrapped, no pptx modified, no git touched).
Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
Supersedes/extends `OMML_INVENTORY_r1.md`: r2 covers ALL 51 slides 001-051 (r1 detailed only the 21 known eq slides).

Method per slide: `unzip -l slide_NNN_recreated.pptx` for `ppt/media/*`; `ppt/slides/slide1.xml` (each pptx has exactly 1 slide)
checked for `mc:AlternateContent` (= OMML-wrapped) and `oMath`; eq sidecars = `recreated_pptx/build/assets/eq_*.json`
(all 180 eq sidecars live in `build/assets/`); sidecar PNGs matched to embedded media by md5 (byte-exact) or, if the PNG is
no longer on disk, by PNG IHDR dims vs sidecar `w_px`/`h_px`; rel_ids read from `ppt/slides/_rels/slide1.xml.rels`.
Wrapper contract: `scripts/18_omml_wrapper.py <in.pptx> <manifest.json>`; manifest rel_ids MUST be re-derived from the
current pptx at wrap time.

## Per-slide table (all 51)

| slide | media | p:pic | eq sidecars | embedded eq images (rel_id) | has eq image | wrapped (AltContent/oMath) | manifest path |
|---|---|---|---|---|---|---|---|
| 001 | 2 | 1 | 0 | - | no | 0/0 | - |
| 002 | 1 | 0 | 0 | - | no | 0/0 | - |
| 003 | 15 | 14 | 1 | - | no | 0/0 | - |
| 004 | 5 | 4 | 4 | eq_004_Yhatvec.json -> rId2; eq_004_Yvec.json -> rId1; eq_004_formula.json -> rId4; eq_004_norm.json -> rId3 | YES | 0/0 | - |
| 005 | 10 | 9 | 9 | eq_005_deriv1.json -> rId6; eq_005_deriv2.json -> rId7; eq_005_finalw.json -> rId9; eq_005_loss1.json -> rId1; eq_005_loss2.json -> rId2; eq_005_loss3.json -> rId3; eq_005_pinkfrac.json -> rId5; eq_005_remember1.json -> rId4; eq_005_remember2.json -> rId8 | YES | 0/0 | - |
| 006 | 1 | 0 | 0 | - | no | 0/0 | - |
| 007 | 1 | 0 | 0 | - | no | 0/0 | - |
| 008 | 1 | 0 | 0 | - | no | 0/0 | - |
| 009 | 3 | 2 | 4 | eq_009_left_attempt4.json -> rId1; eq_009_right_attempt4.json -> rId2 | YES | 4/12 | qa/slide009/omml_manifest.json; qa/slide009/omml_manifest_7.json |
| 010 | 1 | 0 | 0 | - | no | 0/0 | - |
| 011 | 1 | 0 | 0 | - | no | 0/0 | - |
| 012 | 1 | 0 | 0 | - | no | 0/0 | - |
| 013 | 4 | 3 | 0 | - | no | 0/0 | - |
| 014 | 4 | 3 | 0 | - | no | 0/0 | - |
| 015 | 10 | 9 | 9 | eq_015_deriv_l1.json -> rId6; eq_015_deriv_l2.json -> rId7; eq_015_eq1_l1.json -> rId1; eq_015_eq1_l2.json -> rId2; eq_015_eq1_l3.json -> rId3; eq_015_normal.json -> rId8; eq_015_peach_eq.json -> rId5; eq_015_redbox_eq.json -> rId4; eq_015_solution.json -> rId9 | YES | 0/0 | - |
| 016 | 1 | 0 | 0 | - | no | 0/0 | - |
| 017 | 4 | 3 | 0 | - | no | 0/0 | - |
| 018 | 4 | 3 | 0 | - | no | 0/0 | - |
| 019 | 1 | 0 | 0 | - | no | 0/0 | - |
| 020 | 1 | 0 | 0 | - | no | 0/0 | - |
| 021 | 7 | 6 | 6 | eq_021_d5685.json -> rId5; eq_021_det0.json -> rId2; eq_021_invexpr.json -> rId6; eq_021_lambda3.json -> rId4; eq_021_regmat.json -> rId3; eq_021_xtx.json -> rId1 | YES | 0/0 | - |
| 022 | 1 | 0 | 0 | - | no | 0/0 | - |
| 023 | 2 | 1 | 1 | eq_023_main.json -> rId1 | YES | 0/0 | qa/slide023/omml_manifest.json |
| 024 | 2 | 1 | 0 | - | no | 0/0 | - |
| 025 | 5 | 4 | 0 | - | no | 0/0 | - |
| 026 | 1 | 0 | 0 | - | no | 0/0 | - |
| 027 | 1 | 0 | 0 | - | no | 0/0 | - |
| 028 | 1 | 0 | 0 | - | no | 0/0 | - |
| 029 | 1 | 0 | 0 | - | no | 0/0 | - |
| 030 | 3 | 2 | 3 | eq_030_fx.json -> rId1; eq_030_x5_red.json -> rId2 | YES | 0/0 | - |
| 031 | 4 | 3 | 1 | eq_031_main.json -> rId1 | YES | 0/0 | - |
| 032 | 3 | 2 | 1 | eq_032_main.json -> rId2 | YES | 0/0 | - |
| 033 | 3 | 2 | 0 | - | no | 0/0 | - |
| 034 | 3 | 2 | 0 | - | no | 0/0 | - |
| 035 | 1 | 0 | 0 | - | no | 0/0 | - |
| 036 | 2 | 1 | 1 | eq_036_error.json -> rId1 | YES | 2/6 | qa/slide036/omml_manifest.json |
| 037 | 3 | 5 | 5 | eq_037_frac.json -> rId2,rId3; eq_037_sigma.json -> rId1,rId4,rId5 | YES | 0/0 | - |
| 038 | 1 | 0 | 0 | - | no | 0/0 | - |
| 039 | 3 | 6 | 1 | - | no | 2/6 | qa/slide039/omml_manifest.json |
| 040 | 1 | 0 | 0 | - | no | 0/0 | - |
| 041 | 7 | 20 | 0 | - | no | 0/0 | - |
| 042 | 9 | 66 | 0 | - | no | 0/0 | - |
| 043 | 8 | 57 | 14 | - | no | 0/0 | - |
| 044 | 53 | 72 | 62 | eq_044_arrD.json -> rId23,rId35,rId47; eq_044_arrDk.json -> rId59,rId65,rId71; eq_044_arrL.json -> rId30,rId42,rId54; eq_044_dx1_a.json -> rId19; eq_044_dx1_b.json -> rId20; eq_044_dx1_c.json -> rId21; eq_044_dx1_d.json -> rId22; eq_044_dx2_a.json -> rId31; eq_044_dx2_b.json -> rId32; eq_044_dx2_c.json -> rId29,rId33; eq_044_dx2_d.json -> rId34; eq_044_dx3_a.json -> rId43; eq_044_dx3_b.json -> rId44; eq_044_dx3_c.json -> rId41,rId45; eq_044_dx3_d.json -> rId46; eq_044_dx4_a.json -> rId55; eq_044_dx4_b.json -> rId56; eq_044_dx4_c.json -> rId53,rId57,rId63,rId69; eq_044_dx4_d.json -> rId58; eq_044_dx5_a.json -> rId61; eq_044_dx5_b.json -> rId62; eq_044_dx5_c.json -> rId53,rId57,rId63,rId69; eq_044_dx5_d.json -> rId64; eq_044_dx6_a.json -> rId67; eq_044_dx6_b.json -> rId68; eq_044_dx6_c.json -> rId53,rId57,rId63,rId69; eq_044_dx6_d.json -> rId70; eq_044_w1_a.json -> rId24,rId36,rId48; eq_044_w1_b.json -> rId25; eq_044_w1_c.json -> rId26,rId38,rId50; eq_044_w1_d.json -> rId27; eq_044_w1_e.json -> rId28,rId40,rId52; eq_044_w1_f.json -> rId29,rId33; eq_044_w2_a.json -> rId24,rId36,rId48; eq_044_w2_b.json -> rId37; eq_044_w2_c.json -> rId26,rId38,rId50; eq_044_w2_d.json -> rId39; eq_044_w2_e.json -> rId28,rId40,rId52; eq_044_w2_f.json -> rId41,rId45; eq_044_w3_a.json -> rId24,rId36,rId48; eq_044_w3_b.json -> rId49; eq_044_w3_c.json -> rId26,rId38,rId50; eq_044_w3_d.json -> rId51; eq_044_w3_e.json -> rId28,rId40,rId52; eq_044_w3_f.json -> rId53,rId57,rId63,rId69; eq_044_w4_a.json -> rId60,rId66,rId72; eq_044_w5_a.json -> rId60,rId66,rId72; eq_044_w6_a.json -> rId60,rId66,rId72 | YES | 0/0 | - |
| 045 | 1 | 0 | 0 | - | no | 0/0 | - |
| 046 | 19 | 18 | 3 | - | no | 0/0 | - |
| 047 | 1 | 0 | 9 | - | no | 0/0 | - |
| 048 | 7 | 6 | 9 | eq_r1_l.json -> rId1; eq_r2_l.json -> rId2; eq_r3_l.json -> rId3; eq_r4_l.json -> rId4; eq_r5_l.json -> rId5; eq_r6_l.json -> rId6 | YES | 0/0 | - |
| 049 | 1 | 0 | 2 | - | no | 0/0 | - |
| 050 | 9 | 30 | 6 | eq_050_Z1.json -> rId15; eq_050_Z2.json -> rId16; eq_050_Z3.json -> rId17; eq_050_finalW.json -> rId18 | YES | 0/0 | - |
| 051 | 16 | 41 | 26 | eq_051_dzlabel_1.json -> rId33; eq_051_dzlabel_2.json -> rId36; eq_051_dzlabel_3.json -> rId39; eq_051_initw.json -> rId13; eq_051_rowvec_1.json -> rId34; eq_051_rowvec_2.json -> rId37; eq_051_rowvec_3.json -> rId40; eq_051_step.json -> rId14; eq_051_wcol_green.json -> rId35,rId38,rId41 | YES | 0/0 | - |

## Wrap-needed summary

- Already OMML-wrapped (3): [9, 36, 39] — manifests: slide 009: qa/slide009/omml_manifest.json, qa/slide009/omml_manifest_7.json; slide 036: qa/slide036/omml_manifest.json; slide 039: qa/slide039/omml_manifest.json
- NOT wrapped but have embedded eq PNGs — wrap candidates (13): [4, 5, 15, 21, 23, 30, 31, 32, 37, 44, 48, 50, 51]
- Eq sidecars exist but NO eq image embedded in current pptx (6): [3, 39, 43, 46, 47, 49]

## Manifest paths (all omml_manifest*.json under recreated_pptx/qa)

- slide 009: `recreated_pptx/qa/slide009/omml_manifest.json`; `recreated_pptx/qa/slide009/omml_manifest_7.json`
- slide 023: `recreated_pptx/qa/slide023/omml_manifest.json`
- slide 036: `recreated_pptx/qa/slide036/omml_manifest.json`
- slide 039: `recreated_pptx/qa/slide039/omml_manifest.json`

## Detail: sidecar mathtext availability per eq slide

| slide | sidecars with mathtext | sidecars geometry-only (mathtext must be re-banked) |
|---|---|---|
| 003 | 1 (eq_003_remember.json) | 0 (-) |
| 004 | 4 (eq_004_Yhatvec.json; eq_004_Yvec.json; eq_004_formula.json; eq_004_norm.json) | 0 (-) |
| 005 | 9 (eq_005_deriv1.json; eq_005_deriv2.json; eq_005_finalw.json; eq_005_loss1.json; eq_005_loss2.json; eq_005_loss3.json; eq_005_pinkfrac.json; eq_005_remember1.json; eq_005_remember2.json) | 0 (-) |
| 009 | 2 (eq_009_left.json; eq_009_right.json) | 2 (eq_009_left_attempt4.json; eq_009_right_attempt4.json) |
| 015 | 9 (eq_015_deriv_l1.json; eq_015_deriv_l2.json; eq_015_eq1_l1.json; eq_015_eq1_l2.json; eq_015_eq1_l3.json; eq_015_normal.json; eq_015_peach_eq.json; eq_015_redbox_eq.json; eq_015_solution.json) | 0 (-) |
| 021 | 6 (eq_021_d5685.json; eq_021_det0.json; eq_021_invexpr.json; eq_021_lambda3.json; eq_021_regmat.json; eq_021_xtx.json) | 0 (-) |
| 023 | 1 (eq_023_main.json) | 0 (-) |
| 030 | 3 (eq_030_fx.json; eq_030_x5.json; eq_030_x5_red.json) | 0 (-) |
| 031 | 0 (-) | 1 (eq_031_main.json) |
| 032 | 0 (-) | 1 (eq_032_main.json) |
| 036 | 1 (eq_036_error.json) | 0 (-) |
| 037 | 0 (-) | 5 (eq_037_frac.json; eq_037_sigma.json; eq_037_sum_error.json; eq_037_sum_misclass.json; eq_037_sum_only.json) |
| 039 | 1 (eq_039_main.json) | 0 (-) |
| 043 | 14 (eq_043_dx1.json; eq_043_dx2.json; eq_043_dx3.json; eq_043_dx4.json; eq_043_dx5.json; eq_043_dx6.json; eq_043_initw.json; eq_043_step.json; eq_043_w1.json; eq_043_w2.json; eq_043_w3.json; eq_043_w4.json; eq_043_w5.json; eq_043_w6.json) | 0 (-) |
| 044 | 14 (eq_044_dx1.json; eq_044_dx2.json; eq_044_dx3.json; eq_044_dx4.json; eq_044_dx5.json; eq_044_dx6.json; eq_044_initw.json; eq_044_step.json; eq_044_w1.json; eq_044_w2.json; eq_044_w3.json; eq_044_w4.json; eq_044_w5.json; eq_044_w6.json) | 48 (eq_044_arrD.json; eq_044_arrDk.json; eq_044_arrL.json; eq_044_dx1_a.json; eq_044_dx1_b.json; eq_044_dx1_c.json; eq_044_dx1_d.json; eq_044_dx2_a.json; eq_044_dx2_b.json; eq_044_dx2_c.json; eq_044_dx2_d.json; eq_044_dx3_a.json; eq_044_dx3_b.json; eq_044_dx3_c.json; eq_044_dx3_d.json; eq_044_dx4_a.json; eq_044_dx4_b.json; eq_044_dx4_c.json; eq_044_dx4_d.json; eq_044_dx5_a.json; eq_044_dx5_b.json; eq_044_dx5_c.json; eq_044_dx5_d.json; eq_044_dx6_a.json; eq_044_dx6_b.json; eq_044_dx6_c.json; eq_044_dx6_d.json; eq_044_w1_a.json; eq_044_w1_b.json; eq_044_w1_c.json; eq_044_w1_d.json; eq_044_w1_e.json; eq_044_w1_f.json; eq_044_w2_a.json; eq_044_w2_b.json; eq_044_w2_c.json; eq_044_w2_d.json; eq_044_w2_e.json; eq_044_w2_f.json; eq_044_w3_a.json; eq_044_w3_b.json; eq_044_w3_c.json; eq_044_w3_d.json; eq_044_w3_e.json; eq_044_w3_f.json; eq_044_w4_a.json; eq_044_w5_a.json; eq_044_w6_a.json) |
| 046 | 0 (-) | 3 (eq_046_final_w.json; eq_046_initial_w.json; eq_046_step_eta.json) |
| 047 | 7 (eq_047_W.json; eq_047_dz_1.json; eq_047_dz_2.json; eq_047_dz_3.json; eq_047_v_1.json; eq_047_v_2.json; eq_047_v_3.json) | 2 (eq_047_span2.json; eq_047_span3.json) |
| 048 | 0 (-) | 9 (eq_r1_l.json; eq_r1_w.json; eq_r2_l.json; eq_r3_l.json; eq_r4_l.json; eq_r5_l.json; eq_r6_l.json; eq_r_kw.json; eq_slide048_r1.json) |
| 049 | 0 (-) | 2 (eq_slide049_wcol.json; eq_slide049_wcol_paren.json) |
| 050 | 1 (eq_050_finalW.json) | 5 (eq_050_Z1.json; eq_050_Z2.json; eq_050_Z3.json; eq_050_eta.json; eq_050_initialW.json) |
| 051 | 22 (eq_051_col_aug_1.json; eq_051_col_aug_2.json; eq_051_col_aug_3.json; eq_051_col_aug_4.json; eq_051_col_aug_5.json; eq_051_col_aug_6.json; eq_051_col_green.json; eq_051_col_initw.json; eq_051_col_sample_1.json; eq_051_col_sample_2.json; eq_051_col_sample_3.json; eq_051_col_sample_4.json; eq_051_col_sample_5.json; eq_051_col_sample_6.json; eq_051_col_z_1.json; eq_051_col_z_2.json; eq_051_col_z_3.json; eq_051_dzlabel_1.json; eq_051_rowvec_1.json; eq_051_rowvec_2.json; eq_051_rowvec_3.json; eq_051_step.json) | 4 (eq_051_dzlabel_2.json; eq_051_dzlabel_3.json; eq_051_initw.json; eq_051_wcol_green.json) |

Notes:
- rel_id lists combine md5-exact matches with IHDR-dims fallback matches; where the on-disk PNG bytes differ from the embedded media, dims matching can list several rel_ids sharing the same pixel size (superset — re-derive exactly at wrap time per contract).
- eq_index_014 / eq_index_042 sidecars are matrix-bracket assets on slides 14/42, not equations (per r1).
- Slide 23 wrapper previously FAIL-LOUD (`\underline` unsupported) — `qa/slide023/omml_prepass_note.md`; manifest banked, not wrapped.
- Slide 9 has two banked manifests (`omml_manifest.json`, `omml_manifest_7.json`); slide already wrapped.
- Slides 31, 32, 37, 44, 48, 50, 51 have embedded eq PNGs whose sidecars are geometry-only — mathtext must be re-banked from build scripts/evidence before manifest authoring.
- PREP ONLY: no wrap was run; no pptx modified.
