#!/usr/bin/env python3
"""Correct-classifier ASCII ink-map of a region, ORIG vs render (frame space).

Fixed the white/pink ordering bug: white (all>240) is checked BEFORE pink.
Classifies each cell to: ink(#), red(R), blue(B), yellow(y), cyan(c), pink(m),
white(.), light-gray(,), else(space).
"""
import numpy as np
from PIL import Image
import sys

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"


def load():
    o = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
    r = Image.open(QA + "/render_17.png").convert("RGB").resize((960, 540), Image.LANCZOS)
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
        return "y"          # yellow FFFF99
    if g > 195 and b > 195 and 175 < r < 220:
        return "c"          # cyan CCFFFF
    if r > 235 and 160 <= g <= 205 and 185 <= b <= 218:
        return "m"          # pink FFC0CB
    if mn > 235:
        return "."          # white
    if mx - mn < 24 and 150 < r < 238:
        return ","          # light gray
    return " "


def amap(a, win, sx, sy):
    x0, y0, x1, y1 = win
    out = []
    for y in range(y0, y1, sy):
        row = []
        for x in range(x0, x1, sx):
            blk = a[y:y + sy, x:x + sx].reshape(-1, 3).mean(axis=0)
            row.append(ch(blk))
        out.append("".join(row))
    return out


if __name__ == "__main__":
    win = tuple(int(v) for v in sys.argv[1:5])
    sx = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    sy = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    a, r = load()
    ao, ar = amap(a, win, sx, sy), amap(r, win, sx, sy)
    w = max(len(x) for x in ao)
    print(f"win={win} sx={sx} sy={sy} x0={win[0]} y0={win[1]}   LEFT=ORIG  RIGHT=render17")
    for i in range(max(len(ao), len(ar))):
        lo = ao[i] if i < len(ao) else ""
        lr = ar[i] if i < len(ar) else ""
        print(f"{win[1]+i*sy:3d} {lo:<{w}}  {lr}")
