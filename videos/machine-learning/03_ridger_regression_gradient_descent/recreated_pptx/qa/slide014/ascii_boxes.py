#!/usr/bin/env python3
"""ASCII structural dump of the two vector boxes in the ORIGINAL, so the
delimiter/stack/color geometry can be read without a vision call.
One char per 3x3 px block; ink density + dominant color class per block."""
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
og = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)


def cls(R, G, B):
    if R > 242 and G > 242 and B > 242:
        return " "
    if abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 14:
        return " "
    if R > 150 and G < 115 and B < 115:
        return "R"      # red
    if B > 145 and R < 95 and G < 95:
        return "B"      # strong blue
    if G > 115 and R < 155 and B < 155:
        return "G"      # green
    if R < 135 and G < 135 and B < 135:
        return "#"      # black
    return "."          # other/dark


def dump(x0, x1, y0, y1, title, step=3):
    print(f"\n=== {title}  x {x0}..{x1} y {y0}..{y1} (1 char = {step}x{step}px) ===")
    hdr = "     " + "".join(str((x0 + i * step) // 10 % 10) for i in range((x1 - x0) // step))
    print(hdr)
    for y in range(y0, y1, step):
        chars = []
        for x in range(x0, x1, step):
            blk = og[y:y + step, x:x + step].reshape(-1, 3)
            cs = [cls(*p) for p in blk]
            nz = [c for c in cs if c != " "]
            if not nz:
                chars.append(" ")
                continue
            from collections import Counter
            cnt = Counter(nz)
            top, n = cnt.most_common(1)[0]
            density = len(nz) / len(cs)
            if top in "RGB":
                chars.append(top if density > 0.3 else top.lower())
            elif top == "#":
                chars.append("#" if density > 0.3 else "+")
            else:
                chars.append("." if density > 0.3 else ",")
        print(f"y={y:3d} " + "".join(chars))


dump(76, 440, 96, 240, "LEFT VECTOR BOX (x 79..435 border)")
dump(452, 818, 96, 240, "RIGHT VECTOR BOX (x 456..812 border)")
