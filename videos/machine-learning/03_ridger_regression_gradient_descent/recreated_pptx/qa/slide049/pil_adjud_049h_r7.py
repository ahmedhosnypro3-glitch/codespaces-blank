#!/usr/bin/env python3
# Round 7: fix geometry — calc rows 2/4/6 ink censuses, top-table header row, calc right
# border, legend green span, aug-box title/tags, Iteration-2 box red extent, REPEAT color.
import numpy as np
from PIL import Image
from collections import deque

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)


def lum(a):
    return (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) // 1000


olum, rlum = lum(orig), lum(rend)
o_ink, r_ink = olum < 205, rlum < 205
o_red = (orig[:, :, 0] > 150) & (orig[:, :, 1] < 110) & (orig[:, :, 2] < 110)
r_red = (rend[:, :, 0] > 150) & (rend[:, :, 1] < 110) & (rend[:, :, 2] < 110)
o_grn = (orig[:, :, 1] > 150) & (orig[:, :, 1] - orig[:, :, 0] > 25) & (orig[:, :, 1] - orig[:, :, 2] > 25)


def comps(ink, x0, x1, y0, y1, bridge=1):
    sub = ink[y0:y1, x0:x1]
    h, w = sub.shape
    d = sub.copy()
    for k in range(1, bridge + 1):
        d[:, k:] |= sub[:, :-k]
        d[:, :-k] |= sub[:, k:]
    seen = np.zeros((h, w), bool)
    out = []
    for i in range(h):
        for j in range(w):
            if d[i, j] and not seen[i, j]:
                q = deque([(i, j)])
                seen[i, j] = True
                pix = []
                while q:
                    a, b = q.popleft()
                    pix.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < h and 0 <= nb < w and d[na, nb] and not seen[na, nb]:
                                seen[na, nb] = True
                                q.append((na, nb))
                ys = [p[0] for p in pix]
                xs = [p[1] for p in pix]
                out.append((x0 + min(xs), x0 + max(xs), y0 + min(ys), y0 + max(ys), len(pix)))
    out.sort(key=lambda c: (c[0], c[2]))
    return out


print("--- R7 calc row2/4/6 ORIG ink comps x278..850 ---")
for (ya, yb, tag) in ((198, 262, "row2"), (339, 394, "row4"), (471, 527, "row6")):
    cs = comps(o_ink, 278, 850, ya, yb)
    desc = "  ".join(f"x{a}..{b} y{c}..{d}" for (a, b, c, d, n) in cs)
    print(f"  {tag}: {desc}")

print("--- R7 top-table header comps x86..232 y56..77 ---")
for (a, b, c, d, n) in comps(o_ink, 86, 232, 56, 77):
    if n >= 8:
        print(f"  x{a}..{b} y{c}..{d} (w{b-a+1} h{d-c+1} n{n})")

print("--- R7 calc-table right border: ORIG ink n per x, y150..515 ---")
for x in range(846, 862):
    col = o_ink[150:515, x]
    print(f"  x{x}: n={int(col.sum())}")

print("--- R7 legend green span ORIG y105..130 ---")
ys, xs = np.nonzero(o_grn[100:135, 380:520])
if len(xs):
    print(f"  x{380+xs.min()}..{380+xs.max()} y{100+ys.min()}..{100+ys.max()} n={len(xs)}")
    sel = o_grn[100:135, 380:520]
    rr = orig[100:135, 380:520][:, :, 0][sel]
    gg = orig[100:135, 380:520][:, :, 1][sel]
    bb = orig[100:135, 380:520][:, :, 2][sel]
    print(f"  meanRGB=({rr.mean():.0f},{gg.mean():.0f},{bb.mean():.0f})")
    # per-column green extent to see which glyphs are green
    for x in range(380, 520, 4):
        col = o_grn[100:135, x]
        if col.any():
            yy = np.nonzero(col)[0]
            print(f"    x{x}: y{100+yy.min()}..{100+yy.max()}")

print("--- R7 aug-box title + tags comps ORIG x70..250 ---")
for (a, b, c, d, n) in comps(o_ink, 70, 250, 136, 165):
    if n >= 10:
        print(f"  title: x{a}..{b} y{c}..{d}")
for (a, b, c, d, n) in comps(o_ink, 70, 250, 228, 254):
    if n >= 10:
        print(f"  tags: x{a}..{b} y{c}..{d}")

print("--- R7 Iteration-2 box ORIG red extent y270..400 x60..260 ---")
ys, xs = np.nonzero(o_red[265:405, 60:260])
if len(xs):
    print(f"  x{60+xs.min()}..{60+xs.max()} y{265+ys.min()}..{265+ys.max()} n={len(xs)}")

print("--- R7 REPEAT color ORIG vs RENDER (red mask in y55..80 x420..540) ---")
ys, xs = np.nonzero(o_red[55:80, 420:540])
print(f"  ORIG red n={len(xs)}" + (f" x{420+xs.min()}..{420+xs.max()} y{55+ys.min()}..{55+ys.max()}" if len(xs) else ""))
ys, xs = np.nonzero(r_red[55:80, 420:540])
print(f"  RENDER red n={len(xs)}" + (f" x{420+xs.min()}..{420+xs.max()} y{55+ys.min()}..{55+ys.max()}" if len(xs) else ""))

print("--- R7 ORIG initialW label tail x418..445 y58..76 comps ---")
for (a, b, c, d, n) in comps(o_ink, 415, 445, 58, 76):
    print(f"  x{a}..{b} y{c}..{d} (w{b-a+1} h{d-c+1} n{n})")

print("--- R7 RENDER top-band red/ink comps x230..430 y55..85 ---")
for (a, b, c, d, n) in comps(r_ink | r_red, 230, 430, 55, 85):
    if n >= 6:
        print(f"  x{a}..{b} y{c}..{d} (w{b-a+1} h{d-c+1} n{n}) redn={int(r_red[c:d+1,a:b+1].sum())}")
