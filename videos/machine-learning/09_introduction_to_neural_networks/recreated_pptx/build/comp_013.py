#!/usr/bin/env python3
"""Connected-component color analysis of slide_013 original plot + table + callout."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_013.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

CLASSES = {
    "BLUE-ink(pure blue, lines+axis)": (B > 55) & (R < 100) & (G < 70) & (B - R > 40),
    "RED-ink(dark red text/axis)": (R > 90) & (R - G > 50) & (R - B > 50),
    "FIREBRICK(X markers #B22222)": (R > 120) & (R < 215) & (G < 95) & (B < 95) & (R - G > 60),
    "GREEN(circles #008000)": (G > 60) & (G - R > 45) & (G - B > 35),
    "CYAN-ink(circles #00CED1)": (R < 140) & (G > 140) & (B > 140) & (G - R > 60) & (B - R > 60),
    "CYAN-fill(band)": (R > 145) & (R < 215) & (G > 225) & (B > 225) & (G - R > 18) & (B - R > 18),
    "GREEN-fill(band)": (R > 145) & (R < 220) & (G > 215) & (B > 150) & (B < 235) & (G - B > 12) & (G - R > 25),
    "PEACH-fill": (R > 243) & (G > 228) & (G < 252) & (B > 228) & (B < 252) & (R - G > 6),
    "BLACK-bar": (R < 60) & (G < 60) & (B < 60),
    "PURPLE-ink": (R > 70) & (R < 215) & (B > 110) & (B - G > 45) & (R - G > 8) & (B - R > 20),
}


def components(mask, minpx=20, gap=12):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return []
    n = len(xs)
    used = np.zeros(n, bool)
    comps = []
    order = np.argsort(-ys * 10000 + xs)
    for i0 in order:
        if used[i0]:
            continue
        stack = [i0]
        used[i0] = True
        comp = [i0]
        while stack:
            j = stack.pop()
            xj, yj = xs[j], ys[j]
            for k in range(n):
                if used[k]:
                    continue
                if abs(int(xs[k]) - int(xj)) <= gap and abs(int(ys[k]) - int(yj)) <= gap:
                    used[k] = True
                    stack.append(k)
                    comp.append(k)
        if len(comp) >= minpx:
            cx, cy = xs[comp], ys[comp]
            comps.append((int(cx.min()), int(cy.min()), int(cx.max()), int(cy.max()), len(comp)))
    comps.sort(key=lambda c: -c[4])
    return comps


for name, mask in CLASSES.items():
    # global bbox
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"\n{name}: NONE")
        continue
    print(f"\n{name}: total {len(xs)}  bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
    for c in components(mask, minpx=25)[:14]:
        print(f"    x{c[0]}..{c[2]} y{c[1]}..{c[3]} n={c[4]} "
              f"({c[2]-c[0]+1}x{c[3]-c[1]+1}) center=({(c[0]+c[2])/2:.1f},{(c[1]+c[3])/2:.1f})")

# ---- precise per-column blue extents inside plot panel -----------------------
print("\n== BLUE-ink per-column extents (plot panel x 530..860) ==")
bl = CLASSES["BLUE-ink(pure blue, lines+axis)"]
for x in range(530, 865, 4):
    ys = np.where(bl[:H, x])[0]
    if len(ys):
        runs, s, prev = [], ys[0], ys[0]
        for y in ys[1:]:
            if y != prev + 1:
                runs.append((s, prev)); s = y
            prev = y
        runs.append((s, prev))
        print(f"  x={x}: {[(int(r[0]), int(r[1])) for r in runs]}")

# ---- plot panel edge (pink-white) scan --------------------------------------
print("\n== plot panel pink-white runs, row y=250 ==")
pk = CLASSES["PEACH-fill"]
prev, st = False, None
out = []
inp = False
for x in range(500, 900):
    v = bool(pk[250, x])
    if v != prev:
        if v:
            inp = x
        else:
            out.append((inp, x - 1))
        prev = v
if prev:
    out.append((inp, 899))
print("  runs:", out)
print("== plot panel pink-white runs, col x=690 ==")
prev, st = None, None
out = []
inp = None
for y in range(90, 400):
    v = bool(pk[y, 690])
    if v != prev:
        if v:
            inp = y
        else:
            out.append((inp, y - 1))
        prev = v
if prev:
    out.append((inp, 399))
print("  runs:", out)
