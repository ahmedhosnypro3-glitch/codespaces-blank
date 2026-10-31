# LANE_PROTOCOL.md — Gateway-free verification lanes for 10_nn_training_and_example

**Mission:** complete the verification work that does NOT need the shared vision gateway,
while the vision drivers (`_pool/reanalysis_driver.sh`, `_pool/rejudge_certified_driver.sh`)
and the 10 live build workers own the gateway.

**Binding rules (read first, in this order):**
1. `/home/codespace/ai_llm_slides/AGENTS.md` (project root)
2. `videos/machine-learning/10_nn_training_and_example/AGENTS.md` (this video)
3. `_pool/MISSION_PROTOCOL.md` and `_pool/REJUDGE_PROTOCOL.md`
4. This file

**Namespace fence:** write ONLY inside `videos/machine-learning/10_nn_training_and_example/`.
Never outside it. Never in another video's namespace. Never in the project root.

**File-write limit:** ≤75 lines per single Write tool call; use append mode to continue.

**DB:** `_pool/mission.db`. Helper: `~/.agents/skills/pooled-missions/scripts/pool-db.sh`.
- Claim: `scope-claim _pool/mission.db <scope> <your agent id>`
- Close: `scope-done _pool/mission.db <scope> "note"` or `scope-fail <db> <scope> "<reason>"`
- Blocker/work item: `task-add _pool/mission.db <scope> <item> "<detail>"`
- Every write is stamped by the helper. Never write a remembered date.
- Never commit. Never delete anything — park unsolicited files in `_pool/orphans/` with a note.

**NEVER** start a vision-gateway call (`analyze_image.py`) from these lanes — the shared
gateway is stormed fleet-wide and the drivers own it. If a task seems to need the gateway,
record it with `task-add` and move on.

---

## Lane G — Geometry closed-loop PIL verification (scopes `b_geom_1..4`)

For each slide in your list:
1. Render the CURRENT canonical deliverable `recreated_pptx/slide_NNN_recreated.pptx`
   (skip if absent — record a task, do not fail the scope). LO headless with a PRIVATE
   profile under `_pool/lo_geom_<your scope>/`, then `pdftoppm -png -r 150`.
   `TMPDIR` must point inside this namespace. Never use a shared LO profile.
2. PIL-check the PNG: dimensions 2000x1125 (+/- 8px), non-blank mean in 20..245.
3. Measure the INK EDGES of slide-specific content in BOTH the render and
   `unique_slides/slide_NNN.jpg`. The original frame is 960x540; the render is 2000x1125.
   Normalize to the 960x540 frame scale before comparing.
4. Compare region by region (title block, body/equation/diagram/table region, footer).
   Tolerance: ~4px at 150dpi (~2px at frame scale) for a position/size deviation.
5. Write `qa/slideNNN/geom_<your scope>.md` with, per region: measured render box,
   measured original box, normalized delta, and PASS / EXCEEDS-TOLERANCE.
6. A region that EXCEEDS tolerance is a GEOMETRY FINDING — it is an input to adjudication,
   not an automatic rebuild. Record it in the report with numbers.

Done criteria per scope: one `geom_<scope>.md` per slide in scope, each with measured
numbers for every region and an explicit PASS / EXCEEDS-TOLERANCE line per region;
`task-add` for every slide you could not measure and why.

---

## Lane P — doc-parse adjudication (scopes `b_parse_1..4`)

For each slide in your list:
1. Read `analysis/parse/slide_NNN.parse.md` (the parse transcript) and the certified
   `analysis/slide_NNN_final.json` if present.
2. Inspect the SOURCE IMAGE `unique_slides/slide_NNN.jpg` with `ReadMediaFile` — ONE
   image per tool call, never batch two images in one call.
3. Adjudicate every claim the parse makes that you intend to bank: layout order, text
   presence, table column count, chart reading order, reading order of blocks.
   Classify each as REAL / HALLUCINATED / DEBATABLE with a measurement or a quoted
   source-image string as evidence.
4. Write `analysis/parse/adjudication/slide_NNN.md` (≤75 lines/Write) with: parse
   summary, per-claim dispositions, and an overall verdict line
   `PARSE VERDICT: CLEAN | DEFECTS | DEGRADED`.
5. The parse lane is ADVISORY. A defect here never blocks certification on its own — it
   is a judge-adjudication input. Never edit the certified analysis JSON.

Done criteria per scope: one adjudication file per slide in scope, each with a terminal
`PARSE VERDICT:` line and per-claim dispositions.

---

## Lane S — Web-source audit + sources map (scopes `b_src_1..2`)

For each slide in your list:
1. Read `sources/slide_NNN_source/SOURCES.md`. Verify it names the slide's actual topic,
   cites real URLs, and its "Corrections / notes" are honest about what could NOT be verified.
2. Use the web-search MCP (`mcp__agy-cli-mcp__agy_web_search`) to independently confirm the
   slide's DATA claims (algorithm, dataset, library, formula, numeric values) — best-effort,
   never a hard dependency. Never invent a source: if the search returns nothing usable,
   say so honestly in the file.
3. Rewrite that slide's `sources/slide_NNN_source/SOURCES.md` (copy-then-modify; keep every
   prior source and note) so it reflects the audit result.
4. Rebuild the fleet index `SOURCES_MAP.md` with ONE ROW PER SLIDE (1..34) — every slide in
   the deck, not just the scopes that happened to run — with columns:
   slide | SOURCES.md | sources count | state | notes. Only one agent writes SOURCES_MAP.md:
   the agent whose scope contains slide 034 waits for the others' files and writes it last.
5. Never mark a slide "done" unless its SOURCES.md exists and cites at least one real URL.

Done criteria per scope: every slide in scope has an audited `SOURCES.md`; `SOURCES_MAP.md`
lists all 34 slides with one row each.

---

## REPORTING
Final message per agent: scope name, slides covered, files written, findings by severity,
anything left open. Keep it compact. The DB is the complete ledger.
