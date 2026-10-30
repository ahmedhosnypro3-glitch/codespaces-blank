# Slide 015 — delta vs MOST-RELATED CERTIFIED slide (016)

Pre-phase pack S20f. Anchor choice: **slide 016** — certified 2026-10-25
(attempt-8 legA PASS + crop certificates; `gen_status=passed`,
`visual_check=PASS`; evidence `qa/slide016/adjudicate_attempt_8.md`). Same
founder-curated batch (014–016) and the same derivation storyline: 015 minimizes
the ridge objective that 014 defines, and 016 names the L1/L2 regularizers.
No closer certified slide exists — 013/017/018 are certified TABLE slides,
005 (the sibling whose equation recipe 015's build cites) is still `building`.
For equation craft specifically, the certified precedent is **slide 009**
(`passed`/`PASS`, OMML-wrapped in S13) — same mathtext→600dpi-PNG pipeline.

Basis: `recreated_pptx/build/slide_015.js` (current; render_4.png
md5 `0019627f1ec094510c369801269762d3` proven byte-identical to a fresh LO
render of the deliverable) vs `recreated_pptx/build/slide_016.js` (certified,
render_8). Frame px (960×540, 1px=1pt). ADD = 015 needs it, 016 lacks it;
DELETE = 016-only; DIFFER = both, but different.

## Delta table — element by element

| # | Element | 015 (current build, render_4) | 016 (certified, render_8) | Delta |
|---|---|---|---|---|
| 1 | House chrome | `drawHouseChrome(pptx, slide, {numeral: 15})` — panel E9E9E7 x54..903 y45..540; C00000 strokes L x58.5 / R x901 / bottom y538.5, no top stroke; badge d35 @ (876,73) FDFD96 ring 6A5ACD numeral 333333 18pt | identical primitive, numeral "16" | SAME (value-only DIFFER: 15 vs 16) |
| 2 | Title | box x129 y65 w700 h22, LEFT-aligned, 18pt **DejaVu Sans** Bold (verified 698px ink vs 696px predicted at 18pt), 5 alternating runs: "Minimization of " `C00000` / "Objective " `00008B` / "function to obtain " `C00000` / "BEST " `00008B` / "model parameters" `C00000`; ink y68..84 | single run 27pt bold `8B0000` "L₁ and L₂ Regularization", CENTERED box x0.479in y0.612in w12.0 h0.75, Arial | DIFFER: alignment (left x129 vs centered), size (18pt vs 27pt), font family (DejaVu Sans vs Arial — width-verified choice), coloring (alternating red/blue vs solid dark red). Never copy 016's title pattern |
| 3 | Inner content frame | TWO cream rects, not one frame: A x72..892 y104..266 (w820 h162), B x72..892 y344..521 (w820 h177); fill `FBFDE5`, border `C6CBC7` 1pt | ONE white frame x83.5..833.5 y92.5..532.5, fill FFFFFF, border `2B237A` 1.5pt | DIFFER (structural): 015 = two pale-cream content rects with hairline gray borders; 016 = one white blue-bordered frame. Rect count, fill, border hue and thickness all differ |
| 4 | Derivation equations | 7 mathtext PNGs at exact px/600 placements: eq1_l1 x97 y104 (612×50pt, fontsize 17), eq1_l2 x97 y163 (578×51pt, 18), eq1_l3 x97 y216 (503×51pt, 18), redbox_eq x81 y282 (97×44pt, 26), peach_eq x791 y298 (98×28pt, 19), deriv_l1 x79 y350 (572×54pt, 22), deriv_l2 x79 y415 (408×52pt, 21), normal x229 y467 (266×53pt, 30), solution x553 y472 (251×45pt, 25) — dark-blue `00008B` ink, stacked ½ fractions, underlined W where the original underlines | none — equations appear only as unicode subscripts (₁/₂) inside text runs | ADD (015-only). Width-matching solver (build_eq_015.py): redbox_eq 97pt (fixed from 128pt in attempt 3), peach 98, deriv 572/408, normal 266, solution 251. Known geometric residuals, recorded not fixed: eq1 lines w-ratio 0.87–0.90, solution w-ratio 0.76 / census 1.61 — a 332pt-wide 2D form is ~57pt tall and cannot fit the 40pt box |
| 5 | Pink callout box | rect x73..710 y275..334 (w637 h59), fill `F7D0D3`, border `C00000` 1.5pt; contains redbox_eq PNG + sentence textbox x208 y292 w800 h21 18pt DejaVu Sans: "Get Best W that minimizes the Objective Function " black / "J(" `00008B` / "W" `00008B` underlined / ")" blue — ONLY the trailing J(W) is blue, its W is the underlined one; "Best W" NOT underlined | none (016's analog is a plain colored text run inside a per-line box) | ADD (015-only): a filled, red-bordered callout with mixed image+text content |
| 6 | Remember sidebar | rect x786..895 y275..332 (w109 h57), fill `F7DCBE`, NO border; "Remember" bold 11pt `C00000` at x790 y274 (measured 65px vs 67px predicted); peach_eq PNG x791 y298 | none | ADD (015-only): borderless peach note card |
| 7 | Normal equation line | standalone mathtext PNG x229..495 y467..520, NO box behind it | none | ADD (015-only) |
| 8 | Solution box | rect x547..885 y472..516 (w338 h44), fill `CFFFE3`, border `499243` 1pt; solution PNG x553 y472 with `\underline{W}` in the mathtext | none | ADD (015-only) |
| 9 | Arrow after normal equation | NONE — correctly absent. Gap x501..547 over y466..521 is ZERO-ink in the original (banked `adjudicate_arrow.txt`; re-confirmed in `adjudicate_attempt_4.md` MAJOR-2 refutation). The analysis JSON's arrow is a model hallucination; adding one would invent an element | none (016 also has no arrow) | SAME (both arrow-free) — but for 015 this is an ADJUDICATED point: never "fix" the missing arrow back in |
| 10 | Underline mechanism | run underline in the sentence textbox (J(W)'s W) + `\underline{}` inside mathtext PNGs (J(W), λW, solution W); NO standalone underline shapes | 4 standalone 1px rect shapes (red x110..300 y296.5; dark x109..163 y525, x445..641 y500, x709..807 y500) | DELETE (016-only mechanism): 015's original carries no freestanding underline strokes; the "missing Y underlines" MAJOR was REFUTED — the horizontal runs the judge saw are the base bars of the stacked handwritten ½ (4 runs L1 x173/345/474/696 y148..150; 2+2 in L2/L3) |
| 11 | Yellow highlight | none | `FFFF00` rect x287..456 y176..197 | DELETE (016-only) |
| 12 | Body text container model | equations + 2 textboxes inside 2 cream rects + 2 standalone boxes; 3 free textboxes total (title, sentence, Remember) | 12 free one-line textboxes at measured mid-y (y112..516), 17–18pt Arial, valign middle | DIFFER (structural) |
| 13 | Font | DejaVu Sans (title + textboxes; width-verified), mathtext serif math in PNGs | Arial | DIFFER — keep DejaVu Sans; the 18pt/698px measurement is the evidence |
| 14 | Emphasis colors | `C00000` title-red family + box border, `00008B` all equation ink + blue title runs + J(W) run, `F7D0D3`/`C00000` pink box, `F7DCBE` borderless peach, `CFFFE3`/`499243` green box, `FBFDE5`/`C6CBC7` cream rects | `C00000` runs, `0000FF` L1/L2 runs, `8B0000` title, `2B237A` frame, `FFFF00` highlight | DIFFER (per-slide assignments; overlap is only the shared deck red C00000) |

## Re-judge watch list (owner-sanctioned re-judge context)

015 is parked on judge MISPERCEPTION, not on build defects: attempt-4 legA on
current bytes returned 3 consecutive incoherent FAILs; every claim was
PIL-refuted (`adjudicate_attempt_4.md`; garbage transcripts banked). The re-judge
will see the SAME render (render_4, currency proven). Points a fresh judge will
likely re-raise, with the banked refutations to check them against:

1. "Green term on an extra line" → the stacked ½ is full-height in BOTH images;
   green ink sits INSIDE each line's dark band (L1 131..153 in 105..153, etc.).
2. "Missing ⇒ arrow" → the gap is zero-ink in the original; nothing to add.
3. "Missing Y underlines" → the runs are stacked-½ base bars; \underline{W}
   already matches the only real underlines.
4. "Duplicated blue J(W)" → ink census: exactly ONE J(W) cluster per line.
5. "Boundary collisions" → containment_015.py: 0 spills on the render.
6. Ground clause (e): mathtext 2D fractions vs the original's handwritten
   fractions = mandated format upgrade, never a discrepancy.
