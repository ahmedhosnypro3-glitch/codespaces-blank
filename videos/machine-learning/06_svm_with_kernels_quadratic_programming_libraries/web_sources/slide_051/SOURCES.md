# Source verification — slide 051
## Claims checked
- Axis ranges: x from -10 to 50, y from -10 to 40 (tick labels only, no axis titles on the slide)
  — NEEDS_NO_SOURCE — measured from `unique_slides/slide_051.jpg` (white plot panel spans
    x 220-780, y 66-480 px; tick labels resolve to the stated ranges in both the vision
    analysis and the rejudge transcript). This is a slide-internal value, not an external fact.
- Two scatter classes: blue cluster upper-left (x 2-30, y 12-28), red cluster lower-right
  (x 18-42, y 2-17), overlapping across the middle
  — NEEDS_NO_SOURCE — measured from the frame; synthetic point positions carry no external
    authority. No dataset is named anywhere on the slide, and two searches for a matching
    canonical teaching dataset (two overlapping classes, blue upper-left / red lower-right)
    returned no matching figure — the data is lecture-internal.
- Light-blue shaded region over the upper-left half (decision region for the blue class)
  — CONFIRMED (convention) — scikit-learn `plot_svm_kernels` example, which shades predicted
    decision regions and overlays the class scatter,
    https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html
    Cosmetic only: the original uses a light-blue dither/hatch pattern on the left half and a
    light-red one on the right half (the rejudge transcript records "dotted background
    patterns; recreation uses solid light blue shaded region"), so the rebuild may use a solid
    low-alpha fill; no data correction is implied.
- Doc-parse series: 21 points, x = 0,2,...,40 (step 2), y = 15,18,22,23,20,27,23,27,22,21,19,16,
  19,15,16,5,6,7,10,12,16 — the first 15 points fall in the blue cluster's y-band, the last 6 in
  the red cluster's — NEEDS_NO_SOURCE — it is a partial read of slide-internal scatter data
    (`analysis/parse_out_051/slide_051.parse.md`); treat it as an indicative subset, not ground truth.
- Slide carries no title, no equations, no formulas, no library names, no dataset citations, no
  theorem attributions, and no axis titles — NEEDS_NO_SOURCE — the only text on the frame is the
    badge numeral "51" and the numeric tick labels, so there is nothing an external source could
    confirm or correct (spec-correction protocol: sources correct DATA, and no DATA here is
    attributed to anything outside the lecture).
## Overall
- VERDICT: NEEDS_NO_SOURCE
- Tolerance notes for the rebuild: the two colour-to-class assignments and the light-blue /
  light-red decision-region shading are standard SVM plotting conventions and may be rendered
  as solid low-alpha fills; the point cloud is synthetic and lecture-internal, so reproduce the
  frame's measured cluster extents (blue x 2-30 / y 12-28, red x 18-42 / y 2-17) rather than
  fitting any published dataset. Keep the original's absent title and absent axis titles — the
  rebuild's added title "SVM Classes with Decision Region Shading" and "Feature 1"/"Feature 2"
  labels are chrome additions, not slide content; they are acceptable only as house chrome, never
  as transcribed slide text. No number, formula, sign convention, hyperparameter name or
  attribution on this slide is wrong or corrected by any source.
