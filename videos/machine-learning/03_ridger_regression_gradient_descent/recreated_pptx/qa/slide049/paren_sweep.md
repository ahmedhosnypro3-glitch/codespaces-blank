# S23 paren sweep — slide 049 (2026-10-26, s23-paren-worker)

## Census (certified render_18.png — the att18-certified render)
- y150/180 bands: 10 aug/alt-vector pairs, all alternating ( ) with correct
  signs (LP −1.67…−1.78, RP +1.67…+1.89).
- y360 band: 7 wcol pairs, correct signs (−1.67…−1.78 / +1.70…+1.89).
- Initial-W pair (render x691/x734, y120-218): LP delta −1.2 "(" (correct
  sign), RP delta +0.87 (correct sign; thin strokes dilute the metric below
  the curved threshold — direction signs are unambiguous).

## History cross-check
- Event 245 (05:07) claimed "049 MIRRORED DELIMITERS CONFIRMED" on the OLD
  assets; superseded by event 259 (11:47): parens049 assets pixel-verified
  curved correct-belly (LP mid-centroid 10.1<15.2 left, RP 18.0>13.0 right);
  the certified 049 (att18, md5 1f456b09 restored after the orphan-drift
  incident) carries the CORRECT curved parens. The old broken assets are
  parked in qa/paren_sweep_20261026/broken_assets_049/ (not the deliverable).

## Vision leg
- crop_ps_wcol pair: dispatched via 16_vision_gate (Template B payload
  byte-identical, NNN=049) — transcript `crop_ps_wcol_judge.txt`.
- Leg verdict: **PASS**. All six vectors value-correct cell-by-cell; every
  paren spans its three rows, no touching, vertical centering correct. 3
  MINORs, all cosmetic: stroke weight (typed vs JPEG-softened ink, rule (e)),
  slightly flatter mid-section curvature with geometry explicitly correct,
  typed-vs-handwritten headers (rule (c)). No direction finding.

## Final verdict
NO mirrored delimiter in the certified deliverable. CLEAN — no rebuild.
PIL census + asset pixel-scan + vision leg all agree.
