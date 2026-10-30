#!/usr/bin/env python3
"""Find regions matching specific target colors (a11 slides 19/20)."""
from PIL import Image
import sys

def close(px, t, tol):
    return all(abs(px[i] - t[i]) <= tol for i in range(3))

def regions(path, targets, tol=18, min_area=40):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    scale = W / 13.333
    for name, t in targets:
        pts = []
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                if close(px[x, y], t, tol):
                    pts.append((x, y))
        if not pts:
            print(f"  {name:18s} NOT FOUND")
            continue
        # cluster into row-bands then report overall bbox + cluster count
        ys = sorted(set(p[1] for p in pts))
        bands = []
        cur = [ys[0]]
        for y in ys[1:]:
            if y - cur[-1] <= 6:
                cur.append(y)
            else:
                bands.append(cur); cur = [y]
        bands.append(cur)
        xs = [p[0] for p in pts]; yy = [p[1] for p in pts]
        print(f"  {name:18s} n={len(pts):5d} bbox x={min(xs)/scale:5.2f} y={min(yy)/scale:5.2f} "
              f"w={(max(xs)-min(xs))/scale:5.2f} h={(max(yy)-min(yy))/scale:5.2f} bands={len(bands)}")
        for b in bands[:12]:
            bp = [p for p in pts if b[0] <= p[1] <= b[-1]]
            bxs = [p[0] for p in bp]
            print(f"      band y={b[0]/scale:5.2f}..{b[-1]/scale:5.2f} x={min(bxs)/scale:5.2f}..{max(bxs)/scale:5.2f} n={len(bp)}")

if __name__ == "__main__":
    path = sys.argv[1]
    print(path)
    targets = [
        ("cyanpanel", (217, 242, 242)),
        ("tan", (216, 206, 192)),
        ("darkblue", (31, 78, 121)),
        ("cred", (192, 0, 0)),
        ("green", (0, 128, 0)),
        ("magenta", (204, 0, 204)),
        ("blueborder", (46, 92, 138)),
        ("ltblue", (230, 243, 255)),
        ("beige", (232, 224, 208)),
        ("orange", (244, 164, 96)),
        ("cream", (253, 246, 227)),
    ]
    regions(path, targets)
