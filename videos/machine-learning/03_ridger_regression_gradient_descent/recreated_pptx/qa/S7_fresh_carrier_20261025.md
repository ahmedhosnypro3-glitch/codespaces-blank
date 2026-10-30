# S7 fresh-carrier resume note — 2026-10-25 (worker S7-worker-fresh-1792898500)

Prior S7 carriers died in app exits; mission DB scope `S7_judge_045_048_051` is
in_work (45 already certified by the 2026-10-24 carrier). State re-derived from
disk before any dispatch:

## Verified (no re-work needed)
- Judge inputs all CURRENT + chrome-legal: fresh LO re-renders of the current
  pptx files are pixel-identical to the banked judge inputs —
  048: render_9.png == fresh render (diff bbox None); 049: render_9.png == fresh;
  050: render_12.png == fresh; 051: render_2.png == fresh.
- house_chrome_check.py PASS on all four (048/049 render_9, 050 render_12,
  051 render_2) — checks for 048/049 run fresh this session (not previously banked).
- Staged dispatchers syntax-verified + payloads md5-verified:
  048 legA dispatch_legA_attempt7.sh (judge_prompt_1.txt = 8fc11962…, trailing NL),
  048 crops run_crop_judges_048.sh top_band|aug_iter|calc_panel on crop_9 pairs
  (payload crop_1_calc_panel_prompt.txt = f8fed3d1… frozen Template B);
  049 legA run_legs_049_local.sh legA (payload judge_prompt_1.txt = 9387f5fb…),
  049 legB same script header|legend|dxi|wstack|bottom (payload
  judge_prompt_B_template.txt = d137335f…, crop_9 pairs cut 03:30 from render_9);
  050 legA dispatch_legA_attempt10.sh (render_12, payload judge_payload_8.txt =
  9387f5fb…), 050 crops run_crop_judges_12.sh caption|mathzone|tableeq|pinkbox|
  chart|redstop (payload judge_payload_B_8.txt = c21c958c…);
  051 legA dispatch_legA_attempt2.sh (render_2, payload 9387f5fb…),
  051 legB dispatch_legB_attempt2.sh mats|aug|dec (payload 6ae2c27e…).
- All walls: analyzer --timeout 1200 inside `timeout 1700`, gate law <8 before
  each dispatch, ONE leg per Bash call, background+wait.

## In flight at handoff time (never double-dispatch)
- 049 legA attempt 10 (→ qa/slide049/judge_attempt_10.txt) fired 17:52:15 local
  by bash pid 21791 (run_legs_049_local.sh legA; timeout 1700 outer). If it
  wedges with no transcript, re-dispatch `run_legs_049_local.sh legA`.

## Due legs (in dispatch order)
1. 048: `dispatch_legA_attempt7.sh probe` then no-arg → judge_attempt_7.txt
2. 048 crops ×3: run_crop_judges_048.sh top_band / aug_iter / calc_panel
3. 050: dispatch_legA_attempt10.sh probe then no-arg → judge_attempt_10.txt
4. 050 crops ×6: run_crop_judges_12.sh (order caption, pinkbox, mathzone,
   tableeq, chart, redstop)
5. 051: dispatch_legA_attempt2.sh → judge_attempt_2.txt (no probe mode; gate
   check built in), then dispatch_legB_attempt2.sh mats|aug|dec
6. 049 legB ×5 after legA lands: run_legs_049_local.sh header|legend|dxi|wstack|bottom

## Adjudication banks to use (PIL-first, before any fix)
- 048: pil_adjudication_legA6_crop8.md (legA-6 + crop_8 items all refuted/fixed;
  build advanced to render_9 = underline fixes + per-cell class-row boxes)
- 049: pil_adjudication_049g.txt (D2/D5 fixed → W-column v2 per-row geometry;
  D1/D3/D4/D6 refuted with measurements)
- 050: w7_adjudication.md, w7_final_pil_table.txt, w050_legadj_*, w050_adjud*;
  last_error records attempt-9 findings #3 finalW-construct + #8 stop-text as
  CONFIRMED + FIXED into render_11/12 — do NOT re-litigate the w7 2-component
  revert; the later lane re-expanded the construct (substack+phantom rows,
  677x496) and PIL-verified y68..126/x743..823 vs orig y68..133/x744..821
- 051: worker_report.md wedge sections; attempt-2 build fully self-checked
  (tall-bracket matrices), no adjudication bank needed unless a leg FAILs

## Certification law (per slide, after legA + all crops clean/adjudicated)
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3
scripts/15_progress.py: set N visual_check PASS / set N visual_transcript
<legA transcript> / set N visual_attempts <n> / set N gen_status passed /
set N pptx_path <plain deliverable> / heartbeat / release / re-read get N
(claim()/set() can reset gen_status — restore before release).
Then mission DB: task closes + scope-done with note + event row.
Never commit; never delete banked evidence.
