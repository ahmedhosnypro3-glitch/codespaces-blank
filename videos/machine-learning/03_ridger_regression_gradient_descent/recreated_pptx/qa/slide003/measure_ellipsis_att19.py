#!/usr/bin/env python3
"""Ellipsis-cell verification for slide 003 bottom design matrix + weight vector.

Frame space is 960x540 (1px = 1pt); render_19 (2001x1125) is LANCZOS-downscaled
to frame space before measuring so both images share one coordinate system.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"


def load():
    o = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
    r = (Image.open(QA + "/render_19.png").convert("RGB")
         .resize((960, 540), Image.LANCZOS))
    return np.asarray(o).astype(int), np.asarray(r).astype(int)


def ch(px):
    r, g, b = px
    mn, mx = min(r, g, b), max(r, g, b)
    if mn < 100:
        return "#"
    if r > 150 and g < 120 and b < 120:
        return "R"
    if b > 150 and r < 120 and g < 150:
        return "B"
    if r > 205 and g > 205 and b < 200:
        return "y"
    if g > 195 and b > 195 and 175 < r < 220:
        return "c"
    if r > 235 and 160 <= g <= 205 and 185 <= b <= 218:
        return "m"
    if mn > 235:
        return "."
    if mx - mn < 24 and 150 < r < 238:
        return ","
    return " "


def amap(a, win, sx=3, sy=3):
    x0, y0, x1, y1 = win
    return [[ch(a[y:y + sy, x:x + sx].reshape(-1, 3).mean(axis=0))
             for x in range(x0, x1, sx)] for y in range(y0, y1, sy)]


def show(win, sx=3, sy=3):
    a, r = load()
    ao, ar = amap(a, win, sx, sy), amap(r, win, sx, sy)
    w = max(len(x) for x in ao + ar)
    print(f"win={win} sx={sx} sy={sy}   |  y LEFT=ORIG RIGHT=render_19")
    for i in range(max(len(ao), len(ar))):
        lo = ao[i] if i < len(ao) else ""
        lr = ar[i] if i < len(ar) else ""
        print(f"{win[1] + i * sy:3d} {''.join(lo):<{w}} | {''.join(lr)}")


def rowfills(a, win):
    """Mean fill colour per y in win, to locate the design-matrix row bands."""
    x0, y0, x1, y1 = win
    out = []
    for y in range(y0, y1):
        row = a[y, x0:x1].reshape(-1, 3).mean(axis=0).astype(int)
        out.append((y, tuple(row)))
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "map":
        win = tuple(int(v) for v in sys.argv[2:6])
        sx = int(sys.argv[6]) if len(sys.argv) > 6 else 3
        sy = int(sys.argv[7]) if len(sys.argv) > 7 else 3
        show(win, sx, sy)
    else:
        print("usage: measure_ellipsis_att19.py map x0 y0 x1 y1 [sx sy]")
