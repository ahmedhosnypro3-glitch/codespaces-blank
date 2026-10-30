# delta_vs_related.md — slide 044 "Perceptron iteration 3" (No title) vs certified slide 041

Worker S20d (prephase) · 2026-10-25 · READ-ONLY toward the cert lane's products.
Baseline: **slide 041, certified 2026-10-25** (`build/slide_041.js`, attempt 5 PASS).
044 = iteration 3: same family as 042/043 with SIX calc bands (x₁..x₆) and a white-filled
calc area.

Evidence tags: **[041-cert]** certified 041 build; **[044-build]** `build/slide_044.js`;
**[S20d-PIL]** PIL passes (`scratch/tmp/s20d_prephase_pil_043_044.py`,
`s20d_prephase_pil_refine.py`, `s20d_prephase_pil_044extra.py`, `s20d_prephase_pil_zero.py`,
`s20d_prephase_pil_redshape.py`, `s20d_prephase_pil_044stack.py`, `s20d_prephase_pil_044stack2.py`);
**[S20d-vision]** ground-truth reads — `slide_044_stack_desc.txt` + `slide_044_topband_desc.txt`
both LANDED (2026-10-25) and PIL-arbitrated below; the lm/full legs were skipped: their open
disputes resolved by PIL + the two landed reads (lm/full dispatch scripts remain banked for
re-runs); **[044-analysis]** `analysis/slide_044_final.json`.

## House chrome

Identical (numeral 44). NOT a delta.

## Element-by-element delta

| # | Element | 041 (certified baseline) | 044 | Action for 044 build |
|---|---|---|---|---|
| 1 | Cream top box | fill FEFFE8, border 0000FF, x70..718 y54..130 [041-cert] | fill FFFEE8 x70..718 y56..128 + NAVY 221777 outline x68..720 y54..130 [044-build, measured] | DIFFER (tone/two-layer): frame-measured — keep 044's colors; don't normalize |
| 2 | TL x1..x6 headers | txtsub runs BLACK bold 10pt [041-cert] | Unicode "x₁".."x₆" 13pt cx 101..212 [044-build] | DIFFER (mechanism): Unicode subscripts visually approximate but aren't the ported pattern — port 041 txtsub (low-risk polish) |
| 3 | TL column vectors | 2-row stacked, bowed P3 paren PNGs [041-cert] | per-cell "(1)" text rows y80/y96; **two** data rows [044-build, deviation 4] | DIFFER (mechanism + count dispute): [044-analysis] claims a 3rd row "(1)(1)(1)(2)(4)(5)" — build's pixel sampling says two digit bands. VERIFY [S20d-vision topband]; if tall shared parens, port 041 P3 pattern |
| 4 | TL class row | C1C1C1C2C2C2 txtsub red/blue [041-cert] | Unicode C₁ RED/C₂ BLUE y113 [044-build] | KEEP colors — **S20d-PIL CONFIRMS red C1 (24 red px y108..122); [044-analysis] typography "C₁ blue C₂ red" is REFUTED** (frame wins). Port txtsub mechanism |
| 5 | Legend sentence | per-fragment boxes y107..123: C1 RED x237, C2 BLUE x311, Zero GREEN x392..423 [041-cert] | **ONE multi-run addText**: C₁ RED / " positive, " / C₂ BLUE / " negative, Zero is unaccepted" — **Zero is BLACK** [044-build] | DIFFER (2 bugs): (a) **Zero must be GREEN** — S20d-PIL: legend band green=165 px on 044, pixel-identical to 041/042/043 (163/166/165); (b) multi-run addText is the pattern 042 proved breaks run colors in LO renders — **port 041's per-fragment boxes verbatim** |
| 6 | Initial W block | "Initial W =" 12.5pt x263 y72; wvec P3 parens x330.5/x352.5; THREE stacks y59/75/93 [041-cert] | strokes x331/x353 y55..103; THREE digit rows y62/78/93 [044-build] | KEEP count/geometry (frame-verified; S20d-PIL digit rows y63..101 identical to 043's). Mechanism DIFFER: line strokes vs 041's P3 bowed parens — VERIFY [S20d-vision topband] whether the frame's parens are bowed; if so port P3 PNGs |
| 7 | Check classes block | Z1 txtsub + ztab P3 paren PNGs (0,0)(7,6)(3,2) [041-cert] | Z₁ Unicode + per-cell "(0)" text rows, **no tall parens** [044-build] | DIFFER (mechanism): 041 (and 043's mx PNGs) show tall shared parens per column — VERIFY [S20d-vision topband]; if present, port ztab/mx pattern. Also [044-analysis] claims a "blue-outlined box" around the matrix — **S20d-PIL REFUTES** (zero blue stroke px in x555..700 y50..115 beyond the top-band outline rows y54/56); build is right to omit |
| 8 | Plot | present [041-cert] | ABSENT — calc bands | DELETE — correct |
| 9 | LM caption | — | "Upgraded Vectors (from Top)" **BLUE** bold x86 y148 [044-build] | ADD — keep. **[044-analysis] "red caption" REFUTED by S20d-PIL** (596 blue px, 0 red in y145..162) |
| 10 | LM table | — | header y166 + THREE text data rows y184/199/214 ((1)×6 / (1)(2)(1)(5)(6)(6) / (1)(2)(4)(5)(6)(6)) + class row y232 red/blue [044-build] | ADD — keep (rows match [044-analysis]; class colors frame-confirmed: 16 red + 22 blue px y228..246). Mechanism (text) differs from 043's single-PNG — either is fine if frame-faithful |
| 11 | Iteration badge | — | roundRect **FF0000** x84..214 y277..305 + white 15pt "Iteration 3" [044-build] | ADD — keep (matches [044-analysis] "red rounded badge"). Note 042/043 use solid rect C00000 — per-frame difference, keep each |
| 12 | Calc area | — | **WHITE fill rect** x275..852 y141..527 + verticals x273.5/x852.5 + 11 rules [044-build] | KEEP — this is the certified-pattern precedent **043's build is missing** (S20d-PIL: frame interior white (253,254,252) on both) |
| 13 | Band dx/w equations | — | `eqImg` passes `m.path` from `eq_044_*.json` sidecars **straight to addImage** [044-build] | **BLOCKER**: sidecar `path` fields are dead `/workspaces/codespaces-blank/...` absolutes AND the PNG files themselves are **absent repo-wide** (only 042's w-PNGs exist) → any rebuild fails. Fix: regenerate assets locally with corrected paths + dot-product mathtext (see sidecar notes) and switch eqImg to `ASSETS + m.image` |
| 14 | Decision rows + W lines | — | "⇒ Update Weight" RED rows 1–3 / "⇒ Keep same Weight" black rows 4–6 at x333..338, 15pt; W sidecars colored C00000 rows 1–3 / 000000 rows 4–6 [044-build, "red ink measured x337..830"] | VERIFY [S20d-vision stack]: the 042 transcript shows the update equation as black W-parens + blue `− 2 *` + green result — if 044's frame matches the family, the all-red W lines are wrong; the read decides |
| 15 | Far-right ⇐ in update rows | — | none drawn [044-build]; [044-analysis] claims ⇐ at far right of updated rows | DIFFER-risk: 042 precedent = red ⇐ x771..791 in the update box [S20d-vision stack]. If 044's frame carries them, ADD red ⇐ in bands 1–3. Mouse-pointer near d(x₄): keep omitted (capture artifact, same as 042's transcript ruling) |

## S20d original-frame findings (PIL-verified) the lane does not yet have

- **H1 — rebuild blocker (assets)**: dead sidecar paths + missing PNG files (row 13).
  Banked pptx (00:04) is unaffected; only rebuilds break.
- **H2 — legend Zero must be green**: 4-slide PIL identity (green 163/166/165/165);
  build lumps Zero into a black run (row 5a).
- **H3 — legend mechanism risk**: single multi-run addText vs 041's certified
  per-fragment boxes (row 5b).
- **H4 — analysis C₁/C₂ swap refuted**: frame class rows are C₁ red / C₂ blue
  (rows 4/10; build correct).
- **H5 — analysis "blue-outlined box" refuted** (row 7): no blue matrix-box strokes on
  the frame.
- **H6 — analysis "red caption" refuted** (row 9): caption ink is blue.
- **H7 — Initial-W three stacks confirmed** (row 6): PIL digit rows y63..101 identical
  to 043's; [044-analysis] "[4; −2]" dropped the third row (build comment already
  refutes; now PIL-backed).

## Sidecar notes (eq_044_*)

- All 14 sidecars (`dx1..6`, `w1..6`, `initw`, `step`) exist as JSON with **dead**
  `/workspaces/codespaces-blank/...` `path` fields and **no `image` field**; the
  corresponding PNG files exist **nowhere** in the repo.
- `qa/slide044/gen_assets_044.py` is the generator but hardcodes the codespace DECK and
  RENDER paths — port to this host before reuse.
- Mathtext is the flattened dot-product garble, e.g. dx1
  `d(x_1) = [1 \; 1 \; 1; \; -12; \; -8] = -12` — decodes to
  `d(x₁) = |1 1 1| (8,−12,−8) = −12` (043's final W = (8,−12,−8); arithmetic ✓), and its
  w1 `W = [4; -2] + 2 * [3; -2] = [10; -6]` decodes to
  `W = (8,−12,−8) + 2*(1,1,1) = (10,−10,−6)` (first/last components ✓, middle lost in
  the flatten). Regenerate in true dot-product form after [S20d-vision stack] lands.
- 042 contrast: `eq_042_w1..5.png` exist and the 042 lane rebuilt successfully today —
  only 043/044 asset sets are broken.

## [S20d-vision stack+topband] ARBITRATION — transcripts landed 2026-10-25, PIL-arbitrated

Evidence: `orig_judges/slide_044_stack_desc.txt` (stack crop, img/3 + offset (264,206)),
`orig_judges/slide_044_topband_desc.txt` (topband crop, 4× upscale, offset (50,44)),
PIL passes `s20d_prephase_pil_044stack.py` + `s20d_prephase_pil_044stack2.py`.
**Transcript x-positions are LOCALLY DRIFTED (topband worst: Z labels +32px, TL −4px,
Initial-W +5px) — content/colors/structure are transcript-authoritative, absolute
geometry is PIL-authoritative.** All positions below are PIL where a PIL pass exists.

### Row verdicts (supersedes the VERIFY items in the table above)

| Row | Was | Now |
|---|---|---|
| 3 (TL vectors) | VERIFY count + parens | **RESOLVED**: TWO data rows (1/1)(2/1)(1/2)(5/4)(6/5)(6/6) — build correct, [044-analysis] 3rd row REFUTED. Tall thin parens per column (transcript; span ≈36 slide px) → port 041 P3 pattern. Column centres PIL ≈ 96/118/140.5/163/185.5/208.5 = 041-cert identity (transcript's 93.8..237 spacing-28.6 reading is drift) |
| 5 (legend) | VERIFY Zero color + mechanism | **CONFIRMED**: legend reads C₁ RED x≈239 / "positive," italic / C₂ BLUE x≈315 / "negative," italic / Zero GREEN bold x≈398 / "is unaccepted" black (transcript + the 4-slide PIL identity). Both build bugs (Zero black, multi-run addText) stand as fixes |
| 6 (Initial W) | VERIFY paren mechanism | **CONFIRMED**: THREE black digit stacks (4/−2/−2 at y66/81/97; PIL rows y63..101), BLACK tall parens (transcript) at PIL strokes **x330 + x353** (three-frame identity with 042/043 — transcript's 338/360 is drift). `W` carries the underline bar (x319.5..330 y91.5..93). NO ᵀ superscript (layout-map artifact; the verbatim section lists none) |
| 7 (Z-matrix) | VERIFY parens | **CONFIRMED**: tall thin parens per column; values (0,0)(7,6)(3,2) ✓ 041-cert identity. Z labels PIL cx ≈ 605/627.5/648..650 = 041-cert cx 605.5/628/650 (transcript's 637/665.5/695.5 is +32px drift). Z₁ Z₁ Z₁ stands (transcript [?] on 2nd/3rd subscripts is pixelation; 041-cert + 043 build precedent) |
| 13 (assets blocker) | regen needed | **UNCHANGED + spec now final** — see the per-band table below for the exact mathtext/colors to regenerate |
| 14 (decision rows + W colors) | VERIFY | **ARBITRATED — build wrong on placement, right on which rows are red**: (a) update rows = frame boxes 1–3 (d(x₁)=−12, d(x₂)=−16, d(x₃)=−2 all misclassified C₁) ⇒ build's `decRed rows 1–3` is CORRECT; (b) decision ink sits at **⇒ x≈508..514, text x≈529..642** — NOT the build's x333..338 (that zone is the dx cluster; drawing decisions there overprints it); (c) the W-line ink is NOT all-red: per transcript every band reads black `W̲ =` + black old-W column + **RED `+ 2 *`** (PIL: R1 13 red / 0 blue px, R2 6 red / 0 blue — the [?]-red confirmed) + black x-column + GREEN result. All-red w1..w3 sidecars are wrong → multi-part colored regen |
| 15 (far-right ⇐) | VERIFY | **CONFIRMED**: red ⇐ present in update rows ONLY — PIL red px: R1 89, R2 28, R3/R4/R5 0 (x808..838 zones; transcript x≈815..831) → ADD red ⇐ to build bands 1–3 (= frame boxes 1–3, all three update rows; box 1 per the sidecar decode + arithmetic + 042 family pattern) |

### Per-band ground truth (frame boxes 1–6 = build bands 1–6; borders PIL y139.5/197 | 206/263 | 272/329.5 | 338/395 | 404/461 | 470/528)

| Box | d-row (dx sidecar) | ⇒/decision | W group (w sidecar) | ⇐ |
|---|---|---|---|---|
| 1 | `d(x₁) = \|1 1 1\| (8,−12,−8) = −12` — RED digits, GREEN vec [sidecar decode + arithmetic ✓ + family; above the stack crop] | red ⇒ Update Weight | `W̲ = (8,−12,−8) + 2*(1,1,1) = (10,−10,−6)` black/RED+2*/black/GREEN | red ⇐ |
| 2 | `d(x₂) = \|1 2 1\| (10,−10,−6) = −16` — RED/GREEN [transcript] | red ⇒ Update Weight | `W̲ = (10,−10,−6) + 2*(1,2,1) = (12,−6,−4)` | red ⇐ |
| 3 | `d(x₃) = \|1 1 2\| (12,−6,−4) = −2` — RED/GREEN [transcript] | red ⇒ Update Weight | `W̲ = (12,−6,−4) + 2*(1,1,2) = (14,−4,0)` | red ⇐ |
| 4 | `d(x₄) = \|1 5 4\| (14,−4,0) = −6` — BLUE/GREEN [transcript] | black ⇒ Keep same Weight | short `W̲ = (14,−4,0)` only | none |
| 5 | `d(x₅) = \|1 6 5\| (14,−4,0) = −10` — BLUE/GREEN [transcript] | black ⇒ Keep same Weight | short `W̲ = (14,−4,0)` only | none |
| 6 | `d(x₆) = \|1 6 6\| (14,−4,0) = −112` — BLUE/GREEN [transcript + **PIL glyph proof**: three glyphs 1(x434..436)/1(x440..442, no diagonal drift — not 7)/2(x445..450, flat bottom bar — not 0); R4's true `−10` shows a closed-oval 0 for contrast] | black ⇒ Keep same Weight | short `W̲ = (14,−4,0)` only | none |

- **The −112 is the ORIGINAL SLIDE'S OWN ARITHMETIC TYPO** — (1,6,6)·(14,−4,0) = −10,
  and the frame prints −112. Frame wins for recreation: **recreate −112 verbatim, never
  "correct" it**; carry this note into the judge payload so the judge doesn't flag it
  (contrast: 042's last box −104 is arithmetic-true — the family is not uniformly typo'd).
- Every band's `W` carries the **underline bar** (W-bar notation), R1–R5 all transcribed
  with it; the eq_044_w* regen must render it.
- Subscripts on transcript ROW 4 / ROW 5 (= frame boxes 5/6, the d(x₅?)/d(x₆?) [?]
  "5 vs 6" pair): **resolved x₅ (box 5) and x₆ (box 6) by elimination** — six training
  vectors exist (TL/LM), rows read x₂,x₃,x₄ unambiguously, so the last two are x₅,x₆ in
  order; 042's identical five crop boxes resolved the same row to x₆ by glyph shape.
  PIL glyph ID itself inconclusive (3px glyphs).
- Structure per band (transcript x's, PIL where noted): dx cluster x≈282..458 · ⇒ x≈508 ·
  action x≈529..642 · `W̲ =` x≈634..650 · old-W column x≈663..695 · `+ 2 *` x≈703..718 ·
  x-column x≈727..748 · `=` x≈755 · result column x≈765..795 · ⇐ x≈815..831 (Keep rows
  end after the short W group ≈x695).
- Pencil/pen icon in frame box 3 at (455.7,342)..(474,360) = screen-recording cursor —
  capture artifact, omit (same ruling as 042's mouse cursor). The red verticals at the
  crop edges (stack: x≈893..898 zone, PIL red px only at the house stroke x902; topband:
  x50..53) are the **house left/right strokes**, not content.

### New PIL finding — calc-area rule missing

The frame carries **12** border rows (six boxes × top+bottom, gaps between: PIL rows
139/140, 197, 206, 263, 272, **329/330**, 338, 395, 404, 461, 470, 528); the build draws
**11** (`[140,197,206,263,272,338,395,404,461,470,528]` in `build/slide_044.js`) —
**box 3's bottom rule y≈329.5 is missing**, so the build merges the box-3/4 gap into
box 3. Unlike 042, there is NO 7th sliver row below y528 on this frame (scanned to 540).
Border tone ≈ light blue-gray (PIL samples (203,210,218)/(169,176,186); transcript
#9FB6C9; 042's #AEB8C2 — same family, GRAYBLUE constant acceptable).
