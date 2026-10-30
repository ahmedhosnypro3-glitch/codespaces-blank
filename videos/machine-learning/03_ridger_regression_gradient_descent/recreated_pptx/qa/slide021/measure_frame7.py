#!/usr/bin/env python3
"""measure_frame7.py — final unknowns: bottom expr/arrow, det bars, yellow cores,
italic slant, title serif probe, arrow shapes."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

blue = (b > 120) & (b - r > 60) & (b - g > 60)
red = (r > 100) & (r - g > 60) & (r - b > 60)
green = (g > 100) & (g - r > 50) & (g - b > 50)
yellow = (r > 170) & (g > 170) & (b < 150)
dark = (r < 110) & (g < 110) & (b < 110)
ink_lt = (r < 215) | (g < 215) | (b < 215)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(vec) - 1))
    return out

print("=== A. BOTTOM EXPR x255..350 y455..505 (1px classes) ===")
for y in range(455, 506):
    line = []
    for x in range(255, 350):
        c = '.'
        if dark[y, x]: c = '#'
        elif red[y, x]: c = 'R'
        elif blue[y, x]: c = 'B'
        elif green[y, x]: c = 'G'
        elif yellow[y, x]: c = 'Y'
        elif ink_lt[y, x]: c = '+'
        line.append(c)
    if '#' in ''.join(line) or 'R' in ''.join(line) or 'B' in ''.join(line) or 'G' in ''.join(line):
        print(f" {y}: {255:3d} " + ''.join(line))

print("\n=== B. BOTTOM ARROW x340..400 y468..502 ===")
for y in range(468, 503):
    line = []
    for x in range(340, 400):
        c = '.'
        if dark[y, x]: c = '#'
        elif blue[y, x]: c = 'B'
        elif red[y, x]: c = 'R'
        elif ink_lt[y, x]: c = '+'
        line.append(c)
    s = ''.join(line)
    if '#' in s or 'B' in s or 'R' in s:
        print(f" {y}: {340:3d} " + s)

print("\n=== C. DET BARS top chain (x336..400, y186..210) ===")
for y in range(186, 211):
    line = []
    for x in range(336, 400):
        c = '.'
        if dark[y, x]: c = '#'
        elif red[y, x]: c = 'R'
        elif ink_lt[y, x]: c = '+'
        line.append(c)
    s = ''.join(line)
    if '#' in s or 'R' in s:
        print(f" {y}: {336:3d} " + s)

print("\n=== D. YELLOW CORES: badge vs diagonal cells ===")
# badge: circle center (876,73) d~35 -> sample ring interior away from numeral
by, bx = np.where(yellow[60:90, 855:897])
pts = a[by + 60, bx + 855]
srt = pts[pts.sum(axis=1).argsort()][::-1][:20]  # brightest
print(" badge yellow brightest-20 median:", tuple(np.median(srt, axis=0).astype(int)))
cy, cx = np.where(yellow[340:396, 100:290])
pts = a[cy + 340, cx + 100]
srt = pts[pts.sum(axis=1).argsort()][::-1][:40]
print(" cell yellow brightest-40 median:", tuple(np.median(srt, axis=0).astype(int)))

print("\n=== E. ITALIC SLANT probes (leftmost ink per row, top vs bottom) ===")
def slant(name, x0, x1, y0, y1, mask):
    ys = []
    for y in range(y0, y1 + 1):
        xs2 = np.where(mask[y, x0:x1 + 1])[0]
        if len(xs2):
            ys.append((y, xs2.min() + x0))
    if len(ys) > 4:
        top = np.median([x for (y, x) in ys[:max(3, len(ys)//3)]])
        bot = np.median([x for (y, x) in ys[-max(3, len(ys)//3):]])
        print(f" {name}: top-third leftmost~{top:.1f} bottom-third leftmost~{bot:.1f} slant dx={bot-top:.1f} over ~{len(ys)} rows")

slant("No Inverse (red italic?)", 705, 794, 193, 207, red)
slant("Inverse Exists (red italic?)", 761, 876, 359, 373, red)
slant("Singular Matrix (upright?)", 493, 623, 192, 211, dark)
slant("Non-Singular Matrix (upright?)", 517, 691, 359, 377, dark)

print("\n=== F. TITLE SERIF PROBE: 'I' of Inverse (x296..320, y75..100) + digit '0' ===")
for y in range(74, 101):
    line = []
    for x in range(292, 330):
        c = '.'
        if red[y, x]: c = 'R'
        elif ink_lt[y, x]: c = '+'
        line.append(c)
    s = ''.join(line)
    if 'R' in s:
        print(f" {y}: {292:3d} " + s)

print("\n=== G. ARROW SHAPES top/mid ===")
for name, (x0, x1, y0, y1) in {
    "top arrow1": (458, 480, 194, 208), "top arrow2": (658, 680, 194, 208),
    "mid arrow1": (486, 508, 360, 375), "mid arrow2": (725, 747, 360, 375)}.items():
    print(f" {name}:")
    for y in range(y0, y1):
        line = []
        for x in range(x0, x1):
            c = '.'
            if blue[y, x]: c = 'B'
            elif dark[y, x]: c = '#'
            elif ink_lt[y, x]: c = '+'
            line.append(c)
        s = ''.join(line)
        if 'B' in s or '#' in s:
            print(f"   {y}: {x0:3d} " + s)

print("\n=== H. GREEN core ===")
gy, gx = np.where(green)
pts = a[gy, gx]
srt = pts[pts.sum(axis=1).argsort()][:12]
print(" green darkest-12 median:", tuple(np.median(srt, axis=0).astype(int)))

print("\n=== I. TOP/MID/CHAIN label mathtext y-bands incl AA (low-threshold) ===")
for name, (x0, x1, y0, y1) in {
    "top label X^TX": (95, 145, 130, 158), "mid label": (88, 210, 298, 328),
    "bot expr": (150, 290, 462, 494), "top chain red frag": (340, 395, 185, 210)}.items():
    m = ink_lt[y0:y1, x0:x1]
    rr = runs(m.any(axis=1))
    print(f" {name}: ink_lt y runs {[(s+y0, e+y0) for s, e in rr]}")
