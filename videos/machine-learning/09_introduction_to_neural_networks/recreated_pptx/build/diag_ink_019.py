#!/usr/bin/env python3
"""Slide 019 — ASCII ink maps of the duplicate-label regions, original vs render.

Deterministic pixel forensics: classify ink by colour class, drop panel borders
and gridlines, then print an ASCII map of the target window so text orientation
and doubling is visible without loading the image into any vision context.
"""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
RENDER = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_019_rendered-1.png"

PANELS = {
    "sigmoid": (105, 59, 410, 237),
    "tanh":    (499, 59, 804, 237),
    "tan":     (105, 297, 410, 475),
    "arctan":  (499, 297, 804, 475),
}


def load(path, scale=1.0):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if scale != 1.0:
        im = im.resize((int(round(w * scale)), int(round(h * scale))), Image.LANCZOS)
    return np.asarray(im).astype(int)


def classify(px):
    """Return an ink-class code for a pixel; 0 = background/not-text."""
    r, g, b = px
    # blue panel border / axes
    if b > 120 and b - max(r, g) > 60:
        return 2
    # red curve / red caption text
    if r > 120 and r - max(g, b) > 50:
        return 3
    # gray gridlines / gray tan curve
    if r > 150 and abs(r - g) < 12 and abs(g - b) < 12:
        return 4
    # dark text (axes labels, tick numbers, titles)
    if r < 130 and g < 130 and b < 130:
        return 1
    return 0


def ascii_map(arr, x0, y0, x1, y1, step_x=1, step_y=2, title=""):
    H, W = arr.shape[:2]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    print(f"  -- {title}  frame box x={x0}..{x1} y={y0}..{y1} --")
    hdr = "".join(str((x0 + i * step_x) // 10 % 10) if i % 10 == 0 else " " for i in range((x1 - x0 + step_x - 1) // step_x))
    print("     " + hdr)
    for row, yy in enumerate(range(y0, y1, step_y)):
        line = []
        for xx in range(x0, x1, step_x):
            px = arr[yy, xx]
            c = classify(px)
            line.append({0: ".", 1: "#", 2: "B", 3: "R", 4: "g"}[c])
        print(f"  {yy:4d} " + "".join(line))


def counts(arr, x0, y0, x1, y1, label=""):
    H, W = arr.shape[:2]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    sub = arr[y0:y1, x0:x1].reshape(-1, 3)
    cc = {"dark_text": 0, "blue": 0, "red": 0, "gray": 0, "other": 0}
    for px in sub:
        c = classify(px)
        cc[{1: "dark_text", 2: "blue", 3: "red", 4: "gray", 0: "other"}[c]] += 1
    print(f"    {label}: {cc}")
    return cc


if __name__ == "__main__":
    print("##### ORIGINAL #####")
    o = load(ORIG)
    # 1. y-axis label region of the sigmoid panel (top-left interior, above the plot)
    ascii_map(o, 108, 62, 210, 100, 2, 2, "ORIG sigmoid panel top-left interior (y-label + legend band)")
    counts(o, 108, 62, 210, 100, "ORIG sigmoid TL interior")
    # 2. tanh panel top-left interior
    ascii_map(o, 502, 62, 604, 100, 2, 2, "ORIG tanh panel top-left interior (y-label band)")
    counts(o, 502, 62, 604, 100, "ORIG tanh TL interior")
    # 3. arctan title band
    ascii_map(o, 502, 300, 712, 330, 2, 2, "ORIG arctan panel top-left interior (title band)")
    counts(o, 502, 300, 712, 330, "ORIG arctan TL interior")

    print("\n##### RENDER (scaled to frame coords) #####")
    s = 2001 / 960
    r = load(RENDER, s)
    ascii_map(r, 108, 62, 210, 100, 2, 2, "RENDER sigmoid panel top-left interior")
    counts(r, 108, 62, 210, 100, "RENDER sigmoid TL interior")
    ascii_map(r, 502, 62, 604, 100, 2, 2, "RENDER tanh panel top-left interior")
    counts(r, 502, 62, 604, 100, "RENDER tanh TL interior")
    ascii_map(r, 502, 300, 712, 330, 2, 2, "RENDER arctan panel top-left interior")
    counts(r, 502, 300, 712, 330, "RENDER arctan TL interior")
