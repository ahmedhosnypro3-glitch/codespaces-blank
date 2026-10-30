#!/usr/bin/env python3
"""Slide 019 — cut the four panel label bands out of the original for one
batch vision read (crops, not the full frame, so 6pt text is legible)."""
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/crops_019"

CROPS = {
    # name: frame box (x0, y0, x1, y1) in ORIGINAL 960x540 px
    "A_sigmoid_topleft":  (104, 56, 265, 122),
    "B_tanh_topleft":     (497, 56, 660, 122),
    "C_arctan_topleft":   (497, 296, 725, 334),
    "D_tan_topleft":      (104, 294, 330, 356),
    "E_sigmoid_legend":   (115, 70, 200, 92),
}

if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(ORIG).convert("RGB")
    for name, box in CROPS.items():
        c = im.crop(box)
        # 4x upscale with LANCZOS so ~6pt glyphs are legible to the model
        c = c.resize((c.size[0] * 4, c.size[1] * 4), Image.LANCZOS)
        p = f"{OUT}/{name}.png"
        c.save(p)
        print(f"{p}  {c.size}")
