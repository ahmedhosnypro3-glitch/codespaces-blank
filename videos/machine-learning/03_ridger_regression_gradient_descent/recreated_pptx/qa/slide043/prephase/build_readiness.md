# build_readiness.md — slide 043 "Perceptron Iteration 2" (S20d prephase, 2026-10-25)

Worker S20d · READ-ONLY toward the cert lane's products · evidence:
`delta_vs_related.md` (this dir), PIL passes in `scratch/tmp/s20d_prephase_pil_043_044.py`
+ `s20d_prephase_pil_refine.py` + `s20d_prephase_pil_044extra.py`, 042 stack transcript
(`../slide042/prephase/orig_judges/slide_042_stack_desc.txt`).

## Lane state being handed back

- `build/slide_043.js` is the live build; `qa/slide043/` holds the earlier attempt
  cycle's artifacts (build_attempt_2/4.js, crop_4_* judges). The lane's current mission
  cycle had **not fired its judge legs** as of S20d start — this pack is the fast-start
  input for that cycle.
- **Rebuild blocker (must clear first)**: every 043 image asset is missing repo-wide —
  `eq_043_dx1..6.png`, `eq_043_w1..6.png`, `eq043_mx1..3.png`, `aug_043.png` (verified
  by project-wide `find`; only the JSON sidecars exist). Any rebuild dies at addImage.
  The banked pptx (00:04) is unaffected.

## HEADLINE: assets + band content both need regeneration

The sidecars' mathtext is the flattened dot-product garble (e.g. dx1
`[1 \; 1 \; 1; \; -10; \; -8]` = `|1 1 1| (4,−10,−8)` flattened), and the 042 stack
transcript proved the frame's true band form: `d(xᵢ) = |row| (green W col) = value ⇒
decision`, plus a long update equation on Update rows only. **The 043 stack + topband
transcripts have now LANDED and are PIL-arbitrated** — full per-band ground truth in
`delta_vs_related.md` ("Band content ground truth"). Headline corrections vs earlier
drafts: the frame skeleton is **7 box rows on ALL of 042/043/044** (6 content boxes
+ a bottom sliver; the stack crops saw boxes 2–6 only), and band 2 prints **−16**
(the 043 transcript's `−14` is a vision misread — PIL glyph shape + arithmetic).

## Numbered delta→action checklist

1. **Regenerate ALL 043 PNG assets locally** with `scripts/render_eq.py` (certified
   tooling); write sidecars with repo-relative `path` + bare `image` field. Blocker
   above — do this first.
2. **Rewrite the band mathtext in dot-product form** after [S20d-vision stack] lands
   (`prephase/orig_judges/slide_043_stack_desc.txt`): per-band `d(x_i) = |a b c| (w1,w2,w3)
   = v` + Update rows' `W = (old) ± 2*(x) = (new)`. Color runs (red/blue digits, green
   W vectors) are not reachable in one mathtext PNG — split per-run PNGs like the 042
   rebuild plan (see `../slide042/prephase/build_readiness.md` actions 1–3).
3. **Stop full-row stretching**: the current eqImg stretches each dx PNG across
   dxL..dxR (band 1: x287..829 = 1.669× natural width, h clamped 0.20 vs natural 0.28
   → ≈2.3× aspect distortion) and overprints the decision/W zones. Place per-cluster:
   dx cluster x≈282..458, ⇒+decision x≈480..642, W equation right — exact x's from the
   stack read.
4. **Re-anchor the decision texts**: build draws them at x = dxL (x287) with decTop
   between the dx and w rows — the 042 transcript and 044's build both put decisions on
   their own position/row; the stack read arbitrates.
5. **Fix Initial-W** (PIL-verified): right stroke x430.5 → **x353** (three-frame
   identity with 042/044); **add the third digit row** (frame rows y63..69 / 78..86 /
   94..101, pixel-identical to 044's); realign the two existing digits onto rows 2–3.
6. **Delete all four blue arrows** (3× 45px lines + the x673..686 one) — S20d-PIL
   refutes them: the zones hold the dx lines' blue `|digits|` (bar/digit/bar clusters,
   pixel-identical to 044's), and the "extra arrow" zone matches 042's blue `− 2 *`
   ink. Drawing arrows overprints real digit ink.
7. **Add the white calc-area fill** (x275..852 y141..527) — frame interior measured
   (253,254,252) ≈ white; without it the E9E9E7 panel shows through. Copy 044's v2
   pattern (`build/slide_044.js` lines ~185-188).
8. **Port txtsub runs** for TL headers, TL class row, and Z1 (041-cert pattern; the
   build uses plain "x1"/"C1"/"Z1").
9. **TL/Z paren mechanisms** — after [S20d-vision topband]: if the frame shows bowed
   parens (041-cert's P3 pattern), port `qa/slide041/assets/parens041/`; the Z-matrix
   already uses tall-paren PNGs (eq043_mx1..3) — regenerate them in action 1.
10. **LM caption color**: build 3B3F8C vs analysis "black" — S20d-PIL shows the caption
    band is blue-family (611 blue px, 0 red); the lm/topband read picks the exact tone.
11. **Verify aug_043.png content** when regenerating (action 1): the single-PNG LM table
    must carry the colored class row (frame: 15 red + 23 blue px y228..246) and match
    the frame's paren style.
12. **Keep as-is**: legend (already 041's per-fragment pattern, frame-confirmed colors),
    solid-red Iteration 2 badge (frame wins over analysis "red border/black text"),
    calc-area skeleton, cream/navy top band (measured tones), band y-structure.
13. **Re-render → house-chrome check → judge legs** per `scripts/17_worker_instructions.md`;
    hand the judges the 042 transcript + this pack so the dot-product band form is read
    as ground truth.

## Reusable certified components

- `shared_patterns/house_chrome.js` + checker.
- 041-cert P3 paren PNGs: `qa/slide041/assets/parens041/`.
- `scripts/render_eq.py` (certified mathtext → 600dpi transparent PNG; sidecar writer
  pattern in `qa/slide044/gen_assets_044.py` — port paths to this host).
- 044's white-fill calc area + text-row LM table pattern (`build/slide_044.js`).
- 042's `render_stackeq_042.py` (extend for colored runs / dot-product form).
- txtsub pattern from 041-cert.
- 042 stack transcript as the structural ground truth for all three slides' bands.

## Judge-payload notes (when the lane re-judges)

- Carry the analysis-vs-frame corrections so the judge doesn't re-import analysis
  errors: equations are dot-product form (analysis garble is a flatten); class colors
  C₁ red / C₂ blue (frame); LM caption blue-family; no blue arrows exist on the frame.
- GROUND RULES: e-format upgrades are not discrepancies; house chrome disagreements are
  overridden by the house law.

## Topband S20d ground-truth desc (slide_043_topband_desc.txt, 2026-10-25)

Frame facts now CERTIFIED for arbitration:
- Initial W = (4; −2; −2) — a 3-ROW column vector (parens span slide y62..116).
  Judge's "Initial W missing −2 component (MAJOR)" was REAL.
- TL vectors: SIX 2-row columns (1/1)(2/1)(1/2)(5/4)(6/5)(6/6); C1 red ×3,
  C2 blue ×3. Z vectors: (0/0)(7/6)(3/2); Z subscripts read Z1 Z1 Z1 [?].
- Legend: "C1 positive  C2 negative  Zero is unaccepted" — C1 RED here
  (differs from 042's black-C1 frame; per-frame, not a template constant).
- Step η = 2 red bold italic. Blue box border #1A1ACC on cream #FFFFE8 fill,
  slide-space (68,55.3)..(739.5,132).
- Attempt-4 stack/equation judge findings still need crop-leg arbitration
  against the stack/midleft S20d descs before any digit edits.
