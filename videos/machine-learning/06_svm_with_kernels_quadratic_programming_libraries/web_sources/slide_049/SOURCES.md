# Source verification — slide 049

## Claims checked

- No readable text, so no verifiable DATA claim: doc-parse
  (`analysis/parse_out_049/slide_049.parse.md`) returns only the chart's data table and
  `analysis/slide_049_raw.json` records the chart title and both axis titles as unreadable
  at capture resolution — no title, legend, formula, dataset or library name,
  hyperparameter, theorem attribution or sign convention exists to check — NEEDS_NO_SOURCE
- Figure genre — a red outer ring enclosing two inner clusters (blue left-center, black
  right-center) with sparse red outliers is the canonical non-linearly-separable
  illustration motivating the SVM kernel trick (no straight hyperplane divides the groups;
  a kernel lifts them so one can) — CONFIRMED, genre only — DataCamp, "Kernel Trick"
  https://www.datacamp.com/tutorial/kernel-trick
- Axis-label convention — "Feature 1" / "Feature 2" is the standard x/y label pair for 2-D
  kernel-trick teaching plots — CONFIRMED, convention only — DataCamp, "Kernel Trick"
  https://www.datacamp.com/tutorial/kernel-trick; scikit-learn `make_circles` examples plot
  exactly `xlabel("Feature 1")` / `ylabel("Feature 2")`
- sklearn `make_circles` must NOT be substituted for this figure — it generates exactly TWO
  classes (0 = outer circle, 1 = inner circle) while slide 049 shows a two-class inner pair
  PLUS an outer ring and outliers — CONFIRMED, do not use — scikit-learn `make_circles`
  https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_circles.html
- Axis tick ranges (x 0-40, y 0-35) and point positions (blue ~x 8-16 / y 10-22, black
  ~x 24-32 / y 14-22, red outliers densest top-right, per
  `qa/slides_045_055/judge_049.txt`) — UNVERIFIABLE — no source: lecture-internal plotting
  window and synthetic geometry; no authoritative value exists, nothing to reconcile
- Build strings in `recreated_pptx/build/slide_049.js` (title "SVM Kernel Visualization —
  Four-Cluster Structure", four legend entries, axis titles) — UNVERIFIABLE, builder-added
  chrome — no source: the original shows none of these and the banked judge records them as
  additions; they must never be transcribed into `verbatim_text`

## Overall

- VERDICT: NEEDS_NO_SOURCE
- 2 agy web searches spent (figure genre, axis-label convention); no slide value was
  corrected and none could be — the frame prints no number, formula, name or attribution.
- Tolerance notes: no sign convention, symbol, formula or named concept is at stake, so
  nothing may be tightened or edited from a source. Reproduce only the measured tick ranges
  (x 0-40, y 0-35) and the cluster geometry the banked judge PASSes (red ring `FF0000`,
  blue `0000FF`, black `000000`, red outliers `FF0000`). Do NOT import `make_circles` — it
  is a two-class figure, not this four-group one. Keep the original's absent title, legend
  and axis titles; "Feature 1"/"Feature 2" is acceptable only as optional house chrome.
  Doc-parse's 28-row x/y table is a partial raster sample, not the full point set:
  regenerate the clusters from measured geometry per the advanced-graph rule.
