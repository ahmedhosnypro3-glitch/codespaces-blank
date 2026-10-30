# Slide 035 Regeneration Report

**Date**: 2026-10-23
**Worker**: worker_slide035_regenerator
**Action**: Regenerate missing PPTX deliverable from existing banked build script

## Summary

The previously judge-certified PPTX for slide 035 (`slide_035_recreated.pptx`) was missing from the workspace. This report documents the regeneration from the existing build script and verification.

## Steps Performed

1. **Claimed slide 035** — DB claim via `15_progress.py claim 35 worker_slide035_regenerator`
2. **Ran existing build script** — `NODE_PATH=$(npm root -g) node videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_035.js`
   - Build succeeded: `wrote videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_035_recreated.pptx`
3. **Verified PPTX integrity** — `unzip -t`: No errors detected in compressed data
4. **Re-rendered with private LibreOffice profile**:
   - `soffice --headless -env:UserInstallation=file://$TMPDIR/lo_slide035 --convert-to pdf --outdir $TMPDIR ...`
   - `pdftoppm -png -r 150` → `qa/slide035/render_regen.png`
5. **House chrome check** — `python3 shared_patterns/house_chrome_check.py qa/slide035/render_regen.png 35`
   - **Result: PASS** (panel x 112-1882, y 94-bottom; strokes L/R/bottom present, top bare; badge center (1824,152) d=68; all within tol 8)
6. **Verified banked judge transcripts** — All transcripts present in `recreated_pptx/qa/slide035/`:
   - `judge_attempt_1.txt` — Full-slide verdict: **PASS**
   - `crop_1_title_judge.txt` — Zoomed title crop: **PASS**
   - `crop_1_sub_judge.txt` — Zoomed subtitle crop: **PASS**
   - Plus supporting artifacts (renders, probes, payloads, worker report)
7. **Released claim** — `15_progress.py release 35 worker_slide035_regenerator`

## DB State After Regeneration

| Field | Value |
|-------|-------|
| gen_status | passed (implicitly, visual_check=PASS and pptx_path valid) |
| visual_check | PASS |
| pptx_path | videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_035_recreated.pptx |
| build_script | videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_035.js |
| visual_transcript | videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide035/judge_attempt_1.txt |

## Banked Judge Transcripts (Verified)

| File | Verdict |
|------|---------|
| `judge_attempt_1.txt` | PASS — Full-slide comparison, no blockers/majors/minors |
| `crop_1_title_judge.txt` | PASS — Title block glyph-for-glyph match |
| `crop_1_sub_judge.txt` | PASS — Subtitle glyph-for-glyph match, parentheses intact |

## Notes

- No geometry/content changes made — the existing build script was run as-is.
- No re-judging performed — the banked judge transcripts from the original certification (2026-10-19) remain the accepted verdicts.
- House chrome uses the deck-specific template (white canvas + gray panel + red L/R/bottom strokes + yellow badge with purple ring), measured from slide_003.jpg and verified constant across reference frames.

## Deliverable

**PPTX**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_035_recreated.pptx` (49,553 bytes, valid zip)
**Render**: `qa/slide035/render_regen.png` (59,007 bytes, 150dpi PNG)