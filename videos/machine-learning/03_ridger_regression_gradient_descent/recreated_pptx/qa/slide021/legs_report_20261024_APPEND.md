
---

# LEGS-ONLY lane — slide 021 attempt-10 judge legs (2026-10-24, 16:20 UTC)

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`
Worker lane: `w021-legs-20261024` (claimed 12:36 UTC, `--force` auto-takeover over the
parked `w021-buildfirst-20261024` claim whose heartbeat was 141 min stale).
Scope: LEGS-ONLY — land the two judge legs and certify. The build lane owns the deliverable;
this lane never edited `build/slide_021.js` or `slide_021_recreated.pptx`.

## Banked state verified at lane start (md5, all current)

| item | md5 | status |
|---|---|---|
| `recreated_pptx/slide_021_recreated.pptx` | `6ea9e28cce3f9c47e6cf6abd42365147` (content) | current |
| `recreated_pptx/build/slide_021.js` | `56e8f2db37e3500b32013f9446b47b47` | current |
| `recreated_pptx/qa/slide021/render_10.png` | `a17310a3cac93cf23e3c8daed2bd0cea` | current (2001x1125 @150dpi) |
| `qa/slide021/judge_prompt_10.txt` | `d072bded39c074be91988270e02fda97` | current |
| `qa/slide021/crop_prompt_template_10.txt` | `b5b152e31e2ca54989eff597374025fb` | current (1925 B / 1915 chars, `NNN`->021 substituted) |

The pptx's whole-archive md5 reads `74364813557716b5a83e0fde790d510f` because rebuilding
refreshes `docProps/core.xml` timestamps; the content md5 above is authoritative and
unchanged (per the build lane's part-by-part verification).

## Judge lanes — what landed

### LEG A (Template A full-slide): PASS
`recreated_pptx/qa/slide021/judge_attempt_10.txt` (2662 B, written 11:13:00Z)

- Dispatched 10:58:41Z with the gate **genuinely open** (`pgrep` = 3), through
  `dispatch_leg1_fullslide.sh` with the frozen `--timeout 600`. The analyzer's internal
  630 s `HangError` fired once and its own retry (attempt 2) then produced the verdict —
  so this leg completed *inside* the 600 s wall on the retry, in 859 s total.
- `FINAL VERDICT: PASS` — "All text is verbatim, every numeric value in all three
  matrices matches, element ordering and colors are correct, layout regions match,
  nothing is missing, no overflow. Only minor stylistic differences (arrow weight, rule
  weight, minor column proportion) remain."
- Four MINOR findings, all adjudicated PIL-first (below). No BLOCKER, no MAJOR.

### LEG B (Procedure B crop pairs): 1 of 5 landed
| crop | transcript | outcome |
|---|---|---|
| `top_table_eq` | `crop_10_top_table_eq_judge.txt` (11:33:21Z) | **FINAL VERDICT: PASS** |
| `top_chain` | `crop_10_top_chain_judge.txt` | no verdict |
| `mid_table_eq` | `crop_10_mid_table_eq_judge.txt` | no verdict |
| `mid_chain` | `crop_10_mid_chain_judge.txt` | no verdict |
| `bot_eq_table` | `crop_10_bot_eq_table_judge.txt` | no verdict |

All ten `crop_10_*` PNG pairs are cut and banked at matched effective scale 2.0833, with
both crops proven identical in pixel dimensions on BOTH axes (verified this lane with PIL:
top_table_eq 490x223, top_chain 981x77, mid_table_eq 506x236, mid_chain 1168x73,
bot_eq_table 1032x145 — render and orig equal in every case).

## Three distinct vision-gate failure modes observed this lane

This lane encountered three *different* blockers. Only the third is an upstream-provider
fault; the first two were known from the build lane's hand-off and remain relevant to the
founder's open wall decision.

1. **Gate congestion** — `pgrep -c -f analyze_image.py` mostly 11..50 for the entire
   session, with brief drops to 2..5 (windows at 10:58 and 14:47..14:59 UTC).
2. **630 s analyzer `HangError` + 1700 s outer-wall kill** — the earlier leg-1 wall abort
   banked as `wall_abort_evidence_10.txt`, and the leg-1 dispatch that eventually PASSed hit
   the 630 s `HangError` once before its own retry succeeded. An attempt on the
   superseded `--timeout 600` wall was stopped by this lane (PID 593359, 1416 s in, no
   transcript) rather than let it burn to the 1700 s kill.
3. **HTTP 504 `upstream_timeout` (Nvidia)** — a *fast* failure (~61 s), NOT a wall. During
   the genuinely open 14:47..14:59 window all four remaining crops were dispatched (queue
   2..5) and each returned `HTTP 504 {"code":"upstream_timeout","ironrouter":
   {"candidate":"nva…hWGS","provider":"Nvidia"}}` with `0/1 result(s) analyzed
   successfully`. A direct gateway probe at 15:47 returned **HTTP 200 in 12.4 s**, so the
   outage was transient and the upstream has since recovered. Fleet-wide: no peer lane in
   this deck has landed a judge transcript since 14:00 UTC.

## Timeout-resume history (this lane)

| when | event |
|---|---|
| 10:33 | gate poll started (supervisor `run_legs_10.sh`) |
| 10:58 | window (pgrep=3) — LEG A dispatched |
| 11:13 | LEG A verdict PASS banked |
| 11:13 | LEG B dispatched: crop 1 landed PASS 11:33; then the gate read 25 and the remaining four parked |
| 12:36 | this lane claims row 21 (`--force`) |
| 12:37 | stopped the superseded-`--timeout`-600 crop attempt (no verdict) |
| 12:47 | re-dispatched the four with the orchestrator's `--timeout 1200` override |
| 14:47..14:59 | windows open (pgrep 2..5) — all four dispatched, all HTTP 504 |
| 15:15 | re-launched; no window; dispatcher process died 15:51 (before its cap) |
| 15:47 | gateway probe HTTP 200 — upstream recovered |
| 16:19 | 161 s wait, pgrep=14 — no window |

## Adjudications (PIL-first, measured against BOTH images; 960x540, 1px = 1pt)

`adjudicate_crops_1200.py` + `adjudicate_leg1_10.py` — measurements banked under
`qa/slide021/` and `scratch/tmp/021_crop_adjudication_baseline.txt`.

**LEG A's four MINORs — all admissible, none a build trigger:**

1. *Arrow weight* — PIL on the blue class puts render_10's arrows within **0.6 px** of the
   original in x and **3.2 px** in y on all five arrows (P1 arrow1 x460..476 y196..207 vs
   x460..476 y198..204; P2 arrow1/arrow2, P3 arrow likewise). The closed-loop bank
   (`render_10_closedloop.txt`) marks every arrow `OK` at the 6 px position / 10 px width
   tolerance. The visual "boldness" impression is a typed-vector vs handwritten-medium
   difference — capped at MINOR by the ground rules; no pixel evidence of a wrong arrow.
2. *Matrix grid styling* — P1/P2/P3 table ink boxes: ORIG (97..303, 173..227), (89..295,
   340..395), (421..626, 457..511) vs REND (97..303, 173..221), (89..294, 341..393),
   (421..625, 458..506) — dx 0..0, dy 5.7..1.9, all `OK`. Gridline structure and all 27
   cell values match; the original's heavier look is JPEG softening.
3. *Column proportions in the top-left matrix* — nine values verbatim per the judge, and
   the closed-loop table row-measurements are inside tolerance. No cell value or column
   count differs; not a defect.
4. *Cell padding* — the row-pitch defect was a REAL defect and was **already fixed** by
   the build lane (now within 0.8 px on all three tables: P1 172.7/189.5/207.3 vs
   173/190/208; P2 340.6/358.4/375.2 vs 341/359/376; P3 457.2/474.5/491.3 vs 458/475/492;
   all 27 digit rows within 1.4 px). Residual impression only.

**Crop-region baseline for the four outstanding crops** (`adjudicate_crops_1200.py`,
frame px, render_10 vs original): chain1 dark (341,794,189,212) vs (341.1,794.0,187.3,213.7);
chain1 red (348,794,189,206) vs (345.0,794.0,187.3,207.9); chain1 blue (461,676,196,206) vs
(459.6,676.0,197.8,203.6); regmat+table (90,294,301,395) vs (88.6,294.5,300.1,389.3);
lambda3 green (247,287,305,320) vs (245.0,288.2,304.0,317.4); the three FDFD96 highlight
bands all within 1 px on both axes and (253,253,150) is the dominant render colour with
**0** saturated-FFFF00 pixels; chain2 (338,888,348,381) vs (338.2,888.5,348.0,381.6);
bottom dark (155,625,458,510) vs (155.2,625.4,457.2,504.7); P3 inverse table
(422,625,458,510) vs (421.0,624.9,457.4,504.9). Frame containment is clean on P1/P2/P3
(0 ink px outside the blue strokes in BOTH images). Every region is within the closed-loop
tolerance, so no outstanding crop has any PIL-supported defect.

**Refuted (do not re-fix):** the attempt-3 judge's claim 7 ("a strike/slash marker on the
15 cell") — the original's P1 "15" is a plain digit at x263..275 y177..187 (n=49); no extra
mark exists in either image, and leg A of attempt 10 independently classified it as a
capture artifact. Claims 1/2/3/4/6 were refuted by the build lane with measurements. The
missing TOP stroke is house chrome by design and is never a discrepancy. `judge_attempt_3.txt`
itself is a FAIL on the **superseded** attempt-3 build (it flagged the singular-matrix
`det=5685` state) and is historical only — the attempt-10 build fixed the row-pitch,
highlight and stale-asset defects (three real defects, see the build lane's section above).

## DB state at hand-off

```
```

**NOT CERTIFIED.** `visual_check` is deliberately NOT written: `visual_check=PASS` requires
BOTH judge legs clean, and 4 of the 5 Procedure B crops have no verdict. The full-slide leg
(DENOMINATOR leg A) is clean, and every outstanding region is PIL-verified inside the
closed-loop standard, but the crop certificates are a founder-mandated second leg and cannot
be waived or inferred from PIL alone. Banked scripts, transcripts and this report give the
next lane an exact resume.

## Exact resume commands

```bash
cd /worksp""aces/codespaces-blank/ai_llm_slides
V=videos/machine-learning/03_ridger_regression_gradient_descent
QA=$V/recreated_pptx/qa/slide021

VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py get 21

# probe the gate; <8 is required before every vision call, and the upstream must be
# answering (a fast ~61s HTTP 504 upstream_timeout means it is still down):
pgrep -c -f analyze_image.py

# dispatch ONE crop at a time (waits up to 3000s for a window, then dispatches with the
# orchestrator's --timeout 1200 override inside the frozen outer timeout 1700):
bash $QA/dispatch_one_crop_10.sh top_chain    "the first block's determinant chain: |X^T X| = 0, two blue arrows, Singular Matrix, red italic No Inverse" 3000
bash $QA/dispatch_one_crop_10.sh mid_table_eq "the second block's left side: the (X^T X + lambda I) label, green lambda=3, the full 3x3 regularized matrix, and the three FDFD96 highlight bands on the 17/43/95 diagonal" 3000
bash $QA/dispatch_one_crop_10.sh mid_chain    "the second block's determinant chain: |X^T X| = 5685, two blue arrows, Non-Singular Matrix, red italic Inverse Exists" 3000
bash $QA/dispatch_one_crop_10.sh bot_eq_table "the bottom block: the (X^T X + lambda I)^-1 expression, the long blue arrow, and the 3x3 inverse matrix table of decimals" 3000

# once all five crop transcripts carry a FINAL VERDICT line, adjudicate any FAIL PIL-first
# (qa/slide021/adjudicate_crops_1200.py, adjudicate_leg1_10.py) and then certify:
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py set 21 visual_check PASS --worker <your-id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py set 21 visual_transcript $QA/judge_attempt_10.txt --worker <your-id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py set 21 visual_attempts 10 --worker <your-id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py set 21 gen_status passed --worker <your-id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py release 21 <your-id>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py get 21   # must read gen_status=passed, visual_check=PASS, worker_id=""
```

Payloads are byte-verified and must not be re-typed: `qa/slide021/judge_prompt_10.txt`
(`d072bded…`) and `qa/slide021/crop_prompt_template_10.txt` (`b5b152e3…`).

## Banked artifacts added by this lane

`run_legs_10.sh`, `run_remaining_crops_10.sh`, `run_crops4_1200.sh`,
`dispatch_one_crop_10.sh` (dispatchers; per-crop gate check + honest park),
`adjudicate_crops_1200.py` (crop-region PIL measurements in frame px on both images),
`legs_status_crops_remaining_20261024.md` (full gate-poll + 504 evidence log),
`judge_attempt_10.txt` (LEG A PASS), `crop_10_top_table_eq_judge.txt` (crop 1 PASS),
`scratch/tmp/021_crop_adjudication_baseline.txt`, `scratch/tmp/crops4_pid*.txt`.
