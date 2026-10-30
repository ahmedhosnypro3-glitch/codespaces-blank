# Worker report — slide 007 "Problems of Linear Regression"

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Slide id: 007 (root build — no dependencies)
Worker: `worker-1792762049`
Resumed: no prior WIP beyond `dispatch_brief.txt` (the prior worker left only the brief).

## Deliverable
- pptx: `recreated_pptx/slide_007_recreated.pptx` (single plain-named version)
- build: `recreated_pptx/build/slide_007.js`

## Frame measurements (unique_slides/slide_007.jpg, 960×540 px = 1px = 1pt)
- canvas FFFFFF | E9E9E7 panel x54..903 y45..540 | C00000 strokes L x58.5 / R x901 / B y538.5 (NO top)
- badge (876,73) d≈32 FDFD96 / 6A5ACD ring / bold Arial 18pt numeral `333333` = 7
- title red ink x242..677 y78..100, center x≈460
- blue content box outer x78..885 y120..513, stroke cores x80.5/881.5 y122.5/510, fill FFFFFF, border #0000FF
- body text (ink top / ink x / size): intro y154 x90..809 ~18pt; header y202 x90..562 ~20pt;
  bullet1 y249 x92..308 ~22pt; bullet2 y294 x92..554 ~22pt; bullet3 y348 x92..631 ~22pt;
  bullet4 y397 x92..859 ~22pt. Inter-line pitch 48, 47, 45, 54, 49 (pt).

## FRAME-vs-SPEC adjudications (PIL-first, decided before judging)
1. **Intro-line underlines**: spec (step 5, `[?]`-marked) claims underlined key phrases. PIL on the
   original shows NO underline on the intro line — rows y173..175 carry only ~90 px of descender ink
   versus the header underline's 472 px stroke. Frame wins: intro drawn WITHOUT underlines.
2. **Bullet glyph**: original is a small filled arrowhead ~18pt tall; pptxgenjs U+27A2 renders
   ~34pt tall in LO. Frame wins: bullets drawn as explicit triangle shapes at the measured geometry.
3. **Line wrap**: bullet4 wrapped to a second line at 22pt in LO (810.8pt > 792pt usable).
   Closed with `charSpacing: -0.6` (never font size — that breaks cap-height/baseline metrics).

## Build history
| render | build | note |
|---|---|---|
| render_1..3 | iter 1 | intro underline attempt (explicit line shapes drawn at y162 — a defect) |
| render_4 | iter 2 | intro underlines removed (frame has none) |
| render_5 | iter 3 | bullet4 `charSpacing: -0.3` — still wrapped (7 clusters) |
| render_6 | iter 4 | bullet4 `charSpacing: -0.6` — 6 clusters, 774.3pt vs original 768pt. **BASIS OF JUDGING** |

## Self-check (banked `selfcheck_attempt_1.py` + `.txt`, run on render_6)
`SELFCHECK PASS` — containment 0 px text-colored ink outside the box; all six line tops Δ≤3.4pt vs
original; all pitches Δ≤0.5pt; header underline present, intro has no stray strokes; arrowheads
h≈15pt each; nothing below bullet4. Plus `house_chrome_check.py 7` → **PASS**.

## Judge — CERTIFIED (all three legs PASS, attempt 1)
Attempts used: **1** (both legs dispatched on attempt 1, render_6 basis).

| leg | transcript | verdict |
|---|---|---|
| Template A full-slide | `qa/slide007/judge_attempt_1.txt` | **PASS** |
| Procedure B crop `body` | `qa/slide007/crop_1_body_judge.txt` | **PASS** |
| Procedure B crop `title` | `qa/slide007/crop_1_title_judge.txt` | **PASS** |

Judge findings (full-slide): verbatim title and all four bullets + intro + header, matching
colors/styling (dark-red title, blue bold list text, red-italic parentheticals, blue frame),
consistent line stepping, left-aligned text centered in the blue frame, **full containment**
— nothing crosses or touches the blue border, no missing elements, no overflow, no clipping,
no wrapping anomalies. The only original-frame artifact (a mouse cursor near "Singular Matrix")
is correctly omitted per ground rule (c).

Crop legs confirmed glyph-by-glyph: title letters match one-for-one with correct capitalization;
badge numeral "7" vertically centered in the yellow disk; no wrong/missing/garbled characters;
no delimiter or table issues; residual differences are IMG2 compression halos and
typed-vs-capture rendering, both explicitly excluded by ground rules (c)/(e).

Both crop clients logged internal provider aborts (EmptyStreamError / 630s HangError) before the
validated winner landed on attempt 3 — those are the skill's automatic retry ladder, not judge
attempts. `visual_attempts` correctly records **1**.

Judge procedure fallback: executed by the worker via Bash through `scripts/16_vision_gate.sh`
(no Agent/Task spawn tool available).

## Final verdict
**PASS** — certified. DB: `visual_check=PASS`, `visual_transcript=qa/slide007/judge_attempt_1.txt`,
`visual_attempts=1`, `gen_status=passed`. Crop transcript paths listed above and banked in this
report as required by the deck's certificate law.

## Not done / follow-up
- OMML wrap (`scripts/18_omml_wrapper.py`) is a POST-certification orchestrator pass — NOT
  performed here (the slide has no equations, so it is a no-op for this slide).
- Title horizontal centering: measured off by ~19pt vs the original (render center 478.8 vs
  original ~459.5). Both judges PASSed it as "centered"; left as-is deliberately rather than
  modifying a certified build.
- Claim released at completion; no dependents, so no component bank was required.
