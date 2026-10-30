#!/usr/bin/env python3
"""Slide 032 — grayscale heat map of the ORIGINAL's right chord-endpoint label.

Prints per-pixel luminance as hex-ish intensity so faint JPEG-thresholded
strokes are visible; also prints a component census at several thresholds.
"""
import os
from collections import deque
from PIL import Image

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")

RAMP = " .:-=+*#%@"   # light -> dark

def heat(path, x0, y0, x1, y1, label):
    im = Image.open(path).convert("L")
    px = im.load()
    print(f"--- {label}: x{x0}..{x1} y{y0}..{y1}   (ramp: ' '=white .. '@'=black)")
    print("      " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("      " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = ""
        for x in range(x0, x1):
            v = px[x, y]
            i = min(9, max(0, int((255 - v) / 255 * 9.999)))
            row += RAMP[i]
        print(f"{y:4d} {row}")
    print()

def comps(im, x0, y0, x1, y1, thr):
    px = im.load()
    pts = {(x, y) for y in range(y0, y1) for x in range(x0, x1) if px[x, y] < thr}
    out = []
    while pts:
        s = pts.pop(); q = deque([s]); b = [s]
        while q:
            cx, cy = q.popleft()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    p = (cx + dx, cy + dy)
                    if p in pts:
                        pts.remove(p); q.append(p); b.append(p)
        out.append(b)
    out.sort(key=lambda b: min(p[0] for p in b))
    return out

def census(path, label, x0, y0, x1, y1):
    im = Image.open(path).convert("L")
    print(f"===== component census {label} (thr sweep) =====")
    for thr in (200, 185, 170, 150):
        print(f"  thr<{thr}:")
        for b in comps(im, x0, y0, x1, y1, thr):
            xs = [p[0] for p in b]; ys = [p[1] for p in b]
            print(f"    x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} "
                  f"({max(xs)-min(xs)+1}x{max(ys)-min(ys)+1}) n={len(b)}")
    print()

heat(ORIG, 714, 136, 756, 158, "ORIGINAL right label (grayscale)")
heat(REND, 1489, 283, 1576, 330, "RENDER_10 right label (frame x714.7..754.1, y135.8..158.3)")
census(ORIG, "ORIGINAL right label", 714, 136, 756, 158)
census(ORIG, "ORIGINAL control '(2, 10)'", 616, 138, 662, 160)
