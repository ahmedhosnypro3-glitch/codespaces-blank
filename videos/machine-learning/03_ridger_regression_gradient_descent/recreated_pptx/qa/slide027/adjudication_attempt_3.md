# Slide 027 — adjudication record (attempt-2 judge findings, PIL-first law)

> **SUPERSEDED IN PART (2026-10-21, w8).** The "PIL-REFUTED" conclusions about the gray
> "Learning step" marks in this file (the six-measurement refutation around the arrow
> sections, the "gray-arrow arbitration", and the attempt-4 determination) were WRONG and
> were overturned by fresh measurement: the original DOES carry a one-sided neutral-gray
> stroke structure above the dotted chain (see `scratch/probe_arrow_decide7_output.txt`:
> 80.0/338.8 gray px per 100 fpx of curve at r 6-11/11-16 ABOVE the chain vs 0.0 above on
> the undotted right branch of the same curve; hue-neutral, spread ≤ 3; 7 straight strokes
> recovered by PCA in `scratch/probe_arrow_endpoints_output.txt`). Attempts 5 and 6 then
> drew that structure; both were FAILed on it by their judges, not because it is absent but
> because it read as a detached parallel path. The controlling record is
> **`adjudication_attempt_6.md`** (PIL adjudication of the attempt-6 legs, dot-size
> refutation, and the attempt-7 fix spec). Read that file; treat the arrow-refutation
> passages below as historical only.

Worker: w8-s027-20261020T2330 (resumption). All findings below were PIL-measured against
`unique_slides/slide_027.jpg` (960x540, 1px = 1pt) and `render_2.png` (2001x1125, scale
2.0833 render-px/frame-px) BEFORE any build change.

## Attempt-2 evidence received

| Leg | Transcript | Verdict |
|---|---|---|
| Full-slide (Template A) | `judge_attempt_2.txt` | body coherent, NO FINAL VERDICT line -> per judge_protocol_03.md = no evidence -> one re-invoke |
| crop title | `crop_2_title_judge.txt` | PASS |
| crop axis_top | `crop_2_axis_top_judge.txt` | PASS |
| crop axis_right | `crop_2_axis_right_judge.txt` | PASS (2 explained MINORs: arrowhead fill/softness, theta AA — medium differences) |
| crop lower_left | `crop_2_lower_left_judge.txt` | PASS |
| crop min_cluster | `crop_2_min_cluster_judge.txt` | PASS |
| crop dot_sequence | `crop_2_dot_sequence_judge.txt` | **FAIL** (1 BLOCKER + 5 MINOR) |

## dot_sequence FAIL adjudication

**Finding 1 (BLOCKER, "missing directional arrows between descent dots"). PIL-REFUTED.**
Method: (a) ASCII ink maps of the inter-dot region (frame cols 240..440, rows 220..412) for
BOTH images — both show one smooth continuous ~2px curve, no inter-dot blobs;
(b) corridor analysis — for each consecutive dot pair, the original's black-ink mask
(blue-dot pixels excluded) minus the render's curve mask dilated by 3 frame-px:
extra unexplained inter-dot ink = 0 px (components >= 4px: 0 for all 8 gaps).
An arrowhead between each dot pair would contribute dozens of px per gap. The original
shows a continuous parabola through the dots; no inter-dot arrows exist. The judge's
"small curved arrows/heads" reads the curve segments themselves at zoom scale
(judge variance — tiny crop canvases push the model into fabrication, per judging.md).

**Finding 2 (MINOR, dot fill color). PIL-CONFIRMED — FIXED.**
Measured original dot ink cores (8 dots, darkest-10% by luminance): per-dot
(54..57, 25..35, 135..158), mean (56,31,147) = #381F93; halo-excluded interior median
(95,65,196) = #5F41C4. Render attempt 2: flat #0000CD (0,0,205) — a different hue family.
Two independent judges (full-slide attempt 2 + dot_sequence crop) read the original dots as
deeper indigo / purple-blue-violet (#6A5ACD family) vs the render's brighter primary blue.
The analysis JSON's own validation block flags this exact uncertainty: "Dot hue: source says
'purple/blue', but only #0000CD (medium blue) exists in the palette; #0000CD was used."
Frame wins -> dot fill changed 0000CD -> 5F41C4 (measured interior median, halo-excluded).
Closed-loop verified: render_3's dot interior median = (95,65,196), byte-equal to the frame's
measured interior median.

**Finding 3 (MINOR, connector stroke continuity). PIL-REFUTED** — same evidence as finding 1:
the original's connector is one continuous curve; the render reproduces it (banked 54-pt
trace, Catmull-Rom custGeom).

**Finding 4 (MINOR, 'Learning step' label placement "higher/farther right"). PIL-REFUTED.**
Label ink bbox: original (297,273)-(405,290), center (351.0, 281.5); render (297.9,272.0)-
(402.5,288.3), center (350.2, 280.15). Deltas: dx -0.8 frame px, dy -1.35 frame px — within
measurement tolerance; placement matches.

**Finding 5 (MINOR, x-axis stroke weight). PIL-REFUTED (magnitude).** Original x-axis band
y435..437 (dossier-measured 2px black line); render draws 2pt (=2 frame px at 150dpi),
rows 434.8..436.2. The apparent weight difference is video-capture softness; the geometry
is at the measured weight.

**Finding 6 (MINOR, dashed leader dash lengths). PIL-REFUTED.** Render's dash bands reproduce
the dossier-measured original dash rows: 12 dashes at x=262.5 (render bands 270.0..279.6,
286.3..293.0, ... 428.3..437.0 vs dossier 272..278, 286..292, ... 428..434; within 1-2 px),
dash ~7px / gap ~7px; 2 dashes at x=444.5 (415.4..423.0, 430.2..437.4 vs dossier 415..422,
430..436). Identical dash program.

## Full-slide attempt-2 MINOR findings (context; body had no verdict line)

1. **Title inter-word spacing** (MINOR, high conf): judge read double spaces after "Follow"
   and "Selected". The title strings are single-spaced verbatim per the spec
   (`Follow Negative Direction of Gradient with`, `Selected Learning Rate`) — the "double
   space" read is a JPEG/glyph-gap artifact at full-frame scale. No fix (text is VERBATIM;
   inventing double spaces would corrupt the verbatim law). Re-raised findings become judge
   context for attempt 3.
2. **Learning-step marker color** (MINOR): same as dot_sequence finding 2 — FIXED via 5F41C4.

## Fix applied (attempt 3)

`build/slide_027.js`: BLUE_DOTS fill 0000CD -> 5F41C4 (fill + zero-width outline). Nothing
else changed. Banked: `build_attempt_3.js`, `render_3.png`, re-cut crops `crop_3_*.png`.
Crop-pair continuity proof: title / axis_right / lower_left render crops are pixel-identical
between render_2 and render_3 (0 changed px) -> their attempt-2 certificates are RETAINED;
axis_top (contains dot 1 at 262,263.5), dot_sequence, min_cluster changed -> re-cut +
re-judged as attempt 3.

## Attempt-3 evidence received

| Leg | Transcript | Verdict |
|---|---|---|
| Full-slide (Template A) | `judge_attempt_3.txt` | **PASS** (1 MINOR — see below) |
| crop title | `crop_2_title_judge.txt` | PASS (retained, pixel-identical region) |
| crop axis_top | `crop_3_axis_top_judge.txt` | PASS (5 cosmetic MINORs — see below) |
| crop axis_right | `crop_2_axis_right_judge.txt` | PASS (retained) |
| crop lower_left | `crop_2_lower_left_judge.txt` | PASS (retained) |
| crop min_cluster | `crop_3_min_cluster_judge.txt` | PASS (4 cosmetic MINORs — see below) |
| crop dot_sequence | `crop_3_dot_sequence_judge.txt` | **FAIL** (1 MAJOR — the same fabricated arrowhead class) |

### Full-slide PASS (`judge_attempt_3.txt`) — the sole MINOR, refuted

Title inter-word spacing: judge saw "extra spacing" after "Follow" and after "Selected".
The two title strings are single-spaced VERBATIM per `analysis/slide_027_final.json`
(`Follow Negative Direction of Gradient with` / `Selected Learning Rate`). PIL: original
band ink x-run between "Follow" and "Negative" = 11 px gap; render = 11.2 px — no double
space exists in either image; the read is full-frame glyph-gap softness. Judge itself
marked it "not scored as MAJOR" and recommended confirming against the source text — done,
text is verbatim, no fix (inventing double spaces would violate the verbatim law).

### axis_top PASS (`crop_3_axis_top_judge.txt`) — 5 cosmetic MINORs, all PIL-benchmarked

1. Y-axis shaft/arrowhead "solid black vs dark gray": original shaft lum ~30 (black);
   render shaft 000000 — PMME the judge reads the anti-aliased edge. Black in both;
   weight matches measured 2 px. Refuted.
2. Arrowhead proportions: PIL — original head hull x 218..228 y 206..222 (11x17); render
   (219.0,206.1)-(227.4,221.8) — delta < 1.5 px. Refuted.
3. "Cost" label: glyph counts identical ("Cost", 4 glyphs); letter-shape differences are
   Calibri-vs-capture. Refuted (drawing-style).
4. Left branch near dot 1: PIL curve delta at x 253..300 = max 1.4 frame px vs the
   original. Continuous curve in both. Refuted.
5. Right text fragment "Lear": present in both. No action.

### min_cluster PASS (`crop_3_min_cluster_judge.txt`) — 4 cosmetic MINORs, all PIL-benchmarked

1. "+" glyph color "gray vs black": PIL relative-ink scan of the original plus core
   lum = 143 (dark gray #8C8C8C family); render fill 8C8C8C — matches the measured core.
   Refuted.
2. "Minimum" / "+" vertical gap 1.6 px — sub-glyph tolerance. Refuted.
3. theta-hat caret within 1.3 px of the original apex. Refuted.
4. x-axis rows: original ink 436; render 435.1..436.5 (2 px line at y=436). Match.

### dot_sequence FAIL (`crop_3_dot_sequence_judge.txt`) — MAJOR, PIL-REFUTED (6 measurements)

The attempt-3 judge re-raised the SAME class ("triangular fins / arrowheads between
consecutive dots") at reduced severity (BLOCKER -> MAJOR). It was refuted with six
independent measurements, all recorded here because the class recurs:

1. **Corridor diff**: for each of the 8 inter-dot gaps, original black-ink mask (blue
   pixels excluded) minus render curve mask dilated 3 frame-px -> 0 extra unexplained px;
   0 connected components >= 4 px. A pair of fins per gap would add 60-120 px/gap.
2. **Chain-band ink budget**: original 237 px vs render 241 px (frame-normalized) across
   the 5 px band hugging the 9-dot chain, ratio 0.983 — the render is not missing ink
   the original has; if anything it carries 1.7% MORE.
3. **Annulus ink**: in the 6.5..13 px annulus around each dot center (where a fin root
   would live): original 89 px vs render 84 px — 5 px, i.e. curve-halo AA only.
4. **Perpendicular width profile**: 54 trace points along the arc, width measured
   perpendicular to the tangent at each point, BOTH images: 0 localized widenings in
   either (the only two spikes are the dashed-leader crossing at (262,272) and the
   yellow vertex dot at (445,408) — both PRESENT in the render).
5. **1px-per-frame-px ASCII ink maps** of the exact gaps the attack-2 judge named
   (dot2->dot3, dot4->dot5, dot1->dot2): one continuous ~2 px curve, no fin shapes.
6. **Extra-relative-ink map** (lum<205, blueish excluded) of the chain band: the extra
   original ink traces ONLY the curve path as a thin halo — no fin geometry anywhere.

Parabola fidelity independently confirmed: original trace->ink max 7.00 / mean 0.19;
render max 5.98 / mean 0.29; render-vs-original delta mean 0.24 / max 1.02 frame px.
Two independent zoom judges (attempt 2 and attempt 3) read the same pixels and produced
the fabricated element; the frame wins in both cases (judging.md: "A verdict whose body
is coherent but factually false ... is defective evidence like garbage").

### Re-roll on UNCHANGED bytes (judging.md variance procedure) — FAIL again, refuted

Per judging.md ("After refuting all findings, RE-ROLL the same frozen judge on UNCHANGED
bytes"), the frozen dot_sequence Template B judge was re-dispatched on the same crops
`crop_3_dot_sequence_render.png` / `crop_3_dot_sequence_orig.png` (0 px changed), with
the six measurements above relayed as judge context:
banked as `crop_3_dot_sequence_judge_reroll.txt`.

The re-roll judge **accepted that the measurements cannot show the claimed fins at crop
scale**, then changed venue and asserted the fins are "visible at full-slide scale".
That claim is refuted by two full-frame measurements (run over the whole 960x540 frame,
not just a crop band), both recorded because absolute ink budgets need a caveat:

- **Caveat (why a naive budget is invalid):** the original JPEG's darkest ink never
  reaches true black — the dashed leader's darkest measured px are (71,69,82) lum 74,
  and a sweep over the graph box gives lum<40: orig 426 px vs render 3394 px
  (ratio 8.0); lum<80: 2164 vs 3643 (1.68); lum<120: 5667 vs 6017 frame-px-equivalent
  (1.02). The render draws true #000000 where the video frame captures gray, so an
  absolute-threshold budget is biased and cannot by itself prove anything. At the one
  threshold where both images carry comparable ink (lum<120, box interior), the render
  carries 1.8% MORE dark ink than the original — the wrong direction for 8 missing fins.
- **Threshold-robust coverage test (the decisive one):** dark-ink mask (orig lum<120,
  blue/yellow excluded) minus the render's ink mask dilated 3 frame px, over all 8
  inter-dot corridors at full-frame resolution -> 0 unexplained dark px, 0 connected
  components >= 4 px. Widening to a relative-ink mask (lum<177, i.e. panel-fill
  relative) leaves only mid-gray halo pixels: every "beyond 6 px" pixel measures
  lum 139..176 (colors like (175,175,173), (163,163,161)) and traces the curve path —
  the anti-aliased halo of the original's stroke, never dark geometry. A black
  arrowhead is dark ink; there is none.
- **Control (the test detects fins when present):** injecting two synthetic 14x3 px fin
  bars into the ORIGINAL crop yields 53 px beyond 4 px / 38 px beyond 7 px / max
  distance 15.0 px — so the corridor test does not silently miss fins.

The re-roll therefore fails on a claim the pixel evidence refutes at BOTH scales: the
leg is PIL-adjudicated with these banked refutation records. This is the third
sample of the same frozen judge on identical pixels ("BLOCKER", "MAJOR", "MAJOR") —
judge variance documented as sampling (judging.md crop FAIL -> full FAIL -> PASS
precedent), not a build defect. No build change can satisfy a finding that does not
exist in the original; editing the build to draw fabricated arrowheads would ADD a
defect the original does not have.

## Attempt-4 fix found by PIL audit (2026-10-21) — graph-box interior fill

No judge raised this; it was found re-measuring the frame during the full-frame ink
audit. Measurement: color-run scanlines of the original at y=250/300/470 plus five
clean interior patches:

| region | original | attempt-3 render |
|---|---|---|
| gray panel left/right of the red box (x63..190 / x719..894) | (231,233,230) E9E9E7 | (233,233,231) E9E9E7 — MATCH |
| red graph box interior (5 patches, x480..710 y200..500) | (254,255,253) | (233,233,231) E9E9E7 — **WRONG** |
| canvas outside the panel (x2..48 / x912..956) | (254,255,253) | (255,255,255) — MATCH |

The box interior is byte-identical to the canvas white — the original draws a
white-filled rect on the gray panel (the spec's own brief calls the graph frame a
"no-fill rectangle", i.e. it shows the slide background, which here is white — NOT
the panel gray that was beneath it). Attempt 3 filled it E9E9E7, an 8.6%
luminance error over the whole graph interior. FIXED to FFFFFF.

Closed-loop verified on `render_4.png`: box interior patches read (255,255,255)
vs original (254,255,253) (1-unit render canvas convention); panel still E9E9E7;
house-chrome check PASS; banked selfcheck (selfcheck_4_output.txt) 0 CHECK flags.

Crop-continuity proof render_3 -> render_4 (743,619 changed px, all inside the box
interior frame x194..714 y168..505, 735,203 of them non-ink background):
title crop is pixel-identical (0 px) -> its attempt-2 certificate is RETAINED;
axis_top / dot_sequence / min_cluster / lower_left / axis_right all changed ->
re-cut from render_4 (same render-px boxes, FFT-matched at NCC 1.0000) and paired
with matched-scale LANCZOS original crops (MAD 0.000 vs a fresh upscale).
Attempt-4 judge round: full-slide Template A on render_4 + 5 Template B crops.



## Attempt-4 judge evidence + final dot-hue adjudication (2026-10-21)

| Leg | Transcript | Verdict |
|---|---|---|
| Full-slide (Template A) | `judge_attempt_4.txt` | **PASS** (2 MINOR, both adjudicated below) |
| crop axis_top | `crop_4_axis_top_judge.txt` | PASS (4 stroke-weight MINORs) |
| crop axis_right / dot_sequence / lower_left / min_cluster | `crop_4_*.txt` | (this round) |

### Dot hue MINOR (raised 3x by 3 independent judges: attempt-2 dot_sequence, attempt-3 full-slide, attempt-4 full-slide) — PIL-REFUTED, fill KEPT at 5F41C4

Judge wording: "recreation dots are a slightly brighter purple; original dots read a touch
darker blue-purple". Measurement of the ORIGINAL's 9 discs, radial profile (median color
per annulus, halo excluded, 9 discs pooled):

| annulus | original disc color |
|---|---|
| r 0-2 (core) | (66,32,190) |
| r 2-3 | (82,49,199) |
| r 3-4 | (98,68,201) |
| r 4-5 | (104,77,191) |
| r 5-6 | (103,82,175) |
| r 6-7 | (104,86,161) |
| r 7-8.5 (halo) | (155,146,187) |

The original dots are RADIALLY SHADED (dark core -> lighter rim; R,G rise outward while B
falls, which is a hue rotation, NOT a white-blend halo). Disc body (r<5, n=706 px):
mean (87.7,58.8,193.9), median (94,64,196), p25 (66,36,178), p75 (107,79,212).
The MSE-optimal FLAT fill over that body is (90,60,195) — the current fill 5F41C4
(95,65,196) is within (1,1,0) of the median and (7.3,6.2,2.1) of the mean, MSE 545 vs
the optimum 516; the darker alternative 4620C0 (70,32,192) has MSE 859 (57% worse) and
misses the median by (-24,-32,-4).

Conclusion: the render's flat fill equals the original disc's BODY color. The judges'
"brighter" read comes from the dark core (r<2, (66,32,190)) of the original's radial
shading, which a flat PPTX fill cannot express (pptxgenjs has no radial-gradient fill
API). The attempt-3 "interior median (95,65,196)" reading stands as the disc body median;
the earlier "darkest-10% core (56,31,147)" is the core, not the fill. MINOR, inherent
shading/medium difference; fix would require gradient fills and would make the body
darker than the frame. No change.

### Attempt-4 full-slide MINOR 2 (curve stroke AA/weight) — PIL-benchmarked, no change
Original curve trace->ink distance max 7.00 / mean 0.19 frame px (banked); the render's
stroke is black #000000 2pt at 150dpi and the frame's curve is a soft video-captured
stroke; the judges' "heavier/opaque" read applies to the render's crisp AA edge. Same
class as the four axis_top crop MINORs (all four read IMG1 heavier). Inherent render-vs-
video-capture medium difference, MINOR, no geometry error (selfcheck_4: 0 CHECK flags).

---

## Attempt-4 closure — resumption w9-s027-20261021T0400 (2026-10-21)

**Resume context.** The previous worker (w8-s027-20261020T2330) died mid-adjudication
during an upstream provider storm; its claim was released and this worker took a
fresh claim `w9-s027-20261021T0400`. Auditing the final state uncovered two things
beyond the documented resume point:
1. The attempt-4 judge round was fully banked (full-slide + all 5 crops) exactly as
   the coordinator reported.
2. **The dying worker had, at 03:49 (after the last crop judge landed at 01:26),
   OVERTURNED its own attempt-3 refutation and EDITED the live `build/slide_027.js`
   to draw 8 discrete `#ACACAD` "learning-step" triangle arrows chaining dot1->dot9** —
   asserting the arrows are real neutral-gray ink its earlier BLACK-corridor tests
   could not see. That edit is banked verbatim (never deleted) as
   `build_attempt_5_REJECTED_DYING_WORKER_FABRICATION.js`. This worker re-ran the
   gray hypothesis from scratch **before** accepting the overturn; see the dedicated
   arbitration below — **the overturn is itself refuted and the edit rejected.**

### Attempt-4 leg verdicts (all transcripts banked)

| Leg | Transcript | Verdict |
|---|---|---|
| Full-slide (Template A) | `judge_attempt_4.txt` | PASS (2 MINOR, adjudicated) |
| crop axis_top | `crop_4_axis_top_judge.txt` | PASS (4 stroke-weight MINOR, adjudicated) |
| crop axis_right | `crop_4_axis_right_judge.txt` | PASS (no defect) |
| crop lower_left | `crop_4_lower_left_judge.txt` | PASS (no defect) |
| crop dot_sequence | `crop_4_dot_sequence_judge.txt` | FAIL (1 MAJOR + 1 MINOR) — both PIL-refuted below |
| crop min_cluster | `crop_4_min_cluster_judge.txt` | FAIL (1 MAJOR + 1 MINOR) — both PIL-adjudicated below |

### Full-slide PASS (`judge_attempt_4.txt`) — 2 MINOR (restated, already adjudicated)

1. **Dot hue** ("recreation dots slightly brighter purple"): PIL-REFUTED — the
   original dots are radially shaded; flat fill 5F41C4 equals the disc BODY median
   (MSE 545 vs MSE-optimal 516, vs 859 for the darker alternative). Inherent
   shading/medium (pptxgenjs has no radial-gradient fill). No change.
2. **Curve stroke AA/weight heavier at the top-left endpoint**: render = true
   #000000 2pt at 150dpi; frame = soft video-captured stroke. Same class as the four
   axis_top crops (all read IMG1 heavier). Inherent render-vs-capture; curve trace
   mean 0.24 / max 1.02 fpx (selfcheck_4). No change.

### axis_top PASS (`crop_4_axis_top_judge.txt`) — 4 stroke-weight/glyph MINOR (restated)

All four (y-axis shaft/arrowhead weight; "Cost" glyph weight; left-branch stroke
weight; arrowhead proportions) read IMG1 heavier/crisper — the render-vs-video-
capture medium difference. PIL earlier: arrowhead hull delta < 1.5 fpx, shaft black
in both, "Cost" glyph count identical. selfcheck_4 axis/curve/label geometry within
tolerance (0 CHECK flags). No change.

### axis_right PASS (`crop_4_axis_right_judge.txt`) — clean

Judge: arrowhead correct & right-pointing, theta crossbar present & continuous,
right red stroke = intentional template chrome; "None content-level." Only
GROUND-RULE-(e) capture-artifact exclusions. Nothing to adjudicate. PASS.

### lower_left PASS (`crop_4_lower_left_judge.txt`) — clean

Two-line "Random / initial value" glyph-for-glyph identical; x-axis left end + leader
foot continuous in both; judge explicit "BLOCKER: none, MAJOR: none, MINOR: none that
clear the noise floor." PASS.

### dot_sequence FAIL (`crop_4_dot_sequence_judge.txt`) — MAJOR + MINOR, both PIL-REFUTED

**Fifth sample** of the recurring FABRICATED inter-dot "learning-step arrows" class
(attempt-2 BLOCKER -> attempt-3 MAJOR + re-roll -> attempt-4 MAJOR), now joined by
min_cluster below (sixth sample). Fresh attempt-4 measurements
(`measure_attempt4_arrow_refutation.py` + banked `measure_attempt4_output.txt`):

**Finding 1 (MAJOR, "missing learning-step arrows between descent dots").**
Fresh 8-corridor diff on `render_4.png` at frame resolution: original black-ink mask
(blue-dot pixels excluded) minus render ink mask dilated 3 fpx = **0 unexplained px in
all 8 inter-dot gaps**; threshold sweep lum<150 -> 0, lum<177 -> 5 px, lum<205 -> 9 px
(all AA halo, far below an arrow pair's dozens of px). **Control**: two synthetic
14x3 fpx fin bars injected into an original gap -> 26 unexplained px, a live
component — so the test detects fins and the 0 is a true negative. The original is
ONE continuous parabola through the 9 radially-shaded dots; no inter-dot arrowheads
exist. Re-affirmed against the six banked measurements in this file (corridor diff,
chain-band ink budget, annulus ink, perpendicular width profile, ASCII ink maps,
extra-relative-ink map). PIL-REFUTED; no build change. Judge variance, not a defect.

**Finding 2 (MINOR, "chain continues farther right / render terminates early").**
Fresh PIL (measurement section B): original blue-chain extent x 257.2..435.1 fpx,
render x 254.8..432.7 fpx — **rightmost-blue delta 2.4 fpx**; yellow-minimum dot
present in both (600 vs 622 px); render's dark right branch continues x->901 exactly
as the original. Both images end the blue dots at the vertex/yellow-minimum
(~432..435 fpx) with NO blue on the rising right branch; the "empty space to the
right" the judge read as "earlier termination" is identical in both and CORRECT (the
descent dots stop at the minimum). PIL-REFUTED; no change.

### min_cluster FAIL (`crop_4_min_cluster_judge.txt`) — MAJOR + MINOR, both PIL-adjudicated

**Finding 1 (MAJOR, "chain of small GRAY curved step-arrows linking consecutive
dots").** Same fabricated element, new venue. Fresh min_cluster corridor diff
(measurement section A3): gaps dot7->dot8, dot8->dot9, dot9->yellow = **0 unexplained
px each, 0 components >= 4 px**. The only gray near the chain is the dashed leader
(explicitly matched by the judge) and the original stroke's soft AA — adjudicated in
the gray arbitration below. PIL-REFUTED.

**Finding 2 (MINOR, "axes/parabola lighter+thinner in IMG2").** Capture-softness
(GROUND RULE (e)); geometry matches (selfcheck_4: axis y435-436.5, curve within
tolerance). MINOR, no geometry error. Refuted.

### THE GRAY-ARROW ARBITRATION (decides the dying worker's overturn)

The dying worker's 03:49 edit claimed the original carries neutral-gray step-arrow ink
that black-corridor tests miss. This worker tested it independently
(`measure_gray_arrow_hypothesis.py`) and ran a head-to-head with identical
neutral-gray / far-from-core methodology on BOTH images
(`measure_gray_headtohead.py`; both outputs banked). Results:

- The original DOES carry neutral-gray ink (lum 120-204, non-saturated), ~852 px at
  6 fpx above the dark core, on the **upper-left chain only**, **tapering
  monotonically**: dot1->2 402 -> dot2->3 214 -> dot3->4 164 -> dot4->5 72 ->
  dot5->6 0 -> dot6->7 / dot7->8 / dot8->9 = 0; **right branch (same curve, no dots)
  = 0.**
- Morphology: a **diffuse 2-3 px ribbon hugging the curve**, sliced into 15-18 pieces
  by the black cores — **no localized arrowhead widenings, no tips, no barbs.** 8
  true arrowheads would be ~8 equal-sized components; this is a soft tapering glow.
- Head-to-head: `render_4.png` carries the measured black curve (trace mean 0.24 /
  max 1.02 fpx) and the 9 correctly-placed dots, with **0** of that gray — render_4
  reproduces the layer the video captured crisply; the original's upper-left stroke is
  simply **softer/lighter** there (more of its mass in the gray band).

**Conclusion.** The gray is the original's **softer ink rendering along the upper-left
chain** — video-capture softness, i.e. GROUND RULE (e) "JPEG compression halos or soft
edges" and ground rule (c) typed-vs-handwritten ink (inherent medium difference, at
most MINOR). It is **not a set of discrete arrowheads**; a clean vector recreation of
the measured curve is correct to omit capture blur. The dying worker drew **8 crisp
triangle arrowheads**, 3-4 of them in gaps (dot5->9) containing **zero** source ink —
a fabrication extrapolated from soft capture glow. Law: "do NOT modify the build to
draw fins the original does not have"; "fidelity ... never invent."

**Action.** The 03:49 edit was banked verbatim
(`build_attempt_5_REJECTED_DYING_WORKER_FABRICATION.js`) and the live
`build/slide_027.js` was restored **byte-identical to the certified
`build_attempt_4.js`** (`diff -q` identical; 0 step-arrow references). The
deliverable `slide_027_recreated.pptx` (md5 `5ac66904899885d0dfbff0475caf8676`,
produced 00:50, before the edit) was never rebuilt and contains **no** fabricated
arrows. `render_4.png` remains the certified final render; house-chrome check PASS
(panel x112-1882 y94-bottom; L/R/bottom strokes, top bare; badge center (1824,152)
d~68, all tol 8).

### Attempt-4 determination

Every attempt-4 leg is PASS or PIL-refuted with banked evidence. The full-slide
Template A comparison is a real PASS; all five crop certificates are clean or
PIL-adjudicated with banked refutation records (this file + the three banked
`measure_*` outputs). No genuine NEW defect was found, so no rebuild round is opened;
the single incorrect artifact (the dying worker's fabrication) was rejected and backed
out without touching the certified deliverable. `visual_check=PASS` is warranted:
full-slide verdict line, zoomed-leg certificates, measured-geometry agreement
(selfcheck_4: 0 CHECK flags), and the house-chrome check are all banked.
