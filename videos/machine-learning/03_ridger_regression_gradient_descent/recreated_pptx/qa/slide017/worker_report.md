# Slide 017 worker report — "Adding Ridge Regularizer to the model λ=3"

Worker: `kimi-slide017`.
Deck: `machine-learning/03_ridger_regression_gradient_descent` (namespace
`videos/machine-learning/03_ridger_regression_gradient_descent/`).
Protocol: `shared_patterns/judge_protocol_03.md` (Template A full-slide + Procedure B
crop-pairs, byte-exact payloads).
Row 17 is dependency-gated: `depends_on=13` (certified); slide **018 is gated on 17**.

## Status at this writing: PARKED ON GATE CONGESTION — NOT certified, NOT a defect

At the time of this section the lane has **no real judge verdict** on the current render.
`gen_status=building`, `visual_check=NULL`, `visual_transcript=NULL`, `visual_attempts=0`,
`worker_id=kimi-slide017` (claim HELD, heartbeat fresh). See "Final DB rows" and
"Exact resume commands" below — every artifact needed to dispatch both legs is banked
and byte-verified; only the vision gate is blocking.

## State at pickup

| item | value |
|---|---|
| build script | `recreated_pptx/build/slide_017.js` (banked) |
| deliverable pptx | `recreated_pptx/slide_017_recreated.pptx` (md5 `7374f15e46372898ac8b9b5ac330d15f`) |
| renders in bank | `render_1.png`, `render_2.png`, `render_3.png`, `render_4.png` (all preserved; none deleted) |
| current render | `qa/slide017/render_4.png` 2001×1125 (150 dpi of 13.33×7.5 in) |
| house chrome check | PASS on `render_4.png` (panel x 112–1882, y 94–bottom; strokes L/R/bottom present, top bare; badge centre (1824,152) d=68; all within tol 8) |
| selfcheck | `selfcheck_attempt_4.txt` → `RESULT: FAIL (6)` — all 6 refuted as checker artifacts (numbers below) |
| judge transcripts | only `judge_attempt_3.txt` — a **VOID** body (no `FINAL VERDICT:` line) |
| qa bank | renders, measurement scripts, selfchecks, adjudications, payload/crop emitter, dispatch scripts |

## Attempt history

| attempt | render | leg | outcome | counted? |
|---|---|---|---|---|
| 1–2 | `render_1`, `render_2` | selfcheck / forensics | superseded (build fixes landed) | — |
| 3 | `render_3` | Template A | **VOID** — `judge_attempt_3.txt` (1701 B) is free-form markdown with **no `FINAL VERDICT:` line**; per protocol it is not a verdict | no |
| 4 | `render_4` | Template A + 5 crop pairs | **NOT DISPATCHED** — gate congestion (probe cap) | — |

The prior worker's `emit_payloads.py` crashed on its own reverse byte-check because
`K=3` collided with the literal `(3)` inside Template A's prose, and it then hand-built
the call instead of emitting from the frozen template. That emitter was replaced by
`emit_payloads_kimi.py` (see below) so the payload is derived programmatically and
reverse-checked byte-for-byte.

### Attempt 3 (VOID) — claims adjudicated, all refuted

`judge_attempt_3.txt` raises four items. All are refuted by PIL measurement against
**both** images (960×540 frame px, 1 px = 1 pt; render at 2.0833 render-px/frame-px):

1. **"Test label is red in the original"** — REFUTED. Original Test-label **red px = 0**;
   its ink median is (193,190,255) — a pale periwinkle (JPEG-shifted blue). Render ink
   median (233,233,231)/(252,252,253) is white with **red px = 0** as well. Neither side
   is red; the judge read a soft blue cast as red. (Carried forward as a MINOR
   readability-neutral tint difference — see "Known open item" below.)
2. **"The y=42.5 cell is blue/grey, should be mint"** — REFUTED. Band-3 row-3 cells 2/3/4
   are original (204,255,222)/(201,255,225)/(204,255,223) vs render (204,255,225) — mint
   in both, within JPEG noise.
3. **"Badge outline is heavier/darker than the original's"** — REFUTED as house chrome.
   The render's ring is exactly the mandated `6A5ACD` (106,90,205); the original's ring
   median (132,95,163) is JPEG-shifted purple. House chrome is never a discrepancy
   (GROUND RULES a).
4. **"Overall saturation/sharpness differs"** — REFUTED as a format difference (rule e:
   JPEG lecture frame vs crisp PPTX render), explicitly not a fidelity error.

## Build / render currency — PROVEN (no build change was needed)

A fresh `soffice` render of the **current** pptx (private LO profile under
`scratch/tmp/lo_017_kimi_r4/user`, `--convert-to pdf`, then `pdftoppm -png -r 150`) was
compared pixel-by-pixel against the banked `render_3.png`:

- pptx md5 `7374f15e46372898ac8b9b5ac330d15f`
- `render_3.png` md5 `a575c650e993af2f6b363ec2b07a4d44`
- `render_4.png` md5 `a575c650e993af2f6b363ec2b07a4d44` — **byte-identical**
- fresh render vs `render_3`: **0 differing px of 2,251,125**

Banked as `qa/slide017/render_4.png` + `qa/slide017/currency_proof_attempt_4.txt`.

### CRITICAL CORRECTION — the "missing test-table bottom border" defect was a PHANTOM

An earlier scan compared the original (960×540) against the render (2001×1125) at
**unscaled** coordinates. The correct factor is `2001/960 = 2.0833` render-px per frame-px
(equivalently `H_render/540`). At matched scale the render paints the rose bottom border
at render rows 524–525 = frame y **251.7–252.2** (band 1), 389.7–390.7 (band 2),
526.7–527.2 (band 3) — exactly where the original has it. Border-row colour in the render
is `D7BEC2` (215,190,194) in all three bands; the original's is the same rose softened by
JPEG to (224,208,209)/(230,214,215)/(233,221,224). **No build fix is needed and the
component was NOT edited.** The earlier "mint fill suppresses the border" hypothesis is
refuted by direct measurement.

## Selfcheck attempt 4 — 6 FAILs, all 6 refuted as checker artifacts

Script `qa/slide017/adjudicate_selfcheck_fails_attempt_4.py`, output
`adjudicate_selfcheck_fails_attempt_4.txt`. Numbers below are frame px.

| # | selfcheck FAIL | adjudication |
|---|---|---|
| F1 | title RED "count 2 vs 5" | The checker's `colgroups()` merges with a gap of **14 LOCAL px** — 14 original px on the original side but 14 *render* px (6.72 frame px) on the render side. With a symmetric **14 FRAME-px** gap both sides: orig `[(178,278),(380,724)]` vs rend `[(176.2,276.6),(380.7,726.3)]` — identical word runs within 4 frame px. **REFUTED.** |
| F2 | title BLUE "746..866 vs 746..880" | The checker's x window (170..880) includes the badge ring, whose purple `6A5ACD` (b−r=99, g−r=−16) is caught by its blue mask. Excluding the badge zone (x>850) on both sides: orig `[(289,369),(746,850)]` vs rend `[(289.5,369.2),(745.5,849.7)]`. House chrome is never a discrepancy (GROUND RULES a). **REFUTED.** |
| F3 | test B1 bottom gridline "missing [251]" | The checker's `hrows()` merges the mint-filled y-row into the preceding gridline run so the bottom border is swallowed, and it never computes the original's h-rows for comparison. Border IS present at the measured position: render rose `D7BEC2` full-width rows at frame y 251.7 and 252.2 (427/443 columns), colour at (690, 251) = (215,190,194) vs original (224,208,209). **REFUTED.** |
| F4 | test B2 bottom gridline "missing [389]" | Same mechanism. Render rose rows at frame y 389.7/390.2/390.7, colour (215,190,194) vs original (230,214,215). **REFUTED.** |
| F5 | test B3 bottom gridline "missing [527]" | Same mechanism. Render rose rows at frame y 526.7/527.2, colour (215,190,194) vs original (233,221,224). **REFUTED.** |
| F6 | "no ink left of left stroke" | 4124 non-white px left of x56 — **all** of them panel gray `E9E9E7` (the panel starts at x54), **0 other ink**. The original's own margin has 1480 non-white px. **REFUTED.** |

Support measurement (mint y-row cells, identical across all three bands):
orig (200–204,255,221–226) vs render (204,255,225); the label column cell is white in
both. The mint fill is therefore reproduced, not suppressed.

Earlier adjudications still on file and still valid: `adjudicate_kimi_20261024.py`
(items 1–7 of the earlier forensics), `adjudicate_fails*.py` (attempts 1–5).

## Payload derivation — byte-exact, reverse-checked

Emitter: `qa/slide017/emit_payloads_kimi.py` (final version). It follows the certified
slide001 `bank_prompts.py` convention: the banked `*_prompt_4.txt` files hold **only the
`-p` payload prose**, while the shell command lines live in the `.sh` dispatch scripts.
That convention makes the reverse byte-check exact and unambiguous.

- A whole-fenced-block reverse check is impossible for K=4 because "4" already occurs in
  `13.33x7.5in`, in `2.083`, and in `(3)`/`(4)` prose. Instead the emitter asserts that
  the extracted payloads contain **zero** `K` tokens, so the only substitutions inside the
  payload files are `NNN → 017` (plus `attempt K → attempt 4` and, for Template B, the
  NAME + region description) — and the reverse check
  `payload.replace("attempt 4","attempt K").replace("017","NNN") == frozen_payload`
  reproduces the frozen payload **byte-for-byte**.
- Template A payload: `judge_prompt_4.txt`, 4115 chars, sha256 prefix `39b498eaf7048031`,
  md5 `8fc119623b1f020c6d135c834969bf75`, reverse byte-check OK.
- Template B payload: 1914 chars, md5 `8c312dea3126b6ca68d8d2c430095100` (identical for
  all five crops, as the template body is shared), reverse byte-check OK.
- Emitter self-check: `ALL PAYLOAD FILES EMITTED FOR K=4` + `CROSS-CHECK OK: banked
  dispatch scripts reference the emitted payload/crop files`.

## Procedure B crop pairs (cut from `render_4.png`, matched effective scale)

Original crops are LANCZOS-upscaled to the render crop's **exact pixel size**, so the
effective scale is equal by construction; the emitter asserts `abs(sx_r-sx_o)<1e-9`
(and the y axis) for every pair.

| name | frame bbox | size | effective scale x / y | region |
|---|---|---|---|---|
| `wbox` | (497..632, 119..259) | 282×292 | 2.08889 / 2.08571 | W-box band 1: red italic W + underline, `=` bars, the parenthesised 3-value vector (0.1; 1.95; 0.03), blue `‖W‖² = 3.8` |
| `band1` | (84..880, 118..258) | 1658×292 | 2.08291 / 2.08571 | Train table (X1..X8, rows X1/X2/y), two blue arrows, W box, Test table with mint y row |
| `band2` | (84..880, 255..395) | 1658×292 | 2.08291 / 2.08571 | Train table with yellow-highlighted X8 column, W box with (0.67 / 0.64) and `‖W‖² = 2.33` |
| `band3` | (84..880, 392..532) | 1658×291 | 2.08291 / 2.07857 | Train table with yellow-highlighted X8 column, W box with (0.83 / 0.16 / 0.11) and `‖W‖² = 3.59`, Test mint row 26.2 / 34.4 / 42.5 |
| `test` | (660..880, 88..258) | 458×355 | 2.08182 / 2.08824 | Test side: blue Test label box, Test1..Test3 header, 4-column test table, mint y row |

Files: `crop_4_<name>_render.png`, `crop_4_<name>_orig.png`,
`crop_4_<name>_judge_prompt_4.txt`; region descriptions in `region_descs_4.json`.
Five pairs are staged (the protocol's minimum is one per dense region; this slide has
three table bands + a W-box + the Test side).

## Dispatch scripts (staged, byte-exact parameters)

- `qa/slide017/judge_commands_kimi.sh` — Leg A (Template A full-slide), transcript
  `qa/slide017/judge_attempt_4.txt`.
- `qa/slide017/judge_crops_kimi.sh` — the five Procedure B legs, transcripts
  `qa/slide017/crop_4_<name>_judge.txt`; the `--capture` region description is read from
  `region_descs_4.json` (the same file the payload was emitted from).

Both call `scripts/16_vision_gate.sh timeout 1700 python3
.agents/skills/image-analysis/scripts/analyze_image.py comparison <render> <original>
--thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 --transcript
<file> -p "$(cat <payload>)"` — the gate law, the approved 1200 s analyzer wall inside
the 1700 s outer wall, one call per leg, **no retry loop around the gate**.

## Gate evidence — why this lane is parked (congestion, not a defect)

`pgrep -c -f analyze_image.py` probes (the gate law allows max TWO per hour; a probe
count ≥ 8 means "wait"):

| when (UTC) | count | action |
|---|---|---|
| 17:38 | 17 | probe 1 of hour 17 → wait |
| 17:42 | 20 | probe 2 of hour 17 → park |
| 19:20:42 | 12 | probe 1 of hour 19 → wait |
| 19:31:16 | 11 | probe 2 of hour 19 → wait |
| 19:34:27 | 18 | probe 3 of hour 19 (over cap) → stop probing this hour |
| 20:00:13 | 13 | probe 1 of hour 20 → wait (heartbeat + sleep 240) |
| 20:04:53 | 8 | probe 2 of hour 20 → still ≥ 8 → **park honestly** (both probes of hour 20 used) |

Upstream symptom measured by the sibling lane 010: Nvidia `models: images` returning
HTTP 504 `upstream_timeout` at ~61 s, while the local router itself is healthy. The
fleet is saturated with analyzer processes, so the gate law's probe cap is the binding
constraint. **No vision call was dispatched in this window; no verdict was fabricated;
no leg was retry-looped.**

The dispatch scripts now enforce the probe themselves: `judge_commands_kimi.sh` and
`judge_crops_kimi.sh` both run `pgrep -c -f analyze_image.py` before the call (and
before **each** crop leg) and exit 75 with "GATE BUSY" instead of dispatching, so no
leg can ever be launched without a passing probe.

## Known open item (carried, not a defect)

The Train/Test label ink: the render is white, the original reads as a pale periwinkle
(193,190,255) after JPEG softening. Red px count is **0 on both sides** (the attempt-3
judge's "red label" claim is refuted above). This is a tint/readability difference with
no measurable red deficit; it is **not** a fix trigger and must not be "fixed" toward
red, nor silently toward white without a measurement. If the K=4 judge raises it, it is
adjudicated as a MINOR colour-softening difference (rule e) with the measurement banked.

## Final DB rows

To be filled in after certification. Required end state:

```
gen_status       = passed
visual_check     = PASS
visual_transcript= videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide017/judge_attempt_4.txt
visual_attempts  = <n>
worker_id        = ""            (claim released)
```

Current row (parked): `gen_status=building`, `visual_check=NULL`,
`visual_transcript=NULL`, `visual_attempts=0`, `worker_id=kimi-slide017` (claim held,
heartbeat fresh).

Certification is only legal when **both real legs** are banked: `gen_status=passed`
AND `visual_check=PASS` AND `worker_id=""`. A body without a genuine
`FINAL VERDICT: PASS|FAIL` line is VOID and does not count. Note that `claim`/`set`
can reset `gen_status` — always re-`get` after the last `set` and before/after release.

## Exact resume commands

Run from the project root. Nothing else is needed first — the build is verified, the
render is currency-proven, the payloads are byte-checked, the crops are cut at matched
scale, and the dispatch scripts are staged.

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent

# 1) keep the claim alive / take it over if it went stale
python3 scripts/15_progress.py heartbeat 17 kimi-slide017
# (if the heartbeat is stale: python3 scripts/15_progress.py claim 17 kimi-slide017 --force)

# 2) gate probe — max TWO probes per hour; if count >= 8: heartbeat, sleep 240, re-probe
pgrep -c -f analyze_image.py

# 3) Leg A (Template A full-slide) -> qa/slide017/judge_attempt_4.txt
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide017/judge_commands_kimi.sh

# 4) Procedure B crop legs (one at a time, pgrep check before EACH leg)
#    -> qa/slide017/crop_4_{wbox,band1,band2,band3,test}_judge.txt
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide017/judge_crops_kimi.sh

# 5) after BOTH legs land with a real "FINAL VERDICT:" line, adjudicate every
#    FAIL/MINOR PIL-first against BOTH images, then certify:
python3 scripts/15_progress.py set 17 visual_check PASS --worker kimi-slide017
python3 scripts/15_progress.py set 17 visual_transcript \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide017/judge_attempt_4.txt --worker kimi-slide017
python3 scripts/15_progress.py set 17 visual_attempts <n> --worker kimi-slide017
python3 scripts/15_progress.py set 17 gen_status passed --worker kimi-slide017
python3 scripts/15_progress.py heartbeat 17 kimi-slide017
python3 scripts/15_progress.py release 17 kimi-slide017
python3 scripts/15_progress.py get 17   # must read passed / PASS / worker_id=""
```

### Adjudication helper (banked)

`qa/slide017/check_verdict.py <transcript> …` reports VOID for any transcript without a
genuine `FINAL VERDICT: PASS|FAIL` line and rejects an echo of the template's own
"…FINAL VERDICT: PASS or FAIL…" instruction (verified against the banked
`judge_attempt_3.txt`, which it correctly reports as VOID). Exit code 0 only when every
listed transcript is a real verdict. Adjudicate each FAIL/MINOR against **both** images
with `compare_017_orig_vs_render.py` (pre-measured bank) before deciding anything.

### Known deltas to adjudicate against, if a judge raises them

| judge phrasing likely | banked answer |
|---|---|
| "row label glyphs wider than the original" | render's label X₁ ~14 px wide vs original ~11 px at equal cap height; both are bold serif in the build; data cells and header match within 1 px → MINOR font/medium metric |
| "row labels sit slightly high" | label X₁ y165..178 (render) vs y169..181 (original); data cells match (y166..178 vs y167..179) → MINOR vertical centering |
| "header row text smaller" | header X1 cap 13 rows (render) vs 15 rows (original) → MINOR |
| "Test label should be red" | red px = 0 on BOTH sides (original ink median (193,190,255) = JPEG-softened periwinkle) → REFUTED |
| "42.5 cell is the wrong colour" | band-3 y-row cells are mint in both: orig (204,255,222)/(201,255,225)/(204,255,223) vs render (204,255,225) → REFUTED |
| "badge ring too light/thin" | render ring is exactly the mandated 6A5ACD (106,90,205); original median (132,95,163) is JPEG-shifted purple → house chrome, REFUTED |
| "test table bottom border missing" | border present at frame y 251.7/252.2, 389.7–390.7, 526.7/527.2 (render rose D7BEC2) = the original's positions → REFUTED |
| "ink left of the left stroke" | 4124 px left of x56 are all panel gray E9E9E7 (panel starts x54); 0 other ink → REFUTED |
| "colours more saturated than the original" | crisp PPTX render vs JPEG lecture frame → rule (e), expected |

## Banked artifacts (`recreated_pptx/qa/slide017/`)

| file | what |
|---|---|
| `worker_report.md` | this report |
| `render_1.png` … `render_4.png` | all attempt renders, preserved (render_4 = current) |
| `currency_proof_attempt_4.txt` | md5s + 0-diff currency proof + house chrome PASS |
| `emit_payloads_kimi.py` | programmatic payload emitter + reverse byte-check + crop cutter |
| `judge_prompt_4.txt` | Template A `-p` payload (4115 chars, reverse byte-check OK) |
| `crop_4_*_judge_prompt_4.txt` | Template B payloads (5, identical body, reverse byte-check OK) |
| `crop_4_{wbox,band1,band2,band3,test}_{render,orig}.png` | matched-scale crop pairs |
| `region_descs_4.json` | per-region `--capture` descriptions |
| `judge_commands_kimi.sh` / `judge_crops_kimi.sh` | staged dispatchers (Leg A + 5 crop legs) |
| `judge_attempt_3.txt` | VOID attempt-3 body (no `FINAL VERDICT:` line) — kept as evidence |
| `selfcheck_attempt_{1..4}.py/.txt` | selfcheck runs; attempt 4 reports FAIL(6), all 6 refuted |
| `adjudicate_selfcheck_fails_attempt_4.py/.txt` | the F1..F6 refutations with measurements |
| `adjudicate_kimi_20261024.py` | earlier PIL forensics (items 1–7) |
| `adjudicate_fails{,_2..5}.py`, `measure_017.py/.txt` | earlier attempt adjudications + measurements |
| `build_entry_attempt_4.js`, `component_attempt_4.js` | build-side artifacts from the attempt-4 pass |
| `bank/` | peer bank (wbox peer crop + its generator) |
| `compare_017_orig_vs_render.py/.txt` | full side-by-side original-vs-render measurement bank (168 cells) |
| `check_verdict.py` | transcript verdict extractor (VOID detector, template-echo rejecter) |

---

# Pre-judge PIL sweep — original vs render_4 (added 19:5x UTC, before dispatch)

`compare_017_orig_vs_render.py` measures the same quantities on BOTH images (original
960×540 native; render_4 downscaled LANCZOS ×2.0844 to 960×540): chrome, both tables'
gridlines, all 168 table cells' ink counts, label boxes, W-box borders, norm lines,
arrows, title runs, and the Train/Test label ink colour. Bank:
`compare_017_orig_vs_render.txt`. Result: **no missing element, no wrong table value,
no frame-containment violation.** The only deltas found are MINOR-scale and are banked
here so any judge finding can be adjudicated immediately.

| finding | measurement (frame px) | class |
|---|---|---|
| Render's train/test **row-label glyphs are ~3 px wider** at equal cap height | label "X₁": original X core x100..107 (8 px) / cap y169..181; render X core x100..107 but with the stroke pairs at x99..112 (14 px) / cap y165..178. Both are **bold serif** in the build (`cellStyle(... bold: true)`, `fontFace: SERIF`); the data cells and the header row match the original within 1 px. | MINOR — font/medium metrics (the original is a compressed video frame, rule e) |
| Render's row labels sit **~2–3 px higher** than the original's | label "X₁" y165..178 (render) vs y169..181 (original); the row's data cells are y166..178 vs y167..179 — the data text matches, only the label column is offset | MINOR — vertical centering inside the cell |
| Render's **header row cap height is ~2 px shorter** | header "X1" y135..147 (render, 13 rows) vs y136..150 (original, 15 rows) | MINOR |
| Ink counts in the render run **10–30 % higher** in most cells | e.g. B1 r0 c2: original 90 ink px vs render 99; label column X₁: original 56 vs render 84 | not a defect — the render is crisp black (0,0,0) while the original's ink is JPEG-softened (median 38,40,37), so the original falls below the ink threshold |
| Render's **test table y-row fills** are a uniform mint (204,255,225) vs the original's per-cell (200–204,255,220–227) | all three bands | not a defect — the original's per-cell variance is JPEG noise around one fill |
| Render's **right red stroke** reads at x900 (197,27,27) = C00000; the original's at x901 (106,46,56) | the original's stroke is 1–2 px right and JPEG-desaturated, and its x900 column is faint, which is why the original's gridline scan stops at x872 while the render's also catches the house stroke's AA edge at x899 | not a defect — house chrome (GROUND RULES a), and the stroke's x agrees within 1 px |

Nothing here is a BLOCKER/MAJOR trigger, so no build change was made before dispatch.
The glyph-width and vertical-offset deltas are recorded as the standing adjudication for
any MINOR the K=4 judges raise about the row-label column.

---

# Follow-ups / known gaps (non-blocking)

1. **Dangling doc reference:** `build/components/slide_017.js` cites its geometry source
   as `recreated_pptx/qa/slide017/MEASUREMENTS.md`, but that file does not exist (the
   parent slide 013 has one). The measurements themselves ARE banked — `measure_017.txt`
   (the full dossier the component was built from) and `compare_017_orig_vs_render.txt`
   (the original-vs-render bank). A worker who changes the table geometry should write
   `MEASUREMENTS.md` from those two files rather than re-measure; this lane did not
   create it because no build change was made here.
2. **Namespace-root `qa/worker_report.md` is slide 005's report** (it is titled
   "Worker report — slide 005" and duplicates `recreated_pptx/qa/slide005/worker_report.md`).
   It was left untouched; this lane's report is `recreated_pptx/qa/slide017/worker_report.md`.
3. **Train/Test label ink** — the one open colour question, described in "Known open
   item" above: white in the render vs JPEG-softened periwinkle (193,190,255) in the
   original, red px = 0 on both sides. Not a fix trigger; adjudicate as MINOR if raised.
4. **Row-label glyph width / vertical offset** — the two MINOR deltas measured in the
   pre-judge sweep above. Both are inside the tolerance the deck's other certified
   slides already carry for font substitution; no change made without a judge raising
   them as MAJOR.

---

# Certification record — K=4 legs PASSED (2026-10-25, resumed on local workspace)

Workspace moved from the codespace to the local machine; render_4.png and the five
crop pairs were NOT migrated (all *.png under qa/ were lost in the move). They were
regenerated, byte-verified against the banked evidence:

- `slide_017_recreated.pptx` md5 `7374f15e46372898ac8b9b5ac330d15f` — matches the
  banked currency proof (no rebuild).
- Fresh 150dpi LO render re-banked as `render_4.png` (2001x1125); deck house-chrome
  checker: **PASS** (panel x112-1882, strokes L/R/bottom, badge (1824,152) d=68).
- `emit_payloads_kimi.py` re-run: judge_prompt_4.txt md5 `8fc119623b1f020c6d135c834969bf75`
  — byte-identical to the banked payload; five crop pairs re-cut at matched effective
  scale; payload reverse byte-checks OK.
- Dispatch scripts' hardcoded codespace path `/workspaces/codespaces-blank/ai_llm_slides`
  repointed to `/home/ahmed/Projects/ai_llm_slides` (paths only; payloads untouched).

## Verdicts (all real `FINAL VERDICT:` lines)

| leg | transcript | verdict |
|---|---|---|
| Template A full-slide | `judge_attempt_4.txt` | **PASS** (2 MINORs, both pre-adjudicated bank items: λ-run blue title ink is the build's measured design; Train/Test label shade = JPEG softening, rule e) |
| wbox | `crop_4_wbox_judge.txt` | **PASS** (3 MINORs, adjudicated below) |
| band1 | `crop_4_band1_judge.txt` | **PASS** |
| band2 | `crop_4_band2_judge.txt` | **PASS** |
| band3 | `crop_4_band3_judge.txt` | **PASS** |
| test | `crop_4_test_judge.txt` | **PASS** |

`check_verdict.py` regex widened to accept markdown-prefixed verdict lines
(`## FINAL VERDICT: **PASS**`) — the VOID detector semantics unchanged
(judge_attempt_3.txt still VOID, control verified).

## wbox MINORs — PIL adjudication (both images, frame px)

1. "missing blue underline under W in the norm line" — REFUTED. Render blue
   underline rows y 238.6..244.3 (145 blue px) vs original 239..241 (33 px, JPEG
   thinned). The underline is present on both sides.
2. "IMG1 spaced '‖W‖² = 3.8', IMG2 tight" — REFUTED. Original gaps: ‖²→= 10px,
   =→3.8 5px; render 6.7px / 5.7px. Both are spaced; deltas ≤3px (JPEG noise).
3. "red border slightly heavier in IMG1" — rule (e) medium difference as the judge
   itself conceded (video-capture softening). No action.

## Final DB rows

gen_status=passed, visual_check=PASS, visual_attempts=4, visual_transcript=
videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide017/judge_attempt_4.txt,
worker_id="" (released). **SLIDE 017 CERTIFIED.** Slide 018 unblocked.
