S12b evidence regeneration (pool run 299640) — slide 040
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's crop_3_* judge transcripts. Zero vision calls; no deliverable, DB row, or
transcript modified. Only render_regen.png + the crop pairs + this README are
new.

Render
------
slide_040_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide040/render_regen.png, 2001x1125.
render_regen.png md5: 0578cda44d07ca266caa1b0c15b4c336

Regions cut (frame-px bbox x0,y0,x1,y1; coord source: worker_report.md
verbatim — "Crop pairs were cut at matched effective scale ... (Sx=2001/960,
Sy=1125/540): title_block bbox 85,166..858,376 (1612×439), blue_line
359,240..589,300 (480×126), badge 850,47..904,101 (114×114)"; construction:
render crop at (round(x0*Sx), round(y0*Sy))..(round(x1*Sx), round(y1*Sy));
original crop LANCZOS-upscaled to the render crop's exact pixel size):

1. crop_3_title_block (85, 166, 858, 376) -> pair 1611x437 (banked 1612x439, Δ1w Δ2h)
2. crop_3_blue_line   (359, 240, 589, 300) -> pair 480x125 (banked 480x126, Δ1h)
3. crop_3_badge       (850, 47, 904, 101)  -> pair 112x112 (banked 114x114, Δ2w Δ2h)

Δ rationale: the report printed frame-px-ROUNDED bboxes next to the banked
pair sizes; the worker's exact sub-pixel floats are unrecoverable (the badge's
114x114 implies a ~849.5..904.5 box whose integer-rounded edges give 112).
The protocol-canonical integer construction above was applied to the printed
bboxes — matched effective scale holds by construction, the ≤2px delta is on
the cut boundary only, and the transcripts' findings are claims about ink
inside the regions, unchanged.

Files created:
  render_regen.png
  crop_3_title_block_render.png (ea686d3dae42cc9bb498b6765b0a450e)
  crop_3_title_block_orig.png   (cb28113ad03752ad9a2ce691ea1368ca)
  crop_3_blue_line_render.png   (73c33841a7df01a9ec6f9e590f801905)
  crop_3_blue_line_orig.png     (542dada83f0a7f1f04abf9d4686fb839)
  crop_3_badge_render.png       (c743209f8f710b9a026c5f5f5aac206e)
  crop_3_badge_orig.png         (3f7a64d1bdc6efd0d004fe288f7584eb)
  README.txt (this file)

Note: crop_3_badge was cut but never judged in the banked record (no
crop_3_badge_judge.txt exists — only blue_line and title_block were judged);
it is regenerated here for completeness with its two judged siblings, not to
hang a new certificate on it.

Verification (zero vision): banked selfcheck_attempt_3.py re-run (paths
patched, copy in scratch/tmp/s12b_selfcheck/) against render_regen.png ->
SELF-CHECK: PASS (background-chrome adjudication included: white canvas +
E9E9E7 panel on both sides).
Original-side crops cut from unique_slides/slide_040.jpg (960x540).
