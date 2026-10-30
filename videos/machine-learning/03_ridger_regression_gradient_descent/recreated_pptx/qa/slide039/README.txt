S12b evidence regeneration (pool run 299640) — slide 039
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's three crop_2_* judge transcripts. Zero vision calls; no deliverable, DB
row, or transcript modified. Only render_regen.png + the crop pairs + this
README are new.

Render
------
slide_039_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide039/render_regen.png, 2001x1125.
render_regen.png md5: 7fdd25e202da8ffb68765ee8b49d35bb — byte-identical to the
banked OMML wrap-proof record (omml_prepass_note.md: baseline pre-wrap render
md5 == post-wrap render md5 == 7fdd25e202da8ffb68765ee8b49d35bb). Today's
pipeline reproduces the wrap leg's render bytes exactly, and the
OMML-wrapped deliverable's LibreOffice render is unchanged by the wrap.

Regions cut (frame-px bbox x0,y0,x1,y1; coord source: worker_report.md crop
table verbatim — eq_stack x339..863 y251..311, title_lines x114..842 y71..136,
notes_bullets x76..403 y300..378; construction: render crop at
(round(x0*2001/960), round(y0*1125/540))..(round(x1*..), round(y1*..));
original crop LANCZOS-upscaled to the render crop's exact pixel size — matched
effective scale by construction):

1. crop_2_eq_stack      (339, 251, 863, 311) -> pair 1092x125
2. crop_2_title_lines   (114, 71, 842, 136)  -> pair 1517x135
3. crop_2_notes_bullets (76, 300, 403, 378)  -> pair 682x163

No banked pixel-size record exists for this slide's pairs (the transcripts and
worker_report.md record frame bboxes only), so no size match is assertable;
the pairs are at matched effective scale by construction.

Files created:
  render_regen.png
  crop_2_eq_stack_render.png      (79b24ec50d236170358b9823b2aa4d7d)
  crop_2_eq_stack_orig.png        (5dca5095b7d45bd29928922d69a10767)
  crop_2_title_lines_render.png   (d0da8ad0a033e206370e7d01ec9b50c8)
  crop_2_title_lines_orig.png     (0d6c57afe46593a0b070647265a6377e)
  crop_2_notes_bullets_render.png (bbfdf1895022ca92597a12b2b8d353c6)
  crop_2_notes_bullets_orig.png   (9bec4a00edcdaa2e8ef72d219d4b6318)
  README.txt (this file)

Verification (zero vision): banked selfcheck_attempt_2.py re-run (takes the
render path as argv[1]; copy in scratch/tmp/s12b_selfcheck/) against
render_regen.png -> SELF-CHECK: PASS (all elements within tolerance; no wrapped
lines; equation ink present and inside the green callout; caption centres/pitch
match).
Original-side crops cut from unique_slides/slide_039.jpg (960x540).
