# Defect patterns — 08_performance_measure (from 19 judge transcripts, 2026-10-28)

Generated pattern map: judge natural-language findings -> fix recipes + pre-judge checks.
Sources: recreated_pptx/qa/slide*/judge_attempt_*.txt (all attempts).

## Pattern A — illustrative imagery substituted (slides 2, 20)
The originals use hand-drawn airplane sketches per class; builders substitute generic
dart/rocket glyphs or shapes.
Fix: generate the sketch set in-house (graphgen-style asset script) OR copy measured
geometry from the original frame with PIL; never invent a lookalike.
Pre-judge check: crop each imagery region and vision-compare shape+scale vs original.

## Pattern B — diagram type replaced (slide 20 activation-function panel)
Original: circle containing cross-axes at panel right. Builders drew a bare S-curve.
Fix: PIL-measure the original's diagram bbox, then draw the EXACT type (shape, fill,
stroke); a "similar" diagram is a MAJOR mismatch.

## Pattern C — panel borders/fills dropped (slides 11, 20)
Enclosing rectangles (e.g. blue-outlined block, light-blue class panel) are lost.
Fix: extract every enclosing rect from the original (position+line+fill) before build;
treat as first-class elements, not decoration.

## Pattern D — color coding lost (slide 20)
Three-line color scheme (blue/blue/bold-red) flattened to one color.
Fix: per-string color map from the fresh image-analysis transcript (section 4 COLORS).

## Pattern E — slide-number badge clipped/wrong (slide 19)
Badge printed "9" for original 19; or title bar overlaps badge left half.
Fix: house rule: badge x12.48 w0.5 at 18pt bold — shrink font or shorten so the FULL
numeral fits; never extend a title bar past x12.48.
Pre-judge check: crop badge, OCR/vision-read the numeral, compare with original.

## Pattern F — flow arrows reversed / panels re-ordered (slides 19, 20)
Diagram edge directions and panel ordering deviate from the original.
Fix: transcribe arrows as A->B pairs from fresh analysis (section 3 DIAGRAMS) and
assert direction at build; verify each arrow start/end box labels match original.

## Pattern G — panel overflow (slide 20)
Flowchart elements spill outside their enclosing panel.
Fix: PIL-measure each original panel's inner bounds; clamp child bounds to them with
margin; run frame-containment check (pre-judge) on every panel, not just house frame.

## Pattern H — textual/line metrics drift (general, from founder directives in template)
Inter-line spacing, vertical centering inside delimiters, legend sizes/gaps, label-value
alignment. Fix: measure the original's text metrics with PIL/vision before writing sizes.
