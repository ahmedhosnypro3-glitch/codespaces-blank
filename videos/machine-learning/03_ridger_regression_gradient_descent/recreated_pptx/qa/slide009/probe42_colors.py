#!/usr/bin/env python3
"""Probe 42: exact color cores — annotation-box border, caption red keyword,
caption black remainder, blue fitted line, orange point fill, grid line.
"""
import numpy as np
from PIL import Image
from collections import Counter

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def top(name, region, k=6):
    sub = a[region[1]:region[3]+1, region[0]:region[2]+1].reshape(-1, 3)
    c = Counter(map(tuple, sub))
    print(f"  {name}: {c.most_common(k)}")

print("=== annotation box border cores ===")
top("L box left border x216..217 y150..172", (216, 150, 217, 172))
top("L box right border x316..317 y150..172", (316, 150, 317, 172))
top("L box top border y147..148 x230..300", (230, 147, 300, 148))
top("L box bottom border y174..175 x230..300", (230, 174, 300, 175))
top("L box interior x240..290 y155..165", (240, 155, 290, 165))

print("=== caption colors ===")
top("LCAP1 red 'Overfit' x109..160 y490..500", (109, 490, 160, 500))
top("LCAP1 black x162..419 y490..503", (162, 490, 419, 503))
top("LCAP2 'Fails...' x179..349 y508..520", (179, 508, 349, 520))
top("RCAP1 red 'Generalized' x523..610 y490..500", (523, 490, 610, 500))
top("RCAP1 black x607..819 y490..503", (607, 490, 819, 503))
top("RCAP2 x502..774 y508..526", (502, 508, 774, 526))

print("=== chart ink colors ===")
top("blue fitted line LEFT x260..262 y286..290", (260, 286, 262, 290))
top("orange point (260.5,333)", (257, 330, 264, 336))
top("grid line LEFT row y120..121 x200..300", (200, 120, 300, 121))
top("grid col LEFT x103..104 y200..300", (103, 200, 104, 300))
top("red y-axis LEFT x125..127 y300..400", (125, 300, 127, 400))
top("red x-axis LEFT y433..435 x300..400", (300, 433, 400, 435))
