"""Fourth pass: the 'Cost' label's ink tone + position (both crop judges confirmed the
word is present in both crops; measure its tone/placement for the completeness of the
axis_top adjudication)."""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
REND = QA + "render_10.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(float)
    return a, a.shape[1] / 960.0


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


for tag, im, s in (("ORIG", *load(ORIG)), ("REND", *load(REND))):
    print(f"### {tag} (scale {s:.4f})")
    # text ink above the arrowhead: any non-white, non-panel ink in frame y 168..200,
    # x 195..270, excluding the red C00000 panel stroke at x 193-194
    y0, y1, x0, x1 = (int(v * s) for v in (168, 200, 196, 270))
    sub = im[y0:y1, x0:x1]
    L = lum(sub)
    S = sub.max(axis=2) - sub.min(axis=2)
    R = sub[:, :, 0]
    # the panel stroke is dark red C00000: R high, G/B low, and it is a thin vertical bar
    redbar = (R > 150) & (S > 100)
    ink = (L < 200) & (S < 90) & (~redbar)
    if ink.any():
        ys, xs = np.where(ink)
        px = sub[ink]
        print(f"  text ink bbox x {xs.min()/s+196:.1f}..{xs.max()/s+196:.1f} "
              f"y {ys.min()/s+168:.1f}..{ys.max()/s+168:.1f} n={len(px)}")
        print(f"  mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) "
              f"| lum p50 {np.median(0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2]):.0f} "
              f"| lum p10 {np.percentile(0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2],10):.0f}")
        # glyph runs
        colpres = ink.any(axis=0)
        runs, k = [], 0
        while k < len(colpres):
            if colpres[k]:
                k0 = k
                while k < len(colpres) and colpres[k]:
                    k += 1
                runs.append((k0, k))
            else:
                k += 1
        runs = [(round(a / s + 196, 1), round(b / s + 196, 1)) for a, b in runs
                if (b - a) / s > 0.6]
        print(f"  glyph col runs: {runs}")
        rows = ink.any(axis=1)
        rr = np.where(rows)[0]
        print(f"  text rows: {rr.min()/s+168:.1f}..{rr.max()/s+168:.1f}")
    else:
        print("  no text ink found in that band")
