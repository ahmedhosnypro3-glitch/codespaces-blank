# S23 paren sweep — slide 021 (2026-10-26, s23-paren-worker)

## Census (certified render_11.png)
- y630 band: `(` x185 (−4.35) / `)` x406 (+4.35) — the main equation's paren
  pair. Correct.
- y960 band: `(` x322 (−4.34) / `)` x543 (+4.58). Correct.

## Asset/cross evidence
eq_021_xtx.png pixel-scanned in the S22 sweep: left paren belly LEFT (true
"("), right paren mirrored (true ")") — the S22 auto-pair FLAG was resolved
FALSE POSITIVE (tall strokes were sub/superscript digit strokes). Mathtext
glyphs correct by construction.

## Vision leg
- crop_ps_main_eq pair: dispatched via 16_vision_gate (Template B payload
  byte-identical, NNN=021) — transcript `crop_ps_main_eq_judge.txt`.
- Leg verdict: **FAIL** — but ZERO delimiter/direction findings: the leg
  explicitly verified the main-equation paren pair "spans all terms, no
  collision — Match" on both sides, plus every glyph, color and the trailing
  cropped "λ =". The single MAJOR is an OUT-OF-CLASS notation claim: missing
  matrix underbars under both X glyphs.

## X-underbar adjudication (PIL, crop ascii 416x114)
- CONFIRMED as a factual claim: the original carries two baseline underbars
  (crop y78: x40-66 under X #1, x98-130 under X #2); the render has none.
- Build provenance: the certified composer's equation segment is mathtext
  "X^T X" (build/assets/eq_021_invexpr.json, composer att5 2026-10-24) with
  no \underline — the omission originates in the certified equation source.
- History: the att3 judge had raised related underline claims on the BOX
  headers (MAJOR header-mislabel + MINOR underline color); the certified
  att12 transcript records Box 1 header "X^TX (red)" and PASSED without an
  underline requirement on the main equation.
- Disposition: NOT the paren-curve-direction defect class → no rebuild from
  this sweep; escalated to the orchestrator via pool task-add (they decide
  fix-lane vs wontfix). Certification not reopened by S23.

## Verdict
NO mirrored/wrong-direction delimiter. Direction class CLEAN. Out-of-class
confirmed notation omission (X underbars) escalated; no rebuild.
