# Worker report — slide 009 (Overfit vs. Generalized), deck 03

Worker: `w009-root-20261024` (this session ran as the orchestrator's freshly-dispatched
lane "Slide 009 root build+judge", agent-111). Claimed 2026-10-24 06:52:44.

## Situation found on dispatch (verified by live process inspection, not mtime guesses)

The dispatch premise ("prior lane interrupted mid-build, unjudged WIP pptx") was FALSE at
claim time. While I was inspecting, the prior lane (`w009`) **completed and certified at
06:58:41**: `visual_check=PASS`, `visual_transcript=qa/slide009/judge_attempt_5.txt`,
`gen_status=passed`, then `release 009 w009`. I watched its certification shell (pid
225677) finish, then read the banked row. So the deliverable already existed and was
certified; the orphaned build processes I first saw (slide_009.js → soffice) belonged to
this same session's parent chain and landed `render_5.png` (08:53 ref: built 06:53, md5
`84c8bf3179992d74717fa070f5f8c607`) — no rebuild, no re-judge, no row overwrite by me.

Per the laws (never re-dispatch certified components, never fabricate verdicts) I did NOT
rebuild or duplicate the lane's judge. Instead I ran an **independent verification pass**:
PIL-first measurements, then both mandated legs through the vision gateway on the same
certified bytes.

## Verification evidence (all banked under `recreated_pptx/qa/slide009/`)

### PIL-first (before any vision call)
- `pil_verify_5c.py/.txt` (corrected scales SX=2.084375, SY=2.083333): chart frames
  (94.5,106.6)-(465.8,473.8) / (485.5,106.6)-(871.2,473.8) vs original (95,107)-(466,474) /
  (486,107)-(872,474); equation boxes (216.4,148.3)-(316.6,174.2) / (631.4,148.3)-(733.6,174.2)
  vs original (219,149)-(314,172) / (635,150)-(731,173), glyph ink inside with pads
  6.7-11.5px (original 6-8px); caption boxes (97.9,480)-(431.3,526.6) / (503.7,480)-(838.1,526.6)
  vs original (98,483)-(431,526) / (504,482)-(838,526). All match.
- `containment_5.txt`: content ink outside the house panel = **0 px** (strips pure white).
- `house_chrome_5_rootw009.txt`: deck chrome checker PASS (strokes L/R/bottom, top bare,
  badge (1824,152) d=68).
- `cut_crops_5.py/.txt` + `pil_verify_5c.py` cut `crop_5_*` pairs (matched effective scale:
  original crop LANCZOS-resized to the render crop's exact size).
- `crossbuild_diff_5.txt`: cap_left/cap_right pixel-identical across render_3/4/5 → their
  certificates carry; eq_left/eq_right/chart_left/chart_right all changed → fresh gateway
  crop legs run for all four. (First diff pass used a wrong scale — 2001/540 on both axes —
  which falsely reported eq_right unchanged and r4≡r5; corrected here. Self-caught bugs
  banked in `pil_verify_5.py/5b.py`.)
- Deliverable integrity: valid zip, 1 slide, 2 equation-image parts, all verbatim strings
  present (captions split into bold-keyword+remainder runs; badge "9").

### Gateway legs on render_5 (payloads byte-for-byte from `shared_patterns/judge_protocol_03.md`)
- Probe: `probe_5_rootw009.txt` — valid body; transcribed all six verbatim strings + layout.
- **Leg A (full-slide)**: `judge_attempt_5_rootw009.txt` — **FAIL**, 2 findings, both
  PIL-refuted below.
- **Leg B crops**: `crop_5_rootw009_eq_left_judge.txt` PASS (1 MINOR: `=` sidebearing —
  same ink width 82px, same glyph inventory; matching). `crop_5_rootw009_eq_right_judge.txt`
  PASS (3 MINORs: superscript hue medium shift, `=` sidebearing, box-stroke weight —
  all matching-level). `crop_5_rootw009_chart_right_judge.txt` PASS (1 MINOR: dimension
  connector hue — PIL-refuted below). `crop_5_rootw009_chart_left_judge.txt` — see below.
- Carried certificates (pixel-identical regions): the prior lane's `crop_5_lane_*_judge.txt`
  (6 regions, all PASS) + `crop_3_cap_*`; the prior lane's crop IMAGES were overwritten by
  my (equivalent) cuts, so I reconstructed theirs as `crop_5_lane_*_{render,orig}.png`
  (`reconstruct_lane_crops.txt` — exact size match 805×787 chart_left, confirming their
  scale was correct).

### Adjudications of the Leg-A FAIL (PIL-first, against BOTH images)
1. **[MAJOR refuted] "left marker is a disc 2-3× the original's small red dot; arrow stops
   on the disc rim"** — `adjudicate_5_disc.py/.txt`, `adjudicate_5_disc2.txt`,
   `adjudicate_5_ascii.txt`. Both images carry the SAME structure: a solid red disc ~24 px
   diameter on the dimension line with the arrowhead merged directly on top, and the arrow
   tip at the fit-line foot (249,292) in both. Render disc 24.5×24.0 vs original 29.0×26.0 —
   the render's is ~10% SMALLER, not 2-3× larger. The original's disc is NOT orange-dot
   sized (dots are 7.2 px in the render; the original's dot cores (254,125,0) are the same
   class): it is a ~25 px disc in both. The judge misread the original's disc at full-slide
   scale. NOT a fix trigger.
2. **[MINOR refuted] "nested/double chart frame"** — blob census finds exactly ONE navy
   border component per chart in the render (same as the original); the extra "columns" the
   judge saw are the render's single 1 pt stroke at its correct 2.08 px 150dpi width.
3. **[chart_right MINOR refuted] connector hue** — `adjudicate_5_connector.txt`: the
   original's dimension line is rose-family (mean 224.8,155.8,152.0; core (240,190,200)), the
   render's is the same rose (ECBAC4); the periwinkle residual dashes match in both
   ((192,193,217) vs (195.6,199.6,218.2)). The judge conflated the rose dimension line with
   the blue-ish residual dashes.

## Final state
- `get 9`: gen_status=passed, visual_check=PASS, visual_attempts=5,
  visual_transcript=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/judge_attempt_5.txt,
  worker_id="" (released after verification).
- Full-slide PASS basis: `judge_attempt_5.txt` (prior lane; real FINAL VERDICT: PASS line).
- Fresh certificates covering the changed regions: `crop_5_rootw009_eq_left/eq_right/chart_right_judge.txt`
  (PASS) + `crop_5_rootw009_chart_left_judge.txt` (pending at report time — see below).
- Deliverable: `recreated_pptx/slide_009_recreated.pptx` (build
  `recreated_pptx/build/slide_009.js` md5 `dbb694bc840268f9e8008cf1307aa0ab` = the banked
  `build_attempt_5.js`; render_5 md5-linked).
- **Component for child 010** (import, never copy): `recreated_pptx/build/components/slide_009.js`
  — verified loadable, exports `renderBase(pptx, slide, opts)` with `opts.skip`/`opts.only`
  per-block control (BLOCKS: panels, fittedLines, points, marks, axes, eqBoxes, capBoxes,
  captions) + geometry constants; requires the shared `shared_patterns/house_chrome.js`
  primitive. Component is certified single-source-of-truth for 010's delta.

## In-progress items — CLOSED 09:29

- `crop_5_rootw009_chart_left_judge.txt`: **no gateway verdict** — both the original dispatch and
  the W4 hard-wall retry died at the analyzer's 630 s internal wall (HangError, attempts
  aborted, outer timeout 124; logs `legB_chartleft.log`, `legB_chartleft_retry.log`). The W4
  allowance (one hard-wall retry per leg) is exhausted; per law no third attempt and no
  fabricated verdict. The region's coverage stands on: the prior lane's
  `crop_5_lane_chart_left_judge.txt` (PASS), my gateway `crop_5_rootw009_eq_left_judge.txt`
  (PASS — the equation box sitting in that crop's corner), and the banked PIL measurements of
  every contested element in it (`adjudicate_5_disc*`, `adjudicate_5_ascii.txt`: disc 24.5px
  vs 29px, arrowhead-on-disc, arrow tip (249,292) both, one navy border, 12 dots at 7.2px).
- Exact next command if a future lane wants the gateway crop certificate (unchanged bytes):

```
cd "/worksp""aces/codespaces-blank/ai_llm_slides" && Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009 && scripts/16_vision_gate.sh timeout 1700 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison "$Q/crop_5_chart_left_render.png" "$Q/crop_5_chart_left_orig.png" --view "Slide 009 zoomed crop chart_left — render vs original at matched scale (attempt 5, independent verification worker w009-root-20261024)" --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: LEFT scatter chart frame x95..466 y107..474" --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 --transcript "$Q/crop_5_rootw009_chart_left_judge.txt" -p "$(cat "$Q/payload_B_v.txt")"
```

- Note: the chart_left region is exactly where the refuted Leg-A MAJOR sits; both crop-level
  certificates that DO exist for it (prior lane `crop_5_lane_chart_left_judge.txt`, PASS)
  and the banked PIL measurements already cover the disc/annotations.

## Evidence index
- Verdicts: `judge_attempt_5.txt` (full-slide PASS, prior lane);
  `crop_5_rootw009_{eq_left,eq_right,chart_right,chart_left}_judge.txt` (this lane);
  `crop_5_lane_*_judge.txt` (prior lane crops, preserved copies);
  `crop_3_cap_left/right_judge.txt` (carried).
- Adjudication/measurement: `adjudicate_5_disc.py/.txt`, `adjudicate_5_disc2.txt`,
  `adjudicate_5_ascii.txt`, `adjudicate_5_connector.txt`, `pil_verify_5{,b,c}.py/.txt`,
  `containment_5.txt`, `house_chrome_5_rootw009.txt`, `cut_crops_5.py/.txt`,
  `crossbuild_diff_5.txt`, `reconstruct_lane_crops.txt`.
- Dispatch provenance: `judge_prompt_5.txt`, `payload_A_v.txt`, `payload_B_v.txt`,
  `dispatch_legs_5.sh`, `dispatch_crops_5.sh`, `dispatch_crops_5.log`,
  `legB_*.log`, `probe_5_rootw009.txt`.
