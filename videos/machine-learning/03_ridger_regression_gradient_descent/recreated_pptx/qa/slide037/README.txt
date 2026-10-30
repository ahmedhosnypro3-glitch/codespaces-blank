S12b evidence regeneration (pool run 299640) — slide 037
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's four crop_6_* judge transcripts. Zero vision calls; no deliverable, DB
row, or transcript modified. Only render_regen.png + the crop pairs + this
README are new.

Render
------
slide_037_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide037/render_regen.png, 2001x1125.
render_regen.png md5: 21a00c30e89014dd6a7647396ff72ec4

Regions cut — coordinates AND construction taken from this dir's banked
selfcheck_attempt_6.py §6, which both documents and performed the banked cut:
scalar S = render_W/960 = 2001/960 = 2.084375 applied to BOTH axes, render crop
at int(round(v*S)) edges, original crop LANCZOS-resized to the render crop's
exact pixel size:

1. crop_6_def_lines  (70, 135, 860, 202)  -> pair 1647x140 (banked 1647x140, MATCH)
2. crop_6_eq_stack   (140, 250, 884, 306) -> pair 1551x117 (banked 1551x117, MATCH)
3. crop_6_update_eqs (75, 395, 790, 460)  -> pair 1491x136 (banked 1491x136, MATCH)
4. crop_6_green_box  (70, 455, 500, 525)  -> pair 896x146  (banked 896x146, MATCH)

All four banked pair sizes (crop_6_*_judge.txt headers) reproduced exactly, and
all four regenerated ORIGINAL-side md5s are byte-identical to the md5s the
banked transcripts record for the banked crops (def_lines 8a64cd66f45cfdc7990ba99da1384f9d,
eq_stack 1922ebf4f3a5a1f3a1625f5e4a7e2831, green_box 4fc9433ed415d488a6e31f10a1b06780,
update_eqs e4d4de23451bdf3c325d041c78a1a6b4). The original side is a
deterministic LANCZOS resize of the same source box, so byte equality proves
the boxes and construction reproduce the banked cut exactly.

Files created:
  render_regen.png
  crop_6_def_lines_render.png  (2b4d689357ea15d8e7625ef5fe644c8a)
  crop_6_def_lines_orig.png    (8a64cd66f45cfdc7990ba99da1384f9d)
  crop_6_eq_stack_render.png   (8673078afd16f23b5703d1655260fa82)
  crop_6_eq_stack_orig.png     (1922ebf4f3a5a1f3a1625f5e4a7e2831)
  crop_6_update_eqs_render.png (e4261b2bfd0a8634e2d67260b2cec9ca)
  crop_6_update_eqs_orig.png   (e4d4de23451bdf3c325d041c78a1a6b4)
  crop_6_green_box_render.png  (ed52aa171e139736163b7c865171f2a2)
  crop_6_green_box_orig.png    (4fc9433ed415d488a6e31f10a1b06780)
  README.txt (this file)

Not regenerated: crop_4_eq_stack (crop_4_eq_stack_judge.txt) was cut from
render_4.png, which no longer exists; that transcript is already adjudicated
superseded banked history (crop_4_eq_stack_adjudication.txt: render_4 was
superseded by render_5, then render_6), and the region is covered by the
regenerated crop_6_eq_stack pair above.

Render-side byte note: the regenerated RENDER-side md5s differ from the md5s
the banked transcripts record (e.g. def_lines f81d053dddd09453c5f09f472abfccb2
vs 2b4d689357ea15d8e7625ef5fe644c8a) and render_regen.png != banked render_6
md5 7251b2caec4d74e5ff199aa98a814fe8 (judge_attempt_6.txt) — cross-environment
rasterizer bytes (codespace-era render_6 vs this machine); sizes and
original-side bytes match exactly. 039's byte-exact render match in this same
run scopes the same-machine determinism claim.

Verification (zero vision): banked selfcheck_attempt_6.py re-run (paths
patched, copy in scratch/tmp/s12b_selfcheck/) against render_regen.png ->
SELF-CHECK RESULT: PASS; its §6 re-cut all four pairs byte-identically to the
regenerated files (md5s compared before/after the re-run). The deliverable was
never mutated by the OMML leg (omml_prepass_note.md: NOT WRAPPED, deliverable
untouched).
Original-side crops cut from unique_slides/slide_037.jpg (960x540).
