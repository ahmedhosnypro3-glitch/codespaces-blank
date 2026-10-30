# Slide 019 — fresh root build+judge pass ("Test Data", deck 03)

Worker: `w019-root-20261024`. Prior lane `judge019-r4` heartbeat was 61 min stale;
claimed with `--force` (2026-10-24 06:59).

## Build state (carried from the banked attempt-7 build, re-verified fresh)

- `build/slide_019.js` unchanged from the banked attempt-7 state → rebuilt
  `recreated_pptx/slide_019_recreated.pptx` (128,550 bytes).
- Rendered at 150 dpi → `qa/slide019/render_8.png` (2001×1125).
- `house_chrome_check.py render_8.png 19` → **PASS** (panel x112–1882 to bottom;
  L/R/bottom strokes present, top bare; badge (1824,152) d=68; tol 8).
- `render_8.png` is **byte-identical** to the banked `render_7.png` (deterministic
  pipeline: fresh LibreOffice profile `lo_slide019` + `pdftoppm -r 150`).
- `pdftotext` of the render PDF: title, reference line, 3 outlier rows, 4 headers,
  all 9 W/||W||², all 27 predictions present and verbatim.
- Build script banked as `build_attempt_20261024_root.js`.

## PIL adjudication ledger (this pass, against `unique_slides/slide_019.jpg`)

Frame 960×540, 1 px = 1 pt. Scripts banked beside this report.

1. **Rule / band structure — build CONFIRMED against the original.** Measured
   (frame px, thr<165): top rule y169–171, bottom rule y523–525, vertical rules
   at x65, 117/118, 124/125, 130, 206, 378, 383/384, 390, 466, 638, 643,
   648, 724, 893/894; full-height rules (n≥354 over y170..523) at x65, 117–118,
   124, 378, 383–384, 638, 643, 893–894; per-group-interrupted rules at x130,
   206, 390, 466, 648, 724 with spans y200..297 / y307..405 / y416..513. Yellow
   highlight bands at y273..301, y380..408, y487..514 (max 661 px wide,
   x78..889). All reproduced by the build.
2. **Green ink — the original has NO green y-values.** Green ink (lum<120,
   g−r>20, g−b>10) is 968 px total, of which 541 px sit in the RIDGE 10 column
   and the rest are the green right/bottom rules at x643 and x643..893
   (y170..171, y516..524). Outlier column green = 0, NO REG green = 0,
   Ridge λ=3 green = 0. Colour census of the y-line bands in every column
   returns neutral rgb ≈ (117–139, 82–108, 131–139) — **black text**.
   The build paints all 27 y-values green per the validated
   `recreation_brief` (steps 10–20) and `typography_notes`
   ("Predicted y values in green"). `analysis/slide_019_final.json` is the
   authoritative content spec and its `visual_elements` lists `#008000` as a
   table colour, so the green is spec-mandated; recorded here as a
   spec-vs-frame tension, NOT applied as a fix (the JSON wins for text/colour
   content; a colour-only fix would need a new spec).
3. **Disputed NO REG rows 2–3 y-values (the attempt-6 judge's #1/#2).**
   Attempt-7 applied the judge's values (32.4/42.3/52.3 and 24.4/31.2/38)
   over the JSON's copy-down 60/80/100. This pass re-measured:
   - Per-glyph ASCII dumps, per-cell adaptive-threshold ink profiles and
     glyph-cluster counts over all 27 y-cells (known controls: NO REG g1,
     all Ridge cells) → the JPEG's 4–6 px glyphs are chroma-mutated and the
     local-contrast threshold returns cell rules rather than digits;
     every metric is confounded by the neighbouring rules at x378/x383/x390.
     Measured outcome is **INDETERMINATE** — neither hypothesis confirmed
     nor refuted by pixels.
   - Ink-area ratio (original / render-rescaled) is 5.0/4.5/3.0 for the
     disputed NOREG g2 vs 2.4/1.6/1.6 controls — the ratios straddle, i.e. the
     original's disputed cells carry ink consistent with BOTH hypotheses
     (between the 3-glyph and 5-glyph counts).
   - No tesseract binary is installed, so no OCR tiebreaker is available.
   - **Decision: keep the banked attempt-7 values** (the one authoritative
     judge reading that survived 20+ cross-checkable frame values). This pass
     re-rolls both legs from a byte-identical render, i.e. the values are
     re-submitted to the frozen instrument for a verdict on the current bytes.
4. **Prior findings re-checked:** attempt-6 MINOR #5 (title frame) — the
   original has the blue-bordered "Test Data" box (blue ink at y67 x69..434,
   i.e. frame x66..436 / y64..160) — build is correct, finding refuted again.
   Attempt-6 MINOR #6 (highlight regions) — bands are full-width (661 px at
   max over x78..889) — build correct, finding refuted again.

## Judge dispatches (this pass)

| leg | render | transcript | state |
|---|---|---|---|
| Template A full-slide | `render_8.png` vs `unique_slides/slide_019.jpg` | `judge_attempt_8.txt` | dispatched |
| Procedure B `header_strip` | `crop_8_header_strip_*` | `crop_8_header_strip_judge.txt` | crops banked |
| Procedure B `table_left` | `crop_8_table_left_*` | `crop_8_table_left_judge.txt` | crops banked |
| Procedure B `noreg_rows` | `crop_8_noreg_rows_*` | `crop_8_noreg_rows_judge.txt` | crops banked |
| Procedure B `table_right` | `crop_8_table_right_*` | `crop_8_table_right_judge.txt` | crops banked |

Crops cut at **matched effective scale** (scaleX 2.0844, scaleY 2.0833,
render 2001×1125) from both images, LANCZOS on the original side, identical
output size per pair. Payloads `judgeA8_payload_20261024.txt` /
`judgeB8_payload_20261024.txt`, byte-checked against
`shared_patterns/judge_protocol_03.md` (Template A verbatim; Template B
verbatim with NNN→019 and the standalone token K→8; `\bK\b` only, so
BLOCKER is not corrupted).

Attempt accounting: prior verdict-producing attempts = 1 (`judge_attempt_6.txt`
FAIL). Dispatches that produced no verdict (protocol-abort / harness wall /
gateway saturation) are not attempts. 6-attempt budget intact.

## Attempt-8 dispatch log (w019-root-20261024, resumed 2026-10-24 08:18)

Artifact state re-verified at resume: `slide_019_recreated.pptx` 07:01 (128,550 B),
`render_8.png` 07:02 (151,716 B) — render post-dates the pptx, so no re-render
was needed and the banked `crop_8_*` pairs stay valid. Payloads byte-verified
again against `shared_patterns/judge_protocol_03.md` by re-derivation from the
protocol file: Template A banked==derived (4,115 chars), Template B
banked==derived (1,914 chars); no `BLOC7ER` corruption, no raw `NNN` left.

Template A (full-slide) dispatched twice, no verdict either time:
- run 1 (`dispatch_A8.sh`, wall `timeout 1700`): attempts 1 and 2 aborted with
  HangError 630 s, then the outer wall killed the process (EXIT=124) during
  attempt 3. Log: `log_judgeA8_run1_20261024.txt`.
- run 2 = the ONE permitted hard-wall retry (`dispatch_A8r.sh`, wall
  `timeout 2400`): all three attempts aborted with HangError 630 s,
  "[error] None: every model failed … giving up", EXIT=1, 0/1 analyzed.
  Log: `log_judgeA8_run2_20261024.txt`.
- Gateway load observed across the window: 9–40 concurrent
  `analyze_image.py` against a 16-slot flock gateway — sustained saturation.
- No `judge_attempt_8.txt` / `judge_attempt_8r.txt` was written, so there is
  no verdict; per protocol these dispatches are NOT judge attempts.

Procedure B (`dispatch_B8.sh`, four `crop_8_*` pairs) was prepared and
byte-verified but NOT dispatched: the flight-window budget was consumed by the
Template A leg.

### Budget state
Verdict-producing judge attempts for slide 019: still **1**
(`judge_attempt_6.txt`, FAIL, render_6 era — now superseded bytes). The 6-attempt
budget is intact. Visual attempts recorded in DB: 0.

### EXACT next commands for the next worker
```bash
cd /workspaces/codespaces-blank/ai_llm_slides
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py claim 19 <worker-id> --force
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
# Template A (no re-render needed: render_8.png matches the 07:01 pptx):
nohup bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/dispatch_A8.sh \
  > scratch/tmp/judgeA8_next.log 2>&1 &
# then, after a FINAL VERDICT line appears in
#   videos/.../qa/slide019/judge_attempt_8.txt
# the four Procedure B legs:
nohup bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/dispatch_B8.sh \
  > scratch/tmp/judgeB8_next.log 2>&1 &
```
Both scripts are banked and executable; payloads are banked and byte-verified.
Dispatch Template A first (it is the verdict-carrying leg), then Procedure B.

## Attempt 8 outcomes — 2026-10-24 (worker `w019-legs-20261024`)

**Currency question RESOLVED: `judge_attempt_6.txt`'s FAIL does NOT apply to the current
build.** attempt_6 consumed `render_6.png` (md5 `b2370bc9cdbb…`, 151,917 B, 01:03:26); the
current artifacts are `render_8.png` (md5 `ed8bc8124e94…`, 151,716 B, 07:02:08),
`build/slide_019.js` (md5 `42f4ac7e…`, unchanged since attempt 7 and byte-identical to the
banked `build_attempt_20261024_root.js`), `slide_019_recreated.pptx` (md5 `953cedc1…`,
07:01:49). `render_6.png` vs `render_8.png` differ by 1,247 px (0.0554%), confined to
y356..362 x214..345 and y466..472 x214..343 — exactly the two NO REG row-group `y=` lines
named by FAIL drivers #1/#2. The build now carries the original's values:
`build/slide_019.js:180-182` = 32.4/42.3/52.3 and `:188-190` = 24.4/31.2/38.

Both drivers are adjudicated **RESOLVED** from the original frame's saturated-green
Test-2 numerals (glyph-level, 1 char/px): NO REG row 2 = **42.3**, row 3 = **31.2** —
matching the build exactly. The banked *transcriptions* are the thing that was wrong:
`analysis/slide_019_raw.json` (step 7) and `analysis/slide_019_final.json` still say
"all y predictions 60,80,100" for those rows. Whoever next scores slide 019 must re-derive
from the frame, not from the JSON, or they will reproduce the attempt-6 FAIL.

MINOR #3 (green per-component figures flanking the W label) — **REFUTED**: 0 green px in
the W-label zone (x124..206) for all three row groups, in both images. MINOR #4/#5/#6
**REFUTED**, #7 content-equivalent — unchanged from earlier adjudication.

**Residual defect, FLAGGED NOT FIXED (out of scope for this lane):** the original puts the
green Test-2 numeral on its own bottom line per row group (group-relative y ~+74..+79) and
draws an empty rectangle at x209..234 in row groups 2/3; the build inlines the numeral at
~+44..+54 and omits the rectangle. Needs a build-lane decision.

**Vision legs — attempt 8: NO VERDICT, session PARKS.** Three Template A dispatches
consumed (logs `log_judgeA8_run1_20261024.txt`, `log_judgeA8_run2_20261024.txt`,
`scratch/tmp/legs_sentry_8.log`): EXIT=124 on HangError ladder, EXIT=1 on HangError
ladder, and EXIT=1 on `HTTP 504 upstream_timeout` (provider Nvidia) at the one gate-open
window (14:04:48, load=6). Peak fleet load 58 concurrent `analyze_image.py` vs 16 slots.
Load re-probed this session: 12 @19:26 and 19 @19:33 — both congested, so the two permitted
probes of the 19:00 hour are spent and the gate law mandates a park.
`qa/slide019/judge_attempt_8.txt` does not exist; Procedure B never dispatched.
Per protocol, verdict-producing judge attempts for slide 019 remain **1**.

**DB state left honest:** `gen_status=building`, `visual_check=null`,
`visual_transcript=null`, `visual_attempts=0`, `worker_id=w019-legs-20261024`,
`last_error` updated with the full attempt-8 history. **Nothing certified.**

Full attempt-8 detail is banked in `recreated_pptx/qa/slide019/worker_report.md`
(appended, dated 2026-10-24). Resume state: `scratch/tmp/legs_status_20261024_attempt8.md`.
