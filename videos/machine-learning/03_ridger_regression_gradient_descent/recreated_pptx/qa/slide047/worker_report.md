# worker_report — slide 047 "Check Classes of Z Vectors" (deck 03) — fresh BUILD+JUDGE pass

Worker: w047-root-20261024 · started 2026-10-24 07:02 UTC · deck: `videos/machine-learning/03_ridger_regression_gradient_descent/`
Attempt: **6**. Status: **CERTIFIED** — `gen_status=passed`, `visual_check=PASS`,
`visual_attempts=6`, `visual_transcript=.../qa/slide047/judge_attempt_6.txt`, `last_error=""`,
claim released (`worker_id=""`). All six judge legs (full-slide + 5 crops) returned genuine
`FINAL VERDICT: PASS` bodies; nothing was fabricated.

## Lane history / inputs treated as leads (not conclusions)

- Claimed with `--force` over stale `w047` (heartbeat >40 min).
- Prior banked FAILs read as inputs: `judge_attempt_1.txt` (FAIL, render_1),
  `judge_attempt_2.txt` (FAIL, render_2), `crop_3_augmatrix_judge.txt` (FAIL, render_3).
  Prior lane's PASS bank: `judge_attempt_5.txt` + 5 crop PASSes (render_9).
- Prior lanes also suffered path-rewrite failures (artifacts spilled into the repo-root
  `scratch/tmp/`). All of this pass's paths are deck-namespaced, split-path form.

## §1 PIL adjudication of every claimed defect (before any build decision)

Full record: `adjudication_record_w047.md` (+ scripts `adjudicate_w047*.py`, outputs
`adjudicate_w047*.txt`, 4 parts). Rulings (frame is authority, 960×540, 1px=1pt):

| prior claim | PIL ruling |
|---|---|
| augmented table duplicated rows | CONFIRMED original has 3 data rows (data block h48 px = 3×15.5 px rows; top-left calibration h31 = 2 rows); parens span the 3-row block |
| class rows C₁C₁C₂C₂C₂C₂ | REFUTED — original prints C₁C₁C₁ (red) C₂C₂C₂ (blue) in BOTH matrices (per-cluster core sampling) |
| "Ugmented" = clipped A | REFUTED — the source itself prints the typo "Ugmented" (1:1 ASCII: first glyph U, nothing to its left) |
| "C₂negative" missing space | REFUTED — original gap C₂→"negative" is 2 px (kerning) vs 6–8 px for real word gaps |
| sign statements red/blue | REFUTED — core (128,130,127) = BLACK bold |
| calc boxes "light blue tint" | REFUTED — interiors median (254,255,253) = white; hairline (210,215,221) |
| uppercase X headers | REFUTED — lowercase italic x₁..x₆ |
| square brackets in calc vectors | REFUTED — round parens spanning the stack (both x381 and x405, y150..189) |
| result boxes narrower | REFUTED — original boxes x273..855, identical |
| W = [4; -2] | CONFIRMED three entries 4 / -2 / -2 (digit column y62..71 / 77..87 / 93..102) |
| Z headers Z₂/Z₃ | CONFIRMED Z₁ Z₁ Z₁ (1:1 ASCII, three identical glyphs) |
| all d(Z₁) | CONFIRMED d(Z₁) / d(Z₂) / d(Z₂) (4× bitmaps: box2/box3 subscripts end in a bottom bar) |
| garbled bracket notation | CONFIRMED blue row vector × green (14;-4;0) stack × black result |
| box3 "= -2" | CONFIRMED minus bar at y263 x424..431 — verbatim source arithmetic slip |
| legend colours | CONFIRMED C₁ red (151,29,37), C₂ blue (47,33,132), Zero green (70,134,57) |
| top band white | CONFIRMED cream #FFFFE8 + dark-blue hairline |

Conclusion: no content-level defect survived re-verification; the existing build
(`build/slide_047.js`, md5 856e4002eaef3492e3d00c19d3308b94) already carried the
frame-corrected values and they are re-confirmed here. No build change was needed.

## §2 Build + render

- Fresh render: `render_attempt6.sh` → `render_10.png` (soffice → 150 dpi PDF → pdftoppm,
  2001×1125). **Pixel-identical to the banked certified render_9** (0 of 2,251,125 px differ).
- House chrome: `house_chrome_check_render_10.txt` → **HOUSE CHROME CHECK: PASS**.
- PIL selfcheck: `selfcheck_attempt_6.txt` → **ALL CHECKS PASS** (containment, equation ink,
  18 matrix columns + 3 stack delimiters, table data vs measured frame values, calc-run
  sequence, zero ink in all 6 gap bands, single-paragraph text boxes).
- Region-level ink-bbox comparison vs the original (`region_compare_attempt6.py/.txt`):
  every element within 4 frame-px except aug-title width +4.7px (font substitution) and
  sign-statement starts box2/box3 −10.4/−3.4px (the ORIGINAL's own inconsistent placement:
  measured 508/518/511 with widths 79–88px; box1 matches to 0.4px; all contained, no collision).

## §3 Judge legs (attempt 6) — all PASS

| leg | transcript | verdict |
|---|---|---|
| full-slide (Template A) | `judge_attempt_6.txt` (2873 B) | FINAL VERDICT: PASS |
| crop topband | `crop_6_topband_judge.txt` (1502 B) | FINAL VERDICT: **PASS** |
| crop augmatrix | `crop_6_augmatrix_judge.txt` (1418 B) | FINAL VERDICT: PASS |
| crop calceq | `crop_6_calceq_judge.txt` (1481 B) | FINAL VERDICT: PASS |
| crop calcright | `crop_6_calcright_judge.txt` (1686 B) | FINAL VERDICT: PASS |
| crop button | `crop_6_button_judge.txt` (1481 B) | FINAL VERDICT: PASS |

Payloads were extracted programmatically from `shared_patterns/judge_protocol_03.md`
(NNN=047 substituted) and verified byte-identical to the banked prior-lane prompts modulo
attempt number. Crop pairs are matched effective scale (render sx=2.08438 sy=2.08333,
original LANCZOS-upscaled to the same; audit `crop_6_scale_audit.txt`). The full-slide
judge independently re-confirmed every adjudicated value (C₁C₁C₁/C₂C₂C₂ rows, W=[4;-2;-2],
Z₁Z₁Z₁, d(Z₁)/d(Z₂)/d(Z₂), legend, "Ugmented" title) — the fresh judge agrees with the
PIL record on all points.

## §4 Certification

`visual_check=PASS`, `visual_attempts=6`, `visual_transcript=.../qa/slide047/judge_attempt_6.txt`,
`gen_status=passed`, `last_error=""`, claim released. Verified with `get 47`:
`gen_status=passed`, `visual_check=PASS`, `worker_id=""`.

## Artifacts (all under `recreated_pptx/qa/slide047/`)

| artifact | md5 |
|---|---|
| unique_slides/slide_047.jpg | 6617111d7f1c530fe9bc6c4d60981838 |
| recreated_pptx/slide_047_recreated.pptx | 7a6a73103f61839a082501cf6a0c928c (unchanged) |
| build/slide_047.js | 856e4002eaef3492e3d00c19d3308b94 (unchanged) |
| render_10.png (== prior render_9, pixel-identical) | 1e73a453ca54f0d45455780b109857af |
| judge_attempt_6.txt (+ preserved copy judge_attempt_6_leaf.txt) | 620725751eae95c4b443bdf1ed28639e |

New this pass: `adjudication_record_w047.md`, `adjudicate_w047*.py/.txt` (p1–p4),
`render_attempt6.sh`, `render_10.png`, `house_chrome_check_render_10.txt`,
`selfcheck_attempt_6.py/.txt`, `region_compare_attempt6.py/.txt`, `prep_attempt6.py`,
crop_6 pairs + prompts + scale audit, `judge_attempt6.sh` (dispatcher),
`finish_attempt6.sh` + `finisher_log.txt`, `certify_attempt6.sh` + log,
judge transcripts 1–6 above. Prior lane's report preserved as
`worker_report_w047_prior_lane.md`; nothing banked was deleted.

## Operational notes (honest)

- Gateway was saturated for ~2.5 h (fleet load 10–39 vs the gate-law threshold 8). The
  dispatcher paced with heartbeat+sleep-240 cycles; a first finisher attempt mis-sequenced a
  certification check against a just-landed transcript (logged in `finisher_log.txt`) and a
  duplicate leaf dispatch briefly raced the transcript path — the genuine PASS transcript was
  preserved to `judge_attempt_6_leaf.txt` before the redundant call was stopped. Both stray
  processes were killed; DB state is correct and no verdict was fabricated.
- The full-slide judge call needed a 1200s wall (the client's 600s hard wall aborted under
  load — the same adaptation the fleet's slide049 lane used) with the frozen payload unchanged.
- No component export needed: slide 047 has no dependents (edges are 10>9, 13>12, 17>13, 18>17).
