S12b evidence regeneration (pool run 299640) — slide 012
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's FINAL certificate. Zero vision calls; no deliverable, DB row, or
transcript modified. Only render_regen.png + the crop pair + this README are new.

Render
------
slide_012_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide012/render_regen.png, 2001x1125.
render_regen.png md5: f481c04973ae93643d113286ecd88a55

Region cut (frame-px bbox; construction per Procedure B step 3: render crop at
(round(x0*2001/960), round(y0*1125/540))..(round(x1*..), round(y1*..)); original
crop LANCZOS-upscaled to the render crop's exact pixel size — matched effective
scale by construction):

1. crop_4_perfect (203, 120, 571, 260) -> pair 767x292 (banked 767x292, MATCH)
   coord source: worker_report.md zoomed-crop section verbatim: "Pair:
   crop_4_perfect_render.png vs crop_4_perfect_orig.png (both 767x292, re-cut
   from render_3.png at matched effective scale, original upscaled LANCZOS to
   match). Region: the perfect training table, x203..571 y120..260."

Files created:
  render_regen.png
  crop_4_perfect_render.png (2358efad612239c1760dd1bdc532fde4)
  crop_4_perfect_orig.png   (e0085a00586f0bfbff1f635c5c68bf9a)
  README.txt (this file)

Not regenerated: crop_2_perfect_table_judge.txt (attempt-1 certificate) was cut
from render_1.png, which no longer exists; worker_report.md records render_1 vs
render_3 differing in 790,109 of 2,251,125 px, so that transcript is superseded
banked history and its pair cannot be faithfully re-cut. The current-build
certificate is crop_4_perfect (regenerated above).

Verification (zero vision):
- Perfect-table column gridline centers on render_regen.png measured at
  [203, 244, 285, 326, 367, 407, 448, 489, 530, 572] vs original frame
  [202..204, 244, 285, 326, 367, 407, 448, 489, 529/530, 571/572] — exact
  center match (original lines are ~3px wide, render lines 1px).
- Arrow anchor re-measured in the y244..258 window: x670..705 y248..253 vs
  the banked render_3 measurement x671..705 y248..253 (worker_report;
  original x669..705 y246..251) — ≤1px edge-rounding on the left edge.
- Region ink present on both sides of every cut pair.
- Build-era probe verify_fixes.py (re-run on current bytes) reproduces its
  banked outputs: header phase RED/BLUE/RED on both sides, render arrow-mask
  bbox x670..705 y248..253, matching the banked x671..705 within 1px edge
rounding. Its final "head left
  edge near x670: False" line is a unit bug inside the probe itself ((560 +
  xs.min())/sc mixes render-px and frame-px; unsatisfiable for any in-tolerance
  render — the banked run printed the same False); the printed strict-red bbox
  x670..714 y248..316 and stroke top y=248 (orig 246) are the authoritative
  anchor values and match the banked record.
Original-side crops cut from unique_slides/slide_012.jpg (960x540).

── S19 payload-exact confirmation round (2026-10-25) ──────────────────────
Payloads (byte-frozen from shared_patterns/judge_protocol_03.md, S16-verified):
  payload_A_confirm.txt        md5 9387f5fbb94ef05a31db19f1e018dde1 (= tplA)
  payload_B_N012_confirm.txt   = tplB (md5 d137335f924c3d7e8ff77bdcc68e8c6e)
                               with the mandated NNN→012 substitution only
Legs + transcripts:
  legA-1 (render_regen)      → judge_attempt_3_confirm.txt   FAIL (2 MAJOR)
  adjudication (PIL-first)   → adjudication_confirm_legA.txt
  legA-2 (render_4, Fix 1)   → judge_attempt_4_confirm.txt   FAIL (label col)
  legA-3 (render_6, Fix 2)   → judge_attempt_5_confirm.txt   TRANSPORT WALL
         (stream cut mid-sentence at 1041B, no verdict; banked as-is;
          re-dispatched byte-identical as attempt-6 → judge_attempt_6_confirm.txt)
  crop (perfect table)       → crop_4_perfect_table_judge_confirm.txt <pending>
Fixes applied (no cascade: makeTestTable untouched; 013/017/018 verified):
  Fix 1  test-table y-row fill FFF7C2 → CCFFE1 (measured mint 203,255,224)
  Fix 2  label column added: table x719→669, w154→204, colW [50,50,51,53],
         header ["","Test1","Test2","Test3"], rows X1/X2/y (dark, non-bold,
         left+middle aligned, white fill), SHADE guarded to value cells,
         phase re-anchored (Test1/2/3 stay RED/BLUE/RED)
Renders + md5 chain (deliverable slide_012_recreated.pptx):
  render_regen.png  f481c04973ae93643d113286ecd88a55  (pre-Fix-1, banked)
  pptx d7312b78233c990d1e0937a91fa1edc1 → render_4.png (Fix 1)
  pptx 3d1361064db14f8b671beb0167e8dc01 → render_5.png (Fix 2, valign-top interim)
  pptx 886a3536228f0fc7b65ff6cf57bd83ff → render_6.png e5432e50d1ac6176f43eb57712a56408
                                       (Fix 2 + valign middle, CURRENT)
Verification: house_chrome_check PASS on render_4/5/6; value columns byte-
  identical r4/r5/r6; perfect-table crop region [423..1190,250..542] ZERO-DIFF
  (crop certificate carries over); label glyphs Δ≤1px vs original
  (fix2_pil_verify*.txt). Banked: slide_012_recreated_prefix2.pptx.
C2 corroboration: s19_corroborate_label_ink.txt (achromatic label ink vs
  same-frame muted-blue data ink; fix recipe + cascade proof for the
  open residual task).

── S19 close addendum (fresh carrier agent-46, agent-zq2at9bw, 2026-10-25) ──
Crop leg LANDED before the last carrier died: crop_4_perfect_table_judge_confirm.txt
  (complete, PASS, 4 MINORs) — adjudicated in adjudication_crop_confirm.txt:
  C1/C3/C4 certified-accepted, C2 (row-label ink blue vs original achromatic
  dark, PIL-confirmed NEW MINOR) banked as accepted residual + open DB task
  slide_012_label_ink_residual. No fix loop. legA = PASS by adjudication
  (adjudication_confirm_legA6.txt: attempt-6 MAJOR = third re-raise of F-N2,
  REFUTED; 4 MINORs certified-accepted). Slide 012 S19: ALL LEGS CLEAN.
Line 68 above ("crop ... <pending>") is RESOLVED by that transcript + adjudication.
Deliverable md5 superseded 886a3536228f0fc7b65ff6cf57bd83ff →
  c65c53b5e1dae8dd23516c1adc28a8f2 (carrier-side no-op rebuild via require()
  of build/slide_012.js, which writes at import; content-identity proven:
  slide1.xml raw-equal to final-deck page 12 + fresh LO render byte-identical
  to render_6.png e5432e50d1ac6176f43eb57712a56408, 0/2,251,125 px) —
  INCIDENT_deliverable_md5_supersession.md. Never require() build/slide_NNN.js
  for load checks; require build/components/*.js only.
