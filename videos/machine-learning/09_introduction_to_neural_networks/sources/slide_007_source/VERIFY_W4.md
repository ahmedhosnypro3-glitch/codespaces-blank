# VERIFY_W4.md — slide 007 "Multi-Class Classification using [ONE VS ALL] Binary Classifiers"

Wave 4 web-source audit · scope `src_w4_005_008` · worker `w4-src-005` · date 2026-10-30
Spec audited: `analysis/slide_007_final.json` · banked record: `sources/slide_007_source/SOURCES.md`
Independent second read: `sources/docparse_cascades/slide_007/composed/slide_007_composed.md` + `analysis/reanalysis_v2/slide_007_reanalysis.txt` (11,488 B)
Tooling: `agy -p` CLI quota-exhausted (HTTP 429 RESOURCE_EXHAUSTED, resets ~131 h — re-tested this wave); searches ran through the agy MCP web-search tool (same Antigravity/Google grounding backend; `agy_check_setup` reports no blockers). Every URL marked CONFIRMED was re-fetched live on 2026-10-30.

## Claim register

| # | Claim (from the spec) | Status | Evidence URL | Change to the analysis spec |
|---|---|---|---|---|
| 1 | Title/concept: multi-class classification via [ONE VS ALL] binary classifiers — one binary classifier per class, class k vs. all the rest | CONFIRMED | https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 | none. Verbatim: "a binary model is created for each of the multiple output classes… against its complement (all other classes in the model)" |
| 2 | Each classifier's boundary d_k(x) = 0 is a straight line in 2D | CONFIRMED | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. The c-th classifier is written w₀⁽ᶜ⁾ + xᵀw⁽ᶜ⁾ = 0 — a hyperplane, hence a line in 2D |
| 3 | "+ve" marks each boundary's positive half-space, containing that class's points | CONFIRMED | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. Verbatim §1.3: "the class to be distinguished from the rest lies on the positive side of its respective classifier… w₀⁽ᶜ⁾ + x_pᵀw⁽ᶜ⁾ > 0 if y_p = c and < 0 if y_p ≠ c" |
| 4 | Independent hard-threshold OvA leaves overlap regions (positive for >1 classifier) and an all-negative central region — the geometry this slide draws and slide 008 annotates | CONFIRMED | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. Verbatim §1.4: "regions where points are on the positive side of more than one classifier - these are the three triangular white regions"; §1.5: "the one in the very middle of the plot whose points are on the negative side of all three classifiers" |
| 5 | The joint rule argmax_k d_k(x) tiles the plane with per-class regions | CONFIRMED | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. Verbatim: "y = argmax_{j=1..C} w₀⁽ʲ⁾ + xᵀw⁽ʲ⁾ … applies to the entire space of our problem" |
| 6 | The dot clusters are illustrative synthetic data (unlabeled, un-ticked axes, no numeric ranges) | CONFIRMED (as schematic, non-dataset) | https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html | none. The frame prints no axis numbers or dataset name; the source page's own C = 3 dataset is a different, illustrative set — do not import its points |
| 7 | "Q(x)" label | UNVERIFIED — `[?]` (carried from wave 3) | — | none. Doc-parse chart table lists "Q(x) | +ve"; the fresh vision read (12 text blocks: C1/C2/C3, d₁/d₂/d₃, three "+ve", badge 7) and no source surface it. Do not render Q(x) without a frame check |
| 8 | Exact slopes/intercepts of the three lines; exact point positions | UNVERIFIED (rendering detail, not DATA) | — | none |

Corroborating reads (no web spend): doc-parse composed parse gives the exact title text, badge 7, chart table "C1 | +ve / Q(x) | +ve / C2 | +ve / C3 | +ve", and picture text "+ ve C1 + ve C2 + ve + ve".

## Questions asked (agy, this wave)
1. one-vs-all dead zone (no classifier positive) and ambiguity/overlap regions in 2D feature space
2. re-fetch check of the mlrefined OvA post for the verbatim overlap / all-negative region text and the argmax fusion rule
3. re-fetch check of the Microsoft Learn One-vs-All component description

## Verification summary
- Claims checked: 8
- CONFIRMED: 6 · CORRECTED: 0 · UNVERIFIED: 2 (Q(x) glyph = `[?]`; line geometry = visual)
- Verified URLs (live-fetched 2026-10-30): 4
  1. https://rezaborhani.github.io/mlr/blog_posts/Linear_Supervised_Learning/Part_5_One_versus_all.html — HTTP 200, full text extracted
  2. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/one-vs-all-multiclass?view=azureml-api-2 — HTTP 200, text extracted
  3. https://cseweb.ucsd.edu/~dasgupta/151/multiclass-handout.pdf — HTTP 200, pdftotext extracted
  4. https://en.wikipedia.org/wiki/Perceptrons_(book) — HTTP 200, text extracted
- Honest failures (not cited as verified): none this slide
- Spec patches applied: none (0 corrected claims; frame text unchanged)
