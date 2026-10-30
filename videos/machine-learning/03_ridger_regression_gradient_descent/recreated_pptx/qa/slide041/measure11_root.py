#!/usr/bin/env python3
"""Slide 041 pass 11: shift-tolerant IoU classifier for the panel glyphs
(matrix digits, C-label glyphs, header subscripts) vs Liberation Sans.
Banks measurements11.json.
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
HERE = os.path.dirname(os.path.abspath(__file__))
a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
diff = (255 - R) + (247 - G) * 0.8 + (224 - B) * 0.6
loose = diff > 40

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def render(ch, size_pt):
    S = 4
    f = ImageFont.truetype(FONT, int(round(size_pt * S)))
    im = Image.new("L", (80 * S, 80 * S), 0)
    ImageDraw.Draw(im).text((15 * S, 15 * S), ch, fill=255, font=f)
    big = np.asarray(im)
    H2, W2 = big.shape[0] // S, big.shape[1] // S
    small = big[:H2 * S, :W2 * S].reshape(H2, S, W2, S).mean(axis=(1, 3))
    arr = small > 110
    ys, xs = np.where(arr)
    if not len(ys):
        return None
    return arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def best_iou(om, dm):
    # try shifts of dm within a padded canvas around om
    best = 0.0
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
            h = max(om.shape[0], dm.shape[0] + abs(dy)) + 1
            w = max(om.shape[1], dm.shape[1] + abs(dx)) + 1
            A = np.zeros((h, w), bool)
            Bm = np.zeros((h, w), bool)
            A[:om.shape[0], :om.shape[1]] = om
            y0 = max(0, dy)
            x0 = max(0, dx)
            Bm[y0:y0 + dm.shape[0], x0:x0 + dm.shape[1]] = dm
            inter = (A & Bm).sum()
            union = (A | Bm).sum()
            if union:
                best = max(best, inter / union)
    return best


def classify(x0, y0, x1, y1, chars, sizes):
    om = loose[y0:y1 + 1, x0:x1 + 1]
    scores = []
    for ch in chars:
        for s in sizes:
            dm = render(ch, s)
            if dm is None:
                continue
            scores.append((round(best_iou(om, dm), 3), ch, s))
    scores.sort(reverse=True)
    return scores[:4]


LET = "0123456789CSGceasz"
out = {}
targets = {
    "clabel_1": (89, 112, 103, 125),
    "clabel_4": (159, 112, 173, 125),
    "r1c1": (94, 79, 100, 89),
    "r1c2": (114, 79, 122, 88),
    "r1c3": (135, 79, 141, 89),
    "r1c4": (159, 79, 167, 88),
    "r1c5": (182, 79, 190, 89),
    "r1c6": (203, 79, 214, 89),
    "r2c1": (94, 95, 100, 105),
    "r2c2": (114, 95, 122, 105),
    "r2c3": (137, 95, 146, 105),
    "r2c4": (159, 95, 168, 105),
    "r2c5": (182, 95, 191, 105),
    "r2c6": (203, 95, 214, 105),
    "r3c1": (89, 110, 104, 126),
    "hdrsub_1": (99, 68, 102, 74),
    "hdrsub_2": (119, 68, 124, 74),
    "hdrsub_3": (143, 68, 147, 74),
    "hdrsub_4": (164, 68, 170, 74),
    "hdrsub_5": (187, 67, 193, 73),
    "hdrsub_6": (202, 67, 216, 75),
}
for name, bb in targets.items():
    out[name] = {"bbox": bb, "top": classify(*bb, LET, [8, 9, 10, 11, 12, 13, 14])}
with open(os.path.join(HERE, "measurements11.json"), "w") as f:
    json.dump(out, f, indent=1)
for k, v in out.items():
    print(k, v["top"])
