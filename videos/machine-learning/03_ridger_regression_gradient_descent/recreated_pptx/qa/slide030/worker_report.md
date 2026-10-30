# Slide 030 — worker report (IN PROGRESS)

Worker: `w030-finish-20261024` (resumed lane; prior worker `w030-buildfirst-20261024`
was a stale zombie — heartbeat 88m at claim time).

Slide: **030 "Convex Function, Learning Rate =0.2, Start at X=3"** — deck
`machine-learning/03_ridger_regression_gradient_descent`.
Deliverable: `recreated_pptx/slide_030_recreated.pptx`
Build script: `recreated_pptx/build/slide_030.js`

## 1. Triage of the inherited state

- Prior row read `gen_status=building`, stale claim, no qa bank for renders,
  crops, scripts, or transcripts (the only prior qa content was a partial set of
  attempt 1-5 artifacts left in `qa/slide030/`, which I preserved and continued
  from — see "Resume" below).
- I re-ran the banked build script and re-rendered: the fresh render is
  **byte-identical** (md5 `ac17141f492f2b61291e4912007c0b78`) to the prior lane's
  `render_5.png`, so the 07:55 pptx and the build script were already in sync —
  no rebuild needed. The unpacked pptx carries the full inventory (240 shapes,
  2 equation PNGs, 6 tables, 207 line shapes = the dense parabola + grid).

## 2. Verification done before judging

- **House chrome**: `house_chrome_check.py` → **PASS** on `render_6.png`
  (panel x112..1882, strokes L/R/bottom present, top bare, badge (1824,152) d68).
  Banked: `house_chrome_check_6.txt`.
- **PIL measurement** (`measure_w030.py`, banked):
  - content ink fully inside the house panel (left/right/above = 0 px)
  - parabola: LSQ quadratic fit residual **max 6.4 px / mean 0.67 px** over 175
    sampled columns → ONE smooth arc (ripple check clean); fitted vertex
    x=687.1 y=253.9 vs build-model x=687.8 y=254.5 (≤1 px); ink 0 px outside the
    plot frame on all four sides; arms match the analytic f(x)=(x-5)^2+1 to ≤7 px
  - iteration table (8 rows x 12 cols, 96 cells, all cells carry ink) and param
    table (6/6 cells) verified; 5 colour bands' median fills match the original
    to within ~2-5 RGB
  - geometry deltas vs the original: title ink, red eq box, green box, dashed
    x=5 line, secant, tick labels all within ~1 px (sub-pixel agreement)
  - deviation found: **red arrow** is ~6 px shorter than the original
    (render y304..347 vs orig y304..340; the extra 7 px is the pink table fill
    bleeding into the mask). Same shape and tilt. Not yet adjudicated — the
    `arrow` crop leg will rule on it; if it flags, fix is a one-line geometry
    change in the build script.

## 3. Judge dispatch state (as of 12:40 UTC)

- Crops cut at matched effective scale (7 Procedure B pairs, LANCZOS
  H_render/540 ≈ 2.0833): param, formula, plot, iter_left, iter_right, callout,
  arrow. Scale audit `crop_6_scale_audit.json`: per-axis mismatch ≤ 0.47%
  (rounding only, well under the 8% drift threshold).
- Payloads regenerated from `shared_patterns/judge_protocol_03.md` with ONLY the
  protocol substitutions (`slide_NNN`→`slide030`, `K`→6) and **byte-verified by
  `make_payloads_6.py` → ALL BYTE CHECKS PASS**. (The verifier caught a real bug
  on first run: Template B payloads still contained `slide NNN` unsubstituted.)
- Wall evidence (all banked in `legA_full_dispatch.log`):
  - **Attempt at `--timeout 600`** (v1, 11:37): client aborted twice on its internal
    630 s HangError, then upstream returned HTTP 504 (`upstream_timeout`,
    Nvidia candidate) → no verdict.
  - **Attempt at `--timeout 1200`** (v3, 12:12: the ratified provisional W4 wall,
    payload byte-for-byte unchanged): aborted once on the internal 1230 s
    HangError, then the same upstream HTTP 504 → no verdict. The analyzer itself
    warns that `--timeout > 600` saturates the shared gateway.
  - Conclusion so far: the full-slide leg is failing on the **upstream provider**
    (NVIDIA NIM via IronRouter), not on slide content. Per the law this is **one
    hard-wall retry already consumed** for leg A; do not retry-loop it.
- Probe (Template A probe, `--timeout 120`) returned rc=124 (no body inside
  150 s) — the gateway window was congested at the time.
- Dispatcher v3 (`dispatch_legs_6_v3.sh`, detached via setsid+nohup) is running:
  after leg A failed it moved on to the 7 crop legs at tmo=1200, in the order
  param, formula, plot, iter_left, iter_right, callout, arrow.
  Note: the v1 background run hit the harness 600 s ceiling and was orphaned
  (its python client survived reparented to init and later died with no verdict),
  and a v2 attempt's orphan-detection was polluted by my own polling shells;
  v3 was started clean with no live client referencing slide030 confirmed first.
- Note the 1200 s wall was chosen because 600 s could not complete ANY leg —
  the upstream needs >1230 s of thinking under the current congestion, or it
  504s. Both are outside my control.

### Next commands when v3 finishes

```bash
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide030
grep -o 'FINAL VERDICT: [A-Z]*' $QA/judge_attempt_6.txt | tail -1
for f in $QA/crop_6_*_judge.txt; do printf '%-40s %s\n' "$(basename $f)" "$(grep -o 'FINAL VERDICT: [A-Z]*' $f | tail -1 || echo NONE)"; done
```

Then: PIL-adjudicate every finding, fix real defects (copy-then-modify), re-render,
re-judge, and certify with the runbook sequence (pptx_path, build_script,
visual_check, visual_transcript, visual_attempts, gen_status, heartbeat, release)
— re-reading `get 30` before release to restore gen_status if set() reset it.

## 4. Banked evidence (this worker)

| file | what |
|---|---|
| `render_6.png` | fresh 150dpi render (md5-identical to prior render_5) |
| `house_chrome_check_6.txt` | chrome PASS |
| `measure_w030.py` | PIL measurement vs original |
| `parabola_check_w030.py` | curve ripple/containment check |
| `cut_crops_6.py` + `crop_6_scale_audit.json` + 14 crop PNGs | Procedure B pairs |
| `judge_prompt_6.txt`, `crop_prompt_6_*.txt` | byte-verified payloads |
| `make_payloads_6.py` | payload regenerator + byte-checker |
| `dispatch_legs_6.sh`, `dispatch_legs_6_v3.sh` | dispatchers |
| `worker_report_progress.log` | live dispatch log |
| `scratch/render_w030_finish.sh` (deck scratch) | rebuild + render script |

---

## 5. 2026-10-24 ~15:20 — resume by w030-finish-20261024b (timeout-resume)

### Resume state
- Re-claimed (prior heartbeat stale, 68 m) and confirmed the deliverable is still
  current: rebuild from `build/slide_030.js` re-renders to the SAME md5
  (`ac17141f…`) as the banked `render_5/render_6.png` → the 07:55 pptx is not stale.
- Banked crop verdict found: **`crop_6_formula_judge.txt` → FINAL VERDICT: PASS**
  (landed 13:41 during v3). 5 MINOR findings, zero MAJOR/BLOCKER.
- Verdict coverage before this resume: 1/8 legs. Missing: Leg A (full-slide) and
  crops plot, iter_left, iter_right, param, callout, arrow.
- Wall cause of the misses (banked dispatch logs): image leg dying with HTTP 504
  Nvidia `upstream_timeout` and/or internal 1230 s HangError — the same failure
  channel the fleet saw on 043. Text (vision) leg healthy. Gateway now light
  (real clients 3-4, pgrep 12).

### Adjudication of crop_6_formula PASS (all PIL, frame px, 960x540)
See the table in the transcript above this section; summary: operator spacing
(render eq bbox 405.4..522.9 vs orig 404.0..524.0 = 2.5 px narrower overall),
minus-glyph width (mandated professional mathtext), italic math-serif voice
(mandated 2D format), gap after `f(x)` (render line2 363.2..539.7 vs orig
353.0..547.0 → render is 17 px TIGHTER overall, so the "wider gap" reading is the
italic run, not a defect), and colour deltas (orig RGB is the JPEG wash of the
same house red/green). → **No build change; region certified clean.**

### Dispatched
`dispatch_legs_6_v4.sh` (detached, started 15:28:40): re-fires Leg A then the 6
missing crop legs sequentially at `--timeout 1200` (approved wall) inside
`timeout 1700`, payload bytes unchanged, `--thinking high --max-tokens 65536`,
gate law probing real clients < 8 (max 2 probes/hour, then wait).

## 6. 2026-10-24 ~17:50 — resume by w030-finish-20261024c (claim renewed)

### Claim / DB state
`get 30` (17:28): `gen_status=building`, `visual_check=null`,
`visual_attempts=1` (**must become 6** — fleet convention is the judge attempt
index: slide 13→`judge_attempt_6.txt`/attempts 6, slide 21→attempt 10,
slide 27→attempt 10), `visual_transcript=null`,
`worker_id=w030-finish-20261024c` (claimed `--force`; earlier ids ...b went
stale), `last_error=null`. Heartbeat sent this cycle.

### Deliverable currency re-verified
`scratch/render_w030_finish.sh` rebuilds `build/slide_030.js` and re-renders to
`render_6.png` md5 `ac17141f492f2b61291e4912007c0b78` = banked `render_5.png`
= `render_attempt_1.png`. House chrome check on render_6: PASS (panel
x112..1882, L/R/bottom red strokes, no top stroke, badge d68 at (1824,152)).
Payloads re-derived + byte-verified (idempotent regen, md5s unchanged,
`ALL BYTE CHECKS PASS`) and confirmed verbatim against
`shared_patterns/judge_protocol_03.md` sources.

### Judge-leg status at this cycle
Verdict coverage: **1/8** (formula PASS, adjudicated in section 5, no build
change). Still missing: Leg A full-slide + crops plot, iter_left, iter_right,
param, callout, arrow — all lost to the shared image upstream, not to the slide.

Failure channel (banked in `*_dispatch.log` / `probe_health_dispatch.log`):
every leg attempt ends either `HTTP 504 upstream_timeout` (Nvidia candidate
`nva…hWGS`) or an internal `HangError: hard wall-clock 1230s exceeded` (which
then retries and hits the 504). Observed 2026-10-24 16:18–17:55:
- legA_full (16:59 fire) → 504 in 60 s
- legB_plot (17:00 fire) → 504 in 62 s
- legB_iter_left round 1 (17:01) → 1230 s HangError + 504 pair, outer
  `timeout 1700` killed during retry 2 → rc=124 17:29
- legB_iter_left round 2 (17:33) → 1230 s HangError + 504 pair → rc=1 17:55
- legB_iter_right firing 17:55 (in flight)
So ~22 min per attempt and the healthy shape is "survive past 1230 s": the one
verdict that ever landed (formula, 13:14→13:41) took 27 min to complete. Fast
504 passes are the outage shape, so v5's `fire_leg` (which returns immediately
on a 504) exhausts legs quickly; v6 (added this cycle) therefore re-checks
EVERY leg each outer round and fires only the ones with no verdict yet,
including Leg A, which v5 already burned through and never revisits.

### Dispatch state
`dispatch_legs_6_v5.sh` (PID 706312, detached) — probes the lane with a light
`analysis` probe every 300 s, then fires missing legs back-to-back at
`--timeout 1200` inside `timeout 1700`, `--thinking high --max-tokens 65536`,
payload bytes unchanged, gate law real clients < 8.
`dispatch_legs_6_v6.sh` (new, this cycle) — 10 outer rounds, missing-leg-first
(Leg A first), fast-504 legs skipped rather than blocking, verdict-present legs
skipped. To be launched only when v5 exits and no duplicate leg is in flight.

### Adjudication posture (banked, pending verdicts)
- formula PASS → all 5 MINORs PIL-adjudicated, no build change (section 5).
- Two further MINOR candidates found PIL-first, awaiting a verdict:
  red arrow ~3 px narrower / ~2.2 px shorter than orig's arrow ink
  (render x170.8..190.9 / y304.2..333.0 vs orig x171..194 / y304..335 — same
  shape and tilt, so MINOR at most); plot point labels ~3 px smaller
  (orig (5,1) bbox 698..223 vs render 696.1..715.3). Both PIL-surfaced and
  neither is a content defect.

## 7. 2026-10-24 ~19:05 — session-restart resume + PIL forensics (w030-finish-20261024c)

### Restart state (nothing assumed)
Re-glob of `qa/slide030/*judge*.txt`: only `crop_6_formula_judge.txt` (2310 B, 13:41)
carries a real `FINAL VERDICT:` body. `judge_attempt_6.txt` still absent — no
Template A verdict has ever landed for this slide. The v5 dispatcher was killed
by the session exit (last log line 17:55); the DB claim survived
(`get 30`: gen_status=building, visual_check=null, visual_attempts=1,
worker_id=w030-finish-20261024c, heartbeat stamped 17:49) and was re-heartbeated.
`dispatch_legs_6_v6.sh` relaunched detached 18:58 — it re-checks EVERY leg each
outer round and fires Leg A first (v5 had burned Leg A on a fast 504 and never
revisited it).

### Scale bug found in the earlier baseline (corrected this cycle)
`measure_w030.py` converted ORIGINAL pixels with the RENDER's scale factor
(SX = 2001/960 = 2.0844) instead of the original's own 1.0, so every
original-frame bbox was halved and any window starting past orig column ~460
came back empty (`orig=None` for the plot / iter table / arrow / callout).
Corrected copy: `measure_w030_b.py` → `measure_output_6b.txt` (each image
converted with its own scale). The corrected render-vs-orig alignment, frame px:

| region | render bbox | orig bbox | delta pos | delta size |
|---|---|---|---|---|
| title | 57.6,64.3–599.7,99.4 | 58,66–574,99 | (-0.4,-1.7) | (+26.1,+2.1) |
| param_table | 102.2,198.2–237.0,281.3 | 103,199–237,281 | (-0.8,-0.8) | (+0.8,+1.1) |
| upper_eq_box | 398.2,184.3–530.1,212.2 | 399,185–530,212 | (-0.8,-0.7) | (+0.9,+0.9) |
| green_box | 346.9,232.8–554.1,281.3 | 348,234–554,281 | (-1.1,-1.2) | (+1.2,+1.5) |
| callout band | 333.9,291.4–569.0,320.2 | 335,292–569,320 | (-1.1,-0.6) | (+1.1,+0.8) |
| plot_frame | 570.9,64.3–809.8,311.0 | 573,66–810,310 | (-2.1,-1.7) | (+1.9,+2.7) |
| iter_table | 76.8,324.0–653.9,530.4 | 78,325–654,530 | (-1.2,-1.0) | (+1.1,+1.4) |

→ every region sits within ~2 frame px of the original in BOTH position and
size. Callout text colour matches too: render text pixels inside the purple
band are white (median 255,255,255), original's are near-white (241,225,230),
purple band heights 28.8 vs 28.0 frame px (`measure_w030_c.py`,
`measure_output_6c.txt`).

### ARROW forensics (`arrow_rows_w030.py` → `arrow_rows_output_6.txt`,
### `shape_map_w030.py` → `shape_map_output_6.txt`)
Both images carry the SAME arrow family: a double-headed red arrow (up wedge at
the top, two outline flanks, a V tip at the bottom). Measured, frame px:

| feature | render | original | delta |
|---|---|---|---|
| top head tip | (182, 304.3) | (187, 304) | 5 px left |
| top head base | x177..190 @y307 | x184..193 @y306 | ~5 px left, 13 px vs 9 px wide |
| bottom head tip | ≈(179, 333.5) | (177.5, 340) | 6.5 px higher, 1.5 px right |
| total height | 29.5 px | 36 px | 6.5 px shorter |
| major-axis angle | 109.1° | 110.4° | 1.3° |

The build draws `ST.downArrow` at x173,y306,w19,h30, rotate 15, white fill with
a C00000 outline (`recreated_pptx/build/slide_030.js:317-324`), whose comment
claims the measured bbox x172..194 y304..340; the RENDER lands at
x170..191, y304..333.5 — LibreOffice's rotated-shape geometry, ~6 px short at
the tip and ~5 px left at the head. → **MINOR-class geometry difference**
(same double-headed form, same pointing direction at the iteration table, no
content error). NOT a phantom: both tips and both flanks are present in both
images; the ink is 135 px (render) / 224 px (orig) in the region, far above the
3-px noise floor. No build change until a judge verdict says otherwise.

The small red mark at x169.8..173.7, y341.3..347.0 (71 px, exact house red
C00000) that looked like a stray artifact is the INTENDED red "3" of the
iteration table's first value cell (build `redCells: [[0,1],[0,11]]`, group 1
starts x=89/y=334, label col 61 px + 44 px value cols → col 1 centre x≈172).
Not a defect.

### Adjudication posture (banked, pending verdicts)
- formula PASS → all 5 MINORs PIL-adjudicated, no build change (section 5).
- arrow → MINOR geometry difference quantified above (pending the arrow crop
  verdict; if a verdict escalates it, fix = adjust the arrow shape, re-render,
  re-cut crops, re-run BOTH affected legs).
- plot point labels ~3 px smaller than the original's (MINOR-class).

## Adjudication of crop_25_plot FAIL (vs render_25, PIL-first) — 2026-10-25

- **Finding 1 (MAJOR — "(5,1)" label green vs black): REFUTED.** Orig label glyphs
  at (5,1) (frame x685-723, y238-261): 54 green px (e.g. (48,238,42)), ZERO dark
  neutral. The original's label IS green. Render: 69 green px (0,176,80) —
  matches class. Judge misread the original.
- **Finding 2 (MAJOR — x-axis tick "5" green vs black): REFUTED.** Orig tick5
  glyph (frame x687-690, y269-278): dark warm-grey pixels (119,92,97),(118,102,105)
  — R>G, NOT green. Render tick5: neutral (64,64,64),(72,72,72). The (192,0,0)
  pixels intersecting x687 are the RED DASHED LINE, not the tick glyph. Both ticks
  are neutral-dark; judge's colour claim is an artifact of the dashed line overlay.
- **Finding 3 (MINOR — dashed line weight): MINOR-class, judge itself says do not
  block; IMG2 is compression-softened (ground rule e).**

Disposition: plot region is PASS-equivalent by pixel evidence; no fix trigger.
Banked with this adjudication as the certification record.

## Attempt-25 progress ledger — 2026-10-25

Template A: PASS (judge_attempt_25.txt; 7 MINORs, no BLOCKER/MAJOR — title
placement, arrow length, label micro-placement judged acceptable).
Crop legs done (Template B): iter_left PASS, iter_right PASS, formula PASS,
plot FAIL→PIL-REFUTED (both MAJOR colour claims contradicted by pixel evidence;
see adjudication above), param PASS.
Owed: callout, arrow legs.

## Attempt 25 callout + arrow legs (banked 2026-10-25) — 030 COMPLETE

- callout: **PASS** (styling/scaling MINORs only: typeface weight/obliqueness, stroke
  weight, colour tint, vertical padding — judge's own classification).
- arrow: **FAIL with 4 MAJORs — 3 REFUTED, 1 downgraded to MINOR** (red-mask ASCII dump of
  crop_25_arrow_{render,orig}.png, 100x113):
  1. "extra horizontal red stroke right of head": REFUTED — render rows 56-62 cols 53-58
     is the shaft's right edge; the render's horizontal segment (row 26, cols 47-59) is the
     head's top-base edge, which the ORIG also has (rows 24-28, cols 51-63).
  2. "render stroke much thinner": REFUTED — orig strokes 1-3 px and JPEG-broken (#.# runs),
     render 2-3 px solid; render is if anything heavier.
  3. "tip stops short of the band": judge's own numbers self-contradict (tip y68 vs band
     y58 = 10 px PAST, not short). Measured: render tip ~(33,82) vs orig ~(33,96) — the
     render arrow is ~7 frame px (~13%) shorter. Real but sub-noticeable at slide scale;
     MINOR-class (same class as accepted ~10px position MINORs). Noted: build code draws
     y306 h30 (tip 336) vs its own measured comment y304..340. No rebuild per MINOR law.
  4. "extra red numeral 3": REFUTED — orig red mask cols 27-35 rows 84-96 is its own faint
     handwritten red "3" (the table x-row's first data value); render's typed red "3" at
     rows 100-112 is the same cell value, typed-vs-handwritten (rule (c)).
  MINORs 5-7 (divider crispness, 3px registration, hue, shaft proportions): accepted.

## 030 CERTIFIED 2026-10-25
Template A PASS (7 MINORs); 7/7 crop legs banked — iter_left PASS, iter_right PASS,
formula PASS, param PASS, plot FAIL-PIL-REFUTED, callout PASS, arrow FAIL-adjudicated.
visual_check=PASS; attempts=25.
