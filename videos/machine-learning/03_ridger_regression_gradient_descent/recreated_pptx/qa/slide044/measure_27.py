#!/usr/bin/env python3
"""Per-x ink y-runs for both tables -> definitive cell/digit layout."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
dark = LUM < 185


def yruns(y0, y1, x0, x1, label):
    print(f"=== {label} ===")
    for x in range(x0, x1):
        ys = np.where(dark[y0:y1 + 1, x])[0]
        if not len(ys):
            continue
        runs = []; s = ys[0]; p = ys[0]
        for i in ys[1:]:
            if i - p <= 2: p = i
            else:
                runs.append((s, p)); s = i; p = i
        runs.append((s, p))
        big = [(y0 + a, y0 + b) for a, b in runs if b - a >= 2]
        if big:
            print(f"  x{x}: " + " ".join(f"y{a}-{b}" for a, b in big))


yruns(58, 132, 88, 226, "T1 (top-left) x88..226 y58..132")
print()
yruns(138, 256, 86, 224, "T2 (left-mid) x86..224 y138..256")
