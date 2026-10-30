#!/usr/bin/env python3
"""Measure slide_011 original frame geometry (frame px = slide pt, 1px=1pt)."""
import sys
import numpy as np
from PIL import Image

IMG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/unique_slides/slide_011.jpg")

a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

RED = (R > 120) & (R - G > 50) & (R - B > 50) & (R < 245)
DARK = (R < 110) & (G < 110) & (B < 120)
BLUE = (B > R + 40) & (B > 100) & (R < 175)
CYAN = (G > R + 25) & (B > R + 25) & (G > 105)
GREEN = (G > R + 40) & (G > B + 25) & (G > 105)
WHITE = (R > 235) & (G > 235) & (B > 235)


def red_x_runs(y, minlen=1, x0=0, x1=None):
    """Red pixel runs on row y within [x0,x1). Returns list of (start,end) inclusive."""
    x1 = x1 or W
    out, x = [], x0
    while x < x1:
        if RED[y, x]:
            x2 = x
            while x2 + 1 < x1 and RED[y, x2 + 1]:
                x2 += 1
            if x2 - x + 1 >= minlen:
                out.append((x, x2))
            x = x2 + 1
        else:
            x += 1
    return out


def red_y_runs(x, minlen=1, y0=0, y1=None):
    y1 = y1 or H
    out, y = [], y0
    while y < y1:
        if RED[y, x]:
            y2 = y
            while y2 + 1 < y1 and RED[y2 + 1, x]:
                y2 += 1
            if y2 - y + 1 >= minlen:
                out.append((y, y2))
            y = y2 + 1
        else:
            y += 1
    return out


def bbox(mask, x0=0, x1=W, y0=0, y1=H):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None
    return (x0 + int(xs.min()), x0 + int(xs.max()), y0 + int(ys.min()), y0 + int(ys.max()))


def report(label, bb):
    print(f"  {label:28s} {bb}")


if __name__ == "__main__":
    print(f"frame {W}x{H}")
    print("== validation probes (known from prior forensics) ==")
    report("plot white body", bbox(WHITE & (np.arange(W)[None, :] > 530) & (np.arange(H)[:, None] > 100) & (np.arange(H)[:, None] < 375), 530, 850, 100, 375))
    print("  axis cross px (617,329):", tuple(a[329, 617]), " y-axis (618,150):", tuple(a[150, 618]))

    print("== truth-table red borders ==")
    for y in range(130, 315):
        rs = [r for r in red_x_runs(y, 25, 90, 340)]
        if rs:
            print(f"   y={y}: {rs}")
    print("== truth-table vertical red borders ==")
    for x in range(90, 340):
        ys = [r for r in red_y_runs(x, 25, 130, 315)]
        if ys:
            print(f"   x={x}: {ys}")

    print("== plot panel red border ==")
    for y in range(100, 385):
        rs = [r for r in red_x_runs(y, 20, 520, 860)]
        if rs:
            print(f"   y={y}: {rs}")
    for x in range(520, 860):
        ys = [r for r in red_y_runs(x, 20, 100, 385)]
        if ys:
            print(f"   x={x}: {ys}")

    print("== element bboxes ==")
    report("blue line", bbox(BLUE, 530, 850, 100, 380))
    report("cyan points", bbox(CYAN, 530, 850, 100, 380))
    report("green point", bbox(GREEN, 530, 850, 100, 380))
    report("red in plot", bbox(RED, 530, 850, 100, 380))
    report("dark in diagram", bbox(DARK, 95, 480, 395, 500))
    report("red in diagram", bbox(RED, 95, 480, 395, 500))
    report("dark in eq box", bbox(DARK, 650, 850, 390, 500))
    report("peach box", bbox((R > 240) & (G > 220) & (G < 240) & (B > 200) & (B < 225), 600, 900, 390, 500))
