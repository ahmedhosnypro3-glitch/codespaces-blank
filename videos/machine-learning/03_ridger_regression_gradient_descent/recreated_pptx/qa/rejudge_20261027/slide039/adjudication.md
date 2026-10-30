# Adjudication — rejudge_20261027 slide039 FULL FAIL (2026-10-30, read-only)

FAIL transcript adjudicated: `judge_full_retry.txt` (banked 2026-10-30 00:21, winner `images` round 1 —
`judge_full.log` is 0 bytes and `result.txt` FULL=NORESULT points at a `judge_full.txt` that was never
written; `driver_S039.out` shows the driver died on a grep miss + syntax error, so the retry transcript
is the only banked full-leg verdict). CROP leg `crop_dense_judge.txt` = PASS (6 MINORs).

Images: `render.png` 2001x1125 (150dpi, scale 2.0833/2.0844 vs 960x540) vs
`unique_slides/slide_039.jpg`. House chrome gate: `chrome_check.txt` PASS.
Equation asset: `build/assets/eq_039_main.json` (rel_id rId2, mathtext
`W^{(updated)}=W^{old}-\eta\,\delta_{i}\,X_{i}`, 17pt, color 000000, 600dpi, w 2.7933in @ x5.084 y3.807);
`slide_039_recreated.pptx` `ppt/slides/slide1.xml` carries the OMML wrap (mc:AlternateContent + oMath),
so the LO render shows the certified PNG fallback (black ink) — consistent with measurements below.
All coordinates below are SLIDE-SPACE px (960x540); colors are median core ink of dark pixels
(sum<450) unless noted. Method: rejudge_adjudicate.py + targeted PIL measurements, original upscaled
2.0833x LANCZOS for comparison.

## Per-claim dispositions

| # | Claim (severity/confidence as filed) | Disposition | Measurements |
|---|---|---|---|
| 1 | Title line-break shift: recreation wraps after "and", original after "SGD)" (MAJOR/High) | **REFUTED** | Both images have exactly 2 title bands (orig y62.2/108.3, render y64.1/109.7). L1 ink ends x839 orig / x834 render (final glyph ")"); L2 starts x279 orig / x281 render with "and". No third band, no ink after ")" on L1 (render x836-860 dark px = 127, all badge edge, not text). Break identical: after "SGD)". |
| 2 | Title color: original L2 all blue, recreation "Gradient Descent" dark red (MAJOR/High) | **REFUTED** | Original L2 is itself 3 runs: "and" core (161,40,53) red, "Mini-Batch" core (25,17,137) navy blue, "Gradient Descent" core (158,40,53) RED. Render: (192,0,0) / (88,76,168)=584CA8 / (192,0,0). Same red/blue/red scheme in both. Residual: blue-run hue navy→violet — MINOR hue shift (also flagged MINOR by crop leg). |
| 3 | Equation box white/neutral + thin dark border, caption green (MAJOR/Med-High) | **REFUTED** | Box fill orig (223,255,238) vs render (225,255,239) — both light green (E1FFEF family), not white. Border orig green-family (121-197,154-234,101-181, JPEG) vs render (89,129,76)=59814C — both green, not dark. Caption "Repeat for ALL misclassified Samples" (x605-841 y279-292): orig core (167,64,69) RED, render (192,5,4) RED — not green. Side note: orig equation ink has 484 red px (x493-563, right side) + 1086 green px vs render all-black (eq color 000000) — that is the crop leg's MINOR #2 (typed-vs-ink), not this claim. |
| 4 | "usually more efficient" / "converges faster" blue+underlined in original, plain black in recreation (MAJOR/Med-High) | **REFUTED** | Orig B4 (x101-402 y337-346) core (84,84,84), B5 (x101-336 y363-371) core (80,81,80) — dark gray/black. Zero blue-classified ink px in orig why-block text zone (x94-700 y330-380); below-text bands hold only 32/65 px descender artifacts (x206-211 / x195-204), no underline strokes. Render bullets plain black (0,0,0). Match; build's frame-measured black over the analysis's "efficient red" guess is corroborated. |
| 5 | "GD and SGD" bold black in original, blue-purple in recreation (MAJOR/High) | **REFUTED** | Caption L1 x347-454 ("GD and SGD"): orig core (151,54,67) RED (same as first words (153,57,68)), render (192,0,0) RED — not blue-purple. L1 remainder x460-832 black in both; L2 black in both. Blue caption line: orig (55,43,159) vs render (88,76,168) — hue nuance only. |
| 6 | Double space in original "gradient  of the Error", single in recreation (MINOR/Medium) | **CONFIRMED (MINOR)** | Orig word gap "gradient"→"of": x740.5→751.6 = 11.03px ≈ 2x normal word gap (5.3-6.7px elsewhere on the line); render gap x733.8→739.6 = 5.76px (single space, matching verbatim analysis text). Advisory only; no reopen trigger. |
| 7 | Title/body slightly heavier/larger in recreation (MINOR/Low-Med) | **REFUTED** | Glyph row extents (slide-space): title L1 orig 61.9-102.7 vs render 63.8-104.1 (~0.5px); L2 19.7px vs 19.7px; B1 18.2 vs 17.3px; caption L1 18.2 vs 17.3px. All within ≤1px; render is marginally smaller if anything — opposite direction of the claim. |

## Whole-frame PIL context

rejudge_adjudicate.py --full: 309,464 diff px (13.75% of frame) concentrated in text bands
(densest cells: title L2 x312-672 y112-135; bullets x312-336 y180-225; caption x528-552 y405-427) —
all anti-aliasing/hue zones, no missing-content blocks. Ink-only-in-original excess (147,518 vs 67,543
render) is JPEG noise + handwritten-ink AA, not absent elements; every original element has a render
counterpart at the measured positions.

## Vision re-read leg

Skipped (optional per task): gate saturated — `pgrep -c -f analyze_image.py` = 28 (all slide014 fleet
calls in flight), precondition `< 8` unmet; adding a call would saturate the fleet-global gateway.
PIL adjudication above is decisive for all 7 claims.

## Disposition

FULL FAIL **DISMISSED** per register rule (vision claims refuted by pixels are dismissed): 6 of 7
claims REFUTED, 1 MINOR CONFIRMED (double space, advisory). No BLOCKER/MAJOR survives. CROP leg was
PASS. Slide 039 remains certified; **no reopen, no fixes** (adjudication-only task). No edits to
builds/pptx/DB; no git.
