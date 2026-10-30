#!/usr/bin/env python3
"""Probe 3: chord, end dots, purple marks, curve vertex."""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ren = Image.open(f"{V}/recreated_pptx/qa/slide031/render_31.png").convert("RGB")
org = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
RW, _ = ren.size
S = RW / 960.0
rp, op = ren.load(), org.load()

def is_dark(c): r, g, b = c; return r < 110 and g < 110 and b < 110
def is_purple(c): r, g, b = c; return r > 70 and b > 70 and g < r - 30 and g < b - 30

print("== R. chord black rows y140..155, x645..730 (dark census per row) ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    out = []
    for y in range(int(140 * sc), int(156 * sc)):
        n = sum(1 for x in range(int(645 * sc), int(730 * sc)) if is_dark(pxl[x, y]))
        if n >= 40: out.append(round(y / sc, 1))
    print(f" {name}: {out}")
    xs = [x for x in range(int(640 * sc), int(735 * sc)) for y in range(int(140 * sc), int(156 * sc)) if is_dark(pxl[x, y])]
    if xs:
        print(f" {name} chord x-extent: {min(xs)/sc:.1f}..{max(xs)/sc:.1f}")

print("\n== S. chord end dots (black blobs) around (650,146) and (717,146) ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    for cx in (652, 717):
        pts = [(x, y) for x in range(int((cx - 8) * sc), int((cx + 8) * sc)) for y in range(int(138 * sc), int(156 * sc)) if is_dark(pxl[x, y])]
        if pts:
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            print(f" {name} dot@{cx}: x {min(xs)/sc:.1f}..{max(xs)/sc:.1f} y {min(ys)/sc:.1f}..{max(ys)/sc:.1f} n={len(pts)}")
        else:
            print(f" {name} dot@{cx}: NONE")

print("\n== T. purple ink census, plot upper area x610..770 y105..145 ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    pts = [(x, y) for x in range(int(610 * sc), int(770 * sc)) for y in range(int(105 * sc), int(146 * sc)) if is_purple(pxl[x, y])]
    print(f" {name}: n={len(pts)}", f"first={pts[0][0]/sc:.1f},{pts[0][1]/sc:.1f}" if pts else "")

print("\n== U. vertex/curve: steel-blue census bottom half of plot ==")
def is_steel(c): r, g, b = c; return 120 <= r <= 200 and 140 <= g <= 215 and 150 <= b <= 225 and b >= r
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    pts = [(x, y) for x in range(int(578 * sc), int(805 * sc)) for y in range(int(200 * sc), int(305 * sc)) if is_steel(pxl[x, y])]
    ys = [p[1] for p in pts]
    print(f" {name}: n={len(pts)}", f"maxY={max(ys)/sc:.1f}" if pts else "")

print("\n== V. extra dash extent in render: red rows at col 687-688 ==")
rows = [y for y in range(60, 320) if (lambda c: c[0] > 150 and c[1] < 110 and c[2] < 110)(rp[int(687.5 * S), int(y * S)])]
if rows:
    print(f" REND x687.5 red y {min(rows)}..{max(rows)} n={len(rows)}")
    gaps = [(a, b) for a, b in zip(rows, rows[1:]) if b - a > 1]
    print(f" gaps: {gaps[:8]}")
