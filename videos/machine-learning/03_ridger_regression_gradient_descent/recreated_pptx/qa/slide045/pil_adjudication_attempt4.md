# Slide 045 — leg A attempt 4 PIL adjudication (2026-10-25, worker s7-judge-1024)

Transcript: judge_attempt_4.txt — FINAL VERDICT: FAIL (1 BLOCKER + 2 MAJOR).
All three findings measured against unique_slides/slide_045.jpg vs render_3.png (current pptx 37c9b1cf…, render_3.png 8ae38d76…, chrome PASS).

## 1. BLOCKER "missing x1..x6 label row in Augmented Vectors panel" — REFUTED

Ink-cluster scan of the label band y160..180 (frame px), x55..340:

- ORIG  clusters: x96..101, 118..123, 140..145, 162..172, 185..191, 208..213 (6 labels, pitch ~22)
- RENDER clusters: x92..106, 115..123, 138..151, 160..174, 183..196, 206..219 (6 labels, pitch ~23; wider clusters only from anti-aliasing at 2.08x)

Six subscript x-labels present in the render at the original's pitch. The BLOCKER's
premise ("labels clearly absent in IMG1") is false.

## 2. MAJOR "round parentheses vs straight bars on all column vectors" — REFUTED

Carried over from attempts 1–3; already pixel-refuted: the ORIGINAL prints straight
vertical bars at x330/x353, x379/x403, x729/x753 (measured in prior adjudication,
measurements_adjudicate_r2.txt). The render's bars match the original. Judge's
IMG2 paren claim is a misread.

## 3. MAJOR "six separate bordered boxes vs one merged panel" — REFUTED

Vertical-border scan of the six-row band y340..460:

- ORIG borders: x57..59 (chrome), 63..65 (panel left), 243..246 (panel right), 274, chrome
- RENDER borders: x58.5..59, 63.3..63.8, 245.2..246.1, 379.5/403.5 (right region)

Both sides: ONE panel spanning x63..246 with no per-row divider columns. Horizontal
structure also matches (both have a mid divider: orig hline y413 run=177, render y415 run=183).

## Conclusion

Attempt 4's FAIL rests entirely on refuted findings. No build edit is warranted;
re-judging would re-roll the same dice. Leg A evidence = judge_attempt_4.txt + this record.
