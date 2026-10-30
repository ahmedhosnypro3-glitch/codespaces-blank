# delta_vs_related — slide 003 (S20a prephase, pool run 299640)

**Target:** `recreated_pptx/slide_003_recreated.pptx` — build `recreated_pptx/build/slide_003.js`
(current state: attempt 8 rebuild, gen_status=building, cert lane S1 judging; attempt-21 verdict FAIL).

**Related certified builds (pattern sources for this slide):**
- `recreated_pptx/build/slide_007.js` (CERTIFIED) — blue-bordered box law, multi-run colored
  text boxes, per-line addText, charSpacing fit. Reuse its run/box idioms.
- `shared_patterns/house_chrome.js` (CERTIFIED module + `house_chrome_check.py`) — slide 003
  IS the frame this deck's chrome was measured from; the build already consumes the module.
- `recreated_pptx/qa/slide003/parens/*.png` — arc images cut from the original (y-vector,
  matrix, w-vector, mid-column parens), already wired into the build.

**Sources of truth for the ORIGINAL side:** PIL pixel passes on
`unique_slides/slide_003.jpg` (960x540, 1px=1pt) re-verified 2026-10-25 (this file, table
below); verbatim-text confirmation rides on the desc legs
(`orig_judges/desc_{full,topbox,matrix,sideboxes,bottomright}.txt`) — items still pending a
leg are marked `[?] desc_<leg>`.

## Element table — ORIGINAL vs current build

Delta legend: KEEP (build matches original within JPEG tolerance) / DIFFER (fix) /
ADD (missing in build) / DELETE (extra in build) / [?] (pending leg evidence).

| # | Element | ORIGINAL (frame px) | Current build (attempt 8) | Delta |
|---|---------|---------------------|---------------------------|-------|
| 1 | House chrome | panel E9E9E7 x54..903 y45..540; C00000 1pt strokes L x58.5 / R x901 / B y538.5, NO top stroke; badge d35 @(876,73) FDFD96 + ring 6A5ACD, numeral 3 | `house_chrome.js` module, numeral 3 | KEEP (003 is the chrome reference frame) |
| 2 | Title | ink x82..832 y68..90, ONE line; "Matrix" + "(N-" blue, remainder red | 4 runs, 23pt bold, box x70 y62 w800 (one-line guarantee) | KEEP — confirm wording/colors vs `desc_full` `[?]` |
| 3 | "N Training Samples" | red bold, ink x81..272 y177..199 | 18pt bold FF0000 @x80 y173 | KEEP |
| 4 | Top matrix box | blue border x271..596 y107..301 (re-verified), white fill | rect x271 y107 w325 h194, line 0000FF w1 | KEEP |
| 5 | Top box column bands | yellow x294..336, cyan x370..417, pink x513..557, y141..296; fills measured (244,251,171)/(165,245,236)/(238,154,240) | cx/w 315/43, 393.5/48, 535/45; FFFF99/CCFFFF/F0A0F0 | KEEP (fills within JPEG tolerance) |
| 6 | Column headers | X1 X2 … Xn (letter x + digit subscripts), black bold italic, y115..139; "..." header over the gray column | 18pt bold italic runs + "..." | KEEP — desc_topbox settles glyph reading `[?]` |
| 7 | Top box entries + rules | entry stacks x11/x12/…/x1d, x21…, xn1… rows y156..258; right-bar delimiters x331.5/414.5/556.5 y155..259; separator line y297.5 | per-entry 11pt italic boxes + 3 line shapes + separator | KEEP — desc_topbox confirms digits `[?]` |
| 8 | Top box y-labels | red y1 y2 yn at band bottoms y274..292 | 12pt red italic @y274 | KEEP — attempt-21 reported COLORED y-labels on the bottom y-vector; whether the TOP box's y1/y2/yn are red or band-colored is settled by `desc_topbox` `[?]` |
| 9 | Ellipsis column (top box) | gray parens x451..472 y157..251 + 4 dot rows y163/190/214/241 + header | arc_midcol_L/R + 4 gray "..." texts + header | KEEP |
| 10 | Remember box | x649..874 y153..221, fill (229,251,246), blue border; red bold italic "Remember" x656..689 y160..176; eq y=WᵀX=XᵀW x697..877 y184..214, blue underlined W/X, superscript T; 'y' underlined (attempt-21 ✓) | rect E5FEFA + 0000FF w1.5; runs 18pt with underline on y/W/X/W | KEEP |
| 11 | In General box | x659..850 y268..294, border #6C5B3D; "In General: N >>> d", N and d red bold, ">>>" red/brown | 15pt, " >>> " FF0000 bold | KEEP — >>> exact hue vs `desc_sideboxes` `[?]` |
| 12 | Bottom-left box | red border x79/x533 cols, y324/y516 rows (re-verified), white fill → x79..533 y323..517 | rect x79 y323 w454 h194 C00000 w1 | KEEP |
| 13 | y-vector (bottom-left) | parens x107..129 y358..486; entries y1 y2 … yn rows y368/397/427/456; **PIL-settled 2026-10-25: the entries sit on COLORED CHIPS — y1 yellow chip x~110..133 y368..390, y2 cyan chip y397..423, yn pink chip x~110..135 y456..478; dots row has NO chip; w-vector has NO chips (white)** — entry TEXT is dark-on-chip | arc_yvec_L/R + 15pt entries drawn as COLORED TEXT (gold C8963C / teal 46A0A8 / black / magenta CC3FB0), no chips | DIFFER: attempt-21's "y1 yellow, y2 cyan, yn pink" = the CHIPS, not the text. Build action: ADD 3 chip rects (band families FFFF99/CCFFFF/F0A0F0 — sample exact hues from the crop) BEHIND the entries and recolor the entry text dark; chips only on the three entry rows, never on dots/w-vector |
| 14 | "=" between y-vector and matrix | x144..168 y387..417, 24pt black bold | 24pt @x144 y387 | KEEP |
| 15 | Matrix leading ones column | PRESENT: dark ink x208..211 in ALL FOUR row bands (yellow y370..388, cyan y399..421, white y429..450, pink y458..476) — PIL-verified 2026-10-25 | row_defs draw "1" at x209 per row | KEEP — cert attempt-21 BLOCKER "missing leading ones column" is REFUTED against the ORIGINAL (the adjudication of attempt 20 scanned the wrong strip x132..192; the column sits inside the bracket at x~210). If a judged render lacks the column, that is a render/build mismatch, NOT an original-fidelity defect |
| 16 | Matrix x-columns | col2 x236..257 ("x11"), col3 x279..303 ("x12"), dots x324..346 (all rows); white row carries dot groups under ALL THREE x-cols (x237..254, x283..300, x329..346) and no dots column of its own | row_defs cells at x209/245/290/330/365 (10pt italic) | KEEP for cols 1-3; 5th cell DIFFER-[?] below |
| 17 | Matrix 5th column + right paren | ink x359..394 exists but is sparse and row-gapped (no ink x347..358; gaps at y402, y422..430): either a WIDE right paren curve (top hook x359..366, bulge x380..394, bottom hook x366..382) or a 5th "x1d" column with a thin paren | arc_matrix_R placed at x388 w3.8 (thin line); build comment says "right curve x358..368" | DIFFER-[?]: `desc_matrix` settles BOTH (a) whether rows end "… x1d" and (b) the paren curve's true extent. If the original paren is a wide curve, a 3.8px arc at x388 under-represents it (consider a wider arc image cut from the original) |
| 18 | "N × d+1" dim label | purple bold, ink x399..460 y468..486 (y474 x399 re-verified) | 11pt bold 993399 @x399 y468 | KEEP — attempt-21 says dim labels use letter "x" not "×"; `desc_matrix` settles glyph form |
| 19 | Red micro-ink | x143..161, y472..474 (19x3px), red-dominant — **RESOLVED 2026-10-25: JPEG chroma fringing around the purple "N × 1" label (label ink x141..162 y466..475); NOT an element** | not drawn | RESOLVED — build correct as-is; nothing to add. Do not re-open without new evidence |
| 20 | w-vector | parens x458..516 y348..478; entries b y350, w1 y388, w2 y416, … y453, wd y470 | arc_wvec_L/R + 13pt entries: b red bold, w-runs blue | DIFFER-[?]: attempt-21 reported "b/w1 red" (w1 red?) vs build's blue w-entries. `desc_matrix` settles entry colors — **PROBE NOTE (pil_probe_003.txt §3, 2026-10-25): entry-1 ("b") is RED on the frame (84 red px, 0 blue in y348..376) — build's red b is correct; the open question is only w1's color (probe row y386..412 mixed red/blue, inconclusive)** |
| 21 | "d+1 × 1" dim label | purple, under w-vector (build x452..528 y486) | 11pt bold 993399 | KEEP — same letter-x question as #18 |
| 22 | Arrow | thin gray line x532..572, head y402..407 | gray 1.5pt line x543 y408 w34, triangle head | KEEP |
| 23 | Bottom-right box | red border cols x585/x886, rows y323..517 (x585/x886 re-verified) → x585..886 y323..517 | rect x585 y323 w301 h194 C00000 w1 | KEEP (note: stale comment at top of slide_003.js says "x572..752" — code is correct; fix the comment) |
| 24 | "Y = XW" heading | glyphs y362..383; Y underlined (x604..620), X BLUE, W RED | 16pt bold runs, underline on Y/X/W, X blue W red | KEEP — desc_bottomright confirms |
| 25 | "Where:" block | line1 y398..431 (X + subscript BLUE, underlined), line2 y446..470 (Y + subscript RED, underlined, indented to align under X) | two 13pt addText boxes @y398/@y446 | KEEP |

## Open questions riding on the desc legs (fill before certification)

1. `desc_matrix` — #17 matrix 5th column + right-paren extent; #18/#21 dim-label glyph
   (letter x vs ×); #20 w1-entry color. (#13 y-vector chips: PIL-settled 2026-10-25 —
   colored chips with dark text; #19 red micro-ink: RESOLVED = JPEG fringing, not an element.)
2. `desc_topbox` — #6/#7 entry digits and header glyphs; #8 top-box y-label colors.
3. `desc_sideboxes` — #11 ">>>" hue; #10 underline extents.
4. `desc_full` — #2 title wording/run split; global cross-check.
5. `desc_bottomright` — #24/#25 text + underline details.
