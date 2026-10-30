# Adjudication — Template A leg on render_7 (judge_attempt_3.txt)

Claim: w26-r3-20261021T0538, attempt 7 (rowC paren BLUE + red tail charSpacing 0.32).
Verdict: **PASS** — no BLOCKER/MAJOR. Two MINOR findings, both **PIL-REFUTED** below by
identical predicates run on BOTH images (frame px; original 1px/frame px, render at
SX=SY=2.0844). Evidence: probe_a7_findings.out, probe_a7_bars2.out.

## F1 (MINOR, low confidence) — "underline coverage in bullet 1 may extend slightly
differently over 'objective function' vs 'is a convex function'"
REFUTED — the difference does not exist. Neither image carries an underline in the N1
(bullet 1) band:
- ORIGINAL, y348..356 is the glyph band (ink 319/248/230/274/242/221/212/270/338 at
  thr 430); y357..360 holds only four 3-6px-wide, 3-row-tall fragments at x176..180,
  x299..308, x390..395, x690..694 — glyph bottoms/descenders (thr 700 shows the full
  y357 text row: those fragments are sparse). A real underline bar in this deck is a
  CONTINUOUS run 100-190 frame px wide (measured bars: rowB x349..716, rowD x287..473,
  N3 x177..277 and x538..728). No such run exists at any y in 357..361.
- RENDER_7, N1 band: glyphs y346..355, then y356:18 / y357:26 / y358:10 faint
  descender pixels and NO run at all from y359 down. No bar either.
- Conclusion: bullet 1 is un-underlined in the original AND in the recreation. The
  judge's "may extend slightly differently" compares two absences. No build change.

## F2 (MINOR, low confidence) — "possible subtle color tone difference in the
'moving step is a hyper parameter,' phrase (blue vs reddish)"
REFUTED — the phrase is BLUE in the original, measured, and in the same hue family as
the blue controls the same judge accepted. Core RGB (darkest 1/8 of the mask, identical
predicate, identical windows, both images):
- disputed rowC phrase x146..517 y208..228: ORIG **(28,18,139) b-r=+111** ; REN7 (0,0,255)
- ctrl rowB "moving along the direction of" x350..660: ORIG **(46,36,142) b-r=+97** ; REN7 (0,0,255)
- ctrl rowA "Start with initial" x146..290:         ORIG **(58,50,143) b-r=+85** ; REN7 (3,3,255)
- ctrl N2 black text:                               ORIG (52,54,51) ; REN7 (0,0,0)
Every original blue line lands at b-r +85..+111 (strongly blue; the ±25 spread is the
usual per-line JPEG/compression variance). The disputed phrase is the MOST saturated of
the three. The render draws every blue run 0000FF, the deck-wide blue already accepted
by Template A attempt 2 and by the crop judge on the surrounding lines. The "reddish"
reading has no pixel support. No build change.

## Additional non-findings recorded for completeness (not raised by the judge)
- Template A text mentions an underline on "(w.r.t. W)" in row C: measured, NEITHER image
  has a bar in the rowC band (ORIG y224..228 = n50/25/23/24/10 descender pixels, no run;
  REN7 y223..226 = n41/53/56/9, no run). RowC is un-underlined in both — the render
  agrees with the original; no discrepancy in either direction.
- N1 text sits ~1px higher in the render (glyph bottom y355 vs y356; descenders end 358
  vs 360) — the pre-adjudicated descender-metric class (selfcheck_attempt_7 N1 "adj").
- N3 underline bar: render y456 vs original y458 (2 frame px) — pre-adjudicated bar band
  (selfcheck_attempt_7 N3a/N3b inside the ±6.6 font-metric noise band). Not raised by
  the judge; recorded for the next worker.
