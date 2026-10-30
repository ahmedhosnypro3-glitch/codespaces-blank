# Worker report — slide 013 ("Effect of Overfitting on model parameter “W”")

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Worker: w013 (pool run 859463) · Date: 2026-10-24 · Verdict: **PASS (attempt 6)**

## Status

- Scope: slide 013 only. Dependency edge 13 > 12 honoured: the build imports the
  certified parent component `build/components/slide_012.js` (table PATTERN:
  `makeTrainTable` / `makeTestTable` + the alternating blue/red ink rule) and
  redraws it at 013's own PIL-measured geometry (train x92..459 vs 012 x203..571,
  test x719..872, three rows of Train table | W box | test table).
- Deliverable: `recreated_pptx/slide_013_recreated.pptx` (single plain-named
  version), md5 `468d84817c02b4ffe703b2f87cc5ea40`.
- Build script: `recreated_pptx/build/slide_013.js` (writer) →
  component `recreated_pptx/build/components/slide_013.js` (composition).
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=6`,
  `visual_transcript=.../judge_attempt_6.txt`, `pptx_path`, `build_script`,
  `last_error=""`.

## Resume point

The previous worker left an unproven build + `qa/slide013/render/render_1..3-1.png`
and no judge transcripts. Those renders are untouched (banked); the pre-existing
pptx is preserved as `qa/slide013/bank/slide_013_recreated_prev_worker.pptx`
(md5 6b021a9f5710ad254ce1f5bf983104c2). Attempt numbering continued from the
highest banked render (3), so this worker's calibrated renders are 4 and 5 and
the certified render is 6. The previous live build script was superseded by the
new component-based one; its measured geometry/values dossier is preserved in
`qa/slide013/MEASUREMENTS.md` + `dump_*.py` scripts.

## Attempts

| K | what | verdict |
|---|---|---|
| 4 | first full rewrite (parent import, Times tables, W images v1, outlined arrow probe) | not judged — calibration; defects found by PIL: subscript descent too deep, blue row-label column (frame is black), solid arrow heads (frame heads are hollow), test header wrap risk |
| 5 | subscripts baseline-aligned, black row labels, header left-align, hollow arrow heads, mathtext W | not judged — calibration; test header still wrapped in the 51px column, W glyph too wide |
| 6 | test-header margins tightened, W glyph redrawn as STIX math italic 21pt with underline | **PASS both legs** |

Attempts used in the judge ledger: 6 (renders 1–3 banked from the previous
worker, 4–5 calibration builds, 6 certified).

## Verdicts (direct image reads; owner directive 2026-10-24 — no vision gateway)

Full-slide: `qa/slide013/judge_attempt_6.txt` → FINAL VERDICT: PASS.
Zero BLOCKER/MAJOR. MINORs: font-advance width (Liberation Serif Bold substitute
for Times New Roman Bold — heights match within 0.5px, no cell overflow), arrow
outline weight (JPEG-blur adjudicated), W-box border brightness (JPEG chroma) —
all PIL-adjudicated in `qa/slide013/adjudicate_minors_attempt_6.txt`.

Crop legs (Procedure B, matched effective scale = render_H/540 = 2.083333):
- `crop_6_wbox1_judge.txt` — band-1 vector/parens/ellipse → PASS
- `crop_6_wbox2_judge.txt` — band-2 widest vector (0.67/0.64) → PASS
- `crop_6_train1_judge.txt` — 9-col training table, headers + all rows → PASS
- `crop_6_test1_judge.txt` — test table + Test label + mint y row → PASS
- `crop_6_arrows1_judge.txt` — arrow pair geometry/hollow heads → PASS

## Pre-judge selfcheck (banked numbers)

`qa/slide013/selfcheck_attempt_6.py` + `.txt` → RESULT: PASS. Covers frame
containment (all blocks), equation ink (3 vectors + 3 ellipse texts),
delimiter geometry (parens span digits, 2.6–3.6px clearance), table gridlines
(exact), table data verbatim (build data == analysis spec, every cell has ink),
single-line/no-wrap checks, crop-scale audit, and
`shared_patterns/house_chrome_check.py` PASS (`qa/slide013/house_chrome_attempt_6.txt`).

## Fixes applied (attempt 4→6)

1. Rebuilt the table pattern on 013's measured geometry; Times New Roman bold
   20pt (header/body heights match the frame's 13-14px digits), left-aligned
   train headers, centered data cells, black row-label column, real baseline-
   aligned index digits (X₁…X₈, Test₁…Test₃).
2. Test y-row mint fill `CCFFE1` on all bands; rose test borders `D7BEC2`;
   gray train borders `CED0CD`; RED/BLUE/RED test ink phase (frame-measured;
   the inherited dossier note "all red" was wrong).
3. W boxes: red-bordered white rect + 600-dpi transparent math image per band
   (`build/assets/make_013_wbox.py` → `wbox_band{1,2,3}.png`): red italic W with
   underline, black "=" bars, thin parentheses spanning all three values,
   pale-yellow `FBFF85` ellipse with olive `||W||² = …` (real superscript).
4. Arrows: hollow shaft + tail bar + HOLLOW outlined head (the frame's head
   interior is white), custGeom triangle outline, measured 464..503 / 627..665.
5. Title 30pt Arial bold `C00000` at x154 y62 (ink 155.8..791.9 × 68.4..95.8 vs
   frame 156..787 × 69..96).

## md5s

- render (certified): `qa/slide013/render_6.png` — 0321e28c3abb6afd3f35b099d5cb5547
- pptx: `recreated_pptx/slide_013_recreated.pptx` — 468d84817c02b4ffe703b2f87cc5ea40
- component probe render: `qa/slide013/component_probe_013.png` —
  0321e28c3abb6afd3f35b099d5cb5547 (pixel-identical to the certified render)
- original frame: `unique_slides/slide_013.jpg` — 25c8009ded61a255b2d76723956b2358

## Component export (slide 017 dependency)

`recreated_pptx/build/components/slide_013.js` — `renderBase(pptx, slide, opts)`
+ per-block exports + data/geometry exports + re-exported parent table builders.
Verified in `qa/slide013/COMPONENT_VERIFICATION.md`: a probe deck built ONLY
through the component render is pixel-identical to the certified render.

## Residual debt

- Times New Roman is not installed on this host; LibreOffice substitutes
  Liberation Serif, which draws the same heights but ~0.5–2.8px wider advances
  than the lecture's font (PIL-measured, no layout consequence).
- The arrow outline is 1.5pt vs the frame's ~2px core (JPEG-blur band).

## Stand-down verification (2026-10-24, worker `w013-root-20261024`)

Full record: `qa/slide013/standdown_verification_20261024.md`. Summary:

- Row 13 verified already certified (`gen_status=passed`, `visual_check=PASS`,
  `visual_attempts=6`, `worker_id=""`); stood down — no rebuild, no re-judge.
- All six verdict transcripts re-read and confirmed to carry real
  `FINAL VERDICT: PASS` lines: `judge_attempt_6.txt` (130) plus
  `crop_6_train1_judge.txt` (52), `crop_6_test1_judge.txt` (46),
  `crop_6_wbox1_judge.txt` (51), `crop_6_wbox2_judge.txt` (45),
  `crop_6_arrows1_judge.txt` (42).
- Deliverable restored to the certified bytes recorded above
  (`468d84817c02b4ffe703b2f87cc5ea40`). The verification lane's rebuild proved the
  deliverable is reproducible from the banked sources (slide XML byte-identical;
  only `docProps/core.xml` differed; its render was pixel-identical to
  `render_6.png`).
- `components/slide_013.js` verified live via `require()`: 47 exports,
  `renderBase` + 7 blocks + `skip`/`only`/`numeral` hooks, and the TABLE PATTERN
  (`makeTrainTable` / `makeTestTable`) re-exported from `components/slide_012.js`
  and confirmed callable. **Children 017/018 are unblocked.**
- Flagged for 017/018: `buildTrainData` / `buildTestData` / `addTable` (013's own
  measured cell restyle: Times bold 20pt, baseline-aligned subscript runs,
  mint/rose/gray fills, hollow outlined arrow head) are module-private and NOT
  exported; importing the builders yields the parent's raw cells, so a child must
  re-measure and restyle itself. Deliberately not patched (cascade law).
- New banked evidence: `standdown_verification_20261024.md`,
  `adjudicate_w013_root.py` + `.txt` (independent PIL adjudication harness, whose
  numbers corroborate every banked verdict),
  `bank/slide_013_recreated_w013_root_inherited.pptx`.
