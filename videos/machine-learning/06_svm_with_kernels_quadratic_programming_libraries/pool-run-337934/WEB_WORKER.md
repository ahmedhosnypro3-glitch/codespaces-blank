# Your task — web-source research for slide __SLIDE__ of 06_svm

Video namespace: `/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries`

## Read first (do not skip)

1. `pool-run-337934/PROTOCOL_WEB.md` — the binding protocol (trust law, economy law,
   spec-correction protocol, exact output shape). Follow it exactly.
2. `parse_out___SLIDE__/slide___SLIDE__.parse.md` — what the slide actually shows.
3. `analysis/slides_final.json` — find the entry for slide `__SLIDE__` to see the spec.

## Do

1. Claim your scope in the mission DB:
   `~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim mission.db scope_web___SLIDE__ web_worker___SLIDE__`
   (run from the video namespace dir). If it is not pending, stop and report that.
2. Do the web research with the `mcp__agy-cli-mcp__agy_web_search` tool — at most 6
   searches, stop early when claims are confirmed. Deterministic searches only.
3. Write `web_sources/slide___SLIDE__/SOURCES.md` in the exact shape in the protocol.
4. Close the scope:
   `~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-done mission.db scope_web___SLIDE__ "<verdict>"`

## Rules

- Max 75 lines per Write tool call; only ONE file to write (SOURCES.md, ≤45 lines).
- Never write outside the video namespace.
- Never invent content the slide does not show; sources correct DATA only.
- If the slide needs no verification (pure prose), spend 0 searches and write
  `NEEDS_NO_SOURCE` — that is a valid, complete result.
- Report back: verdict line, claims checked count, searches spent.
