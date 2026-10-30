# Comprehensive ORIGINAL vs CURRENT-render comparison of the plot region and the
# annotation region, to enumerate exactly which original elements the build's
# oversized annotation box (x243..809 white fill) erases.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
S = 2001 / 960.0


def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    v = a.max(axis=2)
    return dict(
        green=(g > r + 18) & (g > b + 18) & (g < 210),
        red=(r > 90) & ((r - g) > 35) & ((r - b) > 8),
        blue=(b > r + 40) & (b > g + 40),
        dark=v < 170,
        white=(r > 245) & (g > 245) & (b > 245),
    )


mo, mr = masks(O), masks(R)


def count(m, x0, y0, x1, y1, sc):
    return int(m[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)].sum())


REGIONS = [
    ("annot RIGHT green border x564..568 y246..287", 564, 246, 568, 287),
    ("annot BOTTOM green y287..291 x250..565", 250, 287, 565, 291),
    ("annot TOP green y242..246 x250..565", 250, 242, 565, 246),
    ("annot LEFT green x241..246 y250..285", 241, 250, 246, 285),
    ("green POINT (5,1) marker x682..694 y247..260", 682, 247, 694, 260),
    ("black X-AXIS y263..269 x574..806", 574, 263, 806, 269),
    ("red dashed VERT x=5, y246..264", 684, 246, 693, 264),
    ("red dashed HORIZ y=1, x575..805", 575, 250, 805, 257),
    ("parabola vertex region x670..706 y246..264", 670, 246, 706, 264),
    ("plot box bottom red y307..312 x572..811", 572, 307, 811, 312),
    ("plot box left red x571..576 y70..300", 571, 70, 576, 300),
    ("plot box right red x806..812 y70..300", 806, 70, 812, 300),
    ("plot box top red y63..69 x572..811", 572, 63, 811, 69),
    ("chord black y143..150 x650..726", 650, 143, 726, 150),
    ("red dot x655..667 y177..190", 655, 177, 667, 190),
    ("x-tick labels y269..285 x574..808", 574, 269, 808, 285),
    ("y-tick labels x538..572 y80..265", 538, 80, 572, 265),
]
print("%-52s %12s %12s" % ("REGION (frame px)", "ORIG", "RENDER"))
for name, x0, y0, x1, y1 in REGIONS:
    print("%-52s" % name, end=" ")
    out = []
    for k in ("dark", "red", "green", "blue"):
        out.append("%s o=%6d r=%6d" % (k, count(mo[k], x0, y0, x1, y1, 1.0),
                                       count(mr[k], x0, y0, x1, y1, S)))
    print(" | ".join(out))

print("\n=== ORIGINAL annotation interior fill sample (clean spots) ===")
for (x, y) in [(350, 265), (520, 266), (300, 244), (520, 244), (540, 266), (246, 266), (240, 266)]:
    print("   (%3d,%3d) = %s" % (x, y, tuple(O[y, x])))
print("=== RENDER same frame coords ===")
for (x, y) in [(350, 265), (520, 266), (300, 244), (520, 244), (540, 266), (246, 266), (240, 266)]:
    print("   (%3d,%3d) = %s" % (x, y, tuple(R[int(round(y * S)), int(round(x * S))])))

print("\n=== green marker blob search in ORIGINAL x660..720 y240..270 ===")
g = mo["green"]
for y in range(240, 271):
    xs = np.nonzero(g[y, 660:720])[0]
    if len(xs):
        print("   y%3d n=%2d x %d..%d" % (y, len(xs), 660 + xs.min(), 660 + xs.max()))
print("=== same in RENDER ===")
g = mr["green"]
for y in range(int(240 * S), int(271 * S)):
    xs = np.nonzero(g[y, int(660 * S):int(720 * S)])[0]
    if len(xs):
        print("   frame y %6.2f n=%2d frame x %.1f..%.1f"
              % (y / S, len(xs), 660 + xs.min() / S, 660 + xs.max() / S))
