# Slide 043 "Perceptron Iteration 2" — worker report (attempt 3)

Worker: `w043-finish-20261024`
Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Status: **BUILD CURRENT + 3 REAL DEFECTS FIXED (render_3), VISION LEGS NOT RUN — image-leg wedge**

## DB row at handoff

```
gen_status            building
pptx_path             videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_043_recreated.pptx
build_script          videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_043.js
visual_check          null
visual_attempts       3      (staged, not yet dispatched)
visual_transcript     null
worker_id             w043-finish-20261024
```

## Triage of the inherited bank (all md5/timestamp verified)

| artifact | state | verdict |
|---|---|---|
| `build/slide_043.js` | md5 `43d645a7…`, identical to banked `qa/slide043/build_attempt_2.js` | current, reused as the base |
| `recreated_pptx/slide_043_recreated.pptx` | md5 `69b0dfc7…` | was current w.r.t. that script |
| `qa/slide043/render_2.png` | md5 `9cf70ff9…` | **re-rendered from the pptx and md5-IDENTICAL** — the prior render was genuinely current, not stale |
| `shared_patterns/house_chrome_check.py` on render_2 | PASS (panel x112-1882, y94-bottom; L/R/bottom strokes, top bare; badge (1824,152) d68) | reused |
| `build/assets/eq043_dx*.png|json` (Oct 24 08:33) | **ABANDONED partial rebuild** — only 6 of 22 assets produced; the generator `gen_eq_043.py` carries content typos (`"-0"`, `"02"` in the w specs); neither series is wired into the build | NOT reused |
| `build/components/` | contains slide_009/012/013/017/020/022/027/035 — **no perceptron-family component** | nothing to IMPORT |
| `slide_dependencies.json` | edges only `10>9`, `13>12`, `17>13`, `18>17` | **slide 43 is NOT dependency-gated**; the family note in my task brief is not backed by the founder graph |

## The prior bank's selfcheck was wrong on 2 of 4 claims

`selfcheck_attempt_2.txt` claimed 4 unfixed defects. I re-measured every one against BOTH images
(PIL, frame px, 960×540 original vs 2001×1125 render):

| claim | adjudication | action |
|---|---|---|
| `4b class-row colour` "render is black" | **CONFIRMED REAL** — original has 77 red px at x1..x3 and 32 blue px at x4..x6 (77/3 and 0/32 per-column); render had 0 red, 0 blue | FIXED |
| `3b matrix delimiter` "separate one-line parens per entry" | **CONFIRMED REAL** — original col1 ink bbox x593..617 y83..112 with ONE paren pair spanning both stacked entries (`( 0 ; 0 )`); render drew two separate inline `(0)` `(0)` lines at y83..97 / y110..117 | FIXED |
| `5a aug heading overflow` ink to 247.8 vs box edge 246 | **CONFIRMED REAL but marginal** (1.8 px). Box outline verified identical in both images (ORIG x69..246, REND x69..246 via grayblue-C0C3CA scan) | FIXED |
| `3a initial-W delimiter` "Step text starts inside the bracket; vector has no enclosing delimiter" | **REFUTED** — the original has tall bracket strokes at x331 and x431 spanning y62..101, and `Step η = 2` sits INSIDE them exactly as the render does (verified by full-res ASCII of the original) | no action |

Note the failure mode in the inherited report: `probe_1.txt` (a probe of **render_1**, attempt 1)
described four defects that the report asserted were already fixed in render_2 — but the report
never re-ran the probe or the selfcheck on render_2. The 3 defects above survived into the
deliverable untouched.

## Fixes applied (copy-then-modify; `slide_043_pre_fix.js` backed up in `scratch/tmp/`)

`recreated_pptx/build/slide_043.js` only — three edits:

1. **Class-row colour** (`slide_043.js:97`): `C1`→`C00000`, `C2`→`0000FF`, replacing the
   measured-wrong all-black row.
2. **Class-check matrix** (`slide_043.js:109`): the two inline `(0)/(7)/(3)` and `(0)/(6)/(2)`
   text rows are replaced by three generated 600dpi images (`eq043_mx1/2/3.png`) drawn as ONE
   tall paren pair per Z1 column spanning both stacked entries, centred (605/628/651, 95).
   The images come from `gen_eq_043.py`'s already-correct matrix specs (verified against the
   original: the digits really are `(0;0) (7;6) (3;2)`), which the prior lane had generated
   nothing from.
3. **Aug heading** (`slide_043.js:125`): `x 88 → 79`, `w 170 → 160`, keeping 11pt.

New assets: `recreated_pptx/build/assets/eq043_mx1.png|json`, `eq043_mx2.png|json`,
`eq043_mx3.png|json` (125×222/221/225 px at 600dpi, transparent).

## Verification of the fixes (`selfcheck_attempt_3.py` — output banked)

Rendered `render_3.png` at 2001×1125@150dpi (md5 `a050348c…`), house chrome **PASS**.

- FIX 1: render C1 red = 414 px, C2 blue = 489 px (original 77/32 — same direction, typed ink heavier) → PASS
- FIX 2: matrix paren span 26.4/26.4/26.8 frame px vs original 27/25/27; column bboxes
  REND 597.2..620.7 / 612.0..643.7 / 635.0..658.0 vs ORIG 598..612 / 612..643 / 635..657 → PASS
- FIX 3: heading ink x79.3..212.7, inside the 246 box edge (was 247.8) → PASS
- No regressions: all 6 equation bands inked (4128–5319 px each), frame containment
  (67.7,53.7,893.8,519.3) PASS, 24/24 table cells inked.

## Crop pairs cut for attempt 3 (Procedure B, matched effective scale)

`cropcut_attempt_3.py`; regions re-cut from **render_3** per the re-cut-after-rebuild law:

| region | frame bbox | render crop | orig upscaled | eff px/frame x/y |
|---|---|---|---|---|
| `topband` | 70,50..675,132 | 1261×171 | 1261×171 | 2.0843 / 2.0854 |
| `eqstack` | 268,133..859,535 | 1231×838 | 1231×838 | 2.0829 / 2.0846 |
| `midleft` | 60,130..260,320 | 417×396 | 417×396 | 2.0850 / 2.0842 |

All MATCHED (|eff − render dpi| < 0.005). `render_2 → render_3` region diff proves the
**eqstack region is pixel-identical (0 px changed)** — my three fixes all landed in the top band
and middle-left, so the calc-row stack was untouched.

## BLOCKER — image vision leg wedged (evidence banked)

Both probe dispatches for attempt 3 (`scratch/tmp/043_probe3.sh`, `043_probe3b.sh`, each under
the protocol's `timeout 150`) returned **EXIT_PROBE=124 with zero output and no transcript**.

Banked in `qa/slide043/wedge_evidence_3.txt` (+ `wedge_probe_attempt_3.py`):

- Queue depth 9→12 `analyze_image.py` processes, **9/9 at <1% CPU** in `futex_wait_queue` /
  `do_wait`, cputime 00:00:00, elapsed 39–274s — blocked on network I/O, not computing.
- Direct router measurements in the same window: `images` route (the analyzer's only
  `DEFAULT_MODELS` entry, `analyze_image.py:30`) **32.9s** for a 30-token image request;
  `nemotron-3.5-super-vl-120b-a12b` **1.7s**; text leg 0.5s (also seen at 31.6s in an earlier
  window).
- So: router alive and serving, text leg swings between 0.5s and 31.6s, the `images` virtual
  route is ~19× the direct VL route. A full-frame (2001×1125) analysis cannot complete inside
  the probe's `timeout 150` wrapper on that route, and the real judge's `timeout 600` /
  `timeout 1700` walls are at high risk for the same reason.

**Nothing was recorded as PASS.** No `visual_check`, no `visual_transcript`, no
`gen_status=passed` was written, because no judge leg produced a banked verdict with a
`FINAL VERDICT:` line. `gen_status` stays `building`.

## Files touched

- `recreated_pptx/build/slide_043.js` — the three fixes above (+ stale header comments corrected).
- `recreated_pptx/build/assets/eq043_mx1.png|json`, `eq043_mx2.png|json`, `eq043_mx3.png|json` — new.
- `recreated_pptx/slide_043_recreated.pptx` — rebuilt, md5 now differs from the inherited one.
- `recreated_pptx/qa/slide043/` — `render_3.png`, `selfcheck_attempt_3.py`, `cropcut_attempt_3.py`,
  `crop_3_topband_{render,orig}.png`, `crop_3_eqstack_{render,orig}.png`,
  `crop_3_midleft_{render,orig}.png`, `judge_prompt_3.txt`, `crop_prompt_3_{topband,eqstack,midleft}.txt`,
  `crop_prompt_3_*_desc.txt`, `wedge_probe_attempt_3.py`, `wedge_evidence_3.txt`,
  `build_attempt_2.js.md5guard`, this report.
- `scratch/tmp/` — `043_adj.py`, `043_ascii.py`, `043_initw.py`, `043_wdef.py`,
  `043_verify_fixes.py`, `043_cut_crops.py`, `043_verify_cur.sh`, `043_render_att3.sh`,
  `043_leg_a.sh`, `043_leg_b.sh`, `043_probe3.sh`, `043_probe3{,.b}.log`,
  `043_wedge_probe.py`, `slide_043_pre_fix.js`.
- No banked evidence deleted. No slide outside 43 touched.

## To finish this slide (next worker, fully staged)

The build side is DONE. Only the two judge legs remain. Staged dispatch scripts are banked and
runnable verbatim:

```bash
cd /worksp""aces/codespaces-blank/ai_llm_slides
# option 1 — the staged wrapper (heartbeats the DB, then dispatches):
bash scratch/tmp/043_leg_a.sh                      # Leg A: full-slide Template A on render_3
bash scratch/tmp/043_leg_b.sh topband              # Leg B: 3 dense regions, one call each
bash scratch/tmp/043_leg_b.sh eqstack
bash scratch/tmp/043_leg_b.sh midleft

# option 2 — re-arm the probe first if the gateway looks wedged again:
bash scratch/tmp/043_probe3.sh
```

Payloads are already banked and byte-verified: `judge_prompt_3.txt` (4115 bytes, identical to the
Template A template with `NNN→043`; the template contains **zero** standalone `\bK\b` tokens so the
attempt number never alters it — `BLOCKER` stays intact, 4/4 occurrences) and
`crop_prompt_3_{topband,eqstack,midleft}.txt` (1914 bytes each, `BLOCKER` intact 2/2).

On both legs clean (or every finding PIL-refuted with a banked record):

```bash
D=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 pptx_path videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_043_recreated.pptx --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 build_script videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_043.js --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_check PASS --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_transcript $D/judge_attempt_3.txt --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_attempts 3 --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 gen_status passed --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 43 <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 43      # re-read: claim()/set() can reset gen_status
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 43 <id>
```

Judge attempts used this lane: **0 verdicts obtained** (2 probe hangs, 0 real-judge dispatches).

---

# Resume 3 — 2026-10-24, worker `w043-finish-20261024b`: build CURRENT, 4 real defects fixed, VISION LEGS STILL PARKED

## Final DB row (parked, `get 43`)

```
gen_status            building
pptx_path             videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_043_recreated.pptx
build_script          videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_043.js
visual_check          null
visual_attempts       0        (0 judge dispatches reached a transcript)
visual_transcript     null
worker_id             w043-finish-20261024b
worker_heartbeat_at   2026-10-24T13:49:04Z
```
`gen_status` was never advanced, `visual_check` was never written, `release` was not run.
No verdict was fabricated. `set` operations were limited to heartbeat + claim this resume.

## Triage outcome (reuse-after-verification, md5 + timestamp)

- `build/slide_043.js` **md5-identical** to banked `build_attempt_2.js` → inherited as the base.
- `render_2.png` **re-rendered from the pptx and md5-IDENTICAL** → the prior render was genuinely current, not stale.
- `house_chrome_check.py` on render_2 **PASS** (panel x112-1882 y94-bottom; L/R/bottom, top bare; badge (1824,152) d68).
- `build/assets/eq043_dx*.png|json` (Oct 24 08:33) = **ABANDONED partial rebuild**: only 6 of 22 assets, and the generator `gen_eq_043.py` carries content typos (`"-0"`, `"02"`) plus different values than both the frame and the validated analysis. **Not reused.**
- `build/components/` holds slide_009/012/013/017/020/022/027/035 — **no perceptron-family component** to IMPORT. `slide_dependencies.json` has edges only `10>9`, `13>12`, `17>13`, `18>17`: **slide 43 is NOT dependency-gated**, so the "import a certified family component" instruction in the lane brief has no object in this repo.

## The inherited selfcheck was wrong on 1 of 4 claims — and missed 1 entirely

| claim (from `selfcheck_attempt_2.txt`) | adjudication, PIL, BOTH images | action |
|---|---|---|
| `4b` class row "render is black" | **REAL**. Original x1..x3 red=77 blue=0, x4..x6 red=3 blue=32; render 0/0 | FIXED |
| `3b` matrix "separate one-line parens per entry" | **REAL**. Original col1 ink x593..617 y83..112 = ONE paren pair spanning both stacked entries `( 0 ; 0 )`; render drew two inline `(0)` `(0)` lines | FIXED |
| `5a` aug heading overflow to 247.8 vs box edge 246 | **REAL, marginal (1.8px)**. Box outline verified identical in both (x69..246 via the grayblue C0C3CA scan) | FIXED |
| `3a` initial-W "Step text inside bracket / no enclosing delimiter" | **REFUTED**. Full-res ASCII of the original shows tall bracket strokes at x331 and x431 spanning y62..101 and `Step η = 2` inside them, exactly as the render draws it | none |
| *(not in the inherited selfcheck at all)* legend "C1/C2 not coloured on the frame (red 1-2px)" | **REAL, MISSED**. Original per-token: C1 red=72, C2 blue=52, Zero green=165; render 0/0 | FIXED |

Root cause of the inherited report's error: `probe_1.txt` was a probe of **render_1** (attempt 1). The report asserted its four defects were fixed in render_2 but never re-ran the probe or the selfcheck on render_2. Three real defects survived into the deliverable untouched.

## Fixes (copy-then-modify; pre-fix script kept at `scratch/tmp/slide_043_pre_legend_fix.js`)

All in `recreated_pptx/build/slide_043.js`:

1. **Top-left class row** (`slide_043.js:101`): `C1`→`C00000`, `C2`→`0000FF`.
2. **Class-check matrix** (`slide_043.js:118`): the two inline paren-text rows replaced by three generated 600dpi images `eq043_mx1/2/3.png` — one tall paren pair per Z1 column spanning both stacked entries, centred (605/628/651, 95). The generator's matrix specs were correct (frame digits really are `(0;0) (7;6) (3;2)`); nothing had been generated from them.
3. **Aug heading** (`slide_043.js:139`): `x 88 → 79`, `w 170 → 160`.
4. **Legend** (`slide_043.js:130`): split into `C1`(red @239) / ` positive, ` / `C2`(blue @312) / ` negative, ` / `Zero`(green @396) / ` is unaccepted`(black @431), anchored on the original's measured run positions.

New assets: `recreated_pptx/build/assets/eq043_mx1.png|json`, `eq043_mx2.png|json`, `eq043_mx3.png|json` (125×222/221/225 px at 600dpi, transparent).

**Equation content verified against the validated analysis, not just the frame**: all 12 equations in `analysis/slide_043_final.json` `verbatim_text.equations[0..11]` match the build's in-use `eq_043_*.json` mathtexts exactly. That independently confirms `gen_eq_043.py`'s differing w-series values were wrong and must not be adopted.

## Verification — `selfcheck_attempt_4.txt` (banked), `render_4.png` 2001×1125 md5 `dd94595e`, chrome PASS

```
FIX 1 class row      ORIG red 77/32 -> REND red 414/489, blue 489        PASS
FIX 2 matrix paren   ORIG (598,82,612,109) -> REND (597.2,81.8,620.7,108.2) span 26.4
                     col2 ORIG 612..643 -> REND 612.0..643.7             PASS
                     col3 ORIG 635..657 -> REND 635.0..658.0             PASS
FIX 3 aug heading    REND ink x79.3..212.7 vs box edge 246 (was 247.8)   PASS
FIX 4 legend         C1 REND red=185 | C2 REND blue=163 | Zero REND green=309   PASS
regression  eq bands all inked (4128-5319 px), 24/24 table cells inked,
            content ink bbox (67.7,53.7,893.8,519.3) inside x57..902 y45..539   PASS
RESULT: ALL PASS
```
`render_2 → render_4` region diff proves the **eqstack region is pixel-identical (0 px)** — all four fixes land in the top band and middle-left, the calc stack untouched, so the banked eqstack crop pair remains valid evidence for that region.

## Crop pairs cut for attempt 4 (Procedure B, matched effective scale)

`cropcut_attempt_4.py`, regions from **render_4**, orig LANCZOS-upscaled to match:

| region | frame bbox | render crop | orig upscaled | eff px/frame x/y |
|---|---|---|---|---|
| `topband` | 70,50..675,132 | 1261×171 | 1261×171 | 2.0843 / 2.0854 |
| `eqstack` | 268,133..859,535 | 1231×838 | 1231×838 | 2.0829 / 2.0846 |
| `midleft` | 60,130..260,320 | 417×396 | 417×396 | 2.0850 / 2.0842 |

All MATCHED. Payloads byte-verified against the protocol with only the documented substitutions (`NNN→043`, `\bK\b→4` — the template has **zero** standalone `\bK\b` tokens so `BLOCKER` stays intact 4/4 and 2/2, no `BLOC5ER` corruption anywhere):

`judge_prompt_4.txt` (4115 B), `crop_prompt_4_{topband,eqstack,midleft}.txt` (1914 B each) + matching `_desc.txt`.

## BLOCKER — vision upstream provider wedged, 0 verdicts

Every dispatched image call failed. Full wall evidence in `wedge_evidence_4.txt`:

| call | wall | outcome |
|---|---|---|
| `probe_4.sh`, `probe_4b.sh` | 150s | EXIT 124, hung, no transcript |
| `probe_4c.sh` (`--timeout 1200`) | 1400s | **HTTP 504 `upstream_timeout`, provider Nvidia** |
| `leg_a4.sh` (full-slide, `--timeout 1200`) | 1700s | HangError 1230s wall at ~1117s, killed |
| `leg_b4.sh eqstack` (crop, `--timeout 1200`) | 1700s | HangError 1230s wall at ~1050s, killed |

The orchestrator's 1200s override was applied and **still hung** — the wall was not the constraint; the upstream is. A 1MP crop pair hung identically to the 2.25MP full frame, so it is not a size problem. Text leg in the same window: HTTP 200 in 55.8s. Fleet queue was 40-42 concurrent judges. Conclusion: **the router and auth are healthy; the Nvidia image upstream is not serving.**

Per the deck's wedge law I banked the evidence and stopped. Nothing was recorded as PASS.

## To finish (next worker, fully staged and verified)

```bash
cd /worksp""aces/codespaces-blank/ai_llm_slides
pgrep -c -f analyze_image.py          # if >= 8, sleep and retry before dispatching
bash scratch/tmp/043_leg_a4.sh        # Leg A, full-slide Template A on render_4, --timeout 1200
bash scratch/tmp/043_leg_b4.sh topband
bash scratch/tmp/043_leg_b4.sh eqstack
bash scratch/tmp/043_leg_b4.sh midleft
```
The judge payloads are already banked and byte-checked; the scripts heartbeat the DB themselves.
On both legs clean (or every FAIL/MINOR PIL-refuted against `unique_slides/slide_043.jpg`):

```bash
D=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 pptx_path videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_043_recreated.pptx --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 build_script videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_043.js --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_check PASS --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_transcript $D/judge_attempt_4.txt --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 visual_attempts 1 --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 43 gen_status passed --worker <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 43 <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 43 <id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 43   # re-read: set/claim can reset gen_status
```

## Files touched this resume

- `recreated_pptx/build/slide_043.js` — 4 fixes + header comments corrected.
- `recreated_pptx/build/assets/eq043_mx1/2/3.png|json` — new.
- `recreated_pptx/slide_043_recreated.pptx` — rebuilt (441751 → current).
- `recreated_pptx/qa/slide043/`: `render_3.png`, `render_4.png`, `build_attempt_4.js`,
  `selfcheck_attempt_4.py`/`.txt`, `cropcut_attempt_4.py`,
  `crop_4_{topband,eqstack,midleft}_{render,orig}.png`,
  `judge_prompt_4.txt`, `crop_prompt_4_{topband,eqstack,midleft}.txt` + `_desc.txt`,
  `wedge_evidence_4.txt`, this section.
- `scratch/tmp/`: `043_adj.py`, `043_ascii.py`, `043_initw.py`, `043_wdef.py`,
  `043_verify_fixes.py`, `043_cut_crops.py`, `043_eqvals.py`, `043_legend_icon.py`,
  `043_img_latency.py`/`.log`, `043_verify_cur.sh`, `043_render_att3.sh`,
  `043_leg_a4.sh`, `043_leg_b4.sh`, `043_probe4{,b,c}.sh`/`.log`,
  `slide_043_pre_fix.js`, `slide_043_pre_legend_fix.js`.
- No banked evidence deleted; no slide outside 43 touched.
