# Rebuild brief — 08_performance_measure slide workers (2026-10-30 re-judge wave)

You are rebuilding ONE slide of the deck `videos/machine-learning/08_performance_measure/`.
Read this file fully, then your slide-specific section in `pool_run/spec_gaps.md`.

## Binding rules (read first)
- Root `AGENTS.md` (house frame rule, math format rule, single-version rule) and
  this namespace's `AGENTS.md` — both bind you.
- `pool_run/MISSION_PROTOCOL.md` — the binding worker contract (DB duties, liveness).
- Slide-recreation skill at `~/.agents/skills/slide-recreation/` — read
  `references/patterns/index.json` + `references/building.md` + `references/judging.md`
  before building/judging.

## Inputs for YOUR slide NNN (all inside this namespace)
1. `pool_run/image_analysis/slide_NNN_analysis.txt` — FRESH image-analysis-script read of
   the original frame (verbatim text, layout px at 960x540, chart values, colors). If it
   is a stub (<5000 bytes), use input 2 instead and say so.
2. `analysis/reanalysis/slide_NNN_raw.json` — machine-readable re-read of the original.
3. `analysis/slide_NNN_final.json` — the consumed spec (may be missing content; see 4).
4. `pool_run/spec_drift.md` / `pool_run/spec_gaps.md` — MATERIAL deltas: content present
   in the original but absent from the consumed spec. You MUST add every drifted item.
5. `sources/slide_NNN_research.md` — web-source research (confirms/corrects data values
   like ROC/AUC definitions; never invents frame content).
6. `unique_slides/slide_NNN.jpg` — the original frame (960x540; 1px = 1pt in build).

## House chrome (overrides everything, root AGENTS.md 2026-10-09)
- LAYOUT_WIDE 13.33x7.5in, bg `#E8E8E8`; red frame x0.15 y0.15 w13.03 h7.2 line
  `#C00000` 1.5pt no fill; badge oval x12.48 y0.30 w0.5 h0.5 fill+line `#FFF9C4`,
  bold 18pt `#333333` numeral = NNN (printed badge number); title box y0.28 x0.6
  w12.13 centered.
- Equations: matplotlib mathtext -> 600dpi transparent PNG -> addImage at exact size
  (w = px/600 in). Professional 2D format only. OMML wrap via `scripts/18_omml_wrapper.py`
  only after judge PASS.
- Graphs needing real plotting: generate with the correct library in `graphgen/` venv,
  embed in the same single pptx.

## Build + verify loop
1. Write `recreated_pptx/build/slide_NNN.js` (pptxgenjs). Copy-then-modify: never delete
   prior build scripts or QA evidence.
2. Render: LibreOffice headless -> pdftoppm 150dpi -> `recreated_pptx/qa/slideNNN/render_K.png`.
3. Pre-judge PIL self-checks (frame containment, delimiters, tables, line spacing) —
   closed-loop against the original's measured ink edges (~4px tolerance at 150dpi).
4. JUDGE (mandatory original-first order):
   `scripts/16_vision_gate.sh <pyenv python> .agents/skills/image-analysis/scripts/analyze_image.py \
     comparison <unique_slides/slide_NNN.jpg> <render_K.png> --thinking high --max-tokens 65536 \
     --timeout 420 --rounds 1 --tries 1 -p "$(cat pool_run/judge_prompt_template.txt)"`
   wrapped in `timeout 540`. IMG1 = original frame, IMG2 = render. Transcript:
   `recreated_pptx/qa/slideNNN/judge_attempt_K.txt`. Probe first with `--timeout 120`.
5. PASS -> corroboration read: fresh call, same order, transcript
   `judge_verify_K.txt`. Both PASS = certified. Record both paths in
   `pool_run/verification_ledger.md` and set status in `pool_run/mission.db` via
   `~/.agents/skills/pooled-missions/scripts/pool-db.sh`.
6. FAIL -> adjudicate findings against pixels (never obey blind), fix, re-render as
   render_{K+1}, judge again. Max 6 attempts, then `scope-fail` with reasons.

## Interpreter / endpoint
- Python: `/home/codespace/.pyenv/versions/3.15.2/bin/python3` (bare python3 lacks openai).
- Vision gate: `bash scripts/16_vision_gate.sh ...` from repo root. Always stream (the
  script does). Never read the API key file yourself.

## Done criteria
- `recreated_pptx/slide_NNN_recreated.pptx` exists (single version, no suffixes),
  all drift items from spec_gaps.md are visibly present, judge_attempt_K + judge_verify_K
  both end `FINAL VERDICT: PASS` in original-first order, ledger + DB updated.
