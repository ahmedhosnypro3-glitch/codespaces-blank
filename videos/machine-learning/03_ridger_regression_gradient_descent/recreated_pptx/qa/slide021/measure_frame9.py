#!/usr/bin/env python3
"""measure_frame9.py — panel edges, title edges, boldness, λ/I splits (fixed)."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
blue = (b > 120) & (b - r > 60) & (b - g > 60)
red = (r > 100) & (r - g > 60) & (r - b > 60)
dark = (r < 110) & (g < 110) & (b < 110)
ink_lt = (r < 215) | (g < 215) | (b < 215)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(vec) - 1))
    return out

print("=== panel edges: blue col runs at rows 200/350/480 (full width) ===")
for y in (200, 350, 480, 140, 300, 450, 250, 400, 520):
    rr = runs(blue[y, :])
    print(f" y={y}: {rr}")

print("=== title edges (red mask y78..99) ===")
m = red.copy(); m[:78] = False; m[100:] = False
m[:, :270] = False; m[:, 730:] = False
ys, xs = np.where(m)
print(f" bbox x {xs.min()+270}..{xs.max()+270} y {ys.min()+78}..{ys.max()+78}")
cnt = m.sum(axis=1)
for y in range(78, 100):
    xs2 = np.where(m[y, 270:730])[0]
    if len(xs2):
        print(f"  y={y}: n={len(xs2)} x {xs2.min()+270}..{xs2.max()+270}")

print("=== 'Singular Matrix' stroke boldness (x491..512, dark) ===")
for y in range(192, 212, 2):
    line = "".join('#' if (r[y, x] < 130 and g[y, x] < 130) else ('+' if ink_lt[y, x] else '.') for x in range(491, 513))
    print(f"  y={y} x491: {line}")

print("=== λ/I blue row runs: bottom expr (x232..266) ===")
for y in range(466, 490):
    rr = runs(blue[y, 232:266])
    if rr:
        print(f"  y={y}: {[(s+232, e+232) for s, e in rr]}")
print("=== λ/I blue row runs: mid label (x168..210) ===")
for y in range(302, 324):
    rr = runs(blue[y, 168:210])
    if rr:
        print(f"  y={y}: {[(s+168, e+168) for s, e in rr]}")

print("=== chain 'Singular Matrix' + 'Non-Singular Matrix' per-glyph band y ===")
for nm, (x0, x1) in (("SingularMatrix", (490, 630)), ("NonSingularMatrix", (515, 695)), ("NoInverse-red", (700, 800)), ("InverseExists-red", (755, 880))):
    m = (red | dark)[170:230 if nm in ("SingularMatrix", "NoInverse-red") else 340:395, x0:x1]
    rr = runs(m.any(axis=1))
    print(f" {nm}: y runs {rr}")

print("=== green lambda=3 glyph map (x244..290, y303..321) ===")
green = (g > 100) & (g - r > 50) & (g - b > 50)
for y in range(303, 322):
    line = "".join('G' if green[y, x] else ('#' if dark[y, x] else ('+' if ink_lt[y, x] else '.')) for x in range(244, 291))
    if 'G' in line or '#' in line:
        print(f"  y={y} x244: {line}")

print("=== top table gridline color check + bottom table gridline color ===")
def line_core(name, pts):
    pts2 = [a[y, x] for (y, x) in pts]
    arr = np.array(pts2)
    srt = arr[np.argsort(arr.sum(axis=1))][:6]
    print(f" {name}: darkest6 median {tuple(np.median(srt, axis=0).astype(int))}")
line_core("top h-grid y191 x200..250", [(191, x) for x in range(200, 250, 5)])
line_core("top v-grid x166 y180..220", [(y, 166) for y in range(180, 220, 4)])
line_core("mid h-grid y360 x120..250", [(360, x) for x in range(120, 250, 5)])
line_core("mid h-grid y342 x150", [(y, 342) for y in range(342, 343)])
line_core("mid v-grid x158 y345..390", [(y, 158) for y in range(345, 390, 4)])
line_core("bot v-grid x490 y460..505", [(y, 490) for y in range(460, 505, 4)])
line_core("bot h-grid y475 x430..610", [(475, x) for x in range(430, 610, 10)])
line_core("bot h-grid y493 x430..610", [(493, x) for x in range(430, 610, 10)])
line_core("bot v-grid x558 y460..505", [(y, 558) for y in range(460, 505, 4)])
