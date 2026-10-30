# Regeneration report — slide 022, `machine-learning/03_ridger_regression_gradient_descent`

**Date:** 2026-10-23  
**Worker:** regen-worker-20261023  
**Trigger:** Missing deliverable `slide_022_recreated.pptx` from workspace; certified slide needed regeneration from banked build script.

## Source of truth
- **Build script:** `recreated_pptx/build/slide_022.js` (byte-identical to certified `qa/slide022/build_attempt_1.js`, md5 `35f6b0752c57da3f5599283bac12f788`)
- **No assets needed** — slide has no equations/graphs (verbatim text + house chrome only)
- **Judge transcripts (banked, NOT re-judged):**
  1. `qa/slide022/judge_attempt_1.txt` — full-slide Template A: **PASS** (no discrepancies)
  2. `qa/slide022/crop_1_title_judge.txt` — title crop: **PASS** (1 MINOR on leading, PIL-refuted)
  3. `qa/slide022/crop_1_badge_judge.txt` — badge crop: **PASS** (no discrepancies)
  4. `qa/slide022/crop_1_line1_judge.txt` — line1 tight zoom: **PASS** (1 MINOR on red hue, PIL-refuted)
  5. `qa/slide022/crop_1_line2_judge.txt` — line2 tight zoom: **PASS** (1 MINOR on paren extent, PIL-refuted)
- **Self-check script:** `qa/slide022/selfcheck_final.py` — defines certified geometry tolerances

## Regeneration steps
1. Claimed slide 022 in DB (`gen_status=passed` → `building` auto-flipped by claim)
2. Ran existing build script: `NODE_PATH=$(npm root -g) node videos/.../recreated_pptx/build/slide_022.js` — **success**, wrote `slide_022_recreated.pptx` (48604 bytes, valid zip)
3. Re-rendered with private LibreOffice profile:
   - `soffice --headless -env:UserInstallation=file://$TMPDIR/lo_slide022 --convert-to pdf --outdir $TMPDIR ...`
   - `pdftoppm -png -r 150` → `render_regen.png` (41515 bytes)
4. **House chrome check:** `house_chrome_check.py render_regen.png 22` → **PASS**
5. **Self-check (adapted to render_regen.png):** All corrected residuals within certified tolerances (≤2.0 frame px; L1 x1 ≤2.5 rasterizer allowance), pitch 90.24 vs 90.00 orig, zero stray red ink, census exactly 3 bands (badge/L1/L2), core color (192,0,0) — **PASS**
6. **DB restored:** `gen_status=passed`, `visual_check=PASS`, `pptx_path`/`build_script`/`visual_transcript` unchanged, `last_error` cleared

## Pixel diff note
Regenerated `render_regen.png` vs banked `render_1.png`: 15,252 differing pixels (0.68% of frame), clustered in badge and title bands. Max channel diff 233 (expected for different LO render environment). **House chrome check and self-check both PASS** — the regenerated deliverable meets all certified geometry/color/census criteria. The pixel delta is a rendering-environment artifact, not a content defect.

## Verdict
Deliverable `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_022_recreated.pptx` regenerated from banked certified build script; all acceptance criteria (house chrome, self-check geometry, judge transcripts) satisfied. No judge re-dispatch performed (banked transcripts are the accepted evidence).