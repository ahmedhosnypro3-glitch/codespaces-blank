# Slide 014 — delta vs MOST-RELATED CERTIFIED slide (016)

Pre-phase pack S20f. Anchor choice: **slide 016** — certified 2026-10-25
(attempt-8 legA PASS + 2 crop certificates clean; `gen_status=passed`,
`visual_check=PASS` in slides_progress.db; evidence chain
`qa/slide016/adjudicate_attempt_8.md`). It is the third member of the same
founder-curated batch (014–016) and the same regularization topic block — 014
defines the ridge LOSS, 016 defines L1/L2. No closer certified slide exists
(013/017/018 are certified but are TABLE slides; 005, the equation-recipe
sibling 015's build cites, is still `building`, NOT certified).

Basis: `recreated_pptx/build/slide_014.js` (current, = render_7c) vs
`recreated_pptx/build/slide_016.js` (certified, = render_8). All coordinates in
frame px (960×540, 1 px = 1 pt = 1/72 in). "ADD" = 014 needs it, 016 lacks it;
"DELETE" = 016 has it, 014's original does not (so the 016 pattern must NOT be
carried over); "DIFFER" = both have the element but they differ.

## Delta table — element by element

| # | Element | 014 (current build, render_7c) | 016 (certified, render_8) | Delta |
|---|---|---|---|---|
| 1 | House chrome | `drawHouseChrome(pptx, s, {numeral: 14})` — panel E9E9E7 x54..903 y45..540; red C00000 1pt strokes left x58.5 / right x901 / bottom y538.5, NO top stroke; badge d35 @ (876,73) fill FDFD96 ring 6A5ACD numeral 18pt 333333 | identical primitive, `numeral: "16"` | SAME (value-only DIFFER: badge numeral 14 vs 16 — both correct per file-number law) |
| 2 | Title | 3-run 28pt bold Arial, box x0.6in y0.85in w12.13 h0.55, align center, lineSpacing 33.6: "LOSS " `0000FF` / "Function that " `800020` (maroon) / "MINIMIZES Overfitting" `0000FF`; measured ink y70..92, centered x190..744 | single-run 27pt bold `8B0000` "L₁ and L₂ Regularization", box x0.479in y0.612in w12.0 h0.75, align center valign middle; measured ink x312..621 y61..86 | DIFFER: run structure (3 bicolor runs vs 1 solid dark-red run), 28pt vs 27pt, title box y0.85in vs y0.612in (014's title sits ~17px lower). Both centered full-width — do NOT copy 016's single-run pattern |
| 3 | Inner content frame | NONE — content sits directly on the gray panel | white rect x83.5..833.5 y92.5..532.5 (w750 h440), fill FFFFFF, border `2B237A` 1.5pt | DELETE (016-only): 014's original has no inner frame; carrying 016's frame into a 014 rebuild would invent an element |
| 4 | Vector-definition boxes | 2 rects y99..238 (h139): left x80..433 (w353), right x457..810 (w353); white fill, maroon `8F1220` border 2pt. Left: "Let " + "Y" (underlined) + " =" 18pt; `eq_014_Yvec.png` 1.0483×1.2083in (red C00000 ink, recolored attempt-6); "N"+subscript"×1" 12pt; labels at x+2.6in: "Original Labels" bold 14pt `AD0014` (attempt-7 fix: was 18pt), "from Training Samples" 14pt black, lineSpacing 17. Right: "Let Ŷ =", `eq_014_Yhatvec.png` 1.0483×1.22in (blue ink), "N×1", "Predicted Labels" bold 14pt `0000FF`, "from Model Ŷ = " + "X" bold underlined + " " + "W" bold underlined 14pt (attempt-7 fix: bold underlined X restored) | none — 016 has no boxes, no equations-as-images | ADD (014-only). 016's per-line text-box model cannot express bracketed column vectors; 014 needs the 2-rect + mathtext-PNG composition |
| 5 | Yellow highlight | none | `FFFF00` rect x287..456 y176..197 behind "better generalization" | DELETE (016-only) |
| 6 | Underline marks | text-RUN underlines only: "Y" in "Let Y =", "X"/"W" in "from Model Ŷ = XW", "Ŷ"/"Y" in Define-Loss band (attempt-7 fix #6) | SHAPE-rect underlines: red `C00000` x110..300 y296.5 h1 (beneath "customized weigh factor"); dark `333333` h1 at x109..163 y525, x445..641 y500, x709..807 y500 | DIFFER in mechanism: 014 = run underlines inside text; 016 = standalone 1px rect shapes drawn at measured ink positions. 014's original has no freestanding underline strokes → keep run underlines, do NOT port 016's rect mechanism |
| 7 | Band 1 (Ridge Regularization) | band rect x60.5..898.5 (w838) y243..286 (h43) fill `F9FBDC` + 3px top/bottom rules `1E0060`; text 17pt left inset 0.25in, lineSpacing 20: "Objective is " black / "Ŷ=Y" bold `C00000` / " and " / "||W||" bold `0000FF` / " is minimum This is called " / "Ridge Regularization" bold `008000` | none | ADD (014-only). Note the accepted attempt-7 minor: render's inter-phrase gaps narrower than original's wide gaps |
| 8 | Band 2 (Objective function) | band rect x60.5..898.5 y303..342 (h39), same fill/rules; runs 17pt: "Objective function " / "J(W)" bold `0000FF` / " = " / "Loss" bold `C00000` / "(X,Y,W) + " / "λ" `0000FF` / " " / "R(W)" bold `0000FF` / " (" / "λ" `0000FF` / " is a weighting factor)" — note INLINE (attempt-5 fix merged the note runs; a second addText was removed) | none | ADD (014-only) |
| 9 | Define-Loss band | rect x90..665 y347..392 (h45) fill `F9DEC1` peach + maroon `8F1220` 3px rules; runs 17pt: "Define " / "Loss" bold `B60007` / " function as " / "squared distance" bold `5D44AC` purple / " between " / "Ŷ" bold italic underlined / " and " / "Y" bold italic underlined | none | ADD (014-only) |
| 10 | Term boxes | y399..448 (h49): LEFT x89..471 fill `F9DFC8` border `742C2D` 1.5pt — "Loss Term" bold `1E0060` / " = " / "||Y-Ŷ||" bold `C00000` / sup"2" red / " = (Y-Ŷ)" bold red / sup"T" red / "(Y-Ŷ)" bold red; RIGHT x533..880 fill `F9FEDE` border `1E0060` 1.5pt — "Regularization Term" bold `1E0060` / " R = ||W||" black / sup"2" / " = " / "W" bold `008000` / sup"T" / "W" bold green; superscripts via pptxgenjs `superscript: true` runs | none | ADD (014-only). 016 expresses emphasis with colored phrases only, never with boxed formulas |
| 11 | Final objective band | rect x87..880 y469..528 (h59) fill `ECFFFD` border `1E0060` 1.5pt + navy rules; "Objective function " 17pt black at x+1.1in (w2.4in); `eq_014_final.png` 2D stacked-½ formula at x350..735 y479..521 (w3.985 h0.4233in, black ink) | none | ADD (014-only). Equation is a professional-2D mathtext PNG — ground clause (e) covers format |
| 12 | Body text container model | runs placed INSIDE 6 boxed regions (2 vector boxes + 4 bands + 2 term boxes + final band) | 12 standalone one-line text boxes at measured mid-y: y112,137,187,239,264,289,341,366,417,442,493,516, left edges x95/x110/x146, 17–18pt, valign middle, w10.0–10.2in | DIFFER (structural): 014's content is container-bound; 016's is free lines. A 014 rebuild must keep boxes; a 016 pattern import would strip them |
| 13 | Equations as images | 3 mathtext PNGs (Yvec red, Yhatvec blue, final black), `addImage` at exact px/600 sizes | none (unicode ₁/₂ subscripts inside text runs) | ADD (014-only) — consistent with certified equation craft (009 pattern; 015's build uses the same recipe) |
| 14 | Font | Arial everywhere | Arial | SAME |
| 15 | Emphasis color system | red `C00000` = Loss terms, blue `0000FF` = J(W)/R(W)/||W||, green `008000` = Ridge Regularization + WᵀW, navy `1E0060` = box borders/rules, maroon family (`8F1220`/`742C2D`/`B60007`/`800020`) = box borders + title + labels | red `C00000` = headers + key phrases, blue `0000FF` = L1/L2 naming lines, `8B0000` title, `2B237A` frame border | DIFFER (palette roles overlap but assignments are per-slide — take 014's colors from 014's own analysis, never from 016) |

## Re-judge watch list (what the sanctioned re-judge will re-scrutinize)

1. Attempt-7's three REAL fixes are on render_7c and must survive the re-judge:
   bold underlined **X** in "from Model Ŷ = X̲W̲"; vector-box label lines at **14pt**
   wrapping as 2 clean lines; **underlines** under Ŷ/Y in the Define-Loss band.
2. Previously accepted MINORs the re-judge may re-raise (all adjudicated, banked
   in `adjudicate_attempt_7.md`): red PNG delimiter style (#4, style-level),
   band-1 inter-phrase gap width (#5), λW mathtext spacing (#7), ⋮ vs … (#8).
3. Ground clause (e): the final band's stacked-½ mathtext vs the original's
   handwritten fraction is a mandated format upgrade, not a discrepancy.
4. House chrome is identical primitive for both slides — never a finding.
