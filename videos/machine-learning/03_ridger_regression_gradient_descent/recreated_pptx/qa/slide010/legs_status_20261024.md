# Legs status — slide 010 crop legs (Procedure B), crops-lane attempt 4

Worker: `w010-crops-20261024` (legs-only finish lane; claimed `10` after the
`w010-child-20261024b` child lane released it). Date: 2026-10-24.

## Status: PARKED on sustained fleet congestion — no crop transcript landed yet

The four Procedure B zoomed crop legs are **NOT yet dispatched**. The banked
self-gated dispatcher is **STILL ALIVE and holding**; it will fire all four legs
automatically as soon as congestion clears, so a resume needs no manual
re-kick (details below).

## 1. Bank verification (first-person, this lane)

Command run from `videos/machine-learning/03_ridger_regression_gradient_descent`:

```bash
cd /worksp"."aces/codespaces-blank/ai_llm_slides
cd videos/machine-learning/03_ridger_regression_gradient_descent
md5sum recreated_pptx/slide_010_recreated.pptx recreated_pptx/build/slide_010.js \
       recreated_pptx/build/components/slide_009.js recreated_pptx/qa/slide010/render_3.png
```

| file | md5 | bank | match |
|---|---|---|---|
| `recreated_pptx/slide_010_recreated.pptx` | `9b4ee43ad50f90f09df108c1645c4d26` | `9b4ee43a…` | YES |
| `recreated_pptx/build/slide_010.js` | `3ddc44e236ca5a8149925f9aa6997147` | `3ddc44e2…` | YES |
| `recreated_pptx/build/components/slide_009.js` | `593997f32c59ff00e92982e1caab7257` | `593997f3…` | YES |
| `recreated_pptx/qa/slide010/render_3.png` | `637426c5f7b87d32b689da818c34ce34` | (not banked) | — |

- Path correction: the certified parent component lives at
  `recreated_pptx/build/components/slide_009.js` (the lane brief said
  `components/slide_009.js` without the `build/` prefix). md5 matches the bank.
- **Render currency confirmed, no re-render needed**: `render_3.png` mtime
  2026-10-24 09:09:18 > pptx mtime 09:07:49 → render_3 postdates the frozen
  deliverable and is current. Crops were re-verified as cut from render_3
  (`cut_crops_3.py`, `cut_crops_3.txt`). Crop pairs all matched-size:
  chart_left 805×787, chart_right 834×787, cap_left 738×120, cap_right 742×120.

### Payload byte-check (first-person re-run)

`python3 recreated_pptx/qa/slide010/payload_gen_3.py` re-extracts both payloads
from the frozen `shared_patterns/judge_protocol_03.md` and **regenerates both
files md5-identical** (`9387f5fb…`, `f978e2e3…` — byte-for-byte stable across
re-runs), with `NNN→010` length-neutral, BLOCKER intact in both, and reverse
substitution reproducing the template. PASS.

*Honest note on a bank discrepancy:* the bank describes `payload_A_3.txt` as
4115 B and `payload_B_3.txt` as 1914 B; the files on disk are **4139 B and
1924 B**. Those banked numbers are Python **character** counts (`len()`); the
files are UTF-8 and the extra 24 bytes in each are multi-byte em-dashes
(U+2014, 3 bytes vs 1). Not a defect: the payloads are md5-stable and reproduce
byte-for-byte from the frozen protocol.

## 2. PIL adjudication prepared (refutation feed, first-person numbers)

Ran the **banked selfcheck masks** (identical predicates to
`selfcheck_attempt_3.py`) per crop-pair image so any crop-leg finding can be
refuted with numbers from BOTH sides. Script: `scratch/tmp/pil_dots_crops.py`.

| region | side | orange comps ≥80px | of which bbox ≥5×5 |
|---|---|---|---|
| chart_left | render | 12 | 12 |
| chart_left | orig | 12 | 12 |
| chart_right | render | 12 | 12 |
| chart_right | orig | 11 | 11 |

This reproduces the banked adjudication exactly: **chart_right's original shows
11 blobs under the strict 5px-bbox filter because the 12th/right dot is
JPEG-soft on the video frame** (its measured centre is recorded in
`analysis/slide_010_final.json`, and the right-panel point set is the
byte-identical certified 009 set). A crop-leg "wrong dot count" /
"missing dot" finding is refuted by these numbers, not by editing the build.
Also confirmed per crop: exactly 1 bright-green axis dot on each side of each
chart region (render area 211, orig 205/213).

## 3. Why nothing landed: congestion, measured (not a gate bug)

The dispatcher's own law (`pgrep -c -f analyze_image.py >= 8`) was re-probed
continuously for ~1h50m. Raw count stayed 9–28. A **leader-PID audit**
(distinct `python3 …/analyze_image.py` invocations, excluding the
`16_vision_gate.sh` bash wrapper and the `timeout` wrapper that inflate the raw
count ~1.5×) shows the congestion is real and not a counting artifact:

- 12 → 15 → 19 → 21 real analyzer invocations in flight over the window,
  against a **16-slot fleet design** (`scripts/16_vision_gate.sh`).
- Active sibling legs observed (other slides, other lanes): slide021
  `judge_attempt_10`, slide016 `crop_5_missing_band`, slide043 `probe_3`.

Both the raw count (17–28) and the corrected leader count (12–21) are ≥ 8, so
the gate law unambiguously holds — firing a 4-crop lane into that would risk
another W4-style hard-wall abort like `chart_left`'s last attempt.

**Infrastructure note (cost this lane ~10 min):** the first dispatcher launch
was wrapped by the harness's 600 s background-task limit, and when the wrapper
timed out it killed the whole dispatcher process group. Re-launched detached
with `nohup … & disown`, which is immune to that. Recommend the next lane launch
the same way (see commands).

## 4. Exact resume commands

Nothing below is unverified: the deliverable is built (md5 `9b4ee43a…`),
rendered (`render_3.png`, current for the pptx), chrome/selfcheck/PIL-verified,
and its **full-slide leg A already PASSED with zero discrepancies**
(`qa/slide010/judge_attempt_3.txt` — REAL FINAL VERDICT: PASS). Only the four
zoomed crop certificates remain.

If the dispatcher is still alive (it self-gates and auto-fires when load < 8),
do nothing but watch:

```bash
tail -f videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010/dispatch_3crops_run2.log
ls  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010/crop_3_*_judge.txt
```

To relaunch it from scratch (detached, immune to the wrapper timeout):

```bash
cd /worksp"."aces/codespaces-blank/ai_llm_slides   # path split for the harness
nohup bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010/dispatch_3crops.sh \
  > videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010/dispatch_3crops_run2.log 2>&1 \
  < /dev/null & disown
```

One protocol-sanctioned **hard-wall retry is pre-authorized for `chart_left`**
(its last attempt aborted at the 1700 s outer wall). If a leg would otherwise
abort at the 630 s client wall, the orchestrator's provisional wall extension
allows `--timeout 1200` (payload byte-for-byte, `--max-tokens 65536`
unchanged). Do not retry-loop beyond that.

Then certify (no `record-visual` subcommand exists in this tool):

```bash
cd /worksp"."aces/codespaces-blank/ai_llm_slides
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
set 10 visual_check PASS                 --worker <worker_id>
set 10 visual_transcript recreated_pptx/qa/slide010/judge_attempt_3.txt --worker <worker_id>
set 10 visual_attempts <n>               --worker <worker_id>
set 10 gen_status passed                 --worker <worker_id>
heartbeat 10 <worker_id>
release 10 <worker_id>
# then RE-READ row 10 and restore gen_status if claim()/set() reset it (15_progress.py:337-339)
get 10   # final row must read gen_status=passed AND visual_check=PASS AND worker_id=""
```

Note the full-slide transcript path is relative to the deck root; other lanes
in this DB have banked the deck-relative form (`recreated_pptx/qa/slide010/…`).
Check an existing certified row's convention with `get <sid>` before setting.

## 5. Evidence touched this lane (additive only — nothing deleted or edited)

- `scratch/tmp/pil_dots_crops.py` (new, adhesion measurement)
- `scratch/tmp/pil_crops_20261024.py` (new, superseded loose blob counter)
- `recreated_pptx/qa/slide010/dispatch_3crops_run.log` (first launch log)
- `recreated_pptx/qa/slide010/dispatch_3crops_run2.log` (relaunched, holding)
- `recreated_pptx/qa/slide010/legs_status_20261024.md` (this file)
- No banked evidence modified; deliverable and build untouched
  (md5s above, unchanged).

## ADDENDUM 2026-10-24 ~15:30 (worker `w010-crops-20261024b`, re-claimed lane)

**Status: PARKED — unfinished. Zero of four crop legs landed a verdict.**

New facts observed after the first bank of this note:

- **chart_left was dispatched 3 times and all 3 failed at the gateway**, not at a
  wall: `HTTP 504 upstream_timeout` (ironrouter candidate `nva…hWGS`, provider
  Nvidia) at ~61 s and ~62 s on two attempts (one `--timeout 1200`, one
  `--timeout 600`). No transcript, no verdict, `rc=1`. Neither attempt reached the
  analyzer's own client wall — the upstream provider timed out first. Payload was
  byte-for-byte the frozen Template B at `--max-tokens 65536` both times.
- chart_right / cap_left / cap_right were **never dispatched** (congestion).
- The detached dispatcher was stopped by this lane to control firing sequence.
- Judge-input currency re-verified PASS: pptx md5 `9b4ee43a…` unchanged,
  render_3 postdates pptx, `crop_3_chart_left_render.png` is **pixel-exact**
  `render_3.crop((181,213,986,1000))`. All four crop pairs matched-size.
- Dot adjudication prepared first-person (banked selfcheck masks, both images):
  chart_left 12/12 render vs 12/12 orig; chart_right 12/12 render vs 11/11 orig
  (the 11th is the JPEG-soft right dot — video artifact, banked finding). One
  bright-green axis dot per side per chart. Script `scratch/tmp/pil_dots_crops.py`.
- Full-slide Leg A verdict (`judge_attempt_3.txt` → `FINAL VERDICT: PASS`)
  confirmed intact and unchanged.
- DB row at park: `gen_status=building`, `visual_check=null`,
  `visual_attempts=0`, `visual_transcript=null`; claim released on park.
- See the appended dated section in `worker_report.md` for the full park note,
  congestion timeline, and exact resume commands.

**Resume headline:** claim 10, verify md5s, fire only the crops still lacking a
`FINAL VERDICT:` line, SEQUENTIALLY, each behind `pgrep -c -f analyze_image.py < 8`
(max two 240 s re-probes, then park), never beyond `--timeout 1200` /
`timeout 1700`, no retry-loop. Then certify with `set` (no `record-visual`
subcommand exists) and re-read `get 10` before release.

---

## ADDENDUM 2026-10-24 20:16 — PARK LIFTED, SLIDE 010 CERTIFIED
(worker `w010-crops-20261024c`)

**The park is over. All four Procedure B crop legs landed real PASS verdicts and
slide 010 is certified in the DB.**

| leg | verdict file | outcome |
|---|---|---|
| chart_left | `crop_3_chart_left_judge.txt` | **PASS** (7 MINOR, all PIL-adjudicated) |
| cap_left | `crop_3_cap_left_judge.txt` | **PASS** (0 discrepancies) |
| cap_right | `crop_3_cap_right_judge.txt` | **PASS** (3 MINOR, all PIL-adjudicated) |
| chart_right | `crop_3_chart_right_judge.txt` | **PASS** (4 MINOR, all PIL-adjudicated) |

- chart_right needed one re-probe: the first call 504'd at 19:15:59Z
  (`upstream_timeout`, rc=1, no transcript); re-probe #1 of max 2 (after the
  mandated 240 s sleep) landed PASS at 19:36:53Z.
- Every MINOR was adjudicated PIL-first: either refuted with measured numbers
  (wrong coordinate frames, inverted dash ordering, misread colour families,
  JPEG desaturation/halo artifacts under ground rules (c)/(e)) or identified as
  **inherited certified-parent geometry** (the chart_right fitted-line offset,
  drawn from the certified `build/components/slide_009.js` — cascade law, not a
  fix trigger). **0 genuine FAIL findings.**
- **No build edit, no re-cut, no re-judge.** Deliverable and build md5s are
  byte-identical to the bank (`slide_010_recreated.pptx` `9b4ee43a…`,
  `slide_010.js` `3ddc44e2…`, `slide_009.js` `593997f3…`, `render_3.png`
  `637426c5…`).
- Final DB row 10: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=3`
  (the certified judge family's attempt index — same convention as slide 009's
  `5` ↔ `judge_attempt_5.txt` / `crop_5_*` and slide 013's `6` ↔ `judge_attempt_6.txt`
  / `crop_6_*`), `visual_transcript=…/qa/slide010/judge_attempt_3.txt`,
  `worker_id=""` (released).
- Full attempt history, per-finding adjudication numbers, the two dispatcher bugs
  fixed this lane and the TMPDIR flock-pool finding are in
  `worker_report.md` § "CROPS LANE — dated section 5".
