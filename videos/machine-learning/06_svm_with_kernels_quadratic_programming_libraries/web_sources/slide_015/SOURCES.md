# Source verification — slide 015

## Claims checked
- "Non-Linearly Separable Data": the classes on the single feature `x` (red centre group, cyan outer
  groups) cannot be separated by a linear decision boundary — CONFIRMED — LibreTexts, "Non-Linearly
  Separable Data and the Kernel Trick", https://biz.libretexts.org/Courses/Aurora_University/Data_Analytics_with_Applications_in_Business/10%3A_Support_Vector_Machines/10.05%3A_Non-Linearly_Separable_Data_and_the_Kernel_Trick
  The centre cluster surrounded by an outer ring is the canonical non-separable case: no straight line
  separates it, and in 1-D that means no single threshold x = c; a linear boundary is too rigid.
- Setup "Each Sample is represented by one features \"x\"" (single feature) — CONFIRMED — MIT 6.036
  notes, "Feature representation", https://openlearninglibrary.mit.edu/assets/courseware/v1/b5ca509c17bab346cc6252ca41a1aac7/asset-v1:MITx+6.036+1T2019+type@asset+block/notes_chapter_Feature_representation.pdf
  With one feature a cut placed anywhere either takes an outer group together with the centre or
  excludes one side — exactly the configuration the slide draws.
- Association "Non-Linear Decision Boundary" → orange parabola, "Linear Decision Boundary" → blue
  straight line — CONFIRMED (concept) — the MIT 6.036 notes cited above, plus Columbia ORFE SVM slides,
  http://www.columbia.edu/~mh2078/MachineLearningORFE/SVMs_MasterSlides.pdf
  The curved boundary is the non-linear one, the straight line the linear one. The parabola is the
  pre-image of a straight cut in the lifted space φ(x) = (x, x²): x² − c = 0 gives roots ±√c, i.e. two
  boundary points on the 1-D axis — the shape the slide draws.
- Lecture context only (no such text on the slide): φ(x) = (x, x²) feature lifting and the polynomial
  kernel K(x,z) = (xᵀz + c)^d as the general mechanism — CONFIRMED as context — the two sources above
  The slide prints no φ, no kernel formula, and makes no claim about which class is positive/negative;
  sources add mechanism context only, no content is licensed into the rebuild.

## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild (no transcript edits licensed):
  - Keep the label-to-curve association exactly as drawn in the original: Non-Linear → orange parabola,
    Linear → blue straight line. qa/rejudge2/slide_015_judge.txt records the original's association
    that way, and recreated_pptx/build/slide_015.js encodes it correctly. One earlier spec sentence in
    analysis/slide_015_raw.json lists the two arrows the other way round — do not follow it.
  - Point counts and geometry are the slide's own data (~3 cyan left, 6 red centre, 3 cyan right, 11
    total per qa/rejudge2/slide_015_judge.txt); no source governs them — copy them from the original.
  - In this 1-D view the "linear" boundary is a single straight cut and the parabola opens upward,
    symmetric about the centre; do not render it as broken/disconnected straight segments.
  - verbatim_text stays exactly as printed, including the grammatical "one features \"x\"".
