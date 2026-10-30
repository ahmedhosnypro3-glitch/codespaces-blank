# Worker report — slide 035 (machine-learning/03_ridger_regression_gradient_descent)

**Slide:** 035 — "Using Gradient Descent to train Linear Regression Model" / "(Problem Formulation)"
**Worker:** worker-slide035-1792408227 (claimed 2026-10-19, fresh row, no prior worker)
**Final verdict: PASS** — certified 2026-10-19. `gen_status=passed`, `visual_check=PASS`,
claim released.

## Deliverable

- **pptx:** `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_035_recreated.pptx` (single plain-named version)
- **build script:** `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_035.js`
- **component banked (playlist-scoped obligation):** `recreated_pptx/build/components/slide_035.js` — `renderBase(pptx, slide, opts)` + per-block `drawTitleLine1/drawTitleLine2/drawSubtitle`, house chrome via `shared_patterns/house_chrome.js` (drawn once; pass `opts.numeral` when reusing for a child)

## Judge attempts used: 3 real evidence calls (of 6 max; 0 garbage re-invokes; 0 W4 retries)

| # | Leg | Template | Transcript | Verdict |
|---|---|---|---|---|
| 1 | Full-slide comparison | A (frozen, judge_protocol_03.md) | `qa/slide035/judge_attempt_1.txt` | **PASS** — BLOCKER: none, MAJOR: none, MINOR: none. `[winner] images (round 1, attempt 1)`, 0 degenerate events |
| 2 | Zoomed crop-pair, region `title` (the two-line red title block) | B | `qa/slide035/crop_1_title_judge.txt` | **PASS** — Discrepancies: none |
| 3 | Zoomed crop-pair, region `sub` (blue subtitle + parens) | B | `qa/slide035/crop_1_sub_judge.txt` | **PASS** — Discrepancies: none |

Judge flags summary: **zero discrepancies raised on any leg** — the only mentions were
ground-rule waivers (the original's mouse-cursor video artifacts correctly omitted per
rule (c); JPEG/compression softness in IMG2 inherent).

Prompt/verdict provenance: `judge_prompt_1.txt` + `judge_payload_A.txt` +
`crop_payload_B.txt` banked (payloads extracted byte-for-byte from
`shared_patterns/judge_protocol_03.md`; probe transcripts `probe_1.txt`).
Certificate label per routing law: **single-read, default route (images), glm leg
DEFERRED/BLOCKED.** Judge procedure executed by the worker via Bash (no spawn tool in
this environment — orchestrator-approved fallback).

### Storm event (transient, no attempt spent)
The first `sub` crop dispatch (concurrent with the `title` crop) failed with
HTTP 502 `upstream_dns_failed` (IronRouter → Nvidia upstream DNS) — no transcript
written, no evidence, so not a spent attempt. Per storm-resilience law: slept 120s,
re-dispatched once → PASS on retry 1 (retry log `crop_judge_1_sub_retry1.log` banked in
project scratch).

## Closed-loop build evidence

- **Measured geometry** (unique_slides/slide_035.jpg, 960×540, 1px=1pt, JPEG smear ±2px):
  L1 "Using Gradient Descent to train" ink x147..813 center 480, baseline 211;
  L2 "Linear Regression Model" ink x217..743 center 480, baseline 288.5 (pitch 77.5);
  SUB "(Problem Formulation)" ink x271..678 center 474.5 (= slide center minus half a
  trailing space — the ink geometry is replicated, the text stays verbatim), baseline 357.
  Font sizes fit from ink widths (Liberation Sans Bold = Arial metrics):
  L1 44.5pt / L2 44.3pt → 45pt after the LO-render correction; SUB 38.1 → 38.4pt.
  Colors: title C00000 (frame core (181,32,46) = JPEG-darkened C00000, family nominal),
  subtitle 0000FF (frame core (20,9,196)). Two single-line title boxes (pixel-exact
  77.5px pitch, no LO/PPT auto-pitch divergence), lineSpacing pinned (54/54/46pt),
  boxes ~23% wider than ink (no wrap).
- **Pre-judge iterations** (banked, no vision spent): `render_pre1.png` (44pt fit —
  ink 2.1% narrow), `render_pre2.png` (45pt, baselines +1.6px low) → `render_1.png`
  (final): all ink x-extents within 1.6px, baselines within 0.2px of frame targets;
  the frame's x-height "jump rows" sit 2-3px above true x-height (JPEG pre-echo) —
  documented in `selfcheck_attempt_1.py` / `.out.txt`.
- **house_chrome_check.py: PASS** (panel x54..903 y45..bottom; L/R/bottom strokes,
  NO top stroke; badge center (1824,152) d≈68 at 150dpi; numeral 35).
- **Pre-judge self-check** (all 8 items): patterns used (house-chrome shared module,
  explicit-line-spacing, wrap-budget boxes); frame containment — content ink
  x146.4..814.6 / y178.6..365.3 well inside panel x54..903 y45..540; equations — none
  on slide; delimiter geometry — single-line font parens span the one line by
  construction, no overlap; tables — none; zoomed crops — done (leg 2); line/box wrap —
  one band per element, no spillover; lineSpacing pinned + measured pitch = pinned.
- **Render binding proof** (`render_binding_proof.txt`): fresh render of the deliverable
  vs certified `render_1.png` = **0 / 2,251,125 px differ**.

## Frame-vs-spec deviations (frame wins; documented)

- Spec's `#F2F2F2` background / `#FFFF00` badge with black outline / gray `#808080`
  border are pre-house-analysis values — the deck house chrome (white canvas, E9E9E7
  panel, C00000 L/R/bottom strokes, FDFD96 badge + 6A5ACD ring) overrides them (deck
  AGENTS.md law).
- Spec's "white mouse cursor at ~85%/20%": not corroborated by my pixel scans, but the
  full-slide judge did see cursor artifacts in IMG2 — either way it is a video-capture
  artifact (judge ground rule (c)) and is correctly omitted from the recreation.
- Exact line break of the title was unspecified in the spec; PIL-measured descender
  positions prove L1="Using Gradient Descent to train" / L2="Linear Regression Model".

## Incident + repair (recorded for the owner)

Mid-run DB-error: four milestone `set` commands were run WITHOUT the `VIDEO` env var
and hit the default (ml-intro) DB, overwriting certified row 35 of
`videos/machine-learning/01_ml-intro/slides_progress.db` (gen_status→judging,
build_script/pptx_path→deck-03 paths, visual_attempts→1). Repaired immediately from
git (`git show HEAD:...slides_progress.db`): all three string fields restored
byte-equal to the committed certified values (gen_status=passed, ml-intro paths,
visual_attempts=1 — verified by full-row diff, only `updated_at` differs as the
repair's own timestamp). Deck-03 milestones were then re-written WITH
`VIDEO=machine-learning/03_ridger_regression_gradient_descent` and verified. The
committed ml-intro DB copy used for the diff is banked at
`scratch/tmp/mlintro_db_committed.db`. No other rows or fields were touched.

## Files banked under `qa/slide035/`

dispatch_brief.txt, build_attempt_1.js, judge_prompt_1.txt, judge_payload_A.txt,
crop_payload_B.txt, probe_1.txt, judge_attempt_1.txt, crop_1_title_render.png,
crop_1_title_orig.png, crop_1_title_judge.txt, crop_1_sub_render.png,
crop_1_sub_orig.png, crop_1_sub_judge.txt, render_1.png (certified),
render_pre1.png, render_pre2.png, selfcheck_attempt_1.py, selfcheck_attempt_1.out.txt,
render_binding_proof.txt, worker_report.md (this file).

## Notes for the orchestrator

- OMML wrap: N/A — slide 035 contains no equations (`verbatim_text.equations` empty),
  no `eq_*.json` sidecars banked.
- Advanced graphs: N/A.
- No same-deck dependents; component banked for cross-deck reuse.
