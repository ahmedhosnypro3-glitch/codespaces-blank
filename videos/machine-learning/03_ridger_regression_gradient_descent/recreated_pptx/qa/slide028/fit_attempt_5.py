# Robust re-derivation of the slide-028 curve fits (v2).
#
# v1 was poisoned by the chart frame: the 1F4E79 outline is blue-dominant
# (b-r = 90 > 35) and its top border sits at y=127, inside the sampled window.
# Fix: sample y in 131..504 only (frame top 127-128, bottom 507-508), and use the
# per-column MEDIAN blue y as the anchor (median resists the minority of columns
# where a dot staircase arm crosses the curve), then trimmed least squares.
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
im = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
blue = (b - r) > 35

PANELS = {"LEFT": (161, 383), "RIGHT": (514, 737)}
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
    """Trimmed least squares: drop the worst residual anchor each round."""
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


def shape_report(c, x0, x1):
    xs = np.arange(x0, x1 + 0.001, 1.5)
    ys = np.polyval(c, xs)
    d = np.diff(ys)
    vx = xs[int(np.argmin(ys))]
    Lm = xs <= vx
    return dict(vertex=(float(vx), float(ys.min())),
                ymin=float(ys.min()), ymax=float(ys.max()),
                endL=float(ys[0]), endR=float(ys[-1]),
                monoL=bool(np.all(d[Lm[:-1]] <= 1e-9)),
                monoR=bool(np.all(d[~Lm[:-1]] >= -1e-9)),
                ssc=int(np.sum(np.diff(np.sign(d)) != 0)))


for name, (x0, x1) in PANELS.items():
    ax, ay = anchors_for(x0, x1)
    print("=== %s panel (x%d..%d), %d columns with ink ===" % (name, x0, x1, len(ax)))
    print("  profile:",
          " ".join("(%.0f,%.0f)" % p for p in list(zip(ax, ay))[::15]))
    for deg in (2, 3, 4):
        c, keep = robust_poly(ax, ay, deg)
        res = np.polyval(c, ax) - ay
        rmse = float(np.sqrt(np.mean(res[keep] ** 2)))
        mx = float(np.max(np.abs(res[keep])))
        sh = shape_report(c, x0, x1)
        print("  deg%d inliers=%d/%d RMSE=%5.2f max=%5.2f  vertex=(%.1f,%.1f) y:[%.0f..%.0f] "
              "endsL=%.0f endsR=%.0f monoL=%s monoR=%s ssc=%d"
              % (deg, keep.sum(), len(ax), rmse, mx,
                 sh["vertex"][0], sh["vertex"][1], sh["ymin"], sh["ymax"],
                 sh["endL"], sh["endR"], sh["monoL"], sh["monoR"], sh["ssc"]))
        print("       dropped: %s" % " ".join("%.0f" % a for a in ax[~keep]))
        print("       coef: %s" % " ".join("%.10e" % v for v in c))
