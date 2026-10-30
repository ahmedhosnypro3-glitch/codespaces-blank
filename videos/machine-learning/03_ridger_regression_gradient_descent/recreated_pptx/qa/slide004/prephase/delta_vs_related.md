# delta_vs_related — slide 004 (S20a prephase, pool run 299640)

**Target:** `recreated_pptx/slide_004_recreated.pptx` — build `recreated_pptx/build/slide_004.js`
(rebuild attempt 2, gen_status=building; cert lane S1 holds the scope, no attempt-7 verdicts
banked yet; four earlier adjudications hold: Remember FF0000, X_{N×(d+1)} parenthesization,
pale-yellow fills, Remember = single pale-blue box with no white header).

**Related certified build (pattern source):** `recreated_pptx/build/slide_007.js` (CERTIFIED)
— bordered-box law, multi-run colored text, underline-via-run-splitting, per-line addText.
Also `shared_patterns/house_chrome.js` (numeral 4) and the 600dpi equation-PNG assets
`build/assets/eq_004_*.png` (+ sidecars) already wired into the build.

**Sources of truth for the ORIGINAL side:** PIL passes on `unique_slides/slide_004.jpg`
re-verified 2026-10-25; verbatim confirmation rides on desc legs
(`desc_{full,label_boxes,remember,where_block,bottom_full}.txt`) — pending items marked
`[?] desc_<leg>`.

## Element table — ORIGINAL vs current build

| # | Element | ORIGINAL (frame px) | Current build (attempt 2) | Delta |
|---|---------|---------------------|---------------------------|-------|
| 1 | House chrome | deck-03 chrome, numeral 4 | house_chrome.js, numeral 4 | KEEP |
| 2 | Title | ink y70..91, x~280..660; "Concept of " + " Function" red, "LOSS" blue | 32pt bold runs @x240 y68 w440 centered | KEEP — desc_full confirms run split `[?]` |
| 3 | Box1 (Original Labels) | red border x80/x395 cols, y100/y221 rows (re-verified), white fill → x80..395 y100..221 | rect(80,99,315,123) RED w1 | KEEP |
| 4 | Box1 content | "Let Y =" x87..148 y145..157 black + column vector x165..209 y115..203 + "(n×1)"-style sub; "Original Labels" RED bold x246..371 y136..153; "from Training Samples" black x215..388 y159..177 | one 600dpi PNG eq_004_Yvec ("Let Y = (y1..yn)_{n×1}" stacked 2D) @x87 y131; two text boxes | KEEP — desc_label_boxes confirms verbatim + the vector's subscript glyph (letter x vs ×) `[?]` |
| 5 | Box2 (Predicted) | red border x427/x745, y100..221 (re-verified), white fill | rect(427,99,318,123) | KEEP |
| 6 | Box2 content | "Let Yh=" x432..494 y145..163 + vector x511..547 y114..208; "Predicted Labels" BLUE bold x587..722 y137..150; "from Model Yh=XW" black x565..735 y163..183 with W underlined (bar x720..734 y184) | eq_004_Yhatvec PNG @x432 y130; caption + W-underline runs | KEEP — desc_label_boxes confirms `[?]` |
| 7 | Remember box | x784..880 y100..152, fill (219,233,246), NO border; "Remember" red bold; "‖a‖₂ = aᵀa" equation | rect(784,100,97,53) DBE9FC no line; 11pt red bold; eq_004_norm PNG | KEEP — the FF0000-vs-darkred adjudication stands; desc_remember confirms equation + absence of a white header row `[?]` |
| 8 | Objective box | blue border x78..302 y242..301 (rows y244/y300 re-verified), pale-yellow fill (245,248,216); "Objective is Ŷ=Y", NO underline under Ŷ=Y (PIL: no isolated bar) | rect PALE + NAVY w1; 14pt runs, no underline | KEEP |
| 9 | Error box | blue border x78..486 y306..365 (rows y308/y364 re-verified), pale-yellow; "If Ŷ≠Y ⇒ There is an Error (Loss)", "Error (Loss)" red bold | rect PALE; runs 14pt | KEEP — desc_bottom_full confirms wording `[?]` |
| 10 | Predicted/Where box | red border, x494..884 y232..371, white fill | rect(494,232,390,139) | KEEP |
| 11 | "Ŷ = XW  Predicted" line | first line; Ŷ underlined (bar x506..519 y274), X NOT underlined, W underlined (bar x562..579 y274); "Predicted" red bold after | 16pt italic runs with underline split exactly there; "Predicted" 14pt red bold | KEEP |
| 12 | Where: 3 lines | bands y285..303 / y314..332 / y345..363 (pitch 30): "Where: X_{N×(d+1)} is a matrix ⇒ Given" / "Y_{N×1} is labels vector ⇒ Given" / "W is Model Parameter ⇒ Required"; X_{N×(d+1)} parenthesized (adjudicated) | 3 separate addText @y285 pitch 30, 13pt; subscripts written as literal "X_{N×(d+1)}" run text | DIFFER-[?]: desc_where_block confirms (a) the subscript is true subscript positioning in the original vs the build's literal-brace text, (b) letter x vs × inside the dimension. If true subscript, re-split runs with subscript:true |
| 13 | Define box | red border y390/y446 rows (re-verified), x78..655 y388..447; salmon fill (238,215,195); "Define Loss function as squared distance between Ŷ and Y", "Loss" red bold, "squared distance" blue bold | rect(75,387,585,61) FAEBD7 + RED w1; runs 15pt | KEEP fill per founder-spec adjudication (FAEBD7 vs measured (238,215,195) is ~12/channel lighter — recorded, do not change without a founder call); desc_bottom_full confirms text `[?]` |
| 14 | Formula box | blue border x78..486 y464..521 (rows y465/y521 re-verified), pale-yellow; "Loss = ‖Y−Ŷ‖₂ = (Y−Ŷ)ᵀ(Y−Ŷ)" | rect PALE + NAVY; eq_004_formula PNG @x172 y482 | KEEP — desc_bottom_full confirms the norm-subscript form `[?]` |

## Open questions riding on the desc legs

1. `desc_label_boxes` — #4/#6 verbatim captions, vector subscript glyph, "Let Y ="/"Let Yh="
   exact strings, n×1 dimension glyph.
2. `desc_where_block` — #11 underline set, #12 subscript positioning + dimension glyph.
3. `desc_remember` — #7 equation form, no-header confirmation.
4. `desc_bottom_full` — #9/#13/#14 wording and emphasis runs.
5. `desc_full` — global cross-check incl. title run split.
