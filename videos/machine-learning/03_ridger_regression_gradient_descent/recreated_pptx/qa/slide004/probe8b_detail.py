#!/usr/bin/env python3
"""ATTEMPT-8 MEASUREMENT PART 2 — loose-mask stroke extents, box2 rows, lead-in
boldness, underline bars, Where: slant, LO subscript calibration."""
from PIL import Image
import numpy as np

BASE = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
orig = Image.open(f"{BASE}/unique_slides/slide_004.jpg").convert("RGB")
A = np.asarray(orig).astype(int)
r33 = np.asarray(Image.open(f"{BASE}/recreated_pptx/qa/slide003/render_33.png").convert("RGB")).astype(int)
o33 = np.asarray(Image.open(f"{BASE}/unique_slides/slide_003.jpg").convert("RGB")).astype(int)


def loose_red(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 140) & (r - g > 22) & (r - b > 18)


def dark(a, t=430):
    return (a[..., 0] + a[..., 1] + a[..., 2]) < t


def bands(m, gap=2, run=1):
    idx = np.where(m)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - p > gap:
            if p - s + 1 >= run:
                out.append((int(s), int(p)))
            s = v
        p = v
    if p - s + 1 >= run:
        out.append((int(s), int(p)))
    return out


print("## 1. stroke extents (loose red), per stroke window")
for name, x0, x1 in [("box1_L", 154, 163), ("box1_R", 181, 189),
                     ("box2_L", 500, 509), ("box2_R", 526, 534)]:
    m = loose_red(A[100:220, x0:x1])
    rows = bands(m.any(axis=1), gap=6)
    cols = bands(m.any(axis=0), gap=2)
    print(f"  {name} x{x0}..{x1}: rows(abs) {[(100+s, 100+e) for s, e in rows]} cols(abs) {[(x0+s, x0+e) for s, e in cols]}")

print("\n## 2. box2 interior rows (loose red, x506..529)")
m = loose_red(A[105:218, 506:529])
for s, e in bands(m.any(axis=1), gap=4):
    seg = m[s:e + 1]
    cb = bands(seg.any(axis=0), gap=2)
    print(f"  row y{105+s}..{105+e}: cols {[(506+c, 506+d) for c, d in cb]}")

print("\n## 3. box2 label region x528..566 y190..218 (loose red)")
m = loose_red(A[190:218, 528:566])
print("  rows:", [(190 + s, 190 + e) for s, e in bands(m.any(axis=1), gap=3)])
for s, e in bands(m.any(axis=1), gap=3):
    seg = m[s:e + 1]
    print(f"   y{190+s}..{190+e} cols: {[(528+c, 528+d) for c, d in bands(seg.any(axis=0), gap=2)]}")

print("\n## 4. box1 interior rows (loose red, x161..183)")
m = loose_red(A[105:215, 161:183])
for s, e in bands(m.any(axis=1), gap=4):
    seg = m[s:e + 1]
    print(f"  row y{105+s}..{105+e}: cols {[(161+c, 161+d) for c, d in bands(seg.any(axis=0), gap=2)]}")

print("\n## 5. lead-in per-glyph density + bars")
for name, boxes in [
    ("box1", [("Let", 87, 110), ("Y", 118, 131), ("=", 140, 149)]),
    ("box2", [("Let", 431, 455), ("Yh", 464, 475), ("=", 486, 495)]),
]:
    for g, x0, x1 in boxes:
        reg = A[140:170, x0:x1]
        d = dark(reg)
        rows = bands(d.any(axis=1), gap=3)
        den = d.sum() / max(1, d.size)
        print(f"  {name} {g} x{x0}..{x1}: rows {[(140+s, 140+e) for s, e in rows]} inkfrac {den:.3f}")
print("  box1 under-Y raw rows y156..164, x118..132 (r,g,b at x120,x125,x130):")
for y in range(156, 165):
    print(f"   y{y}: " + "  ".join(str(tuple(A[y, x])) for x in (120, 125, 130)))

print("\n## 6. 'Where:' italic slant (L1 x508..531 y285..303)")
reg = A[283:305, 508:531]
d = dark(reg, 480)
ys, xs = np.where(d)
if len(xs):
    top = xs[ys < ys.min() + (ys.max() - ys.min()) / 3].mean()
    bot = xs[ys > ys.max() - (ys.max() - ys.min()) / 3].mean()
    print(f"  top-third centroid {top:.1f} vs bottom-third {bot:.1f} -> slant {top - bot:+.1f}px (italic leans right at top)")

print("\n## 7. LO subscript calibration — slide003 y-vec entries, render vs original")
# build: 15pt 'y' + 15pt subscript digit, textbox x109..143, rows y368/397/427/456
for tag, img, sx, sy in [("RENDER33", r33, 2001 / 960, 1125 / 540), ("ORIG003", o33, 1.0, 1.0)]:
    reg = img[int(362 * sy):int(490 * sy), int(111 * sx):int(141 * sx)]
    dd = (reg[..., 0] + reg[..., 1] + reg[..., 2]) < 430
    for s, e in bands(dd.any(axis=1), gap=4):
        seg = dd[s:e + 1]
        cb = bands(seg.any(axis=0), gap=2)
        hh = [f"x{111+sx and ''}{int(111 + c / sx)}..{int(111 + d_ / sx)} h{int((rr[1] - rr[0] + 1) / sy)}"
              for c, d_ in [(c, d) for c, d in cb]
              for rr in [np.where(seg[:, c:d + 1].any(axis=1))[0]]]
        print(f"  {tag} row y{int(362 + s / sy)}..{int(362 + e / sy)}: {hh}")
