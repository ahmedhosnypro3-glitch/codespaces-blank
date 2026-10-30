# Worker report — slide 029 (03_ridger_regression_gradient_descent)

**Final verdict: PASS** — certified on judge attempt 1 (both legs clean), 1 of 6
attempts used. Deliverable: ONE pptx, single version, no suffixes.

## Resume disclosure (protocol requirement)

This worker RESUMED a dead worker that died from a harness provider timeout
~27 min into its measurement phase. State inherited (all banked, all reused):

- `measure_original.py` + `measure_original_output.txt` — frame measurement:
  three red title bands + house chrome; badge bbox; panel/canvas/stroke colors.
- `measure_rows.py` + `measure_rows_output.txt` — per-row ink profiles
  (ascender/x-height/descender structure, band pitch 78px).
- `fit_fonts.py` — the dead worker's font-fit script, **never run** (died first).

NO build script, pptx, render, or judge attempt existed; this worker started the
build fresh, judge attempt numbering starts at 1, and the dead worker's released
DB claim was replaced by a new unique-id claim
(`worker-slide029-resumed-zcode-20261019`, heartbeat-maintained, released at end).

## Inherited-artifact audit (trust-but-verify)

- `fit_fonts.py` had a fatal bug: it rendered glyphs at 1x but divided ink by 4
  ("supersample" never wired) — its sweep would have been garbage. Replaced by
  `fit_fonts2.py` (copy-then-modify; original kept banked) rendering at 4x with
  clipping guard. First run of the fixed script ALSO hit a sweep-range bug
  (range encoded 82.0-107.9pt instead of 38-58pt) — caught because every line's
  error pinned positive at the range edge; fixed, re-run, banked.
- Banked row measurements were verified against a same-predicate re-derivation
  (predicate drift ±1px on band edges — acceptable, documented in
  `selfcheck_attempt_1.py` output).

## Build (attempt 1 → pre-judge iteration → deliverable)

Content: three centered bold-red title lines + house chrome only (full-frame
sensitive-ink scan of the original shows nothing else — matches spec note).
Spec's pre-house chrome values (#F2F2F2 bg, #FFFF00 badge, gray border) are
overridden by this deck's measured house chrome (white canvas, E9E9E7 panel,
C00000 L/R/bottom strokes, NO top stroke, FDFD96/6A5ACD badge, numeral 29).

- Font fit (`fit_fonts2_output.txt`): Liberation Sans Bold (Arial-metric,
  drawn as `fontFace: "Arial"`) at **44.65pt** fits ALL THREE line widths
  within 0.3% (687.0/395.8/476.0 vs 688/397/477) — residuals ~1px, no
  charSpacing. Width fit beats the h=46 band-height reading, which is
  JPEG-halo-inflated (true glyph extent at 44.65pt = 42px; cap ~32px).
  Corroborates the deck-family title size (sibling slide 035 fit 44.3-44.5pt).
- Layout: THREE single-line boxes (explicit-line-spacing pattern; fixed y per
  line = pixel-exact 78px baseline pitch), pinned `lineSpacing: 53.58`
  (1.2em), `align: center`, bold, `C00000`, margin 0. L2/L3 ink centers sit
  13px/7px left of slide center (original's trailing-space geometry) —
  replicated by centering each box on the measured ink cx, text verbatim
  (sibling slide 035's approach). Box widths 820/500/580 (wrap budget ~20%
  beyond ink).
- **Pre-judge closed-loop fix (render_1 → render_2)**: the peer slide 035 LO
  baseline model (baseline = top + halfLead + 0.905·S) placed the block
  +1.72/+2.20/+1.72px low on all three lines (measured in
  `probe_baselines_1_output.txt`). Folded `LO_CORR = 1.9` into BASE_OFF;
  uniform shift preserves the exact 78px pitch. Post-fix `selfcheck_render_2`:
  baseline deltas −0.20/+0.28/−0.20, pitch 78.48/77.52, halo-aware top deltas
  +2.64/+3.12/+2.64 (the remainder is original-only JPEG halo above thin
  ascender tips — `build_pre_lofix.js` documents the pre-fix state; the
  pre-change bank omission it repairs is disclosed there).
- Mandatory pre-judge self-check (all PASS, `selfcheck_render_2_output.txt`):
  house_chrome_check PASS (panel/strokes L-R-bottom/top-bare/badge d=68);
  exactly 3 bands, no stray ink outside them (wrap check), frame containment
  clearances 79-238px to strokes, badge numeral ink present. No equations,
  multi-line delimiters, or tables on this slide (checks 3/4/5 N/A).
- Patterns used: house-chrome (shared module), explicit-line-spacing,
  wrap-budget boxes. `judge-invocation` + `dense-region-crop-compare` for QA.

## Judge — both legs, both first-attempt PASS

Judge procedure executed by the worker via Bash per the orchestrator-approved
fallback (no subagent-spawn tool in this toolset). All calls through
`scripts/16_vision_gate.sh`; `-p` payloads byte-for-byte from the frozen
`judge_protocol_03.md` (banked: `judge_payload_1.txt`,
`crop_payload_1_title.txt`). Certificate label: **single-read, default route
(images), glm leg DEFERRED/BLOCKED** (per routing law; no glm batch attempted).
Operational note: the frozen template's script path
(`.agents/image-analysis/...`) is the skill's pre-2026-10-11 location — resolved
to `.agents/skills/image-analysis/scripts/analyze_image.py`; `-p` and flags
unchanged.

Binding note: judge attempt 1 judges `render_2.png` (the deliverable);
`render_1.png` is the banked pre-judge engineering iteration — no judge spent
on it. Renders and attempts number independently (judging.md).

| Leg | Transcript | Verdict | Notes |
|---|---|---|---|
| Full-slide (Template A, K=1) | `judge_attempt_1.txt` | **PASS** | "Discrepancies: None found. Severity: N/A. Confidence: High." Verbatim 3-line title confirmed; degenerate events 0; probe `probe_1.txt` valid |
| Crop-pair (Template B, region `title`, K=1) | `crop_1_title_judge.txt` | **PASS** | Glyph-by-glyph verification of all 3 lines; colon + `(GD)` parens verified present/correct; "Discrepancies: NONE"; degenerate events 0 |

Crop pair: frame (125,180)-(840,403) — the slide's single dense region (all
three title lines). Matched effective scale proven in `crop_prep_1_output.txt`
(1490x465 both, dx=dy=0.00000). The crop body's two "non-discrepancies noted"
(black letterbox bars / a dark bottom-right mark in IMG2) are PIL-REFUTED in
`crop_1_title_refutation.txt`: every edge of the exact judged crop is pure
E9E9E7 gray, dark-pixel fraction 0.0000 — judge variance, already not counted
by the judge itself.

## Certification proof

Re-rendered the on-disk deliverable and PIL-diffed against the certified
`render_2.png`: **0 of 2,251,225 pixels differ; identical md5**
(bd7d9b44207a8284586ae667cd2a191a) — the on-disk pptx serves exactly the
certified pixels. Post-certification OMML wrap: N/A — this slide has no
equations (no eq_* sidecars, no manifest needed).

## DB record (verified with get, then released)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide029/judge_attempt_1.txt`,
`pptx_path=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_029_recreated.pptx`,
`build_script=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_029.js`,
`last_error=null`.

## Artifacts (qa/slide029/)

Inherited: dispatch_brief.txt, measure_original.py/.txt, measure_rows.py/.txt,
fit_fonts.py. This worker: fit_fonts2.py/.txt, build_attempt_1.js,
build_pre_lofix.js, render_1.png (pre-judge iteration),
selfcheck_attempt_1.py/.txt, probe_baselines_1.py/.txt,
selfcheck_attempt_1b (inline in transcript history),
selfcheck_render_2.py/.txt, render_2.png (certified),
judge_payload_1.txt, judge_prompt_1.txt, probe_1.txt, judge_attempt_1.txt,
crop_prep_1.py/.txt, crop_1_title_render.png, crop_1_title_orig.png,
crop_payload_1_title.txt, crop_prompt_1.txt, crop_1_title_judge.txt,
crop_1_title_refutation.txt, worker_report.md.

## Judge-flag summary (one line)

Attempt 1 both legs PASS with zero discrepancies; the only judge notes were
two self-classified "non-content" observations (letterbox bars, a dark mark)
that PIL measurement refutes outright — no fix triggers, no findings carried.
