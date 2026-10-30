#!/usr/bin/env python3
"""Exact ink-run extraction for selected rows of the ORIGINAL's vector boxes."""
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
og = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)


def cls(R, G, B):
    if R > 242 and G > 242 and B > 242:
        return " "
    if abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 14:
        return " "
    if R > 150 and G < 115 and B < 115:
        return "R"
    if B > 145 and R < 95 and G < 95:
        return "B"
    if G > 115 and R < 155 and B < 155:
        return "G"
    if R < 135 and G < 135 and B < 135:
        return "#"
    return "."


def runs(y, x0, x1):
    out, start = [], None
    for x in range(x0, x1):
        if cls(*og[y, x]) != " ":
            if start is None:
                start = x
        elif start is not None:
            out.append((start, x - 1))
            start = None
    if start is not None:
        out.append((start, x1 - 1))
    # merge runs closer than 2px, drop 1px noise
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= 3:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return [(a, b) for a, b in merged if b - a >= 2]


def clsof(y, a, b):
    cc = {}
    for x in range(a, b + 1):
        c = cls(*og[y, x])
        cc[c] = cc.get(c, 0) + 1
    return "".join(f"{k}{v}" for k, v in sorted(cc.items(), key=lambda kv: -kv[1]))


print("### LEFT BOX (border x 79..435, y 99..237) — rows sampled")
for y in range(103, 236, 3):
    rr = runs(y, 80, 435)
    if rr:
        s = " ".join(f"{a}-{b}[{clsof(y, a, b)}]" for a, b in rr)
        print(f"y={y:3d}: {s[:230]}")

print("\n### RIGHT BOX (border x 456..812)")
for y in range(103, 236, 3):
    rr = runs(y, 457, 812)
    if rr:
        s = " ".join(f"{a}-{b}[{clsof(y, a, b)}]" for a, b in rr)
        print(f"y={y:3d}: {s[:230]}")

print("\n### COLUMN INK PROFILE, left box interior x 84..430, y 103..234")
for x in range(84, 431, 2):
    ys = [y for y in range(103, 235) if cls(*og[y, x]) != " "]
    if len(ys) >= 25:
        # contiguous spans
        spans, cur = [], [ys[0]]
        for y in ys[1:]:
            if y - cur[-1] <= 2:
                cur.append(y)
            else:
                spans.append((cur[0], cur[-1]))
                cur = [y]
        spans.append((cur[0], cur[-1]))
        print(f"  x={x:3d} inkrows={len(ys):3d} spans={spans}")

print("\n### COLUMN INK PROFILE, right box interior x 460..806")
for x in range(460, 807, 2):
    ys = [y for y in range(103, 235) if cls(*og[y, x]) != " "]
    if len(ys) >= 25:
        spans, cur = [], [ys[0]]
        for y in ys[1:]:
            if y - cur[-1] <= 2:
                cur.append(y)
            else:
                spans.append((cur[0], cur[-1]))
                cur = [y]
        spans.append((cur[0], cur[-1]))
        print(f"  x={x:3d} inkrows={len(ys):3d} spans={spans}")
