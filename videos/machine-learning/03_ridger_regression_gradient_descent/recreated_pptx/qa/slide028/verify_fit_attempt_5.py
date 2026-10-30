# Verify the shipped quartic curves: evaluate at measured anchors, report the
# TRUE valley (argmax of y, since image y grows downward), arm monotonicity,
# ripple (extra slope sign changes), and how the ends compare with the original.
#
# Coefficients are HIGH->LOW (as np.polyfit prints), evaluated with Horner.
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
im = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
blue = (b - r) > 35
YLO, YHI = 131, 504


def anchors_for(x0, x1):
    ax, ay = [], []
    for x in range(x0, x1 + 1):
        col = np.flatnonzero(blue[YLO:YHI, x]) + YLO
        if len(col):
            ax.append(x)
            ay.append(float(np.median(col)))
    return np.array(ax, float), np.array(ay, float)


def robust_poly(ax, ay, deg, iters=25):
    keep = np.ones(len(ax), bool)
    for _ in range(iters):
        c = np.polyfit(ax[keep], ay[keep], deg)
        res = np.abs(np.polyval(c, ax) - ay)
        order = np.argsort(-res)
        cand = keep.copy()
        cand[order[0]] = False
        if cand.sum() < 3 * (deg + 2):
            break
        if np.array_equal(cand, keep):
            break
        keep = cand
    return c, keep


def horner(c, x):
    """c high->low."""
    y = np.zeros_like(np.asarray(x, dtype=float))
    for v in c:
        y = y * x + v
    return y


PANELS = {"LEFT": (161, 383), "RIGHT": (514, 737)}

for name, (x0, x1) in PANELS.items():
    ax, ay = anchors_for(x0, x1)
    c, keep = robust_poly(ax, ay, 4)
    print("=== %s (x%d..%d) ===" % (name, x0, x1))
    print("  coeffs high->low:", " ".join("%.12e" % v for v in c))
    print("  JS [low->high]: [%s]" % ", ".join("%.12e" % v for v in c[::-1]))

    # sample check against measured anchors
    print("  sample   x : fit_y  meas_y  err")
    for x in np.linspace(x0, x1, 13).round():
        i = int(np.argmin(np.abs(ax - x)))
        print("      %6.0f : %6.1f %7.1f %6.1f" % (ax[i], float(horner(c, ax[i])), ay[i],
                                                   float(horner(c, ax[i]) - ay[i])))

    # dense shape: valley = argmax y (deepest point); ends higher up (smaller y)
    xs = np.arange(x0, x1 + 0.001, 1.5)
    ys = horner(c, xs)
    d = np.diff(ys)
    vx = xs[int(np.argmax(ys))]
    Larm = xs[:-1] <= vx          # left arm: y should be non-DEcreasing (descending)
    Rarm = ~Larm                  # right arm: y should be non-INcreasing (ascending)
    monoL = bool(np.all(d[Larm] >= -1e-9))
    monoR = bool(np.all(d[Rarm] <= 1e-9))
    ssc = int(np.sum(np.diff(np.sign(d)) != 0))
    endL, endR = float(ys[0]), float(ys[-1])
    print("  valley x=%.1f y=%.1f   ends: L=%.1f R=%.1f" % (vx, float(ys.max()), endL, endR))
    print("  left arm descending (y non-decreasing): %s" % monoL)
    print("  right arm ascending  (y non-increasing): %s" % monoR)
    print("  slope sign changes (ripple): %d  [0 or 1 = smooth]" % ssc)
    print("  end rise above valley: L=%.0f  R=%.0f px" % (float(ys.max()) - endL,
                                                          float(ys.max()) - endR))
    # inlier RMSE
    res = horner(c, ax) - ay
    print("  inliers %d/%d  RMSE=%.2f  max=%.2f" % (keep.sum(), len(ax),
                                                    float(np.sqrt(np.mean(res[keep] ** 2))),
                                                    float(np.max(np.abs(res[keep])))))
