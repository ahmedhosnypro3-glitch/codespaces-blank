README.txt — S12a evidence regeneration (pool run 299640, worker S12a-worker)

WHAT: regenerated the transient 150dpi render consumed by the banked cut scripts,
then re-ran the certified cut script so the banked crop_3_* judge transcripts
reference existing bytes again. Evidence-regeneration only; deliverable, DB rows
and transcripts untouched; zero vision calls.

RENDER (regenerated from current-bytes deliverable, 2026-10-25):
  source     recreated_pptx/slide_010_recreated.pptx
             md5 9b4ee43ad50f90f09df108c1645c4d26 (== banked worker_report.md md5)
  method     soffice 26.8.1.1 headless (-env:UserInstallation profile under
             project scratch/tmp) -> pdftoppm -r 150 -png
  files      render_1.png, render_3.png (both 2001x1125, identical bytes — the
             script for attempt 1 expects render_1, attempt 3 expects render_3;
             both are the SAME current deliverable rendered once)
  md5        0003a04e677c7ac34985e7c142ea4786
  note       the historical render_3 md5 was 637426c5f7b87d32b689da818c34ce34
             (LibreOffice of 2026-10-24). Same-day same-version renders here are
             byte-deterministic (verified by double render), so the md5 delta is
             a LO-version artifact. Pixel-level fidelity of the regen render was
             confirmed: house_chrome_check.py reproduces the banked
             house_chrome_3.txt values exactly (panel x112-1882 y94-bottom,
             badge center (1824,152) d=68 -> house_chrome_3_regen_S12a.txt).

SCRIPTS RUN (python3, from this directory):
  cut_crops_3.py  — the certified attempt-3 cutter. PASS: 4 pairs
    chart_left 805x787, chart_right 834x787, cap_left 738x120, cap_right 742x120
    — sizes identical to the bank. The script rewrites cut_crops_3.txt; the new
    content is byte-identical to the banked file (md5 e1ffd9d514b048ec1264c0adae9394b7,
    verified against a pre-run snapshot), so no banked evidence changed.
  cut_crops_1.py  — NOT RUN to completion: banks 6-element region tuples but
    unpacks 5 (lines 44 and 59) — a logic bug, not a path issue; recorded as
    mission task-add (id 5, scope S12a_crops_with_scripts) and left unfixed per
    recipe. cut_crops_1.txt was never banked historically either. Its render
    (render_1.png) is in place per recipe; crops for the superseded attempt-1
    family do not exist and no transcript references them.

FILES CREATED (all new):
  render_1.png, render_3.png
  crop_3_chart_left_{render,orig}.png, crop_3_chart_right_{render,orig}.png,
  crop_3_cap_left_{render,orig}.png, crop_3_cap_right_{render,orig}.png
  cut_crops_3_rerun_S12a.out.txt (stdout of the rerun; banked cut_crops_3.txt
    untouched in content)
  cut_crops_1_rerun_S12a.out.txt (stdout of the failed cut_crops_1.py attempt)
  house_chrome_3_regen_S12a.txt (chrome check on the regenerated render_3)

NOT TOUCHED: slide_010_recreated.pptx, build/slide_010.js, build/components/slide_009.js,
all banked transcripts (judge_attempt_3.txt, crop_3_*_judge.txt, cut_crops_3.txt,
house_chrome_3.txt, payloads), all other qa files.
