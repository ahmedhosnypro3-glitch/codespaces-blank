# MISSION PROTOCOL — 09_introduction_to_neural_networks

**Video**: machine-learning/09_introduction_to_neural_networks
**Total slides**: 32 (approved unique frames in unique_slides/)
**Pool size**: 24 workers
**Mission DB**: pooled_missions/mission.db
**Run dir**: pooled_missions/runs/<run-id>/

---

## 1. MISSION INTAKE (three sentences)

**Work items**: 32 slides, each requiring: source research → vision analysis → text validation → pptxgenjs build → render → visual judge → equation/graph post-passes → certification → final deck page replacement.

**Done criteria per scope**: All slides in the scope have judge-certified PASS (comparison verdict PASS against original frame), with equations in 2D format + OMML wrap, advanced graphs generated and embedded, and the final deck page replaced byte-verbatim at OPC level. Scope completes when its 8 slides are fully certified and merged.

**Mode**: ACT — workers modify files (create analyses, builds, renders, wrapped pptx). Never commit; commits only on explicit user request.

---

## 2. BINDING RULES (read project AGENTS.md + video AGENTS.md first)

- **House frame rule**: ALL slides share outer template (red frame 0.15in inset, yellow badge at 12.48/0.30, title at y=0.28). Badge = printed number (1–32). Overrides any analysis/judge finding on these elements.

- **Equations**: Professional Format (2D) only — matplotlib mathtext → PNG 600dpi → pptxgenjs.addImage(w=px/600). OMML wrap via scripts/18_omml_wrapper.py AFTER certification. Never hand-author OMML for rendering.

- **Graphs**: Advanced ML plots → generated via graphgen/ (scikit-learn + matplotlib, real algorithm on real data). Validate via vision comparison vs original. Single version: slide_NNN_recreated.pptx has graph embedded.

- **Source research**: MANDATORY per slide. Web-verified sources confirm/correct DATA only. Bank under sources/slide_NNN_source/ with SOURCES.md. Never invent content slide doesn't show.

- **Single version**: One pptx per slide named slide_NNN_recreated.pptx. No _graphed/_omml suffixes.

- **Continuous final deck**: At approval, initialize deck_final.pptx (32 placeholder pages, original images full-bleed). Replace page byte-verbatim at OPC level on certification. Deck closes when merge gate passes (0/32 pixel mismatches).

- **Vision gateway**: ALL calls through scripts/16_vision_gate.sh (fleet-global throttle on localhost:17844). Stream always. max_tokens=16000 for analysis.

- **Validation model**: validate_slides (IronRouter). Re-run on empty content.

- **Evidence**: Never delete banked evidence (builds, transcripts, renders, pre-fix backups). Overwrite nothing certified; copy-then-modify.

---

## 3. PER-SLIDE WORKER PROTOCOL (each worker owns one slide end-to-end)

### Phase A: Source Research (doc-parse + web search)
1. Run doc-parse skill (crop cascade) on slide_NNN.jpg → parse transcript
2. Web search via agy for key concepts, equations, algorithms on slide
3. Bank sources/slide_NNN_source/SOURCES.md with citations
4. Output: research summary + corrected facts (marked [?] if uncertain)

### Phase B: Vision Analysis (image-analysis skill)
1. Call scripts/16_vision_gate.sh with slide image + analysis prompt
2. Stream response, timeout 600s, max_tokens 16000
3. Output: slide_NNN_raw.json (verbatim text, layout, visual elements, colors, typography, recreation_brief)

### Phase C: Text Validation
1. Run script 13_validate_slides.py on raw.json
2. Output: slide_NNN_final.json with validation block (verdict, fixes, uncertain items [?], recreatability score)
3. Content gate: score >= 8 required to proceed

### Phase D: Build (pptxgenjs + slide-recreation patterns)
1. Read references/patterns/index.json — use applicable patterns
2. Build slide_NNN_recreated.pptx with house frame, badge, title
3. Embed equations as PNG (2D) + OMML wrap post-certification
4. Embed graphs as generated images (graphgen/)
5. Closed-loop PIL checks: measure ink edges vs original (~4px tolerance at 150dpi)

### Phase E: Render + Visual Judge
1. Render via LibreOffice headless → pdftoppm 150dpi → PNG
2. Run visual-judge (comparison mode): original frame vs rendered PNG
3. Judge template: frozen, versioned (from slide-recreation skill references/judging.md)
4. PASS = done | FAIL = adjudicate findings vs measurements → fix → re-judge

### Phase E2: Post-passes (after judge PASS)
- Equations: OMML wrap via scripts/18_omml_wrapper.py (manifest from eq_*.json sidecars)
- Graphs: already embedded in build
- Re-render → re-judge if post-pass changes visual output

### Phase F: Final Deck Merge
1. Replace page in deck_final.pptx at OPC level (byte-verbatim, no re-encode)
2. Update state ledger (placeholder|certified with source md5s)

---

## 4. WORKER DISCIPLINE

- **Claim scope**: `scope-claim <db> <scope> <agent-id>` — then work ONLY that scope's slides
- **Complete scope**: `scope-done <db> <scope> [note]` — all 8 slides certified
- **Fail scope**: `scope-fail <db> <scope> <reason>` — honest blocker report
- **Task tracking**: `task-add <db> <scope> <slide> <detail>` for each slide milestone
- **Clock**: Every DB write auto-stamped via pool-db.sh (datetime('now'))
- **Never**: commit, delete certified files, touch other scopes' items, invent content
- **Park, never delete**: unsolicited files → run_dir/orphans/ after diff saved

---

## 5. JUDGE PROTOCOL (visual-judge skill)

- **Mode**: Comparison judge (original frame FIRST, rendered PNG SECOND)
- **Probe first**: one cheap call on banked image before expensive judge call
- **Capture**: settle ≥4s, PIL-check PNG (dims + mean), verify state before/after
- **Pre-check gate**: mechanical checks on capture — FAIL = retake, never score as-is
- **Measure**: pixel measurement (PIL) for rendered artifacts — ground truth wins
- **Arbitrate**: vision proposes; pixels dispose. Disproven finding = DISMISSED
- **Verdict law**: only banked transcript with coherent body + explicit verdict line counts
- **Single-model cert**: valid but labeled "single-read, unconfirmed"
- **Banned routes**: kimi-k3, gemini, claude — verdicts void
- **Leg count**: single-read vs corroborated (≥2 models)

---

## 6. DOC-PARSE LANE (crop cascade)

- Script: ~/.agents/skills/doc-parse/scripts/parse_document.py
- Config: ~/.agents/skills/doc-parse/scripts/.doc-parse-config (never read/print)
- Crop cascade: scripts/crop_cascade.py for dense slides
- Prompt file: references/prompts/crop_decision.md (pass via --prompt-file)
- Chat adjudicator: advisory only, never gatekeeper
- Output: <stem>.parse.md + <stem>.parse.json in fresh output dir per call
- Adjudicate parse claims against source image (vision subagent for visual claims)

---

## 7. POOL OPERATIONS

- **Spawn**: 24 background subagents max (Agent tool, run_in_background=true)
- **Refill**: on completion, cross-check DB (scope row advanced?), refill slot immediately
- **Priority**: failed scopes needing redispatch first, pending scopes second
- **Resume**: interrupted workers via Agent(resume=<agent-id>); DB is source of truth
- **Drift**: worker editing outside scope → stop via TaskStop, redispatch FRESH agent
- **Watch**: checksum-watch tree if gate fails on unowned items (find -newermt + md5sum)

---

## 8. FINAL VERIFICATION (gate)

```bash
# Run from video namespace
python3 scripts/15_progress.py --video machine-learning/09_introduction_to_neural_networks --gate
# Must report: 32/32 slides certified, 0/32 pixel mismatches in merge gate
```

Exit code captured explicitly (no piping to tail). Non-zero = red exit.

---

## 9. REPORT DELIVERABLES

- Per-scope completion table
- Every task with resolution
- Failure/wontfix rationales
- Open items for user decision
- mission.db as complete ledger
- Recommendation: APPROVE / RE-RUN OPEN SCOPES / NEEDS DECISIONS

---

## 10. SCOPE DEFINITIONS (registered in mission.db)

| Scope | Slides | Count |
|-------|--------|-------|
| scope_01_08 | slide_001–slide_008 | 8 |
| scope_09_16 | slide_009–slide_016 | 8 |
| scope_17_24 | slide_017–slide_024 | 8 |
| scope_25_32 | slide_025–slide_032 | 8 |

Workers claim ONE scope at a time. 4 scopes × 8 slides = 32 total. Pool size 24 means up to 3 scopes in flight simultaneously (24/8).