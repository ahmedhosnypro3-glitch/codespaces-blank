# 1px-resolution colour map of the "(5,1)" label neighbourhood in ORIGINAL vs CURRENT
# render, so the label's glyph shapes AND colours can be read without guessing.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
SX = 2001 / 960.0


def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r > 120 and g < 90 and b < 90:
        return "R"          # saturated red
    if g > r + 25 and g > b + 25:
        return "G"          # saturated green
    if b > r + 30 and b > g + 30:
        return "B"          # saturated blue
    if g > r + 8 and g > b + 8:
        return "g"          # weak green
    if r > g + 25 and r > b + 25:
        return "r"          # weak red
    mx = max(r, g, b)
    if mx < 110:
        return "#"
    if mx < 170:
        return "%"
    if mx < 215:
        return "*"
    if mx < 240:
        return ":"
    return "."


def dump(tag, a, x0, x1, y0, y1, sc):
    print("--- %s  frame x %d..%d  y %d..%d ---" % (tag, x0, x1, y0, y1))
    print("    " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("    " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        yy = int(round(y * sc))
        print("%3d " % y + "".join(cls(a[yy, int(round(x * sc))]) for x in range(x0, x1)))


dump("ORIGINAL", O, 488, 560, 246, 264, 1.0)
dump("RENDER", R, 488, 560, 246, 264, SX)
