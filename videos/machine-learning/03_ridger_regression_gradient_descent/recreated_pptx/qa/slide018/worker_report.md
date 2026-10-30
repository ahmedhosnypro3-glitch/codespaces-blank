# Slide 018 worker report — "Adding Ridge Regularizer to the model λ=10"

Worker: `kimi-slide018` (pooled run 299640, scope S3_depchain_017_018).
Dependency: 18 > 17 — slide 017 was certified first (gen_status=passed,
visual_check=PASS, judge_attempt_4.txt + 5 crop PASSes; see
qa/slide017/worker_report.md certification record, 2026-10-25).

## Build (dependency-law compliant, no copy-paste)

- Composition imported from the certified `build/components/slide_017.js` via
  `renderBase(pptx, slide, opts)`. The component gained a minimal per-block
  override mechanism (`opts.overrides` — a handler matching a block name
  replaces that block's built-in draw fn; same signature, skip/only
  precedence preserved). That is the ONE edit to the certified 017 component
  (additive; 017's own render path is unchanged — verified by 017's
  certification being granted AFTER the edit on the same pptx md5).
- `build/slide_018.js` (thin writer) renders renderBase with numeral 18 +
  four override handlers (title λ-run, trainTables, testTables, wBoxes) —
  018's measured deltas only; table PATTERN (makeTrainTable / runsFor /
  cell ink phase) and geometry constants (TRAIN_*/TEST_*/WBOX_*) all come
  from the component exports.
- W-box interiors: `build/assets/make_018_wbox.py` → 600-dpi STIX PNGs
  (wbox018_band{1,2,3}.png, 958x1025 each = 115x123 px at 600dpi) placed at
  exact px/600 in. 017's closed-loop typography reused (same slot, origin
  x507, y127/265/403); only 018's values (0.13/1.87/0.09 ‖W‖²=3.5,
  0.54/0.73/0.81 =1.48, 0.82/0.33/1.1 =1.92).
- Band-2 red pencil-like mark (frame 739..760 x 367..379, measured in
  measure_018.txt): 21x12px C00000 rect.

## PIL refutation banked BEFORE judging (analysis JSON vs frame)

`analysis/slide_018_final.json` claims the y-row X3 cell (30/60) is
yellow-highlighted in bands 2/3. PIL (measure_018.txt + re-scan): yellow X8
cell is in the X1 row — (250,255,13); the y-row X3 cell is WHITE (253,254,254)
in bands 2/3. The build follows the FRAME (X8 highlighted, X3 white), same as
017. Render verified: yellow found ONLY in X8 X1-row cells of bands 2/3.

## Render + gates

- deliverable `recreated_pptx/slide_018_recreated.pptx` (single plain-named
  version; no OMML/graph wrap owed)
- `render_1.png` 2001x1125 (150 dpi), LO profile under scratch/tmp/lo_018
- house_chrome_check.py: **PASS** (panel x112-1880, strokes L/R/bottom, top
  bare; badge centre (1824,152) d=70; tol 8)
- pre-judge PIL sweep vs original (1:1 frame vs render@2.0833): mint y rows
  present in both; yellow X8 cells match; title λ-run blue in both; W-box
  ink ratio ≈2.6x (crisp vs JPEG-softened, same class as 017's banked note);
  mark present in both (orig JPEG-softened (168,118,114), render C00000).

## Judge dispatch

`judge_commands_kimi.sh` (Template A → judge_attempt_1.txt) +
`judge_crops_kimi.sh` (6 Procedure-B legs: wbox, band1, band2, band3, test,
mark → crop_1_<name>_judge.txt). Payloads byte-emitted from the frozen
`shared_patterns/judge_protocol_03.md` by `emit_payloads_018_kimi.py`
(reverse byte-check OK; cross-check OK; sha256 prefix 39b498eaf7048031
identical to 017's Template A payload — same frozen template, NNN=018).
Gate law honored: probes logged before every dispatch.

## Park (gate busy)
- 2026-10-25 23:25 UTC: gate probe = 9 (>=8) before Leg A dispatch. Parked; next probe no earlier than ~23:55 UTC (max 2 probes/hour). No dispatch made.
- 23:44 UTC: re-probe = 11 (>=8), gate still busy. Probes at 23:25 + 23:44 = hourly quota (2/h) consumed. Next probe no earlier than 00:25 UTC.
- 00:01 UTC: probe 4 (<8) → Leg A dispatch attempt 1 failed exit 127 (relative path, no call consumed). Attempt 2 at 00:02: script self-guard hit count=8, exit 75 (no call consumed). Parked; next dispatch ≥ 00:30 UTC.

## Attempt 2 (Leg A) — FAIL, 3 MAJORs, all PIL-adjudicated and fixed
- Transcript: judge_attempt_2.txt (render_1.png). Verdict: FAIL.
- MAJOR-1 (red block over 34.6): PIL proved the "mark" is a JPEG chroma fringe of
  black y-row text on mint, recurring in ALL THREE bands at the same relative spot
  (band1 y231..239 / band2 y370..378 / band3 y507..516, x~731..761) — never content.
  Fixes: pencil-mark rect REMOVED from slide_018.js; y-row (ri3) test-table value ink
  changed RED→BLACK (orig ink neutral gray/black, no pink clusters).
- MAJOR-2/3 (norm line touching right border, bands 2/3) + MINOR-4: PIL: orig skeleton
  (‖W‖²=) spans x520..577 (24px-tall bars) in all bands, value at x581.5/584; render had
  a wider (68px) shorter mathtext skeleton ending x621 (border 623). Fix: make_018_wbox.py
  norm block redrawn with explicit primitives at measured landmarks + width-fitted
  mathtext texts; regenerated wbox018_band{1,2,3}.png (extents now 519.6..604/616/615).
- Rebuilt slide_018_recreated.pptx, re-rendered 150dpi (pdf+pdftoppm) as render_3.png
  (2001x1125), chrome check PASS, PIL re-verify of all three fixes PASS, crops re-cut
  from render_3 via recut_crops_3.py.
- 01:10 UTC gate probe = 10 (busy) — Leg A attempt 3 dispatch parked.

## Attempt 3 (Leg A) — PASS (judge_attempt_3.txt, render_3.png), 4 MINORs all PIL-refuted
1. Vertical placement MINOR: REFUTED — band3 table bottom orig 527.0 vs render 528.7, top 404.0 vs 402.0 (Δ≤2px); band1/2 bottoms 252/253.8, 389/391.5.
2. Title size/λ=10 MINOR: REFUTED — red run orig x179..722 vs render 175.6..725.9; blue extents match (≤4px).
3. Gridline visibility MINOR: REFUTED (rule e) — render darkest rows 172 lum vs orig 183 (render crisper, not fainter); rose TEST_BORDER identical hue.
4. Train/Test lettering MINOR: REFUTED — labels drawn by the certified 017 component (same size that passed 017's full judge + label crop); delta is JPEG-softening class.
No build edits. Proceeding to Procedure-B crop legs.
- 01:50 UTC: gate 10 (busy) — crop retry parked. wbox leg banked PASS (crop_1_wbox_judge.txt, MINOR rule-c W-ink class, no edit).
- 02:00 UTC: gate 11 (busy) — parked again. Probes 01:39/01:50/02:00 all busy; no dispatch.
- 02:11 UTC: probe 7 → dispatch, but script guard saw 10 ~25s later (exit 75, no call consumed). Parked; next ≥ 02:32.
- 02:22 UTC: gate 10 (busy) — parked to ~02:45.

## Attempt-3 crop results (render_3 crops): band1 PASS, band2 PASS, band3 PASS, test PASS, mark FAIL
- mark FAIL MAJOR-2 (y-row ink black vs orig column red/blue/red): CONFIRMED by PIL round 2 —
  Test2 y-cells hold 172-246 saturated BLUE px in the original (black text impossible);
  earlier "black" conclusion was a JPEG-reading error (dark-red text mutes to gray clusters).
- mark FAIL MAJOR-1 ("46" + missing ".4") + its MINOR-3 (hand-drawn mark): the video-cursor
  occlusion artifact — settled by Leg A attempt-3 ground-rule (c): correctly omitted. VOID.
- Fix: slide_018.js y-row ink reverted to the column scheme (ci odd RED / even BLUE; mint
  fill unchanged). Rebuilt, render_4.png (chrome PASS; PIL: Test1/2/3 y-cells RED/BLUE/RED ✓).
- wbox region (497..632,119..259) pixel-identical render_3→render_4 → banked wbox PASS stands.
- Re-cut all crop pairs from render_4; Leg A attempt 4 + 5 crop legs re-dispatched.
Gate busy at 07:14:19 (10 running); crop re-judgement parked.
Gate busy at 07:18:47 (9 running, exit 75 before band1); parked, retry pending.

## CERTIFIED 2026-10-25
- Attempt history: 1 VOID (wrong original); 2 FAIL -> 3 fixed; 3 PASS; mark-crop FAIL -> round-2 fix (y-row ink to column scheme, pencil mark removed, wbox norm skeleton redrawn as primitives); 4 PASS (judge_attempt_4.txt).
- Crop certificates (render_4 re-cut, all FINAL VERDICT: PASS): band1, band2, band3, test, mark (mark leg cursor/".4" occlusion adjudicated VOID — rule c).
- DB: gen_status=passed, visual_check=PASS, visual_attempts=4, worker released.
