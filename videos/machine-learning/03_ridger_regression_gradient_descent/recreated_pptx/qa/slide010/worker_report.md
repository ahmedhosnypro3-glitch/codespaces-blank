# Worker report — slide 010 (Overfit vs. Generalized Model Fits), deck 03

Worker: `w010-child-20261024b` (gated-child build+judge lane; dispatched after
009's certification cleared the `10 > 9` dependency gate).
Claimed: 2026-10-24 09:06:49 — `claim 10 w010-child-20261024b` succeeded
("took over from 'w010', heartbeat 120m stale"); note CLI syntax is
`claim <sid> <worker_id>` (positional), not `--worker`.

## Gate

`10 > 9` gate: cleared. `get 9` = `gen_status=passed`, `visual_check=PASS`,
`worker_id=''` (resume lane `w009-finalize-20261024` released it). The banked
component `build/components/slide_009.js` (md5 `593997f32c59ff00e92982e1caab7257`)
is the certified single-source-of-truth for the parent composition.

## Situation found

A prior `w010` lane produced WIP that was **never judged** (row 10
`visual_check=null`, no `*_judge.txt` transcripts existed): `build/slide_010.js`
(md5 `3ddc44e236ca5a8149925f9aa6997147` == `qa/slide010/build_attempt_2.js`),
`render_2.png`, `crop_2_*` pairs, `selfcheck_attempt_2.txt`. I audited that
build: it already follows the dependency law — it `require("./components/slide_009.js")`
and composes via `renderBase(pptx, slide, {numeral,only})`: parent underlay
(chrome, panels incl. grid + periwinkle residual connectors, axes, caption boxes)
minus the parent `marks`/`eqBoxes` blocks (which do not exist on 010), then 010's
own PIL-measured delta (green dashed cross + bright-green axis dot per panel; two
pale-rose projection pairs per panel), then the parent fitted lines / points /
captions on top. Z-order matches the frame (blue line over the pale dashes;
orange dots cover delta line ends). This exactly matches `analysis/slide_010_final.json`'s
`recreation_brief` step 1 ("IMPORT the certified slide-009 component … skip only
the parent's marks and eqBoxes blocks"). I re-verified it first-person rather than
trusting the banked render (below), rebuilding from the same bytes.

## What this lane did (first-person rebuild + both judge legs)

- **Build**: `node recreated_pptx/build/slide_010.js` → `slide_010_recreated.pptx`
  (single plain-named deliverable; `numeral:10`; no OMML wrap — no equations).
- **Render** (150dpi): soffice → PDF → `pdftoppm` → `qa/slide010/render_3.png` (2001x1125,
  SX=2.0844 SY=2.0833). Determinism: render_3 is **pixel-identical to render_2**
  (max channel diff 0; 0 px differ>8).
- **House chrome** (`house_chrome_check.py render_3.png 10` → `house_chrome_3.txt`): **PASS**
  (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge center
  (1824,152) d=68; all within tol 8).
- **Selfcheck** (`selfcheck_attempt_3.py`, `selfcheck_attempt_3.txt`): **PASS** — 12
  orange dots/panel, green cross ink at rows 238.5/287 and cols 353/766.5, bright-green
  axis dots (d≈8), pale-rose projection pairs at measured rows/cols, red arrowheads at
  the y-axis + red up-triangles under the highlighted points, delta ink fully inside the
  navy borders, caption ink inside the cream bands, blue fitted lines 5/5 on both panels.
- **PIL-vs-original** (`pil_measure_3.py`, `pil_measure_3.txt`): every delta element
  carries ink at the frame's measured position in BOTH the render and the original
  (green cross, bright dots, pale projections, fitted lines). Orange dots: render 12/12;
  original 12/11 under a strict 5px-bbox filter (the 12th right dot is JPEG-soft on the
  frame; its measured centre is listed in the analysis, and the right-panel point set is
  the byte-identical certified 009 set). Dot count is correct and inherited — not fixed.
- **Crops** (`cut_crops_3.py`, `cut_crops_3.txt`): **PASS** — 4 regions
  (`chart_left`, `chart_right`, `cap_left`, `cap_right`) cut from render_3 with the
  original LANCZOS-upscaled to each crop's exact pixel size (matched effective scale
  by construction).
- **Payloads** (`payload_gen_3.py`): `payload_A_3.txt` (4115 B, Template A, 0 NNN) and
  `payload_B_3.txt` (1914 B, Template B, 1×NNN→010) extracted verbatim from
  `shared_patterns/judge_protocol_03.md`; byte-checked (NNN→010 length-neutral, BLOCKER
  intact in both, reverse substitution reproduces the template).

### Judging (through `scripts/16_vision_gate.sh`, gate-law pgrep holds)

- **Leg A — full-slide** (Template A, `render_3.png` vs `unique_slides/slide_010.jpg`,
  `--thinking high --max-tokens 65536 --timeout 600`, outer `timeout 1700`):
  `qa/slide010/judge_attempt_3.txt` → **FINAL VERDICT: PASS** (0 discrepancies;
  chrome/cursor/typed-vs-handwritten settled by rules a/c/d; captions verbatim; point
  positions, line slopes, dash groupings, colour families match; frame containment clean).
  Transcribed the original's right caption as "Succeeds"; the authoritative analysis
  verbatim and the certified inherited component text are "Successes to detect the
  Pattern" (also appears on 009). No discrepancy raised; certified value kept, not changed.
- **Leg B — zoomed crops**: **NOT COMPLETE — PARKED on sustained gateway congestion**
  (evidence below). Dispatcher `dispatch_3crops.sh` self-gates each call on
  `pgrep -c analyze_image.py >= 8` (task gate law). Observed fleet load: raw
  `pgrep -c` 9–15 for ~50 min; accounting for child-process inflation the real
  distinct concurrent `analyze_image.py` calls were ~6 of the 16-slot design (leader-PID
  audit: every PID cwd = project root, none foreign/zombie; the inflation was child procs
  of ~4–5 calls). No crop landed a transcript before the park:
  - `crop_3_chart_left_judge.txt` — **W4 hard-wall abort**: the call ran ~29 min
    (etime 27:39 … GONE) with no transcript; killed at the `timeout 1700` outer wall
    (the analyzer's internal `--timeout 600` client wall was far exceeded under the queue).
    Zero output → no certificate. Per protocol this leg is eligible for **one** hard-wall
    retry (attempt was NOT incrementing a build; this is W4, not a content retry).
  - `crop_3_chart_right_judge.txt` — was running at TaskStop; not completed.
  - `crop_3_cap_left_judge.txt` / `crop_3_cap_right_judge.txt` — not dispatched.

## PARK — exact resume commands (for the next lane)

Nothing below is unverified: the deliverable is built, rendered, chrome/selfcheck/PIL-
verified, and its full-slide leg PASSED. Only the four zoomed crop certificates remain.
To resume and certify:

```bash
cd /worksp"."aces/codespaces-blank/ai_llm_slides   # path split for the harness
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
# 1. reclaim (this lane released the row):  claim 10 <worker_id>
# 2. export TMPDIR=.../recreated_pptx/qa/slide010/../../../scratch/tmp ; when pgrep -c -f analyze_image.py < 8:
bash recreated_pptx/qa/slide010/dispatch_3crops.sh   # fires all four crop judges, self-gated
# 3. when crop_3_{chart_left,chart_right,cap_left,cap_right}_judge.txt each end 'FINAL VERDICT: PASS'
#    (or their findings are PIL-refuted & banked), certify:
set 10 visual_check PASS                 --worker <worker_id>
set 10 visual_transcript recreated_pptx/qa/slide010/judge_attempt_3.txt --worker <worker_id>
set 10 gen_status passed                 --worker <worker_id>
heartbeat 10 <worker_id>
release 10 <worker_id>
# 4. verify: get 10 shows gen_status=passed AND visual_check=PASS AND worker_id=''
```

The crop render/orig pairs (`crop_3_*_render.png` / `crop_3_*_orig.png`) and the byte-checked
Template B payload (`payload_B_3.txt`) are already banked at matched effective scale, so a
resume only needs to run the four comparisons against congestion (no re-cut, no rebuild).
Re-read row 10 before release — `claim()` resets `gen_status` to `building`.

## Final DB row at park (`... 15_progress.py get 10`)

`gen_status=building`, `visual_check=None`, `visual_attempts=0`,
`visual_transcript=None`, `worker_id=w010-child-20261024b` (about to release).
Deliverable: `recreated_pptx/slide_010_recreated.pptx` md5 `9b4ee43ad50f90f09df108c1645c4d26`.
Build: `recreated_pptx/build/slide_010.js` md5 `3ddc44e236ca5a8149925f9aa6997147`
(imports certified `build/components/slide_009.js` md5 `593997f32c59ff00e92982e1caab7257`).

## PIL adjudication notes

- Orange-dot count: PIL refutes any "wrong dot count" finding — render carries exactly 12/12
  (selfcheck), matching the certified inherited 009 point set; the original's soft 11th right
  dot is a video artifact, not a missing element.
- "ONLY" all-caps and "Successes" grammar in the captions are VERBATIM source text
  (`analysis/slide_010_final.json` verbatim_text; slide_009 comment "'Successes' sic"),
  not defects.

## Evidence index

- `render_3.png`, `house_chrome_3.txt`, `selfcheck_attempt_3.py/.txt`,
  `pil_measure_3.py/.txt`, `cut_crops_3.py/.txt`, `crop_3_*_render/orig.png`,
  `payload_gen_3.py`, `payload_A_3.txt`, `payload_B_3.txt`, `dispatch_3crops.sh`,
  `probe_3.txt`.
- `judge_attempt_3.txt` (Leg A full-slide PASS).
- `crop_3_{chart_left,chart_right,cap_left,cap_right}_judge.txt` (Leg B certificates).
- Deliverable: `recreated_pptx/slide_010_recreated.pptx`; build:
  `recreated_pptx/build/slide_010.js` (imports certified `build/components/slide_009.js`).

---

## CROPS LANE — dated section 4 (2026-10-24, worker `w010-crops-20261024b` / `w010-crops-20261024`)

**Verdict: PARKED — unfinished. Zero of the four Procedure B crop legs landed a
verdict. No certification performed. Honest state, nothing fabricated.**

### Final DB row at park (`... 15_progress.py get 10`)

| field | value |
|---|---|
| slide_id | 10 |
| gen_status | `building` |
| visual_check | `null` |
| visual_attempts | 0 |
| visual_transcript | `null` |
| validation_verdict | `PASS_WITH_FIXES` |
| worker_id | `w010-crops-20261024b` → released on park |
| worker_heartbeat_at | `2026-10-24T15:15:13` (fresh) |
| updated_at | `2026-10-24T14:25:29` |

### 1. Bank verification (first-person, this lane) — PASS

Command: `cd videos/machine-learning/03_ridger_regression_gradient_descent` then
`md5sum recreated_pptx/slide_010_recreated.pptx recreated_pptx/build/slide_010.js
recreated_pptx/build/components/slide_009.js recreated_pptx/qa/slide010/render_3.png`

| file | md5 | bank | match |
|---|---|---|---|
| `recreated_pptx/slide_010_recreated.pptx` | `9b4ee43ad50f90f09df108c1645c4d26` | `9b4ee43a…` | YES |
| `recreated_pptx/build/slide_010.js` | `3ddc44e236ca5a8149925f9aa6997147` | `3ddc44e2…` | YES |
| `recreated_pptx/build/components/slide_009.js` | `593997f32c59ff00e92982e1caab7257` | `593997f3…` | YES |
| `recreated_pptx/qa/slide010/render_3.png` | `637426c5f7b87d32b689da818c34ce34` | not banked | — |

Everything banked is intact. Deliverable and build were **never touched** (md5s
above, byte-identical to the bank). Path correction vs the lane brief: the
certified parent component lives at `recreated_pptx/build/components/slide_009.js`
(brief said `components/slide_009.js`).

### 2. Judge-input currency — PASS (no re-render, no re-cut needed)

- pptx mtime `2026-10-24 09:07:49` < render_3 mtime `09:09:18` → render_3
  **postdates** the frozen deliverable and is the render Leg A judged.
- Pixel-exactness proven first-person: `crop_3_chart_left_render.png` equals
  `render_3.crop((181,213,986,1000))` — **every pixel identical**. The whole
  crop chain descends from render_3 (`cut_crops_3.py`).
- Crop pairs all matched-size (verified): chart_left 805×787, chart_right
  834×787, cap_left 738×120, cap_right 742×120. Matched effective scale by
  construction (original LANCZOS-upscaled to the render crop's exact size).
- **Crops lacking verdicts: all four** (glob at `15:15` returned no
  `crop_3_*_judge.txt`; nothing landed after the earlier observation either).

### 3. Payload byte-check — PASS (first-person re-run)

`python3 recreated_pptx/qa/slide010/payload_gen_3.py` re-extracts both payloads
from the frozen `shared_patterns/judge_protocol_03.md` and **regenerates both
files md5-identical** (`9387f5fb…`, `f978e2e3…`; byte-stable across re-runs):
`NNN→010` length-neutral, BLOCKER intact in both, reverse substitution
reproduces the template.

*Bank discrepancy, disclosed:* the bank describes payload A as 4115 B and B as
1914 B; the files on disk are **4139 B / 1924 B**. Those are Python **character**
counts; the files are UTF-8 and the extra 24 bytes in each are multi-byte
em-dashes (U+2014). Not a defect — md5-stable and reproduces byte-for-byte from
the frozen protocol.

### 4. PIL adjudication PREPARED (no verdict to adjudicate yet)

Ran the **banked selfcheck masks** (identical predicates to
`selfcheck_attempt_3.py`) per crop-pair image, so any future crop-leg finding
can be refuted with numbers from BOTH sides. Script `scratch/tmp/pil_dots_crops.py`.

| region | side | orange comps ≥80px | of which bbox ≥5×5 |
|---|---|---|---|
| chart_left | render | 12 | 12 |
| chart_left | orig | 12 | 12 |
| chart_right | render | 12 | 12 |
| chart_right | orig | 11 | 11 |

Exactly **1 bright-green axis dot on each side of each chart region**
(render area 211; orig 205/213). This reproduces the bank's adjudication
precisely: chart_right's original shows 11 blobs under the strict 5px-bbox
filter because the 12th right dot is **JPEG-soft on the video frame** — a
capture artifact, not a missing element. Any crop-leg "wrong dot count" /
"missing dot" claim is refuted by these numbers; the fix is a reply, not a
build edit.

### 5. Crop-leg history this lane — zero verdicts, gateway-side failures

| leg | attempts | outcome |
|---|---|---|
| chart_left | 3 | all failed at the gateway: HTTP 504 `upstream_timeout` (ironrouter candidate `nva…hWGS`, provider Nvidia) — twice at ~61–62 s, plus the sanctioned hard-wall retry also 504. **No transcript, no verdict.** |
| chart_right | 0 | never dispatched (congestion) |
| cap_left | 0 | never dispatched (congestion) |
| cap_right | 0 | never dispatched (congestion) |

The two 504s are **not** client-wall aborts (the analyzer's own `--timeout` was
never reached — the upstream provider returned 504 in ~62 s, twice). Both used
the byte-for-byte frozen Template B payload at `--max-tokens 65536`; one at
`--timeout 1200`, one at `--timeout 600`, neither exceeded the allowed walls.

### 6. Congestion timeline (why nothing landed)

Fleet `pgrep -c -f analyze_image.py` stayed ≥8 for the entire ~3h20m lane.
Observed: 9 → 11 → 13 → 19 → 28 → 40 → 46 raw, with a **leader-PID audit**
(real `python3 …/analyze_image.py` invocations, excluding the `16_vision_gate.sh`
bash wrapper and the `timeout` wrapper that inflate the raw count ~1.5×) showing
6 → 12 → 15 → 21 → 37 real invocations against the 16-slot design. Transient
dips (e.g. 6 real) were followed by re-spikes within minutes; each time the two
directive-2 re-probes expired with load still ≥8.

**Infrastructure note that cost this lane ~10 min:** the first dispatcher launch
ran inside the harness's 600 s background-task limit; when the wrapper timed out
it killed the whole dispatcher process group (no verdicts had landed). Relaunched
detached with `nohup … & disown`, which is immune to that. Prefer detached launch
for any multi-leg dispatch.

Also note: other lanes' image legs **are** landing verdicts during this window
(slide_048 `crop_4_calc_panel_judge.txt`, slide_003 `crop_19_matrix_judge.txt`,
slide_030 `crop_6_formula_judge.txt`), so the 504 is a transient
upstream-candidate failure, not a dead image model.

### 7. PARK — exact resume commands

```bash
cd /worksp"."aces/codespaces-blank/ai_llm_slides          # path split, never the literal plural
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py claim 10 <worker_id>        # row was released on park
python3 scripts/15_progress.py heartbeat 10 <worker_id>   # re-stamp liveness

# 1. verify bank (must all match):
cd videos/machine-learning/03_ridger_regression_gradient_descent
md5sum recreated_pptx/slide_010_recreated.pptx recreated_pptx/build/slide_010.js \
       recreated_pptx/build/components/slide_009.js recreated_pptx/qa/slide010/render_3.png
# 2. compute what still lacks verdicts, then fire the missing legs SEQUENTIALLY,
#    each under the gate law (pgrep >= 8 => heartbeat, sleep 240, re-probe,
#    max two re-probes) and NEVER beyond --timeout 1200 / outer `timeout 1700`:
printf '%s' "$(cat recreated_pptx/qa/slide010/payload_B_3.txt)"   # byte-for-byte Template B
R=recreated_pptx/qa/slide010; export TMPDIR="$PWD/scratch/tmp"
scripts=/workspaces/codespaces-blank/ai_llm_slides/scripts/16_vision_gate.sh   # see path law
for n in chart_left chart_right cap_left cap_right; do
  [ -s "$R/crop_3_${n}_judge.txt" ] && echo "$n has verdict, skip" || echo "$n MISSING"
done
# per missing leg (example = chart_left):
nohup bash "$scripts" timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$R/crop_3_${n}_render.png" "$R/crop_3_${n}_orig.png" \
  --view "Slide 010 zoomed crop ${n} - render vs original at matched scale (attempt 3)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: <desc from cut_crops_3.txt>" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$R/crop_3_${n}_judge.txt" \
  -p "$(cat "$R/payload_B_3.txt")" > "$R/leg_${n}_run.log" 2>&1 < /dev/null & disown
# 3. PIL-adjudicate every finding against BOTH images BEFORE any build change:
python3 scratch/tmp/pil_dots_crops.py     # banked dot adjudication (12/12 & 12/11)
# 4. when all four transcripts end in a real "FINAL VERDICT:" line, CERTIFY:
python3 scripts/15_progress.py set 10 visual_check PASS --worker <worker_id>
python3 scripts/15_progress.py set 10 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010/judge_attempt_3.txt --worker <worker_id>
python3 scripts/15_progress.py set 10 visual_attempts <n> --worker <worker_id>
python3 scripts/15_progress.py set 10 gen_status passed --worker <worker_id>
python3 scripts/15_progress.py heartbeat 10 <worker_id>
python3 scripts/15_progress.py release 10 <worker_id>
python3 scripts/15_progress.py get 10     # MUST read gen_status=passed AND visual_check=PASS AND worker_id=""
                                        # (re-check: claim()/set() can reset gen_status — 15_progress.py:337-339)
```

**chart_left's protocol-sanctioned hard-wall retry was consumed by this lane's
first attempt (which 504'd at the gateway, not at a wall). Do not retry-loop it.**

### 8. Evidence touched this lane (additive only)

- `recreated_pptx/qa/slide010/legs_status_20261024.md` (new — banked park note)
- `scratch/tmp/pil_dots_crops.py` (new — dot adjudication vs both images)
- `scratch/tmp/pil_crops_20261024.py` (new — loose blob counter, superseded)
- `recreated_pptx/qa/slide010/dispatch_3crops_run.log`, `dispatch_3crops_run2.log`
- Payloads re-verified by re-running `payload_gen_3.py` → md5-identical.
- No banked evidence deleted or modified; deliverable and build byte-identical.

---

## CROPS LANE — dated section 5 (2026-10-24, worker `w010-crops-20261024c`)

**Verdict: CERTIFIED. All four Procedure B zoomed crop legs landed REAL PASS
verdicts; every MINOR finding was PIL-adjudicated and adjudicated away (refuted
or covered by a capture/cascade ground rule). The build was NOT rebuilt and NOT
re-cut — the frozen deliverable and its render were certified as they stood.**

### 1. Final DB row (after `release`)

| field | value |
|---|---|
| slide_id | 10 |
| gen_status | `passed` |
| visual_check | `PASS` |
| visual_attempts | `3` |
| visual_transcript | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010/judge_attempt_3.txt` |
| validation_verdict | `PASS_WITH_FIXES` |
| worker_id | `""` (released) |
| updated_at | `2026-10-24T20:16:28` |

Row before this lane: `gen_status=building`, `visual_check=null`,
`visual_attempts=0`, `visual_transcript=null`, `worker_id=w010-crops-20261024c`
(claimed). DB writes used `set` with the `--worker` VALUE flag; `gen_status` was
set LAST (after the other three fields), then `heartbeat`, then `release`, then
`get` re-read.

**`visual_attempts=3` rationale (deck convention, verified against sibling rows):**
the value tracks the **attempt index of the certified judge family**, not a raw
count of vision calls. Slide 009 uses `5` with `judge_attempt_5.txt` + `crop_5_*`;
slide 013 uses `6` with `judge_attempt_6.txt` + `crop_6_*`; slide 012 uses `4`
with its `crop_4_*` family. Slide 010's certified family is `judge_attempt_3.txt`
(Leg A full-slide) + `crop_3_*` (Leg B) → `3`.

### 2. Attempt history (honest, complete)

| leg | attempts | outcome |
|---|---|---|
| Leg A — full slide | 1 | `judge_attempt_3.txt` → **PASS**, 0 discrepancies (banked by the child lane; not re-run) |
| chart_left | 3 earlier + 1 here | earlier lane: 2× HTTP 504 `upstream_timeout` (Nvidia candidate `nva…hWGS`) + 1 sanctioned hard-wall retry (also 504). This lane: **PASS at 19:15:21Z** |
| cap_left | 1 | **PASS at 19:18Z**, "Discrepancies found: None" |
| cap_right | 1 | **PASS at 19:21Z** (3 MINOR findings, all adjudicated) |
| chart_right | 2 | 504 at 19:15:59Z (upstream_timeout, rc=1, no transcript) → re-probe #1 of max 2 (after the mandated 240 s sleep) → **PASS at 19:36:53Z** |

Dispatcher: `qa/slide010/dispatch_crops_w010c.sh` (PID 31171, finished 19:22:00),
log `qa/slide010/dispatch_crops_w010c.log`; re-probe log
`qa/slide010/reprobe_chart_right_w010c.out`.

### 3. Crop verdict certificates (all REAL bodies, all PASS)

| file | size | verdict | findings |
|---|---|---|---|
| `crop_3_chart_left_judge.txt` | 5479 B | `### FINAL VERDICT: **PASS**` | 7 MINOR |
| `crop_3_cap_left_judge.txt` | 1389 B | `FINAL VERDICT: PASS` | 0 |
| `crop_3_cap_right_judge.txt` | 3578 B | `## FINAL VERDICT: PASS` | 3 MINOR |
| `crop_3_chart_right_judge.txt` | 4706 B | `**FINAL VERDICT: PASS**` | 4 MINOR |

Re-verified after certification: all four contain a real `FINAL VERDICT:` line and
**zero** `GROUND RULES` occurrences (i.e. real verdict bodies, not prompt echoes).

### 4. PIL adjudication (PIL-first) — every MINOR resolved, no build change

Authoritative scripts: `scratch/tmp/pil_adj_010_robust.py` (least-squares line
fits), `scratch/tmp/pil_adj_010_decisive.py` (hue/coordinate probes),
`scratch/tmp/pil_adj_010_final.py` (cap_right geometry, arrowhead sizes, dot
deltas). `pil_adjudicate_010_all.py` and `pil_adjudicate_chart_left_010.py` are
**superseded** (their RGB-target predicates missed the actual stroke colours
navy `(0,0,128)`, orange `(255,165,0)`, red `(192,0,0)`, cream `(251,252,236)`)
and their numbers are not cited here.

**chart_left (7 MINOR)**
- *gray stylus on the frame* — render has **0** gray-ink rows (≥4 px, x340..520,
  y395..460); original has **51** rows forming a distinct diagonal tail. Direct
  comparison: `unique_slides/slide_009.jpg` has **no** gray cluster at the
  analogous frame spot `(281,306)` while `slide_010.jpg` does → the shape exists
  only in slide 010's lecture frame (lecturer's on-screen pointer / capture
  artifact). **REFUTED** — correctly omitted per ground rule (c) (Template A).
- *blue line weight* — render blue px/col median **9** crop px (≈4.3 frame px) vs
  original **16** (≈7.7 frame px); the build draws `line: {color: BLUE, width: 2}`
  = 2 pt = 2.08 frame px. The original's apparent thickness is JPEG/upsample
  bleed → ground rule (e). Medium artifact, not content.
- *rose dash hue* — the build uses the SAME pale `ECBAC4` for both dashes
  (`DELTA.LEFT.pairs` `hy: 289.5` upper, `hy: 300.5` lower); on the original frame
  the darker dash is the **upper** one (rows 290–291 mean `(223.8,199.2,204.6)`)
  while the lower rows 298–301 read `(239.8,211.9,218.2)`. The judge inverted the
  two lines. **REFUTED** — the recreation matches the frame's actual dash hues.
- *red arrowheads bolder* — render small red components carry clean saturated
  means in the `(192,0,0)` family; the originals are duller (`≈(212–222,110–128,
  66–76)`) = JPEG desaturation (rule e). Positions and sizes agree.
- *sub-pixel offsets* — all 12 orange-point centroid deltas |dx|,|dy| = 0.40–1.72
  crop px (0.17–0.81 frame px); below threshold. One pair sits at dy = 3.55 crop
  px (1.7 frame px) — still under the MINOR bar.
- *panel tone* — render near-white `(242.19,241.96,241.81)` vs original
  `(242.23,242.70,242.48)`: the original is **-1.5 green** (slightly blue-leaning),
  not greenish as claimed, and the whole difference is ≤0.5/255. **REFUTED**.

**chart_right (4 MINOR)**
- *"blue line 4–5 px too high"* — least-squares fit over x200–600: render slope
  −0.47569 / intercept 668.50 vs original slope −0.47935 / intercept 675.47 →
  dy = **−6.24…−4.78 crop px (−2.99…−2.29 frame px)**. A ~2.3–3.0 frame-px
  vertical offset does exist, consistent in sign with the judge, but it is
  **inherited geometry**: `slide_010.js` stage 3 draws the parent's fitted lines
  via `base.renderBase(pptx, slide, {only:{fittedLines:true, points:true,
  captions:true}})` from the certified `build/components/slide_009.js` (row 9
  `gen_status=passed`, `visual_check=PASS`). Per the cascade law, inherited/cascade
  zones are adjudication inputs, never fix triggers. Severity stays MINOR; no
  build edit.
- *"missing filled green node at (477,307)"* — the judge coordinate decodes as if
  the image were downscaled ~0.796× (its `(477,307)` → actual `(601,384)`); the
  cited pixel is **289 pure-white px in BOTH crops**. At the TRUE intersection
  (crop x≈601–602, y≈384–385) both images show the green horizontal dash row
  with the blue stroke crossing; the original carries a 178 px JPEG-soft green
  vertical blob, the render the same vertical in 18 px dash segments. **No
  distinct filled green node exists in either image** → **REFUTED**.
- *"dot 2–3 px left of the vertical"* — render bright-green dot centroid
  cx = 600.4 vs green vertical dash column x = 601 → offset **−0.6 crop px
  (−0.31 frame px)**; original +0.7. **REFUTED** (sub-pixel; wrong coordinate frame).
- *"points more yellow/gold"* — render modal colour is exactly `(255,165,0)` (the
  build's ORANGE) on all 12 points; original pooled mean `(221.9,119.2,47.3)` with
  JPEG-mottled modes (`≈(212,112,19)…(231,119,31)`) = capture darkening /
  desaturation of the same orange family (rule e). **REFUTED**.
- Point inventory (strict PIL): render 12 components, original 11 (the known
  JPEG-soft 12th right dot); the 11 matched frame-px centroids agree to
  ≈0.5–1.3 px.

**cap_right (3 MINOR)**
- *vertical padding* — line-2 lowest ink y = 88 vs bottom rose rule y = 110 →
  gap **22 crop px (10.55 frame px)**; original: ink y = 90, rule y = 111 → gap
  **21 crop px (10.07 frame px)**. Difference 0.48 frame px → **REFUTED**.
- *line-2 width* — render line-2 ink x extent 154..582 = **429 crop px**
  (205.8 frame px); original 157..583 = **427 crop px** (204.9 frame px).
  Difference 2 crop px → **REFUTED** (the judge's own x-ranges were misread).
- *"Generalized" red saturation* — render red is pure `(192,0,0)` = the build's
  `C00000`; the original is duller = JPEG desaturation (rule e). **REFUTED**.

**cap_left** — the judge found **zero discrepancies**; PIL independently confirms
both caption lines render in the build's colours (cream fill `251,252,236`,
ink `51,51,51`, red `192,0,0`). Clean.

Net adjudication result: **0 genuine FAIL findings → no build edit, no re-cut,
no re-judge.**

### 5. Bank untouched (re-verified after certification)

| file | md5 |
|---|---|
| `recreated_pptx/slide_010_recreated.pptx` | `9b4ee43ad50f90f09df108c1645c4d26` |
| `recreated_pptx/build/slide_010.js` | `3ddc44e236ca5a8149925f9aa6997147` |
| `recreated_pptx/build/components/slide_009.js` | `593997f32c59ff00e92982e1caab7257` |
| `recreated_pptx/qa/slide010/render_3.png` | `637426c5f7b87d32b689da818c34ce34` |

Identical to the bank: **the build was not rebuilt and the render was not
re-rendered.** `crop_3_chart_left_render.png` remains pixel-exact
`render_3.crop((181,213,986,1000))`.

### 6. Two dispatcher bugs found and fixed in this lane (process notes)

1. **Call-site name mismatch** — the dispatcher invoked the analyzer helper as
   `judge_crop`; the actual entry point is `run_leg`. Fixed before firing.
2. **Verdict-detector regex too strict** — the detector matched only `^FINAL
   VERDICT:` and therefore reported `crop_3_chart_left_judge.txt` and
   `crop_3_cap_right_judge.txt` as "NOT a real verdict body" (their verdict lines
   are `### FINAL VERDICT: **PASS**` and `## FINAL VERDICT: PASS`). Both ARE real
   PASS bodies — confirmed by re-reading the transcripts (0 `GROUND RULES`
   occurrences). The corrected detector is
   `grep -qE 'FINAL VERDICT: *\** *(PASS|FAIL)'` **and**
   `! grep -q "GROUND RULES"`.
3. **TMPDIR / flock-pool finding** — the banked `dispatch_3crops.sh` exported a
   **video-scoped** `scratch/tmp` as `TMPDIR`; that directory holds only 2 lock
   files, so the fleet's 16-slot gate (project-root `scratch/tmp` lock pool) was
   bypassed entirely. This lane's dispatcher exports the **project-root**
   `TMPDIR`, so its calls queue behind the real fleet gate.

### 7. Park state

**No park. All legs resolved and certified.** The earlier park
(`legs_status_20261024.md`, sections 1–8) is lifted: 4/4 crop legs PASS,
0 findings outstanding, DB row certified and released.

### 8. Evidence touched this lane (additive only)

- `recreated_pptx/qa/slide010/dispatch_crops_w010c.sh`, `dispatch_crops_w010c.log`,
  `dispatch_crops_w010c.out`
- `recreated_pptx/qa/slide010/reprobe_chart_right_w010c.sh`,
  `reprobe_chart_right_w010c.out`
- `recreated_pptx/qa/slide010/crop_3_{chart_left,cap_left,cap_right,chart_right}_judge.txt`
  (the four certificates)
- `scratch/tmp/pil_adj_010_robust.py`, `pil_adj_010_decisive.py`,
  `pil_adj_010_final.py` (superseded: `pil_adjudicate_010_all.py`,
  `pil_adjudicate_chart_left_010.py`)
- `recreated_pptx/qa/slide010/worker_report.md` (this section),
  `legs_status_20261024.md` (park-lift note)
- No banked evidence deleted or modified; deliverable and build byte-identical.
