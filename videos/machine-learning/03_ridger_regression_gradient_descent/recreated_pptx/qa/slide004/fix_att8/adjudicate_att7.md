# Adjudication of attempt-7 judge claims — slide 004 (PIL-first, this window)

Inputs: `judge_attempt_7.txt` (full slide, PASS), `crop_7_let_boxes_judge.txt` (FAIL),
`crop_7_where_block_judge.txt` (FAIL), `crop_7_remember_judge.txt` (PASS w/ recommendation).
All severity calls below re-measured on `unique_slides/slide_004.jpg` and
`render_7.png` / asset PNGs with PIL (mx<200 / r>150&g<130&b<130 masks).

## CONFIRMED -> fixed in attempt 8

1. **Vector entries black vs red (let_boxes #1/#6, full-slide #1 — MAJOR).**
   Orig: lead-in "Let Y =" dark x86..149; vector + subscript RED x158..208
   (red x158..194 vector, x198..208 subscript, n_red>>n_dark per column).
   Asset was 100% dark (red n=0). FIX: recolor_vectors.py — Yvec ink x>=435 red,
   Yhatvec ink x>=380 red (cuts sit in measured ink gaps x410..459 / x357..405).
   Post-recolor: Yvec red n=21050 x459..951, dark n=9663 x0..410; Yhatvec red
   n=23616 x405..893, dark n=7782 x0..357. Alpha bytes untouched.

2. **Loss-equation color (full-slide #6 — MINOR "all red vs black").**
   Orig: ONLY "Loss =" is red (x94..131 y483..497); body x136..392 dark. The
   full-slide judge overgeneralized. FIX: formula asset ink x<=388 red (asset
   "Loss =" x0..363, body from x414), body stays black.

3. **Formula position (full-slide implicit; window-3 measured).**
   render_7 formula ink x77..459 vs orig x93..392. FIX: eqImage -> (93, 472.8,
   4.1528, 0.3789) mapping asset ink onto the orig span. render_8 ink
   x94..391 y472..500 (orig x93..392 y470..502). Red prefix renders x93..151
   y483..497 (orig x94..131 — wider because the certified asset's "Loss =" is
   proportionally wider than the orig's; asset-internal layout, accepted).

4. **Where-block structure (where_block #1/#2/#3/#5 — MAJOR).**
   Orig: staircase line origins 506/572.5/564, tops 284/309/336; bold
   matrix/vector/Given/Required; X/W blue 1F1FC8 in line 1; Predicted red at
   x672..760 y256..278. att7 build was flush-left, plain-weight, inline
   Predicted, literal braced subscripts. FIX: lines 197-231 rewritten per the
   window-3 spec (staircase, per-run bold/italic/colors, subscript:true idiom,
   underline line-shapes Y black (508,278)-(526,278) / W red (566,278)-(584,278),
   Predicted own textbox (672.5,256,88,22), arrows x770, tags x799).
   render_8 verified: L2 origin x507, L3 x574, L4 x565; arrows x775..784; tags
   x799..833/853; L1 blue x533..565; underline1 black x507..525 y277..283;
   underline2 red x566..583 y277..278; Predicted red x673..736 y257..266.

5. **Remember header underline (remember #3 — MINOR).**
   Orig: solid bar y118 x795..864 under the header (clean gap y117). Build had
   none. FIX: underline:true on the run; renders as a solid red bar
   (render_8 y112..113 x787..843, n=118 full-width).

## REFUTED -> no fix

6. **n-vs-N subscript case (let_boxes #2/#7).** Orig subscript glyphs are
   lowercase-size at 8-9px; prior-window adjudication (adjudication_attempt_3.md)
   settled keep-lowercase. Not re-litigated.

7. **Lead-in underlines (let_boxes #3/#8 "missing Y/Yh underline in Let lead-in").**
   Orig lead-in band y144..158 x86..149 has no isolated bar under Y (the crop
   judge's own where_block certificate confirms the only orig underlines are the
   where-block Y/W bars, x506..519/x562..579 y274 — both present in build).

8. **X underline in "Yh = XW" (let_boxes #8).** The dedicated where_block judge
   ("What matches") confirms underlines under Yh and W present in BOTH images and
   does not list X; orig X at x541..556 has no bar under it.

9. **Remember red border (full-slide #5, remember #6).** 0 red px on the
   perimeter; perimeter dark px = 8/300 top, 2/130 left, 9/182 right (no border
   at all — the zoomed judge's "thin dark border" is JPEG edge shadow).

10. **Remember fill (remember #2).** Orig median (220,233,244) vs build DBE9FC
    (219,233,252) — within JPEG variance, no change.

11. **Font family MINORs (let_boxes #4/#10, where_block #6).** Deck-wide Arial
    acceptance stands (window-3 ruling).

## PARTIAL -> recorded, no fix this attempt

12. **Norm subscript-2 (remember #1 — MAJOR conf 0.7).** Orig 2 = x821..828
    y141..149 (8x9px, top 73% down the a, descends 5px below the a baseline).
    Render 2 = x823.7..828.5 y136.3..145 (5x9px, top 30% down the a, 2px below
    baseline). It IS a true small subscript (9px vs a 10-11px) — the judge's
    "nearly full-height" overstates; the real delta is ~5px of vertical depth,
    which mathtext cannot tune per-glyph in a single string. Content correct;
    remember region verdict was PASS. Recorded; re-render not attempted.

13. **Vector-asset scale (own finding, no judge claim).** Asset ink aspect
    951:356 = 2.67 vs orig equation ink 122:87 = 1.40 — no uniform scale can
    match both (render vector ~50px tall vs orig ~88px; entry pitch 12.5 vs 23).
    Both att7 judges passed this geometry twice (full-slide + let-boxes crop);
    fixing it means a custom multi-part re-render, out of att8 scope. Recorded
    for the worker report; att8 judges see fresh crops and may re-raise it.
