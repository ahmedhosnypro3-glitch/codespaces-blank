# WORKER PROMPT — 09_introduction_to_neural_networks

**Mission**: Recreate 32 slides as judge-certified PPTX
**Your scope**: scope_17_24 (slides: slide_017,slide_018,slide_019,slide_020,slide_021,slide_022,slide_023,slide_024)
**Mission DB**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db
**Video namespace**: /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/
**Protocol**: MISSION_PROTOCOL.md (read and follow exactly)

---

## YOUR TASK

1. **CLAIM YOUR SCOPE**:
   ```
   /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db scope_17_24 worker-17_24
   ```

2. **FOR EACH SLIDE IN YOUR SCOPE** (in order):
   
   a. **Record task start**:
      ```
      /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh task-add /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db scope_17_24 {{SLIDE_NUM}} "source_research_started"
      ```

   b. **Phase A: Source Research** (doc-parse + web search)
      - Run doc-parse crop cascade on slide_NNN.jpg
      - Web search via agy for key concepts/equations/algorithms
      - Bank sources/slide_NNN_source/SOURCES.md with citations
      - Update task: `task-add ... "source_research_done"`

   c. **Phase B: Vision Analysis** (image-analysis skill)
      - Call scripts/16_vision_gate.sh with slide image
      - Output: analysis/slide_NNN_raw.json
      - Update task: `task-add ... "vision_analysis_done"`

   d. **Phase C: Text Validation**
      - Run python3 scripts/13_validate_slides.py analysis_dir
      - Output: analysis/slide_NNN_final.json
      - Content gate: score >= 8 required
      - Update task: `task-add ... "validation_done"`

   e. **Phase D: Build** (pptxgenjs + slide-recreation patterns)
      - Read references/patterns/index.json
      - Build slide_NNN_recreated.pptx with house frame
      - Closed-loop PIL checks vs original
      - Update task: `task-add ... "build_done"`

   f. **Phase E: Render + Visual Judge**
      - Render via LibreOffice headless → pdftoppm 150dpi
      - Run visual-judge (comparison: original vs rendered)
      - If FAIL: adjudicate findings vs measurements → fix → re-judge
      - Update task: `task-add ... "judge_pass"`

   g. **Phase E2: Post-passes**
      - Equations: OMML wrap via scripts/18_omml_wrapper.py
      - Re-render → re-judge if visual changes
      - Update task: `task-add ... "post_passes_done"`

   h. **Phase F: Final Deck Merge**
      - Replace page in deck_final.pptx at OPC level (byte-verbatim)
      - Update state ledger
      - Update task: `task-add ... "merged"`

3. **COMPLETE YOUR SCOPE**:
   ```
   /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db scope_17_24 "All 8 slides certified and merged"
   ```

---

## KEY COMMANDS & PATHS

- **Vision gate**: `scripts/16_vision_gate.sh` (from project root, pass VIDEO=machine-learning/09_introduction_to_neural_networks)
- **Doc-parse**: `python3 ~/.agents/skills/doc-parse/scripts/parse_document.py` (auto-resolves config)
- **Doc-parse crop cascade**: `python3 ~/.agents/skills/doc-parse/scripts/crop_cascade.py`
- **Analyze slides**: `python3 scripts/12_analyze_slides.py unique_slides_dir analysis_dir` (VIDEO env)
- **Validate slides**: `python3 scripts/13_validate_slides.py analysis_dir` (VIDEO env)
- **OMML wrap**: `python3 scripts/18_omml_wrapper.py input.pptx manifest.json -o output.pptx`
- **Visual judge**: Use visual-judge skill (subagent with frozen template)
- **Image analysis**: Use image-analysis skill (subagent with analyze_image.py)

---

## BINDING RULES (from MISSION_PROTOCOL.md)

- House frame rule: red frame, yellow badge (printed number 1-32), title at y=0.28
- Equations: 2D format (matplotlib mathtext → PNG 600dpi) + OMML wrap post-certification
- Graphs: generated via graphgen/ (scikit-learn + matplotlib, real data)
- Source research: MANDATORY per slide, bank under sources/slide_NNN_source/
- Single version: slide_NNN_recreated.pptx only
- Never commit, never delete certified files, never touch other scopes
- All DB writes via pool-db.sh (auto-stamped)
- Park unsolicited files → run_dir/orphans/

---

## SCOPE-SPECIFIC

scope_17_24 = scope_17_24
Slides: slide_017,slide_018,slide_019,slide_020,slide_021,slide_022,slide_023,slide_024
Count: 8

Start with slide slide_017, end with slide slide_024.