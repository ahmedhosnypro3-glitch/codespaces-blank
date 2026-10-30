# S23 paren sweep — slide 047 (2026-10-26, s23-paren-worker)

## Census (certified render — render_regen.png, the S12b evidence-regeneration
render of the certified pptx; geometry re-verified per qa/slide047/README.txt)
- y150 band: 10 small pairs (LP −2.57…−2.59 / RP +2.48…+2.51). Correct.
- y360 band: 6 pairs (−2.6 / +2.49). Correct.
- y120/y300/y450/y570 bands: pairs (−2.54…−2.86 / +2.48…+2.77). Correct.
- 19 embedded paren instances across 5 unique assets — every instance
  measured correct-direction at its placed position (media-level checker 5/5
  PASS in the S22 sweep; placement swap risk closed by this render census).

## Vision leg
- crop_ps_topband pair: dispatched via 16_vision_gate (Template B payload
  byte-identical, NNN=047) — transcript `crop_ps_topband_judge.txt`.
- Leg verdict: **PASS** — zero discrepancies beyond ground-rule-excluded
  classes. All six header subscripts + twelve vector digits correct; every
  paren pair spans both rows without touching digits; vertical centering and
  stroke continuity verified. No direction finding.

## Verdict
NO mirrored delimiter. CLEAN — no rebuild. PIL census + vision leg agree.
