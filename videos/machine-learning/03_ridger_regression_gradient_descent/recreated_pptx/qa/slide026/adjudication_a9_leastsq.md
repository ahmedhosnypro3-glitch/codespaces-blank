# Adjudication — "Least Squares" bold MINOR (crop_8_notes_judge.txt) — CONFIRMED → attempt-9 fix

Finding (attempt-8 Template B notes leg, MINOR, confidence 0.85): "the original's leading
phrase 'Least Squares' of the first bullet is rendered BOLD (heavier strokes than the adjacent
regular 'Linear regression…'); in the recreation it is regular weight — the bold on those two
words was dropped." Evidence: `probe_leastsq.out` … `probe_leastsq8.out`, `probe_a9_verify.out`,
controlled two-weight render `scratch/tmp/lo_boldtest/test_ls_026.js` → `ls-1.png`
(three lines of the SAME N1 string through the SAME pipeline: L1 regular, L2 bold-LS,
L3 regular control), plus the N2 line as the in-image bold/regular ruler.

## Why a direct density comparison is not enough (and how it was made valid)

Cross-image ink-density comparison is biased: the ORIGINAL is a 72dpi video frame and
render_8/9 is a 150dpi raster of the same slide geometry, so thin strokes soften in the frame
and its measured density runs 0.69–0.79× the render's. The bias cancels only if BOTH images
carry the phrase at the same weight. Therefore the adjudication uses three independent,
bias-cancelling discriminators.

### 1. SAME-LETTER stem mass, within the ORIGINAL (no cross-image confound)

Cap-height zone of the N1 line (y342..354), the 'L' stem:

| image | 'L' in "Least" | 'L' in "Linear" |
|---|---|---|
| ORIGINAL | x111..113 = 3 solid cols × 11/13 rows = **33 ink px** | x231..232 = 2 cols × 11/13 rows = 22 ink px = **1.50×** |
| render_8 (LS regular) | x110.4..111.4, 78 ink px | identical class (1.44 both, no elevation) |
| render_9 (LS bold, attempt 9) | x110.4..112.3, 130 ink px | bold took effect |

Ruler: inside render_8, the same-letter regular-vs-BOLD pair ('Least' L vs the bold
'Learning' L in N4) measures 78 vs 129 ink px = 1.65×. The original's 1.50× Least/Linear
elevation sits inside the bold range and outside the regular range (1.00).

### 2. Phrase-window density with composition-controlled windows

Windows are each image's own phrase extents (Least→Squares→Linear word spaces located by a
≥5-frame-px blank scan on the x-height band), so both images compare the same letter sequences.

| thr | ORIG LS / ORIG REG | render_9 LS / REG | render_9 BOLD class / REG | ORIG BOLD class ("is a convex function") / REG |
|---|---|---|---|---|
| 430 | 1.458 | 1.293 | 1.187 | 1.376 |
| 550 | 1.260 | 1.270 | 1.177 | 1.232 |
| 650 | 1.197 | 1.260 | 1.174 | 1.198 |

Before the fix (render_8, regular LS): LS/REG = 1.01 / 1.02 / 1.03 / 1.06 — flat, the regular
class. Controlled sims: regular LS/REG = 1.04, bold LS/REG = 1.32. After attempt 9 the
render's LS ratio (1.27–1.29) tracks the ORIGINAL's LS ratio (1.20–1.46) at every threshold,
and the residual relationship between the images now mirrors the known-bold span exactly
(1.458/1.293 = 1.13 for LS vs 1.376/1.187 = 1.16 for "is a convex function").

### 3. Cross-image anchor (class-relative bias)

At thr 430 the ORIGINAL's regular-class spans sit at 0.69–0.79 of the render's density, but
its LS span sat at 0.99 of render_8's regular LS — an upward outlier of exactly bold
magnitude. After attempt 9: ORIG_LS / REN9_LS = 0.75, and ORIG_BOLD("is a convex function") /
REN9_BOLD = 0.78 — the LS span now matches the BOLD class anchor (before: it was 0.99 against
a regular-class anchor of 0.69).

## Against the finding

* Spec's emphasis list for bullet 1 names only "is a convex function" and "ONE Minimum" —
  not authority: the same brief normalised the frame's typo "approximatly" to "approximately"
  (attempt-8 CONFIRMED defect) and over-read bold on "variable number of steps" (banked
  refutation, attempt-5/6 lineage). Fidelity target is the frame.
* Word-advance positions were already matched by the attempt-4 charSpacing closure, so the
  extents cannot discriminate weight — the discriminators above were needed instead.

## VERDICT: CONFIRMED → attempt 9

`build/slide_026.js` N1 line 1: `"Least Squares "` is now `bold: true`, with per-run
charSpacing re-calibrated closed-loop (bold advances ~+6px over the line; 0.10pt on the plain
runs left the line at +3.9, so the plain runs sit at 0.06pt). Measured on render_9:
N1 x 90.7..769.1 vs original 91.0..769.0 (d +0.1, inside the ±2.0 band); every other text band,
bar, bullet disc and the containment check are unchanged from attempt 8 (all pre-adjudicated
items identical). Pixel diff render_8 → render_9: 20,190 px, bbox frame x 109.9..769.1
y 341.6..357.9 = the N1 line only — the alg crop and all other regional evidence stays valid.
House chrome on render_9: PASS (`house_chrome_9.txt`).
