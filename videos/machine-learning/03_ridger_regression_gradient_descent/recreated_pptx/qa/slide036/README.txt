README.txt — S12a evidence regeneration (pool run 299640, worker S12a-worker)

WHAT: regenerated the transient 150dpi renders consumed by the five banked cut
scripts (cut_crops_5/7/8, cut_zooms_7/8) and re-ran them so the banked
crop_7_*/crop_8_*/zoom_8_* evidence references existing bytes again.
Evidence-regeneration only; deliverable, DB rows and transcripts untouched;
zero vision calls.

RENDER (regenerated from current-bytes deliverable, 2026-10-25):
  source     recreated_pptx/slide_036_recreated.pptx — the CURRENT single
             plain-named deliverable INCLUDING the S13 OMML wrap (in place per
             the single-version law)
             md5 ee60a2abd2eedcf665b241ff3f594f49 (post-wrap; pre-wrap banked
             md5 ad2a07ddd2e688b40d57d20e5c6ea701 lives in worker_report.md §3)
  method     soffice 26.8.1.1 headless (-env:UserInstallation profile under
             project scratch/tmp) -> pdftoppm -r 150 -png
  files      render_5.png, render_7.png, render_8.png (all 2001x1125, identical
             bytes — three render numbers are needed by three script generations;
             per recipe all were rendered from the SAME current deliverable)
  md5        9477fc0fc9a5eb1a89e0cbc8e8288234 for all three
  provenance EXACT: this equals the S13/S17-verified render md5
             (qa/slide036/omml_prepass_note.md and PROGRESS_PANEL.md: pre-wrap
             backup render == post-wrap render == 9477fc0f…, 0 differing pixels
             of 2,251,225). The banked attempt-8 render_8 md5 (ad8676e6…) came
             from the 2026-10-24 LibreOffice; today's LO renders the same
             certified bytes deterministically (double-render verified).
  chrome     house_chrome_check.py render_8 → PASS with the banked
             house_chrome_8.txt values exactly (house_chrome_render8_regen_S12a.txt)

SCRIPT PATH FIX (trivial, per recipe step 3; disclosed):
  All five scripts hardcoded the old codespace root
  V = "/workspaces/codespaces-blank/ai_llm_slides/…". Replaced with the real
  namespace root on this machine. Originals backed up byte-for-byte at
  scratch/tmp/s12a_script_backups/ (md5s in the before-manifest
  scratch/tmp/s12a_manifest_before.txt). No other line changed.

SCRIPTS RUN (python3, stdout to NEW rerun logs; none of these scripts writes a
.txt itself, so no banked file was rewritten):
  cut_crops_5.py  PASS — crop_5_eq_stack 740x97, crop_5_delta_lines 820x102
                  (render crop resized to match, as the script prescribes)
  cut_crops_7.py  PASS — crop_7_eq_stack 1730x229, crop_7_delta_lines 1709x221,
                  crop_7_class_lines 1709x474 (== banked worker_report.md §5 sizes)
  cut_crops_8.py  PASS — crop_8_eq_stack 1730x229, crop_8_delta_lines 1709x221,
                  crop_8_class_lines 1709x474 (== banked sizes)
  cut_zooms_7.py  PASS — 8 zoom_7_* pairs
  cut_zooms_8.py  PASS — 8 zoom_8_* pairs

VERIFICATION vs banked md5s (worker_report.md §6):
  crop_8_eq_stack_orig.png      441376694dd8b7ef8e4af2e3dcc4ea41  == bank  EXACT
  crop_8_delta_lines_orig.png   b28e95abe75c143ae0f0da519bdb27d5  == bank  EXACT
  crop_8_class_lines_orig.png   0e26e68784e3a05df1845d33c6f3fba7  == bank  EXACT
  (original side byte-identical to the certified evidence; render side derives
  from the S17-verified render bytes above)

FILES CREATED (all new):
  render_5.png, render_7.png, render_8.png
  crop_5_{eq_stack,delta_lines}_{orig,render}.png            (4)
  crop_7_{eq_stack,delta_lines,class_lines}_{orig,render}.png (6)
  crop_8_{eq_stack,delta_lines,class_lines}_{orig,render}.png (6)
  zoom_7_*_{orig,render}.png (16), zoom_8_*_{orig,render}.png (16)
  cut_crops_5_rerun_S12a.out.txt, cut_crops_7_rerun_S12a.out.txt,
  cut_crops_8_rerun_S12a.out.txt, cut_zooms_7_rerun_S12a.out.txt,
  cut_zooms_8_rerun_S12a.out.txt
  house_chrome_render8_regen_S12a.txt
  README.txt (this file)

NOT TOUCHED: slide_036_recreated.pptx (verified md5 ee60a2ab… unchanged after all
work), build/slide_036.js, all banked transcripts (judge_attempt_8.txt,
crop_8_*_judge.txt, cut_crops_5/7/8.txt, cut_zooms_7/8.txt, audit_8.txt, payloads,
assets_eq_036_error_attempt7.*), qa/slide_036/dispatch_brief.txt, all other qa files.
