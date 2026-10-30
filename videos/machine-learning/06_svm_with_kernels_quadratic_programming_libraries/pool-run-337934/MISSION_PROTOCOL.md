# MISSION_PROTOCOL.md — Slide Recreation Mission for 06_svm_with_kernels_quadratic_programming_libraries

## Mission Overview

**Video**: machine-learning/06_svm_with_kernels_quadratic_programming_libraries
**Slides**: 55 unique frames (slide_001.jpg – slide_055.jpg)
**Pool size**: 24 parallel workers
**Mode**: ACT (change things — build and certify PPTX slides)
**Run dir**: pool-run-337934/
**Mission DB**: mission.db (in parent directory)

## Binding Rules

1. **Read the video's AGENTS.md** (at `../AGENTS.md`) and follow it exactly.
2. **Read the project AGENTS.md** (at `../../../../AGENTS.md`) and follow it.
3. **All file writes stay inside** `videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/` — never write outside.
4. **Max 75 lines per single Write tool call** — split larger files across calls.

## Scope Claim Protocol

- Claim your scope: `/home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim ../mission.db <scope_name> <your_agent_id>`
- Complete your scope: `scope-done ../mission.db <scope_name> [note]`
- Fail your scope: `scope-fail ../mission.db <scope_name> <reason>`
- Add task findings: `task-add ../mission.db <scope_name> <item> [detail]`
- Log events: `event ../mission.db <kind> <detail>`
- **Clock discipline**: Every DB write stamps via the helper (uses `datetime('now')`); never write a remembered date.

## Per-Slide Pipeline (Each Worker Executes for Every Slide in Its Scope)

For each slide number N in your scope's item list:

### 1. Vision Analysis (image-analysis skill)
- Input: `../unique_slides/slide_NNN.jpg`
- Tool: `/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py`
- Endpoint: `http://localhost:17844/v1` (model `images`, streaming, thinking disabled)
- Invocation: `python3 analyze_image.py analysis ../unique_slides/slide_NNN.jpg --timeout 240 --rounds 1 --tries 1 --view "Slide NNN — SVM/kernels/QP lecture frame" --capture "960x540 CSS px, 1.0, app" -p "$(cat /home/codespace/.agents/skills/image-analysis/assets/audit-prompt-template.md)"`
- Output: analysis transcript → `analysis/slide_NNN_raw.json` (per project script 12 contract)

### 2. Doc-Parse with Crop Cascade (doc-parse skill)
- Input: `../unique_slides/slide_NNN.jpg`
- Tool: `/home/codespace/ai_llm_slides/.agents/skills/doc-parse/scripts/parse_document.py` (full-frame) + `crop_cascade.py` (if dense)
- Config: `/home/codespace/ai_llm_slides/.agents/skills/doc-parse/scripts/.doc-parse-config` (script resolves it)
- Full-frame: `python3 parse_document.py ../unique_slides/slide_NNN.jpg -o parse_out_NNN --timeout 180`
- Crop cascade (if needed): `python3 crop_cascade.py ../unique_slides/slide_NNN.jpg --prompt-file /home/codespace/.agents/skills/doc-parse/references/prompts/crop_decision.md --out parse_cascade_NNN --max-crops 16 --max-parse-calls 24 --max-depth 6`
- Output: structured markdown + JSON parse per slide

### 3. Web Source Research (when slide references external sources)
- Use web search tool for any cited papers, algorithms, datasets, libraries
- Follow `references/source-research.md` laws (trust + economy, spec-correction protocol)
- Output: `sources/slide_NNN/SOURCES.md` where applicable

### 4. slide-recreation (Build + Certify)
- Tool: pptxgenjs build script; house chrome per `../AGENTS.md` (house rule wins over any spec)
- Build ONE version: `recreated_pptx/slide_NNN_recreated.pptx` — never `_graphed`/`_omml` suffixes
- Math: matplotlib mathtext → 600dpi PNG → `addImage()` at exact size, then `python3 ../../../../scripts/18_omml_wrapper.py <pptx> <manifest.json>`
- Graphs: `graphgen/` venv — correct library + the real algorithm on the real data, matched to the original's measured colors/orientation/region
- Render: `soffice --headless --convert-to pdf` + `pdftoppm -png -r 150` → `recreated_pptx/renders/`
- Closed-loop PIL checks (ink edges vs original, ~4px tolerance) BEFORE judging
- Judge: visual-judge with original FIRST, render SECOND → PASS required to certify

### 5. Certification (Per-Slide Close-Out)
1. Judge transcript banked to a file with a `FINAL VERDICT:` line bound to the slide's PPTX md5
2. Certified slide recorded in the mission DB and the progress DB
3. Final-deck page replaced at OPC level (placeholder → certified content, byte-verbatim)
4. Page replaced in final deck (placeholder → certified content)
5. Progress DB updated: `python3 ../../../../scripts/15_progress.py --video machine-learning/06_svm_with_kernels_quadratic_programming_libraries --slide NNN --stage certified`

## Failure Handling

- If a slide cannot be honestly completed: `task-add` with detail, or record blocker in scope note
- Reporting a blocker is valid completion; silent skipping is NOT
- Vision timeout/hang: retry once under wider wall (`--timeout 420` wrapped in `timeout 540`)
- Validation model empty content: re-run script 13 (transient)
- Judge FAIL: adjudicate findings vs measurements (pixels/DOM dispose), fix, re-judge (max 1 fix-loop cycle)
- If vision route wedged: probe first, sleep 300s, re-probe once; then batch ≥4 glm calls if consensus needed

## Guardrails

- Never commit; never delete anything — unsolicited files move to `$RUN_DIR/orphans/` after diff saved
- Workers never touch items outside their scope's list; cross-boundary work = new registered scope
- Park, never delete
- Report-only mode stops after reporting; acting never starts unasked (this mission is ACT mode)
- Run dir and DB are scratch state — safe to inspect, never part of target project

## Acceptance Gate (Final Verification)

After all scopes done:
1. All 55 slides have certified PPTX + PASS verdict
2. Final deck merge gate: `python3 ../../../../scripts/19_build_final_deck.py --video machine-learning/06_svm_with_kernels_quadratic_programming_libraries`
   - 0/N mismatched pages
   - Merged render vs every source render (one LO session)
   - Delivers final.pptx + md5 + gate report
3. Consolidated report: per-scope completion table, every task resolution, failures/wontfix rationales, open items
4. Mission DB (`../mission.db`) as complete ledger

---

# ADDENDUM — REJUDGE WAVE 2 (supersedes the prior scope set)

All 55 PPTX exist (`recreated_pptx/slide_NNN_recreated.pptx`) and all 55 renders were
regenerated fresh (2001x1125 @150dpi) under `recreated_pptx/renders/`. **No rebuilds in
this wave.** The mission is now purely: judge every slide, bank transcripts, report verdicts.

## Your scope

Your scope name is `scope_rej_<first>_<last>` with two slide numbers. Claim it first:

```
~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim ../mission.db <scope_name> <your_agent_id>
```

## Per-slide judging (both slides)

Run the driver — it does the gated call, the banking, the retry, and the ledger:

```
cd /home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
python3 tools/judge_slides.py <NNN> <MMM>
```

Driver details you must know:
- **Image order: image 1 = ORIGINAL frame, image 2 = recreation render** (visual-judge doctrine).
- It routes through `scripts/16_vision_gate.sh` (fleet cap 16 concurrent invocations).
- Wall: `timeout 540` around `--timeout 420 --rounds 1 --tries 1` (two-image comparisons need the wider wall).
- Up to 3 attempts per slide; a HangError/abort counts as a retry, a real PASS/FAIL stops the loop.
- Ledger: `qa/rejudge2/ledger.jsonl` (one row per attempt, never overwritten). Transcripts: `qa/rejudge2/slide_NNN_judge.txt`.
- Idempotent: a slide already PASS at its current PPTX md5 is skipped — safe to re-run.

## Reporting your scope

After both slides are judged:

```
~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done ../mission.db <scope_name> "NNN=PASS MMM=FAIL"
```

Record every non-PASS slide as a task so the fix wave can find it:

```
~/.agents/skills/pooled-missions/scripts/pool-db.sh task-add ../mission.db <scope_name> <NNN> "verdict: FAIL — <one-line finding summary>"
```

A FAIL is a valid, honest outcome. A scope is DONE when both slides have a banked
transcript with a terminal verdict line — not only when both are PASS.

---

# ADDENDUM — REBUILD WAVE 3 (supersedes the prior scope set)

The prior judge wave used a weak template and the prior builds for 29 slides were
"dump" builds (fewer than 15 content calls) created from UI-audit transcripts that
carry no recreation contract. Both problems are now fixed:

- `qa/reanalysis2/slide_NNN_analysis.txt` — NEW 11-section recreation spec per slide
  (SLIDE_TITLE, VERBATIM_TEXT, LAYOUT, VISUAL_ELEMENTS, IMAGERY, COLORS,
  TYPOGRAPHY_NOTES, EQUATIONS, MEASUREMENTS, RECREATION_BRIEF, CONFIDENCE).
  **This is the only source of content for a rebuild.**
- `judge_prompt_active.txt` — frozen v4 judge template (full ground rules + binding
  output contract). Do not trim or paraphrase it.

## Your scope

Scope name: `scope_rb_<first>_<last>`. Claim it first:

```
~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim ../mission.db <scope_name> <your_agent_id>
```

## Rebuild contract (per slide)

1. Read the NEW spec: `qa/reanalysis2/slide_NNN_analysis.txt` (skip any preamble
   before the line `1. SLIDE_TITLE` — the spec starts there).
2. Write `recreated_pptx/build/slide_NNN.js` (pptxgenjs). **Never** build from
   `analysis/slide_NNN_raw.json`, from a `## N.`-headed UI-audit transcript, or from
   the old build script — those are the dump source and are wrong.
3. House chrome is MANDATORY and overrides the spec:
   - 13.33 x 7.5 in (`LAYOUT_WIDE`), slide background `#E8E8E8`
   - outer red frame: `x=0.15, y=0.15, w=13.03, h=7.2`, line `#C00000` width 1.5, no fill
   - badge: oval `x=12.48, y=0.30, w=0.5, h=0.5`, fill `#FFF9C4`, outline `#FFF9C4`,
     centered bold 18 pt `#333333`, numeral = the slide number (no zero padding)
   - title: `x=0.6, y=0.28, w=12.13`, horizontally centered, bold, `#C00000`
   - the badge/frame/title box are never a discrepancy — do not "fix" them
4. Everything else comes from the spec, placed at the spec's measured geometry.
   Normalized spec coords [x0,y0,x1,y1] map to inches: `x*13.33`, `y*7.5`,
   `w=(x1-x0)*13.33`, `h=(y1-y0)*7.5`.
   - Use the spec's verbatim strings exactly, including its line structure and
     colors. Do NOT paraphrase, merge, or re-order text lines.
   - Do NOT invent or add text that the spec does not contain (a previous judge
     FAILed a slide for an extra body line that the original never had).
   - Keep title-case / styling per the spec's TYPOGRAPHY_NOTES.
5. Math (spec section 8): render with matplotlib mathtext at 600 dpi, tight
   transparent PNG, then `addImage()` at exact size (`w = px/600` inches, never
   rescaled). Never plain-text `x^2`, `x_1`, inline `a/b`, or `sum from i=1 to n`.
   Reuse `recreated_pptx/build/render_math.py` (see its usage docstring) and the
   existing `eq_034/` pattern for a multi-color equation; put new assets in
   `recreated_pptx/build/eq_NNN/`.
6. Graphs (spec section 4 IMAGERY/plot): a real generated plot, not a hand-drawn
   approximation. If `recreated_pptx/build/slide_NNN_graph.png` already exists and
   the spec's plot region matches it, reuse it; otherwise generate with matplotlib /
   scikit-learn per the spec and the advanced-graph rule.
7. Build with: `cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_NNN.js`
   — it writes `recreated_pptx/slide_NNN_recreated.pptx` (single version, NO suffix).
8. Render: `bash tools/render_all.sh NNN` from the video root →
   `recreated_pptx/renders/slide_NNN_recreated-1.png` (2001x1125 @150dpi).
9. Closed-loop check: compare the render against the original frame
   `qa/rejudge2/orig_png/slide_NNN.png` with PIL (ink edges, text presence). Fix
   obvious geometry errors before reporting. Scripts measure, judges judge.
10. Never delete anything. Never commit. Never write outside the video namespace.

## Reporting your scope

```
~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done ../mission.db <scope_name> "NNN=built NNN=built"
~/.agents/skills/pooled-missions/scripts/pool-db.sh task-add ../mission.db <scope_name> <NNN> "built from reanalysis2 spec; <notes>"
```

A blocker (e.g. spec missing) is a valid outcome: record it with `task-add`.
