# Slide 049 — vision-judge worker report (worker-fresh-049f)

Status: **BLOCKED — NOT CERTIFIED** (formal verdicts unobtainable: gateway/model
stalls on the mandated heavy invocations). No FINAL VERDICT was produced on any
leg; nothing was fabricated. `visual_check` was NOT written; row left honest.

## 1. Claim + banked state verified
- Claimed 49 via `claim 49 worker-fresh-049f --force` (took over from
  `worker-fresh-049d`, heartbeat 62m stale). Heartbeats maintained.
- Project root used: `videos/machine-learning/03_ridger_regression_gradient_descent`
  (deck). Repo-level tooling (`scripts/15_progress.py`, `scripts/16_vision_gate.sh`,
  `.agents/skills/image-analysis/scripts/analyze_image.py`) lives at the repo root.
  NOTE: the real analyzer is `…/image-analysis/**scripts**/analyze_image.py`
  (the `analyze_image/analyze_image.py` path in some briefs does not exist).
- Banked starting files all present under `recreated_pptx/qa/slide049/`:
  `render_6.png` (2001×1125), `judge_prompt_6.txt` (Template A payload),
  `crop_6_calc_table_{render,orig}.png` (1207×806, matched scale),
  `crop_6_callout_{render,orig}.png` (300×270, matched scale),
  `crop_prompt_6_{calc_table,callout}.txt`, `capture_6_*.txt`, `build_attempt_6.js`.
  Build `recreated_pptx/slide_049_recreated.pptx`; original `unique_slides/slide_049.jpg`.

## 2. Render integrity (verified, no rebuild needed)
- Re-rendered the current pptx (`soffice --headless` → pdf → `pdftoppm -png -r 150`)
  to `render_verify_049f.png`: **pixel-IDENTICAL to render_6.png** (0 differing px).
- House-chrome check on render_6: `HOUSE CHROME CHECK: PASS` (panel x54..903 y45..540,
  C00000 strokes L/R/bottom present + top correctly bare, badge center (876,73) d~35).

## 3. Vision legs — outcome
| Leg | Invocation (law-fixed) | Result |
|-----|------------------------|--------|
| A  full-slide (Template A, 4KB payload, 2001×1125 render + 960×540 orig) | `comparison … -p judge_prompt_6.txt --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1` | **STALL**: `attempt 1/2: ABORT HangError 630s` (run 1 all 3 attempts, outer killed rc=124 0B at 07:44:12); relaunch attempt 1 also ABORT 630s. No body. |
| B2 callout crop (Template B payload on 300×270 pair) | same factors | **STALL**: `attempt 1: ABORT HangError 630s`. No body (retry killed early). |
| B1 calc_table crop (1207×806 pair) | same factors | **NOT RUN** — deferred behind callout; would stall identically (below). |

Logs: `legA_dispatch.log`, `legB_callout_dispatch.log`, `judge_status_049f.txt`,
`worker_report_progress.log`, `run_judge_049f.sh`, `run_leg_049f.sh`.

## 4. Root cause (evidenced, not speculation)
- The gateway + `--thinking high` are HEALTHY. Two control probes on the SAME images,
  with SHORT prompts and the analyzer's DEFAULT token budget, returned coherent bodies
  on `round 1 attempt 1` in **81s** (analysis, `probe_6_049f.txt`, 331B) and **10s**
  (comparison, `probe_cmp_049f.txt`, 133B: *"YES. Both crops display the same red
  'Iteration 2' header and identical 'No change in W / Stop Iterations' text."*).
- The mandated blades — byte-for-byte GROUND-RULES payload + `--max-tokens 65536`
  (+ `--timeout 600`) — deterministically stall the model's thinking stream past the
  analyzer's internal 630s per-attempt abort. This is **independent of image size**
  (callout stalled on a 300×270 crop; full-slide stalled on the big frame) and of
  transient congestion (probes passed in the same window). Total observed stalls:
  full-slide ×4 attempts, callout ×1 attempt — every one at exactly 630s.
- Gate congestion was NOT the blocker for the legs themselves: the callout dispatcher
  waited for a slot (fleet load observed 13→10→7) and, once admitted at 08:20:27,
  still stalled at 630s.

## 5. Adjudication status
- No judge findings exist to adjudicate (no verdicts). PIL pass was pre-staged:
  render==pptx identical, chrome PIL PASS, render→frame transform measured
  (x=2.0844, y=2.0833); crop-region origins recovered (callout ≈(754,344),
  calc_table ≈(245,108)) for reactive mapping.
- Probe content corroborates the original's substance (Iteration 2, d(x)=[x,d], C1/C2,
  "Keep same Weight", W=(5,−1,−1), "No change in W / Stop") — no evidence of a
  content defect, but this is NOT a substitute for the two required verdicts.

## 6. DB state (honest, not certified)
- `visual_check` = null (NOT written), `visual_transcript` = null,
  `gen_status` = building, `last_error` set to the block summary.
- Claim released at end of run so a future worker can reclaim when fixed.

## 7. EXACT next commands (for a future worker when the 65536 stall is resolved)
From the deck root; `QA=…/recreated_pptx/qa/slide049`, `PROJ=<repo root>`:
```
# claim
(cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
   python3 scripts/15_progress.py claim 49 worker-fresh-049g --force)
# three legs (unchanged law-fixed invocations), gated + heartbeated:
bash "$QA/run_judge_049f.sh"        # Template A + both crop pairs, sequential
# (or per-leg: bash "$QA/run_leg_049f.sh" <tag> <out> <img1> <img2> <payload> <view> <capture>)
# If any leg returns a real FINAL VERDICT, PIL-adjudicate -> fix build (copy-then-modify)
# -> so re-render -> re-run BOTH legs. Only on clean/Adjudicated legs:
(cd "$PROJ" && VIDEO=… python3 scripts/15_progress.py record-visual 49 PASS "$QA/judge_attempt_6.txt")
(cd "$PROJ" && VIDEO=… python3 scripts/15_progress.py set 49 gen_status passed)
(cd "$PROJ" && VIDEO=… python3 scripts/15_progress.py release 49 worker-fresh-049g)
```
Re-render if the pptx changes (recipe in §2). Law rationale to flag upward: the
founder-frozen `--max-tokens 65536` + verbatim GROUND-RULES payload cause a
deterministic 630s client-side abort on the current vision model; if the model cannot
be prompted to finish under those constraints, this needs a founder decision
(either a gateway/model fix, or a sanctioned reduction of max-tokens) — NOT a local
workaround, which the byte-for-byte/token law forbids.

## 2026-10-26 fresh-carrier addendum (S7a, att14)

- att14 legA PASS (3 MINORs adjudicated in pil_adjudication_att14.md: Initial-W "="
  + REPEAT underline settled-refuted; Z-subscript order unscoreable — orig marks 1px).
- 5/5 crop legs clean-or-adjudicated: top_band 3 MAJORs all settled Initial-W
  refutations / unscoreable delimiter (render objectively paren asset, unchanged
  since a12); aug_box, legend, calc_rows, iter_stop PASS.
- Fix cycle applied: top-table digit row2 (1,1,2,4,5,6) restored y97 h10; class tags
  moved to y113 h12; legend + aug tags switched subscript:true → plain unicode ₁₂
  (certified 044/045/047 idiom). render_13 chrome-PASS.
- **CERTIFIED**: DB slide 49 gen_status=passed, visual_check=PASS, attempts=14,
  transcript judge_attempt_14.txt; stale 2026-10-24 last_error cleared; pool cert event.
- 048 att8 dispositions + fix recipe banked at qa/slide048/HANDOFF.md (parked at
  wall); pool parked event.
