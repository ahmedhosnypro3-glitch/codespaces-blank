# AGENTS.md — Video-Specific Directives for 06_svm_with_kernels_quadratic_programming_libraries

## Video Identity

- **Course**: machine-learning (Zewail CSAI)
- **Lecture**: 06_svm_with_kernels_quadratic_programming_libraries
- **Namespace**: `videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/`
- **Unique slides**: 55 frames (slide_001.jpg – slide_055.jpg) in `unique_slides/`
- **Status**: Unique-frame extraction complete; human review **APPROVED** by the owner
  (2026-10-28: "do it, approved") — the HARD STOP is LIFTED for this namespace.

## KNOWN DEFECT (root cause of dump slides) — verification recorded 2026-10-28

Slides 023–055 were built from **UI-audit transcripts**, not recreation specs:

- `analysis/slide_023–055_raw.json` contain the image-analysis skill's *UI-audit* template
  (`## 1. LAYOUT MAP`, `## 2. FIRST-GLANCE TEST`, `## 6. AXIS 3` …) and carry **no**
  `slide_title`, `verbatim_text`, `layout.regions` or `visual_elements` — the fields the
  build step consumes. The build therefore had no content to place.
- Evidence: `slides_final.json` holds only 5 validated entries; 45 raw specs exist but only
  21 reached validation. Build scripts correlate with spec quality — slide 017 (valid spec)
  101 lines / 22 content calls, slide 022 128 lines / 27, while slide 045 56 lines / 5 and
  slide 050 51 lines / 5. 29 of 55 builds have fewer than 15 content calls.
- **Fix in flight**: `tools/reanalyze_all.py` re-analyses every original through
  `.agents/skills/image-analysis/scripts/analyze_image.py` with `analysis_prompt_v2.txt`
  (11 numbered sections: SLIDE_TITLE, VERBATIM_TEXT, LAYOUT, VISUAL_ELEMENTS, IMAGERY,
  COLORS, TYPOGRAPHY_NOTES, EQUATIONS, MEASUREMENTS, RECREATION_BRIEF, CONFIDENCE),
  banking to `qa/reanalysis2/slide_NNN_analysis.txt`. Idempotent and resumable.
- Never build a slide from a `## N.`-headed spec or from a parse transcript alone: those
  formats do not carry the recreation contract.

## Verified banked state (2026-10-28)

- `web_sources/slide_NNN/SOURCES.md` — **55/55** web-verified source research (per-slide
  claims, CONFIRMED/CORRECTED/UNVERIFIABLE, trusted sources only, ≤6 searches per slide).
- `qa/reanalysis2/slide_NNN_analysis.txt` — re-analysis transcripts as they land.
- `qa/rejudge2/ledger.jsonl` — judge verdict ledger; `judge_prompt_active.txt` holds the
  v4 judge template (full ground rules + binding output contract).
- `mission.db` — pooled-missions ledger: scopes, tasks, events.

## HARD STOP: Human Review Required (Non-Negotiable)

Per project-wide founder directive (2026-10-10): after frame extraction + phash dedup produce
`unique_slides/`, the pipeline HARD-STOPS. A human must review the extracted unique frames and
approve the set before ANY downstream processing (script 12 analysis, script 13 validation,
DB registration as ready, build dispatch, subagent fan-out). The machine may prepare a review
packet (index, contact sheet, new2old mapping draft) but must never approve the set itself.

## Pooled-Missions Configuration

- **Pool size**: 24 parallel subagents
- **Mission DB**: `videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/mission.db`
- **Run dir**: `videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/pool-run-<random>/`
- **Protocol file**: `MISSION_PROTOCOL.md` in the run dir (written before any spawn)
- **Scope partitioning**: 55 slides → scopes of ~5-15 slides each, cut along natural boundaries
- **All pooled-missions artifacts stay inside this video namespace** — no writes outside

## Parallel Skill Execution (Per-Scope Workers)

Each pooled-missions worker runs the full per-slide pipeline for its assigned slides:

1. **image-analysis + visual-judge** (combined):
   - Vision analysis of the slide frame via local gateway (http://localhost:17844/v1, model `images`)
   - Visual judge comparison (render vs original) using the frozen judge template
   - Output: analysis transcript + judge verdict (PASS/FAIL) per slide

2. **doc-parse** (with crop cascade):
   - Parse slide image via nemotron-parse family (doc-parse skill script)
   - Crop cascade for dense/complex regions (automated via `crop_cascade.py`)
   - Output: structured markdown transcript + JSON parse per slide

3. **web search** (source research):
   - Web-verified source research when slide content references external sources
   - Follows `references/source-research.md` laws (trust + economy, spec-correction protocol)
   - Output: SOURCES.md per slide where applicable

4. **slide-recreation** (build + certify):
   - pptxgenjs build per slide (house frame rule: outer red frame, badge, title position)
   - 2D math equations (matplotlib mathtext → PNG → pptxgenjs; OMML wrap via `18_omml_wrapper.py`)
   - Generated graphs for advanced plots (graphgen/ subproject, validated vs original)
   - LibreOffice headless render → pdftoppm 150dpi → closed-loop PIL checks
   - Visual judge certification (render vs original frame)
   - Output: `slide_NNN_recreated.pptx` (single version, no suffix variants)

## Model Endpoints (Project-Wide)

| Setting | Value |
|---|---|
| Vision base URL | `http://localhost:17844/v1` (IronRouter dist lane) |
| Vision model | `images` (virtual; fallback `glm-5.3-flash`) |
| Validation model | `validate_slides` (IronRouter model, 2026-10-21) |
| API key | `.analyze-image-key` at project root (mode 600) |
| Doc-parse endpoint | Per `scripts/.doc-parse-config` in doc-parse skill dir |

## House Frame Rule (Project-Wide, Overrides Per-Slide Analysis)

ALL recreated slides share ONE outer visual template from slide 3 (reference render):

- Slide size: `LAYOUT_WIDE` 13.33 × 7.5 in; background `#E8E8E8`
- Outer red frame: rect at `x=0.15, y=0.15, w=13.03, h=7.2`, border `#C00000` width 1.5
- Slide-number badge: yellow circle `x=12.48, y=0.30, w=0.5, h=0.5`, fill `#FFF9C4`,
  outline `#FFF9C4`, centered bold 18pt `#333333`. **Badge numeral = printed number on
  original slide image** (after curation, `unique_slides/slide_NNN.jpg` is named by that
  printed number, so badge reads exactly `N`).
- Slide title: text box starts at `y=0.28` (`x=0.6, w=12.13`, horizontally centered).

If a slide's spec or judge verdict disagrees with these positions/sizes, the house rule wins.

## Math Equation Format Rule

Any equation on a recreated slide renders in **Professional Format (2D / non-linear visual
representation)** — never Linear Format:

- Fractions: stacked with horizontal fraction bar (numerator above, denominator below)
- Summation (`∑`): large glyph with limits above/below (or to the right, e.g. `∑ᵢ₌₁ⁿ`)
- Subscripts/superscripts: spatially aligned with proper math-font spacing/proportions
- Mechanism: matplotlib mathtext → tight transparent PNG (600 dpi) → pptxgenjs.addImage()
  at exact size (`w = px/600` in). Hand-authoring OMML for rendering is forbidden.
- OMML wrap (editable in PowerPoint, pixel-identical in LibreOffice): `18_omml_wrapper.py`
  post-processes the certified PNG-based pptx (Choice = PowerPoint-authored pattern,
  Fallback = original PNG pic).

## Advanced-Graph Generation Rule

Slides with advanced graphs (3-D scatters, PCA projections, learned-model plots — anything
pptxgenjs native charts/shapes can only approximate) get graphs embedded from properly
generated images:

- Correct Python libraries per slide topic (e.g. scikit-learn + matplotlib for ML plots)
- Same AI algorithm on right data (e.g. `sklearn.decomposition.PCA` on real IRIS dataset)
- Tooling in `graphgen/` venv subproject; web research for lib choice via agy CLI
- Workflow: pick lib/function/algorithm/data → generate image matched to original's measured
  colors/orientation/region → validate (vision comparison) → fix → embed
- Single version per slide: `slide_NNN_recreated.pptx` HAS the generated graph; no
  `_graphed` variants. Evidence banks under `qa/slideNNN/graphgen/`.

## Continuous Final Deck

At human approval of the unique-frame set:
1. Initialize `<deck>_final.pptx` as PLACEHOLDER: one page per confirmed frame in printed-badge
   order, each page the original frame image full-bleed (presentable from day one).
2. When a slide certifies, replace its page with the certified per-slide deck's content at
   the OPC package level, byte-verbatim (never re-encode, never rebuild).
3. When last page replaced, run merge gate (0/N mismatched pages, merged render vs every
   source render, one LO session) and deliver final deck + md5 + banked gate report.

## Output Contract

`analysis/slides_final.json` — array of slide objects with: `slide_title`, `verbatim_text`
(bullets/labels/equations — VERBATIM, no paraphrasing), `layout` (arrangement + regions),
`visual_elements` (type, chart data values, colors, position), `imagery`, `colors`
(approx hex), `typography_notes`, `recreation_brief` (numbered recreation checklist),
`validation` block (verdict, fixes, uncertain items marked `[?]`, recreatability score).
Never invent facts — uncertain content keeps its `[?]` marker.

## Operational Rules

- **Always stream** vision-model requests (non-streaming cut at ~60s by upstream gateway).
- **phash dedup threshold 8** groups slide builds/animations; keep LAST frame of each group.
- **Validation model empty content** = transient parse error; re-run script 13.
- **Never delete banked evidence** — per-attempt builds, transcripts, renders, pre-fix
  backups, archived runs. Overwrite nothing certified; copy-then-modify.
- **All file writes stay inside this video namespace** — never write to another video's
  directory or project root.
- **Max 75 lines per single Write tool call** — split larger files across calls.
- **DB clock discipline**: stamp every DB write via `pool-db.sh` (uses `datetime('now')`);
  never write a remembered date.