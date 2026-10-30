# Adjudication — slide 027, attempt 9/10 (worker `w11-s027-a9-20261021T2100`)

**CONTROLLING INPUT: the founder's own visual review of `render_8.png` / the shipped
attempt-8 `slide_027_recreated.pptx`.** Three findings, quoted substance, BINDING. Per
the owner's precision mandate (a visible deviation from the original is a MAJOR even over
a judge PASS) they override every earlier judge PASS and every PIL census banked for
attempts 3, 6 and 8 (`adjudication_attempt_{3,6,8}.md`, `probe_adj7_*`, `probe_adj8_*`).
Nothing in this record re-litigates them: they are the fix spec. Everything superseded
stays banked; nothing was deleted.

| # | Founder finding (substance) | What attempt 8 actually shipped | Fix shipped in attempt 9/10 |
|---|---|---|---|
| A | The black cost curve reads "noticeably jagged/rippled rather than a smooth mathematical curve"; identify it as a quadratic curve and draw ONE SMOOTH mathematical curve (a quadratic cost function of the iterate position) | 54 hand-traced knots joined as a Catmull-Rom polyline, the knots taken from a JPEG-halo-traced centre-line — the ripple was the input data, not the renderer | one analytic quadratic `y = -0.00395282*(x-450.41)² + 407.25`, 420 samples at 1 frame px, extent x=239..658 |
| B | The grey dashed step connectors "are misaligned arc connectors: some overlap awkwardly or float slightly off from the centers of the purple data points" — each connector must run between CONSECUTIVE purple dot CENTRES | 9 links stopping 8–12 fpx short of the adjacent centre, and dot centres rounded to 0.5 fpx from a halo-contaminated census | 9 cubic arcs anchored dot-centre→dot-centre on the measured halo-excluded centroids; the dots are repinned to those centroids |
| C | "The grey connectors are NOT headless plain arrows — they are ARROWS WITH ARROWHEADS … draw real arrowheads at the terminating end of each connector … Measure the head geometry from the original frame rather than guessing" | nine headless shafts (`line.endArrowType` never used; no head geometry existed at all) | nine filled grey triangles measured from the original frame (length 5.4 fpx, half-width 2.7 fpx, tangent along the arc's terminal direction, tip 6.32–6.58 fpx from the target centre) |

---

## 1. Measurement of the original frame (all banked under `qa/slide027/`)

`probe_adj9_geometry_output.txt` (+ `adj9_geometry.json`, the machine-readable form):

- **Curve.** Orthogonal-distance TLS over 1748 neutral-dark ink px. Free quadratic
  `a=-0.00421895`, vertex (450.414, 414.429), RMS 6.641. Vertex-y-locked to the yellow
  minimum's measured centre (444.49, 407.25): the selected fit is
  **`a=-0.00395282`, vertex (450.410, 407.250)`, RMS 6.924, max 16.744 fpx**, traced
  orthogonal deviations on 10 stations `-12.4 -2.7 +8.7 +13.6 +4.9 +0.2 +0.2 +7.0 +6.9
  -12.0` (max 13.63). The 420-point dense sample has constant second difference
  `2a = -0.0079 fpx` — mathematically zero ripple; the 1-fpx chord facets are 0.002 fpx
  deep.
- **Arm caps** (`probe_adj9_extent_output.txt`): the original's ink envelope runs
  x 232..642; the LEFT arm cap reads y 228..233 (centre 230.5) at x=253 and the RIGHT
  cap y 235..239 (centre 237.0) at x=642.
- **Nine dot centres** (halo-excluded interior centroids, disc masks dilated to kill the
  JPEG ring): (263.12,263.41) (283.64,309.88) (306.85,341.79) (331.65,366.36)
  (354.26,381.00) (373.91,390.45) (392.40,396.74) (410.77,401.75) (428.21,405.90);
  yellow minimum (444.49, 407.25).
- **Nine connectors** (`probe_adj9_connector_output.txt` + `probe_adj9_geometry`):
  bows 18.8–29.4 fpx; visible-ink RMS 0.92–4.98 fpx against the fitted quadratic; **0/60
  sample points cross the parabola** (each bows away from it); head tips 6.32–6.58 fpx
  from the target centres with tangents along `(-0.30…0.26, 0.95…1.00)` — i.e. pointing
  steeply DOWN-RIGHT, the descent direction.
- **Chain grey**: core-35% (162,162,161) `#A1A2A0`, darkest-10% (155,155,154); shipped
  `CHAIN_GRAY = ACACAD`, inside the measured band, renders at (172,172,173).
- **Dashes: the founder's description says "dashed"; the frame's connectors are SOLID.**
  Link 1 is 95% on-density over its ink span and links 2–9 are 100% on
  (`probe_adj9_connector_output.txt` line 15: "ink spans s 9.0..34.0; 95 px in 26 bins",
  no gaps in any other link's profile). No dash cadence is measurable in the original, so
  none is drawn — a dashed render would have invented geometry the original does not have.
  This is a description-vs-frame difference recorded honestly, not a fight over the
  finding: the substance of B and C (centre-to-centre anchoring, real arrowheads) is
  implemented exactly as asked.

## 2. What attempt 9 changed, and attempt 10 refined

- **Attempt 9** (`build_attempt_9.js`): finding A's analytic quadratic with extent
  x=241..660; findings B/C's nine arcs + nine heads + repinned discs
  (`triShape(pts, col)` extended to carry a colour; the two axis arrowheads still call it
  colourless, so their bytes are unchanged).
- **Attempt 10** (`build_attempt_10.js`, == `build/slide_027.js`): the curve extent was
  refined to **x=239..658**. `probe_adj9_extent_output.txt` shows the shipped 241/660 sat
  3.4 fpx short at the left cap and 3.4 fpx over at the right; 239/658 lands both stroke
  tips on the measured arm-cap positions. Draw order: curve → connectors → heads → discs →
  yellow minimum, so each shaft's overrun into the receiving centre is covered by its own
  head and then by that disc.
- Everything else in the build (title, graph box, axes + arrowheads, dash leaders, all
  eight text labels, containment) is byte-identical to attempt 8.

## 3. Verification of the three findings on `render_10.png` (`probe_adj9_verify_output.txt`)

**A — SMOOTH. PASS.**
Band-limited (20 fpx) neutral-dark column centroids against the shipped analytic
quadratic: residual rms 0.8271, max 1.7691 fpx (0.4% of the 400-fpx span); de-noised
ripple (|d2| of the residual after a 5-pt moving average) rms **0.1202**, max **0.4798**
fpx. Attempt-8 control through the identical code path: residual rms 8.9817, max 19.7601;
ripple rms **1.9531**, max **21.1094** fpx — the ripple is **16× smaller** than what the
founder saw. Reported honestly: the sign-flip count is 245/325, which looks alarming but
is the expected signature of per-column centroid quantisation (a second difference of any
quantised trace flips sign most of the time); the founder's complaint was about the
visible amplitude, which is now sub-pixel.

**B — ANCHORED. PASS.**
Worst render-disc centroid offset from the anchor: **0.87 fpx** (attempt 8: up to 2.9 fpx,
plus the 11-fpx short yellow-dot gap). All nine arcs carry chain ink at 8–9 of 9 sample
points along their own fitted quadratic. Radial walk from each dot centre along the arc:
each shaft's first visible chain ink appears at **r = 6.65–7.06 fpx** (disc radius 6.5) on
BOTH ends of all nine connectors, with zero misses — i.e. the shafts run INTO the discs
and are occluded by them, exactly what "centre-to-centre" looks like on a render. The
stretch inside r < 6.5 is covered by the disc drawn on top, so it is not a gap.

**C — ARROWHEADS. 9/9. PASS.**
Point-in-triangle census of the nine measured head triangles: 86–92% of each triangle's
render px carries chain grey; centroid-window ink 95–99 px per head (a filled triangle,
not a stroke crossing). Total grey inside the nine triangles: **512 px on attempt 10 vs
70 px on attempt 8** (7.3×) through an identical census — attempt 8 had no heads.
`selfcheck_attempt_10_output.txt` confirms 41–69 px of chain ink at each head's tip.

**Also PASS on attempt 10:** `house_chrome_check` (panel x112-1882, y94-bottom; L/R/bottom
strokes, top bare; badge centre (1824,152) d≈68; tol 8);
`selfcheck_attempt_10_output.txt` (title/box/axes/dashes/labels within 2.0 fpx; curve ink
within 2.33 fpx of the analytic y at 365/365 unoccluded columns — the 39 disc-halo
columns are the discs drawn over the curve; envelope x=238..658 == the shipped extent);
`reproducibility_attempt_10.txt` (the pptx regenerates content-identically).

## 4. Judge legs (deck 03 law: BOTH legs, zoomed)

Dispatch scripts (`dispatch_A_10.sh`, `dispatch_B_10_{chain_full,min_cluster,axis_top,
dot_sequence}.sh`) take their `-p` payload **byte-identically** from
`shared_patterns/judge_protocol_03.md` (verified by string equality against the protocol
file at bank time). A new region `chain_full` frame(240,240)-(460,430) was added because
the banked `dot_sequence` bbox stops at x=415 and therefore cuts out dot 9 (428.21,405.90)
and the yellow minimum — the exact ink findings B and C concern.

Retention proof (`render_8` vs `render_10` render crops, same slide-space bboxes):
`title`, `lower_left`, `axis_right` are **0 px differing** (their attempt-8 transcripts
stay valid); `axis_top` (1890 px), `dot_sequence` (6914 px) and `min_cluster` (4960 px)
changed and are re-judged.

## 4a. Template A (`judge_attempt_10.txt`) — **PASS** (full-slide, attempt 10)

No BLOCKERs, no MAJORs. Elements verified present and correctly tied
(θ̂ under its tick, "+" left of the tick, "Minimum" up-right of the yellow dot, "Random
initial value" under the dashed leader). Frame containment clear (tightest ~20 px, no
contact). Two MINORs were raised; both adjudicated PIL-first below (§4c).

## 4b. Template B crop legs

`chain_full`, `min_cluster`, `axis_top`, `dot_sequence` dispatched 2026-10-21 through
`scripts/16_vision_gate.sh` (banked `dispatch_B_10_*.sh`, `crop_B_10_*_run.log`).
Results appended in §4d when the dispatch settles.

## 4c. PIL-first adjudication of Template A's two MINORs

**MINOR 1 — title inter-word spacing (high confidence). SUPPORTED in detail, adjudicated
not-a-fix-trigger (font-metric artifact).** Column-ink-run analysis of line 1
(`Follow Negative Direction of Gradient with`), frame px:

| | text bbox x0..x1 | total width | the five word gaps |
|---|---|---|---|
| original | 193..744 | **551.0** | 20, 11, 11, 8, 11 |
| render_10 | 191.4..742.7 | **551.3** | 9.6, 10.5, 10.5, 7.6, 8.6 |

Line 2 bboxes: original 58..901/108..149 vs render 58.1..900.5/107.9..149.2 — the
58/901 runs are the panel's red frame strokes, not title ink. So the original does render a
wider space after "Follow" (20 vs 9.6 fpx) and uniformly ~2-3 fpx wider spaces, exactly as
the judge saw. But the **total line width already matches to 0.3 fpx** (551.0 vs 551.3):
the original's wide word gaps are bought with tighter glyph advances in its font, the
render's narrow gaps with wider glyphs. Widening the render's five gaps to the original's
values would push the title 14 fpx WIDER than the original — trading a matching-total-width
result for a mismatched one. Words, line break, colour, weight and centering are identical;
the residual is a font-substitution side-bearing difference (the same class as the
typed-vs-handwritten allowance in GROUND RULES (d)). Not a fix trigger.

**MINOR 2 — "schematic parabola proportion" (medium confidence). REFUTED in substance; the
residual is a documented, mandated property of the analytic quadratic.** PIL measurement of
the very elements the judge cited:

- Yellow minimum/θ̂ marker centre — **original x=444.5, y=407.0; render_10 x=444.0, y=406.6**
  (yellow mask, badge band excluded). Offset **0.5 fpx**.
- Inner plot frame — **identical in both images**: vertical red strokes at cols 193-194 /
  715-717, horizontal at rows 166-168 / 506-508 (original); render 192.4-193.8 / 714.8-716.3
  and 166.0-167.4 / 505.7-507.1.
- Marker as a fraction of inner-frame width — **original (444.5-193.5)/(716-193.5) = 48.0%;
  render (444.0-193.1)/(715.5-193.1) = 48.0%**. The two markers are colocated.
- Right-arm headroom below the frame's top border — original right cap (x=642, y 235..239,
  centre 237.0) → 237.0-167.0 = **70.0 fpx**; render quadratic tip (x=658, y=236.9) →
  236.9-166.5 = **70.4 fpx**. Same, within 0.4 fpx.

The judge's own numbers (marker "≈40-41% in the recreation vs ≈52% in the original") are
therefore wrong by 8-12 points **in the same direction for both images** — it measured one
thing and reported a different position. The only real difference is horizontal, not
vertical: a single quadratic cannot reproduce the original's steeper arms, so to reach the
same cap heights the fitted quadratic runs further out (left cap x 253 orig → 239 render,
right cap 642 → 658). That is the documented cost of the founder's finding A, which names a
quadratic curve, and it is already recorded in §1/§2 (fit RMS 6.92 fpx, arm deviations
-12.4…+13.6 fpx). Every label stays tied to its own mark, which is the failure mode MINOR 2
was guarding against. Not a fix trigger.

## 4d. Template B results

Chain of records, in dispatch order (all attempts use the frozen protocol payload):

| crop | verdict | notes |
|---|---|---|
| `chain_full` (240,240)-(460,430) | **PASS** | 5 MINORs, no MAJOR/BLOCKER |
| `min_cluster` (195,355)-(520,512) | **PASS** — clean, no discrepancies at all | third re-invocation (see §4f) |
| `axis_top` (190,170)-(332,292) | **FAIL** — 2 MAJORs | adjudicated PIL-first in §4e |
| `dot_sequence` (245,225)-(415,440) | **PASS** | 1 MINOR, no MAJOR/BLOCKER |

## 4e. PIL-first adjudication of the `axis_top` FAIL
(`probe_adj10_axis_top_output.txt`, `probe_adj10_axis_top2_output.txt`,
`probe_adj10_tone_output.txt`, `probe_adj10_cost_output.txt`)

The two MAJORs and their measured verdicts:

**MAJOR 1 — "the y-axis is a solid black medium-weight line with a filled crisp black
triangular arrowhead in IMG1; noticeably thinner, LIGHT-GRAY line with a softer/lighter
gray arrowhead in IMG2". TONE: CONFIRMED. WEIGHT: REFUTED. Fix trigger: NO.**

| | original | render_10 |
|---|---|---|
| shaft core ink | mean RGB **(80,81,79)**, lum p50 81 | mean RGB (36,36,36), lum p50 0 |
| shaft width | **3.00 fpx** (centre x 223.0) | 2.40 fpx (centre x 222.35) |
| arrowhead ink | **83 px, mean RGB (96,98,95), 0 px pure black** | 315 px, mean RGB (1,1,1) |
| arrowhead geometry | bbox x 218..228, y 206..219 | bbox x 218.3..227.0, y 205.8..219.7 |
| x-axis core | mean RGB (103,103,103), lum p50 113 | mean RGB (0,0,0) |
| "Cost" label | mean RGB (107,94,95), lum p50 112 | mean RGB (41,41,41), lum p50 0 |
| curve core (bowl bottom) | mean RGB (61,62,61) | mean RGB (11,11,11) |

So the original really does draw its diagram ink in soft dark greys (axis 81-113, curve
61, chain 162, labels 112) while the recreation uses pure 000000 — a real, measured tone
difference over the whole diagram, confirmed. But the judge's "thinner … medium-weight /
heavier" is the wrong direction: the render's shaft is **2.40 fpx against the original's
3.00 fpx, i.e. 20 % THINNER**, and the arrowhead's shape matches to 1 fpx (this also
refutes the attempt-8 crop judge's "wider base / different side-slope" on the same
region). Not a fix trigger because the axis, arrowhead and label inks are **byte-identical
to the geometry the founder reviewed in `render_8.png`** — the founder's three findings
were A/B/C, not tone; and attempt 8's crop judge scored this identical region MINOR on
weight only and PASSed. It is an **inherited/cascade zone** (deck-03 procedure B step 6:
"adjudication inputs, never fix triggers"). Note the Template A judge, which saw the whole
slide at normal scale, raised no tone finding at all — the difference only reads at 2.08x
zoom. Recorded as a known residual with the numbers above; the purple dots, by contrast,
match within a few units (original (97,70,187) vs render (97,67,196)).

**MAJOR 2 — "the dark stroke through the purple marker reads as a predominantly STRAIGHT
diagonal that KINKS at the dot; IMG2's marker is carried by one smooth, continuously
curved branch; the only curvature is a faint separate gray arc hugging the lower-right of
the dot". ALL THREE DESCRIPTIVE CLAIMS REFUTED; the one true difference is the documented
arm deviation.**

1. **"Kink" is impossible by construction and refuted by measurement.** The shipped stroke
   is ONE analytic quadratic `y=-0.00395282(x-450.41)²+407.25` — a single C² path with no
   join at all. Measured on the crop's own window (frame x 244..300, relaxed dark ink,
   anchored on the analytic curve): de-noised second difference **rms 0.160 fpx, max
   0.382 fpx** — at the 5-pt-centroid quantisation floor (~0.30) and 3x lower than the
   ORIGINAL's own trace over the same window (rms 0.517, max 2.193). The recreation's
   branch is measurably SMOOTHER than the original's frame ink, so it cannot be the
   "chorded/kinked" stroke IMG1 is accused of being.
2. **"Straight vs smooth" is refuted.** Chord-bow over the identical window, trace vs
   chord: **original 3.32 fpx (chord length 99.3) vs render 1.99 fpx (length 96.8)** —
   both strokes are essentially straight over that stretch; the difference is 1.3 fpx
   (0.0024 of the slide height). The piece of the original that bows steeply is the LEFT
   ARM CAP at x 253 (the trace's slope runs 8.7 there), which is outside the stretch the
   judge drew, and the render's fitted quadratic reproduces the cap position itself
   (§1: extent 239..658 puts both stroke tips on the measured arm caps).
3. **The "faint separate gray arc hugging the lower-right of the dot" is the dashed
   leader, and it is in BOTH images.** Grey census (spread<=12, lum 100..200) NW of
   dot 1: **original 59 px at frame (253..260, 233..255)** — the dashed drop-line collar,
   the same ink the attempt-8 crop judge explicitly listed as "same short dashes;
   position count consistent"; the render has 8 px in the same zone. The connector
   1→2 itself occupies a different zone (S-SE of the dot, x 264..282) where the render
   carries 166 px to the original's 87 — the difference is the mandated arrowheads plus the
   wider CHAIN_GRAY stroke, not a displaced path.
4. **The one true difference, conceded and explained.** The original's left branch deviates
   from the analytic quadratic by **rms 1.98 / max 5.22 fpx** in this window, and by up to
   12.4 fpx orthogonal at the left cap — the documented price of finding A's single
   quadratic, which is pinned to the two hard anchors of the slide (the stroke tips on the
   measured arm caps, the vertex on the yellow minimum at y=407.25). No quadratic can do
   better: the three-point solve through the two caps and the marker asks
   `a=-0.004720` from the left cap and `a=-0.004834` from the right cap — a 2.4 %
   inconsistency, i.e. the frame's curve is measurably steeper-armed than any quadratic.
   This is the same proportional point Template A scored MINOR (§4c) at zoom, and it is a
   **cascade of the founder's own finding-A spec, not a worker error**.

Verdict: `axis_top` FAIL is PIL-adjudicated; both MAJORs' descriptive bodies are refuted
with measurements, and the two real residuals (tone, arm shape) are inherited/cascade
inputs recorded above. The region's contained elements — the "Cost" word, the y-axis
arrowhead pointing up at the shaft's top, the dashed drop-line, dot 1 — are all present
and at the measured coordinates.

**The decisive control for MAJOR 1 — the axis ink the finding is about is PIXEL-IDENTICAL
between render_8 and render_10.** Diff of the two crops, same slide-space bbox:
**1839 differing px of 75184, all confined to frame-x 238.0..288.3 / frame-y 229.6..291.5**
(the redrawn left branch plus dot 1) — and **0 differing px inside the y-axis shaft band
(frame x 220.5..224.5) and 0 inside the arrowhead band (frame x 214..232, y 198..222)**.
The build confirms it at source level: `build_attempt_8.js` lines 90-126 ==
`build/slide_027.js` lines 96-123 for the two axis lines and both arrowhead calls;
`triShape` only gained an optional colour argument that defaults to black, and the two axis
calls still pass none. So the tone the crop judge escalated to MAJOR is the exact geometry
the founder reviewed in `render_8.png` and the exact geometry `crop_8_axis_top_judge.txt`
scored MINOR on weight only and **PASSed**.

## 4f. `min_cluster` — PASS on the third re-invocation (`crop_10_min_cluster_judge.txt`)

The dense-region leg needed three dispatches. The first two produced no winner body at
all: the client's own 630 s hard-wall ladder aborted twice inside each dispatch and my
outer `timeout 1700` closed the third, so no transcript existed
(`crop_B_10_min_cluster_run.log`, `crop_B_10_min_cluster_retry_run.log`). Protocol: no
evidence, not a FAIL; sleep 300 and re-invoke. The third invocation
(`crop_B_10_min_cluster_invoke3_run.log`) returned a coherent body: **no BLOCKER, no
MAJOR, not even a content MINOR** — dots 7-9, the yellow minimum, the vertex, the
"Minimum" label, the θ̂ caret, the faint grey "+" and the two-line "Random / initial value"
label all present and correctly placed, with only the expected render-medium differences.
PIL pre-measurement of the same region (`probe_adj10_mincluster_output.txt`) agrees:
violet-blob centroid and bbox within 1 fpx, yellow minimum within 0.7 fpx, ink row bands
identical to 1 fpx, the θ axis row is the same 100 %-coverage row at frame y 435-437 in both.

## 4g. The PASS legs' MINORs — measured, none a fix trigger

**`dot_sequence` MINOR 1 — "IMG1's first connector is a pronounced over-the-top arc
rising above the black curve; IMG2's tracks just along/under the curve with no hump"
(`probe_adj10_link1b_output.txt`). DESCRIPTION REFUTED, SUBSTANCE ~2.5 fpx CONFIRMED,
NOT A FIX TRIGGER.** Direct census of connector-1 ink in both images with the two dot
halos, the dashed-leader column and the black curve all excluded: the **ORIGINAL's**
connector-1 ink sits at **mean +8.09 / median ~+11.2 fpx up-right of the dot1→dot2 chord**
(chord length 50.8 fpx; the black curve itself is only +1.29 fpx up-right at the same
station), i.e. the original's first connector is itself an over-the-top arc 6.8-9.9 fpx
above the curve — the judge's "no over-the-top hump … along/under the black curve" is
false. What is true is a small overshoot: the built arc reaches **+13.63 fpx at s=0.5**
against the original's median ~+11.2 — about 2.4 fpx, inside the banked fit uncertainty
(this link measured quadRMS 0.464 fpx; the nine arcs' VIS-ink RMS against their fitted
quadratics is 0.92-4.98 fpx). The anchors the founder's finding B cares about are exact:
the arc starts and ends on the two measured dot centres.

**`chain_full` MINOR 2 — "IMG1's first descent dot is markedly larger, a strong size
step-down" (`probe_adj10_discs_output.txt`). REFUTED.** The build draws all nine discs at
`w: px(13), h: px(13)` — identical by construction. Measured extents: render **14.4-14.9
fpx for dots 1-7** (18.8 for dots 8-9 only because the neighbouring dot's ink merges
inside the ±11 fpx window) against the original's uniform **14-15 fpx** for the same dots
(dots 8/9 likewise merge). Dot 1 is the same size as dots 2-7 in both images; there is no
size step-down.

**`chain_full` MINOR 3 — "IMG1 places the 2nd dot lower / first arc longer". REFUTED.**
Dot 2 renders at **0.67 fpx** from the original's measured centre; the worst of the nine
discs is 0.87 fpx (`probe_adj9_verify_output.txt`).

**`chain_full` MINOR 1 — "Minimum" clipped at the crop's right edge.** A crop artefact,
not a slide defect: the region bbox ends at frame x=460 and so cuts the label in BOTH
images; Template A verified the word is present, correctly spelled and correctly placed.

**`chain_full` MINORs 4-5 — colour/contrast and the "Learning step" label's vertical
centering.** The colour claim is the same measured, inherited tone class as `axis_top`
MAJOR 1 (§4e — the purple itself matches within a few units: 97,70,187 vs 97,67,196). The
label geometry is byte-identical to attempt 8, which was reviewed by the founder and whose
full-slide/crop legs verified it.


