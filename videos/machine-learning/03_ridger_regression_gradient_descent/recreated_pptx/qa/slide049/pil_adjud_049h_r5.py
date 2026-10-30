#!/usr/bin/env python3
# Round 5: contiguous rule/vertical mapping + top-table paren bitmap extraction.
import numpy as np
from PIL import Image
from collections import deque

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)
H, W = orig.shape[:2]
rh, rw = rend.shape[:2]
sx, sy = rw / W, rh / H
olum = (orig[:, :, 0] * 299 + orig[:, :, 1] * 587 + orig[:, :, 2] * 114) // 1000
rlum = (rend[:, :, 0] * 299 + rend[:, :, 1] * 587 + rend[:, :, 2] * 114) // 1000
x0s = np.minimum((np.arange(W) * sx).astype(int), rw - 1)
y0s = np.minimum((np.arange(H) * sy).astype(int), rh - 1)
rmin = np.minimum.reduceat(np.minimum.reduceat(rlum, y0s, axis=0), x0s, axis=1)
r_ink = rmin < 150
o_ink = olum < 205


def longest_run(v):
    run = best = 0
    for x in v:
        run = run + 1 if x else 0
        best = max(best, run)
    return best


print("--- R5 ORIG contiguous horizontal rules (run>=250, y40..510) ---")
for y in range(40, 510):
    b = longest_run(o_ink[y, 57:903])
    if b >= 250:
        xs = np.where(o_ink[y, 57:903])[0]
        print(f"  y{y}: run={b} x{57+xs.min()}..{57+xs.max()}")

print("--- R5 ORIG contiguous verticals (run>=150, x57..903) ---")
for x in range(57, 903):
    b = longest_run(o_ink[40:510, x])
    if b >= 150:
        ys = np.where(o_ink[40:510, x])[0]
        print(f"  x{x}: run={b} y{40+ys.min()}..{40+ys.max()}")

print("--- R5 RENDER contiguous horizontal rules (run>=250) ---")
for y in range(40, 510):
    b = longest_run(r_ink[y, 57:903])
    if b >= 250:
        xs = np.where(r_ink[y, 57:903])[0]
        print(f"  y{y}: run={b} x{57+xs.min()}..{57+xs.max()}")

print("--- R5 RENDER contiguous verticals (run>=150) ---")
for x in range(57, 903):
    b = longest_run(r_ink[40:510, x])
    if b >= 150:
        ys = np.where(r_ink[40:510, x])[0]
        print(f"  x{x}: run={b} y{40+ys.min()}..{40+ys.max()}")


def cc_label(ink, x0, x1, y0, y1, bridge=1):
    h, w = y1 - y0, x1 - x0
    sub = ink[y0:y1, x0:x1]
    d = sub.copy()
    for k in range(1, bridge + 1):
        d[:, k:] |= sub[:, :-k]
        d[:, :-k] |= sub[:, k:]
    lab = np.zeros((h, w), int)
    comps = []
    for i in range(h):
        for j in range(w):
            if d[i, j] and lab[i, j] == 0:
                q = deque([(i, j)])
                lab[i, j] = 1
                pix = []
                while q:
                    a, b = q.popleft()
                    pix.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < h and 0 <= nb < w and d[na, nb] and not lab[na, nb]:
                                lab[na, nb] = 1
                                q.append((na, nb))
                ys = [p[0] for p in pix]
                xs = [p[1] for p in pix]
                comps.append((min(xs), max(xs), min(ys), max(ys), pix))
    comps.sort(key=lambda c: (c[0], c[2]))
    return comps


print("\n--- R5 ORIG top-table comps x86..232 y74..127 (h>=6, w<=20) ---")
for (cx0, cx1, cy0, cy1, pix) in cc_label(o_ink, 86, 232, 74, 127):
    w, h = cx1 - cx0 + 1, cy1 - cy0 + 1
    if h >= 6 and w <= 20:
        print(f"-- x{86+cx0}..{86+cx1} y{74+cy0}..{74+cy1} (w{w} h{h})")
        if h <= 50:
            for yy in range(cy0, cy1 + 1):
                print("   " + "".join("#" if (yy, xx) in {(a, b) for a, b in pix} else "." for xx in range(cx0, cx1 + 1)))
