# Source verification — slide 047

## Claims checked
- "Two interleaved spiral arms wound around a common centre, one class per arm, arcs
  spiralling inward" — CONFIRMED — this is the classic Two-Spirals benchmark picture:
  interlocking Archimedean-style spirals used to demonstrate non-linear separability and the
  need for kernels (Unideb GyBITT ch08s09 https://gyires.inf.unideb.hu/GyBITT/06/ch08s09.html;
  conx Two-Spirals https://conx.readthedocs.io/en/latest/Two-Spirals.html).
- "No straight-line/hyperplane boundary separates the two arms" — CONFIRMED — sources state
  no single straight line divides the intertwined arms; linear classifiers score ~50% on it
  (Unideb GyBITT ch08s09, same URL; LMU PCML SVM exercise
  https://emtiyaz.github.io/pcml15/ex7-svm.pdf).
- Canonical construction: angle theta = (i/16)*pi with radius decreasing ~linearly in i, and
  the second class is the first rotated by pi (per-class sign multiplier spiral_num = +/-1) —
  CONFIRMED — that rotation is exactly what makes the two arms interlock (conx Two-Spirals
  https://conx.readthedocs.io/en/latest/Two-Spirals.html). The canonical form is Archimedean
  (r linear in theta); logarithmic-spiral variants exist but are not the canonical benchmark.
- Slide title text "SVM Kernel Visualization — Spiral Decision Regions" — UNVERIFIABLE by
  sourcing — a lecturer-chosen heading with no external authority; settle visually against
  unique_slides/slide_047.jpg (both banked judge transcripts read it off the original frame).
- Axis tick labels 0..35 (x) and -10..40 (y) — UNVERIFIABLE — no authoritative axis window
  exists for this figure; these are the lecturer's plotting choice and must be measured off
  the original frame, not sourced.

## Overall
- VERDICT: CONFIRMED
- Searches spent: 2 of 6 (stopped early — both factual claims confirmed at the first hit).
- Tolerance notes for the rebuild:
  - Generate the figure as a real two-spirals dataset (advanced-graph rule): theta = (i/16)*pi,
    r decreasing ~linearly in i, class 2 = sign-flipped copy; scale/translate so points fill the
    measured window (x 0-35, y -10..40). Do not hand-draw arcs.
  - Curve count and colors are frame measurements, not sourced facts: the certified judge
    reading of the original is three thin continuous nested curves (black/red/blue) on pastel
    decision regions split at x ~ 17.5 — take colors/splits from the frame's own pixels.
  - The frame carries no formula, no kernel symbol, no library name and no numeric datum other
    than the badge numeral (47) and the axis ticks; there is nothing else a source could
    correct. Do not treat doc-parse's `chart type="area"` table (x 0,5,...,35 / values
    0,21,26,27,31,28,24,35) as on-slide data — it is a transcription artifact; sources never
    license adding text or values the slide does not show.
