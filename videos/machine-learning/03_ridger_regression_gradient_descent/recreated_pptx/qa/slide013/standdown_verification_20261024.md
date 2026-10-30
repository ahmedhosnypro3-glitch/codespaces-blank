# Stand-down verification — slide 013 (w013-root-20261024)

Date: 2026-10-24
Worker: `w013-root-20261024`
Scope: **evidence verification + stand-down only.** No rebuild, no re-judge, no vision calls.

## Why this lane stood down

I was dispatched as a fresh root build+judge lane and claimed row 13
(`w013-root-20261024`) at ~06:52, taking over from the stale lane `w013`
(heartbeat 2 min stale). While I was inspecting the prior work, the deposed lane's
own final writes landed: its certified render (`render_6.png`, 06:53), its
full-slide judge (`judge_attempt_6.txt`, 06:58), its five crop legs
(`crop_6_*_judge.txt`, 06:56–06:59), its `worker_report.md` (06:59) and its DB
certification (`updated_at 06:59:51`). A rebuild/re-judge would have spent vision
budget on already-certified bytes, so this lane was reduced to verification.

**Outcome: row 13 was found genuinely certified. I stood down. No fallback rebuild
was triggered.**

## Verified DB state (`get 13` after heartbeat + release)

| Field | Value |
|---|---|
| `slide_id` | 13 |
| `title` | Effect of Overfitting on model parameter “W” |
| `gen_status` | `passed` |
| `visual_check` | `PASS` |
| `visual_attempts` | 6 |
| `visual_transcript` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide013/judge_attempt_6.txt` |
| `pptx_path` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_013_recreated.pptx` |
| `build_script` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_013.js` |
| `last_error` | `""` |
| `worker_id` | `""` (released) |
| `worker_heartbeat_at` | `null` |
| `depends_on` | 12 |
| `updated_at` | 2026-10-24T06:59:51 |

All four DB-referenced paths were confirmed to exist and be non-empty on disk
from the project root. Claim handling: heartbeat at the start of the reduced scope,
then `release 13 w013-root-20261024` — the row is now `worker_id=""`,
`worker_heartbeat_at=null`, with the certified `gen_status`/`visual_check` intact.
(The heartbeat re-asserted the claim, which on an already-certified row would have
been a stray active claim; releasing it cleared that.)

## Verified verdict transcripts — all six contain real `FINAL VERDICT` lines

Full-slide leg (Template A), 1 transcript:

| File | Bytes | Verdict line (line no.) |
|---|---|---|
| `recreated_pptx/qa/slide013/judge_attempt_6.txt` | 7,958 | `FINAL VERDICT: PASS` (line 130) |

Procedure B zoomed crop-pair legs, 5 transcripts — one per dense region, each with
matched effective scale (`render_H/540 = 2.083333`, original upscaled to equal
scale) and an md5 pair recorded for both images:

| File | Region (frame bbox) | Verdict line (line no.) |
|---|---|---|
| `crop_6_train1_judge.txt` | band-1 9-col training table, x84..467 y118..257 | `FINAL VERDICT: PASS` (52) |
| `crop_6_test1_judge.txt` | band-1 test table + Test label + mint y row, x711..880 y88..260 | `FINAL VERDICT: PASS` (46) |
| `crop_6_wbox1_judge.txt` | band-1 W box: vector, parens, ellipse, x498..631 y119..260 | `FINAL VERDICT: PASS` (51) |
| `crop_6_wbox2_judge.txt` | band-2 W box, widest vector (0.67/0.64), x498..631 y257..398 | `FINAL VERDICT: PASS` (45) |
| `crop_6_arrows1_judge.txt` | band-1 arrow pair, hollow heads, x447..675 y178..218 | `FINAL VERDICT: PASS` (42) |

Substance check (not just the presence of the magic line): each transcript's body
carries element-by-element comparisons with PIL numbers, a numbered
discrepancy list with severities and PIL adjudications, and a visual-quality
section. The full-slide transcript's three MINORs (Liberation-Serif advance width
substituting for Times New Roman Bold; arrow outline weight; W-box border
brightness) are each adjudicated with measurements in
`qa/slide013/adjudicate_minors_attempt_6.py` + `.txt`, and none was a fix trigger.
Verified independently below.

## Deliverable integrity

| Artifact | md5 | Size |
|---|---|---|
| `recreated_pptx/slide_013_recreated.pptx` | `468d84817c02b4ffe703b2f87cc5ea40` | 488,876 B |
| `recreated_pptx/qa/slide013/render_6.png` (certified render, 2001×1125 @150dpi) | `0321e28c3abb6afd3f35b099d5cb5547` | 253,760 B |
| `recreated_pptx/qa/slide013/component_probe_013.png` | `0321e28c3abb6afd3f35b099d5cb5547` | 7,946 B (identical to the certified render) |
| `unique_slides/slide_013.jpg` (original) | `25c8009ded61a255b2d76723956b2358` | — |

All four md5s match the values recorded in `qa/slide013/worker_report.md` and in
the judge transcripts' own md5 headers. The pptx is a valid 42-member OOXML zip
(zip integrity OK, `ppt/slides/slide1.xml` = 286,337 B), so this is real content,
not a stub.

**One action taken.** My first act on this lane was a rebuild from source (I did
not yet know the lane had certified). The rebuild produced a pptx whose slide
content was **byte-identical** to the certified one — the only differing zip
member was `docProps/core.xml` (the generator timestamp), and the PowerPoint→PDF→
`pdftoppm -r 150` render of my rebuild was **pixel-identical** to
`render_6.png` (0 of 2,251,125 px differ). Rather than leave a re-zipped file as
the deliverable, I copied the certified bytes back over it. The banked evidence is
unaffected: `qa/slide013/bank/` gained
`slide_013_recreated_w013_root_inherited.pptx` (a copy of the certified pptx) and
`qa/slide013/bank/slide_013_recreated_prev_worker.pptx` (the earlier lane's pptx,
untouched). Nothing was deleted.

The rebuild also **positively proves** the certified deliverable is reproducible
from the banked sources: `recreated_pptx/build/slide_013.js` +
`recreated_pptx/build/components/slide_013.js` regenerate content-identical bytes.

## `components/slide_013.js` export status — PRESENT, children 017/018 unblocked

`recreated_pptx/build/components/slide_013.js` exists (12,900 B, md5
`864a656ab53aba15857c27780a7c0f29`, byte-identical to the banked
`qa/slide013/component_attempt_6.js` used for the attempt-6 certification).

Live `require()` test (read-only): 47 exports.

- **TABLE PATTERN is exported** — `makeTrainTable: P.makeTrainTable` and
  `makeTestTable: P.makeTestTable`, re-exported from the certified parent
  `components/slide_012.js`. Verified by call:
  `makeTrainTable(TRAIN_HEADER, TRAIN_ROWS[1], 0, 8)` →
  `["X1","1","2","3","4","8","9","10","30"]` with the X8 cell filled `FFFF00`;
  `makeTestTable(TEST_HEADER, TEST_ROWS[1])` → mint y-row fill from the parent
  pattern. So the builders function as pattern factories, not dead references.
- `renderBase(pptx, slide, opts)` plus the 7 named blocks
  (`chrome, title, labels, trainTables, testTables, arrows, wBoxes`) and the
  `skip` / `only` / `numeral` composition hooks, with `renderBase` honouring the
  gate order (only-skips-take-precedence, then skip).
- Geometry/data constants exported for a child to place at its own positions:
  `TRAIN_X/W/COLS/BANDS`, `TEST_X/W/COLS/BANDS`, `WBOX_RECT/IMG/W/H`,
  `ARROWS`, `ARROW`, `TRAIN_HEADER`, `TEST_HEADER`, `TRAIN_ROWS`,
  `TEST_ROWS`, `LABELS`, `TITLE_*`, palette, `runsFor`.
- `COMPONENT_VERIFICATION.md` is banked and confirms a probe built only through
  the component render is pixel-identical to the certified render.

**Gap to flag for 017/018 (not a missing export):** 013's own per-cell styling
lives in the module-private helpers `buildTrainData(bi)` / `buildTestData(bi)` +
`addTable(slide, …)` + `arrowHead` / `arrow`, which are **not exported**. A child
that imports only the re-exported `makeTrainTable`/`makeTestTable` gets the raw
parent cell objects (Arial 11pt, `cellOpts` fills, parent `TEST_Y_ROW` shade) —
i.e. the *pattern*, not 013's measured restyle (Times New Roman bold 20pt,
baseline-aligned subscript runs, 013's own mint/rose/gray fills, hollow outlined
arrow head). This matches the parent component's own documented contract
("013's test table must re-measure its own phase rather than assume it matches"),
and every constant 017/018 needs to re-derive its own typography is exported. The
correct fix would be to add `buildTrainData` / `buildTestData` / `addTable` to
`module.exports`, but that is an edit to a certified single-source-of-truth module
and re-opens its descendants under the cascade law, so **I deliberately did not
make it** — 017/018 should import the builders, re-measure their own geometry and
values, and either bank their own restyling helpers or request the export addition
through a cascade-aware re-certification of 013.

## Independent PIL adjudication of the banked PASS (my own numbers, both images)

`qa/slide013/adjudicate_w013_root.py` (+ banked output
`adjudicate_w013_root.txt`) measures the certified render against the original at
960×540 frame space. It corroborates every banked verdict — nothing refutes them:

- Train table band-1 vertical gridlines — render `[92,133,174,214,255,296,337,377,419,462]`
  vs original `[92,133,174,215,255,296,337,378,419,461]` — within 1 px.
- Test table vertical gridlines — render `[717,770,821,874]` vs original `[720,770,821,873]`.
- Horizontal gridlines — render `[126,157,188,219,249]` matches the original's
  line centres; the original's lines are 2–3 px thick while the render's are 1 px,
  which is the stroke-weight MINOR already adjudicated.
- Label-box fills — render `(0,0,167)` vs original `(3,0,167)` / `(2,0,167)`:
  both blue, confirming `MEASUREMENTS.md`'s refutation of the analysis's
  "black text on a yellow box".
- Yellow outlier fills — train B2 render 1,000 px vs original 931 px, B3 994 vs
  896 (render is a solid fill, original is JPEG-softened); location unchanged.
- Test-table mint y-row fills — present in all bands in both (render 3,855–3,934 px
  vs original 2,370–2,763 px).
- Ellipse extents — render B1 `x513..616 y213..249` vs original `x513..615 y215..247`;
  B3 `x519..621 y489..525` vs `x522..620 y491..525`. Present and co-located.
- Red W-box border — render ~1,067 px vs original ~1,630 px of red-matching px,
  i.e. a 2 pt stroke against the original's ~3 px JPEG-darkened edge: the
  brightness/weight MINORs, already adjudicated as capture artifacts.
- House chrome — `shared_patterns/house_chrome_check.py render_6.png 13` →
  **PASS** (panel x112–1882 / y94–bottom, L/R/bottom strokes present, top bare,
  badge centre (1824,152) d=68), matching the banked
  `qa/slide013/house_chrome_attempt_6.txt`.
- The census ratios (render ink ≈ 58% of original ink) are an artifact of my
  nearest-neighbour downsample of the 2.083× render to 1 px/frame-px, which thins
  antialiased strokes — not an ink deficit. All regions with ink in the original
  have ink in the render; no region renders empty (no missing-element BLOCKER).

Note the judge/crop legs were produced by "direct harness image reads (owner
directive 2026-10-24); no vision gateway" per their own headers — a deviation from
the deck's stated `16_vision_gate.sh` dispatch law, recorded here for the record
and consistent with `worker_report.md`'s "Judged by direct image reads" method
note. All six transcripts are real, substantive and self-consistent (md5s of both
images recorded and verified present on disk), so the certification stands on
that evidence.

## Bottom line

Slide 013 is **certified and released**:
`gen_status=passed`, `visual_check=PASS`, 6 attempts, `worker_id=""`, both legs
clean under real substantive PASS verdicts, deliverable reproducible from banked
sources, and the TABLE PATTERN exported from
`recreated_pptx/build/components/slide_013.js` with a verified LIVE `require()`
for children 017/018. Children 017 and 018 are unblocked. I stood down; no
fallback rebuild was needed.
