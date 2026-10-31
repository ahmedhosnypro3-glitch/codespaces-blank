#!/usr/bin/env python3
"""Slide 020 where-strip crop comparison: dump both sides at 2x for visual read."""
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 960 / 13.3333
IN = 2001 / 13.3333

O = Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")
R = Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("L")

# left half and right half of the where strip, upscaled 3x
for tag, im, sc in (("orig", O, S), ("rend", R, IN)):
    for nm, (x0, x1) in (("L", (0.6, 4.9)), ("R", (4.9, 9.1))):
        X0, X1 = int(x0 * sc), int(x1 * sc)
        Y0, Y1 = int(6.70 * sc), int(7.42 * sc)
        c = im.crop((X0, Y0, X1, Y1))
        c = c.resize((c.size[0] * 3, c.size[1] * 3), Image.LANCZOS)
        c.save(f"{NS}/_pool/tmp_b10wave2/where_{tag}_{nm}.png")
        print(tag, nm, c.size)
