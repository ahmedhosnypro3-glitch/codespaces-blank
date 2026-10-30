# Worker report — slide 022 (badge numeral 22), `machine-learning/03_ridger_regression_gradient_descent`

Worker: `w4-s022-20261020T1854` (10-20). **RESUMED** from a crashed predecessor
(`s022-w3-20261019T2344`, heartbeat stale 1149 min at claim time; died in the
2026-10-19/20 vision-upstream outage with substantial banked offline state).
Attempt numbering continues from 1 — **no judge transcript existed** before this
run. All banked evidence was reused and nothing was deleted.

## Final verdict: **PASS** (certified)

- Full-slide Template A judge: **PASS** — `qa/slide022/judge_attempt_1.txt`
  (ends `FINAL VERDICT: PASS`; no BLOCKER/MAJOR/MINOR discrepancies found).
- Template B crop certificates (all four clean):
  | crop | transcript | verdict | notes |
  |---|---|---|---|
  | title (two-line block, x170..750 y220..380) | `crop_1_title_judge.txt` | PASS | 1 MINOR (inter-line leading perception) — PIL-refuted |
  | badge (x840..897 y46..102) | `crop_1_badge_judge.txt` | PASS | no discrepancies |
  | line1 tight zoom (x180..735 y228..282) | `crop_1_line1_judge.txt` | PASS | 1 MINOR (red hue) — PIL-refuted |
  | line2 tight zoom (x265..665 y318..372) | `crop_1_line2_judge.txt` | PASS | 1 MINOR low-confidence (paren extent) — PIL-refuted |
- Attempts used: **1 of 6**. No fix cycle, no re-render, no re-judge was needed.

Deliverable (single version): `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_022_recreated.pptx`
Build script: `videos/.../recreated_pptx/build/slide_022.js` (byte-identical to
the banked `qa/slide022/build_attempt_1.js`; the on-disk pptx is provably what
this script produces — a redirected rebuild renders pixel-identical, 0/2,251,125
px; only the zip's `docProps/core.xml` timestamp differs).

## Resume verification performed before judging (outage-ruling offline work)

1. **Fresh re-render of the CURRENT pptx** (150 dpi, private scratch, own LO
   profile `/tmp/lo_slide022`, `TMPDIR=scratch/tmp`) is **pixel-identical** to the
   banked `qa/slide022/render_1.png` (md5 `1a4b00687a154164f26cc785b260dd3f`) — the
   banked render is current, so no new render number was needed.
2. **`house_chrome_check.py`**: PASS — `panel x 112-1882, y 94-bottom; strokes L/R/bottom
   present, top bare; badge center (1824,152) d=68; all within tol 8`.
3. **Pre-judge self-check** (banked `selfcheck_final.py` logic re-run on the fresh
   render, output banked in `selfcheck_resume_current.txt`): PASS — L1 band
   x190.5..723.0 y236.6..272.2, L2 x275.9..650.6 y326.9..362.4, all corrected
   residuals within 2.0 frame px (L1 x1 at −1.50 inside the adjudicated 2.5
   rasterizer allowance), pitch 90.24 vs 90.00, zero stray red ink above/between/
   below the title, census = exactly {badge, L1, L2}, core color exactly (192,0,0).
4. **Crop pairs re-cut from the current render** (`make_crops_2.py`): all four
   regions re-derived from the fresh render (IMG1 provably current), originals
   LANCZOS-upscaled to each render crop's EXACT output size — matched effective
   scale per axis by construction (asserted in-script). The re-cut title/badge
   render crops are byte-identical to the banked ones (28840 / 3090 bytes),
   proving the predecessor's pair was already current.
5. **Component banked**: `recreated_pptx/build/components/slide_022.js`
   (`renderBase` + per-block `skip`/`only`-style opts, house-chrome numeral
   override) — playlist-scoped obligation; a render of the component is
   pixel-identical (0/2,251,225 px) to the certified deliverable. No slide in this
   video depends on 022 (root, no children).

## Judge-finding adjudication (PIL-first, all banked in `judge_adjudication.txt`)

All three MINOR findings were **refuted by measurement** (none is a fix trigger):

1. *Title leading "larger in the recreation"* — measured pitch 90.24 vs 90.00 frame px
   (0.27%) and identical vertical band positions (residuals ≤0.38 px); the read is
   JPEG-wash/upscale softening of the original.
2. *Line-1 red hue "brighter in the recreation"* — render core is exactly `C00000`
   (192,0,0); the original's darkest core measures (121,1,13), i.e. the original is
   JPEG-DARKENED C00000 (founder-ratified family nominal).
3. *Line-2 paren extent "taller in the recreation"* (low confidence) — fixed
   full-glyph window probe (`judge_adjudication_paren2.txt`): render paren
   36.5 vs original 39.0 frame px = the expected −3.0 px wash allowance within 2 px;
   same Arial 38 pt glyph, same extent.

Also artifact-classified (not discrepancies): the "stray diagonal gray stroke above
the M" in the line-2 crop is the mouse-cursor sliver measured at x 519..556,
y 311..325 (`measure_cursor.py`) — correctly omitted per ground rules (c) +
recreation_brief step 9. Note: the analysis JSON's claimed cursor position
(44% x / 50% y = (422,270)) was wrong; the measured position is (519..556, 311..325).

## Content fidelity (verbatim law)

- Title line 1 `[3] Inverse of High Dimension`, line 2 `(non-singular) Matrix` —
  verbatim, bold Arial 38 pt `C00000`, each line its own single-line box at its
  measured ink position (spec pinned 48 pt from a 44–54 estimate; the frame
  measured 38 pt — frame wins, same law as the certified sibling 020).
- Badge numeral `22` (file number, printed on the original; verified via the raw
  analysis `verbatim_text.labels`) — house chrome module, deck 03 geometry
  (E9E9E7 panel, C00000 L/R/bottom strokes with NO top stroke, FDFD96 badge with
  6A5ACD ring).
- No equations, no tables, no charts, no graphs on this slide — nothing to render
  via mathtext/OMML and nothing for the graphgen path; therefore no
  `build/assets/` equation sidecars and no OMML wrap is applicable.
- Mouse cursor correctly NOT recreated (video-capture artifact).

## Vision-law note (outage window)

The Nvidia vision upstream had been down for the fleet since 2026-10-19 16:48; it
**recovered during this run** — the probe at 16:23 UTC and every subsequent judge
dispatch (full-slide + 4 crop pairs) produced winner bodies on the first call
except one internal gate retry (line1 crop: a 630 s hard-wall HangError abort
that the gate itself retried; the winner body landed on its retry). That recovery
signal should be broadcast fleet-wide. Per the coordinator's outage ruling, dead
dispatches consume no attempt budget, and none were dead here. Vision law honored
throughout: all calls via `scripts/16_vision_gate.sh` wrapping
`.agents/skills/image-analysis/scripts/analyze_image.py`, positional
`comparison` mode, `--thinking high --max-tokens 65536 --timeout 600`, outer
`timeout 1700`, no `--models`, `--transcript` banking. judge procedure executed
by the worker via Bash — **no judge-spawn tool available in this environment**.

## DB state

`gen_status=passed`, `visual_check=PASS`,
`visual_transcript=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide022/judge_attempt_1.txt`,
`visual_attempts=1`, `pptx_path`/`build_script` unchanged and verified. Every
`15_progress.py` invocation was prefixed `VIDEO=machine-learning/03_ridger_regression_gradient_descent`
(no stray writes to the closed ml-intro deck). Claim released at close.

## Banked QA artifacts (`qa/slide022/`)

Inherited (predecessor, never deleted): `dispatch_brief.txt`, `build_attempt_1.js`,
`build_pre_tune1.js`, `render_1.png`, `render_2.png`, `render_pre_tune.png`,
`selfcheck_attempt_1.py`, `selfcheck_attempt_2.py`, `selfcheck_final.py`,
`selfcheck_pass1_render.png`, `measure_frame_1.py`, `measure_frame_2.py`,
`measure_cursor.py`, `judge_prompt_1.txt`, `make_crops_1.py`,
`crop_1_title_prompt.txt`, `crop_1_title_*`, `crop_1_badge_*`.

Added by this run: `probe_1.txt`, `judge_attempt_1.txt`,
`judge_attempt_1_cmd.txt` (the exact Template A dispatch),
`crop_1_title_judge.txt`, `crop_1_badge_judge.txt`, `crop_1_line1_judge.txt`,
`crop_1_line2_judge.txt`, `crop_1_badge_prompt.txt`,
`crop_1_line1_prompt.txt`, `crop_1_line2_prompt.txt`,
`crop_1_line1_render/orig.png`, `crop_1_line2_render/orig.png`,
`make_crops_2.py`, `selfcheck_resume_current.txt`,
`judge_adjudication.txt`, `judge_adjudication_paren.txt`,
`judge_adjudication_paren2.txt`, `worker_report.md` (this file).

One-line judge-flag summary: full-slide PASS with zero discrepancies; four crop
certificates PASS (title/badge/line1/line2); the only three MINOR observations
(title leading, red hue, paren extent) were all PIL-refuted as JPEG-capture
artifacts, and the build was left unchanged.
