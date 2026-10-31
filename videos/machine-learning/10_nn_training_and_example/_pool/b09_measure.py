#!/usr/bin/env python3
"""b09: measure ground-truth geometry of slide 17/18 originals (960x540)."""
import sys
from PIL import Image

def load(p):
    return Image.open(p).convert("RGB")

def near(px, rgb, tol=28):
    return all(abs(px[i] - rgb[i]) <= tol for i in range(3))

def bbox_of(img, rgb, tol=28, region=None):
    W, H = img.size
    x0, y0, x1, y1 = region or (0, 0, W, H)
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if near(img.getpixel((x, y)), rgb, tol):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))

def color_at(img, x, y):
    return img.getpixel((x, y))

def main(path):
    im = load(path)
    W, H = im.size
    print(f"== {path} size={im.size}")
    probes = [
        ("cream_panel", (247, 241, 228)),
        ("panel_border_maroon", (150, 40, 40)),
        ("error_bar_darkred", (204, 0, 0)),
        ("eq_box_paleyellow", (255, 255, 224)),
        ("class_box_green", (204, 255, 204)),
        ("inputbox_pink", (255, 153, 255)),
        ("badge_yellow", (255, 249, 196)),
        ("magenta_dot", (204, 0, 204)),
        ("title_maroon", (192, 0, 0)),
    ]
    for name, rgb in probes:
        b = bbox_of(im, rgb, 30)
        print(f"  {name:22s} {rgb} -> {b}")

    # row profile: count non-background pixels per row within panel
    print("  -- red-ish pixel column histogram (x:count) --")
    for name, rgb, tol in [("darkred", (204, 0, 0), 40)]:
        cols = {}
        for x in range(W):
            n = sum(1 for y in range(H) if near(im.getpixel((x, y)), rgb, tol))
            if n > 5:
                cols[x] = n
        # group contiguous
        groups = []
        cur = []
        prev = None
        for x in sorted(cols):
            if prev is None or x - prev <= 2:
                cur.append(x)
            else:
                groups.append((cur[0], cur[-1], sum(cols[k] for k in cur)))
                cur = [x]
            prev = x
        if cur:
            groups.append((cur[0], cur[-1], sum(cols[k] for k in cur)))
        print(f"    {name} groups: {groups}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
