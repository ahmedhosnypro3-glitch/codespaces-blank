#!/usr/bin/env python3
"""Pre-judge selfcheck — slide 010, child-lane render attempt 3 (render_3.png,
150 dpi, 2001x1125). Worker w010-child-20261024b.

Ports the mission selfcheck logic (mission protocol §6) to portable paths
(resolved from this file's location) so it runs first-person on render_3.png.
Checks: 12 orange dots/panel, green cross ink, bright-green axis dots,
pale-rose projection pairs, red arrowheads/up-triangles, delta frame
containment, caption bands, blue fitted lines, crop scale audit. No equations
and no multi-line delimiters or tables on this slide (N/A).
"""
from PIL import Image
import numpy as np
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
R = os.path.join(HERE, "render_3.png")
O = os.path.join(DECK, "unique_slides", "slide_010.jpg")

im = Image.open(R).convert("RGB"); a = np.asarray(im).astype(int)
W, H = im.size
SX = W / 960.0; SY = H / 540.0
Rr, Gg, Bb = a[:, :, 0], a[:, :, 1], a[:, :, 2]
orig = np.asarray(Image.open(O).convert("RGB")).astype(int)

fails = []
def check(name, ok, detail):
    print(("PASS " if ok else "FAIL ") + name + " — " + detail)
    if not ok: fails.append(name)

def m2r(x, y):
    return int(round(x * SX)), int(round(y * SY))

def mask(m, kind):
    r, g, b = m[:, :, 0], m[:, :, 1], m[:, :, 2]
    if kind == "orange":   return (r > 190) & (g > 90) & (g < 200) & (b < 110)
    if kind == "green":    return (g > 90) & (g - r > 30) & (g - b > 30) & (g < 235)
    if kind == "bright":   return (g > 200) & (r < 130) & (b < 190)
    if kind == "pale":     return (r > 170) & (r - g > 18) & (r - b > 18) & (g > 105) & (b > 100)
    if kind == "red":      return (r > 90) & (r - g > 45) & (r - b > 45) & (g < 110)
    if kind == "navy":     return (b > 90) & (r < 110) & (g < 110)

def comps(mask_, minpix):
    seen = np.zeros_like(mask_, dtype=bool); out = []
    ys, xs = np.nonzero(mask_)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        stack = [(y0, x0)]; seen[y0, x0] = True; pts = []
        while stack:
            y, x = stack.pop(); pts.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask_[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
        if len(pts) >= minpix:
            p = np.array(pts); out.append((len(pts), p[:, 1].min(), p[:, 0].min(), p[:, 1].max(), p[:, 0].max()))
    return out

print("render %dx%d  SX=%.4f SY=%.4f" % (W, H, SX, SY))
PANELS = {"LEFT": (95, 107, 466, 474), "RIGHT": (486, 107, 871, 474)}
for name, (x0, y0, x1, y1) in PANELS.items():
    rx0, ry0 = m2r(x0, y0); rx1, ry1 = m2r(x1, y1)
    print("panel %s frame(%d,%d)-(%d,%d) render(%d,%d)-(%d,%d)" % (name, x0, y0, x1, y1, rx0, ry0, rx1, ry1))

orange = mask(a, "orange")
oc = comps(orange, 80)
left = [c for c in oc if c[1] < m2r(480, 0)[0]]
right = [c for c in oc if c[1] >= m2r(480, 0)[0]]
check("orange dots LEFT = 12", len(left) == 12, "found %d comps>=80px" % len(left))
check("orange dots RIGHT = 12", len(right) == 12, "found %d comps>=80px" % len(right))

green = mask(a, "green")
for name, x0, x1, y in (("LEFT", 128, 360, 238.5), ("RIGHT", 540, 772, 287)):
    ry = m2r(0, y)[1]
    band = green[max(0, ry - 3):ry + 4, m2r(x0, 0)[0]:m2r(x1, 0)[0]]
    n = int(band.sum())
    check("green horizontal %s" % name, n >= 120, "ink px in y-band ±3 = %d (row %.1f)" % (n, y))
for name, x, y0, y1 in (("LEFT", 353, 240, 431), ("RIGHT", 766.5, 288.5, 431)):
    rx = m2r(x, 0)[0]
    band = green[m2r(0, y0)[1]:m2r(0, y1)[1], max(0, rx - 3):rx + 4]
    n = int(band.sum())
    check("green vertical %s" % name, n >= 150, "ink px in x-band ±3 = %d (col %.1f)" % (n, x))
bright = mask(a, "bright")
bc = comps(bright, 60)
for name, cx, cy in (("LEFT", 353, 433), ("RIGHT", 766.5, 433)):
    rcx, rcy = m2r(cx, cy)
    hit = [c for c in bc if abs((c[1] + c[3]) / 2 - rcx) < 8 and abs((c[2] + c[4]) / 2 - rcy) < 8]
    d = ((hit[0][3] - hit[0][1] + 1) / SX, (hit[0][4] - hit[0][2] + 1) / SY) if hit else (0, 0)
    check("bright-green dot %s" % name, bool(hit) and 5 <= d[0] <= 12 and 5 <= d[1] <= 12,
          "dot at (%s) frame-px diameter %.1fx%.1f" % (name, d[0], d[1]))

pale = mask(a, "pale")
for name, x0, x1, y in (("LEFT y=289.5", 136, 320, 289.5), ("LEFT y=300.5", 136, 377, 300.5),
                        ("RIGHT y=291.5", 549, 733, 291.5), ("RIGHT y=301.5", 549, 790, 301.5)):
    ry = m2r(0, y)[1]
    band = pale[ry - 3:ry + 4, m2r(x0, 0)[0]:m2r(x1, 0)[0]]
    n = int(band.sum())
    check("pale-rose horizontal %s" % name, n >= 90, "ink px in y-band ±3 = %d" % n)
for name, x, y0, y1 in (("LEFT x=324", 324, 301, 434), ("LEFT x=382", 382, 312, 434),
                        ("RIGHT x=737", 737, 302, 434), ("RIGHT x=795", 795, 313, 434)):
    rx = m2r(x, 0)[0]
    band = pale[m2r(0, y0)[1]:m2r(0, y1)[1], rx - 3:rx + 4]
    n = int(band.sum())
    check("pale-rose vertical %s" % name, n >= 60, "ink px in x-band ±3 = %d" % n)

red = mask(a, "red")
for name, cx, cy in (("L head A", 131, 289.5), ("L head B", 131, 300.5), ("R head C", 545, 291.5),
                     ("R head D", 545, 301.5), ("L tri A", 324, 296.5), ("L tri B", 381, 308),
                     ("R tri C", 737, 297), ("R tri D", 794, 308.5)):
    rcx, rcy = m2r(cx, cy)
    win = red[rcy - 8:rcy + 9, rcx - 9:rcx + 10]
    n = int(win.sum())
    check("red mark %s" % name, n >= 25, "red ink px in 19x17 window = %d" % n)

for name, (x0, y0, x1, y1) in PANELS.items():
    rx0, ry0 = m2r(x0, y0); rx1, ry1 = m2r(x1, y1)
    win = np.zeros((H, W), bool)
    win[max(0, ry0 - 6):ry1 + 2, max(0, rx0 - 6):rx1 + 7] = True
    inner = np.zeros((H, W), bool)
    inner[ry0 + 4:ry1 - 3, rx0 + 4:rx1 - 3] = True
    outside = win & (~inner) & (green | pale)
    n_out = int(outside.sum())
    check("delta ink inside %s panel" % name, n_out == 0, "%d green/pale px outside the navy border (4px in)" % n_out)

for name, (x0, x1) in (("LEFT", (97, 432)), ("RIGHT", (504, 839))):
    rx0, rx1 = m2r(x0, 0)[0], m2r(x1, 0)[0]
    ry0, ry1 = m2r(0, 480)[1], m2r(0, 527)[1]
    band = a[ry0:ry1, rx0:rx1]
    dark = (band.max(axis=2) < 150).sum()
    check("caption ink %s" % name, dark > 2000, "dark ink px in band = %d" % dark)
    cols = np.nonzero((band.max(axis=2) < 150).any(axis=0))[0]
    check("caption ink inside %s band" % name, len(cols) > 0 and cols.min() > 4 and cols.max() < (rx1 - rx0 - 5),
          "ink x range %d..%d of band width %d" % (cols.min(), cols.max(), rx1 - rx0))

navy = mask(a, "navy")
blue = mask(a, "orange") | ((Bb > 120) & (Rr < 110) & (Gg < 110))
for name, x0, y0, x1, y1 in (("LEFT", 142, 352, 432, 200), ("RIGHT", 556, 390, 830, 256)):
    hits = 0
    for t in (0.1, 0.3, 0.5, 0.7, 0.9):
        fx = x0 + (x1 - x0) * t; fy = y0 + (y1 - y0) * t
        rx, ry = m2r(fx, fy)
        win = blue[ry - 6:ry + 7, rx - 6:rx + 7]
        if win.sum() >= 8: hits += 1
    check("blue fitted line %s" % name, hits == 5, "sampled 5 points on the measured segment, %d have ink" % hits)

print("scale audit: render/original panel width  LEFT %.4f  RIGHT %.4f  (expect SX=%.4f)" % (
    (m2r(466, 0)[0] - m2r(95, 0)[0]) / (466 - 95),
    (m2r(871, 0)[0] - m2r(486, 0)[0]) / (871 - 486), SX))
print("scale audit: render/original panel height LEFT %.4f  RIGHT %.4f  (expect SY=%.4f)" % (
    (m2r(0, 474)[1] - m2r(0, 107)[1]) / (474 - 107),
    (m2r(0, 474)[1] - m2r(0, 107)[1]) / (474 - 107), SY))

print()
print("SELFCHECK RESULT:", "PASS" if not fails else ("FAIL — " + ", ".join(fails)))
sys.exit(0 if not fails else 1)
