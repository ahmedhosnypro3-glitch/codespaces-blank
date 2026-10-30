# Slide 050 — chart-region adjudication chain (att13 → att19 → att20), closed 2026-10-26

Controlling records: `w050_crop13_ADJUDICATION.md` (att13, chart F1–F7),
`crop_19_chart_judge.txt` (att19 crop FAIL), `w050_chartfix_pil_raw.txt` +
`w050_arrow_redstop_pil_raw.txt` (PIL forensics), `crop_20_chart_judge.txt`
(att20 crop PASS), `judge_attempt_20.txt` (att20 full legA PASS).

## The one real defect and its fix

The chart region had ONE substantive recurring defect across attempts, with two
descriptions at two zooms:

- att13 (crop_13 legs): findings F1 "extra triangle on the line ≈(1,4.1)" and
  F2 "broken/doubled stroke x≈0.4–0.9" were REFUTED as stated — both shapes are
  the +ve arrow annotation, present in the ORIGINAL too (orig arrow-1
  x402..415 y306..318). The att10-era MINOR arrow-geometry delta (render arrow-1
  31px vs orig ~13px; arrow-2 ~14px left) was left standing.
- att19 (crop_19, post-table-fix render): the same annotation zone now FAILED
  as one MAJOR — "'+ve' repositioned below the line, arrow pointing horizontal
  instead of down-left, plus a thick dark-red arrow/parallelogram blob lying
  ALONG the decision line with no counterpart in the original."

Root cause of the att19 state: the build carried TWO arrows — old "arrow 1"
hugged the decision line (the spurious on-line blob at PIL window x350..500
y260..330: orig 624 red px vs render 2169 px) and old "arrow 2" sat horizontal
beside '+ve'. The orig ground truth (fine-ASCII + runs, `w050_chartfix_pil_raw.txt`
F2b/F3): a SINGLE small arrow starting ON the line at ~(205,285) crop / branch
(415,309) frame, head down-left at 398..409/318..326; the earlier two-arrow
reading was a misread of one arrow's shaft+head.

FIX (att20 build): replaced both arrows with ONE shape —
`x:fx(399), y:fx(309), w:fw(16), h:fw(17), flipH:true, endArrowType:'triangle'`
(tail on the line, head down-left) and recentered the '+ve' text box to x=364
(glyph centre 385). r19→r20 render diff confined to frame x373..415 y287..328.

## att20 outcome (crop_20_chart_judge.txt + judge_attempt_20.txt)

- Chart crop: **PASS** — all 9 markers, axes, gridlines, line trajectory, "+ve"
  annotation verified matching; residual findings all MINOR:
  1. line color/weight (render ~9–10px "C00000-family darker" vs orig ~7px
     brighter red) — previously adjudicated REFUTED at att13 F5: orig stroke
     variance (#AD2134 fresh vs ~#C8303C build-era) exceeds the render delta;
     render 92211B sits inside the observed orig range; the "1.5–2× thicker"
     claim failed the F2b run-length decode (6.7 vs 6 px at frame scale). At
     crop zoom the thicker appearance is the same bounded delta, not a new
     defect. No fix.
  2. red triangles slightly larger/darker — marker-medium class, position and
     shape verified; no fix.
  3. magenta diamond hue — JPEG-shift class (att13 F4 precedent: the REAL
     defect there was fill FF94FF vs orig E034ED/E03EE9/E04BEB, fixed to
     MARK_MAG=E03FEB, verified vivid in render_19/20). No further fix.
  4. '+ve' letterforms marginally larger/bolder — text-medium class, same text/
     color/position. No fix.
- Full legA att20: **PASS** (judge_attempt_20.txt).

## Disposition

Chart region CLOSED at att20. DB row 50: gen_status='passed',
visual_check='PASS', visual_attempts=20, transcript judge_attempt_20.txt.
Final-deck page 50 updated + render gate PASS 0 px
(qa/final_deck_updates/gate_20261026-135509_p50).
