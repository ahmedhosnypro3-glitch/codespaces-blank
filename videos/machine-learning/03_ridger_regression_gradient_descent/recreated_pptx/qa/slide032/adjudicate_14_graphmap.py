#!/usr/bin/env python3
"""Slide 032 — colour-classified ASCII map of the original graph area + label glyphs."""
import os
from PIL import Image

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")

def classify(r, g, b):
    if r > 200 and g > 200 and b > 200:
        return "."
    if r > 120 and g < 110 and b < 110:      # dark red
        return "R"
    if r < 90 and g < 90 and b < 90:          # black
        return "K"
    if r < 170 and g < 170 and b < 170:        # gray
        return "g"
    if r < 235 and g < 235 and b < 235:
        return "+"
    return " "

def dump(path, x0, y0, x1, y1, label, step=2):
    im = Image.open(path).convert("RGB")
    print(f"--- {label}: {path}")
    print(f"    region x{x0}..{x1} y{y0}..{y1}, 1 char = {step}px")
    px = im.load()
    print("      " + "".join(str((x // step) % 10) for x in range(x0, x1, step)))
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            # sample the 2x2 block, take the "strongest" class present
            best = "."
            order = ". g+R+K"
            for dy in range(step):
                for dx in range(step):
                    c = classify(*px[x + dx, y + dy])
                    if order.index(c) > order.index(best):
                        best = c
            row += best
        print(f"{y:4d} {row}")
    print()

dump(ORIG, 560, 55, 830, 320, "ORIGINAL graph area", step=2)
dump(REND, 1166, 114, 1731, 667, "RENDER_10 graph area (frame*2.0833)", step=4)
