# Worker report — slide 011 (machine-learning/03_ridger_regression_gradient_descent)

**Worker id:** `w8-s011-20261020T2330` (resumption worker)
**Deliverable:** `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_011_recreated.pptx`
(single plain-named version, no suffix)
**DB final state:** `gen_status=passed`, `visual_check=PASS`,
`visual_attempts=1`,
`visual_transcript=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide011/judge_attempt_1.txt`

---

## 1. Resume state and what was actually wrong on arrival

The previous worker had banked `build/slide_011.js` + `qa/slide011/render_1.png` and died in a
fleet-wide provider outage **before any judging ran**. Resume protocol applied:

1. **Render currency verified first** — rebuilt from `build/slide_011.js` and pixel-diffed:
   0 of 2,251,125 pixels differ => `render_1.png` was current. No judging was done on a stale
   render.
2. **House-chrome selfcheck** — `shared_patterns/house_chrome_check.py render_1.png 011` PASS
   (panel x 112..1882 / y 90..1125; three C00000 1pt strokes present, **no top stroke** as this
   deck's law requires; badge disc centre (1824,152) px, d≈68).

## 2. One REAL defect found and fixed BEFORE any vision call

The banked selfcheck (`selfcheck_attempt_1.py`) reported 5 FAILs on the underline. Adjudication
(`selfcheck_attempt_1_adjudication.py`) proved those 5 were **checker bugs**: section 5's union
bbox over "wide" red rows absorbed the red title glyphs, so a glyph row carrying 716 red px blew
its >60 threshold and the "is this the bar's row?" test selected glyph rows. But the
investigation also surfaced a **real geometry defect**: the banked build drew the underline with
pptgen's text `underline: true`, which LibreOffice renders as a 1.44-frame-px hairline, whereas
the original has a **solid 4-row band (rows 258..261, density 0.993, x 595..698 = "outlier")**.

**Fix (no vision call spent):** replaced the text underline with an explicit filled rect, copied
from this deck's own certified family pattern (`build/slide_020.js` header note: "Drawn as an
explicit filled rect at the measured band — renderer-native underlines drift between LO and
PowerPoint; measured geometry is the law"):

```js
slide.addShape(pptx.ShapeType.rect, {
  x: px(595), y: px(258), w: px(104), h: px(4),
  fill: { color: "C00000" },            // no `line` => no outline
});
```

Re-render + `selfcheck_attempt_1_postfix.py` (assembled from v3 head lines 1–149 + corrected
section 5 + `tail -n +171` of v3): **30 checks OK, 0 FAIL**. Pre-fix evidence banked as
`render_1_pre_underline_fix.png` / `build_attempt_1_pre_underline_fix.js`.
Note: an intermediate assembly bug (`tail -171` duplicated sections 2–5, and the corrected
section 5 shadowed the globals `ry0`/`ry1` used by section 7's containment math, producing a
bogus "content ink clears the bottom stroke (B=540.5)" FAIL) was caught and fixed by renaming to
`ul_ry0`/`ul_ry1`.

## 3. Visual verification — both legs, all PATH

Both legs were executed **by this worker** (the dispatch assumed a spawn tool; none exists in
this session, and spawning foreground subagents is forbidden by the rules of engagement, so the
worker ran them itself through the vision gate).

Walls honoured: outer `timeout 1700` > gate 1650 > per-call 600 s. Vision invoked only as
`bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py
comparison ... -p "<frozen payload>" --thinking high --max-tokens 65536 --timeout 600`.

### Leg A — full-slide comparison (Template A)
`judge_prompt_1.txt` (4115 bytes) extracted **programmatically** from
`shared_patterns/judge_protocol_03.md` with assertions verifying deck-03 chrome values are present
and ml-intro values are absent. This deck's frozen payloads carry **no NNN/NAME placeholders** —
the slide id rides in `--view` only.

- **Attempt 1 died with "Response ended prematurely" and NO transcript** => fleet storm, treated
  as not consuming the 6-attempt budget (deck rule). Retry queued after a 13-minute sleep.
- **Attempt 1 (retry leg): PASS.** `judge_attempt_1.txt` — 21 lines / 2956 bytes.
  Verdict token: `FINAL VERDICT: PASS`. Discrepancies section: "none" (no BLOCKER/MAJOR/MINOR).
  Element rulings: title MATCH (incl. "outlier" underlined, verbatim capitalisation); subtitle
  MATCH (incl. the verbatim space before `)`); layout/vertical placement MATCH; delimiter geometry
  SATISFIED; missing elements NONE (the mouse-pointer mark below the subtitle correctly omitted
  per ground rule (c)); frame containment CLEAN; colors approx. consistent.

### Leg B — zoomed crop-pair certificates (Procedure B, 4 regions)
Cut with `cut_crops.py` (~8 px padding around each original region, BOTH images cropped at the
same slide-space region, original LANCZOS-upscaled to the render crop's exact pixel size —
crop-vs-crop ONLY). Banked pairs + per-region commands:

| region | pair | scale | verdict |
|---|---|---|---|
| title | `crop_1_title_orig.png` / `crop_1_title_render.png` | 1506×109 | `FINAL VERDICT: PASS` |
| underline | `crop_1_underline_orig.png` / `crop_1_underline_render.png` | 584×134 (zoom ×2) | `FINAL VERDICT: PASS` |
| subtitle | `crop_1_subtitle_orig.png` / `crop_1_subtitle_render.png` | 959×96 | `FINAL VERDICT: PASS` |
| badge | `crop_1_badge_orig.png` / `crop_1_badge_render.png` | 381×375 (zoom ×3) | `FINAL VERDICT: PASS` |

All four end in PASS; no MAJOR and no BLOCKER in any of them. (A duplicate badge leg was
launched after the runner log was misread; the original runner had in fact completed the badge
PASS at 00:31:35. The duplicates were killed before writing anything — the banked badge
transcript is the original runner's.)

## 4. PIL-first adjudication of every MINOR note

`crop_adjudication_1.py` → `crop_adjudication_1.txt` — **0 FAIL**. Each judge note was measured
against the pixels before any fix was considered (deck rule: judge findings are hypotheses).

| finding | verdict | evidence |
|---|---|---|
| underline heavier (title #1, underline #1) | **REFUTED** | render bar 4.32 frame px vs original 4 (+0.32, density 0.999 vs 0.993, x-extent within 0.3 px). Same ink mass; the heaviness is **crispness** — flat C00000 (192,0,0) vs the original's JPEG-softened red |
| red tone brighter (title #2) | **NOT A DEFECT** | render ink mean RGB (194,13,13) = flat C00000 nominal; original (187,86,96) = JPEG-darkened core. Family-nominal law, founder-ratified; certified siblings 002/035/029/020 draw C00000 against these frames and PASSED |
| "due to" spacing more open (title #3) | **REFUTED** | see §4.1 below |
| blue tone brighter (subtitle #1) | **NOT A DEFECT** | render (29,28,249) = spec #0000FF nominal vs original (62,54,187) video-captured. Nominal-colour law |
| badge numeral style/scale/ink (badge #1/#2/#3) | **HOUSE-CHROME EXEMPTION** | ground rule (b); the numeral's face/size/ink are deck-law constants emitted by the certified shared module `shared_patterns/house_chrome.js` (`drawHouseChrome(pptx, slide, {numeral: 11})`), identical on all 51 slides. Per-slide deviation would break deck chrome uniformity, and editing the module is forbidden (cascade law). Digits identical ('11'), centred (875.1,73.7 vs disc 876,73), extent 14.4×13.0 < the 35 px disc, clear of the ring |
| badge ring heavier (badge note) | **HOUSE-CHROME EXEMPTION** | drawn by the same certified module (6A5ACD ~2pt) |

### 4.1 The "due to" spacing finding — measurement-artifact refutation (method fix banked)

The first adjudication run printed a `-6.6 px` FAIL on the "due"→"to" gap. It was **a bug in my
measurement, not in the slide**, and it is banked as
`crop_adjudication_1_first_run_superseded.txt` with the method note in the script:

- it measured the two images at **different effective resolutions** (original 960×540, render
  2001×1125) and split ink runs at an **asymmetric** threshold (`c - pv > 2` = 2 frame px in the
  original but only 0.96 frame px in the render). The render's crisp glyph cores therefore
  fragmented into 38 letterpair runs while the original's JPEG halo merged into 21 word runs, so
  indexing `og[3]/og[4]` against `rg[3]/rg[4]` compared an *Overfitting*→*due* boundary against
  an intra-*Example* letterpair gap.

**Corrected method** (Procedure B's matched-scale law applied to the measurement itself):
LANCZOS-downsample `render_1.png` to the original's 960×540, split runs at one identical
frame-px threshold (stable across 5/6/7 px), identify words by width signature:

| word | orig extent | render extent | Δext | orig gap→next | render gap→next | Δgap |
|---|---|---|---|---|---|---|
| Example | 111–249 (138) | 113–250 (137) | −1 | 10 | 11 | +1 |
| of | 259–292 (33) | 261–293 (32) | −1 | 9 | 9 | 0 |
| Overfitting | 301–472 (171) | 302–471 (169) | −2 | 11 | 12 | +1 |
| due | 483–542 (59) | 483–541 (58) | −1 | 10 | 11 | +1 |
| to | 552–584 (32) | 552–583 (31) | −1 | 11 | 12 | +1 |
| outlier | 595–698 (103) | 595–697 (102) | −1 | 11 | 11 | 0 |
| in | 709–737 (28) | 708–735 (27) | −1 | 11 | 12 | +1 |
| data | 748–818 (70) | 747–815 (68) | −2 | | | |

Worst word-gap delta **1 frame px**; worst word-extent delta 2 px; total title ink width 707 vs
702 (−0.71%); ink centre 464.5 vs 464.0 (**−0.5 px**). The +1 px residual on 5 of 7 boundaries is
Arial-metric substitution, in-family with this deck's certified siblings. No fix cycle warranted.

## 5. Content fidelity notes (verbatim law)

- Title: `Example of Overfitting due to outlier in data` — verbatim, capitalisation as extracted,
  "outlier" underlined (drawn as a measured rect, see §2).
- Subtitle: `(and how to minimize overfitting )` — verbatim, **including the space before the
  closing parenthesis** (kept per the verbatim-text law even though validation flagged it as a
  possible extraction artifact).
- Mouse/pointer cursor below the subtitle: video-capture artifact, correctly OMITTED (ground
  rule (c)).
- Spec's `[?]`/uncertain items: none were marked `[?]` in the input; the admitted pt-size and
  badge-diameter guesses were resolved by PIL measurement (Arial bold 34 pt advance 704 px vs
  measured title ink 706 px; Arial italic 30 pt 437 vs 441 px) rather than by the estimates.
- Badge numeral: the analysis spec says yellow `#FFFF00` / black numeral; **deck house-chrome law
  overrides** to FDFD96 fill + 6A5ACD ring + `#333333` bold Arial 18 pt numeral, emitted by the
  shared module.
- No equations, no advanced graphs on this slide → no `eq_011_*.json` sidecars, no graphgen work;
  **OMML wrap N/A**. Post-certification wrapping is an orchestrator pass in any case.

## 6. Banked evidence index (`qa/slide011/`)

| file | what it is |
|---|---|
| `dispatch_brief.txt` | the dispatch (verbatim) |
| `build/slide_011.js` → `build_attempt_1.js` | the certified post-fix build (byte-identical) |
| `build_attempt_1_pre_underline_fix.js` + `render_1_pre_underline_fix.png` | pre-fix provenance |
| `render_1.png` | the certified render (2001×1125, 150 dpi) that both judge legs scored |
| `selfcheck_attempt_1.py/.txt` | the inherited (buggy) checker output |
| `selfcheck_attempt_1_adjudication.py/.txt` | proof the 5 underline FAILs were checker bugs |
| `selfcheck_attempt_1_postfix.py/.txt` | corrected checker — 30 OK / 0 FAIL |
| `selfcheck_attempt_1_checkerbug.txt` | the intermediate assembly-bug record |
| `judge_prompt_1.txt`, `judge_cmd_1.sh`, `probe_cmd_1.txt`, `probe_1.txt` | frozen Template A payload + commands + probe |
| `judge_attempt_1.txt` | **full-slide transcript — PASS** |
| `crop_1_regions.json`, `crop_1_region_descriptions.json`, `cut_crops.py` | Procedure B regions + cutter |
| `crop_1_{title,underline,subtitle,badge}_{orig,render}.png` | the four matched-scale crop pairs |
| `crop_1_{title,underline,subtitle,badge}_cmd.sh` | the four Template B commands |
| `crop_1_{title,underline,subtitle,badge}_judge.txt` | the four crop certificates — all PASS |
| `crop_adjudication_1.py/.txt` | PIL adjudication of every MINOR note — **0 FAIL** |
| `crop_adjudication_1_first_run_superseded.txt` | the superseded first run (documents the measurement bug + its fix) |
| `worker_report.md` | this report |

## 7. Verdict tokens per leg

- Full-slide (Template A, attempt 1 retry): `FINAL VERDICT: PASS`
- Crop pair — title: `FINAL VERDICT: PASS`
- Crop pair — underline: `FINAL VERDICT: PASS`
- Crop pair — subtitle: `FINAL VERDICT: PASS`
- Crop pair — badge: `FINAL VERDICT: PASS`

**Judge-flag summary (one line):** no BLOCKER/MAJOR anywhere; 9 MINOR notes across the four
crops (underline weight ×2, red tone, blue tone, "due to" spacing, badge numeral
style/scale/ink, badge ring) — all PIL-refuted, nominal-colour, or house-chrome-exempt.

## 8. Incidents

- None involving the foreign deck DB: every `15_progress.py` call carried
  `VIDEO=machine-learning/03_ridger_regression_gradient_descent`. One `set` was refused by the
  ownership guard ("slide 11 claimed by live worker ... writers pass --worker") and was correctly
  re-issued with `--worker w8-s011-20261020T2330`.
- One provider-storm death on the first full-slide leg (no transcript) — retried after 13 min,
  no attempt consumed.
- No banked evidence deleted; the `*.db.bak` archives untouched.
