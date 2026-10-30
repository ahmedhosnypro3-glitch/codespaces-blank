# Source verification — slide 047

## Claims checked
- "Two interleaved spiral arms wound around a common center (red arm spiraling in from the
  top/upper right, blue arm from the left/upper left)" — CONFIRMED — Two Spirals dataset, the
  canonical non-linearly-separable benchmark used to motivate kernels in SVM teaching
  (Unideb GyBITT ch08s09 https://gyires.inf.unideb.hu/GyBITT/06/ch08s09.html;
  DataCamp Kernel Trick https://www.datacamp.com/tutorial/kernel-trick;
  LMU i2ML ch.17 Nonlinear SVMs https://slds-lmu.github.io/i2ml/chapters/17_nonlinear_svm/).
  All three describe exactly this picture: two classes whose arms interlock so deeply that no
  linear hyperplane separates them — the lecture's stated reason for introducing kernels.
- "Spiral arm curvature (how the arms wind inward)" — CONFIRMED — the canonical form is the
  Archimedean spiral r = b*theta, second class rotated by pi (equivalently (x,y) -> (-x,-y)):
  class 1 x = b*theta*cos(theta), y = b*theta*sin(theta); class 2 the same with a sign flip.
  Wikipedia, Archimedean spiral https://en.wikipedia.org/wiki/Archimedean_spiral. A
  logarithmic spiral is NOT the canonical form for this dataset.
- "Axis tick labels: -10 to 40 on the vertical axis, 0 to 35 on the horizontal" —
  UNVERIFIABLE — no authoritative axis window exists for the Two-Spirals dataset; these limits
  are the lecturer's own plotting choice, so the rebuild must measure the window off the
  original frame rather than source it.
## Overall
- VERDICT: CONFIRMED
- Searches spent: 2 of 6 (stopped early — both data claims confirmed; the third item is a
  measurement, not a fact a source could supply).
- Tolerance notes for the rebuild:
  - Regenerate the figure as a real Archimedean two-spirals dataset (advanced-graph rule):
    class 1 r = b*theta, class 2 the same arm rotated by pi; pick b and the theta range so the
    points fill the measured window (x 0-35, y -10 to 40); small dot markers, red and blue
    classes, equal aspect. Do not hand-draw arcs.
  - The frame carries no title text, no formula, no library name and no hyperparameter — only
    the badge numeral and axis tick numerals. Badge reads 47 (unique_slides/slide_047.jpg is
    named by the printed number, house badge rule); nothing else to transcribe verbatim.
  - Do NOT treat doc-parse's slide_047.parse.md `chart type="area"` table (x 0,5,...,35 /
    value 0,21,26,27,31,28,24,35) as on-slide data: it is a transcription artifact. The frame
    shows a two-spirals point scatter (the sibling parses 045/046/048 all type the same figure
    scatter/multi_line), and that x column merely walks the axis ticks. Sources never license
    adding text or values the slide does not show.
  - The dark hairline/arc elements in the frame are ambiguous (data series vs background
    texture) per the frame's own uncertainty list — measure them off the original, do not
    infer them from a source.
