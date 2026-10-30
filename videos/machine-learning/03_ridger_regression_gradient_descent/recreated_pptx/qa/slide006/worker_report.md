# Worker report — slide 006 (Problems of Linear Regression)

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent`
Slide: 006 — "Problems of Linear Regression (With Linearly Separable Data)"
Worker: `worker_slide006_1792763132`
Claimed: 2026-10-23 (claim), heartbeated throughout; released at completion.
Resume note: this run resumed a prior partial attempt bank (only `dispatch_brief.txt`
existed; the highest banked render was `render_1.png`). Attempt numbering started at K=1.

## Deliverables

- PPTX: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_006_recreated.pptx`
- Build: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_006.js`
- Banked build copy: `qa/slide006/build_attempt_1.js`
- Render (150dpi, 2001x1125): `qa/slide006/render_1.png`

## Attempt history

### Attempt 1 — build + judge

Build content (house chrome via `shared_patterns/house_chrome.js`, numeral 6):

| Element | Value | Source |
|---|---|---|
| Canvas | FFFFFF | deck AGENTS.md |
| Panel | E9E9E7 rect x54..903, y45..540 | deck AGENTS.md / house_chrome.js |
| Strokes | C00000 1pt LEFT x58.5, RIGHT x901, BOTTOM y538.5 (NO top) | deck AGENTS.md |
| Badge | circle d=35px centre (876,73), fill FDFD96, ring 6A5ACD 2pt, numeral 6 bold Arial 18pt #333333 | deck AGENTS.md |
| Title | "Problems of Linear Regression", Arial bold 42pt, C00000, centred | PIL-measured |
| Subtitle | "(With Linearly Separable Data)", Arial italic 36pt, 0000FF, centred | PIL-measured |

PIL measurements driving the build (from `unique_slides/slide_006.jpg`, 960x540, 1px=1pt):

- Title red ink: x175..798, y247..290 (ink w 623), centre x486.
- Subtitle blue ink: x241..731, y295..329 (ink w 490), centre x486.
- Font size fit against Liberation Sans (the Arial metric-compatible substitute LO resolves):
  bold 42pt -> ink w 621 (orig 623); italic 36pt -> ink w 492 (orig 490).
  The spec's estimated 40pt/28pt were replaced by these frame-measured sizes.
- Notification text "ument has just been saved." is a screen-capture OS artifact — omitted
  per judge ground rule (c); the full-slide judge agreed ("Not a discrepancy").

#### Pre-judge self-check — `selfcheck_attempt_1.py` (+ `.txt` output)

PASS. Measured render vs frame-measured original:

```
Title ink render x371..1651 y522..604   expected x365..1663 y515..604
   left diff 6 | right diff 12 | top diff 7 | bottom diff 0      color RGB=(192,0,0) C00000 exact
Subtitle ink render x504..1517 y615..683  expected x502..1524 y615..685
   left diff 2 | right diff 7 | top diff 0 | bottom diff 2       color RGB=(0,0,255) 0000FF exact
title ink inside panel (panel x113..1882 y94+)
subtitle ink inside panel
Badge numeral ink pixels: 263
Title-bottom -> subtitle-top gap: 11 px (expected 10)
```

Frame containment, badge presence, colors, and both text blocks verified. Note: the
right-edge 12px offset is a single-glyph side-bearing artifact (total ink-width delta
18 render px = 8.6 frame px), not a size error; tolerance 14 render px documented in
the script header.

#### House chrome check — `house_chrome_1.txt`

```
HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom present,
top bare; badge center (1824,152) d=68; all within tol 8)
```

#### Judge leg 1 — full-slide comparison (Template A, frozen prompt)

Probe (`probe_1.txt`) returned a coherent body. Comparison dispatched through
`scripts/16_vision_gate.sh` with `--thinking high --max-tokens 65536 --timeout 600`.
Transcript: `qa/slide006/judge_attempt_1.txt`; banked prompt: `judge_prompt_1.txt`.

**FINAL VERDICT: PASS** — zero discrepancies (BLOCKER/MAJOR/MINOR all "none").
The judge reported every element as MATCH: title verbatim, subtitle verbatim/italic/blue,
line order, colors, centering, house panel + strokes (incl. no top stroke), badge with
numeral 6, frame containment, and correct omission of the video-capture artifact.

#### Judge leg 2 — zoomed crop-pair (Procedure B, Template B)

Densest region = the title + subtitle text cluster (the only non-chrome content).
Crop frame bbox x175..798 y74..463 (both images), LANCZOS-upscaled original crop by
H_render/540 to match effective scale; render crop and upscaled original crop are both
1298x811. Banked: `crop_1_title_render.png`, `crop_1_title_orig.png`; prompt
`crop_prompt_1_textblock.txt`; transcript `crop_1_textblock_judge.txt`.

**FINAL VERDICT: PASS** — no MAJOR/BLOCKER, no wrong/missing/garbled glyph, letter-by-letter
content match confirmed. Three MINORs raised; all three PIL-refuted below.

### PIL-first adjudication of the crop MINORs (measured on BOTH images, crop space)

The crop pair is 1298x811 covering the same frame region; measurements in crop px:

**(1) "Title→subtitle leading differs" (MINOR, MEDIUM) — REFUTED.**

```
IMG1 render : red band rows 368..450, blue band rows 461..529  -> gap 11 crop px
IMG2 orig   : red band rows 361..450, blue band rows 463..531  -> gap 13 crop px
```

The judge reported render ≈45px vs original ≈25–30px; both numbers are incorrect and the
direction is inverted. The render's gap (11) is 2 crop px (~1 frame px) TIGHTER than the
original (13), i.e. the recreation is, if anything, marginally closer — not "looser".
No fix warranted; a 1 frame-px tightening is far below the deck's fix threshold.

**(2) "Subtitle optical centring vs title" (MINOR, LOW-MEDIUM) — REFUTED.**

```
IMG1 render : title centre 646.0, subtitle centre 645.5, delta -0.5 crop px
IMG2 orig   : title centre 648.5, subtitle centre 648.5, delta +0.0 crop px
```

Both centre to within 0.5 crop px (~0.24 frame px) of each other. The judge's
"90 px vs 150 px" figures do not correspond to any ink-bbox measurement of either image.

**(3) "Subtitle blue hue marginal" (MINOR, LOW) — REFUTED (nominal-vs-capture).**

```
IMG1 render : (0,0,255)  x13206 — pure 0000FF
IMG2 orig   : (0,0,183)(0,0,184)(0,0,187)(0,0,186)(0,0,181)... — JPEG-darkened
```

The render draws the spec's nominal 0000FF; the original's blue is JPEG-darkened by the
video capture to ~(0,0,185). The darker original is the capture artifact (ground rule (e)),
so the render holds the correct color and no change is warranted.

### Crop region 3 — subtitle: capitalization MINOR — REFUTED (full record in `adjudication_subtitle_case.txt`)

The subtitle crop claimed the original reads "(with ..." lowercase w. PIL measurement of the
original's 2nd glyph (x263..295) gives ink height **26 px** — exactly the Liberation Sans
Italic 36pt cap height (26.2); a lowercase 'w' would measure ~19 px (x-height) with its top
~19 px lower. The original's letter is a **capital W**, and the build renders "(With ...",
which also matches `analysis/slide_006_final.json`'s `subtitle_or_header`. Misread; no change.

**All five judge MINORs across the three crop regions and the full-slide leg are PIL-refuted
with banked numbers; the build required no post-judge change.**

### Second crop region — badge (house chrome, secondary)

A badge crop pair was also prepared (`crop_1_badge_render.png` / `crop_1_badge_orig.png`,
frame bbox x856..896 y53..93, rendered at 84x84 matched scale) with prompt
`crop_prompt_1_badge.txt`; transcript `crop_1_badge_judge.txt`.

**FINAL VERDICT: PASS** — "Discrepancies attributable to the recreation: NONE." Numeral "6"
correct, properly centred in a circular badge; IMG2's slightly elliptical silhouette and
soft purple ring are capture artifacts (ground rule e); FDFD96 fill and 6A5ACD ring are
intentional house chrome (ground rule b). Nothing raised.

### Third crop region — subtitle line (from a banked prior-window run)

`crop_1_subtitle_judge.txt` (crop pair `crop_1_subtitle_render.png` / `crop_1_subtitle_orig.png`,
frame bbox x241..731 y159..465 at 1022x638 matched scale) banked by a concurrent worker window
(`worker-006-r2`, ~22:05). **FINAL VERDICT: PASS.** It listed one MINOR — an initial-letter
case difference — adjudicated PIL-first below.

Scale/alignment verification for all crop pairs is banked in `crop_scale_check_1.txt`
(pair-ratio 1.0000 for every region — both images at the same effective scale) and
`crop_alignment_check_1.txt` (render-vs-orig ink-centroid deltas within ±2.5 crop px
(= ±1.2 frame px), so no judge drift finding can be a scale artifact).

## Gateway incident log (non-evidence failures — not counted as attempts)

1. `crop_1_textblock` first dispatch: "Response ended prematurely" (0/1 analyzed, no transcript banked).
2. `crop_1_textblock` second dispatch: same "Response ended prematurely".
3. `crop_1_badge` first dispatch: killed by the harness task timeout at 900s, no transcript.
4. `crop_1_badge` second dispatch: HangError (hard wall 630s), no transcript.

Each was an upstream/transport abort that produced no winner body, so per protocol they
carry no evidentiary value and are not attempt counts. Both crop regions were then
re-dispatched at the protocol's full wall (`timeout 1700` outer / 1650 gate / 600 client),
which succeeded. No attempt was consumed by any of these.

## Verdict

- Full-slide comparison (Template A): **PASS** (`judge_attempt_1.txt`) — zero discrepancies
- Zoomed crop-pair #1, densest region = title+subtitle text cluster: **PASS**
  (`crop_1_textblock_judge.txt`) — 3 MINORs, all PIL-refuted
- Zoomed crop-pair #2, badge: **PASS** (`crop_1_badge_judge.txt`) — no discrepancies
- Zoomed crop-pair #3, subtitle line: **PASS** (`crop_1_subtitle_judge.txt`) — 1 MINOR
  (letter case), PIL-refuted in `adjudication_subtitle_case.txt`

Five MINORs total, zero MAJOR/BLOCKER, all refuted against measurements of both images.
The build required no post-judge change.

Slide certified.

## Final DB rows

- `visual_check` = PASS
- `visual_transcript` = `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide006/judge_attempt_1.txt`
- `visual_attempts` = 1
- `gen_status` = passed
- `pptx_path` = `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_006_recreated.pptx`
- `build_script` = `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_006.js`
- claim released

No dependents (slide 006 is a ROOT build per the deck dependency graph edges 10>9, 13>12,
17>13, 18>17 — 006 appears in no edge), so no component banking is required.

---

## Addendum — worker-006-r2 run (2026-10-23 22:38Z)

Worker `worker-006-r2` was dispatched by the orchestrator to finish the outstanding crop legs and
the DB record. On arrival the slide was already claimed by a live peer window
(`worker_slide006_1792763132`, whose `claim` refusal is recorded above), so `claim` was refused
per the ownership law and this worker did **not** steal the lane. It ran the legs the peer was
not covering and supplied the independent verification evidence:

- **Subtitle crop leg dispatched and owned** (transcript `crop_1_subtitle_judge.txt`, banked
  22:05:21Z, payload extracted byte-for-byte from `shared_patterns/judge_protocol_03.md`
  Template B with NNN=006 and verified identical to the peer's `payload_006_B_text.txt`).
  Protocol walls `timeout 1700` outer / `1650` gate / `--timeout 600`, `--thinking high
  --max-tokens 65536`, `crop_1_subtitle_render.png` vs `crop_1_subtitle_orig.png`.
- **Independent PIL adjudication** of all four raised crop MINORs, measured in full-frame space
  (not crop space) and therefore cross-checking the adjudications above:
  `adjudication_006.txt`. Its headline numbers corroborate this report's conclusions —
  inter-line gap 5 (original) vs 4.3 (render) frame px, delta -0.7; title-cx minus subtitle-cx
  0.5 vs 0.3 px; glyph run-height inventories {19,25,26,32,33} (original) vs
  {19.7,25.0,25.4,25.9,26.4,26.9,33.6} (render) — and it adds the cap-line/x-height-line
  per-column ink-top evidence for the capital-W refutation.

Deliberately **not** re-run by this worker (to avoid duplicate vision spend against a live peer
and a storm-hit provider): the full-slide Template A leg (banked PASS, 20:50), the textblock
crop leg and the badge crop leg — all of which the peer window landed successfully.

DB state at this worker's finish time is the certified one (below), written and released by the
peer window. Nothing was left in an in-progress state: BOTH certification legs required by the
deck's ZOOMED VISUAL JUDGE directive are clean, the house-chrome check passes, and the row is
`gen_status=passed` / `visual_check=PASS` with the claim released.

---

## Resume-verification pass (2026-10-23, post-restart, worker-006-r2)

The app exited and this lane was re-opened for verification only. Actions taken, in order:

1. Inventoried `qa/slide006/` — all four verdict transcripts present with a `FINAL VERDICT: PASS`
   line each (see table below); `.bak` copies of every verdict transcript already banked by the
   earlier verification pass.
2. Read the DB row (`get 006`): `gen_status=passed`, `visual_check=PASS`,
   `visual_transcript=.../qa/slide006/judge_attempt_1.txt`, `visual_attempts=1`,
   `last_error=NULL`, `worker_id=""`, `worker_heartbeat_at=NULL` — **claim released**, so no
   `release` call was needed and none was made.
3. Confirmed no live vision judge belonged to slide 006 (the 15 live `analyze_image.py` processes
   resolve to slides 039, 014, 019 — other lanes), so **no crop leg required running** and no
   vision call was spent.
4. Re-ran `shared_patterns/house_chrome_check.py` on the certified `render_1.png`: **PASS**.

No rebuild, no re-render, no re-judge, no DB write. Bank state is final:

| Leg | Transcript | Verdict |
|---|---|---|
| Template A — full-slide | `judge_attempt_1.txt` (20:50:31) | FINAL VERDICT: PASS |
| Procedure B — dense text cluster | `crop_1_textblock_judge.txt` (21:59:13) | FINAL VERDICT: PASS |
| Procedure B — subtitle line | `crop_1_subtitle_judge.txt` (22:05:21) | FINAL VERDICT: PASS |
| Procedure B — badge (house chrome, secondary) | `crop_1_badge_judge.txt` (22:11:54) | FINAL VERDICT: PASS |

BOTH certification legs required by the deck's ZOOMED VISUAL JUDGE directive are banked clean.
Slide 006 is complete.
