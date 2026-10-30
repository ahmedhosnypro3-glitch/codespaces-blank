# WORKER PROMPT — 09_introduction_to_neural_networks

**Mission**: Recreate 32 slides as judge-certified PPTX
**Your scope**: slide_020_solo (slides: slide_020)
**Mission DB**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db
**Video namespace**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/
**Run dir**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/runs/run-1793126532/
**Protocol**: MISSION_PROTOCOL.md (read and follow exactly)

---

## YOUR TASK

1. **CLAIM YOUR SCOPE**:
   ```
   /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db slide_020_solo {{AGENT_ID}}
   ```

2. **FOR EACH SLIDE IN YOUR SCOPE** (in order):
   a. `task-add ... slide_020 "source_research_done"`
   b. `task-add ... slide_020 "vision_analysis_done"`
   c. `task-add ... slide_020 "validation_started"` (run scripts/13_validate_slides.py on analysis dir)
   d. `task-add ... slide_020 "validation_done"`
   e. Build (pptxgenjs + patterns) `task-add ... "build_done"`
   f. Render + Judge (LO → pdftoppm 150dpi → visual-judge) `task-add ... "judge_pass"`
   g. Post-pass OMML wrap if equations `task-add ... "post_passes_done"`
   h. Final deck merge (OPC page replace) `task-add ... "merged"`

3. **COMPLETE YOUR SCOPE**:
   ```
   /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db slide_020_solo "slide certified and merged"
   ```

## RULES
- House frame rule: red frame, yellow badge (printed number 1-32), title at y=0.28 — overrides all analysis
- Equations: 2D (matplotlib mathtext → PNG 600dpi) + OMML wrap post-certification
- Graphs: generated via graphgen/ (sklearn + matplotlib, real data)
- Single version: slide_NNN_recreated.pptx only
- Never commit, never delete certified files, never touch other scopes' slides
- DB writes via pool-db.sh (auto-stamped)
- If analysis/slide_NNN_raw.json exists, vision is skipped; if validation already done, skip validation

## SCOPE
Slide: slide_020
Count: 1
