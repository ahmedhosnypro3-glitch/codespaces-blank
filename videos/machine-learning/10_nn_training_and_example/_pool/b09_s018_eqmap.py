#!/usr/bin/env python3
"""b09 s018: fine ASCII ink maps of the original's equation + label regions."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
o = np.asarray(Image.open(NS + "unique_slides/slide_018.jpg").convert("RGB")).astype(np.int16)
os_ = o.sum(2)

def ascii_map(reg, thr=420, step=3, title=""):
    x0, y0, x1, y1 = reg
    print(f"\n== {title} ({x0},{y0})-({x1},{y1}) thr={thr} ==")
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            row += "#" if os_[y, x] < thr else ("+" if os_[y, x] < 700 else ".")
        print(f"{y:4d} {row}")

ascii_map((820, 80, 910, 180), 420, 4, "ORIGINAL equation zone")
ascii_map((350, 180, 420, 210), 420, 2, "ORIGINAL input-label zone")
ascii_map((355, 178, 500, 215), 420, 2, "ORIGINAL bottom strip left")
