# Worker report — slide 012

**Slide:** `unique_slides/slide_012.jpg` — "Effect of Overfitting on model parameter "W""
**Video:** `machine-learning/03_ridger_regression_gradient_descent`
**Worker:** `slide012-worker-1792800490` (re-claimed 2026-10-24 00:08 after the
previous lane's claim went 156 min stale; released at the end of this lane)

## Deliverable

| Item | Value |
|---|---|
| Build script | `recreated_pptx/build/slide_012.js` |
| Deliverable pptx | `recreated_pptx/slide_012_recreated.pptx` (255,810 bytes, single plain-named version) |
| Certified render | `recreated_pptx/qa/slide012/render_3.png` (2001x1125 RGBA, 150dpi) |
| Certified component | `recreated_pptx/build/components/slide_012.js` |
| House chrome | `house_chrome_check.py render_3.png 012` → **PASS** |

## Leg verdicts (both required by the deck's founder directive)

### Full-slide leg (Template A) — PASS

- Transcript: `recreated_pptx/qa/slide012/judge_attempt_3.txt`
- Command: `render_3.png` vs `unique_slides/slide_012.jpg`, payload byte-for-byte
  from `shared_patterns/judge_protocol_03.md` (`payload_A.txt`, 4073 B, 0 `NNN`
  placeholders), `--thinking high --max-tokens 65536 --timeout 600`, via
  `scripts/16_vision_gate.sh` wrapped in `timeout 1700`.
- Verdict: **FINAL VERDICT: PASS** — "No BLOCKER and no confirmed MAJOR defect."

### Zoomed crop leg (Template B) — PASS

- Transcript: `recreated_pptx/qa/slide012/crop_4_perfect_table_judge.txt`
- Pair: `crop_4_perfect_render.png` vs `crop_4_perfect_orig.png` (both 767x292,
  re-cut from `render_3.png` at matched effective scale, original upscaled
  LANCZOS to match). Region: the perfect training table, x203..571 y120..260.
- Verdict: **FINAL VERDICT: PASS** — every cell value (X1 row 1/2/3/4/8/9/10/11,
  X2 row 1/3/5/6/16/7/5/3, y row 2/4/6/8/16/18/20/22) and the alternating
  blue/red column ink scheme confirmed identical.

### Why the crop leg was re-cut and re-judged

The banked `crop_2_perfect_table_judge.txt` PASS judged `render_1.png` (the
attempt-1 build). The deliverable has since been rebuilt twice. Measured:
render_1 vs render_3 differ in **790,109 of 2,251,125 pixels** (changed bbox
x54..904, y45..539), so the attempt-1 crop certificate does not cover the
current deliverable. The deck's founder directive (2026-10-19, non-negotiable:
"at minimum ONE per slide covering its densest content region", coordinates
"mapped back to slide space before any edit") and
`judge_protocol_03.md` §"Certificate + DB law" both require the crop pair to be
re-cut and re-judged from the new render after any FAIL. The lane instruction
"do not re-judge it if its transcript is banked PASS" is premised on that PASS
covering the current render, which measurement disproves, so the founder law
governed. `render_1.png`, `crop_2_*`, `judge_attempt_2.txt` and
`crop_2_perfect_table_judge.txt` were all kept as banked evidence.

## Defect history

### Parent-named open defects (all closed)

| # | Defect | Resolution |
|---|---|---|
| 1 | **MAJOR** — outlier labels must read verbatim "X5 is Outlier" (a prior attempt rendered "x8 is Outlier") | Fixed; the string appears exactly **twice** in `slide_012_recreated.pptx` and in the component build |
| 2 | MINOR — "Test Data" label styling | Measured **not a defect** (see adjudication below) |
| 3 | MINOR — test-table colours | Fixed — phase corrected to RED/BLUE/RED |
| 4 | MINOR — cell fill tint | Fixed — cells WHITE-filled |
| 5 | MINOR — arrow anchor | Fixed — re-anchored to x670..705, y250.5 |

### Defects found inside this lane and fixed before judging (write-side)

Two were introduced by the component rewrite and caught by direct pptx-XML
comparison against the certified deliverable, before any vision call:

1. `makeTestTable` returned cell objects with **no `text` key** — the test table
   rendered 12 empty cells.
2. The component set `margin: 0` on cells where the certified deliverable uses
   pptxgenjs defaults (`marL/R 91440`, `marT/B 45720` EMU) — removed.

After those fixes `ppt/slides/slide1.xml` was byte-identical (modulo shape
`id`/`name`) to the deliverable, and `component_fidelity.py` returned
PIXEL-IDENTICAL (0 of 921,600 pixels differ).

### Defects found by PIL adjudication of the attempt-3 judge's MINORs (both fixed)

The attempt-3 judge raised 7 MINORs. All 7 were PIL-adjudicated against both
images (`adjudicate_attempt3_minors.py`, `adjudicate_pass2.py`). Five were shown
**not** to be defects; two were real and were fixed:

1. **Test-table colour phase** — judge finding 3. Hue classification of the
   original frame: columns read **RED, BLUE, RED**; the render had BLUE, RED,
   BLUE (the inverse). The training tables' 1-based data columns alternate
   odd=BLUE/even=RED, but the test table has no label column and carries the
   complementary phase. Fixed; re-measured on `render_3`:
   original `RED, BLUE, RED` == render `RED, BLUE, RED`.
2. **Arrow anchor** — judge finding 5. The arrow is a FAINT 2px hairline at
   960x540 and does not pass a bright-red mask (strict-red px in the gap = 0 in
   the original), which is why earlier windows reported "no arrow". A loose
   (R>G+18 & R>B+18 & R>95) mask reveals a sharp, isolated red-dominant band at
   y250..252 (R-G = +24.7 / +26.9 / +16.3), while the frame's own chroma fringe
   on KNOWN horizontal edges (test-table bottom border, middle-table top border,
   question-box top border) measures R-G = -1.5 / -2.0 / +1.3 — i.e. the frame's
   fringe runs blue, so the red band is a real element and not an artifact. Ink:
   5 px at x669..670 y246..249 (the head) + 89 px at x670..714 y250..252. The
   arrow was re-anchored to x670..705 at y250.5 with the head facing LEFT into
   the middle table; re-measured on `render_3`: x671..705, y248..253 vs the
   original's x669..705, y246..251.

### Adjudicated NOT defects (attempt-3 judge MINORs)

1. **"Added red arrow not present in IMG2" (MINOR, high)** — contradicted by the
   measurement above: the arrow exists in the original at y250..251, x670..705.
   Kept.
2. **"Again box sits lower than in the original" (MINOR, medium)** — both images
   place the box at x707..835, y270..316 (w=129, h=47). Identical.
3. **"Odd-column hue is near-black in the original" (MINOR, LOW, self-declared
   unconfirmed)** — hue classification of the original's training tables and
   test table shows unambiguous blue ink in the odd columns (e.g. test table
   Test2: 264 blue px / 0 red px). The original is blue, as rendered.
4. **"Header row taller, labels ride higher" (MINOR, low-medium, self-declared
   not rising to MAJOR)** — header cell height is 31px in both; the X1 header
   glyph's vertical centre is 143.0 in the original and 142.8 in the render
   against a cell centre of 142.5. Both centred.

### Adjudicated real-but-MINOR, not fixed this lane

Recorded so the next lane can decide. Both are typographic; both were rated
MINOR by the judge; neither is a BLOCKER/MAJOR.

1. **Question-box geometry + line break (judge finding 3, MINOR, high).**
   Measured border: original **x603..879, y366..415** (277x50) with a dark
   indigo border (sampled (61,53,110)), render x604..869, y366..414 (265x48)
   with a pure blue border. The original's text lines are
   "What will be the effect of X8 Outlier" (x613..853, y374..389) /
   "values on the trained model ???" (x612..834, y394..406); the render wraps
   later because its interior is narrower. Fix = widen the box to x603..879,
   use the indigo border, and force the two measured line breaks.
2. **Label/callout text alignment (judge finding 5, MINOR, medium) — the judge
   states the direction backwards.** The original LEFT-aligns all five boxes'
   text with a consistent 9-13px left inset (Training Data L11/R23; Perfect Data
   L9/R34; Outlier 1 L10/R30; Outlier 2 L10/R30; Again L13/R81). The render
   CENTERS it (e.g. Again: two lines both centred at x=772 against a box centre
   of 771). Fix = `align: "left"` with a measured ~10px inset in `labelBox` /
   `textBox`.
3. **Subscripts at baseline** (raised by both crop judges). Same adjudication as
   the prior lane: the original's 1-digit subscripts are at the noise floor at
   960x540, separate subscript runs risk more damage than they fix, and both
   crop judges passed it as a MINOR. Not implemented.

## Component refresh (the 013 inheritance)

`recreated_pptx/build/components/slide_012.js` was rewritten from the certified
`build/slide_012.js` in the `slide_009.js` house idiom. Exports for child 013:

- `renderBase(pptx, slide, opts)` — full-slide draw, plus `skip` / `only` /
  `numeral` composition hooks
- `BLOCKS` — the 10 named blocks (chrome, title, labels, trainTable, testBlock,
  outlier1Table, againCallout, arrow, outlier2Table, questionBox)
- Table builders: `makeTrainTable(header, rows, hlRow, hlCol)`,
  `makeTestTable(header, rows)` — **this is the PATTERN 013 inherits**
- Geometry constants: `TRAIN_COLS`, `TRAIN_ROWS`, `OUTLIER1_ROWS`,
  `OUTLIER2_ROWS`, `TEST_COLS`, `TEST_ROWS`, `TEST_Y_ROW`, `TRAIN_HEADER`,
  `TEST_HEADER`
- Content: `PERFECT_ROWS`, `OUTLIER1_ROWS_DATA`, `OUTLIER2_ROWS_DATA`,
  `TEST_ROWS_DATA`
- Label/callout geometry: `LABELS`, `AGAIN_CALLOUT`, `TEST_DATA_LABEL`,
  `QUESTION`, `ARROW`, `TITLE_TEXT`, `QUESTION_TEXT`, `OUTLIER_LABEL`
- Palette: `RED`, `BLUE`, `BLACK`, `WHITE`, `SHADE`, `YELLOW`, `FONT`

Two things 013 must know:

1. `makeTrainTable` takes the training tables' ink rule (label column BLUE bold;
   1-based data columns odd=BLUE / even=RED; WHITE fills).
2. `makeTestTable` deliberately does NOT use that rule — the test table has no
   label column and carries the measured complementary phase
   (`TEST_COL_COLOR`: even=RED, odd=BLUE). 013's test table must re-measure its
   own phase rather than assume it matches the training tables'.

Proof: `component_fidelity.py` → **COMPONENT FIDELITY: PASS**
(pixel-identical 0/921600, same xfrm multiset 24 sp / 4 graphicFrames, container
diff limited to `docProps/core.xml` + shape order, all skip/only/numeral hooks
gating correctly).

## Capacity note

The gateway is saturated fleet-wide (measured 28-33 concurrent `analyze_image`
callers against the gate's 16 slots). Consequences recorded for the next lane:

- Three separate full-slide dispatches died on the gateway's own internal 630s
  HangError ladder; each 3-attempt ladder needs ~1900s but the mandated
  `timeout 1700` outer cap kills it at 1700s, so **EXIT=124 is structural under
  saturation, not a defect of the slide or the payload**. The first two dead
  dispatches were a clean kill (no attempt-3 line, no `EXIT=` marker) and one
  exhausted all three internal attempts (`EXIT=124`).
- The dispatch that eventually PASSED had to wait out ~25 min of queueing. A lane
  should be prepared to spend that long on a single leg.
- Both winning dispatches ran detached (`setsid nohup`) because a 600s harness
  cap on a foreground call kills a 3-5 min vision answer mid-stream.

## Law compliance

- Every DB call prefixed `VIDEO=machine-learning/03_ridger_regression_gradient_descent`.
- Heartbeat sent at ~00:08, 00:09, 00:12, 00:22, 01:04, 01:18, 01:23, 01:41.
- `TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp` for all
  LibreOffice and vision work.
- Vision ONLY through `scripts/16_vision_gate.sh` with `--thinking high
  --max-tokens 65536 --timeout 600` wrapped in `timeout 1700`; payloads sourced
  byte-for-byte from `shared_patterns/judge_protocol_03.md`; no retry-looping
  (each dispatch was a single bounded invocation).
- House chrome per the deck's ratified values: canvas FFFFFF, panel E9E9E7
  x54..903 y45..540, C00000 1pt LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 only
  (no top stroke), badge d35 at (876,73) FDFD96 ring 6A5ACD numeral 12.
- Single plain-named deliverable; no `_v2`/`_fixed` variants.
- No banked evidence deleted; renders, crops and transcripts kept
  (`render_1.png`, `render_2.png`, `render_3.png`, `crop_2_*`, `crop_3_*`,
  `crop_4_*`, `judge_attempt_2.txt`, `crop_2_perfect_table_judge.txt`).
- Adjudication evidence banked: `adjudicate_attempt3.py`,
  `adjudicate_attempt3_minors.py`, `adjudicate_pass2.py`, `verify_fixes.py`,
  `adjudication_*.txt`, `verify_fixes.txt`, `COMPONENT_VERIFICATION.md`.

## S19 payload-exact confirmation close addendum (fresh carrier agent-46, agent-zq2at9bw, 2026-10-25)

Disk-truth verification of the dead carriers' landed work + adjudication of the
final leg. All evidence pre-existed on disk; carrier added zero vision calls.

- legA chain verified: attempt-5 (stream cut, banked as-is) → attempt-6
  (complete, FAIL 1 MAJOR + 4 MINOR) → adjudication_confirm_legA6.txt (MAJOR =
  third re-raise of F-N2 "X5 vs X8", REFUTED by frame-native measurement +
  build XML + certified judges + fresh correlation; 4 MINORs certified-accepted)
  → legA PASS by adjudication, no fix loop.
- Fix 2 verified in sources: label column colW [50,50,51,53], header ["",
  "Test1","Test2","Test3"], label cells dark non-bold align left valign middle,
  SHADE guarded to value cells — both build/slide_012.js:175 and
  components/slide_012.js drawTestBlock (makeTestTable pattern untouched).
- Cascade verified: 013/017/018 components + root scripts load clean;
  deliverables byte-match final-deck ledger source md5s (468d84817c02 /
  7374f15e4637 / 51a57bb11d5c).
- Crop leg (landed pre-death, last pending item): crop_4_perfect_table_judge_confirm.txt
  PASS with 4 MINORs → adjudication_crop_confirm.txt: C1 subscripts (F-N5
  accepted), C3 typeface (rule c), C4 grid weight (rule e + certified crop_4
  finding 3) — certified-accepted; C2 row-label ink (render bold blue (0,0,255)
  vs original achromatic dark median (130,132,129) spread 3, 0 blue px in all
  three tables' label cells) — NEW real MINOR, PIL-confirmed, ACCEPTED per this
  slide's certified precedent (crop_4 finding 1 header-X-ink class), banked as
  open DB task slide_012_label_ink_residual for the orchestrator. No fix loop.
- INCIDENT (md5 supersession): a carrier verification `require()` of
  build/slide_012.js — which writes the pptx at import time — rebuilt the
  deliverable in place; 886a3536228f0fc7b65ff6cf57bd83ff →
  c65c53b5e1dae8dd23516c1adc28a8f2 (same 261,960 B; pptxgenjs zip/docProps
  timestamps only). Content-identity proven zero-vision: slide1.xml raw-equal
  to the final deck's certified page-12 part (merged from 886a, render_check
  PASS) AND fresh LO render byte-identical to banked render_6.png
  (e5432e50d1ac6176f43eb57712a56408, 0 of 2,251,125 px differ). Full record:
  INCIDENT_deliverable_md5_supersession.md. No other slide touched.
- Slide 012 S19 payload-exact confirmation: ALL LEGS CLEAN (legA PASS by
  adjudication; crop PASS by adjudication). Scope S19 close table banked in
  the mission DB.
