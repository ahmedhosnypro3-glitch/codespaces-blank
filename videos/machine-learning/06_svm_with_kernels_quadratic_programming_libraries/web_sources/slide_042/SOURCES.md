# Source verification — slide 042

## Claims checked
- The frame is a pure graphic: light-gray slide, thick red border, white square scatter plot, seven saturated-colour point clusters, one small black curved arrow, badge "42", black bottom strip — CONFIRMED (figure-level reading of the validated spec) — no equation, formula, library name, dataset name, hyperparameter, theorem attribution or sign convention appears anywhere on the slide, so no web-verifiable claim exists
- The plotted point coordinates and axis ranges (x ticks 0/10/20/30/40, y ticks -10/0/10/20/30/40) are the only numbers on the slide — UNVERIFIABLE by external source — the figure is synthetic in-slide lecture content with no published counterpart, so its numbers must be rebuilt verbatim from the frame, not sourced; the rebuild reference is `analysis/slide_042_final.json` (per-cluster regions and hex colors) plus `sources/slide_042/slide_042.parse.md`
- The doc-parse table is a 9-row subset — rows (5,4) (10,27) (12,28) (15,29) (20,23) (22,24) (30,20) (32,26) (35,22) — that does not enumerate every plotted point — UNVERIFIABLE from the parse alone — treat the validated vision regions in `analysis/slide_042_final.json` as authoritative for the rebuild; the parse's `bind: x ;  ; x` / `bind: y ;  ; y` are empty axis bindings (the slide prints no axis quantity or title)
- Generic context (2 searches, no slide-specific hit): a multi-cluster multi-colour scatter is the standard teaching illustration that such data is NOT linearly separable and requires a nonlinear kernel (RBF / polynomial) — CONFIRMED at concept level only — scikit-learn SVM kernels example https://scikit-learn.org/stable/auto_examples/svm/plot_svm_kernels.html and GeeksforGeeks "ML | Non-Linear SVM" https://www.geeksforgeeks.org/machine-learning/ml-non-linear-svm/

## Overall
- VERDICT: NEEDS_NO_SOURCE
- Tolerance notes for the rebuild:
  - Cluster centres (approx, from the validated spec): blue upper-left x≈10-14 y≈24-26; yellow mid-left x≈7-9 y≈12; green lower-left x≈7-9 y≈4-5; magenta lower-centre x≈12-26 y≈6-12; red upper-centre x≈20-25 y≈23-25; black right x≈32-37 y≈7-12; cyan upper-right x≈32-37 y≈22-28. Arrow: small black curved arrow between red and cyan near x≈26 y≈29, pointing down/right.
  - Add NO axis titles, legend, title, or any text the slide does not show; the only frame text is the tick numbers and "42".
  - Do NOT substitute a real dataset (e.g. sklearn `make_blobs(centers=7)`) for the frame's coordinates — no source endorses a dataset identity here; the on-slide points are the spec.
  - House frame rule overrides the analysis JSON's own look (red #FF0000 border, #D3D3D3 background): build the outer frame #C00000 1.5pt at x=0.15 y=0.15 w=13.03 h=7.2, background #E8E8E8, badge circle "42" at x=12.48 y=0.30 w=0.5 h=0.5 fill #FFF9C4, title box y=0.28.
  - `verbatim_text` stays verbatim: "-10", "0", "10", "20", "30", "40" (both axes) and "42".
