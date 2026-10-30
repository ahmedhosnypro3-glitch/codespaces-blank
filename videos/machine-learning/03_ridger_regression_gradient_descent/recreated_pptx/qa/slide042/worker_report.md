# Worker report — slide 042 "Iteration 1"

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Lane: build + visual judge (both legs)
Worker: `worker-fresh-02`

## Deliverable

- **pptx**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_042_recreated.pptx`
  (single plain-named version, per founder single-version law)
- **build script**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_042.js`
- **final render**: `recreated_pptx/qa/slide042/render_10.png` (150 dpi)

## What the slide contains

Perceptron iteration-1 worked example: top-left x1..x6 vector table with C1/C2 class
row, top-centre `Initial W = (4;-2)` + red italic `Step η = 2`, top-right
check-classes matrix with the colour legend, left-middle "Upgraded Vectors (From Top)"
table, a red "Iteration 1" badge, and a five-box right computation stack for
`d(x1)..d(x5)` with update/keep actions and W matrices.

## Frame measurements (960×540, 1px = 1pt)

Measured from `unique_slides/slide_042.jpg` with PIL. Banked in
`qa/slide042/` (`calibrate_*.txt`, `final_verify.txt`, `selfcheck_*.txt`) and the
scratch scans under `scratch/tmp/eq042/`.

| region | measured geometry |
|---|---|
| blue-bordered box | x68..720, y54..130, border 0000FF 1pt, **white** interior |
| top-left table | caption y64..73 blue; digit band A y79..91; digit band B y94..105; class row y110..123 (C1 red x90..137, C2 blue x158..205); red ⇒ x239..253 |
| top-centre | `Initial W =` x266..323 y75..84; matrix parens x330..353 y63..102; `Step η = 2` red italic x365..435 y66..80 |
| top-right | `Check classes of` x499..582 y79..88; Z header y64..76 x601..655; Z digits y82..108; **legend x257..508 y110..123** |
| legend colours | black `C1 positive,` x257..302 — blue `C2` x310..326 — black ` negative,` x330..378 — green `Zero` x395..423 — black ` is unaccepted` x430..508 (**no red in the legend: the frame has zero red ink there**) |
| left-middle | caption x81..234 y148..159; **four** digit bands y166..175 / 183..191 / 195..211 / 214..222; class row y231..243 |
| LM parens | thin 1px strokes per column at (93,107), (115,128), (137,150), (173,182), (205,218), spanning the four bands |
| iteration badge | red rect **x84..214, y277..305** (not x54..200), white bold text x99..197 y284..298 |
| right stack | **five white boxes** x276..898 at y228..261 / 272..327 / 338..393 / 404..459 / 470..527, separated by **panel-gray gaps** (NOT black rules — the frame's gap rows carry zero dark ink) |
| green marks | present in every box at x~384..406; boxes 3–5 also at x~736..750 |

Table values (cross-checked against `analysis/slide_042_final.json`):

- top-left columns: x1=(1,1) x2=(2,1) x3=(1,2) x4=(5,4) x5=(6,5) x6=(6,6)
  (band A = 1,2,1,5,6,6; band B = 1,1,2,4,5,6)
- left-middle band1 = 1,1,1,2,1,1; band2 = all 1; band3 = all 1; band4 = 1,2,1,5,6,6
- check-classes: Z1=(0,0) Z2=(7,6) Z3=(3,2)
- stack: d(x1)=…=0 → Update Weight → W=(4;-2)+2·(1;1)=(6;0);
  d(x2)=…=6 → Keep same Weight → W=(6;0);
  d(x3)=…=6 → Keep same Weight → W=(6;0);
  d(x4)=…=6 → Update Weight → W=(6;0)-2·(1;5)=(4;-10);
  d(x5)=…=-96 → Keep same Weight → W=(4;-10)

## Build iterations (all banked in `qa/slide042/`)

| K | what changed |
|---|---|
| 1 | first run; structure roughly right, several metrics off |
| 2 | white content areas + white stack boxes replacing black rules; badge corrected to x84..214 y277..305; legend rebuilt |
| 3 | font-size calibration pass (from `calibrate.txt` render-vs-frame width ratios) |
| 4 | **legend fix**: pptxgenjs emits `<a:pPr>` between rich-text runs, which breaks the run sequence — replaced the single multi-run `addText` with five separate per-colour text boxes |
| 5 | `d(x_i) =` label: the Unicode subscript glyph renders far too wide; replaced with adjacent `d(x` + small digit + `) =` boxes |
| 6 | tightened label box widths |
| 7 | raised text boxes to stop descender spill into the gray gaps |
| 8 | compressed matrix row pitch 12px → 11px; tightened line-B box heights |
| 9 | raised line B per box → **all four gaps verified ink-free** |
| 10 | **LM parens**: 48pt glyph parens swallowed the digits (render y179..223 vs frame thin strokes) — replaced with thin 0.75pt line shapes + top/bottom hooks; 84/84 self-checks pass |

## Self-check

`qa/slide042/selfcheck_attempt_10.py` — 84/84 PASS on `render_10.png`, covering
the blue box and its four edges, both TL digit bands, TL class-row colours, the red
arrow, `Initial W =` + matrix parens + `Step η`, the check-classes caption/header/digits,
all five legend segments in order (and confirming **no red** in the legend, matching
the frame), the LM caption, all four LM digit bands, the LM paren span, the LM class row,
the badge rect edges and white text, five white boxes at their measured y-ranges with
the panel gaps ink-free (no black rules), the green marks, and the red `Update Weight`
occurrences.

`shared_patterns/house_chrome_check.py render_10.png 42` → **PASS**

## Visual judge legs

| leg | variant | transcript |
|---|---|---|
| A | full-slide comparison, `render_10.png` vs original | `qa/slide042/judge_attempt_10.txt` |
| B | zoomed crop-pairs (`stack`, `tl_table`, `lm_table`, `topright`, `legend`), matched effective scale LANCZOS ×2.0833 | `qa/slide042/crop_10_*_judge.txt` |

Crop pairs are cut from slide-space regions with 8px padding; the original crop is
LANCZOS-upscaled to the render's pixel dimensions so both sides have identical
effective scale (see the Procedure B law in `shared_patterns/judge_protocol_03.md`).

---

# SECTION 2 — 2026-10-24, worker `w042-finish-20261024` (resume + adjudication + fixes + PARKED on gateway)

## Resume history (timeout-resume)

- Took over a **stale claim** (`worker-fresh-042-final`, heartbeat 259 min stale) with
  `claim 42 w042-finish-20261024 --force`; row read `gen_status=building`,
  `visual_attempts=0`, pptx_path + build_script already set.
- Triage: the bank held 12 build attempts (`build_attempt_3..11.js`), renders 1..12,
  `judge_attempt_10.txt` (a real FAIL), crop-10 pairs, calibrate/selfcheck files.
- **Currency verified by reproduction, not assumption:**
  - `build/slide_042.js` rebuilt in-place → pptx XML content **byte-identical** to the
    banked `slide_042_recreated.pptx` (only `docProps/core.xml` timestamps differ), so the
    banked pptx was current.
  - Fresh LibreOffice render (soffice → PDF → `pdftoppm -r 150`) of that pptx →
    **md5-identical** to the banked `render_12.png` (`e82df095…`). Render current too.
  - `analysis/slide_042_final.json` `_meta._reconcile_md5_snapshot` == the original JPEG's
    md5 → ground truth unchanged.
- The banked `render_12.png` was therefore reused as the adjudication baseline (banked as
  `render_13.png` after a byte-identical re-render) and the lane continued from attempt 12.
- **No certified perceptron-family component existed to import.** `build/components/`
  holds 009/012/013/017/020/022/027/035 — none is a perceptron-family member, and every
  sibling in the family (041/043/044/045) is still `building`/uncertified, so the cascade
  law ("children import only *certified* components") barred importing from them. The
  slide's own monolith build was the correct path.

## Banked verdict being adjudicated

`qa/slide042/judge_attempt_10.txt` — **FINAL VERDICT: FAIL**, confidence ~0.7, rendered on
`render_10.png` (attempt 10's build). Note attempt 11 had already replaced the per-box
line B, which is the substance of items 1–2, so those two items are adjudicated against
the **current** build.

## Item-by-item adjudication (measured against BOTH images, 960×540, 1px = 1pt)

Full measurements and scripts: `adjudication_16.md`, `scratch/tmp/042*.py`.

### Independent PIL defects found first (not raised by the judge) — FIXED, both real

| defect | measurement | fix |
|---|---|---|
| box1 W equation crosses its box border | image top y258, h 14.4 → ink y258..272; box1 bottom border y263. Render ink in the y264..272 inter-box gap = **750 dark px** (per-row 130/129/96/139/88/77 for y264..269) where the **frame has 0**. | `BAND_B[0]` 258 → 247 |
| box4 W equation sits ABOVE its `d(x4)` line | `BAND_B[3]=420 < BAND_A[3]=434`; the W4 image (y420..434) overlapped `= 6` (x610..642) and inverted the frame's order (frame: d-line y426..437 **above** W-line y444..452); render y420..443 was one merged band vs the frame's two separated bands. | `BAND_B[3]` 420 → 442, `BAND_A[3]` 434 → 427 |

Root cause: attempt 11 calibrated the bands from the frame then applied one blanket "+8"
shift measured for **text** boxes; line B is an **image** (ink at image top), while
LibreOffice puts a h=14 text box's ink ~2 px **below** its box top. Every derived band is
now checked against its box interior (219..262 / 274..327 / 342..393 / 408..458 / 474..526).
Also matrix row pitch 11 → 7 px (the frame's per-box 2-row matrix fits a 12–13 px line).

### Item 1 — per-step weight-result equations "omitted" (MAJOR conf 0.6)
**REFUTED for the current build.** The judge's own downgrade condition is met: attempt 11
gives each box its **own distinct** mathtext PNG — `eq_042_w1.png`
(W=(4;−2)+2·(1;1)=(6;0)), `w2`/`w3` (W=(6;0)), `w4` (W=(6;0)−2·(1;5)=(4;−10)), `w5`
(W=(4;−10)) — via the mandated pipeline (matplotlib mathtext → 600 dpi transparent PNG →
addImage at px/600 + `assets/eq_index_042.json` sidecar). All five distinct, one per box,
in the line-B band. **Partial substance, real and carried as an open item:** on the frame
the W result is *not* a wide horizontal equation where the build draws it — the frame's
box1 line-B region x395..704 y250..258 is **100% ink-free** (darkest px lum 735–760 ≈ pure
white; per-10px-column scan darkest = 760 throughout x395..704). The only frame ink in that
band is a green ⇐ at x384..393 (RGB 130,157,124, green excess +39) and a narrow dark paren
pair at x713..729 spanning the whole box height. The judge's own wording ("at the **right**
of every iteration row") agrees with the frame. The five equations are kept (the analysis
JSON's `verbatim_text.equations` mandates them) but are now placed inside their boxes.

### Item 2 — garbled/merged step equations (MAJOR conf 0.7)
**REFUTED for the current build.** Attempt 10 stacked 2×1 tiles (that is what read as
"cluttered stray stacked numerals" and "W× 4/−2 + … = −6 0"). Attempt 11's single
horizontal mathtext PNG per row removes the stacking; measured render line-B ink is one
clean 14 px band per box with no merged stray tokens.

### Item 3 — Z / "Check classes of" layout (POSSIBLE MAJOR conf 0.4)
**The judge's arrangement reading is REFUTED; two real frame mismatches found instead and FIXED.**
- The frame is caption → header → two digit rows (the analysis's structure); frame ink
  row-runs x490..670: (55,56) box border, (64,76) caption+header, (79,121) digit rows — no
  evidence of the 3×3 layout the judge could not reconcile.
- **Real defect 1:** the build printed `Z1 Z2 Z3`. The frame prints `Z1` **three times** —
  1 px ASCII of y60..78 shows three glyph groups at x595..610 / 616..631 / 638..653 with
  identical x-masks and shapes. → fixed to `Z1 Z1 Z1`.
- **Real defect 2:** the build drew those headers blue; the frame's header ink is dark
  (darkest px RGB 31,33,11; 0 px pass a blue test). → fixed to black.

### Item 4 — upgraded-vector delimiter / transposition (MINOR conf 0.7)
**REFUTED.** The frame's premise (repeated blue x1..x6 headers, "(n)" cells) does not hold:
the frame's LM data is **column-major with thin vertical strokes** — ink row-runs x76..240
are (148,159) caption, (166,175), (184,191), (199,206), (215,222) four digit bands,
(231,243) class row, i.e. the build's `LM_BANDS` order, with the paren span y166..222
matching the build's measured `LM_PAREN_PAIRS`. No transpose fix.

### Item 5 — missing repeated header row above the LM matrix (MINOR conf 0.6)
**REFUTED with numbers.** No second header exists on the frame: blue ink in the candidate
header zone y140..168 = 236 px (accounted for by the single blue
"Upgraded Vectors (From Top)" caption, the only ink between caption and first digit band),
vs 132 px in the matrix zone y168..230; the gap y160..166 carries **0** ink. Adding a
header row would fabricate an element the frame lacks.

### Item 6 — top grouping box "rounded, ~#FFF2CC" (MINOR conf 0.75)
**REFUTED.** Fill: frame interior px are (254,255,234) / (255,247,224) / (254,255,232) —
the frame's cream is **FEFFE9 ≈ FEFFE8**, not #FFF2CC and not white; the build already
uses `CREAM = FEFFE8` and the judge's "IMG1 rectangular white box" is wrong. Rounded: the
frame's extreme corner px (69,58) is dark border ink (RGB 33,24,103) — a rounded container
would leave that corner empty, so the frame's box is **rectangular**, matching the build.
Border: frame RGB (34,27,107)/(162,156,230) — blue, matching the build's 0000FF 1 pt.

### Visual note — "Keep same Weight" wraps to two lines
**REAL, FIXED.** Frame action ink for row2 is x688..727 in **one** line; the pre-fix render
split rows 2/3/5 into two row-bands (row2 y285..298 + y304..318) because the 130 px box was
too narrow for 16 pt. Action box widened 130 → 148 px; each action now renders as one band
(row2 294..308, row3 360..374, row5 492..506).

### Extra frame-measured deviation found while adjudicating item 3 — FIXED (attempt 17)
The TL table's `x1..x6` header is **black** on the frame but the build drew it **blue**.
Channel-order test (unambiguous, and blue *is* detectable in this JPEG): the header's 12
darkest px (y64..73, x86..216) all carry **b − r = −19..−20** (blue is the *lowest*
channel) and 0 px pass `b>r+25 & b>120`, while the known-blue LM caption's darkest px carry
**b − r = +45..+77**. Same signature as the check-classes header already fixed. The red/blue
C1/C2 class row was measured separately and left alone (red 422 px, blue 502 px preserved).

## What changed (build attempts, all single plain-named deliverable)

- `build_attempt_16.js` (md5 `976b3d64…`): band re-derivation (`BAND_A`/`BAND_B`), matrix
  row pitch 7, `Z1 Z1 Z1` headers in black, action box 148 px.
- `build_attempt_17.js` (md5 `6fe3d19b…`, identical to the live
  `build/slide_042.js`): + TL `x1..x6` header black.
- Deliverable rewritten by the build into the single plain-named
  `recreated_pptx/slide_042_recreated.pptx`; renders `render_14..17.png` banked.

## Verification of the fixed build (`render_17.png`, 2001×1125 @150 dpi)

- `shared_patterns/house_chrome_check.py render_17.png 42` → **PASS**
- Inter-box gap ink (x276..853): **0 / 0 / 0 / 0** for y264..271, y330..337, y396..403,
  y462..469 — the frame keeps these ink-free and the pre-fix build spilled 750 px into gap 1.
- Per-box ink contained and in frame order: 231..259, 294..322, 360..388, 426..454, 492..520
  (all inside their boxes 219..262 / 274..327 / 342..393 / 408..458 / 474..526).
- TL header black (0 blue px); check-classes `Z1` headers black (0 blue px); LM caption
  still blue (2581 px); C1 red / C2 blue preserved.

## Vision legs — NOT certified (gateway wedge, no verdict produced)

| event | transcript | outcome |
|---|---|---|
| attempt 16 dispatch, Template A | — | my dispatch script had a path typo (`slide042.jpg` vs `slide_042.jpg`); the analyzer exited on "not a file" **before any model call**, so 0 model calls were made and no attempt was consumed. Evidence: `legA_16_abort_504.log`. Script corrected + re-verified. |
| attempt 17 dispatch, Template A | — | **HTTP 504 `upstream_timeout`**, ironrouter candidate `nva…hWGS` provider `Nvidia`; "0/1 result(s) analyzed"; no FINAL VERDICT. `legA_17_abort_504.log`. |
| protocol probe (Template A's prescribed window-opener, `analysis`, `--timeout 120`, tiny prompt) | — | **identical HTTP 504** from the same Nvidia candidate at gate count 7. |

**Wall attribution (banked):** the failure is upstream-provider-level, not queue depth — the
attempt-17 dispatch ran at gate count **7** (below the 8-slot law) and the tiny probe still
died, with no 630 s/1200 s client wall involved (both returned in ~60 s). Fleet trend
`gate_trend_20261024.log`: 44→41→39→38→33→28→25→21→23→20→20 true analyzers between
13:06 and 13:25 UTC, with the oldest process aged 1271–1673 s (past its own 1200 s wall),
matching the documented fleet IMAGE-leg wedge; TEXT legs on the same router were healthy
per the 043 lane's banked evidence.

**Attempt accounting:** attempt 10 produced a real FAIL verdict on a superseded build;
attempt 17 was dispatched on the current build and produced no verdict. No verdict exists
for the current build → **NOT certified, no PASS fabricated.**

### Payload integrity (audit finding from the bank)
The prior lane's `judge_prompt_10.txt` and `crop_10_*_prompt.txt` contain "**BLOC10ER**"
where the protocol template says "BLOCKER" — a naive `K`→`10` substitution corrupted the
severity keyword. This lane's payloads are generated with **`\bK\b` word-boundary-only**
substitution and byte-verified: `judge_prompt_17.txt` md5 `65de405e669cf6574e9465221fbec5f3`
== protocol Template A line; all five `crop_17_*_prompt.txt` identical
(md5 `4ce754a2f9515f1f5ac69be4ee0cf04e`) == protocol Template B with `NNN`→`042` only.
"BLOCKER" intact in all 6 payloads; no `BLOC\d+ER` anywhere in this lane's outputs.

## Banked artifacts (this lane, all under `qa/slide042/`)

`render_14.png`, `render_15.png`, `render_16.png`, `render_17.png`,
`build_attempt_12_pre_bandfix.js`, `build_attempt_16.js`, `build_attempt_17.js`,
`judge_prompt_17.txt`, `crop_17_{stack,tl_table,lm_table,topright,legend}_{render,orig,prompt}.png/.txt`,
`dispatch_A17.sh`, `dispatch_B17.sh`, `adjudication_16.md`,
`gate_trend_20261024.log`, `legA_16_abort_504.log`, `legA_17_abort_504.log`.
Measurement scripts: `scratch/tmp/042measure.py`, `042bands.py`, `042origbands.py`,
`042boxbands.py`, `042clean.py`, `042adjudicate.py`, `042maps.py`, `042cc.py`,
`042crops17.py`, `042payloads17.py`.

## PARK STATE — verdicts outstanding, exact resume commands

Row 42 is parked **`gen_status=building`, `visual_check=FAIL` (no vision evidence for the
current build), `visual_attempts=2`** (attempt 10 FAIL on a superseded build; attempt 17
dispatched and aborted with no verdict), `worker_id=""` after release. Build side is
**complete and verified** — only the two judge legs are missing.

Resume (the Nvidia `images` upstream must be returning 200s first):

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"     # mandatory split path
export VIDEO=machine-learning/03_ridger_regression_gradient_descent

# 0) gate check — dispatch only when pgrep -f "python3 .*analyze_image.py" | wc -l  < 8
# 1) LEG A — full-slide comparison judge (Template A), payload already byte-verified
./videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/dispatch_A17.sh
# 2) LEG B — Procedure B crop pairs (stack/tl_table/lm_table/topright/legend), matched scale
./videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/dispatch_B17.sh
```

Both scripts carry the mandated walls (`--timeout 1200` inside `timeout 1700`,
`--thinking high --max-tokens 65536`, `--rounds 1 --tries 1`), the byte-verified payloads,
and the ≥8 gate back-off. Expected outputs:
`qa/slide042/judge_attempt_17.txt` and `qa/slide042/crop_17_<name>_judge.txt`.

If both legs return `FINAL VERDICT: PASS` (or every finding is PIL-refuted with a banked
number from `adjudication_16.md`):

```bash
python3 scripts/15_progress.py set 42 pptx_path videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_042_recreated.pptx
python3 scripts/15_progress.py set 42 build_script videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_042.js
python3 scripts/15_progress.py set 42 visual_check PASS
python3 scripts/15_progress.py set 42 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/judge_attempt_17.txt
python3 scripts/15_progress.py set 42 visual_attempts 3
python3 scripts/15_progress.py set 42 gen_status passed
python3 scripts/15_progress.py heartbeat 42 <worker-id>
python3 scripts/15_progress.py release 42 <worker-id>
python3 scripts/15_progress.py get 42     # must read gen_status=passed AND visual_check=PASS AND worker_id=""
```

If either leg FAILs: adjudicate PIL-first against `adjudication_16.md`, fix the build
(copy-then-modify, single plain-named deliverable), re-render, re-cut crops, re-dispatch
both legs — up to 6 attempts total.

---

## ATTEMPT 24 — carrier-s6-251025b handoff (2026-10-25)

Status at claim: attempt-24 micro-fix phase. Prior 8-item fix spec was already
applied to `build/slide_042.js` (full map in its ATTEMPT 24 header; pre-edit bank
`build_attempt_23.js` md5 cc3f18277cf1dd3054a26595d941c267; content ground truth =
`adjudication_attempt23.md` read-legs at bottom).

This session completed the last 2 of 3 micro-fixes:

1. box1 ROWS x1 `eqX: 400 → 411` ("= 0" was ~11px left of ORIG ink 414..429)
2. Initial-W row3 `txt("-2", 339, 95, …) → y 91` (was ~4px low vs ORIG ink 91..102)

(the 3rd item, LM paren-pairs x {353,360,372,384,391,403,410,422,429,441,448,460},
was applied earlier in this attempt)

Verified after fixes:

- rebuild: `TMPDIR=scratch/tmp node build/slide_042.js` → `slide_042_recreated.pptx` OK
- render: `qa/slide042/render_24.png` md5 **83280ab5789092e0fa656bb0b9781ab6**,
  2001×1125 (150dpi, same soffice recipe as before)
- house chrome check: **PASS** (panel x112-1882, y94-bottom; strokes L/R/bottom,
  top bare; badge center d=68; all within tol 8)
- banked: `qa/slide042/build_attempt_24.js` md5 **5f1350f758b1099716e29f4c5bcb05e8**
- PIL selfcheck: everything within ~2-6px of ORIG except two drifts (was: two
  drifts before these micro-fixes; paren-pair edit + these two landed)

NOT done (deadline hit): legA judge. Next carrier steps:

1. Gate check `pgrep -c -f analyze_image.py` (need <8), then legA Template A
   comparison exactly per `shared_patterns/judge_protocol_03.md` — payload line 71
   byte-identical, substitute only NNN=042 K=24. ONE leg per Bash call,
   background+wait. Transcript: `qa/slide042/judge_attempt_24.txt`.
2. Zoomed crop-pair certs (Template B, protocol line 117), render crop ×2.083
   LANCZOS from render_24, 5 windows (orig coords): stack (320,135,810,540),
   Initial W (312,45,415,110), legend (225,95,570,132), lm (30,140,340,252),
   topright (560,30,850,125). Transcripts `crop_24_<name>_judge.txt`.
3. Adjudicate any FAILs PIL-first vs `adjudication_attempt23.md`; fix = copy-then-
   modify the build; re-render; re-cut crops; re-dispatch.
4. Certify: visual_check PASS + visual_transcript + visual_attempts + gen_status
   passed, then `15_progress.py release 42 <carrier>`.

Key measured facts this attempt (PIL-arbitrated, from `scratch/tmp/s6_042_pil24.py`
follow-ups): LM digit rows y166/184/199 with values [1,1,1,1,1,1]/[1,2,1,5,6,6]/
[1,1,2,4,5,6]; LM paren pairs (93,107),(115,128),(137,150),(159,173),(182,196),
(205,218) span y166..222 (identical in 043); legend ORIG: C1 RED x239..253,
"positive," ends 302, C2 312..319, "negative," 322..378, Zero 396..422, "is
unaccepted" 431..508; box1 anchors: ⇒ RED ~486, action ~507..591, W̲= 614,
vec(4,−2,−2) black (646,672), "+ 2*" red 676, vec(1,1,1) (708,725), "=" 728,
vec(6,0,0) GREEN (740,758), ⇐ 774; Initial W rows y63/79/91; paren asset
`build/assets/parens042/paren_z_{lp,rp}_red.png` (tinted 192,0,0, alpha kept).

## ATTEMPT 25 — CERTIFIED (2026-10-25, kimi-s6-FRESH-1792954337)

Build `build/slide_042.js` md5 **7b459f1ae97e3f0d478673f61cbdb6e1** (banked
`build_attempt_25.js`), render `qa/slide042/render_25.png` md5
**98bedc4be123bff2f592b6c18edcfd07** (2001×1125), house chrome check **PASS**.
Fix basis: `adjudication_attempt24.md` (all 6 a24 legs dispositioned + the
lm_table refutation correction + the topright hang incident + the B24 DESC
arrow-wording correction). Edits: TL parens/TL_CX, legend (⇒ removed, commas
removed, re-centred), Initial-W bowed parens + 11pt digits, LM restructure
(white card + x₁..x₆ header + bands 183/198/214 + bowed parens ink y179..225),
tallVec → side-aware bowed PNGs (black/green), DVEC_XS per-box spans,
W̲ all 6 rows, b4 eqX 406.5, Z-block digits/tips.

Judge round (dispatch_A25.sh / dispatch_B25.sh; frozen payloads byte-for-byte):
| Leg | Verdict |
|---|---|
| legA full slide | **PASS** (3 MINOR: arrow glyph variant, LM border hairline, spacing) |
| crop initial_w | **PASS** (MINOR: hyphen-minus, spacing) |
| crop lm_table | **PASS** (MINOR: typography only) |
| crop tl_table | **PASS** (MINOR: typography, 1-2px baseline wobble) |
| crop legend | **PASS** (MINOR×4; the 1 MAJOR is the Initial-W sliver — certified by initial_w) |
| crop stack | **PASS** (MINOR×4: hyphen-minus, serif, spacing, arrow weight) |
| crop topright | **PASS** (MINOR/non-defect: glyph weight) |

DB: visual_check PASS · visual_transcript legA-25 · visual_attempts 25 ·
gen_status passed · released. **No OMML wrap** (042 draws no mathtext PNGs —
eqImage is dead code in the build; verify grep eqImage( → definition only).

043 prep done this window: `build/assets/eq043_mx1..3.png` regenerated
(gen_eq_043.py mx specs; dims match the banked sidecars exactly; stale codespace
`path` field repaired). Remaining 043 asset regen needs band-value corrections
first (dx2 −16 not −14; x₄ "(10;02;0)" PIL arbitration) per
`qa/slide043/prephase/build_readiness.md` + `orig_judges/slide_043_stack_desc.txt`.
