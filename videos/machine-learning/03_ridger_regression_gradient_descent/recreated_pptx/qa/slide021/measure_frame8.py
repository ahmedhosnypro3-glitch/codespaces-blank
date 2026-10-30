#!/usr/bin/env python3
"""measure_frame8.py — last probes: bar/superscript colors, panel edges, glyph decomposition."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
ink_lt = (r < 215) | (g < 215) | (b < 215)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(vec) - 1))
    return out

def core(name, x0, x1, y0, y1):
    m = ink_lt[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    if not len(ys):
        print(f" {name}: EMPTY"); return
    pts = a[ys + y0, xs + x0]
    srt = pts[np.argsort(pts.sum(axis=1))][:8]
    print(f" {name}: n={len(ys)} darkest8 median {tuple(np.median(srt, axis=0).astype(int))} bbox x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")

print("=== det bar colors ===")
core("top left bar (x338..345)", 338, 345, 190, 210)
core("top right bar (x387..394)", 387, 394, 190, 210)
core("mid left bar (x333..342)", 333, 342, 356, 376)
core("mid right bar (x385..398)", 385, 398, 356, 376)
print("=== bottom superscript colors ===")
core("bot minus (x270..281, y469..475)", 270, 281, 469, 475)
core("bot '1' (x281..291, y464..478)", 281, 291, 464, 478)
core("bot '(' (x150..165)", 150, 165, 462, 495)
core("bot ')' (x264..272)", 264, 272, 462, 495)
core("bot '+' (x214..230)", 214, 230, 468, 490)
core("bot blue lambda (x234..256)", 234, 256, 464, 490)
core("bot blue I (x255..265)", 255, 265, 468, 490)
print("=== mid label pieces ===")
core("mid '(' (x86..97)", 86, 97, 300, 328)
core("mid ')' (x198..210)", 198, 210, 300, 328)
core("mid '+' (x148..166)", 148, 166, 305, 322)
print("=== panel right edges per panel (blue col runs at 3 rows each) ===")
for (y0, y1, pn) in ((200, 0, 1), (0, 350, 2), (0, 480, 3)):
    for y in [yy for yy in (y0, y1, 200, 350, 480) if yy]:
        rr = runs((b > 120) & (b - r > 60) & (b - g > 60))[y, :]
        if rr:
            print(f" y={y}: blue col runs {rr}")
print("=== title precise ink edges (red mask, y78..99, x270..730) ===")
red = (r > 100) & (r - g > 60) & (r - b > 60)
m = red[78:100, 270:730]
ys, xs = np.where(m)
print(f" title red bbox: x {xs.min()+270}..{xs.max()+270} y {ys.min()+78}..{ys.max()+78}")
# leftmost/rightmost per row for centering
rows = {}
for y in range(78, 100):
    xs2 = np.where(red[y, 270:730])[0]
    if len(xs2):
        rows[y] = (xs2.min() + 270, xs2.max() + 270)
for y, (x0, x1) in list(rows.items())[:5] + list(rows.items())[-5:]:
    print(f"  y={y}: x {x0}..{x1}")
print("=== top chain 'Singular Matrix'/'No Inverse' bold? thickness probe ===")
# stem width of 'S' in Singular: rows y193..207 at x493..500
for y in range(192, 212, 2):
    line = "".join('#' if (r[y, x] < 110 and g[y, x] < 110) else '.' for x in range(491, 512))
    print(f"  y={y} x491: {line}")
print("=== λ glyph in bottom expr (blue mask rows) ===")
bluem = (b > 120) & (b - r > 60) & (b - g > 60)
for y in range(464, 490):
    rr = runs(bluem[y, 232:266])
    if rr:
        print(f"  y={y}: {[(s+232, e+232) for s, e in rr]}")
print("=== mid label λ/I split (blue rows) ===")
for y in range(300, 328):
    rr = runs(bluem[y, 168:210])
    if rr:
        print(f"  y={y}: {[(s+168, e+168) for s, e in rr]}")
