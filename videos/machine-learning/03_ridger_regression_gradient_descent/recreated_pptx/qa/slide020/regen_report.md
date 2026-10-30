# Slide 020 regeneration report — ML lecture 03 (Ridge Regression & Gradient Descent)

Worker: `regen-worker-020-139656`. Run date: 2026-10-23.

## Task

Slide 020 was previously judge-certified (DB `visual_check=PASS`, 3 banked judge
transcripts) but its single-plugin-named deliverable
`recreated_pptx/slide_020_recreated.pptx` was MISSING from the workspace. Job:
regenerate the pptx from the existing banked build script and re-render it, then
verify. NO re-judge — the banked transcripts are the accepted verdicts.

## What was done

1. **Claimed** slide 20 as `regen-worker-020-139656` via
   `VIDEO=machine-learning/03_ridger_regression_gradient_descent
   python3 scripts/15_progress.py claim 20 <worker-id>`.
2. **Ran the existing build script as-is** — no edits, no asset restoration needed:
   ```bash
   cd /workspaces/codespaces-blank/ai_llm_slides \
   && NODE_PATH=$(npm root -g) node \
     videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_020.js
   ```
   Output: `wrote .../recreated_pptx/slide_020_recreated.pptx`.
   The script contains no equation/graph asset references (`verbatim_text.equations`
   is empty; no `build/assets/` dependency for this slide), so nothing had to be
   restored.
3. **Verified the zip**: `unzip -t` reports `No errors detected in compressed data`
   (40 entries, incl. `ppt/slides/slide1.xml` and `ppt/media/`).
4. **Re-rendered with a private LibreOffice profile** (TMPDIR redirected to project
   scratch `scratch/tmp`):
   ```bash
   soffice --headless -env:UserInstallation=file://$TMPDIR/lo_slide020 \
     --convert-to pdf --outdir $TMPDIR \
     videos/.../recreated_pptx/slide_020_recreated.pptx
   pdftoppm -png -r 150 $TMPDIR/slide_020_recreated.pdf $TMPDIR/slide
   cp $TMPDIR/slide-1.png recreated_pptx/qa/slide020/render_regen.png
   ```
   `render_1.png` (the 2026-10-19 certified render) was NOT overwritten.
5. **House chrome check** on the regenerated render:
   ```
   python3 videos/.../shared_patterns/house_chrome_check.py \
     videos/.../qa/slide020/render_regen.png 20
   ```
   Result: **HOUSE CHROME CHECK: PASS** (panel x 112-1882, y 94-bottom; strokes
   L/R/bottom present, top bare; badge center (1824,152) d=68; all within tol 8).
   The badge center/geometry match the certified `render_1.png` record in
   `worker_report.md` exactly (panel x 112-1882, badge center (1824,152) d=68).

## Judge verdicts (banked, NOT re-run — law: do not re-judge)

Verified present and readable (text transcripts only, never PNG bytes):

| Artifact | Path | Content |
|---|---|---|
| Full-slide comparison | `qa/slide020/judge_attempt_1.txt` | FINAL VERDICT: **PASS**, zero BLOCKER/MAJOR/MINOR discrepancies |
| Title crop pair | `qa/slide020/crop_1_title_judge.txt` | FINAL VERDICT: **PASS**, zero discrepancies |
| Badge crop pair | `qa/slide020/crop_1_badge_judge.txt` | FINAL VERDICT: **PASS**, one MINOR (numeral weight) PIL-refuted |
| Gateway probe | `qa/slide020/probe_1.txt` | valid body, window open |
| Judge prompts (banked verbatim) | `qa/slide020/judge_prompt_1.txt`, `crop_1_title_prompt.txt`, `crop_1_badge_prompt.txt` | Templates A/B from `judge_protocol_03.md` |
| Prior worker report | `qa/slide020/worker_report.md` | CERTIFIED PASS, `gen_status=passed`, no OMML wrap needed |

The badge MINOR ("numeral weight heavier in the recreation") was already
adjudicated PIL-first and refuted in the original worker run
(`adjudicate_badge_minor.py`): the numeral is this deck's founder-ratified house
chrome (bold Arial 18pt `333333`, drawn by the shared module), and the original's
strokes are JPEG/video ghosts at matched scale. Judge findings on chrome are
overridden by law. Not a fix trigger; no action taken.

## DB state

- `pptx_path` = `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_020_recreated.pptx` (re-confirmed after rebuild)
- `build_script` = `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_020.js` (re-confirmed)
- `gen_status` = `passed` (the row had regressed to `building`; restored to `passed`
  to match the banked certification + the now-present deliverable)
- `visual_check` = `PASS` (left as-is; the DB already carried PASS)
- `visual_attempts` = 3, `visual_transcript` unchanged
  (`qa/slide020/judge_attempt_1.txt`)
- `last_error` = null

Claim released: `VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py release 20 regen-worker-020-139656`.

## Deliverables in place

- `recreated_pptx/slide_020_recreated.pptx` — 48948 bytes, valid zip, single
  plain-named version (single-version law respected).
- `recreated_pptx/qa/slide020/render_regen.png` — 150dpi render of the regenerated
  pptx, house-chrome PASS.

## Environment / notes

- `export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp` used for the
  LibreOffice profile and scratch (never `/tmp`).
- Private LO profile `file://$TMPDIR/lo_slide020` (parallel-worker isolation).
- Build script unchanged: no geometry/content edits, no asset restore, no
  copy-then-modify needed (nothing was being changed).
- No banked evidence deleted; `render_1.png` preserved.
- OMML wrap: not applicable (slide has no equations) and not needed (this is a
  regeneration of the same build, not a content change).
