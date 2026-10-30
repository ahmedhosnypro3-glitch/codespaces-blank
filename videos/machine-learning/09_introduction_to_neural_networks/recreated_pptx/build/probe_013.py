#!/usr/bin/env python3
"""Detailed PIL geometry probe for slide_013 original frame + a render (if given).

Measures: title ink bbox, badge, truth-table grid + cell fills, scatter-plot
frame, marker positions/colors, blue line extents, perceptron region, callout.
"""
import sys
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
SRC = sys.argv[1] if len(sys.argv) > 1 else f"{V}/unique_slides/slide_013.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"SOURCE {SRC}  SIZE {W}x{H}")
if W != 960:
    print("  NOTE: not 960x540 — frame is a render; use scale factors below")
    print(f"  scale to frame = {960/W:.4f} (x), {540/H:.4f} (y)")


def bbox(mask, name, minpx=30):
    ys, xs = np.where(mask)
    if len(xs) < minpx:
        print(f"  {name}: none ({len(xs)} px)")
        return None
    print(f"  {name}: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} "
          f"({xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}) n={len(xs)}")
    return xs.min(), ys.min(), xs.max(), ys.max()


def close(c, t, tol):
    return (np.abs(a[:, :, 0] - t[0]) <= tol) & \
           (np.abs(a[:, :, 1] - t[1]) <= tol) & \
           (np.abs(a[:, :, 2] - t[2]) <= tol)


print("\n== RED / firebrick strokes ==")
red = close((178, 34, 34), (178, 34, 34), 38) | close((192, 0, 0), (192, 0, 0), 38)
bbox(red, "all red ink", 100)
rowsum = red.sum(axis=1)
for y in range(H):
    if rowsum[y] > 100:
        xs = np.where(red[y])[0]
        print(f"    row y={y}: n={rowsum[y]} x{xs.min()}..{xs.max()}")

print("\n== TITLE band ink (dark red text) ==")
dred = close((128, 0, 0), (128, 0, 0), 70) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
band = dred.copy()
band[110:, :] = False
bbox(band, "dark-red title ink y<110", 20)

print("\n== YELLOW badge ==")
yel = (a[:, :, 0] > 210) & (a[:, :, 1] > 190) & (a[:, :, 2] < 200) & \
      (a[:, :, 0] - a[:, :, 2] > 40)
bbox(yel, "yellow blob", 50)

print("\n== TABLE cell fills (left region x<520, y 130-320) ==")
reg = np.zeros((H, W), bool)
reg[130:320, 0:520] = True
for name, t, tol in [("cyan #CCFFFF", (204, 255, 255), 18),
                     ("green #CCFFCC", (204, 255, 204), 18),
                     ("white #FFFFFF", (255, 255, 255), 6),
                     ("gray #E0E0E0", (224, 224, 224), 8)]:
    m = close(t, t, tol) & reg
    bbox(m, name, 80)

print("\n== TABLE red grid: columns/rows inside x 90..330 y 130..320 ==")
tred = red.copy()
tred[:, :85] = False
tred[:, 335:] = False
tred[:125] = False
tred[325:] = False
colsum = tred.sum(axis=0)
rowsum2 = tred.sum(axis=1)
print("  cols with ink>40:", [x for x in range(W) if colsum[x] > 40])
print("  rows with ink>40:", [y for y in range(H) if rowsum2[y] > 40])

print("\n== SCATTER PLOT region (x 500..900) ==")
preg = np.zeros((H, W), bool)
preg[80:400, 480:900] = True
pred = red & preg
bbox(pred, "red plot-frame ink", 40)
prows = pred.sum(axis=1)
pcols = pred.sum(axis=0)
print("  rows>40:", [y for y in range(80, 400) if prows[y] > 40])
print("  cols>40:", [x for x in range(480, 900) if pcols[x] > 40])

print("\n== MARKERS in plot ==")
for name, t, tol, minp in [("red X #B22222", (178, 34, 34), 40, 30),
                            ("green #008000", (0, 128, 0), 45, 30),
                            ("cyan #00CED1", (0, 206, 209), 45, 30),
                            ("darkblue #191970", (25, 25, 112), 45, 60)]:
    m = close(t, t, tol) & preg
    # split into components
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f"  {name}: none")
        continue
    order = np.lexsort((xs, ys))
    xs, ys = xs[order], ys[order]
    clusters = []
    used = np.zeros(len(xs), bool)
    for i in range(len(xs)):
        if used[i]:
            continue
        stack = [i]
        used[i] = True
        comp = []
        while stack:
            j = stack.pop()
            comp.append(j)
            for k in range(len(xs)):
                if not used[k] and abs(xs[k]-xs[j]) < 30 and abs(ys[k]-ys[j]) < 30:
                    used[k] = True
                    stack.append(k)
        if len(comp) >= minp:
            cx = xs[comp]; cy = ys[comp]
            clusters.append((cx.min(), cy.min(), cx.max(), cy.max(), len(comp)))
    print(f"  {name}: {len(clusters)} component(s)")
    for c in clusters:
        print(f"      x{c[0]}..{c[2]} y{c[1]}..{c[3]} n={c[4]}  "
              f"center=({(c[0]+c[2])/2:.1f},{(c[1]+c[3])/2:.1f})")

print("\n== BLUE line pixels: per-column y-extents (plot area) ==")
db = close((25, 25, 112), (25, 25, 112), 45) & preg
for x in range(530, 860, 20):
    ys = np.where(db[:, x])[0]
    if len(ys):
        # split into runs
        runs, s = [], ys[0]
        for i in range(1, len(ys)):
            if ys[i] != ys[i-1] + 1:
                runs.append((s, ys[i-1])); s = ys[i]
        runs.append((s, ys[-1]))
        print(f"  x={x}: runs {runs}")

print("\n== PERCEPTRON region (x 100..560, y 330..520) ==")
per = np.zeros((H, W), bool)
per[330:525, 90:570] = True
for name, t, tol, minp in [("purple #9370DB", (147, 112, 219), 55, 8),
                            ("blue ? #0000FF", (0, 0, 255), 60, 15),
                            ("red ink", (178, 34, 34), 38, 10)]:
    m = close(t, t, tol) & per
    bbox(m, name, minp)

print("\n== CALLOUT (bottom-right) ==")
creg = np.zeros((H, W), bool)
creg[400:540, 560:960] = True
peach = (a[:, :, 0] > 240) & (a[:, :, 1] > 225) & (a[:, :, 1] < 252) & \
        (a[:, :, 2] > 225) & (a[:, :, 2] < 252) & \
        (a[:, :, 0] - a[:, :, 2] >= 8) & (a[:, :, 0] - a[:, :, 1] >= 3) & creg
bbox(peach, "peach fill", 200)
cred = red & creg
bbox(cred, "callout red border", 40)

print("\n== BLACK ink clusters (axis arrows, text) in plot ==")
blk = (a[:, :, 0] < 70) & (a[:, :, 1] < 70) & (a[:, :, 2] < 70) & preg
bbox(blk, "black ink in plot", 30)
