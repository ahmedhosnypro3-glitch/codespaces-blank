# Sources — slide_040

## Web-verified sources

1. **Shape/benchmark clustering datasets used in the slide.** The six filenames shown
   (Aggregation.txt, Compound.txt, Spiral.txt, Pathbased.txt, Flame.txt, Jain.txt) are
   the canonical synthetic shape-based clustering benchmark sets widely used to evaluate
   clustering algorithms on non-linear structures, varying densities and arbitrary
   geometric shapes — settings where centroid-based methods (K-means) fail.
   - ResearchGate figure "Synthetic data sets: (a) Aggregation (b) S2 (c) Flame (d) Spiral
     (e) Figure2b (f) Jain (g) D6 (h) ..." — https://www.researchgate.net/figure/326629609
   - "Data Clustering: User's Dilemma" (ICTACT Journal on Soft Computing) —
     https://www.ictactjournals.in/paper/IJSC_Vol_17_Iss_2_Paper_2_4228_4238.pdf
   - "Clustering aggregation" (Gionis, Mannila, 2005) — https://www.cs.helsinki.fi/... (see
     https://www.researchgate.net/publication/220345083_Clustering_aggregation and
     https://cs-people.bu.edu/evimaria/cs565/aggregated-journal.pdf)

2. **Standard file naming.** Aggregation, Compound, Flame, Jain, Pathbased and Spiral are
   the classic shape sets distributed as `.txt` point files in clustering benchmark suites
   (origin paper: Jain & Law, "Data clustering: A user's dilemma", 2005, used for density
   vs. distance comparisons).

## Application to this slide

The slide asks the learner to classify each background point in the six datasets — i.e.
label which cluster each point belongs to, in preparation for discussing why linear
classifiers fail and kernels/QP are needed. The visual elements (7 colored clusters in
Aggregation, ring + inner clusters in Pathbased, spiral arms, etc.) match the published
benchmark plots. Build uses matched colors and cluster layouts per the vision analysis;
exact point coordinates are approximations derived from the frame (marked `[?]` in the
validated spec where unreadable).

## Trust & economy

- Two independent sources corroborate the dataset set and its pedagogical use.
- No slide-specific citation appears in the original frame beyond the filenames; the
  lecture context (SVM with kernels) is the teacher's framing, not a cited source.
