#!/usr/bin/env python3
"""Third pass: diagram label blobs, panel backgrounds, plot bg, equation box."""
import numpy as np
from PIL import Image

IMG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/unique_slides/slide_011.jpg")
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = a.shape


def hexs(px):
    return "#%02X%02X%02X" % tuple(px)


def classify(px):
    r, g, b = px
    mxv, mnv = max(px), min(px)
    s = mxv - mnv
    if r > 110 and r - g > 45 and r - b > 45:
        return "R"
    if b - r > 45 and b > 100:
        return "B"
    if g - r > 25 and b - r > 25:
        return "C"
    if g - r > 40 and g - b > 25:
        return "G"
    if s < 18:
        if mxv < 90:
            return "#"
        if mxv < 190:
            return "+"
        return "."
    return "?"


print("=== region backgrounds (is it white #FEFFFD or gray #E7E9E6?) ===")
pts = {
    "plot interior (700,150)": (700, 150), "plot interior (650,300)": (650, 300),
    "plot exterior (540,120)": (540, 120), "plot exterior (860,250)": (860, 250),
    "between table & plot (450,250)": (450, 250),
    "table interior (150,165)": (150, 165), "table interior (150,220)": (150, 220),
    "title area (400,80)": (400, 80),
    "diagram area (250,450)": (250, 450), "diagram area (480,450)": (480, 450),
    "eq box (620,430)": (620, 430), "eq box (790,455)": (790, 455),
    "below eq (700,480)": (700, 480), "bottom-left (100,450)": (100, 450),
    "far left (20,300)": (20, 300), "far right (940,450)": (940, 450),
}
for k, (x, y) in pts.items():
    print(f"  {k}: {hexs(a[y,x])}")

print()
print("=== diagram glyph blobs (dark text) x140-700 y390-490 ===")
reg = a[390:490, 140:700]
mx = reg.max(axis=2); mn = reg.min(axis=2)
dark = (mx < 150) & ((mx - mn) < 45)
seen = np.zeros_like(dark, bool)
comps = []
for yy in range(dark.shape[0]):
    for xx in range(dark.shape[1]):
        if not dark[yy, xx] or seen[yy, xx]:
            continue
        st = [(yy, xx)]; seen[yy, xx] = True; pts_ = []
        while st:
            cy, cx = st.pop(); pts_.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < dark.shape[0] and 0 <= nx < dark.shape[1] \
                            and dark[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; st.append((ny, nx))
        if len(pts_) >= 4:
            ys = [p[0] for p in pts_]; xs = [p[1] for p in pts_]
            comps.append((140 + min(xs), 140 + max(xs), 390 + min(ys), 390 + max(ys), len(pts_)))
for c in sorted(comps, key=lambda z: (z[2], z[0])):
    print("   blob x%d..%d y%d..%d n=%d" % c)

print()
print("=== diagram red/pink box edges: scan for long red horizontal/vertical runs x140-720 ===")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (R > 110) & (R - G > 45) & (R - B > 45)
PINK = (R > 200) & (B > 200) & (G < R - 15) & (G < B - 5)
for y in range(390, 495):
    xs = np.nonzero(RED[y, 140:720])[0]
    if len(xs) > 60:
        print(f"  RED row y={y}: x {140+xs.min()}..{140+xs.max()} n={len(xs)}")
for x in range(140, 720):
    ys = np.nonzero(RED[390:495, x])[0]
    if len(ys) > 30:
        print(f"  RED col x={x}: y {390+ys.min()}..{390+ys.max()} n={len(ys)}")
print("  --- pink runs ---")
for y in range(390, 495):
    xs = np.nonzero(PINK[y, 140:720])[0]
    if len(xs) > 60:
        print(f"  PINK row y={y}: x {140+xs.min()}..{140+xs.max()} n={len(xs)}")
for x in range(140, 720):
    ys = np.nonzero(PINK[390:495, x])[0]
    if len(ys) > 30:
        print(f"  PINK col x={x}: y {390+ys.min()}..{390+ys.max()} n={len(ys)}")

print()
print("=== full bottom strip map x140-720 y390-490 (sx=3,sy=3) ===")
for y in range(390, 490, 3):
    row = []
    for x in range(140, 720, 3):
        counts = {}
        for dy in range(3):
            for dx in range(3):
                c = classify(a[y + dy, x + dx]); counts[c] = counts.get(c, 0) + 1
        row.append(max(counts, key=counts.get))
    print(f"{y:4d} " + "".join(row))
