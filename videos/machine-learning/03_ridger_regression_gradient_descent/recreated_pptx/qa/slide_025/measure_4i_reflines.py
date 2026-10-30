import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
R, G, B = orig[..., 0], orig[..., 1], orig[..., 2]
red = (R > 130) & (R - G > 55) & (R - B > 55)
sat = (orig.max(axis=2) - orig.min(axis=2)) > 45
white = (R > 248) & (G > 248) & (B > 248)

def rl(y, x0, x1):
    xs = np.where(red[y, x0:x1])[0] + x0
    if not len(xs): return []
    o, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i-1]+1: o.append((s, xs[i-1])); s = xs[i]
    o.append((s, xs[-1]))
    return o

print("--- TL red rows (mask threshold R>130,R-G>55,R-B>55) ---")
for y in range(115, 296):
    r = rl(y, 54, 470)
    long = [q for q in r if q[1]-q[0]+1 >= 8]
    if long:
        print("  y=%3d  %s" % (y, long))

print("\n--- what is at y=186 from x255..300 (color classes) ---")
def cl(p):
    r, g, b = p
    if r > 248 and g > 248 and b > 248: return "W"
    if r > 130 and r-g > 55 and r-b > 55: return "R"
    if (max(p)-min(p)) > 45: return "#" if p[0] >= p[2] else "o"
    if max(p) < 90: return "K"
    if abs(r-233) < 12 and abs(g-233) < 12 and abs(b-231) < 12: return "."
    return "-"
for y in [168, 185, 186, 187]:
    print("  y=%d: %s" % (y, "".join(cl(orig[y, x]) for x in range(250, 300))))
print("  x-axis labels: ", "".join(str(x // 10 % 10) for x in range(250, 300)))

print("\n--- what is at y=226 from x620..890 ---")
for y in [222, 225, 226, 227]:
    print("  y=%d: %s" % (y, "".join(cl(orig[y, x]) for x in range(615, 890))))
print("  x-axis: ", "".join(str(x // 10 % 10) for x in range(615, 890)))
