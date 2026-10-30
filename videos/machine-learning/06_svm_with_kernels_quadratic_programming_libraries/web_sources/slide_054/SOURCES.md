# Source verification — slide 054

## Claims checked

- Slide is a data-only frame: a two-class scatter with 16 clusters of 2x2 blue/red dots on a 4x4 lattice, axes 0..25 on x and y, badge "54"; no title, no axis labels, no legend, no decision boundary, no formula, no annotation anywhere in the parse — CONFIRMED — doc-parse record, `analysis/parse_out_054/slide_054.parse.md` (chart table + `class_Chart` only; the vision record at `analysis/slide_054_raw.json` §1 lists 8 elements, all chart furniture)
  Sources correct DATA only; nothing verbatim exists to correct, so per the spec-correction protocol the transcript is not edited from any source.

- Checkerboard arrangement of the two classes (alternating blue/red cluster cells across the plot) is the standard not-linearly-separable demonstration that motivates kernelized SVMs — CONFIRMED — banked sibling record, `web_sources/slide_055/SOURCES.md` (same deck, same 0-25 axes, same alternation) — no new query spent per the economy law — GeeksforGeeks, "Non-linear SVM" https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/

- A kernelized (RBF) SVM does not slice this lattice with straight lines; it wraps each discrete, well-separated cluster in a closed decision region ("islands"/"bubbles"), with `gamma` setting the radius of influence — high `gamma` = tight isolated pockets, low `gamma` = broad smooth regions; `C` controls how aggressively the closed boundary bends — CONFIRMED — 1 query spent — scikit-learn, "Plot SVM kernels" / "RBF SVM parameters" https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html and https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html

- Decoded point coordinates (doc-parse reads every dot into one series labelled "red": x 3..22, y 10..21) — UNVERIFIABLE — no external source
  In-lecture synthetic values read off the raster; not a named public dataset (not iris / wine / make_moons), so no authoritative form exists. Treat as approximations of dot positions, not canonical values.

- Build title "SVM Kernel Visualization — Lattice of Decision Regions" and axis labels "Feature 1" / "Feature 2" (`recreated_pptx/build/slide_054.js:4,6`) — UNVERIFIABLE — no external source
  The original frame carries no title and no axis labels. If the house rule requires a title box, keep it, but the wording is not slide content and must never be transcribed back into `verbatim_text`.

- Badge numeral `54` — no source needed — printed on the original frame; the badge rule makes it a curation number, not a data claim.

## Overall

- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: no sign conventions, symbols, formulas, hyperparameter names, library names or theorem attributions appear on the slide — only DATA-level facts are at stake.
  - Fidelity target: the 4x4 alternating two-class cluster lattice over 0..25 axes with **no** decision boundary and **no** legend drawn — the original deliberately shows neither; do not add a working separator to the points as printed.
  - Lattice spacing is 5 units on both axes (cluster centers at 3/8/13/18 and 5/10/15/20) — internal geometry, no source needed; the build's `latticeCenters` reproduce it exactly.
  - Color assignment: doc-parse collapsed every dot into a single series labelled "red", which contradicts the vision record's stable blue/red alternation — the raster read is unreliable on hue. Keep the recorded alternation (build uses `idx % 2`); which specific cells are blue vs red is a frame-read detail, not a data claim.
  - Decoded x/y values are approximate raster reads — regenerate topology via graphgen rather than transcribing the numbers.
  - Gray arrow cursor near (18..19, 19) is a capture artifact, correctly omitted per judge ground rule (c).

  - **Collision note (this run):** the mission DB scope `scope_web_054` was already `done` at 2026-10-28 05:07:07 (agent `web_worker_054`, verdict NEEDS_NO_SOURCE), so `scope-claim` and `scope-done` both returned 0 rows changed and the DB record was never touched by this run. A prior SOURCES.md in this directory (dir created 05:06:59) was overwritten in place at 05:15:50 without a backup; `web_sources/` is untracked in git, so the prior content is unrecoverable. This file supersedes it and restates the slide's verified status. Searches spent by this run: 1 (independent verification of the RBF closed-region behavior); the remaining cross-reference reuses the banked sibling record.
