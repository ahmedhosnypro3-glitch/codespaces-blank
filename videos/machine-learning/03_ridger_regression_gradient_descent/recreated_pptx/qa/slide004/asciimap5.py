"""ASCII ink map + color samples — slide 004 top boxes."""
from PIL import Image
import numpy as np

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
o = Image.open(ORIG).convert("RGB")
a = np.asarray(o).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
red   = (R > 110) & (R - G > 55) & (R - B > 55)
blue  = (B > 100) & (B - R > 30) & (B - G > 15)
black = (R < 110) & (G < 110) & (B < 110) & ~(red | blue)


def ascii_map(x0, x1, y0, y1, sx=4, sy=2):
    print(f"map x{x0}..{x1} y{y0}..{y1}  (1 char = {sx}x{sy} px; R=red B=blue #=black)")
    hdr = "     " + "".join(str((x0 + i * sx) // 100 % 10) for i in range((x1 - x0) // sx + 1))
    print(hdr)
    for yy in range(y0, y1, sy):
        row = ""
        for xx in range(x0, x1, sx):
            cell_r = red[yy:yy+sy, xx:xx+sx].sum()
            cell_b = blue[yy:yy+sy, xx:xx+sx].sum()
            cell_k = black[yy:yy+sy, xx:xx+sx].sum()
            best = max(cell_r, cell_b, cell_k)
            if best == 0:
                row += "."
            elif best == cell_r and cell_r >= cell_b and cell_r >= cell_k:
                row += "R"
            elif best == cell_b:
                row += "B"
            else:
                row += "#"
        print(f"{yy:4d} {row}")


print("### LEFT BOX (Let Y) ###")
ascii_map(80, 396, 99, 224)
print()
print("### RIGHT BOX (Let Yhat) ###")
ascii_map(427, 746, 99, 224)
print()
print("### color samples ###")
for (x, y, tag) in [(172, 120, "L vert x166..179 y116"), (300, 145, "L red words y136..154"),
                    (220, 150, "L black band y145..176"), (160, 200, "L bottom red y192..203"),
                    (516, 120, "R vert x511..525"), (650, 143, "R blue y136..151"),
                    (520, 200, "R red y196..208"), (600, 165, "R black y146..182")]:
    print(f"  {tag}: ({x},{y}) = {tuple(a[y, x])}")
