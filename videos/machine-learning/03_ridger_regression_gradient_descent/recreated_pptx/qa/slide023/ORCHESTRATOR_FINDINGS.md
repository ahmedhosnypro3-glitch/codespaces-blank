# Orchestrator findings — slide 023 (harvested 2026-10-24 00:28)

From judge_attempt_3.txt (FINAL VERDICT: FAIL). PIL-first adjudication required for
every item BEFORE any build change (960x540 frame, 1px=1pt; measure BOTH images).

1. MAJOR (high conf): body text colour — original renders ALL body text in a dark
   maroon/red family (complexity paragraph, "For Example" line, "Solution:" block);
   recreation uses dark navy for the complexity paragraph and black for the rest.
   ACTION: measure the original's body-text ink hue in 2-3 clean bands; if maroon is
   confirmed, restyle body runs to the measured hue. Do not accept at face value
   without measurement — but do not refute without measurement either.
2. MINOR: "lambda I" green highlight dropped inside the formula — original colors the
   regularization term green; recreation renders it black.
3. MINOR: W and Y styling — original BOLDS W and Y in the formula; recreation
   UNDERLINES them (underline substituted for bold).
4. MINOR: "(X^T X)" underline dropped in the caption "if Feature vectors are of
   dimension d => ..." — original HAS the underline; recreation does not. This is the
   open item from the earlier session: CONFIRMED as a real defect, add it.
5. MINOR: key numerals "1000" and "1,000,000,000" not bolded (original bolds them).
6. MINOR: "Matrix inversion" not bolded (original bolds Least Squares / Matrix
   inversion / Gradient Descent in the Solution block).
7. MINOR (low-med): complexity box fill — original's blue-bordered box appears
   unfilled/white; recreation applies a light lavender fill.

No visual-quality defects (no clipping/overflow/collisions/wrapping errors).
Fix items 1-7, rebuild, render, re-judge BOTH legs.
