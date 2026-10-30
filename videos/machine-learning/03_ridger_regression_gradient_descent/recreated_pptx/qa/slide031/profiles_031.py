# Fresh-lane precise row/column profiles, ORIGINAL frame vs CURRENT render.
# Row profiles are dumped raw so each region can be read off exactly, with the
# box borders separated from the text bands by their own signatures.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
SX, SY = 2001 / 960.0, 1125 / 540.0

OV, RV = O.max(axis=2), R.max(axis=2)
# ORIGINAL: canvas 255 / panel 233 / plot-bg 240; glyphs dark. Use two thresholds.
O_dark = OV < 200
O_mid = OV < 226
# RENDER: canvas 255, anti-aliased; glyph cores are darker.
R_dark = RV < 205


def profile(tag, arr, msk, x0, x1, y0, y1, scale, thr=1):
    print("  --- %s : dark-px count per row, x %s..%s" % (tag, x0, x1))
    for y in range(y0, y1):
        c = int(msk[y, x0:x1].sum())
        if c >= thr:
            print("      frame y %6.1f  n=%3d" % (y / scale, c))


print("############ TITLE band, ORIGINAL (x 60..570, y 55..100) ############")
profile("ORIG", O, O_dark, 60, 570, 55, 100, 1.0)
print("############ TITLE band, RENDER (x 60..570) ############")
profile("REND", R, R_dark, int(60 * SX), int(570 * SX), int(55 * SX), int(100 * SX), SX)

print("\n############ ANNOTATION interior, ORIGINAL x 250..805 y 242..292 (MID thr 226 to catch faded text) ############")
profile("ORIG-mid", O, O_mid, 250, 805, 242, 292, 1.0)
print("############ ANNOTATION interior, RENDER x 250..805 ############")
profile("REND", R, R_dark, int(250 * SX), int(805 * SX), int(242 * SX), int(292 * SX), SX)

print("\n############ X-TICK LABEL band, ORIGINAL x 570..812 y 262..300 (mid thr) ############")
profile("ORIG-mid", O, O_mid, 570, 812, 262, 300, 1.0)
print("############ X-TICK LABEL band, RENDER ############")
profile("REND", R, R_dark, int(570 * SX), int(812 * SX), int(262 * SX), int(300 * SX), SX)

print("\n############ (5,1) label region ORIGINAL x 485..560 y 244..266 - green pixels per row ############")
Om = (O[:, :, 1] > O[:, :, 0] + 25) & (O[:, :, 1] > O[:, :, 2] + 25)
for y in range(244, 266):
    xs = np.nonzero(Om[y, 485:560])[0]
    if len(xs):
        print("      frame y %3d  n=%2d  x %d..%d" % (y, len(xs), 485 + xs.min(), 485 + xs.max()))
print("############ (5,1) label region RENDER ############")
Rm = (R[:, :, 1] > R[:, :, 0] + 25) & (R[:, :, 1] > R[:, :, 2] + 25)
for y in range(int(244 * SX), int(266 * SX)):
    xs = np.nonzero(Rm[y, int(485 * SX):int(560 * SX)])[0]
    if len(xs):
        print("      frame y %6.2f  n=%2d  frame x %.1f..%.1f" % (y / SX, len(xs), 485 + xs.min() / SX, 485 + xs.max() / SX))

print("\n############ '(5,1)' DARK glyphs (label text is dark green/black?) ORIGINAL x 490..545 ############")
for y in range(244, 266):
    xs = np.nonzero(O_dark[y, 490:545])[0]
    if len(xs):
        print("      frame y %3d  n=%2d  x %d..%d" % (y, len(xs), 490 + xs.min(), 490 + xs.max()))
print("############ RENDER ############")
for y in range(int(244 * SX), int(266 * SX)):
    xs = np.nonzero(R_dark[y, int(490 * SX):int(545 * SX)])[0]
    if len(xs):
        print("      frame y %6.2f  n=%2d  frame x %.1f..%.1f" % (y / SX, len(xs), 490 + xs.min() / SX, 490 + xs.max() / SX))
