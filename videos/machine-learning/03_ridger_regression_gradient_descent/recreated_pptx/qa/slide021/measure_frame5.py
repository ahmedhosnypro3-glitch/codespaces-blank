#!/usr/bin/env python3
"""measure_frame5.py — fine region dumps: tables (low-threshold ink), chains,
expressions, arrow colors, labels. 1px-accurate, per-cluster color cores."""
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
yellow = (r > 180) & (g > 180) & (b < 140)
dark = (r < 110) & (g < 110) & (b < 110)
# low-threshold ink: anything meaningfully darker than near-white panel fill
ink_lt = (r < 215) | (g < 215) | (b < 215)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(vec) - 1))
    return out

def region_dump(name, x0, x1, y0, y1, gap=4, min_run=1):
    print(f"\n=== {name} (x {x0}..{x1}, y {y0}..{y1}) low-threshold ink ===")
    m = ink_lt[y0:y1 + 1, x0:x1 + 1]
    for (ry0, ry1) in runs(m.any(axis=1)):
        sub = m[ry0:ry1 + 1]
        colsin = np.where(sub.any(axis=0))[0]
        ccl = []; s = colsin[0]; p = colsin[0]
        for x in colsin[1:]:
            if x - p > gap: ccl.append((s, p)); s = x
            p = x
        ccl.append((s, p))
        out = []
        for (cs, ce) in ccl:
            if ce - cs + 1 < min_run and min_run > 1:
                continue
            # color composition
            cls = {}
            for cn, cm in (("D", dark), ("B", blue), ("R", red), ("G", green), ("Y", yellow)):
                n = int(cm[y0 + ry0:y0 + ry1 + 1, x0 + cs:x0 + ce + 1].sum())
                if n >= 2:
                    ys2, xs2 = np.where(cm[y0 + ry0:y0 + ry1 + 1, x0 + cs:x0 + ce + 1])
                    pts = a[ys2 + y0 + ry0, xs2 + x0 + cs]
                    if cn == "D": srt = pts[pts.sum(axis=1).argsort()][:5]
                    elif cn == "B": srt = pts[pts[:, 2].argsort()][::-1][:5]
                    elif cn == "R": srt = pts[pts[:, 0].argsort()][::-1][:5]
                    elif cn == "G": srt = pts[pts[:, 1].argsort()][::-1][:5]
                    else: srt = pts[pts[:, 2].argsort()][:5]
                    med = np.median(srt, axis=0).astype(int)
                    cls[cn] = f"{n}@({med[0]},{med[1]},{med[2]})"
            out.append(f"x{x0+cs}..{x0+ce}[{'; '.join(cls.values())}]")
        print(f" y {y0+ry0}..{y0+ry1}: {' | '.join(out)}")

# 1. top table zone
region_dump("TOP TABLE", 88, 320, 165, 240, gap=6)
# 2. middle table zone
region_dump("MIDDLE TABLE", 88, 320, 328, 400, gap=6)
# 3. bottom table zone
region_dump("BOTTOM TABLE", 420, 660, 445, 515, gap=6)
# 4. top chain
region_dump("TOP CHAIN", 330, 900, 180, 215, gap=8)
# 5. middle chain
region_dump("MIDDLE CHAIN", 330, 900, 345, 385, gap=8)
# 6. middle label zone
region_dump("MIDDLE LABEL", 88, 330, 292, 330, gap=5)
# 7. bottom expression zone
region_dump("BOTTOM EXPR", 100, 340, 450, 505, gap=5)
# 8. top label
region_dump("TOP LABEL", 88, 200, 130, 160, gap=3)
# 9. yellow diagonal cells precise
print("\n=== YELLOW content cells ===")
ym = yellow.copy(); ym[:100, 840:] = False
ys, xs = np.where(ym)
for (ry0, ry1) in runs(np.bincount(ys, minlength=H).astype(bool)):
    if ry1 - ry0 < 2: continue
    sub = ym[ry0:ry1 + 1]
    colsin = np.where(sub.any(axis=0))[0]
    ccl = []; s = colsin[0]; p = colsin[0]
    for x in colsin[1:]:
        if x - p > 6: ccl.append((s, p)); s = x
        p = x
    ccl.append((s, p))
    print(f" y {ry0}..{ry1}: x clusters {ccl}")

# 10. arrows: direct color census in arrow boxes
def color_census(name, x0, x1, y0, y1):
    print(f"\n=== COLOR CENSUS {name} (x{x0}..{x1} y{y0}..{y1}) ===")
    m = ink_lt[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    pts = a[ys + y0, xs + x0]
    # print the darkest 15 unique-ish
    srt = pts[np.argsort(pts.sum(axis=1))]
    uniq = []
    for p in srt:
        if not any(abs(p[0]-q[0])<=12 and abs(p[1]-q[1])<=12 and abs(p[2]-q[2])<=12 for q in uniq):
            uniq.append(p)
        if len(uniq) >= 12: break
    for p in uniq:
        print(f"   ({p[0]},{p[1]},{p[2]})")

color_census("TOP ARROW 1 (x455..480)", 455, 480, 185, 212)
color_census("TOP ARROW 2 (x655..680)", 655, 680, 185, 212)
color_census("MID ARROW 1 (x470..495)", 470, 495, 352, 380)
color_census("MID ARROW 2 (x685..710)", 685, 710, 352, 380)
color_census("BOTTOM ARROW (x270..430)", 270, 430, 465, 500)
