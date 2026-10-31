# VERIFY_W4.md — slide 008 "Multi-Class Classification using [ONE VS ALL] Binary Classifiers"

Wave 4 web-source audit · scope `src_w4_005_008` · worker `w4-src-005` · date 2026-10-30
Spec audited: `analysis/slide_008_final.json` · banked record: `sources/slide_008_source/SOURCES.md`
Independent second read: `sources/docparse_cascades/slide_008/composed/slide_008_composed.md` + `analysis/reanalysis_v2/slide_008_reanalysis.txt` (13,028 B)
Tooling: `agy -p` CLI quota-exhausted (HTTP 429 RESOURCE_EXHAUSTED, resets ~131 h — re-tested this wave); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend; `agy_check_setup` reports no blockers). Every URL marked CONFIRMED was re-fetched live on 2026-10-30.

## Claim register

| # | Claim (from the spec) | Status | Evidence URL | Change to the analysis spec |
|---|---|---|---|---|
| 1 | Same OvA setup as slide 007: three boundaries, one "+ve" tick each, class tags C1/C2/C3 | CONFIRMED | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. Per-class linear classifiers, positive side = the class. Boundary label colours (red/green/blue) are course styling — the frame wins for pixels |
| 2 | The four "?" boxes mark ambiguous / unassigned regions | CONFIRMED | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. Two documented OvA failure modes, both verbatim on that page: "regions where points are on the positive side of more than one classifier" (overlap) and "the one in the very middle of the plot whose points are on the negative side of all three classifiers" (gap) |
| 3 | "Undefined" callout (box outside the plot, leader lines into the plot) = the region where no classifier is positive | CONFIRMED | https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html | none. Oregon State's sign rule ("output positive if the dot product is positive and negative if otherwise") makes a point negative for every classifier exactly this region, which mlrefined names verbatim |
| 4 | "New Class" callout = a region no trained classifier claims; the literature treats such points as unknown/OOD or withholds the prediction (reject option) | CONFIRMED as a documented OvA property — interpretation stays concept-level `[?]` | https://arxiv.org/abs/2311.13355 | none. arXiv:2311.13355 (live): "Unified Classification and Rejection: A One-versus-All Framework" — "rejecting ambiguous and novel (also called as out-of-distribution (OOD)) inputs"; "By decomposing the K-class problem into K one-versus-all (OVA) binary classification tasks… combining the scores of OVA classifiers can give (K+1)-class posterior probabilities". arXiv:1505.04137 (live): "Consistent Algorithms for Multiclass Classification with a Reject Option" — the OvA hinge loss "albeit with a different predictor than the standard argmax" |
| 5 | Doc-parse "Q[x] | ?" chart entry | UNVERIFIED — `[?]` (carried from wave 3) | — | none. The fresh vision read shows a tiny unboxed magenta "?" near the plot centre but no "Q[x]" text; same flag as slide 007. Do not render a Q[x] glyph without a frame check |
| 6 | Exact positions of the "?" markers and the "New Class" box; hatch pattern; dot counts; arrowhead ends | UNVERIFIED (rendering detail, not DATA) | — | none |

Corroborating reads (no web spend): doc-parse composed parse gives the exact title text, badge 8, chart table "C1 | + ve / Q[x] | ? / C2 | + ve / C3 | + ve", and picture text "+ ve C1 ? ? C2 + ve ? New Class ? ? ? ? New Class".

## Questions asked (agy, this wave)
1. one-vs-all dead zone (no classifier returns positive) and ambiguity/overlap regions in 2D feature space
2. re-fetch check of the mlrefined OvA post for the all-negative and overlap region text
3. re-fetch check of the two arXiv records (OvA + OOD rejection; multiclass with a reject option)

## Verification summary
- Claims checked: 6
- CONFIRMED: 4 · CORRECTED: 0 · UNVERIFIED: 2 (Q[x] glyph = `[?]`; marker positions = visual)
- Verified URLs (live-fetched 2026-10-30): 5
  1. https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html — HTTP 200, full text extracted
  2. https://arxiv.org/abs/2311.13355 — HTTP 200, abstract fetched (title verified)
  3. https://arxiv.org/abs/1505.04137 — HTTP 200, abstract fetched (title verified)
  4. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — HTTP 200, text extracted
  5. https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2025fall/unit2/perceptron.html — HTTP 200, text extracted
- Honest failures (not cited as verified): none this slide
- Spec patches applied: none (0 corrected claims; frame text unchanged)
- Concept-level `[?]` kept open: whether "New Class" means a literal extra class or the open-set/reject motivation — not decidable from a source; frame text "New Class" is itself verified.
