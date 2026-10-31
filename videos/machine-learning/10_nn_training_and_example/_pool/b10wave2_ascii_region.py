#!/usr/bin/env python3
"""High-res ASCII read of slide 020 original regions (video frame, 960x540)."""
import sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 960 / 13.3333


def art(im, sc, x0, y0, x1, y1, nc=175, aspect=0.5):
    X0, Y0, X1, Y1 = (int(v * sc) for v in (x0, y0, x1, y1))
    c = im.crop((X0, Y0, X1, Y1))
    w, h = c.size
    nc = min(nc, w)
    nr = max(1, int(h * (nc / w) * aspect))
    c = c.resize((nc, nr), Image.LANCZOS)
    a = np.array(c)
    chars = " .:-=+*#%@"
    return "\n".join("".join(chars[min(9, int((255 - v) / 25.6))] for v in row)
                     for row in a)


O = Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")
R = Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("L")
IN = 2001 / 13.3333

REG = {
    "cream":  (9.00, 3.25, 12.75, 6.80),
    "cyan":   (0.60, 0.60, 5.45, 3.30),
    "where":  (0.60, 6.60, 9.05, 7.45),
    "delta":  (0.75, 5.80, 6.20, 6.82),
}
for nm in sys.argv[1:]:
    x0, y0, x1, y1 = REG[nm]
    print(f"\n########## ORIG {nm} ##########")
    print(art(O, S, x0, y0, x1, y1))
    print(f"\n########## REND {nm} ##########")
    print(art(R, IN, x0, y0, x1, y1))
