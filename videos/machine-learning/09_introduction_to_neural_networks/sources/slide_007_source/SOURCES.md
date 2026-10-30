# Source Research: slide_007

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_007_source/docparse_run/`
- Full frame parse: `full/slide_007.parse.md`
- Composed: `composed/slide_007_composed.md`
- Crop cascade: ran but outputs not individually saved
- Chat lane: DEGRADED (model `docparsechat` not available on gateway) — deterministic fallback used

## Extracted Content (from vision analysis)

### Slide Title / Section Header
**Multi-Class Classification using [ONE VS ALL] Binary Classifiers**

### Slide Number
7

### Diagram Content

**One-vs-All 2D Classification Plot:**
- Three linear decision boundaries:
  - d₁(x): red line, descending (upper-left to lower-right)
  - d₂(x): green line, ascending (lower-left to upper-right)
  - d₃(x): blue line, ascending steeper (lower-left to upper-right)
- Three class regions with diagonal hatching:
  - C₁ (top): light green hatching, green dots
  - C₂ (right): light blue/purple hatching, blue dots
  - C₃ (bottom-left): light red/pink hatching, red dots
- Class labels: C₁, C₂, C₃ in yellow boxes
- "+ ve" annotations with colored arrows on positive side of each boundary

---

## Research Summary

This slide (slide 7) illustrates the **One-vs-All (One-vs-Rest) strategy** for multi-class classification using binary classifiers in 2D:

1. **Three binary classifiers**: Each classifier dₖ(x) separates class k from all other classes
2. **Decision boundaries**: Linear separators in 2D space
3. **Region assignment**: Each point belongs to the class whose positive half-space contains it
4. **Visualization**: 2D plot showing decision boundaries and class regions with hatching
5. **Positive side indicators**: "+ ve" markers showing which side of each boundary is "positive" for that class

This is a **graph slide** requiring generated visualization via graphgen/ (using matplotlib to recreate the 2D classification plot with three linear decision boundaries, shaded regions, class labels, and data points).

### Uncertain Items (marked [?])
- Exact positions of decision boundaries (slopes, intercepts)
- Exact data point distributions
- Whether the hatching patterns are diagonal lines or another pattern

---
*Generated: 2026-10-27*

## Wave-2 verification (2026-10-28)

Evidence basis: reanalysis_v2 for 007 was still empty at read time; fell back to `analysis/slide_007_final.json` + doc-parse cascade `sources/docparse_cascades/slide_007/composed/` (composed parse verbatim: title "Multi-Class Classification using [ONE VS ALL] Binary Classifiers", page number 7, chart entries "C1 / +ve", "Q(x) / +ve", "C2 / +ve", "C3 / +ve", picture text "+ ve C1 + ve C2 + ve C3"). 3 web searches (agy, Google). Claim-by-claim verification — frame text unchanged.

### Verified claims

1. **Title concept: multi-class classification via ONE-VS-ALL binary classifiers** — CONFIRMED. OvA (a.k.a. One-vs-Rest, OvR) is the canonical strategy that decomposes a C-class problem into C binary classifiers, each separating one class from all others combined.
2. **One binary linear classifier per class, each with its own decision boundary d_k(x)** — CONFIRMED. With linear binary classifiers in 2D, each produces a straight line w_k·x + b_k = 0 separating class k from the rest.
3. **Class regions on the +ve side: "+ve" marks showing which side of each boundary is positive for that class** — CONFIRMED. The positive half-space R_k = {x : w_k^T x + b_k > 0} is the class's side; "+ve" annotations on the slide mark exactly those half-spaces.
4. **Class regions C1/C2/C3 with a sample point Q(x) annotated +ve** — CONFIRMED (notation). Q(x) is a query point being tested against each OvA classifier; "+ve" indicates its discriminant is positive for the marked classes — consistent with the multi-discriminant region definition R_k = {x : y_k(x) > y_j(x) for all j≠k} and the argmax_k d_k(x) assignment rule.
5. **Diagonal hatching / shaded regions per class in a 2D feature space** — CONFIRMED as presentation detail: OvA partitions 2D space into convex polygonal per-class regions; the slide's hatched bands visualize those regions. Hatching style itself is a drawing choice (visual, non-data).

### Uncertain items (kept, non-data)
- Exact slopes/intercepts of the three lines and exact scatter positions — closed-loop rendering matters (graphgen), not DATA.

### Data-only corrections
None.

### Citations (Wave-2)
1. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — OvA strategy, per-class binary classifiers, argmax scoring
2. https://www.dremio.com/wiki/one-vs-all-classification/ — OvA/OvR definition
3. https://kenndanielso.github.io/mlrefined/blog_posts/10_Linear_multiclass_classification/10_1_One_versus_all.html — linear One-vs-All geometry, 2D decision lines, ambiguity regions (also cited for 008)
4. https://www.cs.rice.edu/~as143/COMP642_Spring22/Scribes/Lect5 — multiclass lecture scribe (OvA setup)
5. https://medium.com/aimonks/one-versus-all-ovr-the-multi-class-classification-workhorse-21b3d0a76373 — OvR multiclass workhorse
6. https://introml.mit.edu/notes/classification.html — linear classifier, positive/negative half-spaces
7. https://web.stanford.edu/class/stats202/notes/Classification/LDA.html — discriminant regions and pairwise linear boundaries

## Wave-3 verification (2026-10-30)

Evidence basis: fresh vision re-analysis `analysis/reanalysis_v2/slide_007_reanalysis.txt` (11,488 B, present at read time) + doc-parse cascade `sources/docparse_cascades/slide_007/composed/` + 2 web searches. Tooling note: `agy -p` CLI quota-exhausted this wave (HTTP 429, reset ~154 h); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend). All cited URLs re-fetched 2026-10-30; HTTP status noted per URL.

### Claim-by-claim verification (DATA only)

1. **Title "Multi-Class Classification using [ONE VS ALL] Binary Classifiers"** — CONFIRMED. OvA (a.k.a. OvR) decomposes a K-class problem into K binary classifiers, class k positive versus all remaining classes combined (Microsoft Learn, Machine Learning Mastery, UofT CSC411).
2. **Three linear boundaries d1(x), d2(x), d3(x), each a straight line in 2D with its own "+ve" half-space marked** — CONFIRMED. Each is the boundary w_k^T x + b_k = 0 of a binary linear classifier; the "+ve" annotation identifies that class's positive half-space.
3. **Class regions C1/C2/C3 drawn on the +ve side of each boundary, hatched** — CONFIRMED as the hard-threshold OvA picture.
4. **Geometry nuance (DATA-relevant, and the substance of the 007→008 pair)**: under the joint argmax rule the per-class regions are provably convex and tile the whole plane with no gaps — UofT CSC411: "The decision regions of such a discriminant are always singly connected and convex"; Hacettepe l10 gives the same construction. Independent OvA hard thresholds, however, can leave (a) regions positive for MORE THAN ONE classifier and (b) regions positive for NONE — mlrefined §10.1.4 shows both verbatim ("regions where points are on the positive side of more than one classifier ... the three triangular white regions" and "the one in the very middle of the plot whose points are on the negative side of all three classifiers"). Slide 007's drawing (regions that do not cleanly tile the plane) matches this independent hard-threshold geometry; slide 008 annotates those overlap/gap zones with "?". Slide 007 itself therefore already contains the setup for slide 008's ambiguity findings.
5. **Q(x) annotation — DATA DISCREPANCY [?]:** the doc-parse cascade records a chart entry "Q(x) | +ve", but the fresh vision re-analysis of `slide_007.jpg` lists 12 text blocks and NO Q(x) (only C1/C2/C3, d1/d2/d3, three "+ve", and the badge "7"). Q(x) is not confirmed by the fresh frame read — it is downgraded from Wave-2's "CONFIRMED" to [?]. Inspect the original frame at build time before rendering a Q(x) label; do not invent it.
6. **Point clusters (green ~7, red ~5, blue ~8) and hatching are illustrative synthetic data** — CONFIRMED as a non-dataset schematic: the axes are unlabeled and unticked, with no numeric range printed.

### Data-only corrections
- No change to the frame text. The Wave-2 "Q(x) CONFIRMED" item is downgraded to [?] because the fresh vision read does not surface that label.

### Uncertain items (non-data, carried)
- Exact slopes/intercepts of the three lines and exact point positions — rendering detail for graphgen, not DATA.

### Citations (Wave-3; re-fetched 2026-10-30)
1. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — HTTP 200; OvA strategy, per-class binary classifiers, argmax scoring.
2. https://machinelearningmastery.com/one-vs-rest-and-one-vs-one-for-multi-class-classification/ — HTTP 200; OvR definition and argmax combination.
3. https://www.cs.toronto.edu/~urtasun/courses/CSC411/07_multiclass.pdf — HTTP 200; "1 vs all ... PROBLEM: More than one good answer!" and K-class regions convex/singly connected.
4. https://kenndanielso.github.io/mlrefined/blog_posts/10_Linear_multiclass_classification/10_1_One_versus_all.html — HTTP 200; text confirms both the multi-positive overlap regions and the all-negative unassigned region.
5. https://web.cs.hacettepe.edu.tr/~erkut/ain311.f22/slides/l10-linear-discriminant-functions-perceptron.pdf — HTTP 200; linear discriminant functions, hyperplane geometry.
6. https://introml.mit.edu/notes/classification.html — HTTP 200; linear classifier positive/negative half-spaces.
7. https://web.stanford.edu/class/stats202/notes/Classification/LDA.html — HTTP 200; discriminant regions and linear boundaries (also cited in Wave-2).
