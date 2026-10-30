# WORKER PROMPT — 09_introduction_to_neural_networks

**Mission**: Recreate 32 slides as judge-certified PPTX
**Your scope**: scope_016 (slides: slide_016)
**Mission DB**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db
**Video namespace**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/
**Protocol**: MISSION_PROTOCOL.md (read and follow exactly)

---

## YOUR TASK

1. **CLAIM YOUR SCOPE**:
   ```
   /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db scope_016 {{AGENT_ID}}
   ```

2. **FOR EACH SLIDE IN YOUR SCOPE** (in order):
   a. `task-add ... {{SLIDE_NUM}} "source_research_started"`
   b. Phase A: Source Research (doc-parse + agy web search) → bank sources/slide_NNN_source/SOURCES.md
   c. Phase B: Vision Analysis (scripts/16_vision_gate.sh) → analysis/slide_NNN_raw.json
   d. Phase C: Validation (scripts/13_validate_slides.py) → analysis/slide_NNN_final.json, score >= 8
   e. Phase D: Build (pptxgenjs + patterns) → slide_NNN_recreated.pptx + PIL checks
   f. Phase E: Render + Judge (LO headless → pdftoppm 150dpi → visual-judge comparison) → PASS
   g. Phase E2: OMML wrap if equations (scripts/18_omml_wrapper.py) + re-render/re-judge
   h. Phase F: Final deck merge (OPC byte-verbatim page replace) → state ledger
   Record each milestone via `task-add` / `task-done`.

3. **COMPLETE YOUR SCOPE**:
   ```
   /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db scope_016 "All 1 slides certified and merged"
   ```

## RULES (from MISSION_PROTOCOL.md)
- House frame rule: red frame, yellow badge (printed number 1-32), title at y=0.28 — overrides all analysis
- Equations: 2D format (matplotlib mathtext → PNG 600dpi) + OMML wrap post-certification
- Graphs: generated via graphgen/ (scikit-learn + matplotlib, real data)
- Source research MANDATORY per slide → sources/slide_NNN_source/
- Single version: slide_NNN_recreated.pptx only
- Never commit, never delete certified files, never touch other scopes
- All DB writes via pool-db.sh (auto-stamped)
- If outputs already exist from other workers, scripts are idempotent — skip to next phase

## SCOPE-SPECIFIC
Slides: slide_016
Count: 1
Start: slide_016 End: slide_016
