# OMML_WRAP_LOG — deck 03_ridger_regression_gradient_descent

Run 2026-10-31 by OMML-wrap workers. Wrapper: scripts/18_omml_wrapper.py (v2, extended this run with \underline -> m:bar pos=bot, \\ row breaks -> m:m matrix, \substack, \phantom — additive only; previously fail-loud). Rel ids re-derived from each CURRENT slide_NNN_recreated.pptx (pic descr basename -> r:embed in ppt/slides/slide1.xml). Backups: $RJ/slideNNN/slide_NNN_recreated.preOMML.bak.pptx. Only ppt/slides/slide1.xml changed in each wrapped pptx (zip diff vs backup); media byte-identical; no rels/content-types touched; no LO resave; no git. Slide 25 untouched. Already-wrapped 009/036/039 untouched.

## Shard-1 (004/005/015/021/030)

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
## Shard-2 (031, 032, 037, 043, 044 + unowned 023, 048, 050, 051)

Rel ids re-derived from current pptx via pic descr. Manifests: $RJ/slideNNN/omml_manifest.json. Verification per slide: rc=0, mc:AlternateContent count == wrapped eq count (open+close tags = 2x), zip diff vs preOMML backup touches only ppt/slides/slide1.xml, XML well-formed.

| slide | rel ids | md5 before | md5 after | result | note |
|---|---|---|---|---|---|
| 031 | rId1 | c650aa102da5473b4690adb7b5c0840e | c39ca2aa915ea8e10b8128ff9d77bead | WRAPPED rc=0 AltContent=1/1 | mathtext re-banked from qa/slide031/worker_report.md (f(x)=(x-5)^2+1) |
| 032 | rId2 | 6c544c9299dd421e85201f3f0a5ae074 | 269f0316c0dfd7b0fcdcb89f55bccad4 | WRAPPED rc=0 AltContent=1/1 | mathtext re-banked from qa/slide032 (f(x)=(x-5)^2+1) |
| 037 | rId1,rId2,rId3,rId4,rId5 | 39fb487c9a48772c711e330626ffc40c | 655c1012abed0b3fa6b1f4df4ae1928a | WRAPPED rc=0 AltContent=5/5 | frac from qa/slide037/crop_4_eq_stack_adjudication.txt; sigma glyph; prepass caveat: anisotropic rescale in certified pptx, Choice fontsize from sidecar |
| 043 | — | — | — | SKIP no embedded eq sidecar pics | 14 eq_043_* sidecars exist but NONE embedded; embedded eq043_mx1/2/3.png have no sidecars/mathtext — nothing wrappable |
| 023 | rId1 | 8015445ba6de72d21bffb4f6836d5b81 | 8794172a07d2170248cc75085a39c424 | WRAPPED rc=0 AltContent=1/1 | sidecar mathtext (\\underline now wrapper-supported as m:bar bot); rel re-derived rId1; supersedes banked qa/slide023 manifest |
| 044 | rId19..rId72 (54 eq pics) | ccd2f9378556979ef9bb972a0aa5c9b9 | 06f1a314080d2e1f0526f79ac2fa52fa | WRAPPED rc=0 AltContent=54/54 | piece PNGs; mathtext from build/gen_eq_044.py SPECS; col vectors via \\left..\\\\..\\right matrix ext; \\underline via m:bar bot |
| 048 | rId1,rId2,rId3,rId4,rId5,rId6 | e5cfcf57546a1ea7c353028a0d8bddc7 | bf370b6053f16034a466efe03ad74b53 | WRAPPED rc=0 AltContent=6/6 | mathtext from build/gen_assets_048.py; per-entry multi-color flattened to black in Choice (PNG fallback exact) |
| 050 | rId15,rId16,rId17,rId18 | 503cc992efd4d0e38a236dbc849af485 | eee2fee6d69699b6783a199ebd0e058a | WRAPPED rc=0 AltContent=4/4 | Z cols from qa/slide050/render_050_eqs.py; finalW sidecar mathtext (substack/phantom/underline now supported) |
| 051 | rId13,rId14,rId33,rId34,rId35,rId36,rId37,rId38,rId39,rId40,rId41 | 210712ebf0abea3b5804530f954ba32c | a32d9bd36e23434aa7230f25461e1a67 | WRAPPED rc=0 AltContent=11/11 | dzlabel_2/3 + col vectors re-banked from slide_051.js/sidecar rows; step/dzlabel_1/rowvecs from sidecar mathtext |

# OMML_WRAP_LOG — deck 03 shard {023,048,050,051} (this worker)

Run 2026-10-31 by OMML-wrap worker (shard = remaining plan-r3 candidates after shard-1 {004,005,015,021,030}
and shard-2 {031,032,037,043,044}). Finding: on arrival, the concurrent shard-2 worker had ALREADY wrapped
and replaced all four of this shard's slides (rows above, md5 before/after match). This worker therefore
re-derived rel ids from the CURRENT pptx files, banked fresh preOMML backups + manifests under
$RJ/slideNNN/, re-ran the wrapper against the current deliverables (idempotent: rc=0,
skipped_already_wrapped = full count, no bytes changed by this worker), and verified the wrapped state.
Wrapper note: scripts/18_omml_wrapper.py was extended during this session (\underline -> m:bar pos=bot,
\substack/\\ rowbreaks -> m:m matrix, \phantom -> em-space runs), which is what unblocked 023/048/050.
Slide 25 untouched (never opened for write). No LO resave, no git, no evidence deleted.

| slide | outcome (verified by this worker) | wrapped rel ids (sidecar) | manifest | md5 before (preOMML backup) | md5 after (current deliverable) | wrapper rc re-run | verification |
|---|---|---|---|---|---|---|---|
| 023 | ALREADY WRAPPED+REPLACED by concurrent run; verified | rId1=eq_023_main | $RJ/slide023/omml_manifest.json | 8015445ba6de72d21bffb4f6836d5b81 | 8794172a07d2170248cc75085a39c424 | 0 (skipped_already_wrapped=1) | zip OK, slide1.xml well-formed, AltContent/Choice/oMath/Fallback=1 each; zip diff vs backup = ppt/slides/slide1.xml only |
| 048 | ALREADY WRAPPED+REPLACED; verified | rId1..rId6=eq_r1_l..eq_r6_l | $RJ/slide048/omml_manifest.json | e5cfcf57546a1ea7c353028a0d8bddc7 | bf370b6053f16034a466efe03ad74b53 | 0 (skipped=6) | zip OK, AltContent=6; diff vs backup = slide1.xml only; media byte-identical to sidecar PNGs |
| 050 | ALREADY WRAPPED+REPLACED; verified | rId15=Z1, rId16=Z2, rId17=Z3, rId18=finalW | $RJ/slide050/omml_manifest.json | 503cc992efd4d0e38a236dbc849af485 | eee2fee6d69699b6783a199ebd0e058a | 0 (skipped=4) | zip OK, AltContent=4; diff vs backup = slide1.xml only |
| 051 | ALREADY WRAPPED+REPLACED; verified | rId13=initw, rId14=step, rId33/36/39=dzlabel_1-3, rId34/37/40=rowvec_1-3, rId35/38/41=wcol_green | $RJ/slide051/omml_manifest.json | 210712ebf0abea3b5804530f954ba32c | a32d9bd36e23434aa7230f25461e1a67 | 0 (skipped=11) | zip OK, AltContent=11; diff vs backup = slide1.xml only; all 11 eq media byte-identical to sidecar PNGs |

This worker's manifests re-derived rel ids independently and match the concurrent run's (023 rId1;
048 rId1-6; 050 rId15-18; 051 rId13/14/33-41). Manifests banked: $RJ/slideNNN/omml_manifest.json;
backups: $RJ/slideNNN/slide_NNN_recreated.preOMML.bak.pptx (md5 = pre-wrap deliverables);
wrapper run logs: $RJ/slideNNN/wrap_full_run.log. No SKIP rows: every shard slide had sidecars and
embedded eq pics.
