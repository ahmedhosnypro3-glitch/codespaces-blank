# Slide 050 — adjudication records (PIL-first, both images, 960x540 frame 1px=1pt)

Evidence: `unique_slides/slide_050.jpg` vs `qa/slide050/render_2.png` (Template A FAIL, judge_attempt_2.txt)
and `render_4.png` (post-fix). All measurements PIL/numpy; scale = H_render/540 = 2.0833.

## judge_attempt_2.txt findings

### Finding 1 — OMITTED EXPLANATORY KEY LINE (BLOCKER, MEDIUM-HIGH) → CONFIRMED, FIXED
Claim: IMG2 prints beside the Initial-W block a caption assigning class colours /
rejection status, read as "C1 positive / C2 negative / Z0 is unaccepted"; IMG1 omits it.

PIL adjudication:
- Original L4 band x240..510 y110..124 carries dense handwriting (269 px wide, ~36 glyphs);
  the region is EMPTY of any corresponding element in render_2 except a placeholder
  "(0,0) (7,6) (3,2)" line at x266..466 y112..125.
- Vision transcription of the L4 band (banked `orig_l4_caption_transcript.txt`, gate
  analysis mode, 4x LANCZOS crop of frame px x245..515 y105..128):
  **"C1 positive  C2 negative  Zero is unaccepted"** with per-word confidence 0.93-0.99.
- Colour measurements of the L4 band: "C1" RED (x240..253, 61/61 ink px red),
  "Zero" GREEN (x394..423, 183/183 ink px green — matches the 236 green px found by a
  whole-frame green scan of x240..730 y45..135), "is unaccepted" BLACK (0 saturated px);
  "C2" BLUE.
- The build therefore OMITTED a renderable text element → BLOCKER confirmed.

Fix applied (build/slide_050.js): the L4 placeholder line was replaced by
"C1 positive   C2 negative   Zero is unaccepted" at x=240 y=106 w=280 h=20, fontSize 13,
with C1 red / C2 blue / Zero green / remainder black.

### Finding 2 — inconsistent vector formatting in the "Check classes" cluster (MINOR) → FIXED BY RELOCATION
Claim: Z1=(0,0) rendered inline while Z2/Z3 stacked.

PIL: all three Z images are the same mathtext 2D construct
(`\left( \substack{a\\b} \right)`, sidecars eq_050_Z{1,2,3}.json: 19.4x21.6,
19.3x21.2, 19.3x21.5 frame px). The perceived difference came from the OLD positions
(x322/432/542, pitch ~110) which did not match the frame.

Measured original Z mini-table (faint-ink threshold, sum<726):
label x641..656 / x664..678 / x684..702 at y74..85; vector x640..658 / x663..680 /
x684..702 at y86..120 (pitch 23). Glyph reading at 1px resolution of the digit rows:
top row 0,7,3 and bottom row 0,6,2 → Z1=(0,0), Z2=(7,6), Z3=(3,2) (matches
analysis/slide_050_final.json and sibling slide 047's certified mini-table).

Fix: labels moved to y=74 and images to y=86 at x=641/664/686 (label + vector stacked
per column as measured).

### Finding 3 — top-band container styling (MINOR, LOW) → REFUTED
Claim: IMG1 unifies table + math zone into one cream box with a heavy dark-red border,
while IMG2 keeps the table in a thinner bordered cell with a bluish header strip.

PIL: horizontal colour scan of the ORIGINAL at y=100 shows the cream fill (≈254,255,232)
running CONTINUOUSLY from x75 to x714 with NO divider and NO sub-box; the only vertical
strokes are the navy border columns x69..72 and x717..720. Vertical scan at x=400: navy
box top border y54..57 and bottom y128..131, cream fill y58..127.
Border colours: original (34,27,107) = navy; render (30,26,118) = navy. No dark-red
border exists in either image. → REFUTED (no content loss, no deviation).

## Self-check FAIL adjudication (render_3/render_4)

`selfcheck_a_render4.txt` reports one FAIL: "left of chart, red-box zone"
(x60..310 y173..276: orig 769 ink px, render 3260). Excess bbox x97..218 y173..243.

PIL proves this is a MEDIUM difference (typed vs handwritten ink weight), not a content
defect:
- Row bands align: title y148..160 vs y149..158; header y166..176 vs y168..177;
  vector rows y184..223 (3 rows) vs y182..207+214..223; class row y232..240 vs y233..243.
- 6 cell columns per row at the same ~22 px pitch in both images (cell-centre lists
  match on every row).
- Class-row colours match exactly: C1 column orig red=31/blue=0, render red=113/blue=0;
  C2 column orig red=0/blue=32, render red=0/blue=114.
- The excess ink is ~4x heavier typed glyphs on faint handwriting → GROUND RULE (c).

## Additional PIL-found defect fixed (not judge-raised)

render_2 wrapped the caption-box title "Augmented Vectors (from Top)" into TWO lines
(bands y137..149 + y156..164) while the original has ONE line (y148..157, x81..236).
Fixed by fontSize 12 → 10 (fits x82..237 inside the caption box); render_4 now shows a
single band y149..158. The founder's analysis JSON spells the caption "Ugmented"
(verbatim OCR); the vision probe and the Template A judge both read "Augmented", and the
build keeps "Augmented" (2 vision reads vs 1 OCR drop).

## Attempt 5 adjudication (w050-finish-20261024, 2026-10-24)

Template A on render_5 (judge_attempt_5.txt): FAIL — 2 BLOCKERs + 2 MINORs.
Adjudicated PIL-first against unique_slides/slide_050.jpg (960x540, 1px=1pt).

### Finding 1 — W vector truncated (BLOCKER, high) → CONFIRMED, FIXED
Claim: original pink box shows W = (5, −1, −1) (3 components); render shows (5, −1).
PIL: original construct ink x744..821 y69..133 (65pt tall — the sibling Initial-W
2-component stack measures only y59..83 = 24pt, so ~3 lines); three digit sub-bands
in the row profile (y69..88 / y90..108 / y119..135). Render_5: single 21pt construct
(y96..117) + underline y119.6. Vision transcription of the original pink-box crop
(orig_finalW_transcript.txt): "w̲ = ( 5 / −1 / −1 )" — three components verbatim.
The analysis JSON's 2-component read is wrong vs the frame; the image is ground truth.
Fix: eq_050_finalW.png re-rendered as the 3-component mathtext stack (600x308 px
@600dpi = 72x37pt), sidecar rewritten to disk. NOTE: render_eq.py only PRINTS
sidecars — a stale sidecar (557x215) silently squeezed the new PNG into the old
2-component box on the first rebuild (measured: construct compressed to ~70% height);
with the sidecar written, render_6 shows the construct undistorted at x746..815
y70..105, top edge within 1pt of the original's y69. Placed x=744 y=69 (top-matched).

### Finding 2 — "η = 1" missing (BLOCKER, high) → REFUTED (the original has no η text)
Claim: the original reads "REPEAT using Step η = 1"; the render omits the η = 1.
PIL (thr 450/600/726 + a full ASCII luminance map of x415..660 y56..90):
- "REPEAT using Step" red ink x415..537 y59..77.
- The zone right of it (x538..645 y58..77) is BLANK CREAM: luminance histogram
  uniform L=251/252 (1954 of 2053 px; zero ink at any threshold). The only ink in the
  wider band: the Z1/Z2/Z3 label columns (x645/667/689) and the navy box border.
- Two vision transcriptions read "η = 1" (one primed, one neutral on a 3x-upscaled
  crop) — both are phrase-completion hallucinations; uniform cream refutes them.
  "Never fix a defect the original does not have" → do NOT add η = 1 to the render.
- The prior lane's "η = 1" PNG (blue) sits on the Initial-W stack's "−2" denominator
  (black ink x267..330 y74..89 — transcribed as the vector's second entry), and its
  color was doubly wrong: render_eq.py passes "C00000" to matplotlib, which parses it
  as cycle index C0+0000 → tab:blue (31,119,180), verified from the PNG's ink.
Fix: the eta image is REMOVED from the build (an extra element the original does not
have, overlapping the construct's denominator); the stack's own "−2" now shows clean.

### Finding 3 — extra class label, six vs five (MINOR, med-high) → REFUTED
PIL: the original's class rows carry SIX C-label clusters at 22.6px pitch
(x90..101 / 113..124 / 135..146 / 157..169 / 180..192 / 203..214) in both tables,
identical to the render's six labels per table (the table has six columns x1..x6).
The original shows six; no change.

### Finding 4 — cursor artifact reproduced (MINOR, med) → CONFIRMED (ground rule c), FIXED
A lone black "+" at x233..241 y414..419 (empty left margin, no semantic role) is a
video-capture cursor; ground rule (c) mandates omission. Fix: removed from the build.

### render_6 verification (this lane, before judging)
house_chrome_6.txt PASS; caption band still red/blue/green/black
(verify_l4_caption_6.txt); former eta zone blue px = 0; former plus-zone ink = 0;
finalW = three components inside the pink box; Initial-W denominator visible;
chrome/containment unaffected.
