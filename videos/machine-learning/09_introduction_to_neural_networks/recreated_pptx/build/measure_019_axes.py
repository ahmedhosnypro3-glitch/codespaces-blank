#!/usr/bin/env python3
"""Measure axis lines / tick labels in ORIGINAL and in the CURRENT render.

original: unique_slides/slide_019.jpg 960x540  (1px = 1pt)
render:   2001x1125 @150dpi             (1px render = 0.48pt -> scale 0.47976)
"""
import os
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
V = os.path.join(ROOT, "videos/machine-learning/09_introduction_to_neural_networks")
B = os.path.join(V, "recreated_pptx", "build")

# original panel border boxes, measured (blue-purple border ink)
PANELS = {
    "sigmoid": (104, 59, 410, 237),
    "tanh":    (499, 59, 790, 237),
    "tan":     (105, 297, 410, 476),
    "arctan":  (499, 297, 790, 476),
}


def analyze(img, scale, label, panels):
    px = img.load()
    print(f"\n########## {label}  {img.size} scale={scale}")
    for key, (bx0, by0, bx1, by1) in panels.items():
        x0, y0, x1, y1 = (int(round(bx0 / scale)), int(round(by0 / scale)),
                          int(round(bx1 / scale)), int(round(by1 / scale)))
        W, H = img.size
        x1, y1 = min(x1, W - 1), min(y1, H - 1)
        # axis gray ~ (140,140,140); tick text gray/dark
        gray = []
        dark = []
        for y in range(y0 + 3, y1 - 2):
            for x in range(x0 + 3, x1 - 2):
                r, g, b = px[x, y]
                if abs(r - 140) < 26 and abs(g - 140) < 26 and abs(b - 140) < 26:
                    gray.append((x, y))
                if r < 110 and g < 110 and b < 110:
                    dark.append((x, y))
        ng, nd = len(gray), len(dark)
        # long horizontal gray run (axis line) and long vertical gray run
        hrun = 0
        if gray:
            rows = {}
            for x, y in gray:
                rows.setdefault(y, []).append(x)
            for y, xs in rows.items():
                xs.sort()
                run = best = 1
                for a, b2 in zip(xs, xs[1:]):
                    run = run + 1 if b2 - a <= 2 else 1
                    best = max(best, run)
                hrun = max(hrun, best)
        vrun = 0
        if gray:
            cols = {}
            for x, y in gray:
                cols.setdefault(x, []).append(y)
            for x, ys in cols.items():
                ys.sort()
                run = best = 1
                for a, b2 in zip(ys, ys[1:]):
                    run = run + 1 if b2 - a <= 2 else 1
                    best = max(best, run)
                vrun = max(vrun, best)
        # dark text bbox (tick labels / titles)
        if dark:
            db = (min(p[0] for p in dark), min(p[1] for p in dark),
                  max(p[0] for p in dark), max(p[1] for p in dark))
            dbpt = (round(db[0] * scale, 1), round(db[1] * scale, 1),
                    round(db[2] * scale, 1), round(db[3] * scale, 1))
        else:
            dbpt = None
        print(f"{key:8s} panel_pt=({round(x0*scale,1)},{round(y0*scale,1)},"
              f"{round(x1*scale,1)},{round(y1*scale,1)}) "
              f"graypx={ng} darkpx={nd} grayHmax={hrun} grayVmax={vrun} darkbbox_pt={dbpt}")


orig = Image.open(os.path.join(V, "unique_slides/slide_019.jpg")).convert("RGB")
analyze(orig, 1.0, "ORIGINAL", PANELS)

for name in ("slide_019_rendered-1.png", "slide_019_rejudge_rendered-1.png"):
    p = os.path.join(B, name)
    if os.path.exists(p):
        rend = Image.open(p).convert("RGB")
        analyze(rend, 960.0 / rend.size[0], "RENDER " + name, PANELS)
