# OMML_INVENTORY_r1 — S9 closeout prep (deck 03_ridger_regression_gradient_descent)

Generated 2026-10-31 by a read-only inventory pass (PREP ONLY — nothing wrapped, no pptx modified, no git).
Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`. Eq-slide list per deck docs:
3,4,5,9,15,21,23,30,31,32,36,37,39,43,44,46,47,48,49,50,51 — verified against `recreated_pptx/build/slide_NNN.js`
(mathtext/addImage usage) and `recreated_pptx/build/assets/eq_*.json` sidecars. Sidecars exist for exactly this list
(plus non-eq `eq_index_014/042` matrix-bracket assets on slides 14/42, which are not equation slides).

Method: each `slide_NNN_recreated.pptx` was unzipped in-memory; `mc:AlternateContent` in `ppt/slides/slideN.xml`
= wrapped; rel_ids re-derived from the CURRENT pptx by matching `ppt/media/*` to sidecar PNGs by md5 (byte-exact)
or, where the PNG is no longer on disk, by PNG IHDR dimensions vs the sidecar's `w_px`/`h_px` (marked `dims`).
Wrapper contract: `scripts/18_omml_wrapper.py <in.pptx> <manifest.json>` (exists at project root); manifest rel_ids
MUST be re-derived from the current pptx at wrap time.

## Per-slide inventory

| slide | sidecars | manifest(s) | wrapped | embedded eq images (rel_id current) | ready-to-wrap |
|---|---|---|---|---|---|
| 3 | 1 | - | no | none | NO (no embedded eq PNG) |
| 4 | 4 | - | no | eq_004_Yhatvec.png [md5] -> rId2; eq_004_Yvec.png [md5] -> rId1; eq_004_formula.png [md5] -> rId4; eq_004_norm.png [md5] -> rId3 | yes |
| 5 | 11 | - | no | eq_005_deriv1.png [dims] -> rId6; eq_005_deriv2.png [dims] -> rId7; eq_005_finalw.png [dims] -> rId9; eq_005_loss1.png [dims] -> rId1; eq_005_loss2.png [dims] -> rId2; eq_005_loss3.png [dims] -> rId3; eq_005_pinkfrac.png [dims] -> rId5; eq_005_remember1.png [dims] -> rId4; eq_005_remember2.png [dims] -> rId8 | yes |
| 9 | 4 | omml_manifest.json, omml_manifest_7.json | YES | eq_009_left_attempt4.png [dims] -> rId1; eq_009_right_attempt4.png [dims] -> rId2 | ALREADY WRAPPED |
| 15 | 9 | - | no | eq_015_deriv_l1.png [md5] -> rId6; eq_015_deriv_l2.png [md5] -> rId7; eq_015_eq1_l1.png [md5] -> rId1; eq_015_eq1_l2.png [md5] -> rId2; eq_015_eq1_l3.png [md5] -> rId3; eq_015_normal.png [md5] -> rId8; eq_015_peach_eq.png [md5] -> rId5; eq_015_redbox_eq.png [md5] -> rId4; eq_015_solution.png [md5] -> rId9 | yes |
| 21 | 6 | - | no | eq_021_d5685.png [md5] -> rId5; eq_021_det0.png [md5] -> rId2; eq_021_invexpr.png [md5] -> rId6; eq_021_lambda3.png [md5] -> rId4; eq_021_regmat.png [md5] -> rId3; eq_021_xtx.png [md5] -> rId1 | yes |
| 23 | 1 | omml_manifest.json | no | eq_023_main.png [dims] -> rId1 | yes |
| 30 | 3 | - | no | eq_030_fx.png [dims] -> rId1; eq_030_x5_red.png [dims] -> rId2 | yes |
| 31 | 1 | - | no | eq_031_main.png [dims] -> rId1 | yes (sidecar lacks mathtext — re-bank from build/evidence first) |
| 32 | 1 | - | no | eq_032_main.png [dims] -> rId2 | yes (sidecar lacks mathtext — re-bank from build/evidence first) |
| 36 | 1 | omml_manifest.json | YES | eq_036_error.png [dims] -> rId1 | ALREADY WRAPPED |
| 37 | 5 | - | no | eq_037_frac.png [dims] -> rId2,rId3; eq_037_sigma.png [dims] -> rId1,rId4,rId5 | yes (sidecar lacks mathtext — re-bank from build/evidence first) |
| 39 | 1 | omml_manifest.json | YES | none | ALREADY WRAPPED |
| 43 | 14 | - | no | none | NO (no embedded eq PNG) |
| 44 | 62 | - | no | eq_044_arrD.png [md5] -> rId23,rId35,rId47; eq_044_arrDk.png [md5] -> rId59,rId65,rId71; eq_044_arrL.png [md5] -> rId30,rId42,rId54; eq_044_dx1_a.png [md5] -> rId19; eq_044_dx1_b.png [md5] -> rId20; eq_044_dx1_c.png [md5] -> rId21; eq_044_dx1_d.png [md5] -> rId22; eq_044_dx2_a.png [md5] -> rId31; eq_044_dx2_b.png [md5] -> rId32; eq_044_dx2_c.png [md5] -> rId29; eq_044_dx2_d.png [md5] -> rId34; eq_044_dx3_a.png [md5] -> rId43; eq_044_dx3_b.png [md5] -> rId44; eq_044_dx3_c.png [md5] -> rId41; eq_044_dx3_d.png [md5] -> rId46; eq_044_dx4_a.png [md5] -> rId55; eq_044_dx4_b.png [md5] -> rId56; eq_044_dx4_c.png [md5] -> rId53; eq_044_dx4_d.png [md5] -> rId58; eq_044_dx5_a.png [md5] -> rId61; eq_044_dx5_b.png [md5] -> rId62; eq_044_dx5_c.png [md5] -> rId53; eq_044_dx5_d.png [md5] -> rId64; eq_044_dx6_a.png [md5] -> rId67; eq_044_dx6_b.png [md5] -> rId68; eq_044_dx6_c.png [md5] -> rId53; eq_044_dx6_d.png [md5] -> rId70; eq_044_w1_a.png [md5] -> rId24; eq_044_w1_b.png [md5] -> rId25; eq_044_w1_c.png [md5] -> rId26; eq_044_w1_d.png [md5] -> rId27; eq_044_w1_e.png [md5] -> rId28; eq_044_w1_f.png [md5] -> rId29; eq_044_w2_a.png [md5] -> rId24; eq_044_w2_b.png [md5] -> rId37; eq_044_w2_c.png [md5] -> rId26; eq_044_w2_d.png [md5] -> rId39; eq_044_w2_e.png [md5] -> rId28; eq_044_w2_f.png [md5] -> rId41; eq_044_w3_a.png [md5] -> rId24; eq_044_w3_b.png [md5] -> rId49; eq_044_w3_c.png [md5] -> rId26; eq_044_w3_d.png [md5] -> rId51; eq_044_w3_e.png [md5] -> rId28; eq_044_w3_f.png [md5] -> rId53; eq_044_w4_a.png [md5] -> rId60; eq_044_w5_a.png [md5] -> rId60; eq_044_w6_a.png [md5] -> rId60 | yes (sidecar lacks mathtext — re-bank from build/evidence first) |
| 46 | 3 | - | no | none | NO (no embedded eq PNG) |
| 47 | 9 | - | no | none | NO (no embedded eq PNG) |
| 48 | 7 | - | no | eq_r1_l.png [dims] -> rId1; eq_r2_l.png [dims] -> rId2; eq_r3_l.png [dims] -> rId3; eq_r4_l.png [dims] -> rId4; eq_r5_l.png [dims] -> rId5; eq_r6_l.png [dims] -> rId6 | yes (sidecar lacks mathtext — re-bank from build/evidence first) |
| 49 | 2 | - | no | none | NO (no embedded eq PNG) |
| 50 | 6 | - | no | eq_050_Z1.png [dims] -> rId15; eq_050_Z2.png [dims] -> rId16; eq_050_Z3.png [dims] -> rId17; eq_050_finalW.png [dims] -> rId18 | yes |
| 51 | 27 | - | no | eq_051_dzlabel_1.png [md5] -> rId33; eq_051_dzlabel_2.png [md5] -> rId36; eq_051_dzlabel_3.png [md5] -> rId39; eq_051_initw.png [md5] -> rId13; eq_051_rowvec_1.png [md5] -> rId34; eq_051_rowvec_2.png [md5] -> rId37; eq_051_rowvec_3.png [md5] -> rId40; eq_051_step.png [md5] -> rId14; eq_051_wcol_green.png [md5] -> rId35,rId38,rId41; eq_051_wcol_green.png [md5] -> rId35,rId38,rId41 | yes |

## Per-slide detail

### slide 3 — pptx `recreated_pptx/slide_003_recreated.pptx`, wrapped=False, media images=14
- sidecar `recreated_pptx/build/assets/eq_003_remember.json` img=eq_003_remember.png not-embedded match=None rel_now=None fs=18 color=000000 mathtext=`y = W^{T}X = X^{T}W`
- NOTE: sidecar eq_003_remember.json is superseded — note says native text runs with underline; its PNG is NOT embedded (14 media are paren-arc PNGs from qa/slide003/parens/). No wrap target in current pptx.

### slide 4 — pptx `recreated_pptx/slide_004_recreated.pptx`, wrapped=False, media images=4
- sidecar `recreated_pptx/build/assets/eq_004_Yhatvec.json` img=eq_004_Yhatvec.png EMBEDDED match=md5 rel_now=rId2 fs=None color=mixed(black lead / red bars+entries / red subscript) mathtext=`COMPOSED: Let \ \underline{\mathbf{\hat{Y}}}\ = | drawn parens [504, 530] | pieces ['\\wid`
- sidecar `recreated_pptx/build/assets/eq_004_Yvec.json` img=eq_004_Yvec.png EMBEDDED match=md5 rel_now=rId1 fs=None color=mixed(black lead / red bars+entries / red subscript) mathtext=`COMPOSED: Let \ \underline{\mathbf{Y}}\ = | drawn parens [159, 184] | pieces ['y_1', 'y_2'`
- sidecar `recreated_pptx/build/assets/eq_004_formula.json` img=eq_004_formula.png EMBEDDED match=md5 rel_now=rId4 fs=14.0 color=000000 mathtext=`Loss = \left\|Y - \mathbf{\hat{Y}}\right\|_2 = \left(Y - \mathbf{\hat{Y}}\right)^{T} \left`
- sidecar `recreated_pptx/build/assets/eq_004_norm.json` img=eq_004_norm.png EMBEDDED match=md5 rel_now=rId3 fs=14.0 color=000000 mathtext=`\|a\|_2 = a^{T} a`

### slide 5 — pptx `recreated_pptx/slide_005_recreated.pptx`, wrapped=False, media images=9
- sidecar `recreated_pptx/build/assets/eq_005_deriv1.json` img=eq_005_deriv1.png EMBEDDED match=dims rel_now=rId6 fs=22.7 color=000000 mathtext=`\dfrac{\partial Loss}{\partial W} = 0 = \dfrac{1}{2}\left[(XW)^{T}(X) + (X)^{T}(XW) - 2(X)`
- sidecar `recreated_pptx/build/assets/eq_005_deriv2.json` img=eq_005_deriv2.png EMBEDDED match=dims rel_now=rId7 fs=22.7 color=000000 mathtext=`\dfrac{\partial Loss}{\partial W} = 0 = \dfrac{1}{2}\left[2X^{T}XW - 2X^{T}Y\right] \right`
- sidecar `recreated_pptx/build/assets/eq_005_finalw.json` img=eq_005_finalw.png EMBEDDED match=dims rel_now=rId9 fs=24.2 color=000000 mathtext=`W = (X^{T}X)^{-1}X^{T}Y`
- sidecar `recreated_pptx/build/assets/eq_005_loss1.json` img=eq_005_loss1.png EMBEDDED match=dims rel_now=rId1 fs=19.8 color=000000 mathtext=`Loss = \dfrac{1}{2}\,(Y-\hat{Y})^{T}(Y-\hat{Y}) = \dfrac{1}{2}\,(Y-XW)^{T}(Y-XW)`
- sidecar `recreated_pptx/build/assets/eq_005_loss2.json` img=eq_005_loss2.png EMBEDDED match=dims rel_now=rId2 fs=23.4 color=000000 mathtext=`Loss = \dfrac{1}{2}\left[Y^{T}Y + (XW)^{T}(XW) - Y^{T}(XW) - (XW)^{T}Y\right]`
- sidecar `recreated_pptx/build/assets/eq_005_loss3.json` img=eq_005_loss3.png EMBEDDED match=dims rel_now=rId3 fs=22.8 color=000000 mathtext=`Loss = \dfrac{1}{2}\left[Y^{T}Y + (XW)^{T}(XW) - 2(XW)^{T}Y\right]`
- sidecar `recreated_pptx/build/assets/eq_005_pinkfrac.json` img=eq_005_pinkfrac.png EMBEDDED match=dims rel_now=rId5 fs=18.0 color=000000 mathtext=`\dfrac{\partial Loss}{\partial W} = 0`
- sidecar `recreated_pptx/build/assets/eq_005_remember1.json` img=eq_005_remember1.png EMBEDDED match=dims rel_now=rId4 fs=22.0 color=000000 mathtext=`Y^{T}(XW) = (XW)^{T}Y`
- sidecar `recreated_pptx/build/assets/eq_005_remember2.json` img=eq_005_remember2.png EMBEDDED match=dims rel_now=rId8 fs=24.4 color=000000 mathtext=`X^{T}(XW) = (XW)^{T}X`
- sidecar `recreated_pptx/qa/slide005/eq_005_remember2_Yfirst_superseded.json` img=eq_005_remember2.png not-embedded match=None rel_now=None fs=24.4 color=000000 mathtext=`Y^{T}(XW) = (XW)^{T}Y`
- sidecar `recreated_pptx/qa/slide005/eq_fit_slide005.json` img=None not-embedded match=None rel_now=None fs=None color=None mathtext=``

### slide 9 — pptx `recreated_pptx/slide_009_recreated.pptx`, wrapped=True, media images=2
- manifest: `recreated_pptx/qa/slide009/omml_manifest.json`
- manifest: `recreated_pptx/qa/slide009/omml_manifest_7.json`
- sidecar `recreated_pptx/build/assets/eq_009_left.json` img=eq_009_left.png not-embedded match=None rel_now=None fs=14.5 color=000000 mathtext=`50.85^{2} = 2585`
- sidecar `recreated_pptx/build/assets/eq_009_left_attempt4.json` img=eq_009_left_attempt4.png EMBEDDED match=dims rel_now=rId1 fs=12.1 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_009_right.json` img=eq_009_right.png not-embedded match=None rel_now=None fs=14.5 color=000000 mathtext=`63.64^{2} = 4050`
- sidecar `recreated_pptx/build/assets/eq_009_right_attempt4.json` img=eq_009_right_attempt4.png EMBEDDED match=dims rel_now=rId2 fs=12.1 color=000000 mathtext=``

### slide 15 — pptx `recreated_pptx/slide_015_recreated.pptx`, wrapped=False, media images=9
- sidecar `recreated_pptx/build/assets/eq_015_deriv_l1.json` img=eq_015_deriv_l1.png EMBEDDED match=md5 rel_now=rId6 fs=22 color=000000 mathtext=`\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0 = \frac{1}{2}[(XW)^{T}(X) + (`
- sidecar `recreated_pptx/build/assets/eq_015_deriv_l2.json` img=eq_015_deriv_l2.png EMBEDDED match=md5 rel_now=rId7 fs=21 color=000000 mathtext=`\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0 = \frac{1}{2}[2X^{T}XW - 2X^{`
- sidecar `recreated_pptx/build/assets/eq_015_eq1_l1.json` img=eq_015_eq1_l1.png EMBEDDED match=md5 rel_now=rId1 fs=17 color=000000 mathtext=`J(\underline{W}) = \frac{1}{2}(Y-\hat{Y})^{T}(Y-\hat{Y}) + \frac{1}{2}\lambda \underline{W`
- sidecar `recreated_pptx/build/assets/eq_015_eq1_l2.json` img=eq_015_eq1_l2.png EMBEDDED match=md5 rel_now=rId2 fs=18 color=000000 mathtext=`J(\underline{W}) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW) - Y^{T}(XW) - (XW)^{T}Y] + \frac{1}{2`
- sidecar `recreated_pptx/build/assets/eq_015_eq1_l3.json` img=eq_015_eq1_l3.png EMBEDDED match=md5 rel_now=rId3 fs=18 color=000000 mathtext=`J(\underline{W}) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW) - 2(XW)^{T}Y] + \frac{1}{2}\lambda \u`
- sidecar `recreated_pptx/build/assets/eq_015_normal.json` img=eq_015_normal.png EMBEDDED match=md5 rel_now=rId8 fs=30 color=000000 mathtext=`(X^{T}X + \lambda I)\underline{W} = X^{T}Y`
- sidecar `recreated_pptx/build/assets/eq_015_peach_eq.json` img=eq_015_peach_eq.png EMBEDDED match=md5 rel_now=rId5 fs=19 color=000000 mathtext=`\frac{\partial W^{T}W}{\partial W} = 2W`
- sidecar `recreated_pptx/build/assets/eq_015_redbox_eq.json` img=eq_015_redbox_eq.png EMBEDDED match=md5 rel_now=rId4 fs=26 color=000000 mathtext=`\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0`
- sidecar `recreated_pptx/build/assets/eq_015_solution.json` img=eq_015_solution.png EMBEDDED match=md5 rel_now=rId9 fs=25 color=000000 mathtext=`\underline{W} = (X^{T}X + \lambda I)^{-1}X^{T}Y`

### slide 21 — pptx `recreated_pptx/slide_021_recreated.pptx`, wrapped=False, media images=6
- sidecar `recreated_pptx/build/assets/eq_021_d5685.json` img=eq_021_d5685.png EMBEDDED match=md5 rel_now=rId5 fs=20.5 color=multi mathtext=`|X^T X| = 5685`
- sidecar `recreated_pptx/build/assets/eq_021_det0.json` img=eq_021_det0.png EMBEDDED match=md5 rel_now=rId2 fs=22.0 color=multi mathtext=`|X^T X| = 0`
- sidecar `recreated_pptx/build/assets/eq_021_invexpr.json` img=eq_021_invexpr.png EMBEDDED match=md5 rel_now=rId6 fs=24.0 color=multi mathtext=`(\underline{X}^T \underline{X} + \lambda I)^{-1}`
- sidecar `recreated_pptx/build/assets/eq_021_lambda3.json` img=eq_021_lambda3.png EMBEDDED match=md5 rel_now=rId4 fs=18.0 color=#008000 mathtext=`\lambda=3`
- sidecar `recreated_pptx/build/assets/eq_021_regmat.json` img=eq_021_regmat.png EMBEDDED match=md5 rel_now=rId3 fs=24.0 color=multi mathtext=`(X^T X + \lambda I)`
- sidecar `recreated_pptx/build/assets/eq_021_xtx.json` img=eq_021_xtx.png EMBEDDED match=md5 rel_now=rId1 fs=22.0 color=#C00000 mathtext=`X^T X`

### slide 23 — pptx `recreated_pptx/slide_023_recreated.pptx`, wrapped=False, media images=1
- manifest: `recreated_pptx/qa/slide023/omml_manifest.json`
- sidecar `recreated_pptx/build/assets/eq_023_main.json` img=eq_023_main.png EMBEDDED match=dims rel_now=rId1 fs=32.5 color=000000 mathtext=`\underline{W} = \left( X^T X + \lambda I \right)^{-1} X^T \underline{Y}`

### slide 30 — pptx `recreated_pptx/slide_030_recreated.pptx`, wrapped=False, media images=2
- sidecar `recreated_pptx/build/assets/eq_030_fx.json` img=eq_030_fx.png EMBEDDED match=dims rel_now=rId1 fs=20 color=000000 mathtext=`f(x)=(x-5)^{2}+1`
- sidecar `recreated_pptx/build/assets/eq_030_x5.json` img=eq_030_x5.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`X=5`
- sidecar `recreated_pptx/build/assets/eq_030_x5_red.json` img=eq_030_x5_red.png EMBEDDED match=dims rel_now=rId2 fs=18 color=C00000 mathtext=`X\ =\ 5`

### slide 31 — pptx `recreated_pptx/slide_031_recreated.pptx`, wrapped=False, media images=3
- sidecar `recreated_pptx/build/assets/eq_031_main.json` img=eq_031_main.png EMBEDDED match=dims rel_now=rId1 fs=24.0 color=000000 mathtext=``
- NOTE: eq_031_main sidecar is geometry-only (no mathtext field; mathtext source is the slide_031.js/gen pipeline). Embedded rId1 (1690x229). Plus curve_032.png (766x1575, rId2) and arrow_031 (226x351, rId3).

### slide 32 — pptx `recreated_pptx/slide_032_recreated.pptx`, wrapped=False, media images=2
- sidecar `recreated_pptx/build/assets/eq_032_main.json` img=eq_032_main.png EMBEDDED match=dims rel_now=rId2 fs=15.0 color=000000 mathtext=``
- NOTE: eq_032_main embedded as rId2 (1062x149, dims); media image-1-1 (766x1575, rId1) is the shared curve_032.png, not an equation. Sidecar geometry-only.

### slide 36 — pptx `recreated_pptx/slide_036_recreated.pptx`, wrapped=True, media images=1
- manifest: `recreated_pptx/qa/slide036/omml_manifest.json`
- sidecar `recreated_pptx/build/assets/eq_036_error.json` img=eq_036_error.png EMBEDDED match=dims rel_now=rId1 fs=21.0 color=000000 mathtext=`Error = \sum_{all misclassified vectors(i)} W^T X_i \Rightarrow (W^T X_i) take positive an`

### slide 37 — pptx `recreated_pptx/slide_037_recreated.pptx`, wrapped=False, media images=2
- sidecar `recreated_pptx/build/assets/eq_037_frac.json` img=eq_037_frac.png EMBEDDED match=dims rel_now=rId2,rId3 fs=34.0 color=#000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_037_sigma.json` img=eq_037_sigma.png EMBEDDED match=dims rel_now=rId1,rId4,rId5 fs=30.0 color=#000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_037_sum_error.json` img=eq_037_sum_error.png not-embedded match=None rel_now=None fs=17.8 color=#FF0000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_037_sum_misclass.json` img=eq_037_sum_misclass.png not-embedded match=None rel_now=None fs=22.5 color=#FF0000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_037_sum_only.json` img=eq_037_sum_only.png not-embedded match=None rel_now=None fs=22.5 color=#FF0000 mathtext=``
- NOTE: Prepass (qa/slide037/omml_prepass_note.md): NOT WRAPPED, blocked on spec fidelity — sidecars have NO mathtext and the 5 pics are anisotropically rescaled in the certified pptx; needs mathtext re-bank + per-instance fontsize re-derivation. Embedded: sigma -> rId1,rId4,rId5; frac -> rId2,rId3.

### slide 39 — pptx `recreated_pptx/slide_039_recreated.pptx`, wrapped=True, media images=2
- manifest: `recreated_pptx/qa/slide039/omml_manifest.json`
- sidecar `recreated_pptx/build/assets/eq_039_main.json` img=eq_039_main.png not-embedded match=None rel_now=None fs=17.0 color=000000 mathtext=`W^{(updated)}=W^{old}-\eta\,\delta_{i}\,X_{i}`
- NOTE: eq_039_main.json sidecar carries no w_px/h_px; embedded by position as image-1-4 (1676x179, rId4) — matches banked manifest qa/slide039/omml_manifest.json (rId4). Already wrapped. image-1-1 (108x91, rId1..3,5,6) is the evt_039 arrow, not an equation.

### slide 43 — pptx `recreated_pptx/slide_043_recreated.pptx`, wrapped=False, media images=7
- sidecar `recreated_pptx/build/assets/eq_043_dx1.json` img=eq_043_dx1.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`d(x_1) = |\,1\;\;1\;\;1\,|\,(4;\,-10;\,-8) = -14`
- sidecar `recreated_pptx/build/assets/eq_043_dx2.json` img=eq_043_dx2.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`d(x_2) = |\,1\;\;2\;\;1\,|\,(6;\,-8;\,-6) = -14`
- sidecar `recreated_pptx/build/assets/eq_043_dx3.json` img=eq_043_dx3.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`d(x_3) = |\,1\;\;1\;\;2\,|\,(8;\,-4;\,-4) = -4`
- sidecar `recreated_pptx/build/assets/eq_043_dx4.json` img=eq_043_dx4.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`d(x_4) = |\,1\;\;5\;\;4\,|\,(10;\,-2;\,0) = 0`
- sidecar `recreated_pptx/build/assets/eq_043_dx5.json` img=eq_043_dx5.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`d(x_5) = |\,1\;\;6\;\;5\,|\,(8;\,-12;\,-8) = -104`
- sidecar `recreated_pptx/build/assets/eq_043_dx6.json` img=eq_043_dx6.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`d(x_6) = |\,1\;\;6\;\;6\,|\,(8;\,-12;\,-8) = -112`
- sidecar `recreated_pptx/build/assets/eq_043_initw.json` img=eq_043_initw.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`\mathrm{Initial}\;W = (4;\,-2;\,-2)`
- sidecar `recreated_pptx/build/assets/eq_043_step.json` img=eq_043_step.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`\mathrm{Step}\;\eta = 2`
- sidecar `recreated_pptx/build/assets/eq_043_w1.json` img=eq_043_w1.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`W = (4;\,-10;\,-8) + 2\,(1;\,1;\,1) = (6;\,-8;\,-6)`
- sidecar `recreated_pptx/build/assets/eq_043_w2.json` img=eq_043_w2.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`W = (6;\,-8;\,-6) + 2\,(1;\,2;\,1) = (8;\,-4;\,-4)`
- sidecar `recreated_pptx/build/assets/eq_043_w3.json` img=eq_043_w3.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`W = (8;\,-4;\,-4) + 2\,(1;\,1;\,2) = (10;\,-2;\,0)`
- sidecar `recreated_pptx/build/assets/eq_043_w4.json` img=eq_043_w4.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`W = (10;\,-2;\,0) - 2\,(1;\,5;\,4) = (8;\,-12;\,-8)`
- sidecar `recreated_pptx/build/assets/eq_043_w5.json` img=eq_043_w5.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`W = (8;\,-12;\,-8)`
- sidecar `recreated_pptx/build/assets/eq_043_w6.json` img=eq_043_w6.png not-embedded match=None rel_now=None fs=20.0 color=000000 mathtext=`W = (8;\,-12;\,-8)`
- NOTE: 14 eq_043_* sidecars exist (dx1-6, w1-6, initw, step; PNGs on disk) but NONE are embedded in the current pptx. Current media: eq043_mx1/2/3.png (125x22x, rId3/rId4/rId5) + 4 parens042 tall-paren PNGs (29x341). eq_043_dx*/w* renders are superseded by the mx/paren composition.

### slide 44 — pptx `recreated_pptx/slide_044_recreated.pptx`, wrapped=False, media images=52
- sidecar `recreated_pptx/build/assets/eq_044_arrD.json` img=eq_044_arrD.png EMBEDDED match=md5 rel_now=rId23,rId35,rId47 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_arrDk.json` img=eq_044_arrDk.png EMBEDDED match=md5 rel_now=rId59,rId65,rId71 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_arrL.json` img=eq_044_arrL.png EMBEDDED match=md5 rel_now=rId30,rId42,rId54 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx1.json` img=eq_044_dx1.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`d(x_1) = [1 \; 1 \; 1; \; -12; \; -8] = -12`
- sidecar `recreated_pptx/build/assets/eq_044_dx1_a.json` img=eq_044_dx1_a.png EMBEDDED match=md5 rel_now=rId19 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx1_b.json` img=eq_044_dx1_b.png EMBEDDED match=md5 rel_now=rId20 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx1_c.json` img=eq_044_dx1_c.png EMBEDDED match=md5 rel_now=rId21 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx1_d.json` img=eq_044_dx1_d.png EMBEDDED match=md5 rel_now=rId22 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx2.json` img=eq_044_dx2.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`d(x_2) = [1 \; 2 \; 1; \; -10; \; -6] = -16`
- sidecar `recreated_pptx/build/assets/eq_044_dx2_a.json` img=eq_044_dx2_a.png EMBEDDED match=md5 rel_now=rId31 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx2_b.json` img=eq_044_dx2_b.png EMBEDDED match=md5 rel_now=rId32 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx2_c.json` img=eq_044_dx2_c.png EMBEDDED match=md5 rel_now=rId29 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx2_d.json` img=eq_044_dx2_d.png EMBEDDED match=md5 rel_now=rId34 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx3.json` img=eq_044_dx3.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`d(x_3) = [1 \; 1 \; 2; \; -6; \; -2] = -4`
- sidecar `recreated_pptx/build/assets/eq_044_dx3_a.json` img=eq_044_dx3_a.png EMBEDDED match=md5 rel_now=rId43 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx3_b.json` img=eq_044_dx3_b.png EMBEDDED match=md5 rel_now=rId44 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx3_c.json` img=eq_044_dx3_c.png EMBEDDED match=md5 rel_now=rId41 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx3_d.json` img=eq_044_dx3_d.png EMBEDDED match=md5 rel_now=rId46 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx4.json` img=eq_044_dx4.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`d(x_4) = [1 \; 5 \; 4; \; -4; \; 0] = -6`
- sidecar `recreated_pptx/build/assets/eq_044_dx4_a.json` img=eq_044_dx4_a.png EMBEDDED match=md5 rel_now=rId55 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx4_b.json` img=eq_044_dx4_b.png EMBEDDED match=md5 rel_now=rId56 fs=14.0 color=0000C8 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx4_c.json` img=eq_044_dx4_c.png EMBEDDED match=md5 rel_now=rId53 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx4_d.json` img=eq_044_dx4_d.png EMBEDDED match=md5 rel_now=rId58 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx5.json` img=eq_044_dx5.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`d(x_5) = [1 \; 6 \; 5; \; -14; \; -10] = -10`
- sidecar `recreated_pptx/build/assets/eq_044_dx5_a.json` img=eq_044_dx5_a.png EMBEDDED match=md5 rel_now=rId61 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx5_b.json` img=eq_044_dx5_b.png EMBEDDED match=md5 rel_now=rId62 fs=14.0 color=0000C8 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx5_c.json` img=eq_044_dx5_c.png EMBEDDED match=md5 rel_now=rId53 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx5_d.json` img=eq_044_dx5_d.png EMBEDDED match=md5 rel_now=rId64 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx6.json` img=eq_044_dx6.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`d(x_6) = [1 \; 6 \; 6; \; -14; \; -4] = -4`
- sidecar `recreated_pptx/build/assets/eq_044_dx6_a.json` img=eq_044_dx6_a.png EMBEDDED match=md5 rel_now=rId67 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx6_b.json` img=eq_044_dx6_b.png EMBEDDED match=md5 rel_now=rId68 fs=14.0 color=0000C8 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx6_c.json` img=eq_044_dx6_c.png EMBEDDED match=md5 rel_now=rId53 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_dx6_d.json` img=eq_044_dx6_d.png EMBEDDED match=md5 rel_now=rId70 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_initw.json` img=eq_044_initw.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`\mathrm{Initial}\; W = [4; \; -2; \; -2]`
- sidecar `recreated_pptx/build/assets/eq_044_step.json` img=eq_044_step.png not-embedded match=None rel_now=None fs=20 color=C00000 mathtext=`\mathrm{Step}\; \eta = 2`
- sidecar `recreated_pptx/build/assets/eq_044_w1.json` img=eq_044_w1.png not-embedded match=None rel_now=None fs=20 color=C00000 mathtext=`W = [4; \; -2] + 2 * [3; \; -2] = [10; \; -6]`
- sidecar `recreated_pptx/build/assets/eq_044_w1_a.json` img=eq_044_w1_a.png EMBEDDED match=md5 rel_now=rId24 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w1_b.json` img=eq_044_w1_b.png EMBEDDED match=md5 rel_now=rId25 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w1_c.json` img=eq_044_w1_c.png EMBEDDED match=md5 rel_now=rId26 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w1_d.json` img=eq_044_w1_d.png EMBEDDED match=md5 rel_now=rId27 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w1_e.json` img=eq_044_w1_e.png EMBEDDED match=md5 rel_now=rId28 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w1_f.json` img=eq_044_w1_f.png EMBEDDED match=md5 rel_now=rId29 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w2.json` img=eq_044_w2.png not-embedded match=None rel_now=None fs=20 color=C00000 mathtext=`W = [10; \; -6] + 2 * [1; \; 1] = [12; \; -4]`
- sidecar `recreated_pptx/build/assets/eq_044_w2_a.json` img=eq_044_w2_a.png EMBEDDED match=md5 rel_now=rId24 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w2_b.json` img=eq_044_w2_b.png EMBEDDED match=md5 rel_now=rId37 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w2_c.json` img=eq_044_w2_c.png EMBEDDED match=md5 rel_now=rId26 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w2_d.json` img=eq_044_w2_d.png EMBEDDED match=md5 rel_now=rId39 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w2_e.json` img=eq_044_w2_e.png EMBEDDED match=md5 rel_now=rId28 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w2_f.json` img=eq_044_w2_f.png EMBEDDED match=md5 rel_now=rId41 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w3.json` img=eq_044_w3.png not-embedded match=None rel_now=None fs=20 color=C00000 mathtext=`W = [12; \; -4] + 2 * [1; \; 0] = [14; \; -4]`
- sidecar `recreated_pptx/build/assets/eq_044_w3_a.json` img=eq_044_w3_a.png EMBEDDED match=md5 rel_now=rId24 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w3_b.json` img=eq_044_w3_b.png EMBEDDED match=md5 rel_now=rId49 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w3_c.json` img=eq_044_w3_c.png EMBEDDED match=md5 rel_now=rId26 fs=14.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w3_d.json` img=eq_044_w3_d.png EMBEDDED match=md5 rel_now=rId51 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w3_e.json` img=eq_044_w3_e.png EMBEDDED match=md5 rel_now=rId28 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w3_f.json` img=eq_044_w3_f.png EMBEDDED match=md5 rel_now=rId53 fs=14.0 color=009A4A mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w4.json` img=eq_044_w4.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`W = [14; \; -4]`
- sidecar `recreated_pptx/build/assets/eq_044_w4_a.json` img=eq_044_w4_a.png EMBEDDED match=md5 rel_now=rId60 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w5.json` img=eq_044_w5.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`W = [14; \; -4]`
- sidecar `recreated_pptx/build/assets/eq_044_w5_a.json` img=eq_044_w5_a.png EMBEDDED match=md5 rel_now=rId60 fs=14.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_044_w6.json` img=eq_044_w6.png not-embedded match=None rel_now=None fs=20 color=000000 mathtext=`W = [14; \; -4]`
- sidecar `recreated_pptx/build/assets/eq_044_w6_a.json` img=eq_044_w6_a.png EMBEDDED match=md5 rel_now=rId60 fs=14.0 color=000000 mathtext=``

### slide 46 — pptx `recreated_pptx/slide_046_recreated.pptx`, wrapped=False, media images=18
- sidecar `recreated_pptx/build/assets/eq_046_final_w.json` img=eq_046_final_w.png not-embedded match=None rel_now=None fs=13.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_046_initial_w.json` img=eq_046_initial_w.png not-embedded match=None rel_now=None fs=11.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_046_step_eta.json` img=eq_046_step_eta.png not-embedded match=None rel_now=None fs=10.0 color=#FF0000 mathtext=``
- NOTE: 3 eq_046_* sidecars exist but are NOT embedded in the current pptx (slide_046.js references eq_046_initial_w.png/eq_046_step_eta.png, but the shipped pptx was rebuilt). Current media: 18 images = plot_046_scatter (4275x2575, rId18) + W-column strips (125x266 x10, 125x416 x7, 341x391, 358x583).

### slide 47 — pptx `recreated_pptx/slide_047_recreated.pptx`, wrapped=False, media images=0
- sidecar `recreated_pptx/build/assets/eq_047_W.json` img=eq_047_W.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`\underline{\underline{W}} = \left( \substack{4 \\ -3 \\ -2} \right)^{T}`
- sidecar `recreated_pptx/build/assets/eq_047_dz_1.json` img=eq_047_dz_1.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`d(Z_1) = \left( 1 \quad 0 \quad 0 \right) \left( \substack{14 \\ -4 \\ 0} \right)`
- sidecar `recreated_pptx/build/assets/eq_047_dz_2.json` img=eq_047_dz_2.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`d(Z_2) = \left( 1 \quad 7 \quad 6 \right) \left( \substack{14 \\ -4 \\ 0} \right)`
- sidecar `recreated_pptx/build/assets/eq_047_dz_3.json` img=eq_047_dz_3.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`d(Z_2) = \left( 1 \quad 3 \quad 2 \right) \left( \substack{14 \\ -4 \\ 0} \right)`
- sidecar `recreated_pptx/build/assets/eq_047_span2.json` img=None not-embedded match=None rel_now=None fs=None color=None mathtext=``
- sidecar `recreated_pptx/build/assets/eq_047_span3.json` img=None not-embedded match=None rel_now=None fs=None color=None mathtext=``
- sidecar `recreated_pptx/build/assets/eq_047_v_1.json` img=eq_047_v_1.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`= 14`
- sidecar `recreated_pptx/build/assets/eq_047_v_2.json` img=eq_047_v_2.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`= -14`
- sidecar `recreated_pptx/build/assets/eq_047_v_3.json` img=eq_047_v_3.png not-embedded match=None rel_now=None fs=15 color=000000 mathtext=`= -2`
- NOTE: Current slide_047_recreated.pptx has 0 media files and 0 p:pic elements — equations are native text/shape runs; nothing to wrap. eq_047_* sidecars are STALE (qa/slide047/omml_prepass_note.md: no eq sidecar matches embedded media; their mathtext uses \underline + \substack, outside wrapper support).

### slide 48 — pptx `recreated_pptx/slide_048_recreated.pptx`, wrapped=False, media images=6
- sidecar `recreated_pptx/build/assets/eq_slide048_r1.json` img=None not-embedded match=None rel_now=None fs=None color=None mathtext=``
- sidecar `recreated_pptx/build/assets/eq_r1_l.json` img=eq_r1_l.png EMBEDDED match=dims rel_now=rId1 fs=13 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_r2_l.json` img=eq_r2_l.png EMBEDDED match=dims rel_now=rId2 fs=13 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_r3_l.json` img=eq_r3_l.png EMBEDDED match=dims rel_now=rId3 fs=13 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_r4_l.json` img=eq_r4_l.png EMBEDDED match=dims rel_now=rId4 fs=13 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_r5_l.json` img=eq_r5_l.png EMBEDDED match=dims rel_now=rId5 fs=13 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_r6_l.json` img=eq_r6_l.png EMBEDDED match=dims rel_now=rId6 fs=13 color=000000 mathtext=``
- NOTE: eq_r1_l..eq_r6_l sidecars are geometry-only (no mathtext); matched by dims to rId1..rId6. eq_r_kw / eq_initial_w_col not embedded.

### slide 49 — pptx `recreated_pptx/slide_049_recreated.pptx`, wrapped=False, media images=0
- sidecar `recreated_pptx/build/assets/eq_slide049_wcol.json` img=None not-embedded match=None rel_now=None fs=None color=None mathtext=``
- sidecar `recreated_pptx/build/assets/eq_slide049_wcol_paren.json` img=None not-embedded match=None rel_now=None fs=None color=None mathtext=``
- NOTE: slide_049_recreated.pptx has 0 media files / 0 p:pic — slide_049.js uses 0 addImage; equations are native addText runs. eq_slide049_* sidecars (incl. qa/paren_sweep_20261026 superseded/broken variants) are not embedded. Nothing to wrap.

### slide 50 — pptx `recreated_pptx/slide_050_recreated.pptx`, wrapped=False, media images=8
- sidecar `recreated_pptx/build/assets/eq_050_Z1.json` img=eq_050_Z1.png EMBEDDED match=dims rel_now=rId15 fs=12.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_050_Z2.json` img=eq_050_Z2.png EMBEDDED match=dims rel_now=rId16 fs=12.0 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_050_Z3.json` img=eq_050_Z3.png EMBEDDED match=dims rel_now=rId17 fs=12.0 color=#000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_050_eta.json` img=eq_050_eta.png not-embedded match=None rel_now=None fs=13.0 color=C00000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_050_finalW.json` img=eq_050_finalW.png EMBEDDED match=dims rel_now=rId18 fs=13 color=000000 mathtext=`\underline{W} = \left( \substack{5\\ \phantom{5} \\ -1\\ \phantom{5} \\ -1} \right)`
- sidecar `recreated_pptx/build/assets/eq_050_initialW.json` img=eq_050_initialW.png not-embedded match=None rel_now=None fs=13.0 color=000000 mathtext=``
- NOTE: Of 6 eq_050_* sidecars, 4 embedded: Z1=rId15, Z2=rId16, Z3=rId17, finalW=rId18 (dims-matched). eq_050_eta (270x117) and eq_050_initialW (890x190) NOT embedded; media also holds 4 paren PNGs (29x258 / 29x341, parens044/parens042). Sidecars are geometry-only (no mathtext field).

### slide 51 — pptx `recreated_pptx/slide_051_recreated.pptx`, wrapped=False, media images=15
- sidecar `recreated_pptx/build/assets/eq_051_col_aug_1.json` img=eq_051_col_aug_1.png not-embedded match=None rel_now=None fs=16.8 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{\genfrac{}{}{0}{}{1}{1}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_aug_2.json` img=eq_051_col_aug_2.png not-embedded match=None rel_now=None fs=16.8 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{\genfrac{}{}{0}{}{2}{1}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_aug_3.json` img=eq_051_col_aug_3.png not-embedded match=None rel_now=None fs=16.73 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{\genfrac{}{}{0}{}{1}{2}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_aug_4.json` img=eq_051_col_aug_4.png not-embedded match=None rel_now=None fs=16.73 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{\genfrac{}{}{0}{}{5}{4}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_aug_5.json` img=eq_051_col_aug_5.png not-embedded match=None rel_now=None fs=16.67 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{\genfrac{}{}{0}{}{6}{5}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_aug_6.json` img=eq_051_col_aug_6.png not-embedded match=None rel_now=None fs=16.67 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{\genfrac{}{}{0}{}{6}{6}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_green.json` img=eq_051_col_green.png not-embedded match=None rel_now=None fs=17.19 color=#659969 mathtext=`\genfrac{(}{)}{0}{0}{\,5\,}{\genfrac{}{}{0}{}{\,-1\,}{\,-1\,}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_initw.json` img=eq_051_col_initw.png not-embedded match=None rel_now=None fs=18.29 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{\,4\,}{\genfrac{}{}{0}{}{\,-2\,}{\,-2\,}}`
- sidecar `recreated_pptx/build/assets/eq_051_col_sample_1.json` img=eq_051_col_sample_1.png not-embedded match=None rel_now=None fs=12.44 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{1}`
- sidecar `recreated_pptx/build/assets/eq_051_col_sample_2.json` img=eq_051_col_sample_2.png not-embedded match=None rel_now=None fs=12.0 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{2}{1}`
- sidecar `recreated_pptx/build/assets/eq_051_col_sample_3.json` img=eq_051_col_sample_3.png not-embedded match=None rel_now=None fs=12.44 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{1}{2}`
- sidecar `recreated_pptx/build/assets/eq_051_col_sample_4.json` img=eq_051_col_sample_4.png not-embedded match=None rel_now=None fs=12.44 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{5}{4}`
- sidecar `recreated_pptx/build/assets/eq_051_col_sample_5.json` img=eq_051_col_sample_5.png not-embedded match=None rel_now=None fs=12.0 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{6}{5}`
- sidecar `recreated_pptx/build/assets/eq_051_col_sample_6.json` img=eq_051_col_sample_6.png not-embedded match=None rel_now=None fs=12.0 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{6}{6}`
- sidecar `recreated_pptx/build/assets/eq_051_col_z_1.json` img=eq_051_col_z_1.png not-embedded match=None rel_now=None fs=12.0 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{0}{0}`
- sidecar `recreated_pptx/build/assets/eq_051_col_z_2.json` img=eq_051_col_z_2.png not-embedded match=None rel_now=None fs=12.0 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{7}{6}`
- sidecar `recreated_pptx/build/assets/eq_051_col_z_3.json` img=eq_051_col_z_3.png not-embedded match=None rel_now=None fs=12.0 color=#000000 mathtext=`\genfrac{(}{)}{0}{0}{3}{2}`
- sidecar `recreated_pptx/build/assets/eq_051_dzlabel_1.json` img=eq_051_dzlabel_1.png EMBEDDED match=md5 rel_now=rId33 fs=15.38 color=#000000 mathtext=`d(Z_1)\;=\;`
- sidecar `recreated_pptx/build/assets/eq_051_dzlabel_2.json` img=eq_051_dzlabel_2.png EMBEDDED match=md5 rel_now=rId36 fs=12.3 color=#000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_051_dzlabel_3.json` img=eq_051_dzlabel_3.png EMBEDDED match=md5 rel_now=rId39 fs=12.3 color=#000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_051_initw.json` img=eq_051_initw.png EMBEDDED match=md5 rel_now=rId13 fs=13 color=000000 mathtext=``
- sidecar `recreated_pptx/build/assets/eq_051_rowvec_1.json` img=eq_051_rowvec_1.png EMBEDDED match=md5 rel_now=rId34 fs=15.56 color=#0F0087 mathtext=`(1\;\;0\;\;0)`
- sidecar `recreated_pptx/build/assets/eq_051_rowvec_2.json` img=eq_051_rowvec_2.png EMBEDDED match=md5 rel_now=rId37 fs=15.56 color=#0F0087 mathtext=`(1\;\;7\;\;6)`
- sidecar `recreated_pptx/build/assets/eq_051_rowvec_3.json` img=eq_051_rowvec_3.png EMBEDDED match=md5 rel_now=rId40 fs=15.56 color=#0F0087 mathtext=`(1\;\;3\;\;2)`
- sidecar `recreated_pptx/build/assets/eq_051_step.json` img=eq_051_step.png EMBEDDED match=md5 rel_now=rId14 fs=14.43 color=#A1232A mathtext=`Step\;\eta\;=\;1`
- sidecar `recreated_pptx/build/assets/eq_051_wcol_green.json` img=eq_051_wcol_green.png EMBEDDED match=md5 rel_now=rId35,rId38,rId41 fs=12 color=659969 mathtext=``
- sidecar `recreated_pptx/qa/slide051/eq_051_wcol_green.gen.json` img=eq_051_wcol_green.png EMBEDDED match=md5 rel_now=rId35,rId38,rId41 fs=12 color=659969 mathtext=``

## Final deck + merge-gate tooling

- Final deck: `recreated_pptx/03_ridger_regression_gradient_descent_final.pptx` — exists, page count = 51 (counted `ppt/slides/slideN.xml`), wrapped pages = 3 (slides 9, 36, 39), md5 `46732bf2f731f8066b3258e34aeb822d`, 4810879 bytes.
- Merge-gate tools: `recreated_pptx/build/final_deck/render_check_pages.py` (exists), `recreated_pptx/build/final_deck/final_deck_tool.py` (exists).
- OMML wrapper: `scripts/18_omml_wrapper.py` (project root, exists). Deck state: `recreated_pptx/final_deck_state.json` (latest gate events 2026-10-31; render-check mismatch reports under `recreated_pptx/qa/final_deck_updates/gate_20261031-*`).

## Summary

- Eq slides: 21. Already OMML-wrapped: [9, 36, 39] (9, 36, 39 — manifests banked under qa/slide009|036|039).
- Not wrapped but have embedded eq PNGs (wrap candidates once certified): [4, 5, 15, 21, 23, 30, 31, 32, 37, 44, 48, 50, 51]. Of these, sidecars WITH mathtext: 4, 5, 9*, 15, 21, 23, 30, 50, 51 (*9 already wrapped); sidecars geometry-only (mathtext must be re-banked from build/evidence first): 31, 32, 37, 44, 48.
- No embedded eq PNG (native-text equations or superseded renders): 3, 43, 46, 47, 49 — nothing to wrap in the current pptx; 43/46 need a look because sidecars exist but the shipped build used different assets (eq043_mx*, W-column strips).
- Slide 23: wrapper previously FAIL-LOUD (`\underline` unsupported) — qa/slide023/omml_prepass_note.md; not wrapped, manifest banked; needs wrapper extension or a multi-equation manifest before wrap.
- Manifests exist only for 9, 23, 36, 39; all other wraps must re-derive rel_ids from the current pptx per contract.
- Reminder: slide 25 is NOT certified — this inventory is prep only; no wrap was run.
