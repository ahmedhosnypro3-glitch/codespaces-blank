#!/usr/bin/env python3
"""ASCII-render slide 020 equation PNG assets so their content can be read
without an image call."""
import sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def ascii_art(path, nc=170):
    im = Image.open(path).convert("L")
    w, h = im.size
    nr = max(1, int(h * (nc / w) * 0.5))
    small = im.resize((nc, nr), Image.LANCZOS)
    a = np.array(small)
    chars = " .:-=+*#%@"
    return "\n".join(
        "".join(chars[min(9, int((255 - v) / 25.6))] for v in row) for row in a
    )


for f in sys.argv[1:]:
    p = f"{NS}/recreated_pptx/build/eq_slide_020/{f}"
    print(f"\n===== {f} =====")
    print(ascii_art(p))
