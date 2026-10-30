# Compare the annotation-box borders between ORIGINAL and CURRENT render, and
# locate every long vertical line in the y 230..320 band of the render.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
S = 2001 / 960.0


def scan(tag, a, sc, green, red, dark):
    print("=== %s : vertical lines in y 230..320 ===" % tag)
    for fx in range(540, 830):
        x = int(round(fx * sc))
        gy = np.nonzero(green[max(0, int(230 * sc)):int(320 * sc), x])[0]
        ry = np.nonzero(red[max(0, int(230 * sc)):int(320 * sc), x])[0]
        dy = np.nonzero(dark[max(0, int(230 * sc)):int(320 * sc), x])[0]
        tot = len(gy) + len(ry) + len(dy)
        if tot >= 20:
            g = "%d" % (gy.min() / sc + 230) if len(gy) else "-"
            r = "%d" % (ry.min() / sc + 230) if len(ry) else "-"
            d = "%d" % (dy.min() / sc + 230) if len(dy) else "-"
            print("   frame x%3d  green %d rows [%s..%s]  red %d [%s..%s]  dark %d [%s..%s]"
                  % (fx, len(gy), g, "?", len(ry), r, len(dy), d) if False else
                  "   frame x%3d  green n=%d [%s]  red n=%d [%s]  dark n=%d [%s]"
                  % (fx, len(gy), g, len(ry), r, len(dy), d))
    print()


def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    v = a.max(axis=2)
    return ((g > r + 18) & (g > b + 18) & (g < 210),
            (r > 90) & ((r - g) > 35) & ((r - b) > 8),
            v < 150)


og, ore, od = masks(O)
rg, rr, rd = masks(R)
scan("ORIGINAL", O, 1.0, og, ore, od)
scan("RENDER", R, S, rg, rr, rd)

print("=== ORIGINAL annotation box corner pixels ===")
for (x, y) in [(243, 244), (245, 250), (250, 300), (560, 260), (565, 260), (566, 260), (570, 260),
               (566, 245), (566, 250), (566, 280), (566, 288), (243, 260), (244, 260)]:
    print("   (%3d,%3d) = %s" % (x, y, tuple(O[y, x])))
print("=== RENDER same frame coords ===")
for (x, y) in [(243, 244), (250, 300), (560, 260), (565, 260), (566, 260), (570, 260), (566, 280)]:
    print("   (%3d,%3d) = %s" % (x, y, tuple(R[int(round(y * S)), int(round(x * S))])))
