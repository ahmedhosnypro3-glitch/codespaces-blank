# Sources — Slide 35 — ROC Curve for Same Model -different thresholds (thresholds 0.0, 0.1, 0.3, 0.4, 0.6, 0.7, 1)

## Slide identity
NO consumed analysis spec exists: `analysis/slide_035_final.json` and `slide_035_raw.json` are absent (the namespace jumps 034 → 036 among finals). The only record of this frame is the doc-parse crop-cascade output `analysis/parse/full/slide_035.parse.md` (+ `.parse.json`) and `unique_slides/slide_035.jpg`. Every claim below therefore rests on the doc-parse text, not on a validated vision spec — flagged as `[unverified]` per the trust law.

## Claims from the doc-parse record
- One (FPR, TPR) point per threshold, labeled by its threshold value: CONFIRMED — sklearn `roc_curve` docs (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html) — the parallel `fpr`/`tpr`/`thresholds` arrays are exactly this structure; the parse shows a threshold-labeled point set and FPR/TPR axis labels ("TPR", "1.0 FPR").
- Threshold=1 gives TPR=0/(0+5)=0 and FPR=0/(0+6)=0, i.e. the (0, 0) plot corner: CONFIRMED — "From toy boxes to code: simple intro to ROC & AUC" (https://dev.to/akshay_shetty_686041/from-toy-boxes-to-code-a-simple-intro-to-roc-auc-omf) — at threshold 1.0 nothing is predicted positive, so TP = FP = 0 and both rates are 0; this closes the sweep that slide 29 opened at (1, 1).
- Threshold=0.7 reading TPR=3/(3+2)=0.6, FPR=0/(0+6)=0 with a "Best (FPR)" annotation: CONFIRMED — same sources as `sources/slide_034_research.md` (cross-referenced, no new query spent) — FPR = 0 is the best FPR value.
- Threshold=0.6 reading TPR=3/(3+1)=0.6: CORRECTED (same as slide 33) — 3/(3+1) = 0.75, not 0.6; course-authored slip, frame wins for recreation.
- Presence of thresholds 0.0/0.1/0.3/0.4/0.6/0.7/1 confusion panels plus the formula panel and the "ROC Curve for Same Model -different thresholds" title box: [unverified] — the doc-parse markdown shows these strings, but no validated vision spec exists to confirm layout, positions, or the exact panel-to-threshold placement. Resolve through a vision re-analysis of `unique_slides/slide_035.jpg` before any build.

## Course-authored elements (no source counterpart — do not "fix")
- Panel styling, the title box, the legend matrix, and the threshold annotation style are the course's own; the doc-parse truncates garbled prefixes ("P R=", "PFR=") that are OCR artifacts of the column-header row, not distinct content.

## Method
Tool: `mcp__agy-cli-mcp__agy_web_search` (2 queries total for this slide; both already spent for slides 29 and 34 and cross-referenced under the economy law — no new query was needed). Frame: `unique_slides/slide_035.jpg`; badge number 35.
