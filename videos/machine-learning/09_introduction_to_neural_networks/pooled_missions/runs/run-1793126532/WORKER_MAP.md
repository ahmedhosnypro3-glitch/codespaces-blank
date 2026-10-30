# WORKER MAP — wave 3 (rewritten 2026-10-29)

Watchdog resume map. Waves 1-2 are DEAD: wave-1 (agent-36..67) died with app exits;
wave-2 (agent-68..91) died with an app exit AND the Agent(resume=...) path 400s at the
provider for their contexts — do NOT resume those ids. Wave-3 agents are fresh contexts.
Ownership is read FRESH from the mission DB each fire; this file is only the
scope→agent-id lookup used when a resume is actually needed.

DB = /home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/mission.db
PROTOCOL = .../pooled_missions/runs/run-1793126532/REJUDGE_PROTOCOL.md (fixed 2026-10-28:
project-level IMG path; judge comparison order = recreation FIRST, original SECOND)

| Scope / lane | Slides | Agent ID |
|---|---|---|
| src_001-004 (sources_gap) | 001-004 | agent-92 |
| src_005-008 (sources_gap) | 005-008 | agent-93 |
| src_009-012 (sources_gap) | 009-012 | agent-94 |
| src_013-016 (sources_gap) | 013-016 | agent-95 |
| src_017-020 (sources_gap) | 017-020 | agent-96 |
| src_021-024 (sources_gap) | 021-024 | agent-97 |
| src_025-028 (sources_gap) | 025-028 | agent-98 |
| src_029-032 (sources_gap) | 029-032 | agent-99 |
| rejudge_001 | 001 | agent-100 |
| rejudge_003 | 003 | agent-101 |
| rejudge_005 | 005 | agent-102 |
| rejudge_007 | 007 | agent-103 |
| rejudge_008 | 008 | agent-104 |
| rejudge_010 | 010 | agent-105 |
| rejudge_011 | 011 | agent-106 |
| rejudge_013 | 013 | agent-107 |
| rejudge_014 | 014 | agent-108 |
| rejudge_015 | 015 | agent-109 |
| rejudge_018 | 018 | agent-110 |
| rejudge_019 | 019 | agent-111 |
| rejudge_020 | 020 | agent-112 |
| rejudge_021 | 021 | agent-113 |
| rejudge_022 | 022 | agent-114 |
| rejudge_031 | 031 | agent-115 |

Wave-3b (NOT yet dispatched — dispatch FRESH agents as pool slots free, pool cap 24):
slides 002, 004, 006, 009, 012, 016, 017, 023, 024, 025, 026, 027, 028, 029, 030, 032
with scopes rejudge_002 ... rejudge_032.

Orchestrator background lanes (bash, not agents):
- crop cascades: sources/docparse_cascades/slide_NNN/ (all 32 EXIT=0 as of 2026-10-29)
- fresh vision re-analysis: analysis/reanalysis_v2/slide_NNN_reanalysis.txt (all 32)

Contract: pooled_missions/runs/run-1793126532/REJUDGE_PROTOCOL.md
A scope row stays in_work until its worker calls scope-done/scope-fail.
