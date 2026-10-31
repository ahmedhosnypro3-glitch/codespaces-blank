#!/usr/bin/env python3
"""k17h probe: TR red diagonal segment red-hit on k14's TR asset composited at
slide (616,115) size 263x202, and BL extremum projections for k14's BL view.
"""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
A14 = NS + "/recreated_pptx/build/assets"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


# --- TR segment (652,189)->(667,165) on orig and on k14 TR asset composited ---
def seg_hit(canvas, x0, y0, x1, y1, n=60):
    hits = 0
    tot = 0
    for i in range(n + 1):
        t = i / n
        x = int(round(x0 + (x1 - x0) * t))
        y = int(round(y0 + (y1 - y0) * t))
        # 3x3 neighborhood
        nb = canvas[max(0, y - 1):y + 2, max(0, x - 1):x + 2]
        rm = redmask(nb)
        tot += 1
        if rm.any():
            hits += 1
    return hits / tot


print("orig seg (652,189)->(667,165) red-hit = %.3f" % seg_hit(orig, 652, 189, 667, 165))

for name, path in (("k14", A14 + "/plot_025_tr.png"),):
    tr = Image.open(path).convert("RGB").resize((263, 202), Image.BILINEAR)
    canvas = orig.copy()
    canvas[115:115 + 202, 616:616 + 263] = np.array(tr).astype(np.int32)
    print("%s TR asset composited seg red-hit = %.3f" % (name, seg_hit(canvas, 652, 189, 667, 165)))
    # also report red census in TR box for the composite
    from scipy import ndimage
    box = canvas[115:318, 616:880]
    rm = redmask(box)
    rm[:6] = False; rm[-6:] = False; rm[:, :6] = False; rm[:, -6:] = False
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 6:
            comps.append((len(xs), 616 + xs.min(), 115 + ys.min(), 616 + xs.max(), 115 + ys.max()))
    for c in sorted(comps, key=lambda t: (t[2], t[1]))[:12]:
        print("  red comp area=%d x%d..%d y%d..%d" % c)

# --- BL extremum projections under k14 BL geometry (recompute quickly) ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

spec = dict(x0=83, y0=290, w=293, h=237)
DPI = 300
fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
ax = fig.add_axes([0.05, 0.09, 0.90, 0.88], projection="3d")
ax.view_init(elev=28, azim=-62)
x = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, x)
Z = (4.6 * np.exp(-((X - 0.2) ** 2 + (Y - 0.4) ** 2) * 0.9)
     + 3.4 * np.exp(-((X + 1.9) ** 2 + (Y - 1.7) ** 2) * 1.5)
     - 4.8 * np.exp(-((X + 0.7) ** 2 + (Y + 1.6) ** 2) * 1.1)
     - 3.6 * np.exp(-((X - 1.8) ** 2 + (Y + 1.3) ** 2) * 1.4))
ax.plot_surface(X, Y, Z, cmap=plt.get_cmap("jet"), shade=False)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-6, 8)
ax.set_box_aspect((1, 1, 0.95), zoom=1.00)
fig.canvas.draw()


def proj(x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = fig.get_size_inches()[0] * DPI
    H = fig.get_size_inches()[1] * DPI
    fx, fy = disp[0] / W, 1.0 - disp[1] / H
    return (spec["x0"] + fx * spec["w"], spec["y0"] + (1 - fy) * spec["h"])


def extremum(cx, cy, want_max):
    d = (X - cx) ** 2 + (Y - cy) ** 2
    m = d < 0.9 ** 2
    masked = np.where(m, Z, -1e9 if want_max else 1e9)
    i = np.argmax(masked) if want_max else np.argmin(masked)
    return X.flat[i], Y.flat[i], Z.flat[i]


for key, (cx, cy, wm) in (("GM", (0.2, 0.4, True)), ("LMx", (-1.9, 1.7, True)),
                          ("LMn", (1.8, -1.3, False)), ("GMn", (-0.7, -1.6, False))):
    px, py, pz = extremum(cx, cy, wm)
    sx, sy = proj(px, py, pz)
    print("BL %s extremum -> slide (%.0f, %.0f)" % (key, sx, sy))
print("DONE")
