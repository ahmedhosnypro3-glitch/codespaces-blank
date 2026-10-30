# Adjudication — Template B ALG crop leg on render_7 (crop_7_alg_judge.txt)

Claim: w26-r3-20261021T0538, attempt 7.
Verdict: **PASS** — no BLOCKER/MAJOR. One MINOR finding (high confidence), **PIL-REFUTED**.

## F1 (MINOR, high confidence) — "IMG1 adds an underline under 'Random Weights' on the
first numbered line; IMG2 shows the same phrase WITHOUT that underline"
REFUTED on three independent grounds (evidence: probe_rowA_underline.out, probe_a7_bars2.out):

1. **The build cannot draw it.** The banked pptx's slide1.xml contains exactly six
   underlined runs — 'moving along the direction of ', 'negative gradient', 'gradient is ',
   'almost zero', 'approximately', 'variable number of steps'. "Random Weights (W)" is not
   among them, and build/slide_026.js's rowA runs carry no `underline` flag.
2. **No bar exists in either image in the rowA underline position** (baseline 156, so
   y157..162; identical predicate, runs >= 8 frame px, thr 430): ORIGINAL nothing at all;
   RENDER_7 only one 8px run at y158 x400..407 — a paren bottom (the original shows the
   same class of faint paren-bottom pixels at y158..161: n9/11/8/5). A real underline bar
   in this deck is a CONTINUOUS 100-190 frame-px run (measured bars: rowB x349..716,
   rowD x287..473, N3 x177..277 and x539..727); nothing of that size exists in the band.
3. **The cited crop region contains no horizontal stroke.** The judge cited crop-relative
   x0.26..0.56, y0.08..0.10 (= frame x~324..538, y~146..148 — mid-glyph, not below the
   baseline). Scanning the cited box (widened to x0.20..0.62, y0.05..0.16) in BOTH crops:
   the widest horizontal run anywhere in it is 28 crop px (13 frame px = a glyph stem) in
   the render and 26 crop px in the original; a bar here would measure ~200-400 crop px.
   Neither image has one.

Note for the record: attempt 6's alg-crop judge read the OPPOSITE (it listed a
'Random Weights' bar as "present, continuous, and correctly positioned"). Two vision reads
contradict each other; the pixels decide, and neither image has the bar. The render agrees
with the original: no underline on rowA. No build change.
