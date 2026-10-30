#!/usr/bin/env python3
"""Block-averaged ASCII view of a region: text legible, layout clear."""
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


def block_ascii(a, win, bx=3, by=3):
    x0, y0, x1, y1 = win
    chars = []
    for y in range(y0, y1, by):
        row = []
        for x in range(x0, x1, bx):
            px = a[y:y + by, x:x + bx].reshape(-1, 3).mean(axis=0)
            s = px.sum()
            r, g, b = px
            if s > 730:
                row.append(" ")
            elif r > 165 and g < 115 and b < 115:
                row.append("R")
            elif b > 165 and r < 115 and g < 145:
                row.append("B")
            elif r > 205 and g > 205 and b < 195:
                row.append("Y")
            elif abs(r - g) < 28 and abs(g - b) < 28 and 85 < r < 205:
                row.append("g")
            elif r > g + 25 and b > g + 25:
                row.append("P")
            elif g > 205 and b > 205 and r < 215:
                row.append("C")
            else:
                row.append("#")
        chars.append("".join(row))
    return chars


if __name__ == "__main__":
    win = tuple(int(v) for v in sys.argv[1:5])
    label = sys.argv[5] if len(sys.argv) > 5 else ""
    bx = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    by = int(sys.argv[7]) if len(sys.argv) > 7 else 3
    a, r = load()
    ao = block_ascii(a, win, bx, by)
    ar = block_ascii(r, win, bx, by)
    w = len(ao[0])
    print(f"=== {label} win={win} bx={bx} by={by} ===")
    print(f"{'ORIGINAL':<{w+3}}| RENDER")
    print("-" * (w + 3) + "+" + "-" * len(ar[0]))
    for i in range(max(len(ao), len(ar))):
        lo = ao[i] if i < len(ao) else ""
        lr = ar[i] if i < len(ar) else ""
        print(f"{lo:<{w+3}}| {lr}")
    print()
