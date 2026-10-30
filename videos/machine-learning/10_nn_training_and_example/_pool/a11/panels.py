#!/usr/bin/env python3
"""Adaptive-quantize + connected-component panel finder (a11)."""
from PIL import Image
import sys
from collections import deque

def panels(path, max_colors=24, min_px=800, tol_px=1500):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    q = img.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    scale = W / 13.333
    idx = q.load()
    print(f"{path} {W}x{H}")
    for cnt, pi in counts[:12]:
        if cnt < 4000:
            continue
        rgb = tuple(pal[pi*3:pi*3+3])
        # flood-fill largest component of this color
        seen = set()
        best = None
        for y0 in range(0, H, 3):
            for x0 in range(0, W, 3):
                if idx[x0, y0] != pi or (x0, y0) in seen:
                    continue
                q2 = deque([(x0, y0)]); seen.add((x0, y0))
                xs = []; ys = []; n = 0
                while q2:
                    x, y = q2.popleft()
                    n += 1; xs.append(x); ys.append(y)
                    for nx, ny in ((x+2,y),(x-2,y),(x,y+2),(x,y-2)):
                        if 0 <= nx < W and 0 <= ny < H and idx[nx, ny] == pi and (nx, ny) not in seen:
                            seen.add((nx, ny)); q2.append((nx, ny))
                if n > 600 and (best is None or n > best[0]):
                    best = (n, min(xs), min(ys), max(xs), max(ys))
        if best:
            n, x0, y0, x1, y1 = best
            fill = cnt * 1.0 / ((W//2)*(H//2))
            print(f"  color{rgb} share={fill:.2%} comp={n} bbox x={x0/scale:5.2f}..{x1/scale:5.2f} "
                  f"y={y0/scale:5.2f}..{y1/scale:5.2f} w={(x1-x0)/scale:5.2f} h={(y1-y0)/scale:5.2f}")

panels(sys.argv[1])
