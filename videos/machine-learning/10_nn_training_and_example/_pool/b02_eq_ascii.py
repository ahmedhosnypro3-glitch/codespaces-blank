#!/usr/bin/env python3
"""ASCII-ink map of an equation PNG so its mathtext can be recovered verbatim."""
import sys
from PIL import Image

path = sys.argv[1]
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 190
a = Image.open(path).convert("RGBA")
w, h = a.size
step = max(1, w // cols)
cx = max(1, h // step)
for y in range(0, h, cx):
    row = []
    for x in range(0, w, step):
        blk = [a.getpixel((min(x + dx, w - 1), min(y + dy, h - 1)))[3] for dy in range(cx) for dx in range(step)]
        mx = max(blk)
        row.append(" " if mx < 20 else ("." if mx < 90 else ("+" if mx < 170 else "#")))
    print("".join(row).rstrip())
