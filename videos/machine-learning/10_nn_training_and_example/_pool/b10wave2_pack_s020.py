#!/usr/bin/env python3
"""Slide 020 visual comparison pack: render vs original, key regions upscaled."""
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 960 / 13.3333      # original px per inch
IN = 2001 / 13.3333    # render px per inch
OUT = f"{NS}/_pool/tmp_b10wave2"

O = Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("RGB")
R = Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("RGB")


def cut(im, sc, x0, y0, x1, y1, k=3):
    X0, Y0, X1, Y1 = (int(v * sc) for v in (x0, y0, x1, y1))
    c = im.crop((X0, Y0, X1, Y1))
    return c.resize((c.size[0] * k, c.size[1] * k), Image.LANCZOS)


regions = {
    "diagram":      (5.55, 0.60, 12.80, 3.30),
    "omega_mid1":   (0.60, 3.35, 7.60, 3.95),
    "omega_mid2":   (0.60, 4.25, 7.60, 5.05),
    "cream_panel":  (9.00, 3.25, 12.75, 6.80),
    "delta_box":    (0.75, 5.80, 6.20, 6.80),
    "where_strip":  (0.60, 6.65, 9.00, 7.45),
    "cyan_box":     (0.60, 0.60, 5.45, 3.30),
}
for nm, (x0, y0, x1, y1) in regions.items():
    cut(O, S, x0, y0, x1, y1).save(f"{OUT}/s020_orig_{nm}.png")
    cut(R, IN, x0, y0, x1, y1).save(f"{OUT}/s020_rend_{nm}.png")
    print(nm, "done")
