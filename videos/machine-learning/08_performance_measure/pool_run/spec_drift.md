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

### Slide 037 — `verbatim_text.labels`

- **Reanalysis (original frame)**: the Curve)
- **Action**: re-dispatch this slide's build worker to add the missing content, then re-run both judge reads.

## Not compared

- Slide 004: SKIP — verbatim_text.* no consumed final spec
- Slide 014: SKIP — verbatim_text.* no consumed final spec
- Slide 016: SKIP — verbatim_text.* no consumed final spec
- Slide 035: SKIP — verbatim_text.* no consumed final spec

