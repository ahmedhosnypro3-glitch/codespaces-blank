# bl_verify_r1 — PIL verification of candidate BL assets, slide 025 (deck 03)

- NS: `videos/machine-learning/03_ridger_regression_gradient_descent`
- Work dir: `recreated_pptx/qa/rejudge_20261027/slide025` (`$W`)
- Baseline (current build): `recreated_pptx/build/assets/plot_025_bl.png` md5 `7a8e7210f118b728245d268552a7d32d` (1220x987)
- Watched candidate dirs: `assets_k17r/`, `assets_k17s/`, `assets_k17t3/` (poll 60 s, up to 90 min)
- Transform (task spec): `s = asset_width / 411`, origin frame (60, 296); `asset = (frame - origin) * s`
- Ground truth (frame px): labels Global Maxima x242..268 y304..319, Local Maxima x286..315 y337..352,
  Local Minima x286..311 y390..399, Global Minima x145..201 y439..465; red X at (199,445),(270,482);
  red hline y418 x124..381; red rect x80..472 y292..527
- Thresholds: C1 ink density > 0.010 (dark lum<100) per label box; C2 >=8 red px in +-12 asset px
  window per marker and 0 red px in label boxes; C3 hline red col coverage > 0.80 over x124..381 at y418+-2;
  C4 changed-px fraction < 0.08 vs baseline; C5 ink row height in [0.5x,1.5x] of 15 frame px * s
- Red mask: r>110, r-g>50, r-b>50. Diff: |delta|>10 on any channel.

| candidate | md5 | size | C1 ink | C2 markers/collision | C3 hline | C4 diff | C5 text h | VERDICT |
|---|---|---|---|---|---|---|---|---|
| baseline_selfcheck | 7a8e7210 | 1220x987 | C1 FAIL (dens 0.001,0.012,0.076,0.040) | C2 X FAIL (0,0) coll FAIL (redpx 168) | C3 0.25 FAIL | C4 0.0000 PASS | C5 h 3,33,30,81 FAIL | **FAIL** |

## Per-candidate detail

### candidate baseline_selfcheck — plot_025_bl.png
- path: /home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/plot_025_bl.png
- md5: 7a8e7210f118b728245d268552a7d32d  size: 1220x987  scale s=2.9684  verified: 2026-10-31T09:00:41
- C1 ink density (>0.010) per label box:
  - Global Maxima frame x242..268 y304..319 -> asset x540..621 y23..72  ink=0.0013  MISSING
  - Local Maxima  frame x286..315 y337..352 -> asset x670..760 y121..170  ink=0.0120  OK
  - Local Minima  frame x286..311 y390..399 -> asset x670..749 y279..309  ink=0.0759  OK
  - Global Minima frame x145..201 y439..465 -> asset x252..422 y424..505  ink=0.0402  OK
  C1: FAIL
- C2 red X markers (>=8 red px in +-12 asset px window):
  - frame (199,445) -> asset (412,442)  red_px=0  MISSING
  - frame (270,482) -> asset (623,552)  red_px=0  MISSING
  C2 markers: FAIL | C2 collision (red px inside label boxes [0, 0, 168, 0]): FAIL
- C3 red hline y418 x124..381 -> asset x189..956 y356..372  col_coverage=0.253 (thr 0.80): FAIL
- C4 diff vs baseline 7a8e7210 (same size): changed=0.0000 (<0.08) outside-annotation=0.0000  PASS
- C5 text height (expect ~44.5 asset px = 15 frame px * s):
  - Global Maxima measured=3 px  expected=44.5  OFF
  - Local Maxima  measured=33 px  expected=44.5  OK
  - Local Minima  measured=30 px  expected=44.5  OK
  - Global Minima measured=81 px  expected=44.5  OFF
  C5: FAIL
**VERDICT: FAIL**


## Original-side transcription (bl_labels_leg.txt)

Not landed yet.

-- last update: 2026-10-31T09:00:42 --
