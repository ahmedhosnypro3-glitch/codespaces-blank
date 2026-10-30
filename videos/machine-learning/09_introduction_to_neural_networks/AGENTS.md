# AGENTS.md — Video-Specific Directives for 09_introduction_to_neural_networks

## Video Identity

- **Course**: machine-learning (Zewail CSAI)
- **Lecture**: 09_introduction_to_neural_networks
- **Namespace**: `videos/machine-learning/09_introduction_to_neural_networks/`
- **Unique slides**: 32 (reviewed and approved by human)

## Binding Rules for This Video

1. **Human review complete** — unique_slides/ contains 32 approved frames (slide_001.jpg through slide_032.jpg). No further curation needed. Write slides_index.json once from the confirmed files in printed-badge order.

2. **House frame rule applies** — all recreated slides share the outer visual template from the project AGENTS.md (red frame, yellow badge, title position). Badge numeral = printed number on original slide image (1–32, no zero-padding).

3. **Math equations → Professional Format (2D)** — any equation on a recreated slide uses matplotlib mathtext → PNG (600 dpi) → pptxgenjs.addImage(). OMML wrap via scripts/18_omml_wrapper.py after certification.

4. **Advanced graphs → generated images** — slides with ML plots (loss curves, decision boundaries, architecture diagrams) use graphgen/ tooling with correct libraries (scikit-learn, matplotlib, numpy). Single version per slide: slide_NNN_recreated.pptx has the graph embedded.

5. **Source research mandate** — web-verified source research required for every slide's analysis (per course-level precedent from deep-learning/001_transformers_part1). Use agy search CLI; bank sources under sources/slide_NNN_source/ with SOURCES.md.

6. **Vision gateway** — all vision calls route through scripts/16_vision_gate.sh (fleet-global throttle on localhost:17844). Stream always; max_tokens 16000 for analysis.

7. **Validation model** — validate_slides (IronRouter model). Re-run script 13 on empty-content parse errors.

8. **Single-version deliverable** — one pptx per slide named slide_NNN_recreated.pptx (no suffixes). Graph slides have graph; equation slides have OMML wrap. Superseded builds → QA evidence dirs only.

9. **Continuous final deck** — at approval time, initialize <deck>_final.pptx as placeholder (32 pages, original images full-bleed). Replace each page byte-verbatim at OPC level when slide certifies. Deck closes when all 32 pages replaced and merge gate passes (0/N pixel mismatches).

10. **Pooled missions** — pool size 24. All mission artifacts (DB, protocol, run dir) live INSIDE this video namespace. No writes outside.

## Directory Structure (to be created)

```
videos/machine-learning/09_introduction_to_neural_networks/
├── AGENTS.md                          # this file
├── slides_index.json                  # 32 slides in printed-badge order
├── unique_slides/                     # 32 approved frames (EXISTS)
├── analysis/                          # slide_XXX_raw.json → slide_XXX_final.json, slides_final.json
├── sources/                           # slide_NNN_source/ research dirs
├── recreated_pptx/                    # build/, slide_NNN_recreated.pptx, final deck + .md5, qa/
├── slides_progress.db                 # per-video progress DB
├── pooled_missions/                   # mission DB, protocol, run dirs (this mission)
└── MISSION_PROTOCOL.md                # worker contract for this mission
```

## Model Endpoints (inherited from project root)

- Vision: http://localhost:17844/v1, model `images`, streaming, key from .analyze-image-key
- Validation: http://localhost:17844/v1, model `validate_slides`
- Web search: agy CLI (Google via antigravity proxy)
- Doc-parse: nemotron-parse family via doc-parse skill config