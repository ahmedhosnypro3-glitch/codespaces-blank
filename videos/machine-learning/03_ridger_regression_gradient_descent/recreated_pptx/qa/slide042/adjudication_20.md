# Slide 042 — attempt 20 adjudication (leg A judge_attempt_20.txt + PIL)

Full-slide leg A FAILED with 12 findings. Arbitration PIL-vs-frame (frame =
`unique_slides/slide_042.jpg`, 960x540, 1px=1pt), PIL-first per judging.md.

## REFUTED (with evidence)

1. **"missing d(x1) sixth box"** — REFUTED. Two independent zoomed reads (S20d
   stack 3x read + PIL box tops y217/273/340/406/472) confirm FIVE boxes
   starting d(x2). 041 covered d(x1) separately; the frame has no d(x1) box.
2. **"x3 row shows 1 2 1"** — REFUTED. S20d ground-truth read: row2 = |1 1 2|.
3. **"TL/Z vectors truncated to 2 rows / no parens"** — lean REFUTED. Banked
   frame reads: 2-row vectors (TL y78/y93; Z rows (0,0)(7,6)(3,2)). Note PIL
   thr185 merges the two rows into one band (y78..102), which likely fooled the
   judge into "3 components truncated"; finer per-column dumps pending from the
   crop legs (crop_20_tl_table / crop_20_topright) — if a crop leg contradicts,
   re-arbitrate with a 3x zoom of the frame region before any edit.
4. **"stray | delimiter fragments"** — REFUTED. The | bars ARE in the frame
   (PIL x327/x379, h~14, per-box).
5. **"Iteration box proportions"** — REFUTED. Banked frame-measured geometry
   (x84..214 y277..305, red, white bold 15pt).
6. **"red ⇐ on Update rows (plural)"** — REFUTED. Render_21 far-right zones
   x755..852 for boxes 1/2/4/5 contain ZERO colored pixels; red ⇐ exists only
   in box3 (also confirmed on render_20).

## CONFIRMED — fixed in attempt 21 (render_21.png, chrome PASS)

7. **#6 d(x_i) split-line** — CONFIRMED REAL. Old build drew "d(x", sub, ") ="
   as three separate text boxes with a visible gap (render runs
   291..311 vs frame 283..322). FIX: single addText run with inline
   `subscript: true` run. Rebuild d641e610…, render_21 md5
   c60285f2…; render label runs now contiguous, chrome PASS.
8. **#10 legend collision "positiveC2"** — CONFIRMED REAL (but only C2 x-pos).
   Frame ink: "positive," ends x302, blue C2 x312..326 (gap 10px); render_20 C2
   sat at x303..321 (gap 2px). FIX: C2 sub x310→312. Other legend fragments
   matched frame within 2-3px (negative 329..378, Zero 395..422,
   is unaccepted 430..508) — untouched.
9. **LM paren bottoms** (leg-A minor) — bottom "1" digits poked out below the
   LM enclosure lines. FIX: LM paren verticals h 56→60 (y166..226), bottom
   serif stubs y222→226. Verified: LM-region ink rows now end inside the box.

## PENDING crop-leg arbitration (do not edit before these land)

- Q1 InitialW third component (leg A: "InitialW 3-component truncated") —
  PIL InitialW zone x331..353 y62..102 is one merged ink mass (n=155);
  S20d said the frame may show TWO stacks (4/-2); delta_vs_related row 6
  requires topband vision verify. Awaiting crop_20_topright leg.
- Q2 TL vectors, Q3 Z vectors row counts — awaiting crop_20_tl_table /
  crop_20_topright legs; see note in #3 above.
- Q4 "Upgraded" vs "Augmented" caption — awaiting crop_20_lm_table leg;
  frame caption ink x82..236 y148..159. Current build says "Upgraded"
  (banked read). If the crop leg insists, re-zoom the caption at 3x before
  changing text (frame wins, never the analysis JSON).

## Fixed-not-in-scope

- Analysis-JSON delta: the analysis record mandates five wide W-update
  equations the frame does not draw — recorded as delta, never "fixed" toward.
