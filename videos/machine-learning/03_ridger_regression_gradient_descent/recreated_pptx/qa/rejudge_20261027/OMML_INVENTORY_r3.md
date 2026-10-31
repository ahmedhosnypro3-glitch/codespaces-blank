# OMML_INVENTORY_r3 — FINAL wrap status, deck 03_ridger_regression_gradient_descent

Generated 2026-10-31 after the shard-2 wrap run (this file supersedes OMML_INVENTORY_r2 /
OMML_WRAP_PLAN_r3 as the status of record). Namespace:
`videos/machine-learning/03_ridger_regression_gradient_descent/`. Method: rel ids re-derived from
each CURRENT `slide_NNN_recreated.pptx` at wrap time via pic `descr` basename -> `r:embed` in
`ppt/slides/slide1.xml`; wrapper `scripts/18_omml_wrapper.py`; backups
`$RJ/slideNNN/slide_NNN_recreated.preOMML.bak.pptx`; per-slide manifests
`$RJ/slideNNN/omml_manifest.json`; log `OMML_WRAP_LOG.md`. Slide 25 never touched; no LO resave;
no git; no evidence deleted.

Wrapper note: this run extended `scripts/18_omml_wrapper.py` (additive, previously fail-loud
constructs now supported): `\underline{X}` -> `m:bar pos="bot"`, `\\` row breaks inside
`\left...\right` -> `m:m` matrix rows, `\substack{...}`, `\phantom{...}`. Converter self-tested on
every shard mathtext string (all parse + well-formed OMML) before any pptx was modified.

## Final status of ALL plan-r3 candidates (13 wrap candidates + 3 already wrapped + 043)

| NNN | plan action | final status | wrapped rel ids | eqs | manifest | note |
|---|---|---|---|---|---|---|
| 004 | wrap (shard-1) | WRAPPED PARTIAL 1/4 | rId3=eq_004_norm | 1 | $RJ/slide004/omml_manifest_parseable_only.json | rId1/rId2/rId4 were fail-loud at shard-1 run (\underline, \mathbf{\hat{Y}}); wrapper now supports \underline — re-run possible |
| 005 | wrap (shard-1) | WRAPPED PARTIAL 8/9 | rId1,2,3,4,5,6,8,9 | 8 | $RJ/slide005/omml_manifest_parseable_only.json | rId7=eq_005_deriv2 skipped (fail-loud at shard-1 run) |
| 015 | wrap (shard-1) | WRAPPED PARTIAL 1/9 | rId5=eq_015_peach_eq | 1 | $RJ/slide015/omml_manifest_parseable_only.json | other 8 fail-loud at shard-1 run (\underline); re-run possible with extended wrapper |
| 021 | wrap (shard-1) | WRAPPED PARTIAL 5/6 | rId1..rId5 | 5 | $RJ/slide021/omml_manifest_parseable_only.json | rId6=eq_021_invexpr (\underline) skipped at shard-1 run |
| 023 | wrap after pre-transform | **WRAPPED 1/1** | rId1=eq_023_main | 1 | $RJ/slide023/omml_manifest.json | sidecar mathtext; \underline now native (m:bar bot) |
| 030 | wrap (shard-1) | WRAPPED 2/2 | rId1=eq_030_fx, rId2=eq_030_x5_red | 2 | $RJ/slide030/omml_manifest.json | |
| 031 | wrap after re-bank | **WRAPPED 1/1** | rId1=eq_031_main | 1 | $RJ/slide031/omml_manifest.json | mathtext re-banked: f(x)=(x-5)^2+1 |
| 032 | wrap after re-bank | **WRAPPED 1/1** | rId2=eq_032_main | 1 | $RJ/slide032/omml_manifest.json | mathtext re-banked: f(x)=(x-5)^2+1 |
| 037 | wrap after re-bank | **WRAPPED 5/5** | rId1,4,5=sigma; rId2,3=frac | 5 | $RJ/slide037/omml_manifest.json | frac=\frac{\partial Error}{\partial W}; sigma=\Sigma glyph; prepass anisotropic-rescale caveat noted in log |
| 043 | skip (nothing embedded) | **SKIP** | — | 0 | — | 14 eq_043_* sidecars exist but NONE embedded in current pptx; embedded eq043_mx1/2/3.png have no sidecars/mathtext |
| 044 | wrap after re-bank | **WRAPPED 54/54** | rId19..rId72 (all eq_044_* pics) | 54 | $RJ/slide044/omml_manifest.json | mathtext from gen_eq_044.py SPECS; col vectors via matrix ext |
| 048 | wrap after re-bank | **WRAPPED 6/6** | rId1..rId6=eq_r*_l | 6 | $RJ/slide048/omml_manifest.json | mathtext from gen_assets_048.py; multi-color flattened in Choice, PNG fallback exact |
| 050 | wrap after re-bank | **WRAPPED 4/4** | rId15,16,17=Z1-3; rId18=finalW | 4 | $RJ/slide050/omml_manifest.json | Z cols from render_050_eqs.py; finalW sidecar mathtext (substack/phantom/underline) |
| 051 | wrap after re-bank | **WRAPPED 11/11** | rId13,14,33..41 | 11 | $RJ/slide051/omml_manifest.json | dzlabel_2/3 + col vectors re-banked; step/dzlabel_1/rowvecs from sidecars |
| 009 | already wrapped | UNTOUCHED (wrapped) | rId1,rId2 | 2 | qa/slide009/omml_manifest*.json | |
| 036 | already wrapped | UNTOUCHED (wrapped) | rId1 | 1 | qa/slide036/omml_manifest.json | |
| 039 | already wrapped | UNTOUCHED (wrapped) | rId4 | 1 | qa/slide039/omml_manifest.json | |

## Verification (per wrapped slide)

- wrapper rc=0; `mc:AlternateContent` open-tag count in `ppt/slides/slide1.xml` == equation count;
  `mc:Fallback` count == equation count; XML well-formed (ElementTree parse).
- zip diff vs preOMML backup: only `ppt/slides/slide1.xml` differs; all media byte-identical;
  no rels/content-types touched.
- 009/036/039/025 confirmed untouched after the run.

## Remaining debt (not in this shard's scope)

- 004 (3 pics), 005 (rId7), 015 (8 pics), 021 (rId6): unwrapped because shard-1's manifests
  predated the wrapper extension; a re-run with full manifests + the extended wrapper should now
  succeed for the \underline cases (004 rId4 also has \mathbf{\hat{Y}} — \mathbf supported,
  \hat supported, composition should parse; verify before replacing).
- Final deck `03_ridger_regression_gradient_descent_final.pptx` still has only the 3 old wrapped
  pages (9, 36, 39) — re-merge/re-gate after all per-slide wraps land.
