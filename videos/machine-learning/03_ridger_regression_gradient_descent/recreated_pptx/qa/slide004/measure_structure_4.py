#!/usr/bin/env python3
"""Structural map of the top band: not-white run ranges per row, for the
original slide 004 and render_4. Reveals the actual box rectangles and where
the tall matrix strokes sit, independently of any visual reading.
"""
from PIL import Image

ORIG = "unique_slides/slide_004.jpg"
RENDER = "recreated_pptx/qa/slide004/render_4.png"
o = Image.open(ORIG).convert("RGB")
r = Image.open(RENDER).convert("RGB").resize((960, 540), Image.LANCZOS)
opx, rpx = o.load(), r.load()

NW = lambda p: not (p[0] > 235 and p[1] > 235 and p[2] > 235)


def runs_on_row(px, y, x0=0, x1=960, minlen=4):
    out, s = [], None
    for x in range(x0, x1):
        v = NW(px[x, y])
        if v and s is None:
            s = x
        elif not v and s is not None:
            if x - s >= minlen:
                out.append((s, x - 1))
            s = None
    if s is not None and x1 - s >= minlen:
        out.append((s, x1 - 1))
    return out


def report(px, tag, ys):
    print("=" * 72)
    print(tag)
    print("=" * 72)
    for y in ys:
        rs = runs_on_row(px, y)
        desc = " ".join(f"{a}-{b}" for a, b in rs)
        print(f"y={y:3d} n_runs={len(rs):2d} | {desc}")


report(opx, "ORIGINAL slide_004.jpg  (rows every 8px, y90..230)", list(range(90, 231, 8)))
print()
report(rpx, "RENDER_4  (rows every 8px, y90..230)", list(range(90, 231, 8)))

print()
print("=" * 72)
print("ORIGINAL: rows y103..220, not-white runs (minlen 6) — FULL detail")
print("=" * 72)
for y in range(103, 221):
    rs = runs_on_row(opx, y, minlen=6)
    if rs:
        print(f"y={y:3d} | " + " ".join(f"{a}-{b}" for a, b in rs))
