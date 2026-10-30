#!/usr/bin/env python3
"""ASCII-art dump of a region of both images for direct comparison."""
import numpy as np
from PIL import Image
import sys

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")


def load():
    o = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
    r = Image.open(B + "/recreated_pptx/qa/slide003/render_9.png").convert(
        "RGB").resize((960, 540), Image.LANCZOS)
    return np.asarray(o).astype(int), np.asarray(r).astype(int)


def render_ascii(a, win, sx=2, sy=2):
    x0, y0, x1, y1 = win
    # colour chars
    out = []
    for y in range(y0, y1, sy):
        row = []
        for x in range(x0, x1, sx):
            px = a[y, x]
            s = px.sum()
            r, g, b = px
            if s > 700:
                row.append(".")
            elif r > 150 and g < 110 and b < 110:
                row.append("R")       # red
            elif b > 150 and r < 110 and g < 140:
                row.append("B")       # blue
            elif r > 200 and g > 200 and b < 200:
                row.append("Y")       # yellow
            elif abs(r - g) < 30 and abs(g - b) < 30 and 90 < r < 200:
                row.append("g")       # gray
            elif r > g + 20 and b > g + 20:
                row.append("P")       # pink/magenta
            elif g > 200 and b > 200 and r < 210:
                row.append("C")       # cyan
            else:
                row.append("#")
        out.append("".join(row))
    return out


if __name__ == "__main__":
    win = tuple(int(v) for v in sys.argv[1:5])
    label = sys.argv[5] if len(sys.argv) > 5 else ""
    a, r = load()
    print(f"=== {label} win={win}  (ORIG left / RENDER right) ===")
    ao = render_ascii(a, win)
    ar = render_ascii(r, win)
    print(f"{'ORIGINAL':<{len(ao[0])+2}} RENDER")
    for i in range(max(len(ao), len(ar))):
        lo = ao[i] if i < len(ao) else ""
        lr = ar[i] if i < len(ar) else ""
        print(f"{lo:<{len(ao[0])+2}} {lr}")
    print()
