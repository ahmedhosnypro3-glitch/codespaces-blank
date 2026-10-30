"""Fine per-pixel map of the left box equation region + full ink inventory."""
from PIL import Image
import numpy as np

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
o = Image.open(ORIG).convert("RGB")
a = np.asarray(o).astype(int)

# background = near-white panel inside box
bg = 250
dark = (a[..., 0] < bg) | (a[..., 1] < bg) | (a[..., 2] < bg)

X0, X1, Y0, Y1 = 155, 260, 108, 212
print(f"### left-box region x{X0}..{X1} y{Y0}..{Y1}; '.' = white, else class ###")
print("cls: R=red r=light-red B=blue #=dark(other)")
hdr = "     " + "".join(str((X0 + i) // 10 % 10) for i in range(X1 - X0))
print(hdr)
for yy in range(Y0, Y1):
    row = ""
    for xx in range(X0, X1):
        px = a[yy, xx]
        if not dark[yy, xx]:
            row += "."
            continue
        R, G, B = px
        if R - G > 40 and R - B > 40:
            row += "R" if R < 210 else "r"
        elif B - R > 30:
            row += "B"
        else:
            row += "#" if (R < 170) else "g"
    print(f"{yy:4d} {row}")
