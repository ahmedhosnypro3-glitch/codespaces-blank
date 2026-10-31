# Spec drift — reanalysis vs consumed spec

Reanalysis = fresh vision re-read of the ORIGINAL frame (`analysis/reanalysis/`). Consumed spec = `analysis/slide_NNN_final.json`, the spec the build worker actually used.

A MATERIAL delta is text or a table/chart data value present in the reanalysis but absent from the consumed spec — the build could not have rendered it. Per-slide build re-dispatch is the parent orchestrator's call; this lane only banks the finding.

## Material deltas

### Slide 001 — `verbatim_text.labels`

- **Reanalysis (original frame)**: جامعة العلوم والتكنولوجيا
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 002 — `verbatim_text.labels`

- **Reanalysis (original frame)**: (Any value) → (-1, +1)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 002 — `verbatim_text.equations`

- **Reanalysis (original frame)**: (Any value) → (-1, +1)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 009 — `verbatim_text.labels`

- **Reanalysis (original frame)**: Classified as +ve
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 009 — `verbatim_text.labels`

- **Reanalysis (original frame)**: Classified as +ve
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 009 — `visual_elements[table].data`

- **Reanalysis (original frame)**: 90
- **Consumed spec**: Symbolic 2x2 confusion matrix inside a blue rectangular frame. Red bold header 'Predicted as' centered above the two columns; column headers 'P' and 'N' in black; vertical red bold 'Actual' label rotated 90 degrees along the left edge; row headers 'P' and 'N' in black. Cells separated by thin red gr
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 011 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Recall = \frac{TP}{TP + FN}
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 011 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Recall= \frac{28}{28+2} = 93.3\%
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 012 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Recall = \frac{TP}{TP + FN}
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 013 — `verbatim_text.bullets`

- **Reanalysis (original frame)**: Average= 68.7%+60% =65.55%
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 013 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Precision = \frac{TP}{TP + FP}
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 013 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Recall = \frac{TP}{TP + FN}
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 013 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Average= 68.7%+60% =65.55%
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 015 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: -6
- **Consumed spec**: Square Cartesian grid with red border. x-axis ticks from -6 to 6; y-axis ticks from -3 to 3; origin unlabeled. Black axes with arrowheads and labels x and y. Red hyperbola y = 1/x drawn in quadrants I and III. Translucent yellow oval highlight around the steep branches near the y-axis. Caption 'y = 
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 015 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 6
- **Consumed spec**: Square Cartesian grid with red border. x-axis ticks from -6 to 6; y-axis ticks from -3 to 3; origin unlabeled. Black axes with arrowheads and labels x and y. Red hyperbola y = 1/x drawn in quadrants I and III. Translucent yellow oval highlight around the steep branches near the y-axis. Caption 'y = 
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 019 — `verbatim_text.labels`

- **Reanalysis (original frame)**: [Any value]  →   (-1 , +1)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 019 — `verbatim_text.labels`

- **Reanalysis (original frame)**: [Any value]  →   (-1 , +1)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 019 — `verbatim_text.equations`

- **Reanalysis (original frame)**: [Any value]  →   (-1 , +1)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 020 — `verbatim_text.labels`

- **Reanalysis (original frame)**: (Any value → (0, +1))
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 020 — `verbatim_text.labels`

- **Reanalysis (original frame)**: (Any value → (0, +1))
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 020 — `verbatim_text.equations`

- **Reanalysis (original frame)**: Any value → (0, +1)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 028 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP / (TP + FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 028 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP / (FP + TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 029 — `verbatim_text.labels`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 029 — `verbatim_text.labels`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 029 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 029 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 030 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 030 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 031 — `verbatim_text.labels`

- **Reanalysis (original frame)**: 1.0
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 031 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 031 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 031 — `visual_elements[chart].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: ROC-space plot. Vertical axis is labeled TPR with an upward arrow; horizontal axis is labeled FPR with a rightward arrow; both range from 0 to 1 with a light grid. A black diagonal arrow/line runs from lower-left toward upper-right. Three red-outlined circle markers are labeled '0.3' near the left s
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 032 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 032 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 032 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: ROC curve scatter/line plot. Y-axis 'TPR' ranges 0 to 1 with upward arrow. X-axis 'FPR' ranges 0 to 1 with rightward arrow. Background grid. Four red data points connected by red line: (0.33,1.0) labeled '0.3', (0.66,1.0) labeled '0.1', (1.0,1.0) labeled '0.0', (0.16,0.8) labeled '0.4'.
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 032 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: ROC curve scatter/line plot. Y-axis 'TPR' ranges 0 to 1 with upward arrow. X-axis 'FPR' ranges 0 to 1 with rightward arrow. Background grid. Four red data points connected by red line: (0.33,1.0) labeled '0.3', (0.66,1.0) labeled '0.1', (1.0,1.0) labeled '0.0', (0.16,0.8) labeled '0.4'.
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 032 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: ROC curve scatter/line plot. Y-axis 'TPR' ranges 0 to 1 with upward arrow. X-axis 'FPR' ranges 0 to 1 with rightward arrow. Background grid. Four red data points connected by red line: (0.33,1.0) labeled '0.3', (0.66,1.0) labeled '0.1', (1.0,1.0) labeled '0.0', (0.16,0.8) labeled '0.4'.
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 032 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: ROC curve scatter/line plot. Y-axis 'TPR' ranges 0 to 1 with upward arrow. X-axis 'FPR' ranges 0 to 1 with rightward arrow. Background grid. Four red data points connected by red line: (0.33,1.0) labeled '0.3', (0.66,1.0) labeled '0.1', (1.0,1.0) labeled '0.0', (0.16,0.8) labeled '0.4'.
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 033 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 033 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 033 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: Scatter plot with blue border. X-axis labeled 'FPR' ranging 0.0 to 1.0. Y-axis labeled 'TPR' ranging 0.0 to 1.0. Light gray grid lines. A blue diagonal reference line runs from (0,0) to (1,1). Five red circular data points are plotted and labeled with threshold values: '0.0' near (0.0, high TPR), '0
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 033 — `visual_elements[graph].data`

- **Reanalysis (original frame)**: 1.0
- **Consumed spec**: Scatter plot with blue border. X-axis labeled 'FPR' ranging 0.0 to 1.0. Y-axis labeled 'TPR' ranging 0.0 to 1.0. Light gray grid lines. A blue diagonal reference line runs from (0,0) to (1,1). Five red circular data points are plotted and labeled with threshold values: '0.0' near (0.0, high TPR), '0
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 034 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 034 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 036 — `verbatim_text.labels`

- **Reanalysis (original frame)**: 1.0
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 036 — `verbatim_text.equations`

- **Reanalysis (original frame)**: TPR = TP/(TP+FN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 036 — `verbatim_text.equations`

- **Reanalysis (original frame)**: FPR = FP/(FP+TN)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 036 — `visual_elements[chart].data`

- **Reanalysis (original frame)**: 0.8
- **Consumed spec**: ROC line chart (scatter-with-lines). X axis 'FPR' 0 to 1 (red label, bottom), Y axis 'TPR' 0 to 1 (red label, left). Light-blue gridlines on white. Single purple line with circular markers through points (FPR,TPR): (0,0) labeled '1.0'; (0,0.6) labeled '0.7'; (0.16,0.6) labeled '0.6'; (0.16,0.8) labe
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

### Slide 037 — `verbatim_text.labels`

- **Reanalysis (original frame)**: the Curve)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

## Not compared

- Slide 004: SKIP — verbatim_text.* no consumed final spec
- Slide 007: SKIP — verbatim_text.* no consumed final spec
- Slide 008: SKIP — verbatim_text.* no consumed final spec
- Slide 010: SKIP — verbatim_text.* no consumed final spec
- Slide 014: SKIP — verbatim_text.* no consumed final spec
- Slide 016: SKIP — verbatim_text.* no consumed final spec
- Slide 022: SKIP — verbatim_text.* no consumed final spec
- Slide 023: SKIP — verbatim_text.* no consumed final spec
- Slide 024: SKIP — verbatim_text.* no consumed final spec
- Slide 035: SKIP — verbatim_text.* no consumed final spec

