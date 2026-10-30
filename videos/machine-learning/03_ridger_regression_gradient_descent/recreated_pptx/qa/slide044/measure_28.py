#!/usr/bin/env python3
"""Per-cell digit geometry for both tables: bbox width/height/ink identify digits."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
dark = LUM < 190

# cell x-parens measured: col k spans [pl, pr] with digit centred
T1_CELLS = [(90, 107), (111, 125), (133, 147), (156, 170), (179, 193), (201, 215)]
T2_CELLS = [(93, 107), (114, 128), (137, 151), (159, 174), (182, 196), (204, 218)]
T1_ROWS = [(78, 90), (94, 107)]
T2_ROWS = [(164, 177), (182, 194), (197, 209), (212, 224)]


def cells(label, cellx, rows):
    print(f"=== {label} ===")
    for ri, (y0, y1) in enumerate(rows):
        out = []
        for ci, (x0, x1) in enumerate(cellx):
            # digit zone = cell minus 4px paren margins
            sub = dark[y0:y1 + 1, x0 + 4:x1 - 3]
            ys, xs = np.where(sub)
            if not len(ys):
                out.append(f"c{ci+1}:EMPTY")
                continue
            w = int(xs.max() - xs.min() + 1)
            h = int(ys.max() - ys.min() + 1)
            out.append(f"c{ci+1}:x{x0+4+int(xs.min())}-{x0+4+int(xs.max())} w{w} h{h} px={int(sub.sum())}")
        print(f"  row{ri+1} y{y0}-{y1}: " + " | ".join(out))


cells("T1 (top-left)", T1_CELLS, T1_ROWS)
print()
cells("T2 (left-mid)", T2_CELLS, T2_ROWS)
