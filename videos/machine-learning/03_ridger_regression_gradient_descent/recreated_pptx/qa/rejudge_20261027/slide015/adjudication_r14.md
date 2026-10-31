# Adjudication r14 — slide 015 CROP fresh2 claim: "render line-1 reads I(W), original J(W); asset eq_015_eq1_l1.png hook=0"

Date: 2026-10-31. Method: bytes + pixels only (md5, zip XML, PIL/numpy). No vision, no rebuild,
no DB touch, no git.

## Verdict: REFUTED (rendering/vision artifact, not a content defect)

The render's equation line 1 does NOT lack the hook. The embedded asset encodes a hooked capital J,
the pptx embeds that asset byte-identically, and the 150 dpi render reproduces the asset within 1.95%
of band pixels. The original frame's glyph is a hooked J as well. The shard-D "hook=0" pixel claim on
the asset is factually wrong (measurements below), and the judge's I(W) reading is a vision misread of
the blue (00008B) J at crop scale with AA softening.

## (1) Eq assets used by build/slide_015.js

`slide_015.js:77-82` `eqAt(tag)` -> `slide.addImage({ path: assets/eq_015_${tag}.png, x/y/w/h from
assets/eq015_table.json })`. Tags placed: `eq1_l1, eq1_l2, eq1_l3` (lines 100-102), `redbox_eq` (108),
`peach_eq` (130), `deriv_l1, deriv_l2` (136-137), `normal` (142), `solution` (158). So line 1 of the
top equation = `build/assets/eq_015_eq1_l1.png`.

## (2) Mathtext source of each asset (sidecars `build/assets/eq_015_*.json` + `build/gen_eq_015{,_v2,_v3}.py`)

- `eq_015_eq1_l1.json`: `J(\underline{W}) = \frac{1}{2}(Y-\hat{Y})^{T}(Y-\hat{Y}) + \frac{1}{2}\lambda
  \underline{W}^{T}\underline{W} = ...` — line 1 opens with **J** (hooked capital), W underlined.
- `eq1_l2` / `eq1_l3` likewise open with `J(\underline{W})`; `redbox_eq` / `deriv_l1` / `deriv_l2` carry
  `\frac{\partial J(\underline{W})}{\partial \underline{W}}`.
- `deriv_l2` tail is `... + \lambda I \underline{W}` — that **I is the identity matrix**, intentional
  (matches `normal`/`solution` `\lambda I`), NOT a mis-rendered J. All three gen_eq_015*.py sources
  agree verbatim (`J(W)...`, `\lambda I W`).
- Control re-render: rendering the sidecar mathtext at 17 pt / 600 dpi reproduces the asset's left
  130 px at 19.87% pixel diff; rendering `I(\underline{W}) = \frac{1}{2}` against it gives 37.71% —
  the asset is a J-shaped composite, not an I.

## (3) PIL measurements

Embedded-asset identity: `ppt/slides/slide1.xml` has 9 `r:embed` pics; `ppt/media/image-1-1.png`
md5 `b25a4f07a93c78f1937884a8a020c6d8` == `build/assets/eq_015_eq1_l1.png` md5 (byte-identical; the
other 8 media md5s match the other 8 eq_015_*.png assets 1:1, placed at the eq015_table.json frame
coords, e.g. rId1 at slide x=97 y=104 w=612.5 h=50.3 pt).

Asset `eq_015_eq1_l1.png` (4282x223, alpha>40):
- First glyph run x0..60, ink rows 60..163 (h=104). The whole glyph is uniformly RGB(0,0,139) = 00008B
  (the sidecar's blue `part0` segment) — a blue J, which is why vision reads it as a plain bar at crop scale.
- Baseline from the `=` glyph run x153..243: bottom row 139. Descender of glyph#1 below baseline:
  163-139 = **24 px = 2.4 pt**, with the bottom ~8 rows wide and left-extending
  (`#######################` ... `###############`) — the hook. (Template renders: `$J$` 62x133 with
  29 px descender vs `$I$` 35x105 with none; the asset glyph's descender + left-flaring bottom rows
  match the J shape.)

Original `unique_slides/slide_015.jpg` (960x540, ink = sum(RGB)<600), eq1 line 1 band y104..154:
- glyph#1 run x97..111: rows 119..136 (h=18); `=` baseline row 133 -> descender **3 px below baseline,
  14 descender ink px extending to the run's left edge** — hooked J. eq1 line 2 glyph#1: rows 177..195,
  baseline 192, descender 3 px; crop ASCII shows the top bar + bottom-left hook (`#################`).

Render `rejudge_20261027/slide015/render.png` (2001x1125 = 150 dpi, scale 2.0848):
- eq1_l1 band (slide x97..709, y104..155) vs the asset LANCZOS-downscaled to the same 1277x105 box:
  **diff = 2612 px = 1.95% of the band** — the render is a faithful rasterization of the asset.
  First-glyph NCC (downscaled asset vs render) = 0.833; the render glyph's bottom rows carry the same
  left-extending hook mass (3-5 px at 150 dpi, AA-softened).
- Crop pair actually judged (`crop_dense_render.png` / `crop_dense_orig.png`, region slide x88..392
  y160..368, ~2.086x): crop-orig top line glyph shows a pronounced 8-px-wide bottom-left hook;
  crop-render shows the J stem with only a ~2 px AA hook remnant at this scale — present but soft,
  which is what the vision model read as "hookless I".

## (4) pptx XML check

`slide_015_recreated.pptx` -> `ppt/slides/slide1.xml`: 9 `<p:pic>` with rId1..rId9; rels map rId1..rId9
to `ppt/media/image-1-{1..9}.png`; md5s equal the 9 `eq_015_*.png` assets exactly. No text-run equation
(no OMML/linear-math fallback); the equation is purely the image. Placement: rId1 at 1.347in/1.444in,
8.507x0.698in = slide px x97 y104 w612.5 h50.3 — matches `eq015_table.json` `eq1_l1`.

## Disposition

- shard-D fresh2 crop MAJOR (I(W) vs J(W)) — **DISMISSED / REFUTED by pixels**. No fix, no rebuild, no
  re-render. `result.txt` PASS(dismissed) stands.
- The genuine `I` in the deck is the identity matrix in `\lambda I W` (deriv_l2) / `\lambda I`
  (normal, solution) — correct as built.
- Minor residual worth noting (not a defect trigger): at the crop's effective scale the blue J's hook
  AA-thins to ~2 px, so zoomed judges can misread it; the full-res render and asset both retain it.

Evidence files: this adjudication; `slide015/crop_dense_judge_fresh2.txt` (claim), `slide015/adjudicate_20261031_crop_fresh2.txt`
(shard-D pixel claim), `slide015/adjudicate_w5_probe2_015.{py,out}` (w5 asset refutation), build sidecars
`recreated_pptx/build/assets/eq_015_*.json`, `recreated_pptx/build/gen_eq_015*.py`.
