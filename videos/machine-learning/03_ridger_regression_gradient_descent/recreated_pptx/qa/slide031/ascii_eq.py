import sys
from PIL import Image
import numpy as np

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_031.jpg"
REND = DECK + "/recreated_pptx/qa/slide031/render_9.png"
SC = 1125 / 540.0


def ascii_art(img_arr, x0, y0, x1, y1, scale, cols=None, rows=None, thresh=140):
    """Print an ASCII rendering of a region. scale = render px per frame px."""
    sub = img_arr[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    # downsample by block max so thin strokes survive
    h, w = lum.shape
    ch = 2  # chars per block horizontally (aspect)
    dh = 4
    out = []
    for yy in range(0, h, dh):
        line = ""
        for xx in range(0, w, ch):
            blk = lum[yy:yy + dh, xx:xx + ch]
            m = blk.min() if blk.size else 255
            line += "#" if m < thresh else ("+" if m < 190 else ".")
        out.append(line)
    return "\n".join(out)


o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)

print("############ EQUATION BOX — ORIGINAL (frame x398..532 y182..214) ############")
print(ascii_art(o, 398, 182, 532, 214, 1.0))
print()
print("############ EQUATION BOX — RENDER (same window) ############")
print(ascii_art(r, 398, 182, 532, 214, SC))
