#!/usr/bin/env python3
"""b09: find long uniform horizontal/vertical runs of a target color."""
import sys
from PIL import Image

def runs_scan(im, rgb, tol=18, min_run=8, axis="h"):
    W, H = im.size
    out = []
    if axis == "h":
        for y in range(H):
            x = 0
            while x < W:
                p = im.getpixel((x, y))
                if all(abs(p[i] - rgb[i]) <= tol for i in range(3)):
                    x2 = x
                    while x2 < W and all(abs(im.getpixel((x2, y))[i] - rgb[i]) <= tol for i in range(3)):
                        x2 += 1
                    if x2 - x >= min_run:
                        out.append((x, x2 - 1, y))
                    x = x2
                else:
                    x += 1
    else:
        for x in range(W):
            y = 0
            while y < H:
                p = im.getpixel((x, y))
                if all(abs(p[i] - rgb[i]) <= tol for i in range(3)):
                    y2 = y
                    while y2 < H and all(abs(im.getpixel((x, y2))[i] - rgb[i]) <= tol for i in range(3)):
                        y2 += 1
                    if y2 - y >= min_run:
                        out.append((y, y2 - 1, x))
                    y = y2
                else:
                    y += 1
    return out

def clusters(runs, gap=4):
    runs = sorted(runs)
    if not runs:
        return []
    groups = []
    cur = [runs[0]]
    for r in runs[1:]:
        if r[0] - cur[-1][1] <= gap:
            cur.append(r)
        else:
            groups.append(cur); cur = [r]
    groups.append(cur)
    out = []
    for g in groups:
        a = min(x[0] for x in g); b = max(x[1] for x in g)
        lo = min(x[2] for x in g); hi = max(x[2] for x in g)
        out.append((a, min(a, b), b, lo, hi, len(g)))
    # (x_start, x_end, lo_span, hi_span, nruns) -> simplify
    return [(g[0], g[2], g[3], g[4], len(g)) for g in groups]

if __name__ == "__main__":
    path = sys.argv[1]
    im = Image.open(path).convert("RGB")
    print(f"== {path} {im.size}")
    targets = [
        ("eq_paleyellow", (255, 255, 224)),
        ("class_green", (204, 255, 204)),
        ("cream_panel", (243, 234, 213)),
        ("cream_panel2", (240, 230, 205)),
        ("magenta_1", (204, 0, 204)),
        ("badge_yellow", (255, 249, 196)),
        ("darkred_bar", (160, 20, 20)),
        ("outline_maroon", (122, 30, 30)),
    ]
    for name, rgb in targets:
        hr = clusters(runs_scan(im, rgb, 18, 10, "h"), 6)
        vr = clusters(runs_scan(im, rgb, 18, 10, "v"), 6)
        # keep only substantial clusters
        hr = [c for c in hr if (c[3] - c[2]) >= 8 and (c[1] - c[0]) >= 20]
        vr = [c for c in vr if (c[3] - c[2]) >= 8 and (c[1] - c[0]) >= 20]
        print(f"  {name:16s} {rgb}")
        print(f"     H-clusters(x0..x1, y0..y1, n): {hr[:14]}")
        print(f"     V-clusters(y0..y1, x0..x1, n): {vr[:14]}")
