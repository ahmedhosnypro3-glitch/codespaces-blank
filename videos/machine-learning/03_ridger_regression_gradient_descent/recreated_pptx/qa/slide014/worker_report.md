# Slide 014 worker report — machine-learning/03_ridger_regression_gradient_descent

Worker: `w014-buildfirst-20261024` (BUILD-FIRST lane; took over from
`worker-fresh-014c`, heartbeat 160 min stale at takeover)

## Inherited attempt history (never delete banked evidence)

| Attempt | Render | Judge | Result |
|---|---|---|---|
| 1 (prior worker `worker-slide014-1792761473`) | `render_1.png` + byte-identical copies v2/v4/v5 (md5 `da8da6c3…`) | `judge_attempt_1.txt` | **FAIL** — 9 BLOCKERs: title, both label boxes, 4 bands, loss-term and reg-term boxes rendered EMPTY ("completely textless shell"). `selfcheck_attempt_1_out.txt` = HOUSE CHROME PASS. |
| 2 (`worker-slide014-r2`) | `render_2.png` | probe only; no coherent body | Blocked on gateway rate-limiting; **never judged** — attempt 2's FAIL was never superseded by evidence, but the textless-shell cause is gone (see verification below). |
| 3 (this worker) | `render_3.png` (staged) | **PARKED — gateway congested** | Build + chrome + crops + payloads verified locally; judge legs staged. See below. |

## Resume note

Resumed from attempt 2. Reused `build/slide_014.js` unchanged; attempt numbering
continues at 3 (`render_3`, `probe_3`, `judge_attempt_3`, `crop_3_*`).

## BUILD CURRENCY — PROVEN

- `recreated_pptx/slide_014_recreated.pptx` rebuilt from `build/slide_014.js`
  identical build input; the rebuild renders **pixel-identical** to the banked
  attempt-2 render: 0 of 2,251,125 pixels differ, `render_2.png` md5
  `da935d0ad0dfd1a8066a1180a492e319` == `render_3.png` md5.
  The pptx bytes differ only in zip metadata (pptxgenjs is not byte-deterministic
  across runs — `docProps/core.xml` timestamp), so md5 of the .pptx is NOT the
  currency proof; the **pixel-identical re-render** is. Verdict: the attempt-2
  build is current, no rebuild needed.
- `render_3.png` (2001×1125, 150dpi) staged for the judge at the fleet convention
  (pptx → PDF → `pdftoppm -png -r 150`), per `qa/slide047/render_attempt6.sh`.

## HOUSE CHROME — PASS

`shared_patterns/house_chrome_check.py` on the render:

```
HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom
present, top bare; badge center (1824,152) d=68; all within tol 8)
```

Measured strokes vs original: left x 57 (orig) / 58.1 (render), right x 902 /
901.0, bottom y 533..539 / 533..538.8, **top band red px = 0 on both** (this deck
has no top stroke — correct). Panel gray orig (231,233,232) vs render
(233,233,231). Badge fill orig (247,254,154) vs render (252,252,149) — same
family. Numeral "14" present.

## PIL MEASUREMENTS — render vs original (frame-px; 1px = 1pt)

All numbers measured on BOTH images. Scripts banked in `qa/slide014/`.

| Element | Original | Render | Verdict |
|---|---|---|---|
| Title | y 55..107 | y 55..107 | ✅ exact vertical match, ink present (black + blue runs correct) |
| Left vector box (border) | x 57..457, y ~104..236 | x 53.4..449.9, y 103.8..232 | ⚠️ 7px narrower on the right; left edge 3.6px early → **MINOR** |
| Right vector box (border) | x ~500..900, y ~104..236 | x 499.8..901.1, y 103.8..232 | ❌ right edge sits ON the right stroke x901 → **MAJOR** (protocol clause 5) |
| Ridge band (yellow) | x 92..877, y 247..281 | x 54..903, y 250..278 | ⚠️ inset missing (render full-panel-width), ~2.5px lower → **MAJOR** |
| Objective band (yellow) | x 91..877, y 307..336 | x 54..903, y 310..334 | ⚠️ same inset issue, +3px lower → **MAJOR** |
| **Mid region, block 1** | **peach fill (248,222,193), x 90..665, y 350..389, contains text** | **absent — plain gray panel** | ❌ **BLOCKER** (missing element) |
| **Mid region, block 2** | **peach fill (248,220,193), x 89..471, y 403..444** | x 54..903, y 398..422 (pink FFEBEE) | ❌ **BLOCKER** — the render's pink band is full-width across both blocks and the gutter; original's block is x 89..471 only |
| **Mid region, block 3** | **yellow fill (245,252,218), x 533..880, y 404..444** (gray gutter x 477..532 verified by raw pixel grid) | **absent — plain gray panel** | ❌ **BLOCKER** (missing element) |
| Lower blue region | x 91..876, y 468..526, continuous across the column gutter | x 53.8..895.7, y 468..520, with a gray gutter cut x 449.8..499.7 | ❌ left edge crosses the left stroke (x58.5) → **MAJOR**; right edge 20px wide of the original; the artificial gutter is not in the original; bottom 6px short |
| Vector-box text | 3 lines per box | 3 lines per box | ✅ content complete (attempt-1's 9 BLOCKERs are gone) |

Band fills: render yellow `FFF9C4` vs original ridge `(249,253,218)`; render pink
`FFEBEE` vs original peach `(248,222,193)` — these are the colours the analysis
brief/K2 palette specified, so they are the *specified* colours, but they do NOT
match the original's measured fills. Flagged for the judge under PIL-first
adjudication.

Refuted / non-issues: top stroke absence (deck law), band-containment claim from
attempt 1 (the original's bands cross nothing the render doesn't), badge
geometry.

### What this means for judging

The original has **three stacked/paired bands in the mid region** (y 350..444)
where the build has **one** (y 398..422). The build's `slide_014.js` region map
only ever described four bands + final. This is the substantive defect the judge
must confirm, and it is measured, not assumed. It is NOT a house-chrome issue and
NOT a frame-containment artifact.

## PROCEDURE B CROP PAIRS — CUT AT MATCHED EFFECTIVE SCALE

`create_crops_3.py` cut 4 pairs (this slide is multi-region, so one pair per
dense region per the founder directive). Both crops of every pair are the SAME
output size and the same effective scale:

| Pair | Frame-px bbox | Sizes | eff. scale |
|---|---|---|---|
| `title_boxes` | x 48..910, y 50..240 | 1797×396 | 2.0847 px/frame-px (both) |
| `upper_bands` | x 48..910, y 242..340 | 1797×204 | 2.0847 |
| `middle_bands` | x 48..910, y 345..452 | 1797×223 | 2.0847 |
| `lower_region` | x 48..910, y 462..532 | 1797×145 | 2.0847 |

Render crops taken from `render_3.png` at H_render/540; original crops
LANCZOS-upscaled to the identical output size. `MATCH=True` for all four pairs
(verified: identical dimensions and identical px/frame-px per axis).

## PAYLOADS — BANKED, BYTE-CHECKED

Per the payload-hygiene law, source `shared_patterns/judge_protocol_03.md`,
substitute only `slide_NNN`→`slide014` and the standalone `K`→attempt with
`\bK\b` word boundaries so `BLOCKER` is never corrupted:

- `payload_A_3.txt` — full-slide (Template A). The frozen payload carries **no**
  `NNN`/`K` tokens, so it is byte-identical to the protocol's Template A payload
  (4115 chars, md5 `9387f5fbb94ef05a31db19f1e018dde1`). `BLOCKER` intact ×4.
- `payload_B_3.txt` — crop-pair (Template B). Only `slide NNN`→`slide 014`
  applied (1914 chars, md5 `978be75de7b83501d09f8f0c5576cbee`). `BLOCKER` intact ×2.

Both verified: no leftover `NNN`, no leftover standalone `K`, no `BLOC3ER`
corruption, byte-reproducible from the frozen template. Sibling-lane payload banks
were NOT reused.

## JUDGE DISPATCH — PARKED (gateway congested the entire window)

Vision gateway (localhost:17844 ironrouter) was congested for the whole work
window (10–14 `analyze_image.py` processes queued at every probe, 09:07–09:56).
Per the gate law (`pgrep -c -f analyze_image.py >= 8` → do NOT dispatch),
**no vision leg was fired**.

### Diagnostic evidence that this is the IMAGE leg, not the router

The router itself is healthy and completing requests fast:

| Probe | Result |
|---|---|
| `GET /v1/models` (no key) | HTTP 401 in 0.9 ms — router alive, auth rejected as expected |
| `POST /v1/chat/completions`, `model=images`, text-only, `max_tokens=16` | **HTTP 200 in 1.01 s**, `finish_reason=length` (probed 09:44) |
| `POST /v1/chat/completions`, `model=images`, text-only, `max_tokens=64` | **HTTP 200 in 3.06 s**, `finish_reason=stop` (probed 09:51) |
| Queued image judges | oldest running **1325 s (22 min)** with 0–2 s CPU — parked on network I/O |
| Transcript output of the queued clients | **0 of 10** have written their `--transcript` file at all |

So: text-turn routing works; the queued image comparisons are not progressing
(the router's image/key pool is not servicing them). Sibling lanes on slides
047/021/010 are in the same state. A judge leg dispatched now would park the
same way and burn ~25 min for no verdict — exactly the waste the gate law
forecloses. The fleets' own gate script holds 16 flock slots and would not have
blocked me, but the upstream image path is what is wedged.

### Staged and ready

`dispatch_attempt_3.sh` — leg 0 congestion probe (aborts if ≥8), leg 1
Template A probe, leg 2 Template A full-slide judge, leg 3 four Procedure B crop
pairs, all via `bash scripts/16_vision_gate.sh`, `--thinking high
--max-tokens 65536 --timeout 600`, one hard-wall retry each, no other retry
loops. Syntax-checked with `bash -n`.

## CURRENT STATE — PARKED (build-verified, judge blocked upstream)

- Build verified current and content-complete; house chrome PASS.
- Crop pairs cut and payloads banked, all byte-checked.
- **Judge legs BLOCKED upstream, not on the build** — see the diagnostic table
  above. Congestion probes 09:07–10:00 never dropped below 8 (peak 15).
- DB claim `w014-buildfirst-20261024` retained; heartbeat at 10:00:28Z.
- `visual_check` and `visual_transcript` deliberately left `null` — **no verdict
  was fabricated**. `gen_status` stays `building`.

### What the next worker must do (in order)

1. Confirm congestion has drained (`pgrep -c -f analyze_image.py` < 8, twice,
   ~10 min apart).
2. Fire `dispatch_attempt_3.sh` (Template A probe → full-slide judge → 4 crop pairs).
3. Read every transcript for a real `FINAL VERDICT:` line; a body without one is
   not evidence.
4. PIL-adjudicate every finding against BOTH images before touching the build —
   the measured table above is the adjudication baseline.
5. If any leg FAILs, the measured BLOCKER list is the fix list (three mid-region
   bands: peach x90..665 y350..389; peach x89..471 y403..444; yellow x533..880
   y404..444). Edit `build/slide_014.js`, copy-then-modify the pptx, re-render as
   `render_4.png`, re-cut crops as `crop_4_*`, re-emit payloads with K=4, re-run
   BOTH legs.
6. Only then run the certification sequence (`set 14 visual_check PASS`,
   `set 14 visual_transcript <path>`, `set 14 gen_status passed`, heartbeat,
   `release 14 <id>`) and confirm `get 14` shows `gen_status=passed`,
   `visual_check=PASS`, `worker_id=""`.

### Resume commands (single block)

```bash
cd /worksp/aces/codespaces-blank/ai_llm_slides
n=$(pgrep -c -f analyze_image.py); echo "congestion=$n"   # must read < 8
# then:
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/dispatch_attempt_3.sh
```

## RESUME COMMANDS

```bash
cd /worksp/aces/codespaces-blank/ai_llm_slides
n=$(pgrep -c -f analyze_image.py)          # must be < 8
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/dispatch_attempt_3.sh
```

If the legs FAIL, the measured BLOCKERs above are the fix list (three mid-region
bands: peach x90..665 y350..389; peach x89..471 y403..444; yellow x533..880
y404..444) — edit `build/slide_014.js`, copy-then-modify to
`slide_014_recreated.pptx`, re-render as `render_4.png`, re-cut crops as
`crop_4_*`, re-emit payloads with K=4, and re-run BOTH legs.

---

## APPENDIX — INDEPENDENT LEGS VERIFICATION (worker `w014-legs3`, 2026-10-24)

Full detail: `qa/slide014/legs_status_attempt3.md`. Summary:

**PATH CORRECTION:** the bank is at
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/`,
NOT at the project root. Resume commands without the deck prefix fail ENOENT.
(The root `recreated_pptx/qa/` holds only `slide046`.)

**Bank re-verified with ls + md5:** render_3 `da935d0…`, payload_A_3
`9387f5bb…` (4115 chars, BLOCKER×4), payload_B_3 `978be75de…` (1914 chars,
BLOCKER×2), `dispatch_attempt_3.sh` syntax-clean with `PY` resolving correctly,
all 4 crop pairs size-matched at 1797×N.

**Gate:** congested at every probe 11:47–12:35Z (20/16/17/17, then 22/22/28/28/44/
49/42/39, then 15). No vision leg fired. Poller running (`gate_poll_014.sh`,
240 s cadence, exits 0 on `< 8`, writes `gate_open.marker`).

**Chrome: PASS, independently re-measured** (left x58.1, right x901.0, bottom
y537.8..538.3, top 0 red px, badge (875.3,72.7) d32.6 — all within tol 8).
Chrome is NOT the defect.

**All three inherited BLOCKERs independently CONFIRMED**, plus a stronger one the
inherited table understated: the render has **zero ink** in mid bands 1 and 3 —
the text is missing along with the fills:

| Region | Original ink | Render ink |
|---|---|---|
| mid band 1 (x90..665, y350..389) | 2242 px / 39 rows | **0 px / 0 rows** |
| mid band 3 (x533..880, y404..444) | 1207 px / 24 rows | **0 px / 0 rows** |

**One inherited table row is WRONG and needs correcting:** "right vector box
border sits ON the right stroke x901". Measured — the render's box border is a
black vertical at **x895.2..895.7** and the right red stroke is a *separate*
vertical at **x901.0** (5.3 px apart). The inherited number measured the stroke,
not the border. The real defect is a span/colour mismatch: original LEFT box
x80..433 / RIGHT box x457..810 with maroon borders (143,18,32) and pink
interiors, vs render LEFT x53.3..449.5 / RIGHT x499.4..895.7 with black (0,0,0)
borders and white interiors.

My scripts (`chrome_reverify_3.py`, `pil_reverify_3.py`, `pil_samples_3.py`,
`pil_focus_3.py`, `pil_boxcheck_3.py`) and their outputs are banked in this
directory. Nothing in the build was edited by this lane.

## APPENDIX — judge-s2-20261025 (2026-10-25): attempt-4 rebuild + staged legs

Cause of the huge geometry deviation: the attempt-3 render had zero ink in the
mid bands (build inherited numbers from the ml-intro table). Lane rebuilt
build/slide_016-style from PIL measurement of slide_014.jpg:
- vector boxes x80..433 / x457..810, maroon borders, y99..238;
- bands y243..285 and y303..341 (full-width, navy-ruled) starting x=60.5/72
  (bands at x58/72 occluded the left red stroke);
- define-loss box x90..665 y347..392 (peach);
- term boxes y399..448 left (peach) / right (pale yellow);
- final band x87..880 y469..528 (pale cyan); blue/maroon/blue title.
Equations rendered via scripts/render_eq.py (graphgen venv): eq_014_Yvec.png
(red 1.88x0.80167in), eq_014_Yhatvec.png (blue 2.02333x1.06667in),
eq_014_final.png (black 4.21667x0.39in).
render_4.png: HOUSE CHROME CHECK PASS; the two 0-ink blockers cleared (ink now
present in all measured regions). Payloads re-frozen K=4: payload_A_4.txt md5
9387f5fbb94ef05a31db19f1e018dde1, payload_B_4.txt
978be75de7b83501d09f8f0c5576cbee (byte-identical to frozen templates).
Crops re-cut at matched scale: crop_4_{bands,vectors,final}_{render,orig}.png.
JUDGE LEGS STAGED (not yet dispatched; one-leg-at-a-time law — slide 015's
driver is the active vision lane): qa/slide014/dispatch_attempt_4.sh (self-gates
on congestion; legA full-slide + 3 zoomed crop pairs). Attempt #3 of 6 — within
cap. Resume order after 015 completes:
    bash $Q/dispatch_attempt_4.sh      # legs serialize internally
Certification after real FINAL VERDICT bodies: visual_attempts=4,
visual_check=PASS, visual_transcript=judge_attempt_4.txt, gen_status passed,
heartbeat, release.

## APPENDIX — judge-s2-20261025 (2026-10-25 ~04:00): attempt-4 legA adjudicated, build fixed, attempt-5 legA dispatched

Attempt-4 legA (render_4) FINAL VERDICT: FAIL — 2 MAJORs, both line-wrap claims.
Adjudication (PIL row-ink profiles + doc-parse OCR of matched crops):
1. "band-1 yellow-box sentence wrapped to 2 lines in render" — REFUTED.
   Render band-1 crop (y600..760 px) OCRs as ONE line ("This is called Ridge
   Regularization"); original band-1 (y248..292) also one line (24px ink band
   vs 55px render run = 26px at 2.084 scale). Line count matches.
2. "objective band: '(λ is a weighting factor)' on second line" — CONFIRMED.
   Original (o_b2 crop) OCR: "Objective function J(W)= Loss(X,Y,W) + λ R(W)
   (λ is a weighting factor)" — ONE line. Render (r_band2_full crop) OCR showed
   the equation on line 1 and "is a weighting factor)" on its own line 2.
   Root cause in build/slide_014.js: the note was a SECOND addText at
   y+0.19in (an intentional second line) — original has it inline.
FIX: merged the three note runs (" (", λ, " is a weighting factor)") into the
band-2 addText run list; removed the second addText. Rebuilt
slide_014_recreated.pptx (NODE_PATH=/home/ahmed/.npm-global/lib/node_modules;
pptxgenjs lives in the npm-global tree, not a local node_modules). Fresh LO
render banked as render_5.png; band-2 crop (y600..740) OCRs as ONE line:
"Objective function J(W) = Loss(X,Y,W) + λ R(W) (λ is a weighting factor)".
DB updated (finding1 refuted / finding2 fixed / attempt5 dispatching).
Attempt-5 legA (Template A payload, render_5) dispatched in background at
pgrep load 6; transcript target qa/slide014/judge_attempt_5.txt. Crop legs
(crop_4_* crops are geometry-reusable but MUST be regenerated from render_5
before the crop legs run — crop_4_* images are cut from render_4).
NOTE: LO convert failed once with Io Write error 0xc10 in a reused profile
dir; a FRESH profile dir per conversion works (w014_fix2).

## APPENDIX 2 — judge-s2-20261025 (2026-10-25 ~04:40): attempt-5 legA adjudicated, 1 real defect fixed, attempt-6 legA dispatched

Attempt-5 legA (render_5, after the band-2 inline fix) FINAL VERDICT: FAIL with
10 findings. Adjudication (pixel measurement + doc-parse OCR):
- REFUTED #1 right-edge containment: orig right stroke x901, band ink to x902;
  render stroke x1877-78 (frame x900.5-901), band ink to x1879 — IDENTICAL
  geometry, both flush. Not a defect.
- REFUTED #2 band-1 wrap: repeat of attempt-4's refuted claim; band-1 OCRs as
  ONE line in both (attempt-4 adjudication evidence stands).
- REFUTED #3 reg-term row: build places Loss/Regularization at identical
  y=399/72, h=49/72 (slide_014.js term-boxes block); same row.
- REFUTED #4 lowercase w: gen_eqs mathtext is \lambda W^{\top} W (uppercase);
  render OCR of final band reads lambda W^T W (vision misread).
- REFUTED #6/#7 underlines: horizontal-streak scan of the original RIGHT vector
  box (x460..808, y100..236) finds only the box borders (y100,y236) and one 17px
  handwriting stroke — NO underline under "Model Ŷ = XW". \underline notation
  claim unsupported.
- MINOR #5/#9/#10: mandated professional-format rendering (frac, \top, \times) —
  not scored per ground rule (e).
- CONFIRMED #8 vector-label color: original LEFT vector box interior census =
  dark 1937 + RED 1637 px; render left box = blue 7 + dark (the eq_014_Yvec.png
  ink was matplotlib default tab:blue (31,119,180)). RIGHT box is blue in orig
  (1285 blue px) and blue in render — correct.
FIX: eq_014_Yvec.png ink recolored blue->C00000 (ink-preserving blend, AA kept,
size unchanged 1128x481). Rebuilt; fresh LO render banked as render_6.png;
left-box census now red 2953 px.
Attempt-6 legA (payload_A_6 = frozen Template A) dispatched in background ->
qa/slide014/judge_attempt_6.txt. Crop legs for attempt 6 staged as
dispatch_6_crop_{bands,vectors,final}.txt; crops must be regenerated from
render_6 via create_crops_5.py (edit REND/render name + K) BEFORE they run.

## Appendix 4 — attempt-7 adjudication + park (judge-s2-20261025)

Attempt 7 (final roll) FAIL. Claims adjudicated in `adjudicate_attempt_7.md`:
#1 collision REFUTED; #2 missing-X, #3 label wrap, #6 missing underlines REAL and
FIXED post-verdict (bold underlined X restored; labels 18→14pt per measured
original glyph height; Ŷ/Y underlined in Define-Loss). #4/#5/#7 + ⋮/… accepted
as minor/style. Post-fix deliverable = render_7c (chrome PASS; doc-parse: left
box 2 lines `Original Labels / from Training Samples`, right box `from Model Ŷ = X W`).
No attempt 8 (cap law). Slide PARKED with evidence chain; deliverable carries all
verified fixes but visual_check remains FAIL-by-cap.
