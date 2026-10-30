# Slide 025 — delta vs related certified slides 022/023/024 (S20b prephase ground-truth pack)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent` · frame
`unique_slides/slide_025.jpg` (960×540, 1 frame px == 1 pt). Companion doc:
`prephase/build_readiness.md`. 025 is a ROOT slide (no parents, no children —
no cascade either way).

## Baseline — the certified text-slide pattern (022/023/024)

- **022**: title TWO lines "[3] Inverse of High Dimension" / "(non-singular)
  Matrix", Arial Bold **38pt** (per-line addText with per-line TUNE: size,
  charSpacing, dx/dy), red C00000-family (darkest-core px (121,1,13) =
  JPEG-darkened C00000); exports a certified component
  (`build/components/slide_022.js`).
- **023**: red title + black body runs 19–20pt + the main equation as a 600-dpi
  mathtext PNG (`build/assets/eq_023_main.png` + `.json` sidecar for the
  post-certification OMML wrap).
- **024**: title "Gradient Descent (GD)" + two red subheads, C00000-family,
  same darkest-core justification.
- All three: house chrome, text-only bodies, no raster plot assets.

## Evidence instruments cited

- **P1** — prephase reads `prephase/orig_judges/orig_025_title.txt` (title),
  `orig_025_tl.txt` (top-left quadrant). Crops:
  `prephase/orig_judges/crops/slide025_*.png`.
- **P2** — lane zoomed judges: `qa/slide_025/crop_11_tr_judge.txt` + 
  `crop_10_tr_judge.txt` (TR region, both FAIL), `crop_9_lbl_*` (label-box
  face), crop_4/7/8 iterations (earlier Ks).
- **P3** — current build `build/slide_025.js` (md5 96f2197597b59d0f36c562922b298d47,
  2026-10-25 08:07) + plot generator `build/generate_plots_025_k10.py`.
- Parked prephase legs: 025 full-frame, TR, BL, BR (vision gate saturated all
  window — pgrep 15–17 ≥ 8).

Small-glyph hexes are BEST-EFFORT; colors marked **(PIL)** need a census before
gating a fix.

## Delta table (element-by-element, 022–024 baseline → 025 original)

| Δ | Element | 022–024 certified baseline | 025 original (measured) | Class |
|---|---------|----------------------------|--------------------------|-------|
| 1 | House chrome | numerals 22/23/24 | identical system, numeral 25 | SAME |
| 2 | Title | two-line 38pt (022) / title+subheads (023/024), C00000-family | SINGLE line "Types of Loss function shapes", Arial Bold **~22pt** (cap 14–15px), ink #A61C1C–#B02020 → C00000-family (same darkest-core rule as 022/024), no underline, centered x425.5, ink y63..88 | DIFFER (size/line count), ink family SAME |
| 3 | Body | text body runs (+ 600-dpi equation PNG on 023) | **NONE** — verbatim_text.bullets empty, no subtitle: the whole body is a 2×2 grid of 3-D surface plots + 4 label boxes | DELETE text-body pattern |
| 4 | 3-D plots | none | FOUR raster jet surface plots (advanced-graph rule): matplotlib **mplot3d** + jet cmap (already in-repo: `generate_plots_025_k10.py`), 300-dpi PNGs placed UNSCALED at measured figure boxes — TL x85..265 y115..288 (180×173), TR x616..879 y115..317 (263×202), BL x83..376 y290..527 (293×237), BR x615..880 y344..531 (265×187); each in a white figure rect with a thin red border ~3px inside its edge | ADD |
| 5 | Slide-level red strokes | none (text slides) | horizontal 2-D strokes: TL y168 x119..267, y186 x109..281, **y200 x88..274 (third line)**; TR y226 x633..875, y234 x644..867 + slanted stroke A (860,189)→(655,209) rising left→right + short stroke B (737,210)→(755,225); BL y418 x124..382; **BR none** (the y371..396 x698..875 ink is jet colormap, not a line). All present in build (REFLINES + 2 line shapes) ✓ | ADD |
| 6 | Label boxes | none | FOUR blue boxes, white bold two-line text (band pitch ≈12px): LB1 "Concave Function / One Maxima" x270..406 y137..178; LB2 "Convex Function / One Minima" x475..611 y184..225; LB3 "Gradient Descent / Path to reach Minima" x474..611 y354..391; LB4 "Non-Convex / Multiple Minima" x382..518 y452..489. Fill measured **dark navy #1A1A96** (build 0000A0 — minor shade) (PIL); text face **bold SERIF Times-like** per P1-TL + crop_9 lbl judge (build Arial — DIFFER [?]) (PIL); first word YELLOW on LB1/LB2 ✓ build | ADD |
| 7 | Caption↔plot assignment | — | by measured X-OVERLAP: LB1↔TL (concave), LB2↔TR (convex), LB3↔BR (GD path), LB4↔BL (multi-extremum) — the analysis JSON's "right of/left of" phrasings are unreliable; frame geometry wins. Build ✓ | ADD |

## Per-plot ground truth (frame px)

**TL — concave dome**: red frame x88..262 y119..284; THREE red lines
y167–169 x120–270 / y184–187 x110–282 / y199–202 x105–274 (build REFLINES ✓);
wireframe mesh + ~7 contour rings projected on the floor plane; super-gaussian
dome, crown reads olive/green (no red cap) — K10 generator header.

**TR — convex bowl + spike** (`crop_11_tr_judge.txt`, verdict FAIL vs K10):
- MAJOR — **left horizontal axis tick order REVERSED in the recreation**:
  original top→bottom 100, 50, 0, −50, −100; recreation −100…100. (Right axis
  100→−100 ✓; z axis LEFT 2/1.5/1/0.5/0 with ×10⁴ top-left ✓.)
- MAJOR — recreation draws an **extra thick dark-red line at z=0**, edge to
  edge; the original has NO line at z=0 (only the y226/y234 pair + stroke A).
- MAJOR — central spike: original reaches z≈**1.95–2.0** (sharp red apex, the
  focal point); recreation blunter, tip ≈1.6–1.7, with cyan/red diamond
  artifacts at its base.
- MINOR — ref-line pair sits at z≈0.4–0.45 in the original (recreation ≈0.4/0.5,
  slightly higher and more separated, and extends past the box edge where the
  original stops nearer the box); slanted stroke A protrudes past the right
  edge in the recreation; original gridlines are **DOTTED** gray with faint
  **contour projections on the bottom plane** (recreation: solid panes, none);
  corner-peak emphasis differs (corroborates the axis flip).

**BL — non-convex surface**: 4 black annotations with leader lines at slide px —
"Global Maxima" ~x242..268 y304..319, "Local Maxima" ~x286..315 y337..352,
"Local Minima" ~x286..311 y390..399, "Global Minima" ~x145..201 y439..465;
ONE red line y418 x124..382; ticks 6/4/2/0/−2/−4. **No BL crop-judge
certificate exists** (leg parked) [?].

**BR — GD path**: black gradient-descent path with arrows, **NO red line**;
white margins 8/10/37/22. **No BR crop-judge certificate exists** (parked) [?].

## Disputes / PIL-tiebreak queue

1. Label-box fill #1A1A96 vs build 0000A0 — PIL census.
2. Label-box text face serif vs Arial — PIL + one targeted re-read when a
   window opens (two instruments already say serif: P1-TL, crop_9 lbl judge).
3. TR spike exact apex value / ref-line z positions — re-judge after the K11
   regeneration (no separate PIL needed; the crop-pair judge covers it).
4. BL/BR regions carry no crop certificates at all — must be produced before
   certification (parked; see build_readiness.md D6).

## Corroboration & parked legs

- Banked here: 2 of 6 planned legs (title, TL). Crops for all parked legs are
  already cut (`prephase/orig_judges/crops/slide025_{tophalf,bothalf,tr,bl,br}.png`).
- Corroboration for parked regions: lane TR crop judges crop_10/11 (two
  independent FAIL verdicts with region-by-region findings — strong coverage),
  crop_9 label judges, build/generate_plots K-chain headers. BL/BR are the
  least-corroborated regions [?].
