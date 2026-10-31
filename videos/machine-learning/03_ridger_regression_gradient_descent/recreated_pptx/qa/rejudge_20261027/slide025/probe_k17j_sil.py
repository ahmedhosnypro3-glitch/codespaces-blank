#!/usr/bin/env python3
"""Measure orig BR surface silhouette extremes + base diamond + z-axis line,
then numerically fit mplot3d (azim, elev, z-aspect) to the measured box corners.

BR panel crop: slide x615..880 y344..531 (local 266x188).
Orig surface bbox (prior GT): slide x624..864 y355..523.
"""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
X0, Y0, X1, Y1 = 615, 344, 881, 532
p = orig[Y0:Y1, X0:X1]
H, W = p.shape[:2]


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~red


m = colmask(p)
m[:4] = False; m[-4:] = False; m[:, :4] = False; m[:, -4:] = False
ys, xs = np.nonzero(m)
print("colored bbox local x%d..%d y%d..%d -> slide x%d..%d y%d..%d  colored%%=%.1f" % (
    xs.min(), xs.max(), ys.min(), ys.max(),
    X0 + xs.min(), X0 + xs.max(), Y0 + ys.min(), Y0 + ys.max(), 100 * m.mean()))

# extreme points
iL = xs.argmin(); iR = xs.argmax(); iT = ys.argmin(); iB = ys.argmax()
print("L slide (%d,%d)  R (%d,%d)  T (%d,%d)  B (%d,%d)" % (
    X0 + xs[iL], Y0 + ys[iL], X0 + xs[iR], Y0 + ys[iR],
    X0 + xs[iT], Y0 + ys[iT], X0 + xs[iB], Y0 + ys[iB]))

# per-column top/bottom envelope (slide coords)
print("\nper-column silhouette envelope (every 8 cols): col_slide  top_y  bot_y  width")
for lx in range(4, W - 4, 8):
    col = np.nonzero(m[:, lx])[0]
    if len(col):
        print("  x%3d  y%3d..%3d" % (X0 + lx, Y0 + col.min(), Y0 + col.max()))

# per-row left/right envelope
print("\nper-row envelope (every 8 rows): row_slide  left_x  right_x")
for ly in range(4, H - 4, 8):
    row = np.nonzero(m[ly])[0]
    if len(row):
        print("  y%3d  x%3d..%3d" % (Y0 + ly, X0 + row.min(), X0 + row.max()))

# bottom band: per-row colored% over full panel width, y470..531
print("\nper-row colored%% y470..531 (x615..880):")
for ly in range(470 - Y0, 532 - Y0):
    print("  y%d %.1f%%" % (Y0 + ly, 100 * m[ly].mean()))

# z-axis line: longest vertical dark run in slide x725..745
lum = 0.299 * p[:, :, 0] + 0.587 * p[:, :, 1] + 0.114 * p[:, :, 2]
sat = p.max(2) - p.min(2)
dark = (lum < 120) & (sat < 90)
print("\nz-axis scan slide x725..748: longest vertical dark run per col")
for lx in range(725 - X0, 749 - X0):
    col = dark[:, lx]
    best = 0; besty = None; cur = 0
    for y in range(H):
        if col[y]:
            cur += 1
            if cur > best:
                best = cur; besty = y - cur + 1
        else:
            cur = 0
    if best >= 15:
        print("  slide x%d run=%d y%d..%d (slide y %d..%d)" % (
            X0 + lx, best, besty, besty + best - 1, Y0 + besty, Y0 + besty + best - 1))

# ---- fit azim/elev to silhouette extremes via mplot3d's own projection ----
# Box: x,y in [-3,3]; z in [0, zr] (we fit zr as z-aspect). Screen from
# proj3d with elev/azim, then normalize: we compare SHAPE ratios, so scale-free.
# Measured (local px, y down): bbox x 9..249 y 11..179; extremes L,R,T,B.
Lm = np.array([xs.min(), ys[iL]], float)
Rm = np.array([xs.max(), ys[iR]], float)
Tm = np.array([xs[iT], ys.min()], float)
Bm = np.array([xs[iB], ys.max()], float)
MEAS = dict(bbox=(xs.min(), xs.max(), ys.min(), ys.max()), L=Lm, R=Rm, T=Tm, B=Bm)
print("\nmeasured local: bbox=%s L=%s R=%s T=%s B=%s" % (
    MEAS["bbox"], Lm, Rm, Tm, Bm))


def proj_box(elev, azim, zr):
    """project 8 box corners with mplot3d, return 2D pts (fig-normalized)."""
    corners = np.array([[x, y, z] for x in (-3, 3) for y in (-3, 3) for z in (0.0, zr)])
    # emulate Axes3D.get_proj for a unit-ish world: use proj3d with view rotation
    # mplot3d: M = rot_x(elev) then rot_z(azim)? We build the same matrices mpl uses:
    # from mpl_toolkits.mplot3d.proj3d: get_proj -> worldM then view rotation.
    # Easiest: use a throwaway Axes3D.
    fig = plt.figure(figsize=(1, 1), dpi=100)
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(0, zr)
    ax.set_box_aspect((6, 6, zr), zoom=1.0)
    M = ax.get_proj()
    plt.close(fig)
    x2, y2, _ = proj3d.proj_transform(corners[:, 0], corners[:, 1], corners[:, 2], M)
    return np.stack([x2, y2], 1)


print("\n== scan (elev, azim, zr) matching silhouette extremes ==")
best = []
for elev in range(15, 56, 3):
    for azim in range(-100, -19, 5):
        for zr in (2.0, 3.0, 4.0, 5.0, 6.0):
            P = proj_box(elev, azim, zr)
            # normalize: shift/scale so bbox matches measured bbox
            mn = P.min(0); mx = P.max(0)
            span = mx - mn
            if span[0] < 1e-6 or span[1] < 1e-6:
                continue
            target_span = np.array([MEAS["bbox"][1] - MEAS["bbox"][0],
                                    MEAS["bbox"][3] - MEAS["bbox"][2]], float)
            s = target_span / span
            Pn = (P - mn) * s  # now in measured bbox scale (y up though!)
            # mplot3d y is up; our measured y is down. flip:
            Pn[:, 1] = target_span[1] - Pn[:, 1]
            Pn[:, 0] += MEAS["bbox"][0]; Pn[:, 1] += MEAS["bbox"][2]
            # predicted extremes
            iL2 = Pn[:, 0].argmin(); iR2 = Pn[:, 0].argmax()
            iT2 = Pn[:, 1].argmin(); iB2 = Pn[:, 1].argmax()
            err = (np.hypot(*(Pn[iL2] - Lm)) + np.hypot(*(Pn[iR2] - Rm))
                   + np.hypot(*(Pn[iT2] - Tm)) + np.hypot(*(Pn[iB2] - Bm)))
            best.append((err, elev, azim, zr, Pn[iL2], Pn[iR2], Pn[iT2], Pn[iB2]))
best.sort(key=lambda b: b[0])
for b in best[:12]:
    print("err=%6.2f elev=%2d azim=%4d zr=%.1f | pred L(%5.1f,%5.1f) R(%5.1f,%5.1f) T(%5.1f,%5.1f) B(%5.1f,%5.1f)" % (
        b[0], b[1], b[2], b[3], b[4][0], b[4][1], b[5][0], b[5][1],
        b[6][0], b[6][1], b[7][0], b[7][1]))
print("\nmeasured for reference: L=%s R=%s T=%s B=%s" % (Lm, Rm, Tm, Bm))
