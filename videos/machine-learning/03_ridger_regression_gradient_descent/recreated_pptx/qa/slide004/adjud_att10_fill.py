# Settle the att10 legA not-carried item: is the upper-left "Objective is Yhat=Y"
# box cream-filled in the original, or white/unfilled? Render gives both left
# boxes the same cream fill; judge could not confirm at JPEG legibility.
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
O = np.asarray(Image.open(D + "/unique_slides/slide_004.jpg").convert("RGB")).astype(int)
RIM = Image.open(D + "/recreated_pptx/qa/slide004/render_9.png").convert("RGB")
SC = RIM.size[1] / 540.0
R = np.asarray(RIM.resize((int(round(RIM.size[0] / SC)), int(round(RIM.size[1] / SC))), Image.LANCZOS)).astype(int)


def classify(px):
    r, g, b = px
    if r > 235 and g > 235 and b > 235:
        return "."          # white
    if r > 235 and 225 <= g <= 245 and 180 <= b <= 230:
        return "c"          # cream
    if b > 100 and b > r + 30 and g < b:
        return "B"          # blue
    if r > 130 and g < 110 and b < 110:
        return "r"          # red
    if r + g + b < 300:
        return "#"          # dark ink
    return ":"


def band(img, tag):
    print("=== %s: left band x60..500, y230..380, step 4 ===" % tag)
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(60, 500, 4))
    print(hdr)
    for y in range(230, 380, 4):
        row = "".join(classify(img[y, x]) for x in range(60, 500, 4))
        print("%4d %s" % (y, row))


band(O, "ORIGINAL")
band(R, "RENDER_9 (scaled to 540)")


def patch(img, x0, x1, y0, y1, tag):
    reg = img[y0:y1, x0:x1].reshape(-1, 3)
    med = np.median(reg, axis=0).astype(int)
    print("%-46s median RGB %s  (n=%d)" % (tag, tuple(med), len(reg)))


print("\n=== interior fill medians (text-free patches) ===")
for img, tag in ((O, "orig"), (R, "render")):
    print("--", tag)
    patch(img, 200, 296, 250, 292, "objective box interior (right of text)")
    patch(img, 92, 140, 254, 290, "objective box interior (left margin)")
    patch(img, 380, 470, 316, 356, "error box interior (right of text)")
    patch(img, 92, 140, 316, 356, "error box interior (left margin)")
