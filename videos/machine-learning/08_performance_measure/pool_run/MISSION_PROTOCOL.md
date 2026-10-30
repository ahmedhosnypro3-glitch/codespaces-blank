# MISSION_PROTOCOL — 08_performance_measure slide recreation

## Mission

Recreate all 37 slides from `videos/machine-learning/08_performance_measure/unique_slides/` as judge-certified PPTX files (`slide_NNN_recreated.pptx`) following the slide-recreation skill pipeline.

## Binding rules

- Read the project root AGENTS.md and this video's AGENTS.md first — follow both.
- Read `~/.agents/skills/slide-recreation/SKILL.md` and its references (pipeline.md, building.md, judging.md, equations.md, graphs.md, dependencies.md, patterns/index.json, operations.md) for the current phase.
- Read `~/.agents/skills/image-analysis/SKILL.md` and `assets/process-notes.md` for vision analysis routing/dispatch law.
- Read `~/.agents/skills/visual-judge/SKILL.md` and its references for judging protocol.
- Read `~/.agents/skills/doc-parse/SKILL.md` and its references for doc-parse crop cascade.
- Read `pool_run/defect_patterns.md` before your first fix cycle (it exists — re-read at each new slide) — it maps the judge's
  natural-language findings to fix recipes and pre-judge checks. Re-read it when you start a new slide.
- All work stays inside `/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/` — never write outside.
- Pool size: 24 workers. Background subagents only.

## Worker protocol (per slide)

For each slide N in your scope:

1. **Claim scope**: `pool-db.sh scope-claim <db> <scope-name> <your-agent-id>`
2. **Run the full slide-recreation pipeline** per `~/.agents/skills/slide-recreation/references/17_worker_instructions.md`:
   - Read spec: `analysis/slide_NNN_final.json` (after analysis/validation complete)
   - Build PPTX: write `recreated_pptx/build/slide_NNN.js` using pptxgenjs + house chrome from root AGENTS.md
   - Render: LibreOffice headless → pdftoppm 150dpi PNG to `recreated_pptx/qa/slideNNN/render_K.png`
   - Self-check: mandatory pre-judge PIL checks (frame containment, equations, delimiters, tables, line spacing, zoomed crop vision)
   - Judge: invoke visual-judge via image-analysis script through vision gate (`scripts/16_vision_gate.sh`) — comparison args MUST be `comparison <original_frame> <render_png>` — ORIGINAL FIRST, RENDER SECOND (original-first read order is mandatory per visual-judge comparison-judge law; a render-first call is a protocol violation and its transcript is void for certification)
   - Loop: fix issues, re-render, re-judge (max 6 attempts)
   - Post-passes: equations (2D + OMML wrap), graphs (generated images) — single version per slide
   - **Corroboration read (mandatory, dual-read law)**: after the first `FINAL VERDICT: PASS`,
     run a SECOND independent visual read of the SAME render vs the same original — fresh vision
     call, fresh transcript `recreated_pptx/qa/slideNNN/judge_verify_K.txt` (K = the PASS attempt
     number), SAME frozen judge prompt. It must also return `FINAL VERDICT: PASS`.
     A corroboration FAIL re-opens the slide: fix, re-render, re-judge as attempt K+1, and
     corroborate again as `judge_verify_K+1.txt`. Never copy or re-use the first transcript.
   - On dual PASS: update DB `gen_status=passed`, `visual_check=PASS`, bank component if slide has dependents
   - **Continuous final deck**: after the post-passes (equations OMML wrap, graph images) are baked into the
     slide's own pptx, run
     `python3 pool_run/merge_final_deck.py update <N> recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx`
     so the combined deck's page N holds the slide's FINAL bytes. The update is idempotent — re-run it after
     ANY later change to the pptx (the close-time pixel gate compares the deck against the per-slide decks).
3. **Complete scope**: `pool-db.sh scope-done <db> <scope-name> "slide N PASS"` — one per slide, or batch at end

## Done criteria per slide

- `gen_status=passed` in progress DB
- `visual_check=PASS` with comparison transcript
- `slide_NNN_recreated.pptx` exists at `recreated_pptx/`
- Judge transcript at `recreated_pptx/qa/slideNNN/judge_attempt_K.txt` shows FINAL VERDICT: PASS
- **Corroboration transcript** at `recreated_pptx/qa/slideNNN/judge_verify_K.txt` shows FINAL VERDICT: PASS
  (dual-read law — a single PASS is not certification)
- Row present in `pool_run/verification_ledger.md` with `certified=yes`

## Scope partitioning

| Scope | Slides | Items |
|-------|--------|-------|
| scope-1 | 1-9 | 9 |
| scope-2 | 10-18 | 9 |
| scope-3 | 19-27 | 9 |
| scope-4 | 28-37 | 10 |

Each worker claims ONE scope and processes its slides sequentially.

## Concurrency & vision gate

- Vision calls go through `scripts/16_vision_gate.sh` (fleet-global throttle)
- Image-analysis script uses DEFAULT route (`images` model) — NO `--models` flag
- Probe first (timeout 120s), then comparison (timeout 420s wrapped in 540s)
- `--thinking high --max-tokens 65536` for comparisons
- Single-model certificates: record "glm leg DEFERRED/BLOCKED"

## Doc-parse lane

- Enabled per AGENTS.md: run `crop_cascade.py` for dense slides (equations, tables)
- Config: `~/.agents/skills/doc-parse/scripts/.doc-parse-config` (probe first)
- Outputs to `analysis/parse/slide_NNN.parse.md/.json`

## Web research

- Use `mcp__agy-cli-mcp__agy_web_search` for library/algorithm choices (graphs)
- Bank sources under `sources/slide_NNN_source/` + `SOURCES.md`

## DB updates

- Update `slides_progress.db` at every milestone via `scripts/15_progress.py` with `VIDEO=machine-learning/08_performance_measure`
- Fields: `gen_status`, `pptx_path`, `build_script`, `visual_check`, `visual_attempts`, `visual_transcript`, `last_error`

## Failure handling

- If blocked by dependency: `scope-fail` with `dep-gated: waiting on <ids>`
- If judge fails 6×: `scope-fail` with `judge-exhausted: <remaining issues>`
- Never delete banked evidence (transcripts, renders, build scripts)

## Final gate

- All 4 scopes `done` → run merge gate (0/N pixel check on final deck)
- Report: per-scope table, all tasks, failures, `mission.db` as ledger