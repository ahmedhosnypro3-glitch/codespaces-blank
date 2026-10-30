# DISPLACED prior report — slide 012 (parked, not deleted)

The `web_sources/slide_012/SOURCES.md` present at the start of this run belonged to an
earlier `web_worker_012` invocation, which completed the scope at 2026-10-28 05:07:45
(status `done`, note in `mission.db`). This run's Write overwrote it before its content
could be copied aside; git does not track `web_sources/`, so the original bytes are
unrecoverable from disk. The DB note records its verdict verbatim and is reproduced
below so its findings stay banked evidence.

## Prior report — recorded verdict (verbatim from mission.db note)

> VERDICT: CORRECTED — 8 claims checked (7 confirmed, 2 corrected: q^T=[1,1,1,1] sign vs
> authoritative q=-1, and 'SVM Primal Problem' label on the alpha-formulation which is the
> DUAL); P matrix verified internally consistent (symmetric, PSD, rank 2, sign pattern
> matches y=[+1,+1,-1,-1]); 4 agy searches spent; sources: SJSU lec6svm.pdf, Berkeley
> EECS281B lec6, GaTech ECE6254, domino.ai

## Independent corroboration this run

Same verdict class (CORRECTED) reached independently, via 3 agy web searches plus exact
Fraction/numpy arithmetic:

- P symmetric and PSD (eigenvalues 0, 0, 0.9151, 154.0849; rank 2) — agrees with the
  prior report's "symmetric, PSD, rank 2".
- Sign pattern matches y = (+1,+1,−1,−1) — agrees with the prior report.
- q-vector sign — agrees with the prior report (here recorded as: under the slide's
  printed "+ qᵀα" form qᵀ must be [−1,−1,−1,−1]; canonical is −1ᵀα).
- New in this run: the ½-fold relationship between the two objective boxes verified
  numerically (lower box = 2× upper box; ½αᵀPα = 2833/2 at α=(1,2,3,4)).
- Not independently re-derived here: the '"Primal" label vs dual' correction — taken from
  the DB note above, since this run verified the formulation's algebra rather than the
  panel heading's wording.

## Current deliverable

`web_sources/slide_012/SOURCES.md` (25 lines, shape-compliant) — this run's independent
re-verification. It supersedes the displaced file as the deliverable.
