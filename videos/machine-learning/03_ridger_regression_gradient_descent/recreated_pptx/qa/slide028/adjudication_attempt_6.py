# Adjudication of judge_attempt_3 (full-slide FAIL on render_5) +
# crop_4_right_curve_judge (FAIL on render_4) — slide 028.
#
# Every finding is measured against the original frame (960x540, 1px = 1pt).
# Method notes:
#  * curve  : per-column median blue y, trimmed least squares (the dot staircases
#             straddle the curve), then RMSE/max over retained inliers.
#  * markers: connected-component centroids of the original's blue ink inside
#             per-marker windows; a marker is a blob ~11..21px wide AND tall
#             (the curve stroke is 2..5px, the stair connectors are thin).
#  * colour : strict masks on the original vs the render's declared 2E75B6.
import numpy as np
from PIL import Image
from collections import deque

QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/'
ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'

o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
orr, ogg, obb = o[:, :, 0], o[:, :, 1], o[:, :, 2]
blue = (obb - orr > 35) & (obb - ogg > 12) & (orr < 225)
of = np.zeros_like(blue)
of[125:134, :] = True; of[504:513, :] = True
of[:, 85:95] = True; of[:, 854:864] = True
blue &= ~of

print("### A. RIGHT-PANEL MARKER COUNT (judge_attempt_3 finding 1, MAJOR)")
print("Original markers, measured as fat connected components:")
for nm, (x0, y0, x1, y1) in {
    'M1': (540, 265, 585, 332), 'M2': (570, 360, 610, 412),
    'M3': (660, 332, 705, 388), 'M4': (690, 268, 730, 322)}.items():
    sub = blue[y0:y1, x0:x1]
    H, W = sub.shape
    seen = np.zeros_like(sub, bool)
    best = None
    for y, x in zip(*np.where(sub)):
        if seen[y, x]:
            continue
        seen[y, x] = True; q = deque([(y, x)]); pts = []
        while q:
            cy, cx = q.popleft(); pts.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx))
        a = np.array(pts)
        w = a[:, 1].max() - a[:, 1].min() + 1
        h = a[:, 0].max() - a[:, 0].min() + 1
        if 9 <= w and 9 <= h and (best is None or len(pts) > best[0]):
            best = (len(pts), a[:, 1].mean() + x0, a[:, 0].mean() + y0, w, h)
    if best:
        n, cx, cy, w, h = best
        print("  %s: (%.1f, %.1f)  %dx%d  px=%d" % (nm, cx, cy, w, h, n))
print("  => the original's right panel has FOUR large markers.")
print("  render_5's build declares FIVE: [536,300],[563,313],[647,345],[590,394],[706,322]")
print("  => CONFIRMED: one extra marker (the first, at x536) is a build defect.")

print()
print("### B. LEFT-PANEL MARKER COUNT (judge_attempt_3 finding 3, MINOR ~0.5)")
print("Original left-panel fat blobs (window x150..400):")
sub = blue[100:500, 150:400]
H, W = sub.shape
seen = np.zeros_like(sub, bool)
fats = []
for y, x in zip(*np.where(sub)):
    if seen[y, x]:
        continue
    seen[y, x] = True; q = deque([(y, x)]); pts = []
    while q:
        cy, cx = q.popleft(); pts.append((cy, cx))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
    a = np.array(pts)
    w = a[:, 1].max() - a[:, 1].min() + 1
    h = a[:, 0].max() - a[:, 0].min() + 1
    if 9 <= w <= 30 and 9 <= h <= 30:
        fats.append((a[:, 1].mean() + 150, a[:, 0].mean() + 100, w, h, len(pts)))
for cx, cy, w, h, n in sorted(fats):
    print("   (%.1f, %.1f)  %dx%d  px=%d" % (cx, cy, w, h, n))
print("  render_5 declares SEVEN left dots (4px): [293,250],[283,280],[274,308],")
print("       [265,336],[253,372],[264,412],[277,419] — d4 vs the original's ~8-14px.")

print()
print("### C. CURVE GEOMETRY (crop_4 finding 2, MAJOR) — MEASURED IN ATTEMPT 5")
print("  Trimmed-LS quartic vs the original's blue stroke:")
print("    LEFT : RMSE 2.01px  max 4.47px  (old quadratic: RMSE 14.64px  max 45.34px)")
print("    RIGHT: RMSE 2.84px  max 9.72px  (old quadratic: RMSE 15.35px  max 46.87px)")
print("  => CONFIRMED and CLOSED by the quartic fit now in build/slide_028.js.")
print("     See fit_attempt_5.out.txt / verify_fit_attempt_5.out.txt /")
print("     adjudication_attempt_5_r5.out.txt.")

print()
print("### D. MARKER POSITIONS (crop_4 finding 1, MAJOR)")
print("  The crop judge's normalised coords match NEITHER image exactly (its IMG2")
print("  coords disagree with the measured original too), so its per-marker numbers")
print("  are its own measurement artefact. The structural claim — that the marker")
print("  pattern is unfaithful — is CONFIRMED by section A: 5 markers vs 4, and the")
print("  step connectors therefore encode a different path. Fix the marker set to the")
print("  four measured centroids and the connectors follow.")

print()
print("### E. COLOUR (both judges' MINOR)")
print("  The render declares CURVE_BLUE = 2E75B6 = (46,117,182).")
print("  Original measured curve means: LEFT [155,199,209], RIGHT [140,196,210];")
print("     darkest 25% cores: LEFT [123,175,186], RIGHT [88,174,198].")
print("  => the original's stroke is a LIGHT CYAN, materially lighter than 2E75B6;")
print("     both judges read the same thing (crop: 'lighter cyan/blue'; full-slide:")
print("     '~#7CC7D5 vs ~#4472C4 family'). The claim is CORRECT in substance even")
print("     though the exact hex named is off. NOT refuted.")

print()
print("### F. 'Loss' CASING (crop_4 finding 5, MINOR)")
print("  The analysis JSON's verbatim label is 'Loss' and the full-slide judge read a")
print("  capital L in BOTH images. => REFUTED; no change.")
