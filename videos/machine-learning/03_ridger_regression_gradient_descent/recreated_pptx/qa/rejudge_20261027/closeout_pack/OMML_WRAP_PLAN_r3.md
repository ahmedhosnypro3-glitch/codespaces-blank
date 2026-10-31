# OMML_WRAP_PLAN_r3 — deck 03 closeout wrap list (PREP ONLY)

Generated 2026-10-31 by a fresh read-only scan (no pptx modified, no wrapper run, no git touched).
Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
Supersedes OMML_INVENTORY_r1/r2 (which disagreed with each other; r3 re-derives everything from the
current `slide_NNN_recreated.pptx` files).

Method per slide 001–051: `unzip -l` for `ppt/media/*`; `ppt/slides/slide1.xml` counted for
`mc:AlternateContent` (= wrapped) and `oMath`; embedded media matched to eq sidecars
(`recreated_pptx/build/assets/eq_*.json`) by md5 byte-exact, else by PNG IHDR dims vs sidecar
`w_px`/`h_px`; manifests searched under `recreated_pptx/` (`build/` holds eq sidecars only —
no `*manifest*.json` in `build/`; banked OMML manifests live under `qa/slideNNN/`).
Wrapper contract: `scripts/18_omml_wrapper.py <in.pptx> <manifest.json>`; rel_ids MUST be
re-derived from the current pptx at wrap time.

## Summary

- Already OMML-wrapped (skip): **009, 036, 039**
- Eq images present, NOT wrapped → **wrap candidates (13): 004, 005, 015, 021, 023, 030, 031, 032, 037, 044, 048, 050, 051**
- No eq image embedded in current pptx → skip (incl. 003, 043, 046, 047, 049 whose sidecars exist but are not embedded / superseded / native-text equations)

## Per-slide table (all 51)

| NNN | eq images present (match) | already wrapped (AltContent/oMath) | manifest path | action |
|---|---|---|---|---|
| 001 | no (media 2, pic 1, none eq) | no (0/0) | - | skip |
| 002 | no (1/0) | no | - | skip |
| 003 | no (15 media are paren-arc PNGs; eq_003_remember sidecar superseded, not embedded) | no | - | skip |
| 004 | yes — 4 (md5: Yvec, Yhatvec, norm, formula) | no (0/0) | none (derive from build/assets/eq_004_*.json) | **wrap** (mathtext present; 2 COMPOSED entries use `\underline` — wrapper may fail-loud, see 023 note) |
| 005 | yes — 9 (dims: loss1-3, remember1-2, pinkfrac, deriv1-2, finalw) | no | none | **wrap** (mathtext present on all 9) |
| 006 | no (1/0) | no | - | skip |
| 007 | no (1/0) | no | - | skip |
| 008 | no (1/0) | no | - | skip |
| 009 | yes — 2 (dims: left/right_attempt4) | **YES (4/12)** | `qa/slide009/omml_manifest.json`; `qa/slide009/omml_manifest_7.json` | skip (already wrapped) |
| 010 | no (1/0) | no | - | skip |
| 011 | no (1/0) | no | - | skip |
| 012 | no (1/0) | no | - | skip |
| 013 | no (4 media, pic 3, none eq) | no | - | skip |
| 014 | no (eq_index_014 is a matrix-bracket asset, not an equation) | no | - | skip |
| 015 | yes — 9 (md5: eq1_l1-l3, redbox, peach, deriv_l1-l2, normal, solution) | no | none | **wrap** (mathtext present; several use `\underline`) |
| 016 | no (1/0) | no | - | skip |
| 017 | no (4/3) | no | - | skip |
| 018 | no (4/3) | no | - | skip |
| 019 | no (1/0) | no | - | skip |
| 020 | no (1/0) | no | - | skip |
| 021 | yes — 6 (md5: xtx, det0, regmat, lambda3, d5685, invexpr) | no | none | **wrap** (mathtext present; invexpr uses `\underline`) |
| 022 | no (1/0) | no | - | skip |
| 023 | yes — 1 (dims: eq_023_main) | no (0/0) | `qa/slide023/omml_manifest.json` (banked; wrapper previously FAIL-LOUD on `\underline`, qa/slide023/omml_prepass_note.md) | **wrap only after wrapper extension / mathtext pre-transform** |
| 024 | no (2/1) | no | - | skip |
| 025 | no (5/4) | no | - | skip |
| 026 | no (1/0) | no | - | skip |
| 027 | no (1/0) | no | - | skip |
| 028 | no (1/0) | no | - | skip |
| 029 | no (1/0) | no | - | skip |
| 030 | yes — 2 (dims: fx, x5_red; eq_030_x5 not embedded) | no | none | **wrap** (mathtext present on both) |
| 031 | yes — 1 (dims: eq_031_main; sidecar geometry-only, mathtext empty) | no | none | **wrap after mathtext re-bank** from build/slide_031.js |
| 032 | yes — 1 (dims: eq_032_main; geometry-only) | no | none | **wrap after mathtext re-bank** |
| 033 | no (3/2) | no | - | skip |
| 034 | no (3/2) | no | - | skip |
| 035 | no (1/0) | no | - | skip |
| 036 | yes — 1 (dims: eq_036_error) | **YES (2/6)** | `qa/slide036/omml_manifest.json` | skip (already wrapped) |
| 037 | yes — 2 (dims: sigma, frac; geometry-only) | no | none | **wrap after mathtext re-bank** (qa/slide037/omml_prepass_note.md: anisotropic rescale, per-instance fontsize re-derivation needed) |
| 038 | no (1/0) | no | - | skip |
| 039 | no eq pic needing wrap (eq_039_main embedded by position; media 3) | **YES (2/6)** | `qa/slide039/omml_manifest.json` | skip (already wrapped) |
| 040 | no (1/0) | no | - | skip |
| 041 | no (7 media, pic 20, none eq-matched) | no | - | skip |
| 042 | no (9/66; eq_index_042 is matrix-bracket asset) | no | - | skip |
| 043 | no — 14 sidecars exist but NONE embedded (eq043_mx*/paren composition shipped) | no | none | skip (nothing to wrap in current pptx) |
| 044 | yes — 48 (md5: dx1-6/w1-6 piece PNGs + arrD/arrL/arrDk; sidecars geometry-only) | no | none | **wrap after mathtext re-bank** per piece |
| 045 | no (1/0) | no | - | skip |
| 046 | no — 3 sidecars, none embedded (W-column strips shipped) | no | none | skip |
| 047 | no (0 media files; equations are native text/shape runs) | no | - | skip |
| 048 | yes — 6 (dims: eq_r1_l..eq_r6_l; sidecars geometry-only, no `image`/`path` key) | no | none | **wrap after mathtext re-bank** (gen_assets_048.py / slide_048.js) |
| 049 | no (0 media; native addText equations) | no | - | skip |
| 050 | yes — 4 (dims: Z1, Z2, Z3, finalW; finalW has mathtext, Z* geometry-only; eta/initialW not embedded) | no | none | **wrap** (re-bank mathtext for Z1-Z3) |
| 051 | yes — 9 (md5: initw, step, dzlabel_1-3, rowvec_1-3, wcol_green x3 rels; mathtext present on step/dzlabel_1/rowvecs only) | no | none | **wrap** (re-bank mathtext for initw, dzlabel_2-3, wcol_green) |

## Slides needing wraps (13)

004, 005, 015, 021, 023, 030, 031, 032, 037, 044, 048, 050, 051

Of these, sidecars already carry mathtext: 004, 005, 015, 021, 023, 030, 050 (finalW only), 051 (partial).
Geometry-only (mathtext must be re-banked from build scripts/evidence before manifest authoring):
031, 032, 037, 044, 048, 050 (Z1-Z3), 051 (initw, dzlabel_2-3, wcol_green).

## Caveats for the wrap run (not executed here)

- `\underline` appears in sidecar mathtext of 004 (COMPOSED), 015, 021, 023, 050(finalW) — the wrapper
  previously FAIL-LOUDed on `\underline` (slide 023 prepass). Either extend the wrapper or pre-transform
  those manifests before running `scripts/18_omml_wrapper.py`.
- Manifest rel_ids must be re-derived from each CURRENT pptx at wrap time (md5/dims mapping above is
  the prep-time derivation; verify against `ppt/slides/_rels/slide1.xml.rels` when authoring manifests).
- Banked manifests exist only for 009 (x2), 023, 036, 039. 009/036/039 are already wrapped — do not re-wrap.
- Final deck `03_ridger_regression_gradient_descent_final.pptx` currently has 3 wrapped pages (9, 36, 39);
  after per-slide wraps the deck must be re-merged/re-gated.
- PREP ONLY: no `scripts/18_omml_wrapper.py` run, no deliverable modified, no evidence deleted.
