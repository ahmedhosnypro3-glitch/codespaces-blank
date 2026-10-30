#!/usr/bin/env python3
"""Make upscaled crops of slide_013 original for dense-region vision reads."""
import os
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
src = Image.open(f"{V}/unique_slides/slide_013.jpg").convert("RGB")
out = f"{V}/recreated_pptx/qa/slide013"
os.makedirs(out, exist_ok=True)

CROPS = {
    "crop_orig_title_table.png": ((0, 30, 345, 320), 2.4),
    "crop_orig_plot.png": ((520, 95, 870, 385), 2.4),
    "crop_orig_perceptron.png": ((130, 340, 545, 510), 2.6),
    "crop_orig_callout.png": ((560, 395, 910, 515), 2.6),
}
for name, (box, scale) in CROPS.items():
    c = src.crop(box)
    w, h = c.size
    c = c.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    c.save(f"{out}/{name}")
    print(f"{name}: box={box} -> {c.size}")
