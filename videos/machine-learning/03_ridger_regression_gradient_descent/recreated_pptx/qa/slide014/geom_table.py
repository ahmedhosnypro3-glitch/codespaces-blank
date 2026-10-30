#!/usr/bin/env python3
"""DEFINITIVE geometry table for slide014 (build-2) — robust classification that
tolerates JPEG noise. Every element measured against BOTH the original frame
(960x540) and the 150dpi render (2001x1125), in frame-px units.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0


def cls(c):
    R, G, B = int(c[0]), int(c[1]), int(c[2])
    mx, mn = max(R, G, B), min(R, G, B)
    sat = mx - mn
    if mx < 150:
        return "ink"
    if sat < 10 and mx >= 247:
        return "white"
    if sat < 14 and 205 <= mx <= 246:
        return "gray"
    # red stroke (C00000 family, JPEG-darkened maroon)
    if R - G > 40 and R - B > 10 and R > 90:
        return "red"
    if B - R > 4 and G >= 215 and G - B > -40:
        return "blue"          # pale blue band
    if G - B > 12 and R >= 245 and G >= 235:
        return "yellow"        # pale yellow band
    if R - G > 12 and R - B > 12 and R >= 240 and 200 <= G <= 240:
        return "pink"          # pale pink band
    if R - G > 20 and R - B > 30 and R >= 240 and 195 <= G <= 235:
        return "peach"         # peach band
    if G - R > 12 and G - B > 6:
        return "green"
    if R - G > 60 and G < 130:
        return "pure_red"
    if B - R > 60:
        return "pure_blue"
    return "other"


def runs_on_line(line, scale):
    prev = None
    runs = []
    for i, c in enumerate(line):
        k = cls(c)
        if k != prev:
            runs.append([i, i, k])
            prev = k
        else:
            runs[-1][1] = i
    # merge runs shorter than 3 render px into neighbours
    merged = []
    for a, b, k in runs:
        if merged and (b - a) < 3 * scale:
            merged[-1][1] = b
        else:
            merged.append([a, b, k])
    return [(a / scale, b / scale, k) for a, b, k in merged]


def summarize(line, scale, want, min_w=8, label=""):
    runs = runs_on_line(line, scale)
    sel = [(a, b, k) for a, b, k in runs if k == want and (b - a) >= min_w]
    return sel


def y_extent(im, col_x, scale, want, y0, y1):
    rows = []
    for y in range(int(y0 * scale), int(y1 * scale)):
        if cls(im[y, int(col_x * scale)]) == want:
            rows.append(y)
    if not rows:
        return None
    return rows[0] / scale, rows[-1] / scale


def x_extent(im, row_y, scale, want, x0, x1):
    cols = []
    for x in range(int(x0 * scale), int(x1 * scale)):
        if cls(im[int(row_y * scale), x]) == want:
            cols.append(x)
    if not cols:
        return None
    return cols[0] / scale, cols[-1] / scale


def all_runs_of(line, scale, minw=8):
    """All fill-class runs wider than minw, merged across small interruptions."""
    runs = runs_on_line(line, scale)
    return [(a, b, k) for a, b, k in runs if k not in ("ink", "other", "red") and (b - a) >= minw]


print("=" * 104)
print("ORIGINAL — full-width band rows (each row's fill runs)")
print("=" * 104)
for y in (252, 266, 276, 316, 334, 356, 374, 386, 396, 406, 416, 426, 438, 444, 480, 492, 504, 516, 522):
    print(f" y={y:3d}: " + "  ".join(f"{k} {a:.0f}..{b:.0f}" for a, b, k in all_runs_of(o[y], 1.0)))

print()
print("=" * 104)
print("RENDER — same rows")
print("=" * 104)
for y in (252, 266, 276, 316, 334, 356, 374, 386, 396, 406, 416, 426, 438, 444, 480, 492, 504, 516, 522):
    print(f" y={y:3d}: " + "  ".join(f"{k} {a:.0f}..{b:.0f}" for a, b, k in all_runs_of(r[int((y + .5) * SC)], SC)))

print()
print("=" * 104)
print("VERTICAL EXTENTS of each band (column scan through a fill point)")
print("=" * 104)
PROBES = [
    ("ridge yellow band",    500, "yellow", 240, 295),
    ("objective yellow band", 500, "yellow", 300, 345),
    ("peach band (orig only)", 300, "peach", 340, 400),
    ("yellow band y400-445 (orig only)", 700, "yellow", 390, 455),
    ("define-loss band (render)", 700, "pink", 390, 455),
    ("blue term boxes",      100, "blue", 460, 535),
    ("blue term boxes R",    560, "blue", 460, 535),
    ("final blue band",      700, "blue", 500, 535),
]
for name, cx, kind, y0, y1 in PROBES:
    eo = y_extent(o, cx, 1.0, kind, y0, y1)
    er = y_extent(r, cx, SC, kind, y0, y1)
    print(f"  {name:32s} col x={cx:3d}: ORIG {eo}   REND {er}")

print()
print("=" * 104)
print("HORIZONTAL EXTENTS (row scan through a fill point, text-free rows)")
print("=" * 104)
HPROBES = [
    ("ridge band",          261, "yellow"),
    ("objective band",      330, "yellow"),
    ("peach band",          360, "peach"),
    ("orig yellow mid band", 420, "yellow"),
    ("render pink band",    410, "pink"),
    ("left term box",       505, "blue"),
    ("right term box",      505, "blue"),
    ("final band",          512, "blue"),
]
for name, ry, kind in HPROBES:
    eo = x_extent(o, ry, 1.0, kind, 40, 910)
    er = x_extent(r, ry, SC, kind, 40, 910)
    print(f"  {name:22s} row y={ry:3d}: ORIG {eo}   REND {er}")

print()
print("=" * 104)
print("VECTOR BOXES (white vs gray, class-based)")
print("=" * 104)
for tag, im, scale in (("ORIG", o, 1.0), ("REND", r, SC)):
    for name, cx in (("left box", 62), ("right box", 520)):
        # column scan for WHITE only
        ys = [y for y in range(int(90 * scale), int(250 * scale))
              if cls(im[y, int(cx * scale)]) == "white"]
        if ys:
            g = []
            st = ys[0]; pv = ys[0]
            for v in ys[1:]:
                if v - pv > 3 * scale:
                    g.append((st, pv)); st = v
                pv = v
            g.append((st, pv))
            g = [(a, b) for a, b in g if b - a > 3 * scale]
            print(f"  {tag} {name} (white col x={cx}): " +
                  ", ".join(f"y {a/scale:.0f}..{b/scale:.0f} (h {(b-a)/scale:.0f})" for a, b in g))
    for name, ry in (("left box", 110), ("left box low", 240)):
        xs = [x for x in range(int(40 * scale), int(460 * scale))
              if cls(im[int(ry * scale), x]) == "white"]
        if xs:
            print(f"  {tag} {name} white row y={ry}: x {xs[0]/scale:.0f}..{xs[-1]/scale:.0f} (w {(xs[-1]-xs[0])/scale:.0f})")
    for name, ry in (("right box", 110), ("right box low", 240)):
        xs = [x for x in range(int(460 * scale), int(910 * scale))
              if cls(im[int(ry * scale), x]) == "white"]
        if xs:
            print(f"  {tag} {name} white row y={ry}: x {xs[0]/scale:.0f}..{xs[-1]/scale:.0f} (w {(xs[-1]-xs[0])/scale:.0f})")

print()
print("=" * 104)
print("BOX BORDER (dark ink) — vector boxes, left box in ORIGINAL vs RENDER")
print("=" * 104)
for tag, im, scale in (("ORIG", o, 1.0), ("REND", r, SC)):
    # vertical border strokes of the left vector box: scan row y=215 (inside box, below text)
    row = im[int(215.5 * scale)]
    darkx = [x / scale for x in range(int(40 * scale), int(470 * scale)) if cls(row[x]) == "ink"]
    if darkx:
        # group
        g = []
        st = darkx[0]; pv = darkx[0]
        for v in darkx[1:]:
            if v - pv > 2:
                g.append((st, pv)); st = v
            pv = v
        g.append((st, pv))
        print(f"  {tag} left box ink cols at y=215: " +
              ", ".join(f"{a:.0f}..{b:.0f}" for a, b in g))
    # horizontal border of left box: scan col x=250
    col = im[:, int(250 * scale)]
    darky = [y / scale for y in range(int(90 * scale), int(250 * scale)) if cls(col[y]) == "ink"]
    if darky:
        g = []
        st = darky[0]; pv = darky[0]
        for v in darky[1:]:
            if v - pv > 2:
                g.append((st, pv)); st = v
            pv = v
        g.append((st, pv))
        print(f"  {tag} left box ink rows at x=250: " +
              ", ".join(f"{a:.0f}..{b:.0f}" for a, b in g))
