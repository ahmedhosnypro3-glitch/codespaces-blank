# Definitive characterization of the ORIGINAL frame's plot region and annotation
# region. Everything is read off the frame; the build's assumptions are NOT used.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R, G, B = O[:, :, 0], O[:, :, 1], O[:, :, 2]
V = O.max(axis=2)

print("=== 1. plot-box vertical borders: red presence per column, rows 60..320 ===")
red = (R > 90) & ((R - G) > 35) & ((R - B) > 8)
for x in range(565, 585):
    ys = np.nonzero(red[60:320, x])[0] + 60
    if len(ys):
        print("   x%3d red rows %d..%d n=%d" % (x, ys.min(), ys.max(), len(ys)))
print()
for x in range(800, 818):
    ys = np.nonzero(red[60:320, x])[0] + 60
    if len(ys):
        print("   x%3d red rows %d..%d n=%d" % (x, ys.min(), ys.max(), len(ys)))

print("\n=== 2. rows 300..318: what is at x 565..600 and x 800..815 ===")
for y in range(300, 319):
    print("   y%3d  left %s | right %s" % (y, [tuple(O[y, x]) for x in (566, 570, 573, 580)],
                                          [tuple(O[y, x]) for x in (804, 807, 809, 813)]))

print("\n=== 3. x-axis line at y 262..270, x 570..810: colour census ===")
for y in range(262, 271):
    row = O[y, 570:811]
    r, g, b = row[:, 0], row[:, 1], row[:, 2]
    redish = int(((r > 90) & ((r - g) > 35) & ((r - b) > 8)).sum())
    darkish = int((row.max(axis=1) < 170).sum())
    print("   y%3d  red=%3d dark=%3d  sample x573=%s x700=%s" % (y, redish, darkish,
                                                                 tuple(O[y, 573]), tuple(O[y, 700])))

print("\n=== 4. colour map of ORIGINAL x 655..725, y 232..278 (1px) ===")
def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r > 110 and g < 90 and b < 90:
        return "R"
    if g > r + 25 and g > b + 25:
        return "G"
    if b > r + 40 and b > g + 40:
        return "B"
    if g > r + 8 and g > b + 8:
        return "g"
    if r > g + 25 and r > b + 25:
        return "r"
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


print("     " + "".join(str((655 + i) // 10 % 10) for i in range(70)))
print("     " + "".join(str((655 + i) % 10) for i in range(70)))
for y in range(232, 279):
    print("%3d " % y + "".join(cls(O[y, x]) for x in range(655, 725)))

print("\n=== 5. annotation interior fill census, ORIGINAL x 250..560, y 246..287 ===")
reg = O[246:288, 250:561].reshape(-1, 3)
import collections
c = collections.Counter(map(tuple, reg // 4 * 4))
print("   top-6 modal:", c.most_common(6))
print("   is interior pale-green? frac(G>R+6 and G>B+6) = %.3f" %
      float(((reg[:, 1] > reg[:, 0] + 6) & (reg[:, 1] > reg[:, 2] + 6)).mean()))
print("   frac pure white (>248 all) = %.3f" %
      float(((reg.min(axis=1) > 248)).mean()))
print("   median:", np.median(reg, axis=0))
