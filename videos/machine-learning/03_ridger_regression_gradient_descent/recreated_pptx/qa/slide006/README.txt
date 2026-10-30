S12b evidence regeneration (pool run 299640) — slide 006
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's judge transcripts. Zero vision calls; no deliverable, DB row, or
transcript modified. Only render_regen.png + the crop pairs + this README are new.

Render
------
slide_006_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide006/render_regen.png, 2001x1125 (same geometry
as the banked 150dpi renders).
render_regen.png md5: afa2f6cf71029a0c245d9bee769c96f9

Regions cut (frame-px bbox x0,y0,x1,y1; construction per judge_protocol_03.md
Procedure B step 3 and this slide's banked crop_scale_check_1.txt: render crop at
(round(x0*2001/960), round(y0*1125/540))..(round(x1*..), round(y1*..)); original
crop LANCZOS-upscaled to the render crop's exact pixel size — matched effective
scale by construction):

1. crop_1_textblock  (175, 74, 798, 463) -> pair 1298x811  (banked 1298x811, MATCH)
   coord source: worker_report.md "Crop frame bbox x175..798 y74..463 (both
   images) ... both 1298x811" + crop_scale_check_1.txt row "title".
2. crop_1_subtitle   (241, 159, 731, 465) -> pair 1022x638 (banked 1022x638, MATCH)
   coord source: worker_report.md third crop region + crop_scale_check_1.txt row
   "subtitle".
3. crop_1_badge      (856, 53, 896, 93)  -> pair 84x84     (banked 84x84, MATCH)
   coord source: worker_report.md second crop region ("frame bbox x856..896
   y53..93, rendered at 84x84 matched scale") + crop_scale_check_1.txt row "badge".

All three banked pair sizes reproduced exactly. Files created:
  render_regen.png
  crop_1_textblock_render.png (68ae44a35905c6bb5f5eb1872b1ff198)
  crop_1_textblock_orig.png   (6c0ff358e359daed369993fdb07d8790)
  crop_1_subtitle_render.png  (a3e6581d85c9a7c4128204955a3eb74b)
  crop_1_subtitle_orig.png    (d8b7a7a82a7ac745656a4fba1632e03f)
  crop_1_badge_render.png     (60c7058ffee2686d6a8e96f711688673)
  crop_1_badge_orig.png       (d0fa57030eb169766b92f5def27aeffb)
  README.txt (this file)

Not regenerated: crop_scale_check_1.txt also lists a 4th pair ("textblock"
1332x196, slide-space box 639.4x94.1) = the earlier crop_1_title_* pair (report
line "Banked: crop_1_title_render.png, crop_1_title_orig.png"). No judge
transcript references crop_1_title_* files, so no certificate hangs on it; not
re-cut.

Verification (zero vision): banked selfcheck_attempt_1.py re-run (paths patched
to this machine) against render_regen.png -> SELF-CHECK: PASS (title/subtitle ink
geometry within tolerance, all ink inside the house panel, badge numeral present).
Original-side crops cut from unique_slides/slide_006.jpg (960x540).
