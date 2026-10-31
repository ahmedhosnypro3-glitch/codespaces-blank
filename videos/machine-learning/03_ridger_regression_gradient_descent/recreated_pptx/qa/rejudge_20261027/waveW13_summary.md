# Wave W13 summary — slide 042 CROP-gap closure (2026-10-31)

Leg-launcher wave W13. Gap per `VERDICT_CENSUS_r1.md`: slide 042 was the ONLY slide
missing a clean CROP verdict (FULL already PASS via `fresh_042.out` 2026-10-31T08:43:06Z).
No git, no DB/pptx writes, no evidence deleted. All paths under
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/`.

## Inputs

- Deliverable md5: `slide_042_recreated.pptx` = `e3c8f38013575843ccedba7fd550928a`
  (mtime 2026-10-27 16:24:23Z, unchanged; recorded in `slide042/w13/md5_w13.txt`).
- Fresh render: `slide042/render_w13.png` (2001x1125) from unique-profile soffice
  (`-env:UserInstallation=file:///home/codespace/ai_llm_slides/scratch/tmp/lo_w13_042`,
  TMPDIR=`/home/codespace/ai_llm_slides/scratch/tmp`) + `pdftoppm -png -r 150 -singlefile`;
  PDF kept at `slide042/w13/slide_042_recreated.pdf`, log `slide042/w13/render_w13_soffice.log`.
- Crop pair per `fresh_leg_chain.sh` method: `pick_dense_region.py 042` -> region
  `60 88 344 296` (960x540 frame space) -> `slide042/crop_dense_render_w13.png` +
  `slide042/crop_dense_orig_w13.png` (592x434 each, render scale 1125/540).

## Legs launched (one bash call from repo root, setsid nohup, ending with wait)

- CROP: `vision_leg.sh slide042/crop_dense_judge_w13.txt 600 crop_dense_render_w13.png
  crop_dense_orig_w13.png "Slide 042 dense crop W13" "crop pair app render" payload_B_025.txt`
  (OCC_MAX=700 ATTEMPTS=12). Note: `payload_B_025.txt` is byte-identical to
  `payload_B_042.txt` modulo the slide number; used as instructed.
- FULL: `vision_leg.sh slide042/judge_full_w13.txt 1200 render_w13.png
  unique_slides/slide_042.jpg "Slide 042 recreation — fidelity check vs original lecture frame W13"
  "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" payload_A.txt`
  (OCC_MAX=700 ATTEMPTS=12).
- Launcher pid 2848092; leg pids 2848098 (crop), 2848099 (full); started 2026-10-31T09:01Z.

## Verdicts (filled in when legs return)

- CROP `crop_dense_judge_w13.txt`: PENDING
- FULL `judge_full_w13.txt`: PENDING

## Census note

Pending leg completion: if `crop_dense_judge_w13.txt` returns a clean (no-429)
`FINAL VERDICT`, the VERDICT_CENSUS_r1 gap list `(42, 'CROP')` is closed — 51/51 slides
then have a clean CROP verdict.
