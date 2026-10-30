#!/usr/bin/env python3
"""Compare slide_014 original vs render on the same measured features.

Original: 960x540 (72.02 px/in). Render: 2001x1125 (150.07 px/in).
Scale = render_dpi / original_dpi.
"""
import sys
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{BASE}/unique_slides/slide_014.jpg"
REND = f"{BASE}/recreated_pptx/build/slide_014_rendered-1.png"

SCALE = 150.075 / 72.017


def load(path, gray=True):
    im = Image.open(path).convert("L" if gray else "RGB")
    return np.asarray(im).astype(int), im


def classify_rgb(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(axis=2)
    sat = mx - a.min(axis=2)
    cls = np.full(a.shape[:2], ".")
    dark = mx < 215
    redish = (R > G + 35) & (R > B + 35) & (R > 90)
    greenish = (G > R + 30) & (G > B + 30) & (G > 80)
    blueish = (B > R + 30) & (B > G + 30) & (B > 80)
    purpleish = (R > B - 30) & (B > G + 20) & (sat > 18) & (mx > 150) & (mx < 250)
    cls[dark] = "K"
    cls[redish & dark] = "R"
    cls[greenish & dark] = "G"
    cls[blueish & dark] = "B"
    cls[purpleish & ~dark] = "P"
    return cls


def rowruns(cls, x0, y0, x1, y1, minrun=3, label="", only=None):
    print(f"\n== {label}: x[{x0}..{x1}] y[{y0}..{y1}] ==")
    for j in range(y0, y1):
        row = cls[j]
        out, inr = [], False
        for i in range(x0, x1):
            v = row[i]
            ok = v != "." and (only is None or v in only)
            if ok and not inr:
                inr, st = True, i
            elif not ok and inr:
                inr = False
                out.append((st, i - 1, row[st]))
        if inr:
            out.append((st, x1 - 1, row[st]))
        out = [o for o in out if o[1] - o[0] + 1 >= minrun]
        if out:
            print(f"  y={j:4d}  " + "  ".join(f"[{p}..{q}]{c}" for p, q, c in out))


def feature(a, cls, name):
    print(f"\n########## {name} ##########")
    # 1. w11 label zone: red glyphs in x[170..210] orig
    def find_red_bbox(x0, y0, x1, y1):
        sub = cls[y0:y1, x0:x1] == "R"
        ys, xs = np.where(sub)
        if not len(ys):
            return None
        return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)
    print("  red-in-w11-zone bbox:", find_red_bbox(170, 130, 205, 152))
    print("  red-in-w12-zone bbox:", find_red_bbox(225, 130, 275, 152))
    print("  red-in-w21-zone bbox:", find_red_bbox(170, 190, 215, 215))
    print("  red-in-w22-zone bbox:", find_red_bbox(225, 190, 275, 215))
    # 2. threshold box: purple bbox
    sub = cls[150:235, 400:545] == "P"
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  purple bbox: x[{xs.min()+400}..{xs.max()+400}] y[{ys.min()+150}..{ys.max()+150}]")
    # 3. O/P glyphs: black cluster x[495..545] y[195..225]
    sub = cls[190:235, 495:560] == "K"
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  O/P ink bbox: x[{xs.min()+495}..{xs.max()+495}] y[{ys.min()+190}..{ys.max()+190}]")
    else:
        print("  O/P ink bbox: NONE")
    # 4. SUM line 1: ink rows in x[84..300] (left group) and x[380..592] (right group)
    for (lx0, lx1, tag) in [(84, 300, "SUM1-left"), (380, 592, "SUM2-right")]:
        sub = cls[300:480, lx0:lx1] == "K"
        ys = np.where(sub.any(axis=1))[0]
        if len(ys):
            print(f"  {tag} K ink rows: y[{ys.min()+300}..{ys.max()+300}]")
    # 5. equation panel border
    sub = cls[300:500, 60:620]
    dark = cls[300:500, 60:620] != "."
    ys = np.where(dark.any(axis=1))[0]
    print(f"  panel-ish dark rows y[{ys.min()+300}..{ys.max()+300}]")


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "orig":
        a, _ = load(ORIG, gray=False)
        cls = classify_rgb(a)
        feature(a, cls, "ORIGINAL (960x540, 72 px/in)")
    else:
        a, _ = load(REND, gray=False)
        cls = classify_rgb(a)
        S = SCALE
        # scale the feature coordinates
        print(f"render scale = {S:.4f}")
        feature(a, cls, "RENDER (2001x1125, 150 dpi)")
