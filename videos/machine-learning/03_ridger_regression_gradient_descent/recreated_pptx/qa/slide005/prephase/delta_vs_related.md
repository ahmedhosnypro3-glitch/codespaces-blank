# delta_vs_related — slide 005 (S20a prephase, pool run 299640)

**Target:** `recreated_pptx/slide_005_recreated.pptx` — build `recreated_pptx/build/slide_005.js`
(attempt 9 state, gen_status=building; cert lane S1 judging; attempt-11 zoomed legs: legA
FAIL [MAJOR], blue_upper FAIL [BLOCKER X-vs-Y + MAJOR styling], eq_stack FAIL [MAJOR red ½],
pink_band FAIL [red bold W], lower_eqs PASS).

**Related certified build (pattern source):** `recreated_pptx/build/slide_021.js` (CERTIFIED)
— bordered blocks, 600dpi equation-PNG ink-box placement law, multi-color per-segment
equation composition (`qa/slide021/compose_eq_021.py` pattern). Also
`shared_patterns/house_chrome.js` (numeral 5), `eqFit()` ink-box placement in slide_005.js,
and the nine `eq_005_*` PNG+sidecar assets.

**Sources of truth for the ORIGINAL side:** PIL passes on `unique_slides/slide_005.jpg`
re-verified 2026-10-25 (box fills/borders sampled again this window); verbatim + styling
confirmation rides on desc legs (`desc_{full,eq_stack,blue_upper,pink_band,lower_eqs}.txt`)
— pending items marked `[?] desc_<leg>`.

## Element table — ORIGINAL vs current build

| # | Element | ORIGINAL (frame px) | Current build (attempt 9) | Delta |
|---|---------|---------------------|---------------------------|-------|
| 1 | House chrome | deck-03 chrome, numeral 5 | house_chrome.js numeral 5 | KEEP |
| 2 | Title | ink x162..808 y68..92 one line 18pt-bold metrics; red + "BEST" blue (ink x565..619) + red | 18pt bold DejaVu Sans runs @x162 y69 | KEEP |
| 3 | Cream upper box | x72..892 y102..277, fill (251,253,229) = FBFFE5, border BCBEB8 | rect(72,102,821,176) CREAM/CBORD | KEEP |
| 4 | Loss equations (upper) | eq1 ink x98..544 y109..150; eq2 x97..629 y173..214; eq3 x98..522 y230..271; attempt-11: the FIRST ½ fraction is RED in the original | eqFit(loss1/loss2/loss3) at those ink boxes; all three PNGs are single-color 000000 (sidecars) | DIFFER-[?]: `desc_eq_stack` confirms which ½ is red (loss1 per attempt-11). If confirmed, recompose eq_005_loss1.png multi-color (slide_021 compose pattern: per-segment mathtext, red ½, black rest) — **PROBE NOTE (pil_probe_005.txt, 2026-10-25): eq_005_loss1.png ALREADY carries the red ½ (#AC4E4E ink at 15.8–20.9% of ink width = the ½ position, PIL-verified; frame red cluster x150..169 = the ½, zero red in eq2/eq3 bands). Do NOT recompose before re-checking the asset — the gap is only the sidecar's color field (000000 underrecords it). Recomposing from the sidecar alone would DROP the red ½** |
| 5 | Equation TEXT (upper) | loss1 = ½(Y−Ŷ)ᵀ(Y−Ŷ) = ½(Y−XW)ᵀ(Y−XW); loss2 = ½[YᵀY+(XW)ᵀ(XW)−Yᵀ(XW)−(XW)ᵀY]; loss3 = ½[YᵀY+(XW)ᵀ(XW)−2(XW)ᵀY] (sidecar mathtexts) | same | KEEP — desc_eq_stack verifies digit/glyph-level `[?]` |
| 6 | Blue upper box | x676..882 y134..236, fill (218,236,250) = DAEBFA, border 9BAAB0 | rect(676,134,207,105) BLUEF/BBORD | KEEP |
| 7 | Blue upper content | "Remember" red bold x681..761 y138..149; "X is a matrix, W is a vector," x680..873 y158..171; "XW is a vector" x680..792 y179..190; eq x680..864 y213..235 (sidecar fs 21.7); **upper eq first glyph PIL-SETTLED 2026-10-25 = serif Y (fork + center stem + bottom flare)** | 12pt/14pt runs (X red, W blue-underlined 3736BB, XW underlined); eq_005_remember1 renders Yᵀ(XW)=(XW)ᵀY | X-vs-Y RESOLVED: attempt-11's "original reads Xᵀ…" does NOT apply to the upper box — the build's `Y^{T}(XW) = (XW)^{T}Y` is CORRECT; do not re-render remember1 for X. Remaining `[?]`: only per-token colors/bold/underline on the Remember text lines — `desc_blue_upper` |
| 8 | Pink band | x73..506 y288..343, fill (241,202,205) ≈ F8CFD3, border 7D1B28 | rect(73,288,434,56) | KEEP |
| 9 | Pink band content | ∂Loss/∂W = 0 at x79..164 y294..338; "Get Best W that minimizes the loss" x196..500 y306..322 with W red bold (attempt-11) | eqFit(pinkfrac) + 17.4pt runs, W red bold | KEEP — build already draws W red bold (attempt-11's finding appears already addressed; desc_pink_band confirms) `[?]` |
| 10 | Cream lower box | x72..892 y358..522, fill (251,253,229) — SAME cream as upper (re-verified 2026-10-25); analysis JSON's "#F0F0F0 gray" for this box is a vision misread | rect(72,358,821,165) CREAM | KEEP (build correct; do not "fix" toward the analysis JSON) |
| 11 | Derivative equations | eq4 ink x96..592 y374..420 (∂Loss/∂W = 0 = ½[(XW)ᵀX + Xᵀ(XW) − 2XᵀY]); eq5 x96..637 y460..502 (chain …→(XᵀX)W̲ = XᵀY →); attempt-9 noise law: original ink genuinely ends x637 (no ink x639..646, noise-only x647..683) | eqFit(deriv1 @x97..592, deriv2 @x96..637) | KEEP — desc_lower_eqs verifies glyphs `[?]` |
| 12 | Blue lower box | x656..873 y372..422 — left border x656 (re-verified this window: cream → border col x656 → fill from x658; right edge ~x873); fill DAEBFA; "Remember" red bold x661..733 y376..385 (~20px LEFT of the upper box's x681); eq x660..867 y395..420 | rect(656,372,217,51); Remember @x661; eq_005_remember2 @660..867 | KEEP geometry. NOTE: an earlier prephase note claimed left edge x678 — that was a misprobe of equation ink at y400; the border is at x656 (build correct) |
| 13 | Lower Remember equation | **PIL-SETTLED 2026-10-25 (ASCII-art glyph topology): original lower = Xᵀ(XW)=(XW)ᵀY** — first glyph = X (crossing diagonals, four serifs, empty center below the crossing), last glyph = Y | eq_005_remember2 PNG renders Yᵀ(XW)=(XW)ᵀY (sidecar mathtext `Y^{T}(XW) = (XW)^{T}Y`, fs 24.4) | DIFFER CONFIRMED (attempt-11 legA MAJOR stands, no transcript needed): re-render eq_005_remember2.png via scripts/render_eq.py with `X^{T}(XW) = (XW)^{T}Y`, re-place via eqFit at ink box x660..867 y395..420, update the sidecar mathtext |
| 14 | Green ring box | x688..879 y464..497, ring 2F8F3F, fill (203,248,221) ≈ CEFFE3 | rect(688,464,192,35) GFILL/GRING | KEEP |
| 15 | Final W formula | W = (XᵀX)⁻¹XᵀY at x690..878 y465..497 | eqFit(finalw) | KEEP — desc_lower_eqs confirms `[?]` |
| 16 | Fonts | original metrics matched by DejaVu Sans (probe-verified in build comments: title 643.8 vs 647; Get Best W 313.8 vs 311) | DejaVu Sans | KEEP |

## Open questions riding on the desc legs

1. `desc_eq_stack` — #4 red ½ location + extent; #5 glyph-level equation text.
2. `desc_blue_upper` — #7 per-token styling only (upper X-vs-Y PIL-settled = Y;
   attempt-11's X claim refuted for the upper box).
3. `desc_lower_eqs` — #11/#15 glyphs (lower X-vs-Y PIL-settled 2026-10-25 = Xᵀ…Y;
   legA MAJOR confirmed without a transcript).
4. `desc_pink_band` — #9 W styling + ∂-fraction colors.
5. `desc_full` — global cross-check; box region map re-confirmation.
