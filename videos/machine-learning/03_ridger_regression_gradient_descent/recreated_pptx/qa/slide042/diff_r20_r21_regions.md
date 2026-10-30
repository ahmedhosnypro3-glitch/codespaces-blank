# Slide 042 — render_20 → render_21 region diff (carry-over law, protocol line 129)

Run: `python3 scratch/tmp/s6_042_region_diff3.py` (+ component census inline), 2026-10-25 ~16:35.
render_20/render_21 both 2001x1125 (150 dpi). Scale render→frame = 2.0833 (960x540 frame).

Crop-bbox recovery: each `crop_20_<name>_render.png` (frame-res, 1.0 px/frame-px)
matched against a 960x540 downscale of render_20 — identical bboxes under LANCZOS /
BILINEAR / BOX resampling, so positions are exact. Region change = pixels with
max-channel diff > 8 between render_20 and render_21 inside the bbox x2.0833.

| region | recovered frame bbox | r20→r21 changed px | verdict |
|---|---|---|---|
| stack | (365,205)..(800,535) | **0** | pixel-identical → `crop_20_stack_judge.txt` (PASS, landed 16:13) carried over as valid evidence for the delivered build |
| legend | (330,95)..(560,130) | **0** | pair pixel-identical; judge never landed → dispatch on this pair unchanged |
| topright | (560,30)..(850,125) | **0** | pair pixel-identical; judge never landed → dispatch on this pair unchanged |
| tl_table | (30,30)..(330,125) | 320 (frame x311..324 y110..122 = fix #8 C2 shift) | NOT identical → re-cut as crop_21_tl_table from render_21 + re-judge |
| lm_table | (30,148)..(335,250) | 1540 (frame x92..218 y221..226 = fix #9 paren stubs; x283..322 y224..248 = fix #7 d(x2) label) | NOT identical → re-cut as crop_21_lm_table from render_21 + re-judge |

Full-image change census (60 components, all inside three fix zones of
adjudication_20.md):
- comp1 n=320 frame x311..324 y110..122 — legend C2 x-shift (fix #8)
- comps 4–13 n≈530 frame x92..218 y221..226 — LM paren bottom stubs (fix #9)
- comps 15–60 n≈6100 frame x283..322, five bands y224..248 / 287..311 / 352..377 /
  419..443 / 484..509 — d(x_i) label run re-layout (fix #7). Bands 2–5 lie in NO
  crop region; only the full-slide leg A covers them → leg A MUST be re-run on
  render_21 (judge_attempt_21.txt).

Crop-pair convention for re-cuts: same as the banked crop_20 pairs — render side =
frame-res downscale of the render subregion, orig side = raw frame crop (matched
effective scale 1.0/1.0, per axis). Orig-side crops are byte-identical to the
crop_20 originals (frame unchanged).
