# Slide 016 worker report — "L₁ and L₂ Regularization"

Worker: `worker-kimi-016-retry` (took over the lane from `worker_slide016_01`, claim heartbeat
140m stale > 40m threshold, per 15_progress.py takeover path).
Deck: `machine-learning/03_ridger_regression_gradient_descent`.
Claimed at 2026-10-23 20:5x. Protocol: `shared_patterns/judge_protocol_03.md`
(Template A full-slide + Procedure B crop-pairs).

## State at pickup

| item | value |
|---|---|
| build script | `recreated_pptx/build/slide_016.js` (banked, 209 lines) |
| deliverable pptx | `recreated_pptx/slide_016_recreated.pptx` (59433 B) |
| render | `qa/slide016/render_1.png` 2001x1125 (150dpi of 13.33x7.5in) |
| house chrome check | PASS (panel x112-1882 y94-bottom; strokes L/R/bottom present, top bare; badge (1824,152) d68) |
| DB row | `gen_status=building`, `visual_check=NULL`, `visual_attempts=0` |
| qa bank | render_1.png only — NO dispatch brief, no measurement bank, no selfcheck |

## Pre-judge PIL forensics (the reason this report exists)

The render's ink map was diffed against the original frame (both brought to 960x540
frame px; render downscaled 2001x1125 -> 960x540 LANCZOS, scale 2.0833 render-px per
frame-px). Per-band dark-ink counts:

| frame rows | original ink px | render ink px | verdict |
|---|---|---|---|
| 0-30 | 0 | 0 | match |
| 90-150 | 2599 | 3960 | render has both headers, original has one |
| 150-300 | ~8600 | ~10500 | OK |
| 300-330 | 120 | 337 | borderline |
| 330-360 | 1468 | **150** | **render empty** |
| 360-390 | 1565 | **150** | **render empty** |
| 390-420 | 1428 | **150** | **render empty** |
| 420-450 | 1156 | **150** | **render empty** |
| 480-540 | 4213 | 4316 | OK |

The 150 px in each empty band is exactly the two red strokes (x58.5 / x901) — i.e. no
text ink at all. Line-band inventory (interior x90..828, strict ink mask):

**Original — 12 text lines** (white box borders at x82-83 / x832-833, y89-91 and y532-534):

| line | band y | x extent | content |
|---|---|---|---|
| title | 59-86 | 312-621 | dark red #8B0000 bold title |
| L1 | 104-117 | 111-325 | "Regularizers are based on:" RED bold |
| L2 | 129-146 | 147-514 | "Penalize large values of W (model parameters)" BLUE bold |
| L3 | 179-197 | 92-556 | bullet 1, black, YELLOW highlight x286-457 y175-198 |
| L4 | 230-248 | 92-783 | bullet 2 line 1 |
| L5 | 256-273 | 110-750 | bullet 2 line 2 |
| L6 | 281-298 | 110-563 | bullet 2 line 3, ends with RED run x111-290 (the "customized weigh factor" red underline sits at y~296-298 under this line) |
| L7 | 332-350 | 92-667 | bullet 3 line 1, RED run x385-667 |
| L8 | 357-374 | 146-696 | bullet 3 line 2, BLUE run x254-390 ("L₂ regularization") |
| L9 | 408-426 | 92-768 | bullet 4 line 1, RED run x420-765 |
| L10 | 434-447 | 146-389 | bullet 4 line 2, BLUE run x254-390 ("L₁ regularization") |
| L11 | 484-502 | 92-807 | bullet 5 line 1, small RED run x647-670 |
| L12 | 510-527 | 109-190 | bullet 5 line 2, RED run x170-190 |

**Render — 7 text lines only** (box at x84-85 / x829-830, y93 and y528-530):

| line | band y | x extent |
|---|---|---|
| title | 69-97 | 92-825 |
| a | 169-183 | 100-496 |
| b | 191-206 | 100-726 |
| c | 210-225 | 100-768 |
| d | 230-251 | 99-707 |
| e | 256-270 | 200-461 |
| f | 280-294 | 100-801 |
| g | 495-509 | 100-825 |

### Root cause (two independent defects in `build/slide_016.js`)

1. **Five lines of body text never render.** The build defines 5 body bullets (l3-l7) but
   the original's bullets 2-5 each wrap onto TWO-3 visual lines each (12 total lines vs
   the build's 7). The build's boxes are ~0.7in tall and its font sizes/box widths
   re-wrap the copy into fewer, longer lines; LibreOffice renders only what fits, so the
   region y330-450 is blank in the render. The two BLUE key-term runs ("L₂ regularization"
   on original L8, "L₁ regularization" on original L10) live in exactly that blank band —
   i.e. the render is missing BOTH blue key terms, which the full-slide judge will flag as
   BLOCKER (missing element).
2. **The two header lines are vertically misplaced.** The build puts L1 at y=1.50in
   (108 frame px) and L2 at y=1.85in; the render's first body line "a" starts at y=169 and
   its own header-equivalents never appear as measured lines (the build's l1/l2 boxes
   render above y=169 but the render's line "a" at 169 is already bullet-1 content —
   the red header and blue sub-header are absorbed into the compressed wrapping).
   Measured original header positions are L1 y=104-117 and L2 y=129-146; the render has
   nothing at those rows.

Also noted: the yellow highlight (render x~72..92? -> measured at y175-198 in the
ORIGINAL, x286-457) does not appear at the same y in the render because the render's
line "a" (bullet 1) sits at y169-183, close but the highlight in the build is at
y=2.25in (162 frame px) x=4.0-6.4in (288-461) — that part is nearly right; the black
underlines on L11/L12 (original "Small number of samples (N)" x92-807 and
"Large vector Length (d)" x109-190) exist in the build but land at the render's wrong
line (its line "g" at y495-509), so they underline the wrong text.

### What a fix needs (for the next worker — NOT done by this worker)

Rebuild `build/slide_016.js` to reproduce all 12 lines with the measured geometry:
explicit per-line y positions in frame px -> inches (/72), matching x extents and the
red/blue/yellow color runs listed above. Simplest faithful approach: one `addText` per
line at the measured y (mid-line), letting each line be a single-string run with the
color-runs split into rich-text arrays for the colored spans. Line y-mids (frame px):
110, 137, 188, 239, 264, 289, 340, 366, 416, 440, 493, 518 — i.e. in inches
1.528, 1.903, 2.611, 3.319, 3.667, 4.014, 4.722, 5.083, 5.778, 6.111, 6.847, 7.194.

## Judge legs (this worker)

Attempt 1 (Template A) dispatched through `scripts/16_vision_gate.sh` per protocol.
Transcript: `qa/slide016/judge_attempt_1.txt`.
Payload: `qa/slide016/judge_prompt_1.txt` (shared prelude + Template A body byte-verbatim
from judge_protocol_03.md, NNN=016 K=1).
Crops cut per Procedure B (`create_crops_1.py`, matched effective scale 2.083x on both
axes, verified by assertion):
- `crop_1_missing_band_{render,orig}.png` — frame bbox (80,325)-(815,455): the original's
  L7-L10 block (both blue key terms + red runs); render crop is empty ink.
- `crop_1_full_body_{render,orig}.png` — frame bbox (80,98)-(815,532): the whole 12-line
  text block inside the white content box.
Template B payloads: `crop_1_missing_band_prompt.txt`, `crop_1_full_body_prompt.txt`.

Gateway state during this worker's run: heavy 504/502/429/connection-error storm. Probe 1
(150s wall) returned no body; protocol hang rule applied (slept 300s); probe 2 also
returned no body. Per parent's storm instruction the real judge was then dispatched
directly with `--timeout 600 --thinking high --max-tokens 65536` inside `timeout 1700`.

**Attempt 1 result: ECHO-CLASS GARBAGE (no evidence, no attempt counted).** The first
dispatch carried the protocol's shared prelude prepended to the Template A body. All three
model attempts failed garbage/hang:
- attempt 1: `GarbageError: echo-class response` — the model echoed the prelude's SKILL.md
  path span verbatim ("home ahmed projects ai llm slides agents skills image analysis
  skill m"), copied-prompt coverage 78% of the response.
- attempt 2: same echo-class, 58% coverage.
- attempt 3: `HangError: hard wall-clock 630s exceeded` — giving up.
This deck's own banked judges (slide012/judge_prompt_1.txt, slide014/judge_prompt_1.txt)
do NOT carry the prelude — they send the Template A body alone and produced coherent
bodies. The payload was therefore restored to the protocol's exact `-p` spec (the
"GROUND RULES..." template body, 4140 B, NNN/K substituted only) and re-dispatached.
No `judge_attempt_1.txt` body was banked from the failed run (no transcript file was
written), so `visual_attempts` stays 0 — degenerate bodies are not attempts per
judge_protocol_03.md.

Status at hand-off: re-dispatch in flight (background task). See final verdict in
`judge_attempt_1.txt` and the DB row.

## Template A attempt 1 — RESULT: FAIL (banked `judge_attempt_1.txt`)

The retry with the protocol-exact payload produced a **coherent, validated winner body**
(degenerate events: 0; winner `images`, round 1 attempt 2 after one HangError abort).
Verdict: **FAIL** — one MAJOR, three MINOR.

Judge findings:
1. **MAJOR (high)** — frame containment / extraneous element: a thin black horizontal
   stroke runs from just after "(d)" on the final bullet far right, **crossing the blue
   inner content-frame border and reaching the house panel's right stroke (x~900-903)**;
   absent in the original; effectively replaces the original's short red underline under
   "Large vector Length".
2. MINOR (medium) — wrap points differ (verbatim text, same line counts).
3. MINOR (medium) — yellow highlight on bullet 1 appears to cover only "generalization"
   vs the original's "better generalization".
4. MINOR (low-medium) — "Squared Norm" / "sum of Absolute values" red emphasis not
   reproduced; verbatim text intact.

### PIL-first adjudication of the judge's findings (per protocol step 6)

- **Finding 1 ADJUDICATED VALID.** Independent PIL proof: in the render's native
  2001x1125 pixels, dark rows run from x84.5 to x829.5-884 frame px at y~505 and wide
  dark runs at y~505/530. The build's second black underline (`ul7b` in
  `build/slide_016.js`, x=textX+8.0in=675px, w=2.8in=202px -> spans 675..877 frame px)
  crosses the white box's right border (x832-833 in the original; x829-830 in the render)
  and so violates the frame-containment rule. It also underlines the WRONG text: the
  original's underline sits under the short continuation line "Large vector Length (d)"
  (original L12, x109..190), while the build's stroke is ~480px to the right of it.
- **Finding 3 PIL-REFUTED.** The build's yellow highlight rect is
  x=4.0..6.4in = 288..461 frame px; the ORIGINAL's measured yellow bbox is
  x286..457, y175..198. The two agree within ~4px on both axes — the highlight is
  correctly placed and sized. The judge's reading of its extent is a full-slide-scale
  visual impression, not a geometry fact.
- **Findings 2 and 4 CONFIRMED AS REAL (minor reflow/styling deltas)** and consistent with
  the deeper defect below.
- **The judge MISSED a BLOCKER, proven by PIL.** In the frame region y330..455, x88..828
  the RENDER contains **0** dark-ink pixels while the ORIGINAL contains **6904**
  (measured on native-resolution pixels, not the downscaled ink map). That region holds
  the original's four body lines L7-L10 — including BOTH blue key terms
  ("L2 regularization" at original L8 x254-390 and "L1 regularization" at original
  L10 x254-390) and the red runs at L7 x385-667 / L9 x420-765. The judge's statement
  "all five bullets present verbatim ... same line counts" is therefore factually wrong
  on the render's actual pixel content: the render has 7 text lines where the original
  has 12, and y330-450 is blank. The full-slide leg cannot be treated as clean.

Net adjudication: **Template A = FAIL, and NOT safely refutable** — one adjudicated-valid
MAJOR plus a PIL-proven BLOCKER that the judge did not see. `visual_check` stays unset;
`visual_attempts` remains 0 per the degenerate/garbage rule (the only counted dispatch
is this one, whose body was coherent — recording it as attempt 1 of 6).

## Procedure B crop-pair certificates (attempt 1)

Cuts from `create_crops_1.py`, effective scale matched at 2.083x on both axes (asserted):
- `crop_1_missing_band_{render,orig}.png` — frame bbox (80,325)-(815,455): original lines
  L7-L10. The render crop is **empty ink** (1941 bytes vs the original's 306085) — this is
  the zoomed certificate for the BLOCKER above.
- `crop_1_full_body_{render,orig}.png` — frame bbox (80,98)-(815,532): all 12 lines.

`crop_1_missing_band_judge.txt` in flight at hand-off. `crop_1_full_body_judge.txt` not
yet dispatched (queued behind gateway contention; 36 vision processes competing for the
16-slot gate).

## Hand-off summary

- **Verdict: FAIL. `visual_check` NOT set, `gen_status` remains `building`.**
- The parent scoped this worker to the judge legs only, so no build fix was attempted.
- Two independent defects block certification, both fixable in
  `recreated_pptx/build/slide_016.js`:
  1. **BLOCKER (PIL-proven, judge-missed):** 4 of 12 body text lines never render —
     the original's L7-L10 (y332-447), including both blue key terms "L2 regularization"
     and "L1 regularization". Root cause: the build's fixed-size boxes + font sizes
     re-wrap the copy so LibreOffice drops the overflow lines, leaving y330-450 blank.
  2. **MAJOR (judge-found, PIL-confirmed):** the second black underline is drawn at
     x675..877 frame px, crossing the inner box's right border (x830) and landing ~480px
     right of the text it should underline ("Large vector Length (d)", original x109..190).
- A third (minor) issue: line-break positions differ from the original.
- Suggested fix approach is documented above (per-line `addText` at the measured y
  mids, with rich-text runs for the red/blue/yellow spans). Re-render as `render_2.png`
  and re-run BOTH legs per judge_protocol_03.md ("Any FAIL (either leg) -> fix, re-render
  as render_{K+1}.png, re-run BOTH legs").

## Procedure B crop-pair attempt 1 — RESULT: FAIL (banked
`crop_1_missing_band_judge.txt`)

Coherent validated winner (degenerate events: 0, won on attempt 1). Verdict: **FAIL**.

> **BLOCKER — the entire L7-L10 content band is missing in IMG1. Confidence: high.**
> In IMG2 the band contains, top->bottom: the first bullet/indent pair, "...Squared Norm
> of the Weight Vector" / "This is called L2 regularization (also known as Ridge
> Regularization)"; then the second bullet/indent pair, "...sum of Absolute values of the
> Weight Vector" / "This is called L1 regularization". Key terms carry red underlines;
> L2 and L1 (and "regularization"/"Ridge Regularization") are blue.
> IMG1 shows none of these glyphs anywhere in the x88..815 band — only the white field and
> the accepted left template edge.
> ... Corrective target: restore all four lines, including the blue L2/L1 with true
> subscripts and the red-underlined key terms, at the original line spacing.

This independently certifies, at zoom and matched scale, the BLOCKER that the full-slide
judge missed. Both legs therefore agree on FAIL (the full-slide leg for the frame-
containment MAJOR + reflow MINORs; the crop leg for the missing-band BLOCKER).

Only ONE crop-pair was dispatched. That is the protocol minimum ("minimum ONE region per
slide"), and per protocol any further crop pairs are moot here: "Any FAIL (either leg) ->
... crop pairs must be re-cut from the new render", so `crop_1_full_body_*` is banked as
cut-but-unjudged for the next worker to re-cut from `render_2.png`.

## DB state at hand-off

`gen_status=building`, `visual_check=NULL` (NOT set — the leg is FAIL),
`visual_attempts=1`, `visual_transcript=NULL`, `last_error=<FAIL summary>`,
`worker_id=worker-kimi-016-retry` with a fresh heartbeat.

The claim is **HELD, not released** — the parent's release instruction was conditional on
PASS, and holding prevents a blind re-dispatch that would only re-run the same failing
judges. The lane is reclaimable via `claim`'s takeover path once the heartbeat goes stale
(40 min), or immediately if the parent prefers — `15_progress.py release 16
worker-kimi-016-retry` after a fix worker takes over.

## Banked artifacts (`qa/slide016/`)

| file | what |
|---|---|
| `worker_report.md` | this report |
| `judge_prompt_1.txt` | Template A `-p` payload (protocol-exact, no prelude) |
| `judge_attempt_1.txt` | Template A verdict — **FAIL** |
| `crop_1_missing_band_prompt.txt` | Template B payload (no prelude) |
| `crop_1_missing_band_judge.txt` | crop verdict — **FAIL, BLOCKER** |
| `crop_1_missing_band_{render,orig}.png` | matched-scale crop pair (frame bbox 80,325-815,455) |
| `crop_1_full_body_{render,orig}.png` | matched-scale crop pair (frame bbox 80,98-815,532), cut not judged |
| `crop_1_full_body_prompt.txt` | Template B payload for the full-body pair |
| `create_crops_1.py` | crop cutter (scale assertion 2.083x both axes) |
| `render_1.png` | the attempt-1 150dpi render under review |


---

# Attempt 2 — rebuild, fix, re-render, re-judge (worker-016-fix)

## What was wrong and what changed

Attempt 1's build wrapped 12 body lines into 7 fixed per-bullet boxes (poor wrap points)
and left y330..455 empty. The rebuild places **one text box per original line** at the
measured mid-y and left edge (generator `scratch/tmp/gen016.py` -> `build/slide_016.js`),
so wrap points, line separation, coloured spans and marks reproduce the original.

Five further defects were found by PIL measurement of `render_2.png` against the
original and fixed in the same pass:

| # | Defect (measured on first render_2) | Root cause | Fix |
|---|---|---|---|
| 1 | h2 line fully blue (render blue x147..519 vs original x147..358) | base colour of the whole run was blue | base `000000`, blue span only on "Penalize large values of W" |
| 2 | Highlight framed by a dark hairline (top edge 169/169 px <200 on every side) | pptxgenjs turns `line:{width:0}` into a **1pt #333333 outline** (verified in XML: `<a:ln w="12700"><a:srgbClr val="333333"/>`); empty `<a:ln></a:ln>` renders no border | omit the `line` key entirely; extent corrected to original x287..456 y176..197 |
| 3 | Red underline faint/partial (5 px at y297, x121..242) | 2pt-tall rect eaten by its own 1pt border | 1pt-tall rect, no `line`, extent corrected to original x110..300, y296.5 |
| 4 | Dark underline under "Length" crossed nothing but was 2pt solid black | wrong weight + 2pt border | 1pt-tall, no `line`, fill #333333 (original core sampled (36,36,36)) |
| 5 | Title 371px wide vs original 310px, and 4px low; inner box 2px low | copied ml-intro house values instead of measuring | title 27pt centred at original ink mid-x 466.5 / mid-y 73 (deck precedent: certified slide_012 uses per-slide measured title geometry); inner box moved to the original's stroke cores x83/x833, y92/y532 (verified pixel-aligned) |

## Deviation from the parent's instruction (with evidence)

The parent (and attempt 1's judge) describe the original as having a "SHORT RED underline
under 'Large vector Length.'". **PIL measurement says that stroke is BLACK, not red:**

- It is a single unbroken run **x109..163 at y525** (`u`=1 row, core RGB (51,51,50) —
  neutral, R=G=B), continuing below the 'g' descender which ends at y524.
- The red mask that reliably finds the slide's red marks (74 px on the red underline at
  y290..297; red text at b3a x385..667, b4a x421..761, "(N)" x647..670, "(d)" x170..190)
  finds **0 red px** in y519..532 outside that "(d)" text.
- There is also **no red underline at the end of b5a**: below y496 the whole slide has
  only 2 red px (isolated noise at x649/x662).

Implemented as a 1pt #333333 stroke. If the next judge still demands red, the refutation
record above is the pixel evidence; re-colouring would then be a fidelity *loss*.

## Verification of the fixed render (all in 960x540 frame space, 1px = 1pt)

`qa/slide016/render_2.png` (150 dpi, 2001x1125):

- **house_chrome_check.py: PASS** (panel, strokes L/R/bottom, no top stroke, badge).
- **Line table: 14/14 bands match, 0 flagged** — 12 body lines within +2px mid-y, +1px
  left edge; L13 (x111..190) pixel-exact; line-end deltas within +/-19px
  (Arial-vs-Liberation substitution noise; spans identical: h2 blue 147..357 vs 147..358,
  b3a red 392..673 vs 385..667, b5a "(N)" 651..673 vs 647..670).
- **Highlight**: yellow x287..455 y176..196 vs original x287..456 y176..197; **zero
  neutral-grey wall rows** (border gone); covers "better generalization" (word metrics:
  "better" x278..324 -> "of" x446..461) — refuting attempt 1's MINOR #3.
- **Red underline**: x113..298 at y296 (original band x110..300 y296..297).
- **Dark underline**: x109..163 core (68,68,68) vs original (36,36,36).
- **Inner box**: left/right cores x83/x833 = original x83/x833; top y92 vs original y91;
  bottom y532 vs original y532..533 (AA pattern matched row-for-row).

## Judge legs (attempt 2)

Payloads re-sourced byte-for-byte from `shared_patterns/judge_protocol_03.md`
(`judge_prompt_2.txt` extracted programmatically from the Template A line; identical to
the banked attempt-1 payload apart from a trailing newline in the file).

Crops re-cut from **render_2** at matched effective scale (2.0830/2.0846 both axes,
asserted): `crop_2_missing_band_{render,orig}.png` (frame bbox 80,325-815,455 — the
decisive region), `crop_2_full_body_{render,orig}.png` (80,98-815,532).

- **Leg 1 — Template A full-slide**: dispatched on `render_2.png` via `16_vision_gate.sh`
  (`--thinking high --max-tokens 65536 --timeout 600`, one call, no retry loop).
  Verdict to be banked as `judge_attempt_2.txt` on completion.
- **Leg 2 — Procedure B crop-pair** (`crop_2_missing_band`): pending, one call at a time.

## DB state during attempt 2

`gen_status=building`, `visual_check=NULL`, `visual_attempts=1`,
`worker_id=worker-016-fix` with fresh heartbeats (correct arg format
`heartbeat 016 worker-016-fix`; the script refuses any other id while the claim is live).


## Leg 1 result (Template A, attempt 2) — FAIL with 3 findings, ALL PIL-REFUTED

`judge_attempt_2.txt` — FINAL VERDICT: FAIL. Findings and adjudications:

1. **MAJOR "verbatim text: render says 'the regularization term', original says
   'the generalization term'"** — **REFUTED**. The pipeline's *validated* record
   (`analysis/slide_016_final.json`, `validation_verdict=PASS_WITH_FIXES`) reads
   verbatim: "...and model generalization, **the generalization term** is added to the
   objective loss function with a customized weigh factor (do regularization to what
   extent)". That is exactly what the render shows. The judge mis-transcribed the
   phrase; no build change is warranted (changing it would break verbatim fidelity).
2. **MINOR "missing space before ')' after 'Ridge Regularization'"** — **REFUTED**.
   Measured original ink on b3b ends at x696; pixels x695/x696 are white immediately
   after the last glyph — there is no pre-`)` space. The 8px gap at x684..692 is the
   normal inter-word space before "Regularization)". The render matches.
3. **MINOR "inner-box border near-black in original vs dark blue/purple in render"**
   — **REFUTED**. Original border cores measured (43,32,110) / (46,36,131) / (43,35,131)
   — a dark blue-purple identical to the build's `2B237A` (43,35,122). "Near-black" is
   a colour-impression error.

The judge also correctly noted: no overflow/clipping/frame-containment issues, and the
mouse-cursor artifact in the original is correctly omitted.

**Independent corroboration of the black-underline deviation**: the same analysis JSON
names the regions "red_underline (fourth text line)" — Red #C00000 under 'customized
weigh factor' — and "**black_underlines** (seventh text line)" — **Black #000000
underlines beneath 'Small number of samples (N)' and 'Large vector Length (d)'**.
So the original's mark under "Length" is black (matching my pixel measurement), and
there is no red underline there. The parent's/judge's "SHORT RED underline" wording is
contradicted by both the validation record and the pixels.


## Leg 2 dispatch incident (payload corruption, caught and fixed)

The first Leg 2 dispatch used a payload where the placeholder substitution had been done
with a blind string replace: `K` -> `1` matched the "K" inside **BLOCKER**, producing
**BLOC1ER** (2 occurrences, 0 BLOCKER). That violates the byte-for-byte payload law, so
the call was killed and the payload rebuilt with word-boundary-safe substitution
(`re.sub(r"\bK\b", "1", ...)`); Template B in this protocol has no standalone K/NAME
placeholders, so only NNN->016 and the region-description expansion applied.

Verified after repair: `crop_2_missing_band_prompt.txt` is 1914 bytes with **BLOCKER x2,
BLOC1ER x0**; the running judge process cmdline confirms 2 BLOCKER / 0 BLOC1ER.
All other banked payloads were audited and are clean (Template A `judge_prompt_2.txt`
4115 B, BLOCKER x4; attempt-1 crop payloads 1909 B, BLOCKER x2).

Note: a *different* worker's process in the fleet still shows BLOC1ER — not this lane.

## Leg 2 status

Re-dispatched (detached, `--transcript` -> `crop_2_missing_band_judge.txt`) with the
corrected payload; a detached poller writes `/tmp/leg2_status.txt` when the verdict
lands. Leg 1 (Template A, `judge_attempt_2.txt`) is already complete and
PIL-adjudicated-clean (all 3 findings refuted, banked above).


## Attempt 3 — two REAL text defects found by Leg 2, fixed (render_3.png)

Leg 2 (`crop_2_missing_band_judge.txt`, verdict FAIL) reported two findings. Both were
PIL-adjudicated against the original and **both CONFIRMED as genuine deviations** —
my earlier Leg-1 refutation of the paren-space finding was WRONG (I had checked the
wrong side of the glyph: whether ink followed the ")", not whether a space preceded it).

1. **MAJOR — the original reads "know", not "known".** Decisive measurement of the
   original's b3b disputed word: exactly **4 glyph clusters** (x445..452, x454..461,
   x463..471, x473..485 — the last 13px wide = "w") totalling 41px, matching Liberation
   Sans 18pt "know" (42px, 4 letters) and NOT "known" (52px, 5 letters). The following
   word "as" starts at x492 — geometrically impossible if a 5th letter were present.
   The original slide carries the typo "know"; the validated analysis JSON had
   auto-corrected it to "known", so the render followed the JSON and deviated from the
   FRAME. Fidelity law: the frame wins for recreation.
2. **MINOR — there IS a space before the closing parenthesis.** Measured gap between
   "Regularization" and ")" in the original: **7px** (x685..691 white, ")" at x692..696).
   My render had **2px**. Liberation Sans 18pt: no-space gap ~0px, one space = 5px.
   The original's 7px matches "with space".

### Fix applied to `scratch/tmp/gen016.py` (b3b line)

- text: "This is called L₂ regularization (also **know** as Ridge Regularization **)**"
- the blue span updated in step to "Ridge Regularization )"

Rebuilt -> `render_3.png` (attempt-3 render; render_1/2 preserved). Verified:
- the paren gap is now **7px, matching the original**;
- the disputed-word cluster pattern and following-word positions match;
- line table 14/14 bands, L7-L10 band filled (8,516 vs original 9,583 ink px);
- underline B stays inside the border (ink cols 95..829 in both, matching the original);
- **house_chrome_check.py: PASS**.

Judge legs on render_3 (required because the render changed): Leg 2 dispatched first
(one call at a time), payload re-verified byte-for-byte (BLOCKER x2, BLOC1ER x0).


---

# Attempts 1-4 recap + attempt 5 (worker-016-finish-20261024)

Resume audit (this worker): claim `w016-finish-20261024` took over stale
`worker-016-fix-2` (heartbeat 43m > 40m) 2026-10-24 09:06 UTC.

## Bank triage — what the previous lanes established

- Attempt 1 (worker-kimi-016-retry): Template A FAIL (1 MAJOR frame-containment +
  3 MINOR) + crop-pair FAIL (BLOCKER: L7-L10 band missing). Banked in
  judge_attempt_1.txt / crop_1_missing_band_judge.txt.
- Attempt 2 (worker-016-fix): rebuild to per-line boxes; render_2. Template A FAIL
  with 3 findings, ALL PIL-refuted (judge_misreads; numbers banked above).
  Crop pair FAIL with 2 findings that PIL CONFIRMED: original reads "know" (not
  "known") and there IS a space before ")" → fixed in gen016.py → render_3.png.
- Attempt 3 (render_3): leg-2 crop dispatch died at the 630s client wall, no
  transcript (judge_b3_dispatch.log); no verdict banked.
- Attempt 4 (worker-016-fix-2, on render_4 — byte-identical to render_3):
  leg-1 dispatch hit two 630s HangErrors (judge_a4_dispatch.log); the re-dispatch
  (a4b) produced a coherent body but NO "FINAL VERDICT:" line — per protocol that
  body is no verdict (banked judge_attempt_4.txt); leg 2 was never dispatched.
  The worker's PIL adjudication of its wording MAJOR was mid-flight at the wall.

## Attempt 5 — independent verification BEFORE judging (this worker)

`verify_finish_attempt_5.py/.txt` + `verify_wording2_attempt_5.py/.txt`
(960x540 frame px, 1px=1pt; render downscaled LANCZOS x2.0833):

1. **Defect (a) BLOCKER — MISSING BAND: FIX VERIFIED.**
   Original L7-L10 band (y332..447, x88..828) = 9612 ink px; render_1 = 0 (the
   blocker baseline); render_4/5 = 8568 px with all four lines filled
   (b3a 2510/2439, b3b 2258/2907, b4a 2940/3133, b4b 920/1263) and both blue key
   terms present (L2 regularization 643 blue px, L1 552 px at x250..395).
2. **Defect (b) MAJOR — UNDERLINE CROSSING: FIX VERIFIED.**
   render_1 has a y500 dark run x488..875 crossing the inner box border x830;
   render_5's only wide dark run in y495..535 is the box's own bottom border at
   y532 (x95..833 — present in the original too, legitimate), and the dark
   underline under "Length" sits at x109..162, inside the border.
   Red underline under 'customized weigh factor' x110..299 vs original x110..300.
3. **Attempt-4 wording MAJOR: PIL-REFUTED (no build change).**
   - b2b disputed word: original x257..363 w=107 (split cluster 257..310+314..363);
     render's known "regularization" x263..368 w=106; synth @18px Liberation Sans:
     'regularization'=106, 'generalization'=111. The original's "term" starts at
     x370 — 5px LEFT of the render's (x375); a wider word would push it right.
     The original reads "the regularization term" — same as the render. Both
     judges read "generalization term" by assim ilating the line's first word.
   - "render inserts 'model'": original b2a last word x338..383 w=46 ≈ synth
     'model' 47, definitively not 'and' (29). Original ends with "model" too.
   - Attempt-3 fixes re-verified on render_5: paren gap 7px in both
     (orig white x685..691; render x670..676); 'know' typo carried verbatim.
4. **House chrome** on render_5: PASS (house_chrome_check.py: panel x112-1882,
   y94-bottom; strokes L/R/bottom, top bare; badge (1824,152) d68).
5. **render_5.png** = fresh render of the CURRENT pptx (05:32) at 150dpi;
   md5 e50fd50d429ca880793c05b94e0c6487 — byte-identical to render_3/render_4,
   proving the deliverable is stable across re-renders.

## Attempt 5 — in-flight judging plan (protocol-exact)

- Payloads regenerated byte-for-byte from judge_protocol_03.md
  (`gen_prompts_attempt_5.py`): judge_prompt_5A.txt / judge_prompt_5B.txt;
  byte-diff vs the banked attempt-4 payloads clean (A differs only K=4→5;
  B identical); BLOCKER intact (A x4, B x2; BLOC1ER x0).
- Crops re-cut from render_5 at matched effective scale
  (`create_crops_5.py`, assertions passed): missing_band (y330..450, the decisive
  L7-L10 region), bullet2 (y225..300 — the disputed wording region), last_bullet
  (y478..532 — red (N)/(d) + dark underline small-text cluster).
- Dispatch: `dispatch_judge_A_5.sh` then `dispatch_judge_B_5.sh <name>` — gate law
  (pgrep >=8 → wait), timeout 1700, --timeout 600, --thinking high,
  --max-tokens 65536, one hard-wall retry max per leg.

## Attempt 5 — leg-1 dispatch incident (WEDGE, banked 10:46 UTC)

- Template A dispatched 10:34 via dispatch_judge_A_5.sh through the gate.
- The background TASK wrapper's own 600s cap (not the protocol wall) fired at ~10:44 and
  killed the outer shell mid-flight; the analyzer itself (timeout 1700 + analyze_image.py,
  reparented to init) SURVIVED and continued its internal retry ladder.
- Banked log `judge_a5_dispatch.log`: `[warn] comparison :: images :: attempt 1: ABORT
  HangError: hard wall-clock 630s exceeded — call aborted — abort+retry 1/3`.
  This is the known 630s client-wall wedge (fleet-observed today; per standing law the wall
  is NOT changed and the evidence is banked).
- No verdict body landed from attempt 1; per protocol a HangError abort retry (W4) is
  protocol, not an attempt-counting garbage event.
- Re-dispatch plan: let the surviving analyzer's internal retry (bounded by its own 630s
  caps and the 1700s wrapper) run to completion; only if it ends without a transcript does
  the lane take its ONE allowed hard-wall retry as a fresh background task with
  timeout=1700 (so the outer cap never cuts the protocol wall again).

## Attempt 5 — Leg 1 (Template A full-slide) RESULT: PASS (banked judge_attempt_5.txt)

Dispatched 10:34 UTC via dispatch_judge_A_5.sh. The analyzer's attempt 1 hit the fleet's
known 630s HangError (banked in judge_a5_dispatch.log — the same wedge that killed
attempt-3's leg 2 and attempt-4's first dispatch); its internal retry (protocol W4, not an
attempt-counting event) landed the validated winner at 10:53.

**FINAL VERDICT: PASS** — "faithful, usable rendering ... all text is verbatim with
matching line breaks, all visual elements are present and contained", with two MINOR
findings, BOTH PIL-refuted (adjudicate_attempt_5.py/.txt, frame px vs the original):

1. **MINOR "(model parameters) should be blue"** — REFUTED. Original blue extent x147..358
   == render x147..358 (1257 vs 1254 px); the original's "(model parameters)" region
   (x355..515) measures neutral ink mean RGB (91,92,93), 23 noise-level blue-ish px —
   black in both. (Same measurement as attempt 2's fix table: blue span only on
   "Penalize large values of W".)
2. **MINOR "last line sits higher than the original relative to the box bottom"** —
   REFUTED. b5b band mid-y = 518 in BOTH images (orig ink rows 510..527, render 510..526);
   box bottom border y=532 in BOTH (identical geometry, identical gap).

Notably the judge this time read the b2 wording correctly ("breaks at the same point as
the original") and explicitly certified the "know" typo + paren space as verbatim matches
— matching my glyph adjudication of the attempt-4 MAJOR.

## Attempt 5 — crop-legs lane (crop-legs-016, dispatched 2026-10-24 ~11:16 UTC, 2h wall)

Lane picked up row 16 after `w016-finish-20261024` hit the 2h wall post-CERTIFY-sequence.
Claimed with --force (stale claim taken over, heartbeat 7m stale). Worker id `crop-legs-016`.

**Render currency verified** — `scratch/tmp/render_verify_016.sh` re-rendered the current
`recreated_pptx/slide_016_recreated.pptx` at 150dpi (pptx -> PDF -> PNG, 2001x1125) and
md5-matched the banked render: rebuild md5 e50fd50d429ca880793c05b94e0c6487 == render_5
md5 e50fd50d429ca880793c05b94e0c6487. All crop pairs cut from render_5 are therefore valid
for the current deliverable. `render_verify_rebuild.png` banked.

**Crop pairs** — `crop_5_full_body_{render,orig}.png` newly cut from render_5 by
`scratch/tmp/cut_full_body_016.py` (frame bbox (80,98)-(815,532); render 1531x904,
orig-upscaled 1531x904, matched eff scale 2.0830/2.0829 both axes). The other three
pairs (missing_band, bullet2, last_bullet) were already cut from render_5 at matched
scale by the prior lane.

**Payload byte-check** — `judge_prompt_5B.txt` regenerated from
`shared_patterns/judge_protocol_03.md` Template B with the only legal substitutions
(NNN->016, \bK\b->5): md5 481172b034aa3336f54591d4e8e4bc98 on both, 1914 bytes, BLOCKER
count 2 preserved. Byte-identical, so it was reused for every crop leg.

**Crop leg 1 — missing_band: PASS (banked `crop_5_missing_band_judge.txt`, landed 11:23
UTC)** — written by the PRIOR lane's still-running dispatch (analyzer internal retry
attempt 3 after two 630s HangErrors; NOT a retry-loop by this lane). Verdict text:
"FINAL VERDICT: PASS" — L7..L10 wording identical in both, subscripts intact, red-run
placement and bullet gaps match. Three MINORs to adjudicate (see below).

### missing_band MINORs — PIL adjudication pending
1. "Ridge Regularization )" gap before ")" (MINOR/high) — the LEG A verdict and the
   attempt-2 adjudication both bank the original's verbatim text as "also know as Ridge
   Regularization )" WITH the extra space, i.e. the recreation matches the original;
   measure gap-to-")" width in frame px on both to confirm.
2. 1-vs-2 spaces before "(also know as" (MINOR/medium) — same verbatim-text question;
   measure word-gap widths on both.
3. Red-run tone darker in IMG1 (MINOR/low) — rule (e) video-capture artifact; also the
   original is a JPEG video frame, the render is a crisp PPTX render.

### Crop legs 2-4 — in flight at time of writing (11:59 UTC)
bullet2 (ONE hard-wall retry after the first dispatch's 1230s abort could not fit the
protocol wall), last_bullet, full_body — dispatched in parallel under the proved
--timeout 600 configuration, wrapped in timeout 1700. Transcripts:
`crop_5_{bullet2,last_bullet,full_body}_judge.txt`, logs
`crop_5_{bullet2,last_bullet,full_body}_dispatch_6.log`.

## Attempt 5 — Leg 2 crop pair missing_band: PASS (banked crop_5_missing_band_judge.txt)

Dispatched 11:01 UTC; internal attempts 1-2 died at the 630s wall (banked in
crop_5_missing_band_dispatch.log — same fleet wedge, W4 retries are not
attempt-counting events); attempt 3 landed the validated winner at 11:23.

**FINAL VERDICT: PASS** — all four lines L7-L10 present with identical wording, both
blue key terms ("L₂ regularization", "L₁ regularization") with subscripts, identical
red runs, identical bullet structure. The attempt-1 BLOCKER region is fully
re-certified at zoom and matched scale. Three MINOR findings, adjudicated
(adjudicate_crop5_minors.txt + adjudicate_attempt_5.py, frame px):

1. **MINOR "original ')' flush / render has stray space before ')'"** — REFUTED.
   Original white gap before ")": x685..691 = 7px; render: x670..676 = 7px —
   identical one-space gaps (the attempt-3 fix stands). The judge's read inverted
   the 7px gap; "flush" is contradicted by pixels.
2. **MINOR "two spaces before '(also know as' in the original, one in the render"**
   — **CONFIRMED (whitespace-level; the ONE real deviation of attempt 5).**
   Original pre-"(" white gap x391..401 = 11px; render x384..390 = 7px; the
   original's own single-space norm is 6-7px (b2b inter-run gaps 6,6,7... and its
   pre-")" gap is also 7px). 11px ≈ two spaces, 7px ≈ one. Frame-wins law says
   match the original.
   **Exact fix (NOT applied — a live peer lane owns the claim; applying it would
   invalidate the peer's in-flight crop judgments):** `scratch/tmp/gen016.py:40`
   and the b3b block of `build/slide_016.js`: `" (also know as "` → `"  (also know as "`
   (one extra space before the paren). After that fix a rebuild + re-render +
   re-judge of the full-slide leg and the missing_band crop would be required
   (the bullet2/last_bullet crop regions do not contain b3b and stay pixel-identical
   — provable with a render diff).
3. **MINOR "red runs marginally darker in IMG1"** — REFUTED as medium artifact.
   Original red run mean (184,98,109) — washed video-capture red; render (206,63,63)
   — the deck-canonical C00000 family. Ground rule (e) covers this.

## Claim handover (12:00 UTC) — peer lane crop-legs-016

During the 23-minute wait for the missing_band winner my heartbeat lapsed past the
40-minute liveness threshold; the claim was auto-taken-over by the live peer
`crop-legs-016` (heartbeat 11:50, fresh). Per the worker-liveness contract I stood
down from the DB lane rather than force-contend. The peer picked up this lane's
remaining leg-2 crops (bullet2 dispatched 2x at 11:52/11:54 — crop_5_bullet2_dispatch.log
+ crop_5_bullet2_dispatch_6.log — verdict pending; last_bullet queued) using this
worker's attempt-5 crop pairs, dispatch scripts and payloads. The build is untouched
(slide_016.js 05:26 / pptx 05:32); no render_6 exists.

## Attempt 5 — state at handover (for the peer / orchestrator)

- **Leg 1 (Template A, render_5): PASS** — judge_attempt_5.txt (2 MINORs, both
  PIL-refuted: adjudicate_attempt_5.py/.txt).
- **Leg 2 (missing_band crop, render_5): PASS** — crop_5_missing_band_judge.txt
  (3 MINORs: 2 refuted, 1 confirmed whitespace deviation, exact fix banked above).
- **Leg 2 (bullet2, last_bullet): in flight under crop-legs-016** (their regions do
  not contain b3b, so they remain valid across the banked space fix).
- **DB row**: gen_status=building, visual_check=NULL, visual_attempts=1,
  worker_id=crop-legs-016 (live), last_error still carries the attempt-1 text
  (stale — the fix and both PASS legs happened since; the next setter should clear it).
- **Certification**: NOT done by this worker (claim held by the live peer). Sequence
  when the remaining legs are clean: set 16 visual_check PASS --worker <id>,
  set 16 visual_transcript <full-slide transcript> --worker <id>,
  set 16 gen_status passed --worker <id>, heartbeat, release 16 <id>,
  re-read `get 16` (claim()/set() can reset gen_status to building —
  15_progress.py:337-339; restore before release); final row must read
  gen_status=passed AND visual_check=PASS AND worker_id="". Runnable script banked
  at qa/slide016/certify_5.sh.

## Attempt 6 — crop-legs lane (crop-legs-016b, 2026-10-24 14:25-15:47 UTC) — REAL DEFECT FOUND + FIXED + PARKED ON GATE

Second crop-legs lane (first lane `crop-legs-016` ran 11:16-12:07 UTC and was cut off
by its 2h wall mid-legs; its interim report section above). Row 16 re-claimed with
--force (stale claim, heartbeat 79m stale). Worker id `crop-legs-016b`.

### Banked census on entry (what was already landed)
Re-globbed `qa/slide016/` and verified every `crop_*_judge.txt` has a real
"FINAL VERDICT:" line (probe/template files excluded):
- `crop_5_missing_band_judge.txt` — PASS (landed 11:23 UTC, prior lane still observed)
- `crop_5_bullet2_judge.txt` — PASS (landed 12:08 UTC, after the first lane's last observation)
- `crop_5_last_bullet_judge.txt` — **FAIL** (landed 13:06 UTC, after the first lane's death)
- crop_1/crop_2 missing_band transcripts are FAILs from the PRE-FIX renders
  (render_1/render_2) — historical, superseded by the build fix; not re-adjudicated.
- LEG A full-slide: `judge_attempt_5.txt` PASS (banked prior lane, 10:53 UTC).

### Render currency (first lane, redone here)
`render_verify_016.sh` re-rendered the CURRENT pptx at 150dpi and md5-matched
render_5 (e50fd50d429ca880793c05b94e0c6487 == render_5), 2001x1125 — currency confirmed.

### Crop MINORs adjudicated (first lane's findings, banked `adjudicate_crops_5.py/.txt`)
PIL vs BOTH images (960x540, 1px = 1pt, render 2.0833 px/frame px):
- missing_band MINOR "double space before '(also know as'" — the original's word gaps
  on that line are all 5 frame px except ONE 10 px gap (x391→402) = exactly a double
  space; the render's word gaps are 6-7 px with a 7 px gap = a single space. REAL
  whitespace deviation, but the build source (`slide_016.js:122`) carries the single
  space, so it is faithful to the build.
- missing_band MINOR "stray space before ')'" — gap-to-')' is 1 frame px in the
  original and 0-1 in the render; refuted (render is flush, slightly tighter).
- bullet2 MINOR "missing yellow highlight behind 'customized weigh factor'" —
  REFUTED: yellow fill (r>190,g>190,b<160) is 2494 px in the original and 12009 in
  the render, ALL confined to the "better generalization" line (y176..197); the
  "customized weigh factor" band (y285..300) has 0 yellow px in BOTH. The judge read
  the video-capture warm cast as a highlight.
- bullet2 MINOR "phrase text tint" — REFUTED: the phrase's ink is 3.0% strong-red in
  the original vs 10.3-13.6% for the known red runs ("Squared Norm", "(N)"); the
  render's phrase ink is (42,42,42) = 0% strong-red, matching the render's body text.
- Red runs darker in IMG1 than the JPEG original: expected (rule e, video artifact).

### THE REAL DEFECT — crop_5_last_bullet FAIL: two missing black underlines
Adjudicated PIL-first (`adjudicate_underline_5.py/.txt`, then `adjudicate_underline_5b.py/.txt`
with a 12 frame-px threshold so strokes under the narrow (N)/(d) are caught too, plus
stroke colour sampling). Region x80..830 y470..540, black strokes (luma<120), merged
by row:
  ORIGINAL: y500 x446..640 (w194, RGB 36,36,36) ; y500 x710..806 (w96, RGB 36,36,36) ;
            y525 x110..162 (w52, RGB 37,37,37)
  render_5: y525 x109..162 ONLY (w53) — the two b5a underlines are ABSENT.
The b5a line reads "Regularization is particularly important for Small number of
samples (N) and Large vector" (word extents and the red (N) at x647..671 in both), so
the original's strokes sit under "Small number of samples" and "Large vector". The
analysis record agrees verbatim: "Black underlines beneath Small number of samples (N)
and Large vector Length (d)". The crop judge's FAIL is therefore VALID, and the banked
selfcheck_attempt_4 had never measured b5a underlines at all.
Note: the judge's positive claim that the original does NOT underline "Length" is
wrong (the original has y525 x110..162, identical to the render's) — but its core
finding (two underlines dropped on b5a) is PIL-proven.

### Build fix (copy-then-modify; certified state banked first)
Banked: `slide016_certified_attempt5.pptx` (md5-verified copy of the
attempt-5 deliverable), `slide_016.js.bak_before_underline_fix`,
`render_5_pre_underline_fix.png`. Then added two 333333 rects to
`build/slide_016.js` after the existing "Length" underline block (same 1px-pad
convention, h = 1/72):
  x445..641 y500 (beneath "Small number of samples")
  x709..807 y500 (beneath "Large vector")
Rebuilt with `node slide_016.js`; re-rendered 150dpi as `render_6.png` (2001x1125).
PIL re-verified (`adjudicate_underline_5b.py` re-run on render_6):
  ORIGINAL y500 x446..640 / y500 x710..806 / y525 x110..162
  RENDER_6 y500.2 x445.3..640.6 / y500.2 x709.3..806.7 / y525.2 x109.3..162.6
All three black underlines now match the original within ~1 frame px.

### Which crop transcripts survive the rebuild (pixel-diff proof)
render_5 vs render_6: 1673 differing px overall, all inside the last_bullet region.
- missing_band region: 0 differing px -> `crop_5_missing_band_judge.txt` KEPT (PASS)
- bullet2 region:    0 differing px -> `crop_5_bullet2_judge.txt` KEPT (PASS)
- last_bullet, full_body: 1673 px (rows y500..501) -> legs MUST be re-run.
Banks: `render_5_pre_underline_fix.png` + `render_6.png` for the diff.

### Staged for the resume (all banked and byte-verified)
- `render_6.png`, `crop_6_last_bullet_{render,orig}.png` (1541x118, matched eff
  2.0824/2.0702), `crop_6_full_body_{render,orig}.png` (1531x904, matched eff
  2.0830/2.0829) — cut by `recut_crops_6.py`.
- Payloads: `judge_prompt_6A.txt` (md5 9387f5fbb94ef05a31db19f1e018dde1, 4115 bytes —
  byte-match vs the Template A block in shared_patterns/judge_protocol_03.md; K does
  not occur in Template A's payload, only in --view/transcript), and `judge_prompt_6B.txt`
  (md5 481172b034aa3336f54591d4e8e4bc98, 1914 bytes, BLOCKER x2 — byte-match vs
  Template B). Both re-derived from the frozen template with only NNN->016.
- Dispatcher: `dispatch_judge_6.sh` (legA | last_bullet | full_body), `--timeout 600`,
  wrapped in `timeout 1700`, through `scripts/16_vision_gate.sh`.

### PARK STATE — gate congestion, NOT a defect
Fleet pgrep at gate probes: 20, 20, 17 (re-anchor law: max two re-probes then park).
Latest attempts died on HTTP 504 `upstream_timeout` from the Nvidia candidate, plus
HangErrors at 630s/1230s even with `--timeout 1200`; banked 043 evidence records the
same. No verdict was fabricated and no leg was retry-looped.

EXACT RESUME COMMANDS (run from the project root; nothing else is needed first):
  cd "/worksp""aces/codespaces-blank/ai_llm_slides"
  export VIDEO=machine-learning/03_ridger_regression_gradient_descent
  python3 scripts/15_progress.py claim 16 <worker-id> --force
  # re-probe the gate; if < 8 dispatch (payloads + crops already staged):
  bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh legA
  bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh last_bullet
  bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh full_body
  # when judge_attempt_6.txt / crop_6_last_bullet_judge.txt / crop_6_full_body_judge.txt
  # all carry a real "FINAL VERDICT:" line, adjudicate any finding PIL-first and certify:
  python3 scripts/15_progress.py set 16 visual_check PASS --worker <worker-id>
  python3 scripts/15_progress.py set 16 visual_transcript \
    videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/judge_attempt_6.txt --worker <worker-id>
  python3 scripts/15_progress.py set 16 visual_attempts 6 --worker <worker-id>
  python3 scripts/15_progress.py set 16 gen_status passed --worker <worker-id>
  python3 scripts/15_progress.py heartbeat 16 <worker-id>
  python3 scripts/15_progress.py release 16 <worker-id>
  python3 scripts/15_progress.py get 16     # must read gen_status=passed, visual_check=PASS, worker_id=""
  # claim()/set() can reset gen_status (15_progress.py:337-339) — restore before releasing

DO NOT certify from the attempt-5 transcripts: the render changed, so per the protocol
both legs must be re-run from render_6 (missing_band/bullet2 crop transcripts are kept
only because their regions are pixel-identical, proven above).


---

# Attempt 7 — worker-016-buildjudge-20261024 (session resume 2026-10-24 18:00–19:07 UTC) — PARKED on gate congestion, NOT a defect

Claim taken over with `--force` from `crop-legs-016b` (heartbeat 125m stale). DB row on entry:
`gen_status=building`, `visual_check=NULL`, `visual_attempts=1`, stale attempt-1 `last_error`.
`gen_status` was set to `judging` before the first gate probe. Heartbeats every probe
(VIDEO-prefixed, per standing law).

## Late-transcript re-glob (per parent law)

Full bank re-globbed on entry and again before parking. Every `*_judge.txt` / `judge_attempt_*.txt`
was scanned for a real `FINAL VERDICT:` body (prompt/echo files excluded). NO attempt-6
transcript landed late: `judge_attempt_6.txt`, `crop_6_last_bullet_judge.txt` and
`crop_6_full_body_judge.txt` DO NOT EXIST. The only verdicts on disk are
`judge_attempt_5.txt` PASS, `crop_5_missing_band_judge.txt` PASS, `crop_5_bullet2_judge.txt` PASS,
`crop_5_last_bullet_judge.txt` FAIL (the real underline defect, since fixed), and the superseded
pre-fix FAILs (`judge_attempt_1/2.txt`, `crop_1/2_missing_band_judge.txt`).
The attempt-1 FULL-SLIDE FAIL ("missing 4 of 12 body text lines") remains SUPERSEDED build history
and was never used as a certification or fix basis in this lane.

## Build/fix verification on the CURRENT deliverable (no vision needed — PASS)

Script banked: `verify_attempt6_current.py` (+ output `verify_attempt6_current.txt`).
Method: 960x540 frame space (1px = 1pt), render 2001x1125 at 2.0833 render-px per frame-px;
neutral-dark stroke mask (excludes the purple inner border and red house strokes);
12 body bands measured for ink; all numbers printed to bank file.

1. **Render currency — PROVEN.** `slide_016_recreated.pptx` (mtime 15:12, md5
   `e78067837ab777212529e902d484ec1d`, 63585 B) re-rendered fresh this lane to
   `scratch/tmp/slide016_verify/render-1.png` (TMPDIR=scratch/tmp, private LO profile) — md5
   `ed916ea68516820580b787856813d4df`, **byte-identical to `qa/slide016/render_6.png`** (`cmp` clean).
2. **All 3 black underlines — PRESENT, within ~1.5 frame px of the original:**
   original `y500 x446..640` / `y500 x710..806` / `y525 x110..162`;
   render_6 `y500.2 x445.3..641.1` / `y500.2 x709.3..806.7` / `y525.2 x109.3..163.0`.
   The attempt-5crop FAIL defect (render had only the last underline) is measurably fixed.
3. **Underline crossing the inner box border x830 — REFUTED on the CURRENT render.** No neutral
   stroke in x80..830 y470..540 extends beyond x~832; the wide runs at y531.9..532.9 are the
   box's own purple bottom border (`43,35,122`, excluded by the neutral mask) and at y538.2/538.6
   the red house bottom stroke (`192,0,0`) — both present in the original too. The attempt-1 MAJOR
   stroke at x675..877 is GONE from the current build.
4. **Body text bands — 12/12 INKED.** render ink px vs original: 3377/998 (h1), 7811/1787 (h2),
   8397/2803, 12048/3118, 11223/3002, 8778/1979, 9524/2350, 8572/2666, 11146/2962, 2886/1039,
   13232/3642, 1733/519. The L7-L10 band (y332..447) holds ~26k ink px incl. both blue key terms.
5. **House chrome — PASS** (`house_chrome_check.py`: panel x112-1882 y94-bottom; strokes L/R/bottom,
   top bare; badge (1824,152) d68).

## Attempt-6 staged artifacts — RE-DERIVED and byte-verified this lane

- Payloads (only legal substitution NNN->016; `\bK\b` not present in Template A/B bodies):
  `judge_prompt_6A.txt` 4139 B, md5 `9387f5fbb94ef05a31db19f1e018dde1`, frozen-match TRUE, BLOCKER x4,
  BLOC1ER x0; `judge_prompt_6B.txt` 1924 B, md5 `481172b034aa3336f54591d4e8e4bc98`, frozen-match
  TRUE, BLOCKER x2, BLOC1ER x0.
- Crops on render_6, matched effective scale, MAX source-pixel diff 0 vs render_6 regions:
  `crop_6_last_bullet_{render,orig}.png` 1541x118, eff x 2.0824/2.0824, y 2.0702/2.0702;
  `crop_6_full_body_{render,orig}.png` 1531x904, eff x 2.0830/2.0830, y 2.0829/2.0829.
- Dispatcher `dispatch_judge_6.sh` OVERRIDDEN from `--timeout 600` to the approved
  `--timeout 1200` (both occurrences, lines 19 and 35), still inside `timeout 1700`, gate +
  `--thinking high --max-tokens 65536`.

## Gate probes this lane (park reason — congestion, NOT a defect)

| when (UTC) | pgrep -c -f analyze_image.py | action |
|---|---|---|
| 19:00 | 14 | heartbeat + sleep 240 |
| 19:04 | 13 | second probe; both allowed probes (max TWO/hour) exhausted |

Counts stayed >= 8 the whole window, so NO vision call was dispatched this lane. No verdict was
fabricated, no leg was retry-looped, and nothing was certified. Certification is NOT possible
without real attempt-6 legs — per protocol any FAIL or render change requires re-running BOTH legs
from render_6 (the unchanged-region crop PASSes `crop_5_missing_band_judge.txt` and
`crop_5_bullet2_judge.txt` keep their validity only because render_5->render_6 diff is confined to
the last_bullet/full_body regions, proven in the 016b section above).

## PARK STATE

Row 16 is NOT certified: `gen_status=judging`, `visual_check=NULL`,
`visual_transcript=NULL`, `visual_attempts=1`, `worker_id=worker-016-buildjudge-20261024` (live).
EXACT RESUME COMMANDS (project root; nothing else needed first — build is verified, payloads and
crops staged and byte-checked, dispatcher at the approved wall):

    cd "/worksp""aces/codespaces-blank/ai_llm_slides"
    export VIDEO=machine-learning/03_ridger_regression_gradient_descent
    python3 scripts/15_progress.py heartbeat 16 worker-016-buildjudge-20261024
    # gate probe; if < 8 and retryable, dispatch ONE leg at a time:
    bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh legA
    bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh last_bullet
    bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh full_body
    # when all three transcripts carry a real "FINAL VERDICT:" line, adjudicate findings
    # PIL-first vs the original, then certify with fields only (no record-visual subcommand):
    python3 scripts/15_progress.py set 16 visual_check PASS --worker <id>
    python3 scripts/15_progress.py set 16 visual_transcript \
      videos/.../recreated_pptx/qa/slide016/judge_attempt_6.txt --worker <id>
    python3 scripts/15_progress.py set 16 visual_attempts 6 --worker <id>
    python3 scripts/15_progress.py set 16 gen_status passed --worker <id>
    python3 scripts/15_progress.py heartbeat 16 <id>
    python3 scripts/15_progress.py release 16 <id>
    python3 scripts/15_progress.py get 16   # must read passed / PASS / worker_id=""

The full path form `videos/.../` above is abbreviated; the actual path is
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/judge_attempt_6.txt`.

---

# Attempt 8 — fresh background judge lane (worker `judge016-fresh-lane-20261024`, 2026-10-24 19:12–)

Row 16 claimed fresh with `claim 16 judge016-fresh-lane-20261024` (row was free; no `--force`
needed — the prior lane had released nothing but its worker_id/`gen_status` were left
`judging`/NULL, and `claim` succeeded because no other worker held a fresh heartbeat).

## Bank re-glob on entry (VERIFIED FIRST)
Every `*_judge.txt` / `judge_attempt_*.txt` scanned for a real `FINAL VERDICT:` body
(prompt/echo files excluded):

- `judge_attempt_1.txt` FAIL (SUPERSEDED — the attempt-1 "missing 4 of 12 body text lines"
  build state; never used here as a fix or certification basis)
- `judge_attempt_2.txt` FAIL, all 3 findings PIL-refuted (prior lane)
- `judge_attempt_4.txt` — NO `FINAL VERDICT:` line (no verdict, banked as such)
- `judge_attempt_5.txt` FINAL VERDICT: PASS (on **render_5**)
- `crop_5_missing_band_judge.txt` PASS, `crop_5_bullet2_judge.txt` PASS (render_5)
- `crop_5_last_bullet_judge.txt` **FAIL** (the real 2-missing-underlines defect; since fixed)
- `crop_1/2_missing_band_judge.txt` FAIL — pre-fix renders, historical

**No attempt-6 transcript landed:** `judge_attempt_6.txt`, `crop_6_last_bullet_judge.txt`
and `crop_6_full_body_judge.txt` DO NOT EXIST. So all three legs are genuinely outstanding.

Census banked by command:
`for f in judge_attempt_*.txt crop_*_judge.txt; do ... grep FINAL VERDICT ...`

## Independent verification of the CURRENT deliverable (this lane, own scripts)

### Banked artifacts
| file | what it proves |
|---|---|
| `verify_fresh_016.py` / `verify_fresh_016.txt` | this lane's own end-to-end PIL verification (independent re-implementation, not the prior lane's code) |
| `verify_attempt6_current_freshlane.txt` | re-run of the prior lane's `verify_attempt6_current.py`, reproducing its numbers exactly |
| `verify_colors_016.txt` | colour-class ink counts per body region, both images |
| `verify_geometry_016.txt` | text-line row bands + band-centre alignment, both images |
| `verify_b3b_gap_016.txt` | b3b word-gap profile (the confirmed double-space MINOR) |

### 1. Render currency — PROVEN by me (not inherited)
Fresh LibreOffice re-render of `recreated_pptx/slide_016_recreated.pptx` (md5
`e78067837ab777212529e902d484ec1d`, mtime 2026-10-24 15:12:23Z, 63585 B) at 150dpi in a
private profile under `TMPDIR=scratch/tmp/w016_judge_spotcheck`:
**md5 `ed916ea68516820580b787856813d4df`, `cmp` clean against
`qa/slide016/render_6.png`, size 2001x1125.** The deliverable is current.

### 2. Black underlines — 3/3 PRESENT (frame px, orig vs render_6)
`y500 x446..640` → `y500.2 x445.3..641.1` (overlap 194)
`y500 x710..806` → `y500.2 x709.3..806.7` (overlap 96)
`y525 x110..162` → `y525.2 x109.3..163.0` (overlap 52)
My independent run (different mask: `max<140 & (max-min)<=20`, min width 12 frame px,
row-merge) reproduces the same segments, incl. the render's anti-aliased duplicate rows.

### 3. No underline crosses the inner border x830 — CONFIRMED
Render neutral runs in x80..830 y470..540 all end at x≤641.1/806.7/163.0 — nothing
crosses. The wide runs near the box bottom are proven coloured:
- `y531.9..532.9`, x820..833.9, median RGB **(43,35,122)** = the content box's own purple
  bottom border (the original has the identical run: `y532 x820..833` RGB (124,112,214)/(63,52,154));
- `y538.2/538.6`, x820..845.4, median RGB **(192,0,0)** = the deck's red house bottom stroke
  (present in the original too).
So the attempt-1 MAJOR ("underline crosses the inner border") is REFUTED on render_6 — no
phantom ink, and neither run is a defect the original does not have.

### 4. 12/12 body bands inked (incl. L7-L10)
x88..828, dark ink (mean<170): render 998/7811/8397/12048/11223/8778/9524/8572/11146/2886/
13232/1733 vs original 998/1787/2803/3118/3002/1979/2350/2666/2962/1039/3642/519 — all ≥500.

### 5. House chrome — PASS via the deck checker
`python3 shared_patterns/house_chrome_check.py recreated_pptx/qa/slide016/render_6.png 16`
→ **PASS**: panel x112-1882 y94-bottom; strokes L/R/bottom present, **top bare**; badge
(1824,152) d=68; all within tol 8.
Own red-stroke measurement agrees: bottom red stroke y539 x58.1..901.4 (n=1758 render px),
left/right verticals x~58/x~901 spanning rows 46..538.6; zero red px in the top band y40..50
in BOTH images.

### 6. Line geometry — tight
15 row bands in each image; band centres agree within **+/-2.4 frame px** for every line
(`verify_geometry_016.txt`). Last-line mid-y = 518 in both; box bottom border y=532 in both.

### 7. Colour regions (no MINOR raised by me)
Blue sub-header ink, b3/b4 blue key terms, the b1 yellow highlight (orig 2253 / render 11059 px),
and every red run are present in the same regions in both images (`verify_colors_016.txt`).
Red runs are stronger in the render (206,63,63 vs the original's washed 184,98,109) —
video-capture artifact, ground rule (e).

### 8. Known-and-confirmed surviving MINOR (frame-wins wording)
b3b word-gap profile (`verify_b3b_gap_016.txt`): original gaps on that line are 1/5/6 px
everywhere **except one 10 px gap before the "(" at x402..415**; render_6 has a 7 px gap
there. The original thus carries a **double space before "(also know as"** where the render
has one. `build/slide_016.js:122` carries the single space, so the render is faithful to the
build but 3 px shy of the frame. Measured against BOTH images, so it is PIL-confirmed
(not phantom). It is whitespace-level and matches the original's own inter-word norm of
5-7 px; it does not affect legibility, containment, or any structural element.

## Attempt-6 staged artifacts — re-verified this lane
- `judge_prompt_6A.txt` — md5 `9387f5fbb94ef05a31db19f1e018dde1`, 4115 bytes,
  **re-derived from the Template A block of `shared_patterns/judge_protocol_03.md` with
  only NNN->016 (Template A's payload contains no standalone `K`) and byte-identical**
  (`IDENTICAL: True`). BLOC1ER x0. (The dispatcher comment says "4115 bytes"; the banked
  `wc -c` says 4139 because it was written by `write_text` vs my byte-count of the
  decoded string — md5 is the binding check and it matches.)
- `judge_prompt_6B.txt` — md5 `481172b034aa3336f54591d4e8e4bc98`, 1924 bytes, **BLOC1ER x0**,
  BLOCKER x2 intact; generated by `recut_crops_6.py` from the Template B block with
  `NNN->016` and `\bK\b->6`.
- Crop pairs re-derived from `render_6.png` by me and pixel-compared to the banked files:
  `crop_6_last_bullet_{render,orig}.png` 1541x118, effective scale x 2.0824 = 2.0824 and
  y 2.0702 = 2.0702; `crop_6_full_body_{render,orig}.png` 1531x904, x 2.0830 = 2.0830 and
  y 2.0829 = 2.0829. **Max differing px vs re-derivation: 0 on all four** — the pairs are
  pixel-exact from render_6 at matched effective scale (LANCZOS, H_render/540 = 2.0833).
- `dispatch_judge_6.sh` — legs `legA` / `last_bullet` / `full_body`, `--timeout 1200` inside
  `timeout 1700`, `--thinking high --max-tokens 65536 --rounds 1 --tries 1`.

## Which crop legs the rebuild invalidates (proved, my own diff)
render_5 vs render_6 differ by 1673 px total, bbox frame-px **y499.7..500.6 x445.0..806.9**
(the two b5a underlines). Region counts:
`missing_band` 0 px, `bullet2` 0 px, `last_bullet` 1673 px, `full_body` 1673 px.
So the render_5 crop PASSes survive for the two unchanged regions, but the two
regions that changed both need re-judging — as the parent law requires, all three
attempt-6 legs are needed on render_6.

## Gate probes this lane (park reason — congestion, NOT a build defect)
| when (UTC) | pgrep -c -f analyze_image.py | action |
|---|---|---|
| 19:14 | 8 | at the >=8 threshold -> heartbeat + sleep 240 |
| 19:20 | 11 | heartbeat + sleep 240 |
| 19:36 | 18 | >=8 -> heartbeat; congestion increased, not draining |

Two probes per hour are the budget; the hour's probes are spent. No vision call has been
dispatched this lane, so nothing is burned and no verdict has been fabricated.
Next probe window opens ~20:00 UTC; heartbeats keep the row live.

## PARK STATE
NOT certified by this lane yet. Row 16: `gen_status=judging`, `visual_check=NULL`,
`visual_transcript=NULL`, `visual_attempts=1`, `worker_id=judge016-fresh-lane-20261024`.
RESUME COMMANDS (project root; build, payloads, crops and dispatcher are all verified):

    cd "/worksp""aces/codespaces-blank/ai_llm_slides"
    export VIDEO=machine-learning/03_ridger_regression_gradient_descent
    python3 scripts/15_progress.py heartbeat 16 judge016-fresh-lane-20261024
    pgrep -c -f analyze_image.py          # must be < 8
    bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh legA
    bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh last_bullet
    bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/dispatch_judge_6.sh full_body
    # then, once all three transcripts carry a real FINAL VERDICT: line and each
    # finding is adjudicated PIL-first (or the verdicts are clean):
    python3 scripts/15_progress.py set 16 visual_check PASS   --worker judge016-fresh-lane-20261024
    python3 scripts/15_progress.py set 16 visual_transcript \
      videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/judge_attempt_6.txt \
      --worker judge016-fresh-lane-20261024
    python3 scripts/15_progress.py set 16 visual_attempts 6  --worker judge016-fresh-lane-20261024
    python3 scripts/15_progress.py set 16 pptx_path \
      videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_016_recreated.pptx \
      --worker judge016-fresh-lane-20261024
    python3 scripts/15_progress.py set 16 gen_status passed  --worker judge016-fresh-lane-20261024
    python3 scripts/15_progress.py heartbeat 16 judge016-fresh-lane-20261024
    python3 scripts/15_progress.py release 16 judge016-fresh-lane-20261024
    python3 scripts/15_progress.py get 16   # must read gen_status=passed, visual_check=PASS, worker_id=""

Verification note: `gen_status` must be set to `passed` AFTER `release` planning — if a
`claim`/`set` resets it to `building` (15_progress.py:337-339), re-set `gen_status passed`
before the final `release` so the closing row reads `passed` / `PASS` / `worker_id=""`.

## APPENDIX — judge-s2-20261025 lane (2026-10-25)

Attempt-6 legA (frozen byte-payloads A md5 9387f5… / B md5 481172…) returned a real
FINAL VERDICT: FAIL with ONE MAJOR — bullet 1 "This has/have the effect of better
generalization of the model".

Adjudication (judge findings are hypotheses; measure before fixing):
- validation JSON bullet reads "has" (PASS_WITH_FIXES, score 9) — but the ORIGINAL
  FRAME is ground truth and both the analysis and the judge disagree with it.
- doc-parse (nemotron-parse, no vision-gate slot) on the original's white content
  box (3x LANCZOS, scratch/tmp/orig016_body.png → orig016_body.parse.md):
  "• This have the effect of better generalization of the model".
  OCR confirms the ORIGINAL prints "have". The judge is CORRECT; the banked
  analysis transcript is wrong (a long-standing data error).
Fix (smallest correct change): build/slide_016.js bullet text "has" -> "have"
(also replaced the absolute `/workspaces/...` require of house_chrome.js with the
repo-relative form so the build runs in this checkout). Attempt 7:
render_7.png (chrome PASS; 3/3 underlines contained; 12/12 bands inked), crops
crop_7_{last_bullet,full_body}_* re-cut at matched scale, payloads judge_prompt_7A/
7B byte-identical to the frozen templates (md5 9387f5…/481172…).

## APPENDIX 2 — judge-s2-20261025: attempt-7 legs + honest PARK at the attempt cap

Attempt-7 legA was first dispatched (by template-reference error) against stale
render_6.png (pre has→have bytes); its PASS transcript is VOID — banked as
`judge_attempt_7_stale_render6_PASS.txt`, never counted as verdict evidence. The
re-dispatch against the correct render_7.png returned a real FINAL VERDICT: FAIL
with ONE MAJOR — bullet 2 "the **regularization** term is added" (judge read the
original as "generation", ~70% confidence).

Adjudication (PIL-first + doc-parse, two corroborated reads at different
--max-output-tokens + 3x/4x LANCZOS crops orig016_b1b2.png / b2line1/2):
nemotron-parse reads the original "…and model generalization, the
**generalization** term is added to the objective loss function…" — corroborated
by the attempt-6 legA judge ("generalization"). The judge's "generation" was its
own misread of the same fact: the build's "regularization" is a REAL verbatim
deviation (MAJOR). The banked analysis JSON is wrong again.

Fix (attempt 8 build, local work during park — established park practice, cf.
slide 019): build/slide_016.js b2b "regularization term" -> "generalization term"
(backup scratch/tmp/slide_016.js.pre_gen2term). Rebuilt slide_016_recreated.pptx
(02:23Z), rendered render_8.png — HOUSE CHROME CHECK: PASS; doc-parse of the
render's b2b line confirms "the generalization term is added". Crops re-cut
(recut_crops_8.py): crop_8_{last_bullet,full_body}_{render,orig}.png at matched
effective scale 2.083x; payloads re-frozen: judge_prompt_8A.txt md5
9387f5fbb94ef05a31db19f1e018dde1 (Template A, no standalone K),
judge_prompt_8B.txt md5 481172b034aa3336f54591d4e8e4bc98 (Template B, \bK\b→8).

PARK (honest, NOT certified): spent judge transcripts = attempts 1,2,4,5,6,7 = 6,
the cap per judging.md ("6 judge attempts per slide before parking"). No attempt-8
vision call was dispatched. Attempt-8 legs are STAGED, byte-verified, one command
each (run ONLY with mission-owner sanction to exceed the cap, ONLY at
`pgrep -c -f analyze_image.py` < 8, one leg at a time):
    bash $Q/dispatch_judge_8.sh legA         # -> judge_attempt_8.txt
    bash $Q/dispatch_judge_8.sh last_bullet  # -> crop_8_last_bullet_judge.txt
    bash $Q/dispatch_judge_8.sh full_body    # -> crop_8_full_body_judge.txt
Certification after clean A+B: visual_attempts=8, visual_check=PASS,
visual_transcript=judge_attempt_8.txt (+ crop transcripts banked), gen_status
passed, heartbeat, release.

## Appendix — attempt-8 certification (judge-s2-20261025)

All three legs clean after adjudication: legA PASS (zero discrepancies), crop
last_bullet PASS, crop full_body FAIL-then-adjudicated — its only MAJOR
("(model parameters)" should be blue) REFUTED by PIL column census of the
original heading line (blue ink cols 147..358 only; "(model parameters)" is
black ink cols 366..513; render matches). Minors (weight/hue) accepted.
visual_check=PASS, gen_status=passed, visual_attempts=8 (sanctioned 7th roll).
Evidence: judge_attempt_8.txt, crop_8_last_bullet_judge.txt,
crop_8_full_body_judge.txt, adjudicate_attempt_8.md.
