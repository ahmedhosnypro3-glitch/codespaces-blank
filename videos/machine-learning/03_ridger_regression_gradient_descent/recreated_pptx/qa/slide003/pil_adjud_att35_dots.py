#!/usr/bin/env python3
"""att35 topbox MAJOR adjudication: middle ellipsis-column dot-group count, PIL-first.
Judge claim (crop_35_topbox_judge.txt): orig 4 stacked dot groups (crop y~125,185,245,300)
vs render 3 (y~145,225,300). Crop->slide: /2.0833 +105 (y), /2.0844 +266 (x).
Middle-col delimiters at orig x~451/475 (att34 sweep); probe the INTERIOR x455..471
plus a wide context map x430..500 (delimiters appear as tall comps there)."""
from collections import deque
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = D + "/recreated_pptx/qa/slide003"
SX, SY = 2001 / 960.0, 1125 / 540.0


def comps(mask):
    H, W = mask.shape
    lab = np.zeros((H, W), int)
    cur = 0
    for i in range(H):
        for j in range(W):
            if mask[i, j] and lab[i, j] == 0:
                cur += 1
                q = deque([(i, j)])
                lab[i, j] = cur
                while q:
                    y, x = q.popleft()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = cur
                                q.append((ny, nx))
    return lab, cur


def report(img_path, x0, y0, x1, y1, th, tag, ascii_map=False):
    im = np.asarray(Image.open(img_path).convert("L"), dtype=np.uint8)
    reg = im[y0:y1, x0:x1]
    mask = reg < th
    lab, n = comps(mask)
    print("== %s  x%d..%d y%d..%d th%d  ink=%d comps=%d" % (tag, x0, x1, y0, y1, th, mask.sum(), n))
    boxes = []
    for c in range(1, n + 1):
        ys, xs = np.nonzero(lab == c)
        boxes.append((int(xs.min()) + x0, int(xs.max()) + x0, int(ys.min()) + y0, int(ys.max()) + y0, int(len(ys))))
    for b in sorted(boxes, key=lambda b: (b[2], b[0])):
        print("   comp x%d..%d y%d..%d npx=%d" % b)
    if ascii_map:
        H, W = mask.shape
        step = max(1, H // 60)
        print("   ascii (rows=y//%d, cols=x//%d, '#'=ink):" % (step, step))
        for i in range(0, H, step):
            row = "".join("#" if mask[i:i + step, j:j + step].any() else "." for j in range(0, W, step))
            print("   y%4d %s" % (y0 + i, row))


O = D + "/unique_slides/slide_003.jpg"
R = Q + "/render_35.png"
# ORIG: wide context (includes delimiters) then interior-only
report(O, 430, 108, 500, 270, 150, "ORIG wide", ascii_map=True)
report(O, 455, 143, 471, 263, 150, "ORIG interior")
report(O, 455, 143, 471, 263, 170, "ORIG interior th170")
# RENDER: same slide-space boxes scaled
report(R, int(430 * SX), int(108 * SY), int(500 * SX), int(270 * SY), 150, "RENDER wide", ascii_map=True)
report(R, int(455 * SX), int(143 * SY), int(471 * SX), int(263 * SY), 150, "RENDER interior")
report(R, int(455 * SX), int(143 * SY), int(471 * SX), int(263 * SY), 120, "RENDER interior th120")
