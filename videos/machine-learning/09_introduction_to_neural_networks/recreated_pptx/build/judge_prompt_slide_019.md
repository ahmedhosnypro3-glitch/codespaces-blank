# COMPARISON JUDGE — slide_019

## MODE
Comparison judge. Image 1 = ORIGINAL frame (source of truth). Image 2 = RENDERED recreation (must match).

## GROUND RULES (must acknowledge first)

(a) INTENTIONAL HOUSE CHROME OVERRIDES: The recreated slide uses the project's mandatory house frame template (red frame 0.15in inset, yellow badge "19" at 12.48/0.30, title at y=0.28). These override the original's frame/badge/title positions exactly per AGENTS.md. DO NOT charge discrepancies on these elements.

(b) EQUATION FORMAT UPGRADE: All equations rendered in Professional Format (2D stacked fractions, proper superscripts) via matplotlib mathtext → PNG 600dpi. This is an e-format upgrade, not a discrepancy.

(c) CAPTURE ARTIFACTS OMITTED: The original frame has a screen-recording toast "[?]nment has just been saved..." at bottom-left (clipped) and a black letterbox strip at the very bottom. These are capture artifacts, NOT slide content. The recreation correctly omits them. DO NOT charge their absence.

(d) TYPED VS HANDWRITTEN: The original's formula captions appear hand-drawn/serif-italic; the recreation uses typeset mathtext PNGs. This is at most MINOR.

(e) GRAPH GENERATION: The 4 activation function plots (sigmoid, tanh, tan, arctan) are generated from the same mathematical functions (numpy/scipy + matplotlib) on the same domains as the lecture topic. The recreation uses programmatic plots, not hand-traced curves. Minor rendering differences (anti-aliasing, line weight) are expected.

(f) VERDICT IS ABOUT FIDELITY OF RENDERABLE CONTENT ONLY.

## VIEW
Slide 19 from "Introduction to Neural Networks" lecture. A 2×2 grid of activation function graphs: top-left sigmoid, top-right tanh, bottom-left tan, bottom-right arctan. Each has a formula caption below. A red block arrow connects the tan and arctan panels. Yellow badge "19" at top-right. Red outer frame. Light gray background.

## CAPTURE
Image 1 (ORIGINAL): slide_019.jpg, 960×540, video frame capture, JPEG.
Image 2 (RECREATED): slide_019_rendered-1.png, 2001×1125, LibreOffice headless render → pdftoppm 150dpi, PNG.

## FACTS (measured from original frame, 960×540, 1px=1pt)

House frame: dark red (#C00000), 0.15in inset from all edges, 1.5pt line, no fill.
Badge: yellow (#FFFF99) circle at ~x=89%-93%, y=10%-17%, black "19" inside.
Title position: house rule y=0.28in (recreation adds inferred title; original has no title band).

Panels (blue #0000CC border, ~1.5pt, light gray #D9D9D9 bg):
- Sigmoid (TL): x≈11%-43%, y≈11%-44%. Red curve (#E06666). X:-8..8, Y:0..1. Legend "sig(x)=1/(1+e^-x)". Y-label "sig(x)".
- Tanh (TR): x≈52%-84%, y≈11%-44%. Red curve. X:-4,-2,2,4. Y:-1..1. Y-label "tanh x".
- Tan (BL): x≈11%-43%, y≈55%-88%. Gray curve (#A6A6A6). X:-2π..2π (labels -2π,-3π/2,-π,-π/2,π/2,π,3π/2,2π). Y:4,2,-2,-4. Y-label "tan x". 4 dashed red asymptotes at -3π/2,-π/2,π/2,3π/2.
- Arctan (BR): x≈52%-84%, y≈55%-88%. Red curve. X:-3..3. Y:-1,1. Title "Inverse Tangent Graph" upper-left. Origin marker at (0,0).

Captions (rounded rectangles):
- Sigmoid: peach #FCE4D6 fill, red #C00000 serif-italic text, "f(x) = Sigmoid(x) = 1/(1+e^{-x})" (stacked fraction).
- Tanh: peach fill, red text, "f(x) = tanh(x) = sinh x / cosh x" (stacked fraction).
- Tan: gray #D9D9D9 fill, black text, "f(x) = tan(x)".
- Arctan: peach fill, red text, "f(x) = tan^{-1}(x)" (superscript -1).

Arrow: hollow red (#C00000 outline, white fill) right-pointing block arrow between bottom panels, centered vertically ~y=69%-73%.

Capture artifacts (OMIT in recreation): gray toast "[?]nment has just been saved..." at bottom-left (clipped), black letterbox strip at bottom edge.

## INSTRUCTIONS

Inspect Image 2 against Image 1 using the ground rules above. For each region, note:
- PRESENT/ABSENT (is the element rendered?)
- POSITION match (within ~4px at 150dpi ≈ 0.027in tolerance)
- COLOR match (hex proximity)
- TEXT content match (verbatim for equations, labels, ticks)
- SHAPE fidelity (curves, asymptotes, arrow style)

List discrepancies with SEVERITY (BLOCKER/MAJOR/MINOR) and CONFIDENCE (HIGH/MEDIUM/LOW).

End with exactly one terminal verdict line:
FINAL VERDICT: PASS|FAIL for 'slide_019 recreation fidelity'