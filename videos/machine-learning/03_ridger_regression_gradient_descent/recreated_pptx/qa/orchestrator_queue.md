# Orchestrator queue — deck 03 (founder cap: MAX 4 concurrent subagents, session 2026-10-20 night)

## Current slots (4/4)
- 027 resume (complete attempt-2 bank: build, 6 crop pairs, renders, selfchecks; judging never landed)
- 011 resume (build + render banked; judging never ran)
- 023 resume (18-file forensics/geometry bank; NO build yet)
- 026 build from 8-pass measurement bank (no build/render/judge)

## Background validation lanes (NOT subagents — exempt from the cap)
- lane D: slides 019 031 034 037 (one ranged pass each, 32k)
- lane E2: range 38-51 (fills 041-047, 049-051 as the route allows)
- Verify every final by FILE EXISTENCE (script 13 exits 0 on failures). After 51/51:
  full no-range aggregate rebuild of slides_final.json.

## Dispatch queue as slots free (in order)
1. 009 (fresh root; unblocks child 010)        2. 012 (fresh root; unblocks child 013)
3. 010 (child of 009, import build/components/)  4. 013 (child of 012 — inherit 12's table PATTERN, redraw at 013's measured position/numbers)
5. 017 (child of 013)                           6. 018 (child of 017)
7. 007, 014, 015, 036, 039, 040 (fresh roots; briefs banked; prior workers stopped mid-flight — check their banks first)
8. 003, 005, 006, 016, 025, 030, 048, 028 (fresh roots; prior workers stopped)
9. 004, 008, 024, 021 (were LIVE pre-stop; workers died — check banks: 004r/024r mid-fix-cycle, 008 mid-flight, 021r replaced an unverifiable pass)
10. Slides awaiting finals: 019, 031, 034, 037, 041-047, 049-051 — generate brief + dispatch when final lands
11. Research 025/026/027 SOURCES.md (dirs exist, empty; 51/51 close-out requirement) — one worker when a slot frees

## Certified (7/51): 001, 002, 020, 022, 029, 035, 038
## Research records banked: 48/51 (missing 025/026/027)

## Standing laws (do not re-litigate)
- VIDEO= prefix on EVERY 15_progress.py call (stray write hit the CLOSED ml-intro DB 21:05 — only updated_at cells, zero semantic corruption, documented in qa/slide001/worker_report.md)
- Zoomed judge BOTH legs on every slide (Template A + Procedure B crops, matched effective scale)
- No top stroke on this deck's chrome (C00000 strokes: LEFT x58.5, RIGHT x901, BOTTOM y538.5 only)
- Badge numeral = file number; badge (876,73) d35 FDFD96 ring 6A5ACD
- Single plain-named slide_NNN_recreated.pptx; never edit a certified component in place
- Equations: mathtext → 600dpi PNG → addImage px/600 + eq_*.json sidecars; OMML wrap is an orchestrator post-certification pass
- Final: byte-verbatim OPC deck merge + 0/51 pixel gate + md5 + CLOSEOUT_REPORT.md (must include 51/51 research completeness) + memory update
