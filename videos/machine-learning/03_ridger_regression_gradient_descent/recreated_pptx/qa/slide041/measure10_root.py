#!/usr/bin/env python3
"""Slide 041 pass 10: identify matrix digits/subscripts by IoU-matching
bitmaps against Liberation Sans (Arial-metric-compatible) renderings.
Banks measurements10.json.
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
HERE = os.path.dirname(os.path.abspath(__file__))
a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 170) & (G < 170) & (B < 170)

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def render_digit(ch, size_pt):
    # render at 4x supersample, box-downsample to 1x, then threshold
    S = 4
    f = ImageFont.truetype(FONT, int(size_pt * S))
    im = Image.new("L", (60 * S, 60 * S), 0)
    d = ImageDraw.Draw(im)
    d.text((10 * S, 10 * S), ch, fill=255, font=f)
    big = np.asarray(im)
    H2, W2 = big.shape[0] // S, big.shape[1] // S
    small = big[:H2 * S, :W2 * S].reshape(H2, S, W2, S).mean(axis=(1, 3))
    arr = small > 110
    ys, xs = np.where(arr)
    if not len(ys):
        return None
    return arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def orig_bitmap(x0, y0, x1, y1, pad=1):
    m = dark[y0:y1 + 1, x0:x1 + 1]
    m = np.pad(m, pad)
    return m


def iou(m1, m2):
    h = max(m1.shape[0], m2.shape[0])
    w = max(m1.shape[1], m2.shape[1])
    A = np.zeros((h, w), bool)
    Bm = np.zeros((h, w), bool)
    A[:m1.shape[0], :m1.shape[1]] = m1
    Bm[:m2.shape[0], :m2.shape[1]] = m2
    inter = (A & Bm).sum()
    union = (A | Bm).sum()
    return inter / union if union else 0.0


targets = [
    # (name, bbox, candidate sizes)
    ("sub_1_x93", (100, 69, 101, 73), [6, 7, 8]),
    ("sub_2_x116", (120, 69, 123, 73), [6, 7, 8]),
    ("sub_3_x137", (144, 70, 146, 73), [6, 7, 8]),
    ("sub_4_x158", (165, 69, 169, 73), [6, 7, 8]),
    ("sub_5_x181", (185, 68, 191, 71), [6, 7, 8]),
    ("sub_6_x206", (203, 68, 214, 74), [6, 7, 8]),
    ("r1c1", (95, 79, 99, 89), [12, 13, 14]),
    ("r1c2", (115, 79, 121, 87), [12, 13, 14]),
    ("r1c3", (139, 79, 144, 89), [12, 13, 14]),
    ("r1c4", (160, 79, 166, 88), [12, 13, 14]),
    ("r1c5", (183, 79, 189, 89), [12, 13, 14]),
    ("r1c6", (205, 79, 212, 89), [12, 13, 14]),
    ("r2c1", (95, 95, 98, 105), [12, 13, 14]),
    ("r2c2", (116, 95, 120, 105), [12, 13, 14]),
    ("r2c3", (138, 95, 144, 105), [12, 13, 14]),
    ("r2c4", (160, 95, 166, 105), [12, 13, 14]),
    ("r2c5", (183, 95, 189, 105), [12, 13, 14]),
    ("r2c6", (205, 95, 211, 105), [12, 13, 14]),
]

out = {}
for name, bb, sizes in targets:
    om = orig_bitmap(*bb)
    scores = []
    for ch in "0123456789":
        for s in sizes:
            dm = render_digit(ch, s)
            if dm is None:
                continue
            scores.append((iou(om, dm), ch, s, dm.shape))
    scores.sort(reverse=True)
    out[name] = {"bbox": bb, "top3": [(round(sc[0], 3), sc[1], sc[2], list(sc[3])) for sc in scores[:3]]}

with open(os.path.join(HERE, "measurements10.json"), "w") as f:
    json.dump(out, f, indent=1)
for k, v in out.items():
    print(k, v["bbox"], "->", v["top3"])
