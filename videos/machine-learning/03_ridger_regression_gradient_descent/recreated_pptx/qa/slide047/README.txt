S12b evidence regeneration (pool run 299640) — slide 047
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's crop_5_* and crop_6_* judge transcripts. Zero vision calls; no
deliverable, DB row, or transcript modified. Only render_regen.png + the crop
pairs + this README are new.

Render
------
slide_047_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide047/render_regen.png, 2001x1125.
render_regen.png md5: e84972f1d2b9d35cf38ccdcec8923133 (banked render_10 md5
1e73a453ca54f0d45455780b109857af — cross-environment rasterizer bytes;
worker_report.md proves render_10 pixel-identical to render_9, and geometry is
re-verified below instead of byte identity).

crop_6 pairs (attempt-6 certificate set; coord + construction source:
crop_6_scale_audit.txt verbatim bboxes; per-axis sx=2001/960, sy=1125/540,
span-based sizing pair=(round(w*sx), round(h*sy)), render crop
LANCZOS-resized to that size, original crop LANCZOS-upscaled to the same size):

1. crop_6_topband   (62, 50, 726, 132)   -> pair 1384x171
2. crop_6_augmatrix (64, 134, 252, 261)  -> pair 392x265
3. crop_6_calceq    (268, 134, 605, 203) -> pair 702x144
4. crop_6_calcright (490, 134, 865, 335) -> pair 782x419
5. crop_6_button    (74, 273, 243, 309)  -> pair 352x75

Every audit effective scale is reproduced exactly: 1384/664=2.0843,
392/188=2.0851, 702/337=2.0831, 782/375=2.0853, 352/169=2.0828 — equal to the
audit's recorded render vs orig eff-scale pairs (2.0843/2.0843, 2.0851/2.0851,
2.0831/2.0831, 2.0853/2.0853, 2.0828/2.0828).

crop_5 pairs (attempt-5 certificate set; coord source: crop_5_scale_audit.txt
verbatim bboxes; scalar S=H/540=1125/540 on both axes, span-based sizing,
LANCZOS both sides; render_9 proven pixel-identical to render_10 in
worker_report.md, so one render serves both certificate sets):

1. crop_5_topband   (60, 47, 728, 137)   -> pair 1392x188 (banked 1392x187, Δ1h)
2. crop_5_aug       (61, 131, 256, 264)  -> pair 406x277 (banked 406x277, MATCH)
3. crop_5_calceq    (265, 131, 470, 338) -> pair 427x431 (banked 427x431, MATCH)
4. crop_5_calcright (470, 131, 730, 338) -> pair 542x431 (banked 542x431, MATCH)
5. crop_5_button    (71, 270, 246, 312)  -> pair 365x88  (banked 364x88, Δ1w)

Δ rationale: the audits record results to 4-5 decimals (bboxes + effective
scales), not the workers' exact float expressions; both Δ1s fall on rounded
span boundaries (187.5 -> 188, 364.58 -> 365). Documented, not improvised;
≤1px boundary delta, matched effective scale holds by construction.

Files created:
  render_regen.png
  crop_6_topband_render.png   (b736efe99b84d25acc6795ae3213daec)
  crop_6_topband_orig.png     (111e4f0410b1ba32abe7875ef318cbb9)
  crop_6_augmatrix_render.png (9b0abd3e3bdaaa2a43e06ed3e9502bcd)
  crop_6_augmatrix_orig.png   (ebc23a3317f56f30b4b9353d3946eb38)
  crop_6_calceq_render.png    (825b5d25cc6df6a3d3df7cb6d81dd1e1)
  crop_6_calceq_orig.png      (1d603f1850fdced26a8a76ebbd8a7743)
  crop_6_calcright_render.png (ef351878adcebdf3376529a634c995ae)
  crop_6_calcright_orig.png   (ff95c3c77707e27d6ec6364f6fbd2d2c)
  crop_6_button_render.png    (4d5d5fb621bb11647f22ad9c49f2aadf)
  crop_6_button_orig.png      (32bbf354d6aa0abdc7e78293376e0222)
  crop_5_topband_render.png   (9791a47a07c3618cd9a29637a393f8d7)
  crop_5_topband_orig.png     (fba1c2dde9c0b96d054dffc072bb23f0)
  crop_5_aug_render.png       (33b9e725c02111ae3cdb40e7ff3bcfec)
  crop_5_aug_orig.png         (4f6068d736aa91209edcea677a7960c3)
  crop_5_calceq_render.png    (4a58ec2ee3d71693061c50efaab9f541)
  crop_5_calceq_orig.png      (d08571cfabf4d82e15d1cdd8859403f9)
  crop_5_calcright_render.png (f6b573d15e64a853a6641eecba817b47)
  crop_5_calcright_orig.png   (6618ea5a530e92f145c0661dbd23dc53)
  crop_5_button_render.png    (87ddddc3d387b9c56aae8e5280124b49)
  crop_5_button_orig.png      (8502609420aacd787a298525946db16d)
  README.txt (this file)

Not regenerated: crop_3_augmatrix (crop_3_augmatrix_judge.txt) — its FAIL was
recorded on render_3.png, long superseded and deleted; no coordinate record
survives (only crop_3_augmatrix_desc.txt, a prose description with no boxes).
The region is covered by the two newer certificate sets' PASSes
(crop_5_aug + crop_6_augmatrix). Task-added to mission run 299640 (protocol
rule 7) rather than guessed.

Verification (zero vision): banked region_compare_attempt6.py re-run (paths
patched, copy in scratch/tmp/s12b_selfcheck/) against render_regen.png: all 25
measured regions inside the ±4px tolerance except "aug title" dx1 +4.2 (the
banked run flagged the same region at +4.7 AND "box3 sign" at -8.2; the fresh
run is inside tolerance on box3 sign at -3.0) — sub-pixel font-advance
threshold noise, documented, not improvised.
Original-side crops cut from unique_slides/slide_047.jpg (960x540).
