# delta_vs_related.md — slide 042 "Iteration 1" vs certified slide 041

Worker S20d (prephase) · 2026-10-25 · READ-ONLY toward the cert lane's products.
Baseline: **slide 041, certified 2026-10-25** (`build/slide_041.js`, `visual_check=PASS`
attempt 5; report `qa/slide041/worker_report.md`). 042 continues 041's structure: same
top-band family (cream box + TL vector table + Initial-W + check-classes + legend),
then REPLACES 041's plot with the perceptron computation stack.

Legend for evidence tags: **[041-cert]** = certified 041 build; **[042-build]** = current
`build/slide_042.js` (attempt 18); **[042-bank]** = banked 042 lane PIL measurements
(`qa/slide042/worker_report.md`, `adjudication_16/17.md`); **[S20d-PIL]** = this prephase's
PIL pass on `unique_slides/slide_042.jpg`; **[S20d-vision]** = S20d ground-truth vision read
(`prephase/orig_judges/slide_042_*_desc.txt`).

## House chrome

Identical (deck-03 frozen template, `shared_patterns/house_chrome.js`); only the
numeral differs (42 vs 41). Badge d≈35 centered (876,73), fill FDFD96, ring 6A5ACD,
bold Arial 18pt `333333`. NOT a delta. House chrome check already PASS on 042's
render_17/render_18.

## Element-by-element delta

| # | Element | 041 (certified baseline) | 042 | Action for 042 build |
|---|---|---|---|---|
| 1 | Cream top box | rect x70..718 y54..130, fill FEFFE8, border 0000FF 1pt [041-cert] | x68..720 y54..130 same fill/border [042-build, banked] | DIFFER (2px wider) — keep 042's measured x68..720; no fix |
| 2 | TL x1..x6 headers | txtsub runs, BLACK bold 10pt, cx 96.5/118/140/163/185.5/208, y61 [041-cert] | same token set, BLACK (attempt-17 channel-order fix), y62 [042-build] | KEEP — already ported (txtsub, 17 tokens, attempt 18) |
| 3 | TL column vectors | values (1,1)(2,1)(1,2)(5,4)(6,5)(6,6), rows y78/y93 11pt bold, **bowed P3 Bezier paren PNGs** (`qa/slide041/assets/parens041/`, sidecar-placed) [041-cert] | same values via `vecCol` 11pt at y78/y93, cx 95..206, **NO paren glyphs drawn at all** [042-build] | DIFFER (mechanism): 042 draws no TL parens. VERIFY on frame: [S20d-vision topband]. If the frame shows parens, reuse 041's P3 `paren_table` PNGs; if it shows none, keep |
| 4 | TL class row | C1C1C1C2C2C2 txtsub red/blue y110 [041-cert] | same y109 + **red ⇒ at x239..253** [042-build, banked] | **REVISED by S20d-PIL**: the frame's red ink at x239..253 y110..123 is **C1-glyph-shaped and pixel-identical to 041's legend C1** (red-shape map, 4-slide chroma identity) — it is NOT an ⇒. **DELETE the build's ⇒**; that zone belongs to the legend (row 5) |
| 5 | Legend sentence | y107..123 x237..508: **C1 RED** x237, " positive," black ..x301, C2 BLUE x311, " negative," ..x377, Zero GREEN x392..423, " is unaccepted" x428..508; 11.5pt `wrap:false` per-fragment boxes [041-cert] | y107..123 **x257..508**: C1 **BLACK** x257, C2 BLUE x310, Zero GREEN x394; 13pt per-fragment boxes [042-build; banked "no red in the legend"] | **RESOLVED by S20d-PIL**: 4-slide legend-band chroma identity (red 42/43/44/42, blue 33/35/34/33, green 163/166/165/165 on 041/042/043/044) + the C1 shape map ⇒ **all four frames carry the SAME legend: red C1 at x≈239, blue C2, green Zero**. The build's black-C1-at-x257 (that x-zone holds the black " positive," ink) and the ⇒ are misreads. **Port 041's legend pattern verbatim**; [S20d-vision topband] = final glyph-level confirmation |
| 6 | Initial W block | "Initial W =" 12.5pt x263 y72; **wvec P3 paren PNGs** x330.5/x352.5 bandTop 59; **THREE digit stacks** 4/-2/-2 y59/75/93 [041-cert] | "Initial W =" 14pt x262 y71; **line-drawn parens + hooks** x330/x349..356 y63..102; **TWO digit stacks** 4/-2 y66/y80 13pt; "Step η = 2" red italic 15pt x364 y63 [042-build] | DIFFER: digit-stack count (2 vs 3) and paren mechanism. VERIFY [S20d-vision topband]. 044's frame shows THREE stacks (4/-2/-2) per its banked measurements — 042's frame may genuinely have two (iteration-1 W starts as (4;-2)) |
| 7 | Check classes block | "Check classes of" 11pt x494 y75; Z1 Z1 Z1 txtsub black cx 605.5/628/650; **ztab P3 paren PNGs** vals (0,0)(7,6)(3,2) y82/y94 [041-cert] | same texts/values; Z1×3 BLACK (fixed); plain `vecCol` digits y82, **no paren glyphs** [042-build] | DIFFER (mechanism): 042 omits Z-column parens. VERIFY [S20d-vision topband] |
| 8 | Plot (red border, gridlines, ticks, 9 markers) | present, certified [041-cert] | **ABSENT** — plot region replaced by the computation stack | DELETE — correct, keep |
| 9 | LM caption | — (041 has none) | "Upgraded Vectors (From Top)" BLUE bold 11pt x79 y150 [042-build, banked x81..234 y148..159] | ADD — keep |
| 10 | LM table | — | **FOUR digit bands** y164/183/195/212: [1,1,1,2,1,1]/[1,1,1,1,1,1]/[1,1,1,1,1,1]/[1,1,2,5,6,6] (attempt-18 cell swap fix), cx 99..211, thin 0.75pt paren strokes+hooks y166..222 pairs (93,107)(115,128)(137,150)(173,182)(205,218), class row C1/C2 txtsub y230 [042-build, banked] | ADD — keep. Note: **no x-header row** (lane refuted the judge's header claim with ink counts: gap y160..166 = 0 ink). Note 043/044's LM tables DO carry headers — the frames differ; don't normalize |
| 11 | Iteration badge | — | solid red rect x84..214 y277..305 + white bold 15pt "Iteration 1" [042-build, banked] | ADD — keep |
| 12 | Right stack boxes | — (041: plot) | 5 white boxes x273..853, border BEBEBE 1pt, tops y217/273/340/406/472, separated by panel-gray gaps [042-build, banked] | ADD — keep |
| 13 | Stack band structure per box | — | build: lineA = d(x_sub) label x283..317 + 2-row matrix digits x489.. + "= value" x610 + ⇒ x662 + action x688..836; lineB = W-equation PNG at x384 [042-build] | **DIFFER (STRUCTURAL — transcript arbitrated)**: the frame's each box is ONE dot-product line: `d(xᵢ) = |row-vec| (green W col-vec) = value` at x282..458, then `⇒` + action x480..637, then `W = (vec)` x609..790 — see row 15. The build's 2-row garbled sidecar form is not what the frame shows |
| 14 | Stack W-update row (box 3 only) | — | build: ONE W-equation PNG per box (eq_042_w1..w5) on every box's lineB [042-build] | **DIFFER**: the frame carries the long update equation `W=(6,0,0) − 2*(1,5,4) = (4,−10,−8)` ONLY in box 3 (x609..791, blue `− 2 *`, green result vec, red ⇐ x771..791); boxes 1/2/4/5 carry only the short `W = (same vec)` right-hand group. One-PNG-per-box is wrong |
| 15 | Stack dx equations content | — | `eq_042_d1..d5.png` rendered 2-row garbled latex, e.g. d1 = `\left(1\;1\;1\;4,\;-2\;0\right) = 0`; subscripts d(x1)..d(x5) [042-bank sidecar] | **DIFFER — transcript ground truth**: five boxes read `d(x₂) = \|1 2 1\| (6,0,0) = 6`, `d(x₃) = \|1 1 2\| (6,0,0) = 6`, `d(x₄) = \|1 5 4\| (6,0,0) = 6 ⇒ Update`, `d(x₅) = \|1 6 5\| (4,−10,−8) = −96`, `d(x₆) = \|1 6 6\| (4,−10,−8) = −104` [S20d-vision stack]. Arithmetic self-consistent (dot products check: 1·6=6; 4−60−40=−96; 4−60−48=−104). Row-5 subscript reads **`6`** by glyph shape (narrow stem + closed bottom bowl; PIL pool-1 render vs row-3's known `4` — the transcript's `5 vs 6` [?] resolves to 6). Boxes are x₂..x₆; **x₁'s update row is ON THIS SLIDE** as frame box 1 (row 16) — 041's calc area is the plot (x312..825 y173..482), no d-rows there. Rebuild needs NEW sidecars in this form |
| 16 | **Frame box 1 — the `d(x₁)` row** (S20d PIL discovery, post-transcript) | — | **ABSENT from the build**: its five bands sit at frame boxes 2–6 (banked tops y217/273/340/406/472); the frame's box 1 (top border y139, bottom border y198..201) sits ABOVE the stack crop (y206+) and was in no transcript | **ADD the band**: `d(x₁) = \|1 1 1\| (4,−2,−2) = 0  ⇒ Update Weight, W = (4,−2,−2) + 2*(1,1,1) = (6,0,0)`. Evidence: value glyph renders as a closed oval `0` (PIL, full-frame 1×); chroma red 180 / green 694 / blue 0 (red `\|digits\|` + green vectors + red `+ 2*` + red `⇐`, family pattern); arithmetic 4−2−2=0 and (4,−2,−2)+2(1,1,1)=(6,0,0) = box 2's W ✓; Zero is unaccepted (legend) ⇒ Update. Content band ≈ y150..195; insert ABOVE the build's band 1 — no reflow of boxes 2–6 |
| 17 | Frame box-7 sliver (y531..538) | — | not drawn | The table's NEXT row (iteration-2 `d(x₁)` = 043's frame box 1) pokes above the slide bottom: frame shows top border rows y531/534 + white fill + the house bottom stroke (the strip's red/dark px ARE the stroke, not content). Optional 7px fidelity strip; the row's content is below the frame edge and unreadable |

## S20d original-frame findings — now ARBITRATED by the stack transcript

- **F1 — third ink row in EVERY stack box** [S20d-PIL → ARBITRATED]: real text, not
  ghosting. It is the upper part of the **3-row green W column vectors** (e.g. box1
  green `6/0/0` rows at slide y219..247, x387..397) plus the red/blue `|digits|`
  bands (x332..388). The build draws nothing there → **missing elements**, confirmed
  by [S20d-vision stack].
- **F2 — no blue step numbers at box left edges** [S20d-PIL → CONFIRMED]: 0 blue px
  x276..286. The crop-18 judge's "blue 1) 2) 4) 5) 6)" is a misread of the **red/blue
  `|digits|`** at x332..388 (red boxes 1–2, blue boxes 3–5, bars included).
- **F3 — box3 far-right red+green ink** [S20d-PIL → ARBITRATED]: green = result
  vector `(4,−10,−8)` incl. green parens x717..751; red = `⇐` double-arrow x771..791
  [S20d-vision stack]. Real frame content, absent from the build.
- **F4 — box1 tall element x380..393 y229..247** [S20d-PIL → ARBITRATED]: the **green
  tall parens** framing the 3-row W vector (paren span img y35..155 → slide
  y217..257). Real; the build's green ⇐ at x380 is not what the frame shows there.

## Dispute map — crop-18 stack judge vs banked measurements (RESOLVED by [S20d-vision stack])

| crop-18 claim | S20d evidence | verdict |
|---|---|---|
| BLOCKER: 3-element column vectors (6,0,0)/(4,−10,−8), tall green parens | transcript: green `(6,0,0)` boxes 1–3, `(4,−10,−8)` boxes 3(result)/4/5, tall green parens span ~40–50 slide px | **JUDGE RIGHT** — build wrong |
| BLOCKER: results box1 = 6, last box = −104 | transcript: `= 6` boxes 1–3, `= −96` box 4, `= −104` box 5 | **JUDGE RIGHT** |
| BLOCKER: box1 action "Keep same Weight" black | transcript: boxes 1/2/4/5 `⇒ Keep same Weight` black; box 3 `⇒ Update Weight` with **red ⇒** | **JUDGE RIGHT** |
| BLOCKER: blue step numbers 1)2)4)5)6) at box left edges | F2: none at x≤286; the colored ink is red/blue `\|digits\|` (d-vector rows), not step numbers | **JUDGE WRONG on form, RIGHT that colored ink exists** (it is the `\|1 2 1\|`-style rows: red boxes 1–2, blue boxes 3–5) |
| MAJOR: green vector digits / serif underlined W / red ⇐ box4 right | transcript: green vectors all boxes; `W =` carries an **underline bar** (W-bar notation); red ⇐ only in box 3 far-right (x771..791) + red ⇒ box 3 | **MIXED** — underlined W and red arrows real; "box4 red ⇐" is box 3 |
| MAJOR: subscripts/sequence | transcript reads d(x₂), d(x₃), d(x₄), d(x₅), d(x₅?/x₆?) — row-5 subscript flagged [?] | **boxes are x₂..x₆**, sequence shifted vs build's d(x1)..d(x5) |

## Stack transcript digest (slide-space px) — [S20d-vision stack], `slide_042_stack_desc.txt`

- Box bounds (vision estimate): (275.7,207.7)-(854,263.3) / (275.7,271.3)-(854,328.7) /
  (275.7,334.7)-(854,393.7) / (275.7,402.7)-(854,460.0) / (275.7,469.3)-(854,527.7);
  border #AEB8C2 thin; box fill #FFFFFF; gaps #E9E9E9. Lane's banked border tops
  y217/273/340/406/472 are the precise PIL values — use those for the rebuild.
- Row text bands (y): 232–243, 295–306, 359–370, 425–437, 491–503.
- LHS cluster per box: `d(xᵢ) =` x282..327 (italic d/x) · `|` x327..331 · digits
  x332..388 (RED boxes 1–2 #C00000, BLUE boxes 3–5 #0000CC) · `|` x377..390 · green
  `(` x382..392 · green 3-row vector x387..397 (#00A050, pitch 15–16px) · green `)`
  x397..412 · `= value` x399..458 (black).
- MID cluster: `⇒` x480..533 (RED only box 3 #CC0000, else black) · action text
  x500..642 16pt-ish black ("Keep same Weight" ×4, "Update Weight" box 3).
- RIGHT cluster: `W =` with underline bar x609..746 · black `( vec )` x634..783; box 3
  additionally: blue `- 2 *` x655..682, black `(1,5,4)` x686..702, `=` x708..715, GREEN
  result `(4,−10,−8)` x717..751, RED `⇐` x771..791.
- Far-right red vertical x903.3..908 y206..538 = house chrome right stroke (in-crop
  view of the C00000 deck frame) — NOT a new element.
- Mouse cursor between boxes 2/3 at (570.7,322.7)-(584,342.7) = capture artifact, omit.
- W-bar: the `W` of `W =` carries an underline bar (W-bar notation) — check the
  eq_042_w* PNGs render it; plain `W` is a delta.

## Cross-slide correspondence (S20d, for the 043/044 packs)

043's six band rows (dxC y166/235/295/361/427/492) = 042's five box rows
(y232/295/359/425/491) plus ONE extra first band (y166). With 042 ending at
W=(4,−10,−8), 043 band 1 should read `d(x₁) = |1 1 1| (4,−10,−8) = −14` — and the 043
analysis verbatim is exactly `d(x1) = [1 1 1; -10; -8] = -14` (the garbled `[1 1 1;
-10; -8]` IS `|1 1 1| (4,−10,−8)` flattened). The 042 transcript structure therefore
predicts the 043/044 band content: dot-product form `d(xᵢ) = |row| (W) = value`, with
update rows carrying `W = (old) ± 2*(x) = (new)`. The 043/044 stack reads (dispatched
by S20d) confirm/adjust per band; their garbled 2-row sidecars need the same rebuild
042 needs. **(Confirmed 2026-10-25: both descendant transcripts landed — 044's stack
read matches this structure band-for-band, with the family W-line colors, red ⇐ on its
three update rows, and one frame-typo contrast: 042's last box −104 is arithmetic-true,
044's last box prints −112 where arithmetic gives −10 — per-frame verbatim wins on
both. Full arbitration in `../slide044/prephase/delta_vs_related.md`.)**
