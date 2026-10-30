"""min_cluster leg (frame 195..520 x 355..512) — PIL measurement of the elements that
region carries, so the attempt-10 record has the numbers either way (the judge dispatch
has hung twice and is on its last allowed ladder round). Elements: dots 7-9, the yellow
minimum, the parabola vertex, the 'Minimum' label, the theta-hat caret under the axis, and
the faint grey '+'."""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
REN = QA + "render_10.png"
X0, Y0, X1, Y1 = 195, 355, 520, 512


def load(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(float)
    return a, a.shape[1] / 960.0


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


for tag, im, s in (("ORIG", *load(ORIG)), ("REND", *load(REN))):
    print(f"### {tag}  scale {s:.4f}")
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    # purple dots
    m = (B > 140) & (B - R > 40) & (G < 150)
    ys, xs = np.where(m)
    k = (xs / s >= X0) & (xs / s <= X1) & (ys / s >= Y0) & (ys / s <= Y1)
    fx, fy = xs[k] / s, ys[k] / s
    # cluster by connected region: simple 12-fpx binning
    order = np.argsort(fx)
    fx, fy = fx[order], fy[order]
    clusters, i = [], 0
    while i < len(fx):
        j = i
        while j + 1 < len(fx) and (fx[j + 1] - fx[j]) < 12:
            j += 1
        if j - i > 8:
            clusters.append((fx[i:j + 1].mean(), fy[i:j + 1].mean(), j - i + 1,
                             fx[i:j + 1].min(), fx[i:j + 1].max(),
                             fy[i:j + 1].min(), fy[i:j + 1].max()))
        i = j + 1
    for cx, cy, n, ax, bx, ay, by in clusters:
        print(f"  violet blob: centre ({cx:.2f},{cy:.2f}) n={n} "
              f"bbox x{ax:.0f}..{bx:.0f} y{ay:.0f}..{by:.0f} "
              f"d≈{max(bx-ax, by-ay):.0f} fpx")
    # yellow minimum
    yl = (R > 200) & (G > 190) & (B < 110) & (R - B > 110)
    ys, xs = np.where(yl)
    k = (xs / s >= X0) & (xs / s <= X1) & (ys / s >= Y0) & (ys / s <= Y1)
    if k.sum():
        print(f"  yellow: bbox x{xs[k].min()/s:.1f}..{xs[k].max()/s:.1f} "
              f"y{ys[k].min()/s:.1f}..{ys[k].max()/s:.1f} "
              f"centre ({(xs[k].min()+xs[k].max())/2/s:.2f},{(ys[k].min()+ys[k].max())/2/s:.2f}) n={int(k.sum())}")

print("\n### text/label ink census in the region (dark ink, excluding the red frame at x 193-194/716-717)")
for tag, im, s in (("ORIG", *load(ORIG)), ("REND", *load(REN))):
    L = lum(im)
    m = (L < 150)
    sub = m[int(Y0 * s):int(Y1 * s), int(X0 * s):int(X1 * s)]
    ys, xs = np.where(sub)
    # row bands
    rows = np.unique(ys / s + Y0)
    bands, k0 = [], 0
    for i in range(1, len(rows)):
        if rows[i] - rows[i - 1] > 2:
            bands.append((rows[k0], rows[i - 1])); k0 = i
    bands.append((rows[k0], rows[-1]))
    print(f"  {tag}: row bands {[(round(a), round(b)) for a, b in bands]}")

print("\n### '+' mark (grey, small) — search frame x 470..500, y 430..455")
for tag, im, s in (("ORIG", *load(ORIG)), ("REND", *load(REN))):
    L = lum(im)
    S = im.max(axis=2) - im.min(axis=2)
    m = (L >= 110) & (L <= 200) & (S < 50)
    ys, xs = np.where(m)
    k = (xs / s >= 470) & (xs / s <= 505) & (ys / s >= 430) & (ys / s <= 460)
    if k.sum():
        print(f"  {tag}: grey ink x{xs[k].min()/s:.1f}..{xs[k].max()/s:.1f} "
              f"y{ys[k].min()/s:.1f}..{ys[k].max()/s:.1f} n={int(k.sum())}")
    else:
        print(f"  {tag}: none")
