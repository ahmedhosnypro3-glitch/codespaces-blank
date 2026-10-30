# PARKED PRIOR ARTIFACT — do not treat as deliverable

This is the pre-existing `web_sources/slide_040/SOURCES.md` written by a prior
`web_worker_040` run (scope_web_040 was already `done` in mission.db with the note
"CONFIRMED — 9 claims checked, 5 searches spent"; it was never pending, so a fresh
scope-claim was a no-op). The file was untracked in git, so it is preserved here
verbatim per the run's park-before-overwrite convention (same pattern as
`pool-run-337934/orphans/slide_047_SOURCES_unclaimed_prior.md`).

The live deliverable is `web_sources/slide_040/SOURCES.md`, independently re-verified.

--- prior content follows ---

# Source verification — slide 040

## Claims checked
- Six dataset labels, verbatim: `Aggregation.txt`, `Compound.txt`, `Spiral.txt`,
  `Pathbased.txt`, `Flame.txt`, `Jain.txt` — CONFIRMED — SIPU / UEF clustering basic
  benchmark (P. Fränti et al.) distributes exactly these six synthetic sets under these
  names and as `.txt` files — https://cs.joensuu.fi/sipu/datasets/ and
  https://github.com/deric/clustering-benchmark (e.g. `artificial/pathbased.arff`,
  sibling `.txt` files)
- All six datasets are 2-dimensional, so each panel is a plain 2-D x-y scatter —
  CONFIRMED — D = 2 for all six — https://clustering-benchmarks.gagolewski.com/weave/suite-v1.html
- Aggregation panel: 7 point groups, mixed sizes/densities, adjacent clusters —
  CONFIRMED — ground truth is exactly 7 clusters (N = 788), adjacent/touching clusters with
  varying densities — https://clustering-benchmarks.gagolewski.com/weave/suite-v1.html
- Compound panel: blob clusters plus a hollow ring cluster — CONFIRMED — ground truth 6
  clusters (N = 399), a mix of Gaussian blobs and a non-convex ring-shaped cluster —
  https://clustering-benchmarks.gagolewski.com/weave/suite-v1.html
- Spiral panel: interleaved spirals — CONFIRMED — ground truth 3 interleaved spiral arms /
  3 clusters (N = 312, 104 points per arm) —
  https://www.researchgate.net/figure/Clustering-the-3-spiral-data-set-The-spiral-dataset-includes-312-points-partitioned-into_fig1_333657173
- Pathbased panel: an outer spiral/ring plus two inner clusters — CONFIRMED — ground
  truth 3 clusters (N = 300): one large sweeping horseshoe/curved outer path enclosing two
  inner compact groupings — https://cs.joensuu.fi/sipu/datasets/
- Flame panel: upper cluster plus a lower curving base — CONFIRMED — ground truth 2
  clusters (N = 240), two curved/interlocking shapes with upper-and-lower outlier points —
  https://www.mdpi.com/2227-7390/13/14/2272
- Jain panel: one cluster plus a C-shaped arc — CONFIRMED — ground truth 2 clusters
  (N = 373), crescent / horseshoe-shaped arcs —
  https://www.mdpi.com/2076-3412/12/7/1168 (Symmetry 12(7):1168)
- Title task "Check class of each background point in the following datasets" — CONFIRMED
  as the standard decision-surface visualization: build a dense meshgrid of background
  points over the 2-D plot area, classify every one, and shade the result (sklearn
  `DecisionBoundaryDisplay`) — https://scikit-learn.org/stable/modules/generated/sklearn.inspection.DecisionBoundaryDisplay.html
  and https://machinelearningmastery.com/plot-a-decision-surface-for-machine-learning/

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (no transcript edits licensed — the six `.txt`
  filenames, the badge numeral `40`, and the two-line title stay verbatim):
  - Every panel is 2-D; do not add axes, ticks, gridlines, or legends the slide omits.
  - Ground-truth cluster counts per panel are Aggregation 7, Compound 6, Spiral 3,
    Pathbased 3, Flame 2, Jain 2 — the brief's per-panel group descriptions match these,
    so keep them as the color/placement guide rather than inventing extra clusters.
  - Canonical point counts (788 / 399 / 312 / 300 / 240 / 373) back the brief's relative
    size words (small, large, tiny); keep those words rather than chasing exact N.
  - In these `.txt` files the ground-truth label is a third column after (x, y) — useful
    if the rebuild generates the plots programmatically; the slide itself shows no labels.
  - Exact scatter coordinates are not recoverable from the JSON (already flagged in
    validation.uncertain_items); approximate cluster geometry is acceptable.
