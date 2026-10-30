#!/usr/bin/env python3
"""Follow-up probes for slide 004 adjudication (looser JPEG thresholds)."""
import numpy as np
from PIL import Image

D = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
o = np.asarray(Image.open(D + "/unique_slides/slide_004.jpg").convert("RGB")).astype(int)

def masks(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 130) & (R - G > 40) & (R - B > 25)
    blue = (B > 120) & (B - R > 30) & (B - G > 15)
    dark = (a.max(axis=-1) < 165) & ~red & ~blue
    return red, blue, dark

def comps(mask, min_area=4):
    seen = np.zeros(mask.shape, dtype=bool)
    out = []
    for (y, x) in np.argwhere(mask):
        if seen[y, x]:
            continue
        stack = [(y, x)]; seen[y, x] = True; pts = []
        while stack:
            cy, cx = stack.pop(); pts.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] \
                       and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
        if len(pts) >= min_area:
            out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
    return sorted(out, key=lambda c: c[0])

def show(tag, x0, y0, c):
    print(f"  {tag}: x{x0+c[0]}..{x0+c[2]} y{y0+c[1]}..{y0+c[3]} area={c[4]} h={c[3]-c[1]+1} w={c[2]-c[0]+1}")

print("=== P1: remember eq, loose mask, wider band y116..162 ===")
reg = o[116:162, 786:890]
red, blue, dark = masks(reg)
print("  dark comps (x786,y116 origin):")
for c in comps(dark, 5):
    show("dark", 786, 116, c)
print("  red comps:")
for c in comps(red, 5):
    show("red", 786, 116, c)

print("\n=== P2: 'Let Y =' lead-in box1 x85..160 y138..170, per-color comps ===")
reg = o[138:170, 85:160]
red, blue, dark = masks(reg)
for nm, m in (("dark", dark), ("red", red), ("blue", blue)):
    for c in comps(m, 4):
        show(nm, 85, 138, c)

print("\n=== P2b: box2 lead-in 'Let Yh=' x427..500 y138..175 ===")
reg = o[138:175, 427:500]
red, blue, dark = masks(reg)
for nm, m in (("dark", dark), ("red", red), ("blue", blue)):
    for c in comps(m, 4):
        show(nm, 427, 138, c)

print("\n=== P3: under 'from Model Yh=XW' x555..750 y158..200 — horizontal bars ===")
reg = o[158:200, 555:750]
red, blue, dark = masks(reg)
any_ = red | blue | dark
for yy in range(reg.shape[0]):
    xs = np.flatnonzero(any_[yy])
    if xs.size == 0:
        continue
    for s in np.split(xs, np.flatnonzero(np.diff(xs) > 2) + 1):
        if s.size >= 5:
            print(f"  y={158+yy} run x{555+s[0]}..{555+s[-1]} len={s.size}")

print("\n=== P3b: glyph comps of the 'from Model' line itself y158..185 ===")
reg = o[158:186, 555:750]
red, blue, dark = masks(reg)
for nm, m in (("dark", dark), ("red", red)):
    for c in comps(m, 5):
        show(nm, 555, 158, c)

print("\n=== P4: where line2 Y-underline + line3 W-underline bands ===")
for tag, (x0, x1, y0, y1) in {
    "line2 Y region y312..345": (565, 625, 312, 345),
    "line3 W region y343..375": (558, 600, 343, 375),
}.items():
    reg = o[y0:y1, x0:x1]
    red, blue, dark = masks(reg)
    any_ = red | blue | dark
    for yy in range(reg.shape[0]):
        xs = np.flatnonzero(any_[yy])
        if xs.size == 0:
            continue
        for s in np.split(xs, np.flatnonzero(np.diff(xs) > 2) + 1):
            if s.size >= 5:
                print(f"  {tag}: y={y0+yy} run x{x0+s[0]}..{x0+s[-1]} len={s.size}")

print("\n=== P5: line1 subscript glyph inventory x564..626 y284..308 (dark+blue) ===")
reg = o[284:308, 564:626]
red, blue, dark = masks(reg)
m = dark | blue
for c in comps(m, 3):
    show("glyph", 564, 284, c)

print("\n=== P5b: line2 subscript 'N x 1' inventory x574..620 y312..338 ===")
reg = o[312:338, 574:620]
red, blue, dark = masks(reg)
m = dark | red
for c in comps(m, 3):
    show("glyph", 574, 312, c)

print("\n=== P6: box1 subscript 'N x 1' red group x186..214 y192..208 tall window ===")
reg = o[186:212, 160:220]
red, blue, dark = masks(reg)
for c in comps(red, 3):
    show("red", 160, 186, c)
print("  dark comps in same window (for paren/other ink):")
for c in comps(dark, 3):
    show("dark", 160, 186, c)

print("\n=== P7: box2 subscript red group x545..580 y196..214 ===")
reg = o[192:216, 540:585]
red, blue, dark = masks(reg)
for c in comps(red, 3):
    show("red", 540, 192, c)
