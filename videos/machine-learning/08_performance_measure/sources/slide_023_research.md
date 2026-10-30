# Sources — Slide 23 — Effect of Selecting Threshold Value on Model Performance

Consumed spec: analysis/slide_023_raw.json (RAW ONLY — no slide_023_final.json exists). Frame: unique_slides/slide_023.jpg.
Method: NO new query spent — cross-references the banked records in slide_021_research.md (economy law).

- "Threshold=0.4" callout with the two closely spaced dashed lines at x≈0.40/0.41: CONFIRMED (semantics) — the threshold is a cut-off on the model's score; one threshold ⇒ one confusion matrix (Wikipedia ROC article, fetched live, banked on slide 21) https://en.wikipedia.org/wiki/Receiver_operating_characteristic.
- Flowchart annotation "(Any value → (0:+1))": CONFIRMED — squashing maps any real value into (0, 1); reading here is consistent with the corrected label noted on slide_021_research.md (no new fetch spent).
- Matrix cells (4, 1, 1, 5) at threshold 0.4: UNVERIFIED as a source fact (course-authored example data, no counterpart) but SELF-CONSISTENT — 4+1+1+5 = 11 = the same 11 samples as slides 21-26, forcing actual P = TP+FN = 5 and actual N = FP+TN = 6, matching the fixed sample set; because the two off-diagonal cells are equal (1 and 1), the FP/FN orientation issue flagged on slides 21/22/25/26 is immaterial here — no correction needed for this frame.
- Precision/recall position of this threshold inside the series: CONFIRMED — Evidently AI (fetched live, banked on slide 21) https://www.evidentlyai.com/classification-metrics/classification-threshold — 0.4 sits between 0.3 and 0.5 in one fixed experiment, so precision/recall follow the confirmed trade-off direction.
- Strip plot: axis ticks 0.0 / 0.5 / 1.0, 11 airplanes, 6 red-dot and 5 blue-dot planes at listed x-positions: UNVERIFIED — course-authored rendering with no source figure counterpart; dot colour encodes true class in the course's own convention (consistent with actual P = 5 / actual N = 6 from the matrix), so keep it exactly as the frame shows and never recolour toward a source.
