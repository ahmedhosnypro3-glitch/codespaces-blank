# worker_report.md — S4 (worker-s4-3730479), slides 019 / 021 / 025 — 2026-10-25

## Slide 021 — CERTIFIED ✅
- Leg A attempt 12 PASS (`judge_attempt_12.txt`, real verdict body verified before
  certification). gen_status='passed', visual_check='PASS', released.

## Slide 019 — in progress (crop legs vs render_15)
- Attempt-9 leg A FAIL adjudicated PIL-first (findings #1/#2/#5/#6/#7 dismissed;
  #4 maroon rule fixed).
- Crop_10 assets found to be of UNKNOWN provenance (shapes ≠ validated regions);
  re-cut all pairs from render_10 with validated regions (`cut_crops_10v2.log`).
- First header_strip verdict on the bad crops DISCARDED (BLOCKER refuted by ink
  census: render crop 63.7% ink vs orig 64.9%).
- Re-cut header_strip verdict (attempt 11): MAJOR — orig holds stacked 2-D column
  vectors INSIDE the blue box; render had a linear line outside. PIL confirmed:
  orig 0 ink px right of box (x440..850 y66..160) vs render 3158; orig content
  rows y79..148 at x162..430.
- Fix 1: removed linear z-line; added stacked vector groups inside the box
  (render_11, md5 3ad5088e...).
- Crop verdict 12: MAJOR — parens must span both rows; MINOR z-labels red
  underlined, y-values blue. PIL: title color claim REFUTED (both words blue).
- Fix 2: tall parens (fs 44), red underlined z-labels, blue y-values (render_12).
- Crop verdict 13: MAJOR — missing category fills on header boxes; MINOR items.
  PIL confirmed cream/mint tinted header boxes (orig L3 cream 49%, L10 green
  51% coverage); "(as if λ=0)" red claim REFUTED (orig red runs x317..347 ARE in
  the NO-REG parenthetical).
- Fix 3: tinted header boxes FFF4E0 / E8FFE8 (render_13). → header_strip PASS ✅
- table_left verdict 13 FAIL: MAJORs — W vectors must be bracketed 3-entry
  column vectors (banked 2-component dismissal was WRONG — re-adjudicated: fine
  ASCII shows tall brackets x169..182 spanning y207..263 with 3 stacked values;
  doc-parse OCR reads (0.1, 1.95, 0.03) etc.); missing blue flow arrows (orig
  blue 0.33/0.24 in arrow zone); y-row must sit INSIDE the yellow band (orig
  green rows 276-294 inside band 272-303); outlier column color-coded stacked
  digits; test region is a bordered grid, not prose.
- Fixes 4-7 (render_14): color-coded stacked outlier digits, blue rightArrow per
  group, bordered test grid (header Test₁-₃, x₁/x₂ rows, green y row in band),
  W numerals black. Verdict 14: grid/colors/fills consistent; remaining MAJORs —
  outlier column needs bracket; W vectors need tall brackets (judge right).
- Fixes 8-9 (render_15): outlier left bracket; W blocks rebuilt as "[w1;w2;w3]"
  column vectors with fs-46 brackets; third entries recovered from printed
  ‖W‖² (sqrt(norm²−w1²−w2²)) and doc-parse OCR cross-check:
  NO REG (2,0,0)/(2.7,0.67,0.61)/(4,0.29,0.78);
  R3 (0.1,1.95,0.03)/(1.2,0.72,0.7)/(1.77,0.32,0.98);
  R10 (0.13,1.87,0.09)/(0.54,0.73,0.81)/(0.82,0.33,1.07).
- table_left attempt 15: NO VERDICT (3 upstream aborts: GarbageError / 630s
  HangError / EmptyStreamError) — honest no-verdict, re-dispatched as attempt 16.

## Slide 025 — in progress (build fixes applied, crop legs pending)
- Fix: LABEL_BLUE 0000FF → 0000A0 (orig LB1 navy 0,0,160).
- Fix: TR slanted red strokes measured (red-pixel map): A (860,189)→(655,209),
  B (737,210)→(755,225), in addition to horizontals y226/y234. Added both line
  shapes.
- render_11 built, chrome PASS. crop_11 pairs cut (all MATCHED). TR leg
  dispatched (attempt 11); title/lbl legs keep banked PASS certificates.

## Evidence
- qa/slide019/: render_11..15, crop_11..16_*, legs_status_crops_1[1-6]_s4.md
- qa/slide_025/: render_11, crop_11_*, dispatch_one_crop_11.sh
- OCR transcripts: scratch/tmp/w19parse/*.parse.md

## 2026-10-25 ~08:40Z — crop_16 table_left verdict adjudicated (FAIL) → fixes → render_16

- crop_16_table_left (attempt 16, post-router-restart) returned a real verdict: FAIL.
  - #1 MAJOR: NO-REG row-1 W vector rendered (2,0,0) top→bottom; original reads (0,2,0)
    (HIGH confidence). Adjudication: ACCEPTED. Note the tension — the printed test
    predictions (x1=30,x2=15→60) fit W=(2,0,·) mathematically — but founder law is
    verbatim fidelity and the judge read the original at matched scale; frame truth wins.
    FIX: w3 row 1 → ['0','2','0'] in build/slide_019.js.
  - #2 MINOR: missing enclosure rectangles around each W block. CONFIRMED by pixel
    census of the original: thin rects x129..206, bands y200..297 / 306..405 / 415..514
    (one per row group). FIX: added rect (x0+5, gy-5, 77×97) line 0.75 black around
    every W block in all three columns.
  - #3 MINOR low-conf: "W" not distinctly red. FIX (cheap): "W" red run + " =" black run.
  - #4 MINOR: crop-edge visibility only — no fix.
- NO-REG rows 2/3 third-entry provenance unchanged (sqrt(norm²−w1²−w2²)+OCR; row 3
  checks out: 4²+0.29²+0.78²=16.69≈16.7; row 2 norm printed 8.11 fits w1²+w2² alone —
  recorded, not re-derived).
- Rebuilt slide_019_recreated.pptx (08:34Z), rendered render_16.png (150dpi), house
  chrome check PASS.
- Re-cut crop_17 pairs for all 4 legs from render_16 (matched-scale, same regions as
  crop_16); created dispatch_B17.sh.
- Gate note: router restarted mid-session (all legs 05:11–05:21Z died with connection
  refused / premature close — several NO VERDICTs). Fleet heavily shared tonight;
  pgrep-based load includes other workers' waiter shells.
- 025: tr attempt 11 dispatched 3× — first two died on the router restart, third
  queued behind fleet load (no window within 600s). Title/lbl banked PASS stands.

## 2026-10-25 ~12:40Z — crop_17 table_left FAIL adjudicated → 5 fixes → render_17 → crop_18 wave

- crop_17_table_left (attempt 17) FAIL; values all matched (0/2/0 ✓, ridge panel ✓).
  Findings adjudicated:
  - #1 MAJOR label column outside grid border: CONFIRMED (outer rect started after
    labels). FIX: rect from gx0, label column inside with its own rule.
  - #2 MAJOR bracket-over-digits ("1.95"→"95"): CONFIRMED. FIX: parens moved to
    x0+40/x0+64 (w8), entries x0+47 w18 fs7, lineSpacing 20.
  - #3 MAJOR parens not brackets: ADOPTED (judge high-confidence at matched scale;
    raw 1px census ambiguous). FIX: ( ) fs42 both sides.
  - #4 MINOR yellow highlight on outlier "22": CONFIRMED (orig yellow x84..114,
    band y+66..+100 per group; rows 1&2 clear, row3 faint). FIX: yellow rect behind
    third outlier entry; entries re-spaced lineSpacing 33 to orig pitch (~y+0/+33/+66).
  - #5 MINOR W underline (bold-vector convention): CONFIRMED. FIX: underline on W in
    "W =" (kept red) and inside ‖W‖².
  - #6 MINOR extra filled black inter-column arrow: CONFIRMED ABSENT in orig
    (census x375..405/x630..672 y310..330 = only divider rules). FIX: removed both.
- Rebuilt (render_17), chrome PASS. Re-cut crop_18 pairs (4 legs) + dispatch_B18.sh.
- table_left attempt 18 dispatched (desc updated).

## 2026-10-25 13:05Z — PARK (gate starvation), scope closing

- Wave-2 dispatches (1700s caps) ALSO parked: "no window in 1604s (pgrep=19)" at
  13:03:36Z for BOTH table_left and 025-tr. Total 4 park waves 11:16→13:03Z; sibling
  workers (slide031→037→043→044 waves) held 6-20 slots continuously for ~110 min.
- Honest park per MISSION_PROTOCOL §4: DB last_error updated for 19 and 25 with
  resume specs (crop_18 legs via dispatch_B18.sh → Template A → certify; 025: crop_12
  legs via dispatch_one_crop_12.sh → Template A → certify). Claims released.
- No verdict bodies for the current build bytes of either slide — certification was
  NOT claimed. Build fixes, renders, chrome PASS, and staged dispatchers are all on
  disk; the next worker resumes by dispatching, not rebuilding.
