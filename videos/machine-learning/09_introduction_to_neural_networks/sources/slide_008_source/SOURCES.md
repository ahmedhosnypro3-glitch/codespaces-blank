# Source Research: slide_008

## Doc-Parse Transcript (nemotron-3.5-parse)

**Run**: `sources/slide_008_source/docparse_run/`
- Full frame parse: `full/slide_008.parse.md`
- Composed: `composed/slide_008_composed.md`
- Crop cascade: ran but outputs not individually saved
- Chat lane: DEGRADED (model `docparsechat` not available on gateway) — deterministic fallback used

## Extracted Content (from vision analysis)

### Slide Title / Section Header
**Multi-Class Classification using [ONE VS ALL] Binary Classifiers**

### Slide Number
8

### Diagram Content

**One-vs-All 2D Classification Plot with Ambiguity Regions:**
- Axes: x and y axes with arrowheads (no axis labels)
- Three classes of points:
  - C1: green dots (upper region)
  - C2: blue dots (right region)
  - C3: red dots (lower-left region)
- Three linear decision boundaries:
  - d1(x): red line, upper-left to lower-right
  - Blue line: lower-left to upper-right (steeper)
  - d3(x): green line, lower-left to upper-right (shallower)
- Yellow label boxes: C1, C2, C3 near respective clusters
- Four orange boxes with black "?" marking ambiguity/undefined regions
- "+ve" text with colored arrows near boundaries
- Hatched shading between decision lines
- External annotation boxes:
  - "Undefined" (light blue box, top-left) with leader lines into plot
  - "New Class" (purple box, middle-right)

---

## Research Summary

This slide (slide 8) continues the One-vs-All visualization and highlights **ambiguity regions** where multiple classifiers disagree or where no classifier is confident:

1. **Ambiguity regions ("?" boxes)**: Four locations where the one-vs-all strategy produces uncertain classifications
2. **"Undefined" region**: Area where no classifier's positive half-space applies (or multiple apply)
3. **"New Class" concept**: Introduces the idea of regions not covered by existing classifiers
4. **Decision boundaries**: Same three lines as slide 7 but with more annotations

This is a **graph slide** requiring generated visualization via graphgen/ (matplotlib 2D plot with decision boundaries, class points, ambiguity markers, and annotation boxes).

### Uncertain Items (marked [?])
- Exact positions of "?" markers
- Exact geometry of hatched regions
- Whether "New Class" is a new classifier or a meta-concept

---
*Generated: 2026-10-27*

## Wave-2 verification (2026-10-28)

Evidence basis: reanalysis_v2 for 008 was still empty at read time; fell back to `analysis/slide_008_final.json` + doc-parse cascade `sources/docparse_cascades/slide_008/composed/` (composed parse verbatim: title "Multi-Class Classification using [ONE VS ALL] Binary Classifiers", page number 8, chart entries "C1 / + ve", "Q[x] / ?", "C2 / + ve", "C3 / + ve", picture text "+ ve C1 ? ? C2 + ve ? New Class ? ? ? ? New Class" and "+ve C1 ? ? New Class C3"). 3 web searches (agy, Google). Claim-by-claim verification — frame text unchanged.

### Verified claims

1. **Same OvA setup as slide 007 (three linear boundaries, +ve annotations)** — CONFIRMED. The slide carries over the One-vs-All visualization from slide 007 with identical structure.
2. **Q(x) point annotated "?" — ambiguous/undefined classification** — CONFIRMED (concept). In OvA, independently trained binary boundaries can overlap or diverge; the point Q(x) falls where the classifiers disagree or none is confidently positive, so its class is undefined under strict hard-threshold rules.
3. **Multiple "?" boxes marking ambiguous/undefined regions** — CONFIRMED (concept). Two documented OvA failure modes: (a) ambiguous overlap regions where MORE THAN ONE classifier returns positive; (b) unassigned/"dead-zone" regions where NO classifier returns positive — both leave a point's class undefined.
4. **"New Class" annotation** — CONFIRMED (concept). A region covered by none of the trained classifiers' positive half-spaces cannot be assigned to any trained class — in lecture context it motivates the idea that such a region represents a class not present in training (the term appears in literature as "new class region"/dead-zone handling). Whether the lecture intends it as a literal extra class or a motivation for an open-set/new-class mechanism is a teaching nuance — marked [?] as a concept-level uncertainty, not a DATA change.
5. **"Undefined" external annotation with leader lines (per existing Wave-1 entry)** — CONFIRMED (concept): OvA undefined regions are a standard, documented limitation of the strategy.

### Data-only corrections
None. All annotations on the frame correspond to documented OvA behavior.

### Uncertain items (kept, non-data)
- Exact positions of the "?" markers and "New Class" boxes — rendering detail for graphgen, not DATA.
- "New Class" as literal class vs. open-set motivation — concept-level [?] noted above.

### Citations (Wave-2)
1. https://kenndanielso.github.io/mlrefined/blog_posts/10_Linear_multiclass_classification/10_1_One_versus_all.html — linear OvA geometry incl. ambiguous overlap and unassigned/undefined regions
2. https://medium.com/aimonks/one-versus-all-ovr-the-multi-class-classification-workhorse-21b3d0a76373 — OvR multiclass incl. ambiguity discussion
3. https://www.quora.com/What-are-the-issues-with-one-vs-all-classification-approach — OvA issues (multiple/none positive → undefined class)
4. https://medium.com/data-science/multi-class-classification-one-vs-all-one-vs-one-94daed32a87b — OvA vs OvO multiclass comparison
5. https://data-intelligence.hashnode.dev/the-perceptron-algorithm-some-limitations — perceptron limitations (perceptron convergence only if linearly separable)
6. https://medium.com/@ManueleCaddeo/understanding-multilayer-perceptrons-and-the-limitations-of-single-layer-neural-networks-4c559a59ecd9 — single-layer limitations motivating deeper nets
7. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — OvA component reference

## Wave-3 verification (2026-10-30)

Evidence basis: fresh vision re-analysis `analysis/reanalysis_v2/slide_008_reanalysis.txt` (13,028 B, present at read time) + doc-parse cascade `sources/docparse_cascades/slide_008/composed/` + 3 web searches. Tooling note: `agy -p` CLI quota-exhausted this wave (HTTP 429, reset ~154 h); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend). All cited URLs re-fetched 2026-10-30; HTTP status and page titles noted per URL.

### Claim-by-claim verification (DATA only)

1. **Same OvA setup as slide 007: three boundaries d1(x) red / d2(x) blue / d3(x) green, each with a "+ve" tick, class tags C1/C2/C3 on yellow** — CONFIRMED (carried over from 007).
2. **The "?" boxes mark ambiguous / unassigned locations** — CONFIRMED, and now grounded in two documented OvA failure modes: (a) overlap — the positive side of more than one classifier at once; (b) gap / undefined — the negative side of every classifier. mlrefined §10.1.4 shows both verbatim; arXiv:2311.13355 ("Unified Classification and Rejection: A One-versus-All Framework") and UofT CSC411 ("1 vs all ... PROBLEM: More than one good answer!") corroborate that independent OvA classifiers produce exactly these regions.
3. **"Undefined" callout (blue box + leader lines, upper-left, outside the plot)** — CONFIRMED as the annotation of the no-positive / unassigned region (every classifier returns negative there).
4. **"New Class" callout (magenta box at the right edge)** — the frame places it in a region no trained classifier claims. In the literature this is precisely where unknown / out-of-distribution samples are expected to land: OvA "no-positive" gaps are natural OOD indicators, and open-set recognition (Bendale & Boult, "Towards Open Set Recognition") treats such points as "unknown" rather than forcing a known label; alternatively a reject option (Chow 1957; arXiv:1505.04137 "Consistent Algorithms for Multiclass Classification with a Reject Option"; NeurIPS "On the calibration of multiclass classification with rejection") withholds a prediction there. Whether the lecturer intends a literal extra class or this open-set / reject motivation remains a concept-level **[?]** (kept from Wave-2) — the frame text itself is verified.
5. **Doc-parse "Q[x] | ?" entry** — the fresh vision read shows a tiny unboxed magenta "?" near the plot centre but no "Q[x]" text; treat the Q[x] glyph as [?] (same flag as slide_007).

### Data-only corrections
- None to the frame text.

### Uncertain items (carried)
- Exact positions of the "?" markers and the "New Class" box — rendering detail for graphgen, not DATA.
- "New Class" as a literal extra class vs. an open-set/reject motivation — concept-level [?] above.
- Q[x] glyph presence — [?] (see item 5).

### Citations (Wave-3; re-fetched 2026-10-30)
1. https://kenndanielso.github.io/mlrefined/blog_posts/10_Linear_multiclass_classification/10_1_One_versus_all.html — HTTP 200; multi-positive overlap and all-negative unassigned regions, verbatim.
2. https://arxiv.org/abs/2311.13355 — HTTP 200; page title verified: "Unified Classification and Rejection: A One-versus-All Framework".
3. https://vast.uccs.edu/~tboult/PAPERS/towards_openset_recognition.pdf — HTTP 200; Bendale & Boult, Towards Open Set Recognition.
4. https://arxiv.org/html/1505.04137v1 — HTTP 200; page title verified: "Consistent Algorithms for Multiclass Classification with a Reject Option".
5. http://papers.neurips.cc/paper/8527-on-the-calibration-of-multiclass-classification-with-rejection.pdf — HTTP 200; multiclass classification with rejection.
6. https://www.cs.toronto.edu/~urtasun/courses/CSC411/07_multiclass.pdf — HTTP 200; OvA "more than one good answer" problem.
7. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — HTTP 200 (also cited in Wave-2).

## Verified 2026-10-30 (wave 4 — scope src_w4_005_008)

Evidence basis: `analysis/slide_008_final.json` + fresh vision read `analysis/reanalysis_v2/slide_008_reanalysis.txt` (13,028 B) + doc-parse cascade `sources/docparse_cascades/slide_008/composed/slide_008_composed.md` (independent second read) + 3 agy searches + 4 live URL fetches. Tooling note: the `agy -p` CLI is quota-exhausted this wave (re-tested 2026-10-30: HTTP 429 RESOURCE_EXHAUSTED, resets in ~131 h); searches ran through the agy MCP web-search tool — the same Antigravity/Google grounding backend the CLI drives. Every URL below was re-fetched live on 2026-10-30 with HTTP status recorded. Frame text unchanged — DATA-only.

### Verification questions asked (agy, this wave)
1. "one-vs-all classification dead zone region where no binary classifier returns positive undefined class ambiguity overlap regions in 2D feature space"
2. (re-fetch check) does the mlrefined OvA post still state, verbatim, the all-negative region and the overlap regions that the slide's "?" boxes annotate?
3. (re-fetch check) do the arXiv records for "Unified Classification and Rejection: A One-versus-All Framework" and "Consistent Algorithms for Multiclass Classification with a Reject Option" still state the OvA/OOD-rejection and reject-option framing?

### Claim-by-claim verification (DATA only)

1. **Same OvA setup as slide 007: three boundaries (d1 red / d2 green / d3 blue per the frame), each with a "+ve" tick, class tags C1/C2/C3** — CONFIRMED (carried from 007; mlrefined and Microsoft Learn as above). Doc-parse corroborates: chart table "C1 | + ve", "C2 | + ve", "C3 | + ve"; picture text "+ ve C1 ? ? C2 + ve ? New Class ? ? ? ? New Class". Note the frame's own boundary-label colours (red/green/blue) are course styling, not source data — the frame wins for pixels.
2. **The four "?" boxes mark ambiguous / unassigned locations** — CONFIRMED, verbatim, with the two failure modes named separately. mlrefined §1.4: "regions where points are on the positive side of more than one classifier - these are the three triangular white regions bordered by two decision boundaries"; §1.5: "the one in the very middle of the plot whose points are on the negative side of all three classifiers." So "?" covers both (a) overlap — positive for ≥2 classifiers, and (b) gap — positive for none.
3. **"Undefined" callout (box outside the plot, leader lines into the plot) = the no-positive / unassigned region** — CONFIRMED. mlrefined §1.5 verbatim above names exactly that region ("negative side of all three classifiers"); Oregon State's decision rule ("output positive if the dot product is positive and negative if otherwise") makes a point negative for all classifiers the same region. This is the all-negative case, which the frame's leader lines point into.
4. **"New Class" callout = a region no trained classifier claims** — CONFIRMED as a documented OvA property; the *interpretation* stays concept-level `[?]` (carried from Wave-2). Live re-fetch of arXiv:2311.13355 confirms the title and abstract: "Unified Classification and Rejection: A One-versus-All Framework" — "rejecting ambiguous and novel (also called as out-of-distribution (OOD)) inputs"; "By decomposing the K-class problem into K one-versus-all (OVA) binary classification tasks ... combining the scores of OVA classifiers can give (K+1)-class posterior probabilities, which enables classification and OOD rejection in a unified framework." Live re-fetch of arXiv:1505.04137 confirms "Consistent Algorithms for Multiclass Classification with a Reject Option" — "the one vs all hinge loss, albeit with a different predictor than the standard argmax". Both document the modern treatment of exactly the slide's region. Whether the lecturer means a literal extra class or the open-set/reject motivation is not decidable from a source — the frame text "New Class" is verified, the intent remains `[?]`.
5. **Doc-parse "Q[x] | ?" chart entry** — UNVERIFIED / `[?]` (unchanged from Wave-3). The fresh vision read shows a tiny unboxed magenta "?" near the plot centre but no "Q[x]" text. Same flag as slide 007. Do not render a Q[x] glyph without a frame check.
6. **Positions of the "?" markers and the "New Class" box; hatch pattern; dot counts; which end of each arrow carries the arrowhead** — UNVERIFIED: no source counterpart; rendering detail for graphgen, not DATA.

### Data-only corrections
None. No claim on this slide is contradicted by a source; no patch to `analysis/slide_008_final.json`.

### Uncertain items (carried)
- "New Class" as a literal extra class vs. an open-set / reject motivation — concept-level `[?]`.
- Q[x] glyph presence — `[?]`.
- "?" marker positions, hatching, dot counts — rendering detail.

### Citations (wave 4; re-fetched live 2026-10-30)
1. https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html — HTTP 200; full text extracted; verbatim quotes for the overlap regions and the all-negative region.
2. https://arxiv.org/abs/2311.13355 — HTTP 200; abstract fetched; "Unified Classification and Rejection: A One-versus-All Framework"; OvA decomposition + OOD rejection framing.
3. https://arxiv.org/abs/1505.04137 — HTTP 200; abstract fetched; "Consistent Algorithms for Multiclass Classification with a Reject Option"; one-vs-all hinge loss with a reject option.
4. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — HTTP 200; one binary model per class vs. its complement.
5. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html — HTTP 200; the positive/negative sign rule underlying the "no classifier positive" region.

## Wave-4 result register

See `sources/slide_008_source/VERIFY_W4.md` — 6 claims: 4 CONFIRMED, 0 CORRECTED, 2 UNVERIFIED (Q[x] glyph = `[?]`; marker positions = visual), 5 verified URLs, 0 fetch failures.
