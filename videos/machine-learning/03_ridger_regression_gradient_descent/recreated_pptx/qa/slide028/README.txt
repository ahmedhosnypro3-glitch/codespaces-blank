README.txt — S12a evidence regeneration (pool run 299640, worker S12a-worker)

WHAT: regenerated the transient 150dpi render (render_8.png) consumed by the
attempt-8 crop family, and re-created the crop_8_{left,right}_curve pairs whose
bytes had been consumed. The original cut script for this family was transient
(only its run log crop_8_cut.out.txt survived) — a faithful Procedure-B
re-implementation was written as a NEW file. Evidence-regeneration only;
deliverable, DB rows and transcripts untouched; zero vision calls.

RENDER (regenerated from current-bytes deliverable, 2026-10-25):
  source     recreated_pptx/slide_028_recreated.pptx
             md5 cba49e51d031a37a9d8f003bbfee95a5 (== banked worker_report.md md5)
  method     soffice 26.8.1.1 headless (-env:UserInstallation profile under
             project scratch/tmp) -> pdftoppm -r 150 -png
  file       render_8.png (2001x1125)
  md5        3f29a2f6fda667bc4a23952d1666a405
  note       banked historical render_8 md5 was 13c175d4dc6637f63d2b4f4a7acab8a0
             (LibreOffice of 2026-10-24; same-day same-version renders here are
             byte-deterministic, verified by double render, so the delta is a
             LO-version artifact). Pixel-level fidelity confirmed:
             house_chrome_check.py on the regen render reproduces the banked
             house_chrome_check_attempt_8.out.txt values exactly
             (house_chrome_render8_regen_S12a.txt). The worker report also
             already records a fresh re-render of this pptx PIL-matching the
             banked render_8 within 1px AA.

SCRIPT RUN:
  cut_crops_8_regen_S12a.py (NEW file) — Procedure B at the frame boxes recorded
  in the banked crop_8_cut.out.txt:
    left_curve  frame (152,208,400,466) -> 517x538
    right_curve frame (498,205,792,466) -> 613x544
  stdout: cut_crops_8_regen_S12a.out.txt
  VERIFICATION vs banked md5s (worker_report.md):
    crop_8_left_curve_orig.png  db51d8adb37b8b71336baa35c0b7041b  == bank  EXACT
    crop_8_right_curve_orig.png 35aa26682d33fc0dffc824bc1ee62026  == bank  EXACT
  The original-side crops are byte-identical to the certified evidence (the
  original frame is unchanged), so the regenerated pairs are faithful inputs for
  the banked crop_8_*_judge.txt transcripts. Render-side md5s necessarily differ
  (they derive from the regenerated render; sizes match the bank).

FILES CREATED (all new):
  render_8.png
  cut_crops_8_regen_S12a.py, cut_crops_8_regen_S12a.out.txt
  crop_8_left_curve_{render,orig}.png, crop_8_right_curve_{render,orig}.png
  house_chrome_render8_regen_S12a.txt
  README.txt (this file)

NOT TOUCHED: slide_028_recreated.pptx, build/slide_028.js, all banked transcripts
(judge_attempt_8.txt, crop_8_*_judge.txt, crop_8_cut.out.txt, payloads, probes),
leftpanel_probe.png / rightpanel_probe.png, all other qa files.
