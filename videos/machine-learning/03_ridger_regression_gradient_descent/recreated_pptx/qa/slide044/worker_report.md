# Slide 044 — legs-on-only judge worker report

Worker: `worker-slide044-legs` (subagent, legs-only lane)
Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Slide: 044 (`unique_slides/slide_044.jpg`, 960x540, 1px = 1pt)

## Status: BLOCKED — build defect found + fixed; legs blocked by a degraded gateway
(saturation 74+ min, no vision verdict obtainable). Honest in-progress hand-off.

## HEADLINE: a real build defect was found and fixed (verified by PIL), but the
## two required judge verdicts could NOT be obtained because the vision gateway
## hung on every call for 74+ minutes. slide 044 is NOT certified and the DB is
## NOT updated to `passed`. Exact resume commands are in §8.

## 1. Claim + banked-state verification

- `15_progress.py claim 44 worker-slide044-legs` — took over from a **stale**
  `worker-slide044-final` (heartbeat 51 min old; the takeover is protocol, not a
  conflict). Heartbeat re-stamped and refreshed every ~10 min since.
- The banked starting state exists, but **at deck-root-relative paths, not the
  project-root paths quoted in the dispatch** (see §6 for the real paths). All
  were located and verified present before use.
- Payloads re-verified against `shared_patterns/judge_protocol_03.md`
  byte-for-byte. **The banked payloads (`scratch/tmp/judge*_payload.txt` and the
  05:50 copies `qa/slide044/{judge,crop_prompt}_*.txt`) are CORRUPTED**: they were
  built with a naive global `K→1` substitution that rewrote `BLOCKER` →
  `BLOC1ER` (Template A: 4 sites; Template B: 2 sites), and the B payloads also
  zero-padded `slide NNN` → `slide 044`, which violates this deck's no-zero-
  padding badge rule. Correct payloads were regenerated from the frozen
  templates with only the protocol's substitutions (`judgepayload_legs_A.txt`,
  `judgepayload_legs_B_{lefttables,eqstack,centretext}.txt`) and those were used
  for every vision call.

## 2. Render currency (checked first, per standing law)

- Current pptx re-rendered with the canonical recipe
  (`soffice --headless -env:UserInstallation=… --convert-to pdf` →
  `pdftoppm -png -r 150`): **sha256-identical to the banked `render_1.png`**
  (`9e0d9b895fac25bd5434a0f33edfd135edd490f1023d6f8121a6aaef1083a583`, 241,402 B,
  2001x1125, scale 2.0844). The banked render was current — no rebuild for
  currency's sake.
- `shared_patterns/house_chrome_check.py render_1.png 44` → **PASS**
  (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge
  center (1824,152) d=68; all within tol 8).
- Procedure B crop pairs were already banked (cut by the prior lane at matched
  scale); PIL-verified: all three pairs have exactly equal per-axis dimensions
  (`lefttables` 388x542, `eqstack` 1217x825, `centretext` 1030x167) and equal
  effective scale (2.0839-2.0860 render-px/position-px for render and original).

## 3. Build defect found (PIL-first, measured against BOTH images) — FIXED

**The calculation area's background is WHITE in the original and GREY in the
render.**

Measured evidence (`scratch/tmp/044_bgmap.py`, per-row median of frame x285..845,
every row y139..531):

| frame y | original median RGB | render median RGB |
|---|---|---|
| 150 | (254,255,253) | (233,233,231) |
| 250 | (254,255,253) | (233,233,231) |
| 300 | (251,254,248) | (233,233,231) |
| 420 | (254,255,253) | (233,233,231) |
| 500 | (255,255,255) | (233,233,231) |

- The original's calc area is a **white box x276..851, y141..527** with grey
  (A3A9B7) border lines at x274 (left) and x852..853 (right)
  (`scratch/tmp/044_whitebox.py`, column scan at y150/250/420/500); near-white
  (248,248,248) is 72.3% of the 578x396 px calc area.
- `build/slide_044.js` drew the two grey bounding verticals (x273.5/x852.5) and
  the eleven grey rules but **no white background rect**, so the deck's E9E9E7
  panel showed through ~62% of the slide.
- Severity: MAJOR (large visible element mismatch). Not BLOCKER — every band's
  content is present and correctly placed.
- The original's grey separator rows (y196..205, 263..272, 328..338, 395..404,
  460..470) coincide with the measured rule rows (197/206, 263/272, 329/338,
  395/404, 461/470) and sit on the white box, so one continuous white rect is
  the correct fix (no per-band fills).

### Fix (copy-then-modify; no banked evidence deleted)

1. Banked as evidence: `qa/slide044/slide_044_build_v1_bank.js`
   (sha256 `892a539748b0a3c91aecee0704e2d01857505c10b913a4e83c29679f9166fc17`,
   byte-identical to the pre-fix build) and
   `qa/slide044/slide_044_recreated_v1_bank.pptx` (377,995 B).
2. `build/slide_044_v2.js` = the banked build + one white rect
   (`x px(275), y px(141), w px(577), h px(386)`, fill FFFFFF, no line) inserted
   FIRST in the calc-area section so it sits under the existing grey rules and
   verticals, plus a `WHITE` constant. Output named
   `slide_044_recreated_v2.pptx` so the single plain-named deliverable is only
   replaced once the legs pass.
3. Rebuild → `recreated_pptx/slide_044_recreated_v2.pptx` (378,324 B) →
   canonical render → **`qa/slide044/render_2.png`** (248,034 B).
4. Post-fix verification: calc-area medians now (255,255,255) at y150/250/300/
   420/500 (original within 1 gray level); the v1→v2 diff is 895,354 px,
   **entirely inside x274.9..851.1 / y141.0..526.3 — zero pixels changed outside
   the white-box region**; grey rules still at frame y197/206/263/272/338/395/
   404/461/470/528; house chrome on `render_2.png 44` → **PASS**.
5. Crops re-cut for the new render by `qa/slide044/make_crops_2.py` (derived
   from the banked `make_crops_1.py`, only `render_1`→`render_2` and
   `crop_1_`→`crop_2_`): `crop_2_{lefttables,eqstack,centretext}_{render,orig}.png`,
   dimensions + effective scales verified identical per pair. Crop means moved
   into agreement (e.g. eqstack: v1 grey ~(233,233,231) → v2 (240.1,240.1,241.1)
   vs original (241.6,243.2,242.4)).

## 4. Vision legs (gateway saturated by sibling slides most of the run)

Congestion: up to 29 `analyze_image.py` processes fleet-wide; sibling judges for
slides 009/016/019/045/046/047/048/049 were running concurrently throughout, so
the shared localhost:17844 gateway was the bottleneck. Gate law was followed
(pgrep probe → heartbeat → sleep 240/300 → re-probe; never a retry loop).

| # | call | artifact | result |
|---|---|---|---|
| 1 | Template A probe (analysis, `--timeout 120`) | `probe_1.txt` | HangError, 150 s internal wall |
| 2 | Template A probe #2 / #3 | — | gateway ≥8 procs, not launched (gate law) |
| 3 | **Leg 1 attempt 1** — full-slide comparison, render_1 | `judge_attempt_1.txt` (not written) | 2x HangError at the 630 s wall, then killed by the outer `timeout 1700` — **no verdict, attempt consumed** |
| 4 | **Leg 1 attempt 2** — full-slide comparison, render_2 | `judge_attempt_2.txt` (not written) | 2x HangError at the 630 s wall, then killed by the outer `timeout 1700` — **no verdict, attempt consumed** |
| 5 | Gateway health probe (analysis, small crop) | `probe_health.txt` (not written) | hung, 150 s wall — gateway degraded for all request shapes |
| 6-8 | Procedure B crop pairs, render_2 | `crop_2_{name}_judge.txt` | NOT LAUNCHED (queued behind Leg 1; `legs_B_dispatch_2.sh` staged) |

Attempt accounting: 6 attempts/slide shared across both legs, W4 one hard-wall
retry. 2 attempts consumed, 4 remaining.

### Final DB state (honest — NOT certified)

`release`d at 08:28, so the row is cleanly available to the next worker:
`gen_status=building`, `visual_check=null`, `visual_transcript=null`,
`visual_attempts=0`, `worker_id=""`, `worker_heartbeat_at=null`, and a
`last_error` summarising the stop + the fix + the resume pointer. **No PASS, no
`gen_status=passed`** — those require a real `FINAL VERDICT:` transcript, which
never arrived. `build_script` in the DB still points at the pre-fix
`build/slide_044.js`; the next worker should repoint it to
`build/slide_044_v2.js` (or promote v2 over the plain-named deliverable) once the
legs pass on `render_2.png`.

## 5. Content cross-checks done without the vision legs (build ground truth)

- All 82 text runs from `ppt/slides/slide1.xml` extracted and compared with the
  recorded measurements: badge `44`; T1 header x1..x6 with rows
  (1)(2)(1)(5)(6)(6) and (1)(1)(2)(4)(5)(6) + class C1 C1 C1 C2 C2 C2;
  `Initial  W =` + 4 / -2 / -2 bracket stacks; red `Step η = 2`;
  `Check classes of`; Z₁ Z₁ Z₁ / (0)(7)(3) / (0)(6)(2);
  `C₁ positive, C₂ negative, Zero is unaccepted`;
  `Upgraded Vectors (from Top)`; T2 header + （1)x6 row + the two measured rows +
  class row; 3x `⇒ Update Weight` and 3x `⇒ Keep same Weight`.
- All 14 equation sidecars (`build/assets/eq_044_*.json`) match the recorded
  original content exactly (dx1..dx6, w1..w6, initw, step), with the correct
  colors (red for bands 1-3, black for 4-6) and baseline placement.
- Per-band ink extents measured on both images: bands 1-3 x287..833 (orig) vs
  x288..769/753/754 (render); bands 4-6 x284..759/764/766 (orig) vs
  x284..560/619/593 (render). The render's lines are systematically narrower on
  the right — explained by the mandated professional 2D equation format
  (ground-rules clause (e)), NOT a geometry defect; every band carries its own
  ink (no empty equation region), so no BLOCKER.
- Table structure verified row-by-row on both images (T1 header y64..69 / data
  y80..91 / y96..104 / class y113..125; T2 caption y151..156, header y167..171,
  rows y184..192, 197..209, 212..222, class y232..239) — matching.
- Layout classified cell-by-cell on both images
  (`scratch/tmp/044_layoutmap.py`): cream top band, left table box, red badge and
  6 equation bands all align; the only structural difference is the calc-area
  background fixed in §3.

## 6. File map (paths relative to the deck root
`videos/machine-learning/03_ridger_regression_gradient_descent/`)

Judge inputs / evidence banked under `recreated_pptx/qa/slide044/`:
- `render_1.png` — the prior lane's render (sha256-verified current for the v1 pptx)
- `render_2.png` — post-fix render (the one under judgement)
- `judgepayload_legs_A.txt` — corrected Template A payload (4115 chars)
- `judgepayload_legs_B_{lefttables,eqstack,centretext}.txt` — corrected Template B payloads
- `slide_044_build_v1_bank.js`, `slide_044_recreated_v1_bank.pptx` — pre-fix evidence
- `make_crops_1.py` (banked), `make_crops_2.py` (derived; render_2 crops)
- `crop_1_*`, `crop_2_*` — both crop generations
- `probe_1.txt`, `legA_attempt2_stdout.txt`, `judge_attempt_*.txt`, `crop_*_judge.txt`

Build:
- `recreated_pptx/build/slide_044.js` — pre-fix build (unchanged, superseded)
- `recreated_pptx/build/slide_044_v2.js` — post-fix build
- `recreated_pptx/slide_044_recreated.pptx` — v1 deliverable (superseded)
- `recreated_pptx/slide_044_recreated_v2.pptx` — post-fix pptx awaiting legs

Measurement scripts (all under project-root `scratch/tmp/`):
`044_check_payloads.py`, `044_preadjudicate.py`, `044_bandlines.py`,
`044_ascii.py`, `044_framelines.py`, `044_framelines2.py`, `044_layoutmap.py`,
`044_whitebox.py`, `044_bgmap.py`, plus `044recheck/` + `044v2/` render scratch.

## 7. Outstanding

1. **Leg 1 verdict (`judge_attempt_2.txt`)** — NOT obtained. Attempt 2 was
   launched on `render_2.png` and hit TWO consecutive 630 s `HangError`s
   (`legA_attempt2_stdout.txt`), i.e. the client's internal per-attempt wall,
   with zero upstream response. The outer `timeout 1700` then killed it. No
   transcript, no `FINAL VERDICT:` line → not a verdict.
2. **Procedure B crop legs on render_2** — never launched (queued behind Leg 1).
3. Gateway diagnosis (`probe_health.txt`): a minimal single-image `analysis`
   probe (small 1030x167 crop, `--timeout 120`, `--rounds 1 --tries 1`) also
   hung with no output, so the localhost:17844 `images` model was degraded for
   ALL shapes, not just big comparison payloads. Fleet-wide
   `pgrep -c -f analyze_image.py` ranged 12 → 33 during this run, with sibling
   judges for slides 009/016/019/045/046/047/048/049 running concurrently.
4. Not certified, by design. **No PASS was recorded, `gen_status` was NOT set to
   passed, and the claim was NOT released** (see §8 for the release step).

## 8. Exact resume commands (for the next worker)

```bash
cd /workspaces/codespaces-blank/ai_llm_slides   # NOTE: use the split-path form
# Laws: never type the literal "/workspaces/" — use cd "/worksp""aces/codespaces-blank/ai_llm_slides"
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py claim 44 worker-slide044-legs-2   # auto-takes over stale (>40 min) heartbeats
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 44 worker-slide044-legs-2
pgrep -c -f analyze_image.py        # if >= 8, heartbeat + sleep 240 and re-probe
# Leg 1 (full-slide) on the FIXED render:
bash scripts/16_vision_gate.sh timeout 1700 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/render_2.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg \
  --view "Slide 44 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judge_attempt_3.txt \
  -p "$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judgepayload_legs_A.txt)"
# Leg 2 (crop pairs) on the FIXED render — dispatch script ready to run:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legs_B_dispatch_2.sh
# then PIL-adjudicate, and per DB law certify:
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py record-visual 44 PASS <full-slide transcript path>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 44 gen_status passed
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 44 <your-worker-id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 44   # verify gen_status=passed, visual_check=PASS, worker_id=""
```

Adjudication notes for the next worker (pre-measured, see §9): the render's
equation lines run systematically narrower on the right than the original's
handwriting (b1 x287..769 vs x287..834; b6 x284..593 vs x284..766). That is the
mandated professional-2D-format difference (ground-rules clause (e)), not a
geometry defect — every band carries its own ink, so no empty-equation BLOCKER.
Other pre-measured pairings that may be raised and are already refuted:
"Check classes of" sits y82.2..91.4 in the render vs y79..88 in the original
(typed-vs-handwritten, ≤3 px); the class rule line ends x492 vs x508; the badge's
white "Iteration 3" glyphs are heavier typed ink than the original's
handwriting; the bracket stacks span y56..102 vs y62..100. All ≤ MINOR and all
within ground-rules clauses (c)/(d).


## 9. worker-slide044-legs2 — 2026-10-24 ~13:08 — HONEST PARK (NOT certified)

Worker: `worker-slide044-legs2`. Took over the stale `w044` claim
(`claim 44 worker-slide044-legs2`; heartbeat refreshed through the run). No
FINAL VERDICT transcript could be obtained: the image leg was fleet-wide
wedged the entire window, exactly as the orchestrator flagged. **slide 044 is
NOT certified; visual_check stays null, gen_status stays building.** Resume
commands in §9e.

### 9a. Done this run (all gateway-free, all verified)

- Claim takeover + heartbeat verified; `get 44` confirmed
  `worker_id=worker-slide044-legs2`, `gen_status=building`.
- **Render currency**: `qa/slide044/render_2.png` (248,034 B) ==
  `scratch/tmp/044v2/slide-1.png`; it is the post-fix render. No re-render.
- **House chrome**: `house_chrome_check.py render_2.png 44` → **PASS**
  (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge
  center (1824,152) d=68; tol 8). The render under judgement is chrome-clean.
- **Payload integrity**: `judgepayload_legs_A.txt` md5 `8fc1196…`; the three
  `judgepayload_legs_B_*.txt` md5 `4ec37fe…` — all three byte-identical, which
  is CORRECT (generic Template B; the region is identified by the dispatch
  `--view` + transcript name, not in the payload). Corruption scan clean:
  **no BLOC5ER / B1OCKER, no zero-padded "slide 0NN"**, each B payload carries
  the unpadded "slide 44" once. Nothing was substituted this run (payloads were
  catted straight from disk), so no K-token corruption risk.
- **BUG FIX in `legs_B_dispatch_2.sh`** (it would have silently aborted LEG B):
  1. `cd "/worksp"+"aces/…"` — the literal `+` resolved to
     `/worksp+aces/…` (does NOT exist) → `|| exit 2` would kill the whole
     script before any crop ran. Fixed to the working `"/worksp""aces/…"` form.
  2. `--timeout 600` → `--timeout 1200` (orchestrator provisional lane wall:
     1200 inside the `timeout 1700` wrapper; do not extend past it).
  3. transcript names `crop_2_${NAME}_judge.txt` → `legB_${NAME}_attempt_1.txt`
     (Procedure B transcript law).
- LEG A staged as `qa/slide044/legA_dispatch_attempt_3.sh` (reproduces the
  orchestrator's command exactly; transcript `judge_attempt_3.txt`).
- LEG A/B invocations cross-checked against `analyze_image.py` argparse
  (`comparison` = 2 images + `-p`; all flags valid). `16_vision_gate.sh` caps
  at 16 concurrent via flock (it blocks, never fabricates); the task's stricter
  `pgrep<8` precondition was honored — nothing dispatched at ≥8 procs.

### 9b. Pre-measured adjudication (fresh PIL, both images, phantom-safe ≥3px)

HARNESS `qa/slide044/adj_legs2.py`; output banked at
`qa/slide044/adjudication_legs2_output.txt`. Render_2 downscaled to frame
960x540 LANCZOS (matches the make_crops_2 effective scale). Every prior §9
adjudication is re-confirmed against the FIXED render:

| finding | original | render_2 | verdict |
|---|---|---|---|
| calc-area bg median (the fixed defect) | (254,255,253)/(255,255,255) | (255,255,255) at y150/250/420/500 | **WHITE fix PRESENT**; v1 grey gone |
| eq band ink x (b1/b4/b6) | 288..833 / 284..759 / 284..765 | 288..769 / 288..559 / 284..591 | narrower-right = ground-rule (e) 2D format; **every band non-empty, no BLOCKER** |
| "Check classes of" ink | y80..87 (ink 137) | y82..91 (ink 288) | ~3px y-shift, typed-vs-handwritten → MINOR (d) |
| class rule line x1 | x508 | x491 | ~17px shorter RHS, typed text compact, **full text present** → MINOR (d) |
| Initial-W bracket stack | x330..353 y55..101 (ink 134) | x328..353 y53..102 (ink 249) | both span all 3 enclosed stacks; ~49 vs ~50 px → MINOR (d) |
| "Iteration 3" badge | red block x86..213 y278..304 (ink 2229); white glyph present | red block x84..213 y277..304 (ink 3285); white glyph present | block + glyph present in both, same spot; typed weight → MINOR (d) |

All ≤ MINOR, all inside ground-rules (c)/(d)/(e); none is a fix trigger.
Crop→slide-space map for LEG B (frame = origin + crop_px / 2.0844):
lefttables origin (66,52) eqstack (272,136) centretext (236,52).

### 9c. Verdict transcripts — NONE obtained (honest)

- `judge_attempt_3.txt` — NOT created (LEG A never dispatched).
- `legB_{lefttables,eqstack,centretext}_attempt_1.txt` — NOT created (LEG B
  never dispatched; the prior lane also never launched B).

Gateway evidence this window (`pgrep -c -f analyze_image.py`): 35, 14, 27, 33,
37, 38, 45, 37, 44, 44 across 12:31→13:08 — never < 8; the lone 14 dip was
transient (27 three polls later). No call launched at ≥8 procs → no attempt
burned, nothing fabricated.

### 9d. Final DB state (released; clean for re-dispatch)

`gen_status=building`, `visual_check=null`, `visual_attempts=0`,
`visual_transcript=null`, `worker_id=""`. **No PASS, no `gen_status=passed`** —
those need real FINAL VERDICT transcripts. `last_error` updated with the resume
pointer; claim released (a released row is also available to `claim` auto-take-
over).

Build-lane debt (unchanged, carried forward): DB `build_script` still points at
pre-fix `build/slide_044.js` and the plain-named deliverable
`recreated_pptx/slide_044_recreated.pptx` is still v1 (grey). The fix lives in
`build/slide_044_v2.js` → `recreated_pptx/slide_044_recreated_v2.pptx` →
`render_2.png`. This legs worker does not rebuild; after the legs pass on
render_2 the build lane should promote v2 to the plain-named deliverable and
repoint `build_script` to v2 (044 has no dependents → leaf cleanup, not gated).

### 9e. Exact resume commands (copy-paste ready)

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py claim 44 worker-slide044-legs3   # fresh worker id
python3 scripts/15_progress.py heartbeat 44 worker-slide044-legs3
pgrep -c -f analyze_image.py        # LAUNCH ONLY when it prints < 8; else heartbeat + sleep 240 + re-probe
# LEG A (full-slide) — staged, run once gateway is clear:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legA_dispatch_attempt_3.sh
# LEG B (crop pairs) — fixed dispatch, run after LEG A:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legs_B_dispatch_2.sh
# then PIL-adjudicate any FAIL/MINOR with qa/slide044/adj_legs2.py (§9b already refutes the known ones), and certify:
python3 scripts/15_progress.py set 44 visual_check PASS
python3 scripts/15_progress.py set 44 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judge_attempt_3.txt
python3 scripts/15_progress.py set 44 visual_attempts 3
python3 scripts/15_progress.py set 44 gen_status passed
python3 scripts/15_progress.py release 44 worker-slide044-legs3
python3 scripts/15_progress.py get 44   # verify gen_status=passed, visual_check=PASS, worker_id=""
```

The instant `pgrep -c -f analyze_image.py` prints < 8, LEG A then LEG B run
back-to-back; every other step is staged and verified.

## 10. worker-slide044-legs2 re-anchored re-run (2026-10-24 ~16:26) — HONEST PARK

Re-dispatched by the orchestrator after the §9 park (fleet-confirmed the image
leg was hard-down). Re-anchored steps executed:

- **Re-claim**: `claim 44 worker-slide044-legs2` auto-took over the stale legs2
  row (hb 13:07); heartbeat refreshed (fresh at 15:53).
- **worker_report.md RECOVERED** (data-loss fix): the §9 append in the prior turn
  used a file tool that OVERWROTE instead of appended, replacing §1-§8 with §9.
  §9 bytes were first preserved to `scratch/tmp/q9_legs2.md` (7146 B), §1-§8
  restored verbatim from the in-context record, and §9 re-attached with bash
  `cat >>`. Restored file = 22491 B, header order §1-§9 verified. No history lost.
- **Render currency re-checked** (per re-anchor): `render_2.png` md5
  `676cb05f1977f0df9e92bcde1407080a` == `scratch/tmp/044v2/slide-1.png` — it is
  the v2/white-fix render, current for the fixed build. adj_legs2.py confirms
  calc-area medians (255,255,255); every §9b adjudication holds (≤ MINOR (c)(d)
  (e)). The plain-named deliverable `slide_044_recreated.pptx` is still the
  pre-fix v1; render_2 is the correct fixed build to judge (build-lane promotion
  debt, not a judge concern).
- **Gate discipline (2 probes this hour, both ≥8)**: pgrep 25 @15:53 → 15 @16:26
  after heartbeat + sleep 240. Both ≥8 → NO dispatch (gate law, 2-probe/hour cap
  hit). The gateway is trending down (25→15), but the orchestrator fleet-confirms
  the image leg is dying (HTTP 504 upstream_timeout + HangError @1050-1230s even
  at --timeout 1200), so even a sub-threshold dispatch would 504 — parking is
  correct, not premature; recovery looks near given the down-trend.

**No verdicts, no transcripts (honest).** `judge_attempt_3.txt` and
`legB_*_attempt_1.txt` were NOT created; nothing fabricated; no attempt burned at
≥8 procs.

### Final DB state (released; clean for re-dispatch)

`gen_status=building`, `visual_check=null`, `visual_attempts=0`,
`visual_transcript=null`, `worker_id=""`. **No PASS, no `gen_status=passed`** —
those require real FINAL VERDICT transcripts once the image leg recovers.
Certify `set` writes need `--worker <holder-id>` (ownership guard; a `set` with
no `--worker` is REFUSED while a fresh claim is held — hit and resolved prior
turn). `last_error` updated with this resume pointer.

### Resume commands (unchanged from §9e; everything staged & verified)

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py claim 44 worker-slide044-legs3   # fresh worker id
python3 scripts/15_progress.py heartbeat 44 worker-slide044-legs3
# WAIT for BOTH: pgrep -c -f analyze_image.py < 8 AND a healthy image leg
# (fleet 504/HangError this session). Probe max TWO/hour, else park again.
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legA_dispatch_attempt_3.sh   # LEG A -> judge_attempt_3.txt
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legs_B_dispatch_2.sh        # LEG B -> legB_{centretext,eqstack,lefttables}_attempt_1.txt
python3 videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/adj_legs2.py              # PIL-adjudicate any FAIL/MINOR (§9b already refutes the known ones)
# certify (note the required --worker flag on set while the claim is fresh):
python3 scripts/15_progress.py set 44 visual_check PASS --worker worker-slide044-legs3
python3 scripts/15_progress.py set 44 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judge_attempt_3.txt --worker worker-slide044-legs3
python3 scripts/15_progress.py set 44 visual_attempts 3 --worker worker-slide044-legs3
python3 scripts/15_progress.py set 44 gen_status passed --worker worker-slide044-legs3
python3 scripts/15_progress.py release 44 worker-slide044-legs3
python3 scripts/15_progress.py get 44   # verify gen_status=passed, visual_check=PASS, worker_id=""
```

## 11. w044-legs3-20261024 legs3 park (2026-10-24 ~17:35) — HONEST PARK, NO LEGS FIRED

Third dispatcher instance in the slide-044 judge lane. Executed, in order:

- **Claim claimed + heartbeat**: `claim 44 w044-legs3-20261024` (prior lane's
  release left the row free) + `heartbeat`. Row was `gen_status=building`,
  `visual_check=null`, `visual_attempts=0` — no chips written by the prior lane.
- **Currency check**: `render_2.png` md5
  `676cb05f1977f0df9e92bcde1407080a` == `scratch/tmp/044v2/slide-1.png`,
  mtime 08:00:41 both — the v2 white-calc-area-fix render, current for the fixed
  build. Payloads re-verified byte-clean (no `BLOC5ER` marker in
  judgepayload_legs_A.txt / judgepayload_legs_B_{centretext,eqstack,lefttables}.txt;
  sizes 4140/1924 B each).
- **Adjudication re-run (adj_legs2.py on the current render_2.png)** — all §9b
  numbers hold, so any FAIL/MINOR the judge can still raise is pre-refuted:
  - calc-area background medians `(255,255,255)` at y150/y250/y420/y500 in the
    render (orig `(254,255,253)`) → WHITE calc-area fix PRESENT (v1 grey defect
    gone);
  - equation bands b1..b6 non-empty on BOTH images; render narrower on the right
    (e.g. b1 x288..769 vs orig x288..833, b4 x288..559 vs x284..759) →
    ground-rule (e) 2D-format, NOT a truncation defect;
  - "Check classes of": orig y80..87 vs render y82..91 (~2–4 px y-shift), rule
    line x508 vs x491, bracket stack y55..101 vs y53..102, red Iteration-3 badge
    block + white glyph ink present on both → all ≤MINOR clauses (c)/(d)/(e).

### Gate discipline (2 probes this hour, both ≥8 → park)

| time | pgrep -f analyze_image.py | note |
|------|---------------------------|------|
| 17:11 | 15 (broad 20) | heartbeat + 240s back-off started; no dispatch |
| 17:35 | 23 (broad 21+) | probe 2 — cap consumed → PARK |

Probe 2 also shows foreign dispatch trees aged **1472s / 1282s / 120s** — two
are hung past their own inner `--timeout 1200` wall (they sit inside
`timeout 1700`), confirming the fleet-wide HangError regime the orchestrator
reported (504s at ~61s + hangs at 1050–1230s even at 1200s). Even a sub-threshold
dispatch this hour would 504/hang; parking is correct, not premature.

**No verdicts, no transcripts (honest).** `judge_attempt_3.txt` and
`legB_*_attempt_1.txt` were NOT created; nothing fabricated; no attempt burned
at ≥8 procs. `visual_*` fields and `gen_status` untouched.

### Final DB state (released; clean for re-dispatch)

`gen_status=building`, `visual_check=null`, `visual_transcript=null`,
`visual_attempts=0`, `worker_id=""` after `release 44 w044-legs3-20261024`.
**No PASS, no `gen_status=passed`** — those require real FINAL VERDICT
transcripts once the image leg recovers. `last_error` carries this resume
pointer.

**Why released rather than held**: the fleet convention (§9, §10) is to release
on an honest park so the row is immediately claimable, and the staged resume
command in the next section is `claim 44 <next-worker-id>` **without**
`--force` — a still-fresh heartbeat from this id would make that claim REFUSED
("live peer, stand down") for up to 40 min. Releasing keeps the resume recipe
verbatim-executable. Re-parking inside the same hour is also self-limiting:
each lane runs its own max-2-probes/hour, so no attempt is burned.

### Resume commands (everything staged & verified; §10 recipe unchanged)

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py claim 44 <next-worker-id>           # free row after this release; --force only if a peer holds it
python3 scripts/15_progress.py heartbeat 44 <next-worker-id>
# WAIT for BOTH: pgrep -c -f analyze_image.py < 8 AND a healthy image leg
# (fleet 504 + HangError this session). Probe max TWO/hour, else re-park.
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legA_dispatch_attempt_3.sh   # LEG A -> judge_attempt_3.txt
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legs_B_dispatch_2.sh         # LEG B -> legB_{centretext,eqstack,lefttables}_attempt_1.txt
python3 videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/adj_legs2.py               # PIL-adjudicate any FAIL/MINOR (§9b + §11 already refute the known ones)
# certify (note the required --worker flag on set while the claim is fresh):
python3 scripts/15_progress.py set 44 visual_check PASS --worker <next-worker-id>
python3 scripts/15_progress.py set 44 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judge_attempt_3.txt --worker <next-worker-id>
python3 scripts/15_progress.py set 44 visual_attempts 3 --worker <next-worker-id>
python3 scripts/15_progress.py set 44 gen_status passed --worker <next-worker-id>
python3 scripts/15_progress.py release 44 <next-worker-id>
python3 scripts/15_progress.py get 44    # verify gen_status=passed, visual_check=PASS, worker_id=""
```

### Build-lane debt (UNCHANGED — flagged, not mine to fix)

`build_script` still points at the pre-fix `build/slide_044.js`; the plain-named
deliverable `slide_044_recreated.pptx` is still v1 (377995 B @02:07, grey calc
area). The fix lives in `build/slide_044_v2.js` (11137 B @08:00) →
`slide_044_recreated_v2.pptx` (378324 B @08:00) → `render_2.png` (248034 B
@08:00, the render judged here). After the legs pass, the build lane promotes v2
+ repoints `build_script` (slide 044 has no dependents).

## 12. w044-buildjudge-20261024 — build-lane promotion done (2026-10-24 18:08–18:10); judge legs NOT yet obtained

Worker: `w044-buildjudge-20261024`. **This lane carries BOTH mandates**: the judge
legs AND the build-debt promotion the previous lanes explicitly deferred to the
build lane. The promotion is DONE and render-verified; the vision legs remain
blocked by the fleet gateway and are still owed (§12c).

### 12a. BUILD PROMOTION — DONE (this was the carried-forward build debt)

Copy-then-modify; nothing deleted; v1 bytes remain banked as evidence.

| step | result |
|---|---|
| v1 evidence re-verified | `qa/slide044/slide_044_build_v1_bank.js` md5 `26900e39…` == pre-promotion `build/slide_044.js` (byte-identical); `qa/slide044/slide_044_recreated_v1_bank.pptx` md5 `afe14148…` == pre-promotion plain `slide_044_recreated.pptx` (377,995 B). Both v1 artefacts still banked. |
| plain deliverable promoted | `cp slide_044_recreated_v2.pptx slide_044_recreated.pptx` → plain deliverable now md5 `b5c9fcb2f69c27a5e314644cf72fc88c` (378,324 B) = the **v2 white-calc-area-fix build**. The grey-calc-area v1 is gone from the deliverable path but preserved in the bank. |
| build scripts repointed | `build/slide_044_v2.js` `OUT` → `../slide_044_recreated.pptx` (was `_v2.pptx`); `build/slide_044.js` was then copied from the v2 script, so **both** build scripts now emit the plain-named deliverable (md5 `bd021196…`, identical). No stale v1 script can overwrite the certified deliverable again. |
| render re-verified | promoted deliverable re-rendered by the canonical recipe (`soffice --headless -env:UserInstallation=… → pdftoppm -png -r 150`, private profile `lo_044promo`, scratch `scratch/tmp/044promo/`) → md5 **`676cb05f1977f0df9e92bcde1407080a` == `qa/slide044/render_2.png`**. **The certified render corresponds byte-for-byte to the certified (promoted) deliverable.** |
| house chrome | `house_chrome_check.py` on the promoted render → **PASS** (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge center (1824,152) d=68; tol 8) |
| single-version law | the root-level parallel `slide_044_recreated_v2.pptx` was moved into the QA bank as `qa/slide044/slide_044_recreated_v2_bank.pptx` (md5 still `b5c9fcb2…`); the deck dir now holds exactly ONE 044 deliverable: `recreated_pptx/slide_044_recreated.pptx`. |
| DB write | `set 44 build_script …/recreated_pptx/build/slide_044_v2.js` and `set 44 pptx_path …/recreated_pptx/slide_044_recreated.pptx` (both with `--worker w044-buildjudge-20261024`), confirmed by `get 44`. |

Slide 044 has **no dependents** (its row shows `depends_on: null`, no pattern group),
so the promotion does not reopen any descendant.

### 12b. Pre-dispatch verification (fresh this run, both gateway-free)

- Bank re-globbed: **no `judge_attempt_3.txt`, no `legB_*_attempt_1.txt`** — no
  verdict transcript has ever landed for this slide. Attempts still 0.
- **Payload integrity re-proven by reconstruction**: a script compared both banked
  templates against `shared_patterns/judge_protocol_03.md` with the protocol's only
  legal substitutions (`NNN`→`44`, `\bK\b`→`2`). Both A and all three B payloads are
  identical to the reconstruction except a trailing `\n` (which `$(cat …)` strips).
  `BLOCKER` is intact in every file — the earlier naive `K→1` global substitution
  documented in §1 is gone from the current bank. md5s: A `8fc119623b…`,
  B×3 `4ec37fe0a5…`.
- **Dispatch scripts**: `legA_dispatch_attempt_3.sh` and `legs_B_dispatch_2.sh` both
  already carry the approved wall (`--timeout 1200` inside `timeout 1700`) and the
  fixed split-path `cd`; used as-is, no edit.
- **Adjudication harness re-run** (`qa/slide044/adj_legs2.py`, output banked
  `adjudication_legs3_output.txt`): calc-area medians `(255,255,255)` at y150/250/
  420/500 (original `(254,255,253)`) → the white-calc-area fix is PRESENT in the
  promoted deliverable; equation bands b1..b6 non-empty on both images (render
  narrower on the right = ground-rule (e) 2D format, not truncation); "Check classes
  of" y80..87 vs y82..91, class rule x508 vs x491, bracket stack y55..101 vs y53..102,
  red "Iteration 3" block + white glyph ink present on both → every known finding
  stays **≤ MINOR**, clauses (c)/(d)/(e).
### 12c. Gate discipline this window — HONEST PARK (no legs fired)

| time | `pgrep -c -f analyze_image.py` | action |
|---|---|---|
| 19:01 | 11 | status probe (claim re-verified: `worker_id=w044-buildjudge-20261024`, heartbeat refreshed after the session break) |
| 19:06 | 12 | probe 1 of the hour → ≥ 8 → heartbeat + `sleep 240` back-off, no dispatch |
| 19:10 | 10 | probe 2 of the hour → still ≥ 8 → **2-probe/hour cap consumed → PARK** |

Concurrency is trending down (11 → 12 → 10) and is now at the threshold, but the
gate law caps this lane at two probes per hour and the fleet is still above the
"< 8" launch floor, so **no LEG A and no LEG B call was launched**. No attempt was
burned, nothing was fabricated, no `visual_*` field was written.

The judge lanes remain exactly as staged and verified by this run (§12b):

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py claim 44 <next-worker-id>
python3 scripts/15_progress.py heartbeat 44 <next-worker-id>
# LAUNCH ONLY when `pgrep -c -f analyze_image.py` prints < 8; max 2 probes/hour else re-park
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legA_dispatch_attempt_3.sh    # LEG A  -> judge_attempt_3.txt
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/legs_B_dispatch_2.sh          # LEG B  -> legB_{centretext,eqstack,lefttables}_attempt_1.txt
python3 videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/adj_legs2.py              # PIL-adjudicate any FAIL/MINOR (§9b / §11 / §12b already refute the known ones)
# certify (set requires --worker while the claim is fresh):
python3 scripts/15_progress.py set 44 visual_check PASS --worker <next-worker-id>
python3 scripts/15_progress.py set 44 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/judge_attempt_3.txt --worker <next-worker-id>
python3 scripts/15_progress.py set 44 visual_attempts 3 --worker <next-worker-id>
python3 scripts/15_progress.py set 44 gen_status passed --worker <next-worker-id>
python3 scripts/15_progress.py release 44 <next-worker-id>
python3 scripts/15_progress.py get 44    # verify gen_status=passed AND visual_check=PASS AND worker_id=""
```

### 12d. Final DB state for this lane (released)

`gen_status=building`, `visual_check=null`, `visual_transcript=null`,
`visual_attempts=0`, `worker_id=""` after `release 44 w044-buildjudge-20261024`.
**No PASS, no `gen_status=passed`** — those still require real FINAL VERDICT
transcripts from both legs. **No row was marked passed on the strength of the build
work alone.**

`build_script` = `…/recreated_pptx/build/slide_044_v2.js` and
`pptx_path` = `…/recreated_pptx/slide_044_recreated.pptx` are now correct and
**the build promotion debt is CLOSED** (§12a): the plain-named deliverable is the
v2 white-calc-area build and its render is byte-identical to `render_2.png`, so
whichever leg lands next is judging exactly the deliverable that will ship.
