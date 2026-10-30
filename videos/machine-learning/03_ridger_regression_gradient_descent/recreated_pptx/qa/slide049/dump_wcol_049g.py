#!/usr/bin/env python3
"""ASCII dump of the bracket region for original and render."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049"
SX = 68.0 / 142.0
SY = 395.0 / 823.0


def dump(name, thr, fy0, fy1, fx0, fx1, label):
    a = np.asarray(Image.open(f"{QA}/{name}").convert("L"))
    print(f"\n=== {label} {name} thr{thr} frame x{fx0}..{fx1} y{fy0}..{fy1} ===")
    cy0 = int(round((fy0 - 135) / SY))
    cy1 = int(round((fy1 - 135) / SY))
    cx0 = int(round((fx0 - 692) / SX))
    cx1 = int(round((fx1 - 692) / SX))
    band = a[cy0:cy1, cx0:cx1]
    print("     " + "".join(f"{int(692 + (cx0+j)*SX)%10}" for j in range(band.shape[1])))
    for i in range(band.shape[0]):
        fy = 135 + (cy0 + i) * SY
        row = "".join("#" if band[i, j] < thr else ("+" if band[i, j] < thr + 30 else ".") for j in range(band.shape[1]))
        print(f"{fy:6.1f} {row}")


dump("crop_9_wstack_orig.png", 205, 143, 200, 718, 750, "ORIG")
dump("crop_9_wstack_render.png", 150, 143, 200, 718, 750, "RENDER")
