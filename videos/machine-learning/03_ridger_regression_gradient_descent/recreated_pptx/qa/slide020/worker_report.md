# Worker report — slide 020 (ML lecture 03: Ridge Regression & Gradient Descent)

Worker: `slide020-worker-zcode-20261019` (ZCode build worker; no prior worker state —
fresh start, attempt numbering from 1). Root slide (no dependencies; no in-graph children).

## Final verdict

**CERTIFIED PASS** — `gen_status=passed`, `visual_check=PASS`, `visual_attempts=3`
(1 full-slide Template A + 2 zoomed crop-pair Template B certificates; 3 of the
6 shared judge attempts used; 0 garbage re-invokes; 0 W4 hard-wall retries).
Claim released. No OMML wrap needed (slide contains NO equations —
`verbatim_text.equations` is empty; the wrap is an orchestrator pass anyway).
No advanced graphs; no generated assets under `build/assets/` for this slide.

## Deliverable

- **pptx**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_020_recreated.pptx` (single plain-named version)
- **Build script**: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_020.js`
- **Certified render**: `qa/slide020/render_1.png` (150dpi, 2001x1125)
- **Banked component (playlist-scoped)**: `recreated_pptx/build/components/slide_020.js`
  (`renderBase(pptx, slide, opts)`, numeral override + `skip.{chrome,title}`);
  proven faithful by a full re-render pixel-diff: **0 of 2,251,225 px differ**
  vs `render_1.png` (component-check pptx built via renderBase, rendered in a
  private LO profile, PIL-diffed).

## Content reproduced (verbatim, frame-measured)

Two-line red bold title, centered per the frame's own (off-slide-center) axis:
- L1 `[2] Ridge Regularization to overcome` — ink x 159..758, band y 230..264
- L2 `Inverse Problem of Singular Matrix` — ink x 183..744, band y 310..344
- Underline bar under L2 — x 183..744 (w 562), core rows 338..340 (drawn as an
  explicit filled rect at the measured band; renderer-native underline positions
  drift between LO and PowerPoint)
- House chrome via `shared_patterns/house_chrome.js` (numeral 20 — matches the
  printed original; NO top stroke, correct for this deck)
- Mouse cursor (x 454..470, y 397..414): video artifact, OMITTED per GROUND
  RULES (c) + recreation_brief step 5
- Title color C00000 (founder-ratified family nominal; frame's darkest cores
  read (134,10,22) = the documented JPEG-darkening pattern, same law as chrome
  strokes); Arial Bold 34pt (advance fit: L1 17.670em x 34 = 600.8px vs measured
  600; L2 16.449em x 34 = 559.3px vs measured 562)

### Notable measured facts
- The original's title block is NOT centered on the slide: L1 center x=458.5,
  L2 center x=463.5 (slide center 480). Both lines placed at their own measured
  centers (frame wins over intuition).
- No underline exists under L1 (spec's "second line underlined" confirmed:
  solid 562px red bar rows 338-340, verified row-by-row).
- Baseline pitch between the two lines: 80px (reproduced by independent
  placement of two single-line boxes).
- Full-frame ink census: only title words, badge cluster, cursor cluster —
  no other content on the slide.

## Closed-loop self-check (pre-judge; banked)

- `house_chrome_check.py render_1.png 20` → **PASS** (panel x 112-1882 render-px,
  strokes L/R/bottom present, top bare, badge center (1824,152) d=68, numeral present)
- `selfcheck_attempt_1.py` (banked, prints numbers): final deltas vs
  halo-corrected targets — L1 top 231.4/bot 262.6 (targets 231.5/262.5),
  x 159.8..756.0 (w 597.2); L2 top 311.0/bot 342.7 (targets 310.75/343.4),
  x 182.9..744.5 (w 562.6); underline core exactly on rows 338-340
  (2350 render-px/2-row band = full 562f width). Containment OK; no ink below
  L2 band (no wrap spill); all edges within ~1-1.5 frame px.
- One pre-judge TUNE iteration (dy -1.4 both lines, charSpacing +0.06 on L1);
  pre-tune build + render banked as `build_pre_tune1.js` +
  `selfcheck_pass1_render.png` (no evidence deleted).

## Judge legs (frozen protocol `shared_patterns/judge_protocol_03.md`; all calls
through `scripts/16_vision_gate.sh`, default route, `--thinking high
--max-tokens 65536`, walls 1700/600)

- Probe: `probe_1.txt` — valid body, window open.
- **Attempt 1 — full-slide Template A**: transcript `judge_attempt_1.txt`,
  prompt banked `judge_prompt_1.txt`, build copy `build_attempt_1.js`.
  Verdict **PASS** — zero BLOCKER/MAJOR/MINOR discrepancies; line separation
  "within a few px"; cursor omission correctly not flagged. (Body quirk noted:
  it describes BOTH title lines as underlined in BOTH images — a symmetric
  misread of L1, no discrepancy raised, no action.)
- **Crop 1a — title region** (x 148..770, y 220..356; pairs
  `crop_1_title_render.png` / `crop_1_title_orig.png`, matched effective scale
  2.0836x2.0882 proven by `make_crops_1.py`): transcript `crop_1_title_judge.txt`,
  prompt `crop_1_title_prompt.txt`. Verdict **PASS** — glyph content exact on
  both lines, `[2]` brackets present, underline full-span + continuous,
  zero discrepancies, high confidence.
- **Crop 1b — badge region** (x 838..896, y 46..102; pairs
  `crop_1_badge_render.png` / `crop_1_badge_orig.png`): transcript
  `crop_1_badge_judge.txt`, prompt `crop_1_badge_prompt.txt`. Verdict **PASS**
  with one MINOR: "numeral weight heavier in the recreation" (judge's own caveat:
  JPEG softness exaggerates thinness). **Adjudicated PIL-first, banked
  `adjudicate_badge_minor.py`**: the numeral is THIS deck's house chrome
  (founder-ratified bold Arial 18pt 333333, constant across 001/005/009/018/040,
  drawn by the shared module — judge findings on chrome are overridden by law);
  measurement shows the original's numeral strokes are 3-4px ghosts vs the
  render's metrically-correct 5-6px bold strokes at matched scale (bold 18pt
  Arial stem = 4.9 render px), i.e. video-capture wash, not a build defect.
  NOT a fix trigger; recorded here as the refutation record.

## Transcript paths (all under `qa/slide020/`)

- Full-slide comparison: `judge_attempt_1.txt` (the DB `visual_transcript`)
- Title crop: `crop_1_title_judge.txt`
- Badge crop: `crop_1_badge_judge.txt`
- Probe: `probe_1.txt`

## Judge-flag summary (one line)

Full-slide PASS with zero discrepancies; title crop PASS zero discrepancies;
badge crop PASS with one PIL-refuted MINOR (numeral stroke weight = house-chrome
bold 18pt vs JPEG-washed original ghosts — adjudication record banked).

## Environment / process notes

- Judge prompts sourced byte-for-byte from `judge_protocol_03.md` Templates A/B
  (only 020/K/NAME/region substituted). Path-only deviation: the runbook/protocol
  carry the pre-2026-10 image-analysis path `.agents/image-analysis/...`; the
  skill now lives at `.agents/skills/image-analysis/scripts/analyze_image.py`
  (its SKILL.md path law). `-p` payloads untouched.
- No Agent/Task spawn tool exists in this worker environment; per the
  orchestrator-approved fallback the banked judge procedure was executed by the
  worker via Bash (probe + comparisons through the gate; verdicts taken
  verbatim from the vision model's comparison winner bodies).
- Scratch renders in project scratch (`scratch/tmp`, TMPDIR redirected);
  private LO profile `/tmp/lo_slide020`. No provider errors occurred (0 sleeps,
  0 retries). No banked evidence deleted.

## S19 payload-exact confirmation addendum (2026-10-25)

Confirmation legA re-ran on the certified deliverable under the pool-299640
amendment (no rebuild): frozen tplA payload byte-exact from
shared_patterns/judge_protocol_03.md (payload banked as payload_A_confirm.txt,
md5 9387f5fbb94ef05a31db19f1e018dde1), render vs original full-frame
comparison, `--thinking high --max-tokens 65536`.

- Transcript: judge_attempt_1_confirm.txt — FINAL VERDICT: PASS, zero
  discrepancies raised.
- DB: last_error note written ('S19 payload-exact confirmation legA PASS
  2026-10-25; S16 HIGH closed'); gen_status/visual_check untouched.
- No build, render, or banked evidence was modified.
