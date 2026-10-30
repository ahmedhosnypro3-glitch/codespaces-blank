# Slide 027 — Adjudication of attempt 6 (w8, 2026-10-21)

Artifact judged: `build_attempt_6.js` → `recreated_pptx/slide_027_recreated.pptx`
(md5 `39231aeb0b37db9ac89a4fcc1620d288`, verified to contain the attempt-6 build: white
`FFFFFF` graph box ×2, `ACACAD` ×21, `custGeom` triangle heads) → `render_6.png`
(2001×1125, house-chrome and selfcheck both PASS, banked).

Legs dispatched (attempt 6, payloads byte-identical to the frozen templates — 4115 / 1914 chars):

| leg | transcript | verdict |
|---|---|---|
| full-slide (Template A) | `judge_attempt_6.txt` | **FAIL** — 2 MAJOR + 2 MINOR |
| dot_sequence (Procedure B) | `crop_6_dot_sequence_judge.txt` | **FAIL** — 2 MAJOR (high) + 4 MINOR |

Not dispatched: `title`, `axis_top`, `min_cluster`, `lower_left`, `axis_right` —
`.run_crop6_*.sh` scripts and crops are banked for the re-dispatch. Attempt 6 already
carries 2 MAJOR FAIL legs, so further legs cannot change the outcome and the 6-attempt
budget is exhausted (law: `scripts/17_worker_instructions.md` line 333).

## The judge legs contradict each other — the measurement is the arbiter

`judge_attempt_6.txt` reads IMG2 as "small blue dots … joined by one continuously
converging dotted/light trajectory … **This adds geometry/arrowheads that the original
does not show**", while `crop_6_dot_sequence_judge.txt` reads IMG2 as "arrows chained
between consecutive blue dots: one small arrow in each gap, with each arrowhead
co-located at a dot". Two readings of the same frame, mutually exclusive on whether the
gray marks exist. PIL decides it: they exist. Both legs agree on the *defect in IMG1*:
my gray chain reads as a SECOND element, not as part of the dot-bearing curve.

## PIL adjudication, finding by finding

### A1 — "adds geometry/arrowheads the original does not show" (full-slide MAJOR 1) — REFUTED IN FACT

`scratch/probe_arrow_decide7_output.txt` (annuli perpendicular to the curve, gray mask
`spread≤18 & lum 115..220 & distance>4 from all dark/hued ink`):

```
region                   annulus            gray px per 100 fpx of curve
CHAIN (dots)             r 0..3 on curve      107.6
CHAIN (dots)             r 3..6 above          4.1
CHAIN (dots)             r 6..11 above        80.0
CHAIN (dots)             r11..16 above       338.8
CHAIN (dots)             r 6..11 below         9.4
CHAIN (dots)             r11..16 below         8.8
RIGHT BRANCH (control)   r 0..3 on curve     426.4
RIGHT BRANCH (control)   r 3..6 above         0.0
RIGHT BRANCH (control)   r 6..11 above        0.0
RIGHT BRANCH (control)   r11..16 above        0.0
```

Same curve, same frame: the undotted right branch carries its gray **on** the stroke
(r 0-3) and **zero** above at r 3-16, while the dotted chain carries a one-sided soft
gray band **above** it at r 6-16 (338.8 px/100 fpx at r 11-16). Marks are hue-neutral
(spread ≤ 3) and separated from the dots by white valley columns. The element is real and
drawn; a no-arrow build (attempt-4 geometry) omits it — which is exactly why attempts 2,
3 and 4 were FAILED on `dot_sequence`/`min_cluster`. Seven straight strokes recovered by
PCA in `scratch/probe_arrow_endpoints_output.txt` (attempt 6 draws these verbatim).

### A2 — "iterate markers noticeably larger/heavier" (full-slide MAJOR 2) — **REFUTED**

`scratch/probe_dot_size_output.txt`, violet mask `(B>R+40)&(B>110)&(R<160)&(lum<210)`:

```
original dots:  w 13-15, h 14-15 fpx, equivalent diameter 13.9 / 14.2 / 13.9 / 14.2 /
                14.5 / 14.1 / 14.2 / 14.3 / 14.0  -> mean 14.15 fpx
render_6 dots:  w = h = 29 render px = 13.92 fpx (scale 2.0833), area 659-665
yellow dot:     original equivalent 11.9 fpx vs build 12.5
```

The recreation's markers are **0.2 fpx SMALLER** than the original's. The "enlarged
purple discs" reading comes from solid fill + crisp AA in the PPTX render versus the
original's video blur — not from a size error. No size fix is warranted; this finding is
judge context for the re-roll, not a defect.

### A3 — "arrowheads are not at the dots" (dot_sequence MAJOR 1) — REFUTED AS LITERAL FACT, CONFIRMED AS READABILITY

`scratch/probe_arrow_at_dots_output.txt`, r = 7-11 px annulus around each dot centre,
counts of non-white / non-violet-core / non-black pixels per quadrant (UR/UL/LR/LL):

```
dot1 19/27/30/16   dot2 25/29/31/19   dot3 28/29/32/13   dot4 33/29/27/20
dot5 23/36/24/23   dot6 23/37/26/23   dot7 20/33/25/28   dot8 20/29/15/7
dot9 29/16/24/21   yellow 33/37/46/35
```

Balanced across all four quadrants — no upper-right (arrow-direction) concentration at any
dot. There is **no localized arrowhead ink at the dots in the original either**; the PCA
stroke ends land 11-17 px from the next dot's centre (dot2 12.0, dot3 11.0, dot6 12.0,
dot7 11.5, dot8 13.5, dot9 16.8), i.e. ~4-10 px beyond its rim. "Co-located at a dot" is
the judge's holistic reading of IMG2's soft marks merging with the dots' blur.

What survives as a real defect: my chain *reads* as detached. Cause is measurable — each
attempt-6 shaft is a solid 2 pt `#ACACAD` line ending in a solid `custGeom` triangle
(L = 5 fpx), crisp where the original is a bundle of 1-2 px soft strokes, and each head
stops 5-17 px short of the next dot, so nothing visually joins the leader to the iterates.

### A4 — "effective duplicate descent path" (dot_sequence MAJOR 2) — REFUTED AS LITERAL FACT, CONFIRMED AS READABILITY

IMG2 also has two elements (black curve core, recreated to <1 px, + the one-sided soft
gray band proved in A1). The "duplicate" exists in the original too; the complaint is that
in IMG1 the two read as separate because the leader never touches the iterates. Fix in
the attempt-7 spec below (same root cause as A3).

### A5 — MINORs (curve weight, x-axis baseline in crop, dashed-leader top endpoint, label
placement, "+" position, right-arm extent) — no change

These are low-confidence or already-covered items: house chrome + axes were measured and
pass `house_chrome_check.py`; the crop-baseline and leader-endpoint notes are artifacts of
the crop's lower edge and of the original's own blur (the original's dashed leader also
starts beside, not on, the first dot). Carried as judge context for the re-roll.

## Ruling

Attempt 6 is **not certifiable**: two MAJOR legs FAIL. Six judged attempts are consumed
(2, 3, 4, 5, 6 with banked transcripts; attempt 4's `gen_status=passed` write at 04:25 was
premature — that attempt's `dot_sequence` and `min_cluster` crop legs are banked FAIL, and
deck 03 mandates a zoomed judge on every region). Per
`scripts/17_worker_instructions.md` line 333 → DB `gen_status=failed`, `last_error`, STOP;
the orchestrator re-dispatches.

## Attempt-7 fix spec (for the re-dispatch)

Do **not** revert to the no-arrow attempt-4 geometry: A1 proves the marks are real and
attempts 2/3/4 failed for their absence. Do **not** keep attempt 6's rendering: A3/A4 prove
it reads as a detached second path.

`scratch/probe_arrow_endpoints_output.txt` gives the original's actual stroke inventory —
and it is NOT "one line + one chevron per gap". The upper gaps are bundles of thin strokes:

```
gap dot1->dot2 : id17 (270,281)-(278,300) len20.6   id18 (270,289)-(276,301) len13.4
                 (plus main id14 (274,264)-(290,301) len40.3)
gap dot2->dot3 : id20 (290,319)-(301,333) len17.8   id21 (287,321)-(298,336) len18.6
                 (plus main id19 (295,310)-(313,333) len29.2)
gap dot3->dot6 : id22 (318,342)-(375,378) len67.4   [ONE stroke spanning dots 4-5]
gap dot6->dot7 : id30 (378,380)-(392,385) len14.9
gap dot7->dot8 : id31 (399,387)-(411,390) len12.4
gap dot8->dot9 : id32 (418,392)-(428,394) len10.2
gap dot9->min  : id33 (431,394)-(441,395) len10.0
```

So the reconstruction that should read like the original is:

1. Draw these measured strokes at **1 pt** weight (or thinner), color `#ACACAD`
   (measured median 172,171,173), **with no separate solid triangle heads** — the original
   has none; its perceived arrowheads are the stroke ends landing at the iterates.
2. Extend each stroke's lower end **onto the next dot** (overlap its rim by 2-3 fpx), so
   the leader is visually joined to the iterates — this simultaneously answers
   "arrowheads not at the dots" and "parallel duplicate path" by making ONE chained
   trajectory.
3. Respect the measured multiplicity: 2-3 thin strokes per gap in the upper region
   (dots 1-3), a single stroke across dots 4-5, single strokes below. Do not draw one fat
   leader where the original has two thin ones.
4. Optionally draw the chain *under* the dots (send-to-back) so the blue discs sit on it.
5. Keep everything else from attempt 6 (white graph box, curve trace, labels, chrome) —
   all other regions passed their legs in attempts 4-6.

Re-verify with `scratch/probe_arrow_decide7` logic on the new render (one-sidedness above
the chain must reappear at approximately the measured 80/339 per 100 fpx), then dispatch
the full slide + `dot_sequence` again before any certification.
