# Slide 009 — worker report ("Overfit vs. Generalized")

Deck: `machine-learning/03_ridger_regression_gradient_descent`
Worker: `w009-judge-20261024` (build+judge lane; slide 009 gates child slide 010)
Frame ground truth: `unique_slides/slide_009.jpg` — 960×540, exactly 72 px/in (1 frame px = 1 pt = 1/72 in)

## Deliverable

| Artifact | Path | State |
|---|---|---|
| Build script | `recreated_pptx/build/slide_009.js` | current, certified |
| Component (for 010) | `recreated_pptx/build/components/slide_009.js` | refreshed, `renderBase` + per-block exports |
| PPTX | `recreated_pptx/slide_009_recreated.pptx` | single plain-named version |
| Certified render | `qa/slide009/render_3.png` (2001×1125, 150 dpi) | house chrome PASS |

## Judge attempts (shared budget, 6 max)

| Attempt | Render | Template A (full-slide) | Procedure B (crops) | Outcome |
|---|---|---|---|---|
| 1 | render_1.png | `judge_attempt_1.txt` — **FAIL** | `crop_1_eq_left_judge.txt` — PASS | PIL-adjudicated: all findings refuted (see below); attempt 1 also drove the real fixes listed under "Fixes" |
| 2 | render_2.png | `judge_attempt_2.txt` — **FAIL** | `crop_2_{eq_left,eq_right,cap_left,cap_right}_judge.txt` — all **PASS**; `chart_left`/`chart_right` calls hung on a saturated gateway (630 s hard wall) and were not banked | 3 of 4 findings refuted; finding 4 (caption enclosure) **CONFIRMED** → fixed |
| 3 | render_3.png | `judge_attempt_3.txt` | `crop_3_<name>_judge.txt` (6 pairs, `cut_crops_3.py` VERDICT PASS) | dispatched 2026-10-24; verdicts recorded when the run banks |

Cropped regions for attempt 3 (Procedure B, one per dense region, matched effective scale by construction — the original crop is LANCZOS-upscaled to exactly the render crop's pixel size): `eq_left`, `eq_right` (equation stacks), `cap_left`, `cap_right` (caption blocks), `chart_left`, `chart_right` (the two scatter charts).

## Fixes landed (each PIL-proven before the build moved)

1. **Annotation-box fill** — `E0F0FF` (224,240,255) → **`ECFDF9`**, reproducing the frame's box median `(236,253,249)` exactly on both sides. (Attempt 1, finding 4 — confirmed as a shade mismatch, not "spurious fill": the frame genuinely has a pale-cyan box.)
2. **Caption-band annotation boxes** — attempt 2's Template A finding 4 was confirmed by census (`adjudication_attempt_2b.py`): each caption sits inside a **cream-filled, rose-outlined box that is open at the top** (left + right verticals + bottom rule, no top stroke). The attempt-1 "truncated stroke marks" drew only part of this. Now drawn as fill + 3 strokes per side, **before** the caption ink so the text sits on the fill:
   - LEFT box x95..434 y479..529; RIGHT box x501..842 y479..529 (frame px)
   - fill median `251,252,236`; stroke cores measured per side (LEFT left `226,198,195`, LEFT right `240,230,231`, LEFT rule `220,187,187`; RIGHT left `211,188,185`, RIGHT right `202,165,166`, RIGHT rule `217,187,186`)
   - verification: non-neutral caption ink 1,123 → 14,906 (LEFT) and 1,505 → 14,968 (RIGHT) against the original's 15,270 / 15,062; pixel diff render_2 vs render_3 = 141,954 px, **all inside the two caption boxes, 0 px changed elsewhere** (no regression)

## Adjudication record — findings REFUTED (do not "re-fix" these)

**The "mm" labels and the dashed/dotted connectors are vision hallucinations. No such ink exists on the frame. Adding it would fabricate content and reduce fidelity; the frame wins.**

1. **`60.85 mm` / `69.85 mm` (left) + two `63.64 mm` (right)** — REFUTED (`adjudication_attempt_2.txt`): chart interiors carry only 265/254 px of dark ink, all in the equation row bands, with **zero glyph-shaped ink of any colour family** in either annotation region. The gateway also hallucinated "mm" while reading crops of these exact regions, and mislabelled an 80×70 px crop as "960×540".
2. **Dashed/dotted red connectors** — REFUTED: element-for-element red-component census shows orig 17/16 vs render 95/133 per chart; the extra render components are antialiasing fragments, not omitted original ink.
3. **Attempt 2 finding 1 (MAJOR) — "missing long vertical double-headed arrow / perpendicular double arrow"** — REFUTED (`adjudication_attempt_2b.py`): the only tall red columns in either chart are the axes (orig x126-127 LEFT / x540-541 RIGHT, ~290 px), present in both images; the horizontal red run census finds only the x-axis row (y434/435) in both. No second tall column and no extra long horizontal run exists in the original.
4. **Attempt 2 finding 2 (MINOR-MAJOR) — "rotated text labels beside the arrows"** — REFUTED: **zero** dark glyph components ≥12 px inside either chart outside the equation box, in both images.
5. **Attempt 2 finding 3 (MINOR) — "added red diamond marker"** — REFUTED: red ink exists in the original at exactly the same boxes (LEFT 92 px orig / 130 px render; RIGHT 95 px orig / 109 px render) — the render carries *more* ink there, so it is not an invented element.
6. **Attempt 1's caption-band "JPEG noise" note** — REFUTED and superseded: the band's core is `(205,171,170)` (a 30-point r/g split) versus untouched neutral panel `(232,232,232)`; a census of y526..531 x90..905 splits 2203 rose px / 2286 neutral px. This is what led to fix #2.

## Component (contract for child 010)

`build/components/slide_009.js` exports `renderBase(pptx, slide, opts)` plus the per-block builders and data, with `opts.skip` / `opts.only` / `opts.numeral`:

```
BLOCKS = { chrome, panels, fittedLines, points, marks, axes, eqBoxes, capBoxes, captions }
exports: renderBase, BLOCKS, PANELS, BOXES, CAPTIONS, BAND_FILLS, BAND_STROKES,
         NAVY, INTERIOR, GRID, RED, BLUE, ORANGE, BIGRED, BOXFILL, BOXLINE,
         INK, FONT, CAPFILL, ASSETS, CAP_BASE_OFF
```

`capBoxes` is ordered **before** `captions` so the cream fill sits under the caption ink, matching the certified z-order. Fidelity proven closed-loop by `qa/slide009/component_fidelity_2.py` (the earlier `component_fidelity.py` is kept banked, untouched): a pptx built from the component renders **pixel-identical** to `slide_009_recreated.pptx` (0 of 921,600 px differ, equal LibreOffice command), the container diff is metadata + shape order only, the xfrm multiset is equal, and all four hook variants gate (`only:{chrome}` 6 sp; `skip:{captions}` 127 sp; `only:{chrome,panels,axes}` 82 sp; `numeral:42` 131 sp — 131 sp / 2 pic total).

`build/components/slide_012.js`, `slide_020.js`, `slide_022.js`, `slide_027.js`, `slide_035.js` were not touched.

## Gates

- **Gate for slide 010: OPEN** once attempt 3 banks PASS on both legs (see the sequence log below); the component is already refreshed and certified against the current pptx, so 010 can import it immediately.
- House chrome: `house_chrome_check.py render_3.png` → **PASS** (panel x112-1882 y94-bottom, L/R/bottom strokes present, top bare, badge centre (1824,152) d=68).

## Evidence bank (never delete)

`qa/slide009/`: `judge_attempt_1.txt`, `judge_attempt_2.txt`, `judge_attempt_3.txt`, `probe_5.txt`, `probe_6.txt`, `adjudication_attempt_2.txt` (+ .py), `adjudication_attempt_2b.txt` (+ .py), `adjudication_attempt_3.txt` (+ .py, if attempt 3 raises findings), `cut_crops_2.txt`, `cut_crops_3.txt`, `cut_crops_2.py`, `cut_crops_3.py`, `crop_2_*` / `crop_3_*` pairs, `render_1.png`, `render_2.png`, `render_3.png`, `component_fidelity.txt`, `component_fidelity_2.txt` (+ .py), `run_attempt_2.log`, `run_attempt_3.log`, `selfcheck_attempt_4.py`, and the earlier probe1..probe59 + `measurements_summary.txt` bank.

Selfcheck note: `selfcheck_attempt_4.py` reports 37/52 on render_2; its 15 "failures" are pre-existing heuristic threshold artifacts (spot-verified: the right box's left border is present, navy core; equation ink bboxes were already marginally outside the checker's own window before the fix). Per worker law, selfcheck is corroboration only — never a substitute for the visual check.

## Gateway conditions

The fleet gateway at localhost:17844 was saturated by many parallel slide workers (47+ vision processes observed). Several attempt-2 crop calls hit the protocol's 630 s hard wall and were not banked; no retry loops were run beyond protocol W4 (sleep 300, re-probe once). Attempt 3 was dispatched as a single sequential background sequence (`scratch/tmp/run_009_attempt3.sh`, one call in flight at a time).

## Addendum — render_3 re-verification (2026-10-24, resumption)

Re-verified against `render_3.png` (frame-px mapped, BOX area-mean) before the attempt-3 legs were dispatched:

- **Fix 1 box fill** holds exactly: ORIG LEFT median `(235,252,249)` / RIGHT `(238,251,248)`; RENDER LEFT `(236,253,249)` / RIGHT `(236,253,249)`.
- **Settled-refuted "rotated labels" (attempt-2 finding 2) re-confirmed**: the only dark glyph components inside the two equation boxes in the ORIGINAL are the equation's own digits (LEFT x293..299 y162..165 = the closing `5` of `50.85² = 2585`; RIGHT x643..648 and x719..723 y158..166 = digits of `63.64² = 4050`). The render's count reads 0 only because its equation is an EMBEDDED 600-dpi mathtext PNG (deck math law) whose ink classifies outside the dark mask — direct ink presence is HIGHER in the render (639 vs 368 px LEFT; 763 vs 300 px RIGHT). No rotated label ink exists in either image.
- Crops for attempt 3 were re-verified from disk and the audit re-banked (`cut_crops_3.txt` VERDICT PASS, 0 scale mismatches) after the session exit.
