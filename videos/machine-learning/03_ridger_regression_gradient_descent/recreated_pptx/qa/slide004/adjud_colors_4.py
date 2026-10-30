# Colour composition of every text line in the ORIGINAL (frame px, 1px = 1pt).
import numpy as np
from PIL import Image

O = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
RIM = Image.open("recreated_pptx/qa/slide004/render_4.png").convert("RGB")
SC = RIM.size[1] / 540.0
R = np.asarray(RIM.resize((int(round(RIM.size[0] / SC)), int(round(RIM.size[1] / SC))), Image.LANCZOS)).astype(int)


def comp(img, box, label):
    x0, y0, x1, y1 = box
    reg = img[y0:y1, x0:x1]
    m = reg.sum(axis=2) < 690
    px = reg[m]
    if len(px) == 0:
        print("%-42s NO INK" % label)
        return
    n = len(px)
    dark = (px.sum(axis=1) < 260)
    red = (px[:, 0] > 140) & (px[:, 1] < 140) & (px[:, 2] < 140)
    blue = (px[:, 2] > 130) & (px[:, 0] < 150) & (px[:, 1] < 180)
    print("%-42s n=%5d  dark %3d%%  red %3d%%  blue %3d%%  other %3d%%" % (
        label, n, 100 * dark.mean(), 100 * red.mean(), 100 * blue.mean(),
        100 * (1 - dark.mean() - red.mean() - blue.mean())))


print("=== ORIGINAL ===")
comp(O, (240, 68, 700, 95), "title")
comp(O, (245, 132, 375, 158), "box1 caption 'Original Labels'")
comp(O, (210, 156, 388, 182), "box1 sub 'from Training Samples'")
comp(O, (584, 132, 726, 156), "box2 caption 'Predicted Labels'")
comp(O, (565, 164, 740, 190), "box2 sub 'from Model Yhat=XW'")
comp(O, (84, 248, 300, 296), "objective box line")
comp(O, (84, 312, 480, 362), "error box line")
comp(O, (500, 244, 690, 278), "where line 1 'Yhat = XW' only")
comp(O, (690, 256, 770, 276), "where line 1 'Predicted' label")
comp(O, (500, 280, 890, 308), "where line 2")
comp(O, (500, 310, 890, 340), "where line 3")
comp(O, (500, 340, 890, 368), "where line 4")
comp(O, (80, 384, 660, 452), "define box line")
comp(O, (787, 100, 877, 120), "remember 'Remember' label")
comp(O, (797, 122, 877, 150), "remember equation")
comp(O, (150, 476, 490, 520), "formula")

print("\n=== RENDER_4 (for comparison) ===")
comp(R, (240, 68, 700, 95), "title")
comp(R, (245, 132, 375, 158), "box1 caption 'Original Labels'")
comp(R, (210, 156, 388, 182), "box1 sub 'from Training Samples'")
comp(R, (500, 244, 690, 278), "where line 1 'Yhat = XW' only")
comp(R, (690, 256, 770, 276), "where line 1 'Predicted' label")
comp(R, (84, 248, 300, 296), "objective box line")
comp(R, (84, 312, 480, 362), "error box line")
comp(R, (80, 384, 660, 452), "define box line")
comp(R, (150, 476, 490, 520), "formula")
