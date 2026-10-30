# Regen Report — Slide 038 (machine-learning/03_ridger_regression_gradient_descent)

Slide id: 38 — "Gradient Descent (GD) vs Stochastic Gradient Descent (SGD)"

## Purpose

The banked build script existed and its judge verdicts were certified
(visual_check=PASS), but the single plain-named deliverable
`recreated_pptx/slide_038_recreated.pptx` was MISSING from the workspace. This
run regenerated the deliverable from the existing banked build script and
re-rendered it. **No re-judge was performed** — the banked judge transcripts in
`recreated_pptx/qa/slide038/` are the accepted verdicts.

## Steps performed

1. Claimed slide 38 via `scripts/15_progress.py claim 38 <worker_id>` with
   VIDEO=machine-learning/03_ridger_regression_gradient_descent. Heartbeats
   issued. Claim RELEASED at completion.
2. Ran the banked build script UNMODIFIED, exactly as documented in its header:
   `NODE_PATH=$(npm root -g) node videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_038.js`
   Result: `slide_038_recreated.pptx written`. No missing assets; no geometry or
   content changes made; no `last_error` recorded.
3. Verified the deliverable exists and is a valid zip (`unzip -t`): all 38
   entries OK, no CRC errors. Size 50119 bytes.
4. Re-rendered with a PRIVATE LibreOffice profile:
   `soffice --headless -env:UserInstallation=file://$TMPDIR/lo_slide038
   --convert-to pdf --outdir $TMPDIR .../slide_038_recreated.pptx`
   then `pdftoppm -png -r 150`, copied to `qa/slide038/render_regen.png`
   (63244 bytes, single page).
5. Ran the house-chrome checker on the regenerated render.

## House chrome check result

`python3 videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/house_chrome_check.py qa/slide038/render_regen.png 38`

```
HOUSE CHROME CHECK: PASS
(panel x 112-1882, y 94-bottom; strokes L/R/bottom present, top bare;
 badge center (1824,152) d=68; all within tol 8)
```

Note: this run also banks a copy of the render at the project root
`qa/slide038/render_regen.png` (per the worker instruction's stated path),
in addition to the render inside the namespace's QA tree.

## Banked judge transcripts verified (not re-run)

Located in
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide038/`:

- `judge_attempt_1.txt` — full-slide comparison judge — **FINAL VERDICT: PASS**
- `crop_1_badge_judge.txt` — zoomed badge crop judge — **FINAL VERDICT: PASS**
- `crop_1_title_l1l2_judge.txt` — zoomed title lines 1/2 crop judge — **FINAL VERDICT: PASS**
- `crop_1_title_l3_judge.txt` — zoomed title line 3 crop judge — **FINAL VERDICT: PASS**

Both certification requirements of the deck AGENTS.md are satisfied by the
banked records: full-slide judge + at least one zoomed crop-pair certificate
per dense region (badge and each title region).

Supporting banked evidence also present (untouched): `build_attempt_1.js`,
`render_1..3.png`, `selfcheck_attempt_1/2.out|.py`, `probe_1.txt`,
`judge_prompt_1.txt`, `adjudicate_attempt_1.out|.py`, `cut_crops.py`,
`bank_prompts.py`, `crop_1_*_orig.png` / `crop_1_*_render.png`,
`worker_report.md`, `INCIDENT_stray_db_write.md`.

## DB state

The slide's row retains `gen_status=passed` and `visual_check=PASS`;
`pptx_path` and `build_script` were updated to point at the regenerated
deliverable and the banked build script respectively. The claim was released.

## Left in-progress / follow-ups

None. Deliverable present, valid, re-rendered, house-chrome PASS. No judge
finding was reopened, so no re-certification is required.
