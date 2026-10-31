# OMML_WRAP_LOG — deck 03 shard {004,005,015,021,030}

Run 2026-10-31 by OMML-wrap worker. Wrapper: scripts/18_omml_wrapper.py (v2). Rel ids re-derived from each CURRENT slide_NNN_recreated.pptx (descr basename -> r:embed in ppt/slides/slide1.xml; media md5 matched to build/assets/eq_*.png where bytes identical). Backups: $RJ/slideNNN/slide_NNN_recreated.preOMML.bak.pptx. Only ppt/slides/slide1.xml changed in each pptx (zip diff vs backup); media byte-identical; no rels/content-types touched; no LO resave. Slide 25 untouched. Already-wrapped 009/036/039 untouched.

| slide | outcome | wrapped rel ids (sidecar) | skipped rel ids (wrapper fail-loud) | manifest | md5 before | md5 after | wrapper rc (full/subset) | render check |
|---|---|---|---|---|---|---|---|---|
| 004 | WRAPPED+REPLACED (1 mc:AlternateContent blocks) | rId3=eq_004_norm | rId1=eq_004_Yvec, rId2=eq_004_Yhatvec, rId4=eq_004_formula | $RJ/slide004/omml_manifest_parseable_only.json | 4d21712f117e541d74acd852067c44c7 | f65fd3007566b26ba7c36894692c2ad0 | 1/0 | 1284 px vs stale banked pdf; 0 px vs preOMML backup (wrap pixel-identical) |
| 005 | WRAPPED+REPLACED (8 mc:AlternateContent blocks) | rId1=eq_005_loss1, rId2=eq_005_loss2, rId3=eq_005_loss3, rId4=eq_005_remember1, rId5=eq_005_pinkfrac, rId6=eq_005_deriv1, rId8=eq_005_remember2, rId9=eq_005_finalw | rId7=eq_005_deriv2 | $RJ/slide005/omml_manifest_parseable_only.json | 03b77ff50b9b0764d4f0b5c77a2604c4 | c72f0be14ff279b19a993dae0e11a568 | 1/0 | 0 px vs banked pdf |
| 015 | WRAPPED+REPLACED (1 mc:AlternateContent blocks) | rId5=eq_015_peach_eq | rId1=eq_015_eq1_l1, rId2=eq_015_eq1_l2, rId3=eq_015_eq1_l3, rId4=eq_015_redbox_eq, rId6=eq_015_deriv_l1, rId7=eq_015_deriv_l2, rId8=eq_015_normal, rId9=eq_015_solution | $RJ/slide015/omml_manifest_parseable_only.json | 39dc053a3a4ca2d75da8081daec3f5d2 | b6b3a99d9afb17f28cf8ad889eadc473 | 1/0 | 0 px vs banked pdf |
| 021 | WRAPPED+REPLACED (5 mc:AlternateContent blocks) | rId1=eq_021_xtx, rId2=eq_021_det0, rId3=eq_021_regmat, rId4=eq_021_lambda3, rId5=eq_021_d5685 | rId6=eq_021_invexpr | $RJ/slide021/omml_manifest_parseable_only.json | c094b309d669b7561dc27fc6f9802511 | 9099303fa50a5280d9a9adea43a2e430 | 1/0 | 0 px vs banked pdf |
| 030 | WRAPPED+REPLACED (2 mc:AlternateContent blocks) | rId1=eq_030_fx, rId2=eq_030_x5_red | - | $RJ/slide030/omml_manifest.json | bbb6a6345ed77601baf3631c3268dee7 | c48f8fa3a74f880a1f54d0a0b97236ca | 0/- | 0 px vs banked pdf |

Notes:
- Full-manifest runs fail-loud on \underline (unsupported by wrapper) and on \mathbf{\hat{Y}} (004 formula); per plan r3 caveat. Subset manifests (omml_manifest_parseable_only.json) wrap only wrapper-parseable mathtext; the remaining pics stay as plain PNG embeds (idempotent — a later wrapper run with extended mathtext support will wrap them).
- 005/030 embedded media bytes differ from on-disk sidecar PNGs (re-encoded at build); rel ids derived via pic descr basename, which is exact.
- Multi-color sidecars (021 det0/regmat/d5685/invexpr, color='multi') wrapped with color 000000 in the OMML Choice; the mc:Fallback PNG keeps the certified multi-color pixels.
- font key normalized: sidecar 'fontsize_pt' -> manifest 'font_size_pt'.
- Slide 004 banked pdf under $RJ/slide004 predates the current pptx; wrap pixel-identity proven against the preOMML backup render (0/2251225 px).
| 031 | rId1 | c650aa102da5473b4690adb7b5c0840e | c39ca2aa915ea8e10b8128ff9d77bead | WRAPPED rc=0 AltContent=2/1 eqs=1 | pilot: mathtext re-banked from qa/slide031/worker_report.md |
