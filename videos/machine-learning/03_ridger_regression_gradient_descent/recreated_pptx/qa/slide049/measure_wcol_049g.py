#!/usr/bin/env python3
"""Connected-component measurement of the W result column, original vs render.

crop_9_wstack_*.png = frame bbox x692..760, y135..530, scaled to 142x823.
Frame px = 692 + crop_x * 68/142 ; y = 135 + crop_y * 395/823.
"""
import sys
from PIL import Image
import numpy as np

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049"
SX = 68.0 / 142.0
SY = 395.0 / 823.0
ROWS = [(140, 205), (205, 271), (271, 337), (337, 403), (403, 469), (469, 527)]


def cc(mask):
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    cur = 0
    stack = []
    comps = []
    for y in range(h):
        for x in range(w):
            if mask[y, x] and lab[y, x] == 0:
                cur += 1
                stack.append((y, x))
                lab[y, x] = cur
                x0, x1, y0, y1 = x, x, y, y
                while stack:
                    cy, cx = stack.pop()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = cur
                                stack.append((ny, nx))
                                x0 = min(x0, nx); x1 = max(x1, nx)
                                y0 = min(y0, ny); y1 = max(y1, ny)
                comps.append((x0, y0, x1, y1, (x1 - x0 + 1), (y1 - y0 + 1)))
    return comps


def analyse(name, thr):
    im = Image.open(f"{QA}/{name}").convert("L")
    a = np.asarray(im)
    print(f"\n=== {name} thr={thr} ===")
    for ri, (fy0, fy1) in enumerate(ROWS, 1):
        cy0 = int(round((fy0 - 135) / SY))
        cy1 = int(round((fy1 - 135) / SY))
        band = a[cy0:cy1]
        mask = band < thr
        comps = [c for c in cc(mask) if c[4] >= 1 and c[5] >= 1]
        # frame coords
        items = []
        for (x0, y0, x1, y1, w, h) in comps:
            fx0 = 692 + x0 * SX
            fx1 = 692 + x1 * SX
            fy0p = 135 + (cy0 + y0) * SY
            fy1p = 135 + (cy0 + y1) * SY
            items.append((fx0, fy0p, fx1, fy1p, w, h))
        items.sort()
        print(f" row{ri}: ", end="")
        for it in items:
            print(f"[{it[0]:.1f}..{it[2]:.1f} y{it[1]:.1f}..{it[3]:.1f} w{it[4]} h{it[5]}] ", end="")
        print()


analyse("crop_9_wstack_orig.png", 205)
analyse("crop_9_wstack_render.png", 150)
