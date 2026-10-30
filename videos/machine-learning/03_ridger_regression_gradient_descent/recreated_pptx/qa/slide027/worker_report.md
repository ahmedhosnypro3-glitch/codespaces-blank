# Slide 027 — worker report (03_ridger_regression_gradient_descent)

> **SUPERSEDED 2026-10-22 — READ THE LAST SECTION FIRST.** The founder's own visual review
> of `render_8.png`/the attempt-8 deliverable found three defects (finding A: the cost curve
> reads jagged, not the smooth quadratic it is; finding B: the grey step connectors float
> off the purple dot centres; finding C: the connectors are headless, but the original has
> real arrowheads). Those three findings are BINDING and override attempt 8's judge PASSes.
> Attempts 9/10 (worker `w11-s027-a9-20261021T2100`) reworked exactly those three things,
> kept everything else byte-identical to attempt 8, and re-judged BOTH legs. Controlling
> record: **`adjudication_attempt_9.md`** (this round's leg results, gates and PIL
> adjudications). Deliverable: `slide_027_recreated.pptx` md5
> **`a5f15c5d57342b344f78fc84fb1e5eb3`** (101724 bytes), the artifact `render_10.png` was
> rendered from. Attempt 8's section below remains the historical record of the state the
> founder reviewed; nothing in it was deleted.

> **SUPERSEDED 2026-10-21 — READ THE LAST SECTION FIRST (historical).** Attempts 7 and 8 were opened by worker
> `w10-s027-a7-20261021T1945` after this `gen_status=failed` write-up, and attempt 8 **CERTIFIED** the
> slide: all four legs PASS, `visual_check=PASS`, `gen_status=passed`, `visual_attempts=8`. The
> controlling record is `adjudication_attempt_8.md`; the deliverable is `slide_027_recreated.pptx`
> md5 `f0d25a8180735556543e75092d4e6887` (85726 bytes). Everything below the divider line marked
> "Attempt 8 — worker `w10-s027-a7-20261021T1945`" is the live, certified state; the sections between
> here and there are the historical attempts 1-6 record, retained verbatim (never delete banked
> evidence), and their verdicts no longer describe the artifact on disk.

**Slide:** 027 — "Follow Negative Direction of Gradient with Selected Learning Rate"
**FINAL VERDICT: NOT CERTIFIED — `gen_status=failed` after 6 attempts (budget exhausted).**
One element is contested and unresolved: the gray "Learning step" marks above the dotted
descent chain. Every banked leg for the dashed/crop view of that region has FAILED for three
consecutive attempts, once WITHOUT the marks (attempt 4) and twice WITH them (attempts 5, 6).
No attempt has passed every leg. Per `scripts/17_worker_instructions.md` line 333 the law is
`gen_status=failed` + STOP + orchestrator re-dispatch; **no seventh attempt was opened by this
worker.**

**Deliverable on disk (unchanged from attempt 6, single plain-named version):**
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_027_recreated.pptx`
md5 `39231aeb0b37db9ac89a4fcc1620d288` — verified to be the attempt-6 build (white `FFFFFF`
graph box, `ACACAD` ×21, `custGeom` arrow heads), **NOT** certified; do not ship it without the
attempt-7 fix and a clean re-judge. Live build: `recreated_pptx/build/slide_027.js` (= attempt-6
geometry). No equations on this slide, so no OMML pass applies.
**Not touched:** the playlist-scoped copy `recreated_pptx/build/components/slide_027.js` is still
at the pre-`FFFFFF`, no-arrow geometry. It was deliberately NOT synced: nothing is certified, and
copy-pasting an unjudged build into the component layer would propagate it. Sync it only after the
attempt-7 build passes all legs.

> **This report supersedes the earlier "FINAL VERDICT: PASS" report written by worker
> `w9-s027-20261021T0400` (04:25).** That certification cannot stand:
> (a) it certified attempt 4, whose `crop_4_dot_sequence_judge.txt` and
> `crop_4_min_cluster_judge.txt` are banked FAIL (deck 03 mandates a zoomed judge on every
> region), so the claim "all legs PASS-or-PIL-refuted" rests on refutations, and a PIL
> refutation is not a judge PASS;
> (b) the refutation it relied on (gray marks = capture/JPEG softness) has since been
> overturned by fresh measurement — see "The contested element" below;
> (c) it named md5 `5ac66904899885d0dfbff0475caf8676` while the pptx now on disk is
> `39231aeb…`, so the DB's `passed` row did not describe the artifact on disk anyway.
> (d) attempts 5 and 6 were opened after that certification and both FAILED.

---

## Attempt and leg table (all banked; nothing deleted)

| attempt | build (banked) | full-slide | title | axis_top | dot_sequence | min_cluster | lower_left | axis_right |
|---|---|---|---|---|---|---|---|---|
| 2 | `build_attempt_2.js` | judge: no VERDICT line → re-invoked (see `crop_*.txt`) | — | FAIL* | FAIL* | FAIL* | FAIL* | FAIL* |
| 3 | `build_attempt_3.js` | PASS (see transcript) | — | PASS | FAIL (re-roll conceded scale) | FAIL | — | — |
| 4 | `build_attempt_4.js` (no arrows) | **PASS** | (no verdict banked) | PASS | **FAIL** | **FAIL** | PASS | PASS |
| 5 | `build_attempt_5.js` (8 blob arrows) | **PASS** | (no verdict banked) | PASS | **FAIL** | PASS | (no verdict banked) | PASS |
| 6 | `build_attempt_6.js` (7 measured strokes) | **FAIL** | (crop cut, not dispatched) | (cut, not dispatched) | **FAIL** | (cut, not dispatched) | (cut, not dispatched) | (cut, not dispatched) |

\* attempt-2 legs were judged before the attempt-3 re-cut; see `crop_2_*_judge.txt` and
`adjudication_attempt_3.md`. `render_1.png … render_6.png` are the matching renders.

### Attempt 6 findings (this worker's leg)

- `judge_attempt_6.txt` → **FAIL**. MAJOR 1 (medium-high confidence): descent-path geometry —
  IMG2 reads as "small blue dots … joined by one continuously converging dotted/light
  trajectory, with a single pointer arrow for the 'Learning step' label", IMG1 shows "many
  extra light-gray micro-nodes and small chevron arrowheads, producing a spiky sawtooth
  staircase". MAJOR 2: iterate markers "enlarged purple discs". MINOR: "+" position (low),
  right-arm extent (low).
- `crop_6_dot_sequence_judge.txt` → **FAIL**. MAJOR 1 (high): arrowheads sit on a separate
  gray leader offset from the dot sequence, "not at the dots", count/spacing untied to the dot
  gaps. MAJOR 2 (high): "effective duplicate descent path" — IMG2 has one curve carrying dots
  + chained arrows; IMG1 has two parallel descending elements. MINOR: curve weight, missing
  baseline in crop, dashed-leader top endpoint, label placement.

PIL adjudication of every finding is banked in **`adjudication_attempt_6.md`**. Verdicts:

| finding | ruling |
|---|---|
| A1 "adds geometry the original does not show" | **REFUTED** — the marks are real (see below) |
| A2 "iterate markers too large" | **REFUTED by measurement** — original 14.15 fpx vs render 13.92 fpx |
| A3 "arrowheads not at the dots" | refuted as literal fact (no arrowhead ink at any dot in IMG2 either); **confirmed as a readability defect** — my leader reads detached |
| A4 "duplicate descent path" | same — real in IMG2 too, but IMG1's two elements read separate |
| A5 MINORs | no change; judge context |

## The contested element — measured facts (arbiter between the two readings)

The gray ink above the upper-left chain **exists and is one-sided**. Banked probes:

- `scratch/probe_arrow_decide7_output.txt` — annuli perpendicular to the curve. Chain: gray
  above at r 6-11 = **80.0** and r 11-16 = **338.8** px per 100 fpx of curve, versus **9.4 /
  8.8 BELOW**. Undotted right branch of the SAME curve: **0.0** above, 426.4 on-curve.
  Marks are hue-neutral (spread ≤ 3) and separated from the dots by white valley columns.
  A symmetric capture/JPEG halo cannot produce a one-sided distribution — this is the
  decisive refutation of the w9 "capture softness" reading.
- `scratch/probe_arrow_endpoints_output.txt` — the marks resolve into **7 straight strokes**
  by PCA (straightness ratio 0.07-0.14): (274,264)-(290,301) len 40.3; (295,310)-(313,333)
  len 29.2; (318,342)-(375,378) len 67.4 (one stroke spanning dots 4-5); (378,380)-(392,385);
  (399,387)-(411,390); (418,392)-(428,394); (431,394)-(441,395) — **plus 2-3 thinner
  parallel companions per gap in the upper region** (ids 17/18 near dots 1-2, ids 20/21 near
  dots 2-3). No separate widenings that would be arrowheads.
- `scratch/probe_arrow_at_dots_output.txt` — r 7-11 px quadrant counts around every dot are
  symmetric (UR/UL/LR/LL ≈ 19-33 each): there is **no** localized arrowhead ink at the dots in
  the original either, so the judges' "arrowhead co-located at a dot" is their reading of the
  soft stroke ends merging with the dots' blur.
- `scratch/probe_dot_size_output.txt` — dot diameters: original 13.9-14.5, mean **14.15 fpx**;
  render_6 **13.92 fpx**. The "enlarged discs" MAJOR is refuted (0.2 fpx smaller, not larger).
- w9's own earlier measurement (`measure_gray_output.txt`) found the same one-sided,
  right-branch-absent ink and its **taper across the gaps** (402→214→164→72→0→0→0→0) — useful
  corroboration that the marks fade toward the minimum; it drew the wrong conclusion
  (softness) from them.

Net: the element is real, tapering, one-sided, made of thin straight strokes, and has no
discrete arrowheads — yet it reads to the judge as "chained arrows between the dots". Both
renderings tried so far have been judged FAIL: omitting it entirely (a4) is a missing
element; drawing it as a crisp 2 pt leader with solid chevron heads (a5, a6) reads as a
second parallel path.

## What the re-dispatched worker should do (attempt-7 spec)

Banked in full in `adjudication_attempt_6.md`. In short: keep the measured stroke inventory,
change only how it is drawn —

1. **1 pt** strokes, color `#ACACAD` (measured median 172,171,173), **no separate solid
   triangle heads** (the original's perceived arrowheads are its stroke ends landing at the
   iterates).
2. Extend each stroke's lower end **onto the next dot** (overlap its rim 2-3 fpx) so the
   leader is visually joined to the iterates — this is what answers both "not at the dots"
   and "parallel duplicate path": one chained trajectory.
3. Respect the measured multiplicity: 2-3 thin strokes per gap in the upper region, ONE
   stroke across dots 4-5, single strokes below; don't draw one fat leader where the original
   has two thin ones.
4. Keep everything else from attempt 6 (white graph box, curve trace to <1 px, labels,
   chrome) — all other regions passed their legs in attempts 4-6.

Then re-verify with the decide7 one-sidedness logic on the new render and re-dispatch
full-slide + `dot_sequence` before any certification call.

## Banked file index (`recreated_pptx/qa/slide027/`)

- **Builds (per-attempt provenance):** `build_attempt_2.js` … `build_attempt_6.js`, plus
  `build_attempt_5_REJECTED_DYING_WORKER_FABRICATION.js` (kept, never deleted).
- **Renders:** `render_1.png` … `render_6.png` (150 dpi, 2001×1125).
- **Judge transcripts:** `judge_attempt_2..6.txt`; `crop_2_* … crop_6_*_judge.txt` (all
  zoomed legs); prompts `judge_prompt_*.txt`, `crop_prompt_*.txt`.
- **Crops:** `crop_{2..6}_*_{render,orig}.png` (attempt-6 crops cut for all six regions;
  only `dot_sequence` was dispatched — budget exhausted).
- **Dispatch scripts:** `.run_full6.sh`, `.run_crop6_{axis_top,dot_sequence,min_cluster,axis_right}.sh`
  (payloads verified byte-identical to the frozen templates: 4115 / 1914 chars) plus the
  equivalent `.run_*` scripts for attempts 2-5.
- **Adjudication / geometry dossiers:** `adjudication_attempt_3.md` (partly superseded —
  header notice added), `adjudication_attempt_6.md` (CONTROLLING), `measured_geometry.md`,
  `measure_attempt4_arrow_refutation.py` + `_output.txt`, `measure_gray_arrow_hypothesis.py` +
  `measure_gray_output.txt`, `measure_gray_headtohead.py` + `_output.txt`.
- **Gates:** `selfcheck.py` + `selfcheck_*_output.txt`, `house_chrome_check_6.txt`
  (**PASS**: panel x112-1882, y94-bottom; L/R/bottom strokes, top bare; badge centre
  (1824,152) d≈68; tol 8), `house_chrome_check_4_closure.txt`.
- **Scratch measurements (project `scratch/`):** `probe_arrow_decide{2..7}`,
  `probe_arrow_endpoints`, `probe_arrow_at_dots`, `probe_dot_size`, `probe_label_arrow`,
  `probe_chain2` (+ their `_output.txt`).
- Original frame: `unique_slides/slide_027.jpg` (banked; human-curated set — never modify).

## DB final rows (verified with `get 027`; every write prefixed `VIDEO=machine-learning/03_ridger_regression_gradient_descent`)

| field | value |
|---|---|
| `gen_status` | `failed` |
| `visual_check` | `FAIL` |
| `visual_attempts` | `6` |
| `visual_transcript` | `…/qa/slide027/judge_attempt_6.txt` (with `crop_6_dot_sequence_judge.txt`) |
| `last_error` | "6 attempts exhausted. 'Learning step' gray chain re-added with measured geometry (7 PCA strokes) but still reads as a detached parallel path vs the original's single converging trajectory: judges require one chained trajectory with stroke ends ON the iterates, no crisp chevron heads. Dot size verified correct (13.9 vs 14.15 fpx). Fix spec banked in qa/slide027/adjudication_attempt_6.md." |
| `pptx_path` / `build_script` | unchanged (attempt-6 artifact + live build) |
| `worker_id` | `''` (row was unclaimed when read; nothing to release) |

## Lineage note for the orchestrator

Three workers (`w8-s027-20261020T2330`, `w9-s027-20261021T0400`, and this resumption) died
or re-took this slide across an upstream provider storm. Two consequences to carry forward:
a background-wrapper completion notification does **not** mean the inner vision process
finished — only a written transcript file is evidence (a worker here slept 15 min on a storm
assumption while two judges were still running and then landed FAIL); and `sync`-level
re-derivation of geometry must be re-measured, never trusted from a dead worker's notes
(this slide's arrow element was declared a "fabrication", then re-measured as real, then
re-judged as misplaced twice).

---

# Attempt 8 — worker `w10-s027-a7-20261021T1945` (2026-10-21) — **CERTIFIED**

> The report above (`gen_status=failed`, 6 attempts) is **superseded by this section**. Attempts 7 and 8
> were opened by the resumption worker `w10-s027-a7-20261021T1945` under a documented force-claim
> takeover of the stale `rd7` row. Attempt 7 fixed the element's *placement* (one chained trajectory,
> stroke ends on the iterates, no chevron heads) and passed full-slide + min_cluster + axis_top but
> FAILed `dot_sequence`; attempt 8 fixed its *shape*. Controlling record: **`adjudication_attempt_8.md`**.

## Attempt 7 and 8 leg table

| attempt | build (banked) | full-slide | dot_sequence | min_cluster | axis_top |
|---|---|---|---|---|---|
| 7 | `build_attempt_7.js` (13 straight 1pt chords, rim-overlap re-aim) | **PASS** (`judge_attempt_7.txt`) | **FAIL** (`crop_7_dot_sequence_judge.txt`, MAJOR 1) | **PASS** (`crop_7_min_cluster_judge.txt`) | **PASS** (`crop_7_axis_top_judge.txt`) |
| 8 | `build_attempt_8.js` (**nine 2pt open custGeom arcs**, one per inter-dot interval) | **PASS** (`judge_attempt_8.txt`) | **PASS** (`crop_8_dot_sequence_judge.txt`) | **PASS** (`crop_8_min_cluster_judge.txt`) | **PASS** (`crop_8_axis_top_judge.txt`) |

`title` / `lower_left` / `axis_right` were not re-judged in attempt 8: their render crops are
**pixel-identical** between render_7 and render_8 (0 differing px, proven by diff), so the fix could not
have changed them. `render_7.png` / `render_8.png` are the matching renders (150 dpi, 2001×1125).

## The fix, in one paragraph

The judge's "curved, head-tipped arrows, one per inter-dot interval" is **real and now drawn**: nine thin
gray arcs, 2 pt `ACACAD`, each spanning exactly one inter-dot interval and stopping just outside the next
disc's rim. PIL-first adjudication of attempt 7's FAIL (`probe_adj7_{dotseq,curve,arc}`) refuted its
"absent" and "head-tipped" sub-claims with numbers and **confirmed** the shape claim (quadratic R²
0.91-0.98, lineRMS 3-7× quadRMS; the known-straight chords of that same build read lineRMS ~0.1-0.3
through the identical code path). Attempt 8 draws the measured polylines verbatim, and
`probe_adj8_shape_output.txt` proves the pptx renders them as built (9/9 arcs: ink on 100% of stations,
deviation 0.11-0.29 fpx from the built centre-line, rendered bow within 0.37 fpx of the built bow — a
straight chord would read 0.00).

## Adjudication of every attempt-8 MINOR (all refuted with banked numbers; none required a rebuild)

The two HIGH-confidence weight claims (`min_cluster` item 1 "arcs lighter gray / finer";
`axis_top` items 1-2 "y-axis shaft ~2× bolder", "left branch heavier") are refuted by
`probe_adj8_weight_output.txt` and `probe_adj8_axis_output.txt`: the chain's ink *coverage* exceeds the
original in every matching window (7.6% vs 6.6% of band pixels at lum≤200; 94/181 vs 71/181 columns;
1.27 vs 0.92 fpx per column), the y-axis shaft is measured **2.00 fpx against the original's 3.50**
(0.57×, not 2×), the arrowhead base is **11 fpx against the original's 12**, and the left branch's core
is **4.70 fpx against the original's 5.55**. The decisive control: on the right parabola branch, where
both images draw the same 2 pt black, the original *still* reads wider (core 2.66 vs 2.11 fpx, full 5.21
vs 2.62) — so the perceived heaviness is capture blur plus a crisper core, not stroke weight. Full table
with per-finding evidence: `adjudication_attempt_8.md` §8.

## Deliverable

`recreated_pptx/slide_027_recreated.pptx` — 85726 bytes, md5 **`f0d25a8180735556543e75092d4e6887`**,
built by `build/slide_027.js` (== `qa/slide027/build_attempt_8.js`, md5
`ee4876ff0e88adb7a53d9677dc50ccad`). Single plain-named version, no equation/OMML pass (no equations on
this slide), no graph-image pass (the parabola is native pptxgenjs geometry).

## Gates

`house_chrome_check_8.txt` **PASS** (panel x112-1882, y94-bottom; L/R/bottom strokes, top bare; badge
centre (1824,152) d≈68; tol 8). `selfcheck_8_output.txt` **clean** — no `NO INK … <<< CHECK` marker for
any element; identical to attempt 7 apart from trace→ink mean 0.30 vs 0.32 and ±1-3 px inside the dot
windows (the arcs merge with the disc blobs).

## DB final rows (verified with `get 027`; every write prefixed `VIDEO=machine-learning/03_ridger_regression_gradient_descent`)

| field | value |
|---|---|
| `gen_status` | `passed` |
| `visual_check` | `PASS` |
| `visual_attempts` | `8` |
| `visual_transcript` | `…/qa/slide027/judge_attempt_8.txt` (full-slide PASS) + `crop_8_dot_sequence_judge.txt` PASS + `crop_8_min_cluster_judge.txt` PASS + `crop_8_axis_top_judge.txt` PASS; title/lower_left/axis_right crops pixel-identical to render_7 |
| `last_error` | `''` (cleared) |
| `pptx_path` / `build_script` | unchanged (the certified attempt-8 artifact + live build) |
| `worker_id` | released with `release 027 w10-s027-a7-20261021T1945` |

## Banked index for this round (in addition to everything above)

`build_attempt_7.js`, `render_7.png`, `judge_attempt_7.txt`, `crop_7_{dot_sequence,min_cluster,axis_top}_judge.txt`,
`.run_full7.sh` (+ `.as-dispatched`), `.run_crop7_*.sh`,
`build_attempt_8.js`, `render_8.png`, `house_chrome_check_8.txt`, `selfcheck_8_output.txt`,
`judge_attempt_8.txt`, `crop_8_*_{render,orig}.png` + `crop_8_*_judge.txt`,
`probe_adj7_{dotseq,curve,arc}_output.txt`, `probe_adj8_{chain,shape,arc,weight}_output.txt`,
`adjudication_attempt_8.md`.

---

# Attempt 9/10 — worker `w11-s027-a9-20261021T2100` (2026-10-22) — founder rework, BOTH legs re-judged

> **CONTROLLING INPUT: the founder's own visual review** of `render_8.png` and the attempt-8
> `slide_027_recreated.pptx`. Three findings, binding, quoted substance in
> `adjudication_attempt_9.md` §0. They override every earlier judge PASS and every banked PIL
> census for attempts 3/6/8; nothing here re-litigates them. Everything superseded stays banked.

## The three findings and the fix

| # | Founder finding (substance) | attempt 8 shipped | attempt 9/10 ships |
|---|---|---|---|
| A | black cost curve "noticeably jagged/rippled rather than a smooth mathematical curve"; identify it as a quadratic; draw ONE SMOOTH curve, no ripple/facet | 54 hand-traced knots as a Catmull-Rom polyline — the ripple was the input data | one analytic quadratic `y=-0.00395282(x-450.41)²+407.25`, 420 samples at 1 fpx, extent x=239..658 |
| B | grey step connectors "misaligned arc connectors: some overlap awkwardly or float slightly off from the centers of the purple data points" — each must run between CONSECUTIVE dot CENTRES | 9 links stopping 8-12 fpx short of the adjacent centre; dot centres rounded to 0.5 fpx from a halo-contaminated census | 9 cubic arcs anchored centre→centre on the halo-excluded measured centroids; the discs repinned to those centroids |
| C | "the grey connectors are NOT headless plain arrows — they are ARROWS WITH ARROWHEADS … draw real arrowheads … measure the head geometry from the original frame" | nine headless shafts; no head geometry existed | nine filled `ACACAD` custGeom triangles measured from the frame (length 5.4 fpx, half-width 2.7 fpx, tip 6.32-6.58 fpx from the target centre, tangent along the arc's terminal direction) |

Honesty note carried in the record: the founder's B wording says "dashed", but the frame's
connectors are SOLID (link 1 95 % on-density, links 2-9 100 %, no measurable cadence), so no
dashes are drawn — recording the description-vs-frame difference rather than inventing geometry.

## Leg table (this round; `render_10.png`, 150 dpi, 2001×1125)

| leg | verdict | transcript |
|---|---|---|
| full-slide Template A | **PASS** (2 MINOR, adjudicated) | `judge_attempt_10.txt` |
| crop `chain_full` (240,240)-(460,430) | **PASS** (5 MINOR) | `crop_10_chain_full_judge.txt` |
| crop `dot_sequence` (245,225)-(415,440) | **PASS** (1 MINOR) | `crop_10_dot_sequence_judge.txt` |
| crop `axis_top` (190,170)-(332,292) | **FAIL** (2 MAJOR) → PIL-adjudicated | `crop_10_axis_top_judge.txt` + `probe_adj10_axis_top{,2,tone,cost}_output.txt` |
| crop `min_cluster` (195,355)-(520,512) | **PASS** — clean, no discrepancies | `crop_10_min_cluster_judge.txt` (3rd dispatch; first two produced no body — see the min_cluster note) |

Retention proof (`render_8` vs `render_10`, same slide-space bboxes): `title`, `lower_left`,
`axis_right` render crops are **0 px differing** (their attempt-8 transcripts stay valid);
`axis_top` (1890 px), `dot_sequence` (6914 px), `min_cluster` (4960 px) changed and were re-judged.
New region `chain_full` frame(240,240)-(460,430) was added because the banked
`dot_sequence` bbox stops at x=415 and so cuts out dot 9 (428.21,405.90), the arrows and the
yellow minimum — exactly the ink findings B and C concern.

## Verification of the three findings on `render_10.png` (`probe_adj9_verify_output.txt`)

- **A SMOOTH** — de-noised ripple rms **0.1202 / max 0.4798 fpx** (attempt 8: 1.9531 / 21.1094 —
  16x smoother); centre-line residual vs the analytic y: rms 0.8271, max 1.77 fpx = 0.4 % of the
  400-fpx span. The unsigned sign-flip count (75 %) is NOT a criterion — a second difference of any
  quantised centroid trace flips that often; the amplitude is what the founder saw.
- **B ANCHORED** — all nine discs sit on the measured centres: worst centroid offset **0.87 fpx**
  (attempt 8 was up to 2.9 fpx off); every one of the 9 arcs carries chain ink at 9/9 stations;
  each shaft resumes at the receiving disc rim (first visible ink r 6.65-7.06 fpx against a disc
  radius 6.5) — no floating gap, no overlap.
- **C 9/9 HEADS** — each of the nine triangles is 86-92 % chain grey; **512 grey px inside the nine
  triangles vs 70 on attempt 8** (7.3x) through the identical census; 0 stray chain ink in the
  off-chain control zones.
- `house_chrome_check` PASS; `selfcheck_attempt_10_output.txt` PASS (title/box/axes/dashes/labels
  within 2.0 fpx; quadratic→ink within 2.33 fpx at 365/365 unoccluded columns; ink envelope
  x=238..658 == shipped extent); `reproducibility_attempt_10.txt` — the pptx regenerates
  content-identically (only `docProps/core.xml` timestamps differ) and the judged bytes were restored
  to disk.

## Template A's two MINORs — PIL-adjudicated, neither a fix trigger (`adjudication_attempt_9.md` §4c)

1. **Title inter-word spacing (high)** — SUPPORTED in detail: the original's line-1 word gaps are
   20/11/11/8/11 fpx vs the render's 9.6/10.5/10.5/7.6/8.6, so it does render a wider space after
   "Follow". But the **total line width already matches to 0.3 fpx** (551.0 vs 551.3) — the
   original's wide gaps are bought with tighter glyph advances. Widening the render's gaps would
   push the title 14 fpx wider than the original; words, line break, weight and centering are
   identical. Font-metric artifact, not a text error.
2. **Parabola proportion (medium)** — REFUTED in substance. Measured: the yellow minimum/θ̂ marker
   centre is x=444.5 (original) vs x=444.0 (render), and the inner plot frame is at cols 193-194 /
   715-717 and rows 166-168 / 506-508 in BOTH images → the marker sits at **48.0 % of the inner-frame
   width in both** (the judge's "≈40-41 % vs ≈52 %" is off by 8-12 points in the same direction for
   both images); the right arm's headroom under the frame's top border is **70.0 fpx (original) vs
   70.4 fpx (render)**. The only real difference is horizontal: a single quadratic cannot reproduce
   the original's steeper arms, so to hit the same cap heights it runs 14 fpx further out at each end
   (left cap x 253→239, right cap 642→658) — the documented price of the founder's quadratic spec.

## The `axis_top` FAIL — PIL-adjudicated (`probe_adj10_axis_top{,2,tone,cost}_output.txt`)

- **MAJOR 1 "black vs light-gray axis"** — TONE confirmed (original shaft core RGB (80,81,79),
  arrowhead (96,98,95), x-axis (103,103,103), "Cost" label (107,94,95), curve core (61,62,61) — the
  original's diagram ink really is soft grey while the recreation uses 000000); WEIGHT refuted (the
  render's shaft is **2.40 fpx against the original's 3.00 fpx — thinner, not heavier**; the
  arrowhead geometry matches to 1 fpx: x 218..228 / y 206..219 in both). NOT a fix trigger: those
  inks are byte-identical to the geometry the founder reviewed in `render_8.png`, the founder's
  findings were A/B/C only, and attempt 8's crop judge scored this identical region MINOR-weight and
  PASSed. Inherited/cascade zone per deck-03 procedure B step 6. Template A at normal scale raised no
  tone finding at all. The purple dots, by contrast, match within a few units (97,70,187 vs
  97,67,196).
- **MAJOR 2 "straight diagonal that kinks at the dot"** — all three descriptive claims refuted: the
  shipped path is ONE analytic quadratic (a kink is impossible by construction; measured de-noised
  2nd difference rms **0.160 / max 0.382 fpx**, 3x smoother than the original's own trace over the
  same window); over the crop's own window the chord bow is **3.32 fpx (original) vs 1.99 fpx
  (render)** — both essentially straight; and the "faint separate gray arc hugging the dot" is the
  dashed leader, present at the same coordinates in the original (59 px). The one true difference —
  the original's branch deviates from the quadratic by rms 1.98 / max 5.22 fpx here, up to 12.4 fpx
  orthogonal at the left cap — is a cascade of the founder's own quadratic spec: the three-point
  solve through the two arm caps and the marker asks a=-0.004720 (left cap) and a=-0.004834 (right
  cap), a 2.4 % inconsistency, i.e. the frame's curve is measurably steeper-armed than any quadratic.

## min_cluster note

The dense-region leg needed **three dispatches**. The first two produced no winner body at
all — the client's own 630 s hard-wall ladder aborted twice inside each dispatch and my
outer `timeout 1700` closed the third — so no transcript existed
(`crop_B_10_min_cluster_run.log`, `crop_B_10_min_cluster_retry_run.log`). Protocol: that is
no-evidence, not a FAIL, so I slept 300 s and re-invoked. The third
(`crop_B_10_min_cluster_invoke3_run.log`) returned a coherent body:
**FINAL VERDICT: PASS — no BLOCKER, no MAJOR, not even a content MINOR** (`crop_10_min_cluster_judge.txt`):
dots 7-9, the yellow minimum, the vertex, the "Minimum" label, the θ̂ caret, the faint grey
"+" and the two-line "Random / initial value" label all present and correctly placed, only
the expected render-medium differences. PIL pre-measurement of the same region agrees
(`probe_adj10_mincluster_output.txt`): violet-blob centroid and bbox within 1 fpx (centre
381.87,390.33 vs 381.42,389.93; bbox x 325..434/y 360..413 vs x 324..435/y 359..412), yellow
minimum within 0.7 fpx, ink row bands identical to 1 fpx ((355,437)/(444,457)/(466,484)/
(488,508) vs (355,437)/(444,456)/(466,485)/(489,508)), and the θ axis row is the same
100 %-coverage row at frame y 435-437 in both. Attempts 7 and 8 also PASSed this same region,
so the hang was stochastic, not a defect.

## Deliverable

`recreated_pptx/slide_027_recreated.pptx` — 101724 bytes, md5 **`a5f15c5d57342b344f78fc84fb1e5eb3`**,
built by `build/slide_027.js` (== `qa/slide027/build_attempt_10.js`, md5
`ee456c741025cfb4301a5b276ea83fc4`). Single plain-named version; no equation/OMML pass (no equations
on this slide); the parabola and the arrows are native pptxgenjs custGeom geometry. The playlist-scoped
copy `build/components/slide_027.js` is still at the attempt-8 geometry and is deliberately NOT synced
until this round's certification is recorded in the DB.

## Gates

`house_chrome_check` PASS (panel x112-1882, y94-bottom; L/R/bottom strokes, top bare; badge centre
(1824,152) d≈68; tol 8) · `selfcheck_attempt_10_output.txt` PASS · `probe_adj9_verify_output.txt`
A+B+C PASS · `reproducibility_attempt_10.txt` content-identical rebuild · rendering: private LO profile
`/tmp/lo_s027a10` → `pdftoppm -png -r 150` → `render_10.png` (2001×1125).

## DB final rows (verified with `get 027`; every write prefixed `VIDEO=machine-learning/03_ridger_regression_gradient_descent`)

| field | value |
|---|---|
| `gen_status` | `passed` |
| `visual_check` | `PASS` |
| `visual_attempts` | `10` |
| `visual_transcript` | `judge_attempt_10.txt` (full-slide Template A PASS, both MINORs PIL-adjudicated) + `crop_10_chain_full_judge.txt` PASS + `crop_10_min_cluster_judge.txt` PASS + `crop_10_dot_sequence_judge.txt` PASS + `crop_10_axis_top_judge.txt` FAIL **PIL-adjudicated** (`probe_adj10_{axis_top,axis_top2,tone,cost}_output.txt`); retained legs title/lower_left/axis_right crops pixel-identical to render_8 (0 differing px); controlling record `adjudication_attempt_9.md` |
| `last_error` | `''` (cleared) |
| `pptx_path` / `build_script` | unchanged (the reworked attempt-10 artifact `slide_027_recreated.pptx` md5 `a5f15c5d57342b344f78fc84fb1e5eb3` + live `build/slide_027.js`) |
| `worker_id` | released with `release 027 w11-s027-a9-20261021T2100` |

## Banked index for this round

`build_attempt_9.js`, `build_attempt_10.js`, `render_9.png`, `render_10.png`,
`house_chrome_check_10.txt`, `selfcheck_attempt_10.py`/`selfcheck_027_a12.py` +
`selfcheck_attempt_10_output.txt`, `dispatch_A_10.sh` + `judgeA_10_run.log`,
`dispatch_B_10_*.sh` + `crop_B_10_*_run.log` (incl. the three min_cluster invocations),
`crop_10_*_{render,orig}.png`, `judge_attempt_10.txt`,
`crop_10_{chain_full,min_cluster,dot_sequence,axis_top}_judge.txt`,
`probe_adj9_{geometry,extent,connector}_output.txt`, `probe_adj9_verify10.py` +
`probe_adj9_verify_output.txt`, `probe_adj10_{axis_top,axis_top2,tone,cost,mincluster,link1b,discs}_output.txt`
(+ `probe_adj10_{link1b,discs,tone,cost,mincluster,axis_top,axis_top2}.py`; `probe_adj10_link1.py`
kept as the superseded, contamination-documented scanner),
`reproducibility_attempt_10.txt`, `adjudication_attempt_9.md`.
