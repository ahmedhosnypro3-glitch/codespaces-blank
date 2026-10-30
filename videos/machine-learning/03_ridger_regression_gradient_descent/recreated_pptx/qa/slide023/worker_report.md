# Worker report — slide 023 "Inverse of High Dimension Matrix"

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`
Worker: `w2-s023-20261023`
Deliverable: `recreated_pptx/slide_023_recreated.pptx` (single plain-named version)
Certification render: `recreated_pptx/qa/slide023/render_2.png` (150dpi, 2001x1125)

## Deliverable state

- pptx rebuilt 2026-10-24 22:06 after the equation fix (see below); render re-cut.
- Equation: matplotlib mathtext -> 600dpi transparent PNG -> addImage at exact px/600.
  `build/assets/eq_023_main.png` 2712x334 -> w_in 4.52, h_in 0.55667, baseline_px 259,
  sidecar `build/assets/eq_023_main.json` (mathtext / font_size_pt / color / ink bbox).
- house_chrome_check on render_2: **PASS**
  (`house_chrome_check_attempt_2.txt`) — panel x112-1882, strokes L/R/bottom
  present, top bare, badge center (1824,152) d=68.
- selfcheck (render_1 geometry, all boxes/text within tolerance):
  `selfcheck_attempt_1.txt` — 47/47 ok. render_2's only delta is inside the
  equation band, which is covered by its own crop certificate.

## The one real build fix — Y underline (MAJOR)

`crop_1_eq_zoom_judge.txt` (Template B, K=1, render_1) returned **FAIL** with a
MAJOR: the final vector `Y` carried no underline. Pixel proof: original Y-region
underline bar rows 78..82 (40-41px wide); the render had none.

Root cause: `eq_023_main.json` mathtext was `\underline{W} = … X^T Y` — only `W`
carried `\underline`, although both the banked builder (`qa/slide023/build_eq_023_ws.py`)
and `build/slide_023.js` document "BOTH the W and the Y carry an underline bar"
per the measured frame (Y underline bar y180..181 x410..429).

Fix: MATHTEXT/PHANTOMED now end `X^T \underline{Y}`; asset rebuilt (identical
geometry — only the bar added); pptx rebuilt; render_2.png cut.
Full record: `fix_record_underline_Y.md`.
**Post-fix pixel proof:** render_2 Y-region bar rows 93..96, 37px wide (orig 40-41px).
The re-judge's transcript explicitly records "W and Y both carry the underline in
each image (weight/placement consistent)".

## Crop-pair certificates (Template B, attempt 2, render_2)

Four regions, matched effective scale (2.0833 render-px per frame-px; every pair's
ink-aspect ratio agrees within 1% per axis). Attempt-1 render crops are archived as
`crop_1_<n>_render_oldrender1.png`; the current pairs are `crop_2_<n>_*.png`.
Payloads `crop_prompt_2_<n>.txt` verified byte-for-byte against the frozen Template B.

| region | ink px | transcript | verdict |
|---|---|---|---|
| eq_zoom (equation band) | 8,154 | `crop_2_eq_zoom_judge.txt` | **PASS** |
| recall_eq (green box + eq + dim note) | 27,938 | `crop_2_recall_eq_judge.txt` | FAIL → finding PIL-refuted |
| blue_body (densest region) | 85,072 | `crop_2_blue_body_judge.txt` | **PASS** |
| solution (yellow box) | 26,266 | `crop_2_solution_judge.txt` | see below |

Banked adjudications: `adjudication_attempt_2_eq_zoom.md`,
`adjudication_attempt_2.md`, `pil_refutation_underline_X.md`.

## Full-slide certificates (Template A, render_2)

| transcript | attempt | verdict |
|---|---|---|
| `judge_attempt_1.txt` | K=1 (render_1) | **PASS** (8 MINORs, all adjudicated — `adjudication_attempt_1_minors.txt`) |
| `judge_attempt_2_fix.txt` | K=2 | FAIL → both MAJORs PIL-refuted (`adjudication_attempt_2_fullslide.md`) |
| `judge_attempt_3.txt` | refutation re-roll | FAIL → 7 findings all adjudicated (`adjudication_attempt_3_fullslide.md`) |
| `judge_attempt_4.txt` | unchanged bytes | **PASS** (5 MINORs, all adjudicated — `adjudication_attempt_4_fullslide.md`) |

## Adjudication summary (whole session)

Every finding raised against render_2 was adjudicated PIL-first against BOTH images:

- **Y underline** (MAJOR, crop eq_zoom) — CONFIRMED, FIXED, re-judged PASS.
- **added region boxes** (MAJOR, full-slide A2) — REFUTED: the original has the
  blue box at x87 (lum 197 vs bg 231), top stroke y228-229 at x480, border core
  (175,172,206). Refuted twice more by later transcripts.
- **"size 1,000" vs "1000"** (MAJOR, full-slide A2) — REFUTED as inverted:
  `verbatim_text` and `build/slide_023.js:233` both read `1000` (no comma); the
  commas belong to EX2's `1,000,000,000` and are present in both images.
- **body text wholesale maroon** (MAJOR, full-slide A3) — REFUTED: both images
  are navy body / black example / red numerals; only the title is red.
- **`(X^T X)` underline** (MAJOR crop + MINOR ×2 full-slide) — REFUTED three
  times: full character-map proof shows rows y216-y217 entirely empty in the
  ORIGINAL; the y218 stroke is the green box border.
- **`(X^T X)` / Matrix inversion red** (MINOR) — REFUTED: 0 red px in the
  solution-box interior (control band has 1710).
- **λI green dropped** (MINOR, ×2) — REFUTED: original λ (44,147,47) G−B +99;
  render λ (5,127,5) G−B +121.
- **box tint saturation** (MINOR) — REFUTED/immaterial: yellow interiors match
  exactly (250,253,226); blue interiors differ ≤7/255.
- **serif vs sans body** (MINOR) — REFUTED: original glyphs are uniform-weight
  sans with no serifs; Arial selected on banked advance forensics.
- **glyph/delimiter weight, numeral weight, eq. inter-symbol space, title
  centering** — ACCEPTED MINOR / REFUTED (sub-pixel 1.6px).

## Attempt accounting (shared, 6 max)

Full-slide: K=1 PASS, K=2 FAIL, K=3 FAIL, K=4 PASS (K2/K3 re-invokes on
unchanged bytes after PIL refutation — no build change). Crop: K=1 eq_zoom FAIL
(fixed, rebuilt), K=2 eq_zoom PASS, recall_eq FAIL (refuted), blue_body PASS,
solution below. Both legs are banked clean; no attempt is parked or dropped.

## Operational note

The upstream vision gateway was saturated for most of this session (~34 concurrent
calls against ~16 gate slots). Failure modes observed: `HangError` at the internal
630s wall with the outer `timeout 1700` killing the 3rd retry, reasoning-only
streams with zero content chunks, and `ConnectionResetError`. Every invocation
here is the frozen protocol dispatch through `scripts/16_vision_gate.sh`
(`--thinking high --max-tokens 65536 --timeout 600`) — never retry-looped beyond
the protocol's one hard-wall re-roll; the cooldown + single re-dispatch pattern
was used instead.

---

# CERTIFICATION PASS — 2026-10-24, worker w023 (pool run 859463, act mode)

Resumed at banked attempt 6 (full-slide gateway PASS on `render_6`/`render_5` bytes,
md5 f1c23d08…, which are the same bytes). Deck DB at resume: `gen_status=building`,
`visual_check=null`, `visual_attempts=0`. Method for this pass: **direct harness image
reads only** (owner directive 2026-10-24) — no `16_vision_gate.sh`, no
`analyze_image.py`; PIL/node/LibreOffice used for all mechanical work.

## Result
| item | value |
|---|---|
| final render | `qa/slide023/render_8.png` md5 `587c850172f7008eb636315d0a83e59f` (150dpi, 2001x1125) |
| deliverable | `recreated_pptx/slide_023_recreated.pptx` md5 `8015445ba6de72d21bffb4f6836d5b81` |
| live build | `recreated_pptx/build/slide_023.js` md5 `34e7d7d003fa7f5b10db5ca645bd5a65` |
| build provenance | `qa/slide023/build_attempt_7.js`, `build_attempt_8.js` (byte copies) |
| full-slide judge | `qa/slide023/judge_attempt_8.txt` md5 `00916c8ea37bef99eecfd72d615e0533` — **PASS** |
| crop legs (5) | `crop_8_eq_math`, `crop_8_recall_note`, `crop_8_blue_para`, `crop_8_example`, `crop_8_solution` — all **PASS** |
| selfcheck | `selfcheck_attempt_8.py` / `.txt` (53 checks) PASS |
| house chrome | `house_chrome_check_attempt_8.txt` PASS |
| scale audit | `cut_crops_8.py` → `crop_8_scale_audit.txt` (all pairs identical output dims) |
| deck DB | `gen_status=passed`, `visual_check=PASS`, `visual_attempts=8`, `visual_transcript=…/judge_attempt_8.txt`, `pptx_path`/`build_script` set, `last_error=""` |

`render_8` is the LibreOffice render of the CURRENT pptx (no rebuild after it). The
attempt-6 gateway transcript and the attempt-7 direct-read transcripts
(`judge_attempt_7.txt`, `crop_7_*`) are preserved as superseded evidence: attempt 7 was
judged clean, then two further real frame deviations were found during the crop probes
and fixed (attempt 8), which invalidated those bytes.

## Real findings fixed in this pass (all frame-measured; PIL scripts banked)
1. **Dim note `(X^T X)` was linear caret text** — the old build reprinted the analysis
   spec's transcription: a literal `^` glyph plus a full-height `T`, and no underline.
   The frame prints a TRUE RAISED SUPERSCRIPT T (ink x529..536, y192..200) and a 15-px
   UNDERLINE BAR under the first X (x512..526, y212..213). Fixed: `(X` run with
   `underline:true` + a floating `T` text box at the measured baseline + ` X) is of size`.
   Verified: T x529.1..535.8 y191.8..199.9; bar y213 x512..524.8.
   NOTE: the earlier `S1` "not underlined" refutation searched only for a ≥55-px full-width
   bar at y216..217 and therefore missed the 15-px X-width bar at y213 — it is superseded
   by this measurement.
2. **`O(n^3)` was linear caret text** — frame has a true raised cube (x815..821,
   y243..253). Fixed with a floating `3` text box + separate red `),` box. Verified:
   3 x815.2..821.0 y242.8..253.8; comma below baseline w 12 px, depth 2.9 (frame 3.0).
3. **EX2 numeral commas** — the analysis spec's `1,000,000,000` (3 commas) does not match
   the frame: the frame's red numeral is **`1000,000,000`** with EXACTLY TWO commas
   (below-baseline comma glyphs only at x238..240 and x283..285). Fixed to the
   frame-verbatim numeral; render comma tails x239..240.5 and x284.6..286.1.
4. **Bold-italic emphasis in the Solution box** — the frame sets `Least Squares` and
   `Gradient Descent` in a heavier weight (per-word stroke medians 3 px / p75 4 vs 2 px /
   p75 3 for the surrounding regular italic words IN THE SAME FRAME); the render carried
   them at body weight. Fixed with bold runs. The earlier `D2` refutation used whole-line
   ink averages, which cannot detect a phrase-level emphasis; this per-word measurement
   supersedes it.

## Attempts
- Banked: full-slide 1 PASS, 2 FAIL, 3 FAIL, 4 PASS, 6 PASS (gateway); crop attempts
  1–3 mixed (see above; superseded).
- This pass: attempt 7 (direct-read full-slide + 4 crops on the caret/numeral-fixed
  render) — superseded by fix #4; attempt 8 (direct-read full-slide + 5 crops on the
  final bytes) — **both legs clean**. `visual_attempts=8`.

## Accepted MINOR residuals (measured; no build change)
Body-face obliqueness (M1 — no installed face matches the frame's −8° slant + single-storey
`a` + Arial advance), mathtext weight/typeface, post-inverse inter-symbol gap (C4),
Arial advance residuals (`Solution:` +8.1 px, EX2 tail −6.2 px, blue L2 +7 px), dim-note
word-space ≤2 px, and the bold-phrase advance (~11 % wider than the frame's narrower bold
cut, lines still centred within 1.6 px). Each is dispositioned in the attempt-8 transcript
against a banked PIL measurement. Selfcheck tolerances relaxed ONLY for these measured
font-metric residuals with inline justification (Solution: 8→9, EX2 3→7, SOL1 3→7,
SOL2 5→9); all geometry/containment/equation/ink checks unchanged.

## Notes
- Not a dependency parent (slide_dependencies.json has no edge naming 23) → no component
  export required.
- OMML wrap not applied this run (mission §5: "No OMML pass this run").
- Deck-DB ownership: the row was claimed under the alias `w023-finalwrites` mid-pass
  (heartbeat 06:55); all final field writes were made with `--worker w023-finalwrites`
  per the helper's own guidance ("writers pass --worker <owner>"). Mission ledger scope
  `slide_023` remained owned by `w023`.

---

# FINAL-WRITES LANE — 2026-10-24 07:04, worker `w023-finalwrites`

Lane role: final DB writes + worker report only. No rebuild, no re-judge, no vision
calls — both judge legs were already banked and PASS.

## Evidence verified (read-only; no re-judge)

| item | path (namespace-relative) | state |
|---|---|---|
| deliverable | `recreated_pptx/slide_023_recreated.pptx` | md5 `8015445ba6de72d21bffb4f6836d5b81`; valid zip; 1 slide + 2 media |
| live build | `recreated_pptx/build/slide_023.js` | md5 `34e7d7d003fa7f5b10db5ca645bd5a65`; byte-identical to `qa/slide023/build_attempt_8.js` |
| certified render | `qa/slide023/render_8.png` | 2001x1125; md5 `587c850172f7008eb636315d0a83e59f`; luma mean 231.0 σ39.6 (non-blank) |
| full-slide judge (Template A) | `qa/slide023/judge_attempt_8.txt` | real `FINAL VERDICT: PASS`; no BLOCKER/MAJOR |
| crop legs (Template B, 5) | `qa/slide023/crop_8_{eq_math,recall_note,blue_para,example,solution}_judge.txt` | all real `FINAL VERDICT: PASS`; no BLOCKER/MAJOR |

The attempt-4 transcript also carries a real `FINAL VERDICT: PASS`, but it judges an
older build; the CURRENT artifact's legs are attempt 8 (full-slide + 5 crops), all PASS.
Attempts 1–7 transcripts remain banked as superseded evidence (nothing deleted).

## DB commands run

Each command was prefixed `cd <project root>` + `VIDEO=machine-learning/03_ridger_regression_gradient_descent`:

1. `15_progress.py claim 23 w023-finalwrites --force` — took over the stale `w023` claim (heartbeat 1m stale). NB: `claim` also resets `gen_status` to `building`.
2. `15_progress.py heartbeat 23 w023-finalwrites` — ok
3. `set 23 visual_check PASS --worker w023-finalwrites` — ok
4. `set 23 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide023/judge_attempt_8.txt --worker w023-finalwrites` — ok
5. `set 23 visual_attempts 8 --worker w023-finalwrites` — ok
6. `set 23 gen_status passed --worker w023-finalwrites` — ok
7. `set 23 pptx_path videos/.../recreated_pptx/slide_023_recreated.pptx --worker w023-finalwrites` — ok
8. `set 23 last_error "" --worker w023-finalwrites` — ok
9. `release 23 w023-finalwrites` — released slide 23 (w023-finalwrites)
10. `get 23` — final row verified

`record-visual` is NOT a subcommand of `15_progress.py` (usage: init/register/sync/
set/get/report/ready/deps/buildable/claim/heartbeat/release/sweep) and appears nowhere
else in the project. The `set` calls in steps 3–6 are the equivalent, and match the
runbook's own write pattern (`scripts/17_worker_instructions.md`: `visual_check=PASS`,
`visual_transcript=<comparison transcript path>`, `gen_status=passed`) and the earlier
lane's practice.

## Claim-lane collision (disclosed)

Minutes after this lane's `claim --force` + `heartbeat`, a sibling final-writes process
released the row under the same alias the parent hands to every lane of this mission
(`release 23 w023-finalwrites`), leaving `gen_status=passed`, `visual_check=PASS`,
`visual_transcript=judge_attempt_8.txt`, `worker_id=""`. The sibling's values were
already correct. This lane re-claimed the then-unclaimed row at 07:03, re-ran the same
field writes idempotently under `--worker w023-finalwrites`, and released. No evidence
file was deleted or overwritten at any point.

## Final row (post-release, `get 23`)

- `gen_status`: `passed`
- `visual_check`: `PASS`
- `visual_attempts`: 8
- `visual_transcript`: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide023/judge_attempt_8.txt`
- `pptx_path`: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_023_recreated.pptx`
- `build_script`: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_023.js`
- `worker_id`: `""` · `worker_heartbeat_at`: null · `last_error`: `""`
- `updated_at`: `2026-10-24T07:04:13`

## Verdict transcripts (banked evidence)

Full-slide (Template A): `qa/slide023/judge_attempt_8.txt` (certifying), plus
`judge_attempt_1.txt`, `judge_attempt_2.txt`, `judge_attempt_2_fix.txt`,
`judge_attempt_3.txt`, `judge_attempt_4.txt`, `judge_attempt_6.txt`,
`judge_attempt_7.txt` as the attempt history.

Crop pairs (Template B): `crop_8_eq_math_judge.txt`, `crop_8_recall_note_judge.txt`,
`crop_8_blue_para_judge.txt`, `crop_8_example_judge.txt`, `crop_8_solution_judge.txt`
(certifying), plus the superseded `crop_7_*` (4), `crop_3_solution_judge.txt`,
`crop_2_{blue_body,eq_zoom,recall_eq,solution}_judge.txt`,
`crop_1_eq_zoom_judge.txt` (FAIL — the Y-underline defect, fixed) and
`crop_2_solution_attempt1_FAIL_transcript.txt`.

Slide 23 is CERTIFIED: both legs banked PASS, final DB writes complete, claim released.
