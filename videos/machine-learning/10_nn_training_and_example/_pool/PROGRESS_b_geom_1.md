# Lane G `b_geom_1` — geometry closed-loop progress (worker_b_geom_1)

Scope: slides 001, 004, 005, 006, 007 (10_nn_training_and_example)
Gateway-free: PIL/geometry only, no vision calls.

## Status (updated each session)

- [x] Scope claimed (`scope-claim _pool/mission.db b_geom_1 worker_b_geom_1` -> 1)
- [x] Official report path determined: `qa/slideNNN/geom_b_geom_1.md`
- [x] All 5 pptx rendered LO headless, PRIVATE profile `_pool/lo_geom_b_geom_1/<NNN>/`,
      TMPDIR `_pool/tmp_geom_b_geom_1/<NNN>/`, `pdftoppm -png -r 150`
      -> `qa/slideNNN/geom/render_NNN-1.png` (all 2001x1125)
- [x] 960x540 BOX-resampled renders: `_pool/tmp_geom_b_geom_1/frame_NNN.png`
- [x] Final measurement script: `_pool/geom_b_geom_1_final.py` (v1, direct frame coords)
      -> run complete, results in this session
- [x] Fine band probe: `_pool/geom_b_geom_1_fine.py` -> `_pool/fine_b_geom_1.txt`
- [x] Final measurement script v2 (slide-PAGE canonical):
      `_pool/geom_b_geom_1_v2.py` — runs the same ink mask but reduces each image
      to its own SLIDE PAGE first (original gray page / render full frame), which
      cancels all chrome differences. Running; output `_pool/v2_b_geom_1.txt`.
- [x] Report banked: `qa/slide001/geom_b_geom_1.md` (v1 numbers, to be
      rewritten with the v2 page-canonical numbers once v2 lands)

## Coordinate-system decision (key calibration)

Original frames are VIDEO CAPTURES: white margin, gray slide page
(x~53..907, y~42..517), the source deck's OWN red border rect
(x~57..902, y~42..517), own yellow badge (x~858..893, y~55..86), a mouse cursor
on 001, and a black letterbox (y 519..539). The render has DIFFERENT chrome
(house frame at 0.15in inset, house badge at 12.48/0.30in).

Two normalisation options were considered:
(a) map each image's own border rect onto a canonical 960x540;
(b) compare original frame px against render frame px in the shared 960x540
    frame, i.e. no re-normalisation.

`recreated_pptx/build/slide_001.js:123` uses option (b): it maps an
original-frame crop with `x = 588 / 960 * 13.33` and `y = 436 / 540 * 7.5`, so
the deck's own builders treat original frame px == slide frame px. Empirically
(b) also fits better: the yellow badge is 35 px wide in both frames, and the
original title band brackets the render title far more tightly than under (a).
=> FINAL: option (b). Both images are measured in the shared 960x540 frame.

## Pipeline per slide
`_pool/geom_b_geom_1_final.py` prints per image a band census
(y0,y1,x0,x1,px) plus a region table with deltas and verdicts.
Tolerance 2.0 px (~4px at 150dpi).

## Remaining
- [ ] Run `_pool/geom_b_geom_1_final.py` (background, running)
- [ ] Write `qa/slideNNN/geom_b_geom_1.md` per slide (measured boxes, deltas,
      explicit PASS / EXCEEDS-TOLERANCE per region)
- [ ] `scope-done _pool/mission.db b_geom_1 "<note>"`
- [ ] Park superseded probes in `_pool/orphans/` with a note
