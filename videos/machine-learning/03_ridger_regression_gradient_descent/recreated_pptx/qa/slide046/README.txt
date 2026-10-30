README.txt — S12a evidence regeneration (pool run 299640, worker S12a-worker)

WHAT: regenerated the transient 150dpi render (render_4.png) consumed by the
banked cut_crops_4.py and re-ran it so the banked crop_4_* judge transcripts
reference existing bytes again. Evidence-regeneration only; deliverable, DB rows
and transcripts untouched; zero vision calls.

RENDER (regenerated from current-bytes deliverable, 2026-10-25):
  source     recreated_pptx/slide_046_recreated.pptx
             md5 29cafaafa8b1234a6f063a6a2c909706
             (no OMML wrap on this slide — see omml_prepass_note.md: the eq_046
             sidecars are stale, the embedded media are m046_* matplotlib text
             assets; nothing to wrap. The certified worker_report.md also
             records that a fresh re-render of the current pptx is
             pixel-identical to the banked render_4.)
  method     soffice 26.8.1.1 headless (-env:UserInstallation profile under
             project scratch/tmp) -> pdftoppm -r 150 -png
  file       render_4.png (2001x1125)
  md5        a0a7aad3f48064db1dc6e119c34244f1
  note       banked historical render_4 md5 was a68b112d2d0866b77cc59ca82ff6378b
             (LibreOffice of 2026-10-24; same-day same-version renders here are
             byte-deterministic, verified by double render, so the delta is a
             LO-version artifact). Pixel-level fidelity confirmed:
             house_chrome_check.py on the regen render reproduces the banked
             house_chrome_check_attempt_4.txt values exactly
             (house_chrome_render4_regen_S12a.txt).

SCRIPT RUN:
  cut_crops_4.py (banked, unmodified) — run with python3 from the PROJECT ROOT
  (the script's own contract: its D= path is CWD-relative). PASS: 7 regions,
  14 PNGs; every size matches the banked cut_crops_4.txt exactly:
    topmatrix (1385,167)  zmatrix (167,118)  initial (416,120)
    yellowbox (217,195)   augbox (400,255)   plot (1093,669)  stopbox (402,200)
  and every orig-crop byte size matches the banked log line-for-line
  (167804/21091/34175/27445/83090/97718/57221).
  stdout: cut_crops_4_rerun_S12a.out.txt (the script prints only; the banked
  cut_crops_4.txt was not rewritten).

FILES CREATED (all new):
  render_4.png
  crop_4_{topmatrix,zmatrix,initial,yellowbox,augbox,plot,stopbox}_{render,orig}.png (14)
  cut_crops_4_rerun_S12a.out.txt
  house_chrome_render4_regen_S12a.txt
  README.txt (this file)

NOT TOUCHED: slide_046_recreated.pptx, build/slide_046.js, gen_math_046.py,
all banked transcripts (crop_4_*_judge.txt, cut_crops_4.txt, payloads,
judge_prompt_4.txt, verification notes), the pre-existing banked render_3.png,
all other qa files.
