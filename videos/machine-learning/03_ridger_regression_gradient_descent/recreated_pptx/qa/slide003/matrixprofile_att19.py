#!/usr/bin/env python3
"""Row-band + cell ink profiles for the bottom design matrix (slide 003).

Frame space 960x540. Design-matrix column x-centres come from the CURRENT pptx
shape geometry (96dpi EMU / 9525 * 0.75), so the windows track the real
columns. Prints, per y-band, the dark-ink count inside each of the 4 matrix
columns, for the original and the render, so a missing cell shows as a zero
column at the row where the other rows have ink.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"
COLS = [181.5, 225.75, 270.0, 313.5]
CW = 39.75


def ld(p):
    return (np.asarray(Image.open(p).convert("RGB")
                       .resize((960, 540), Image.LANCZOS)).astype(int))


def dark(a):
    return (np.minimum(np.minimum(a[:, :, 0], a[:, :, 1]), a[:, :, 2]) < 100)


def profile(img, y0, y1, step=3, tag=""):
    d = dark(img)
    print(f"{tag} y-profile: dark px per {step}px band, per matrix column")
    print("   y   c1   c2   c3   c4")
    for y in range(y0, y1, step):
        counts = [int(d[y:y + step, int(x):int(x) + int(CW)].sum()) for x in COLS]
        print(f"{y:4d} " + "".join(f"{c:4d} " for c in counts))


if __name__ == "__main__":
    o = ld(B + "/unique_slides/slide_003.jpg")
    profile(o, 355, 500, 3, "ORIG      ")
    print()
    r = ld(QA + "/render_19.png")
    profile(r, 355, 500, 3, "RENDER_19 ")
