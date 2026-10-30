#!/usr/bin/env python3
"""Two-image adjudication of the top cream box: line pitch + vertical centering.

Measures render_9.png and unique_slides/slide_005.jpg side by side in FRAME px
(render 2001x1125 @150dpi -> sx=2001/960, sy=1125/540) and reports:
  * the three Loss-equation ink bands (eq1/eq2/eq3)
  * the inter-equation gaps (the "line spacing" a judge may call stretched)
  * the cream box's own bounds on each image
  * the top and bottom padding inside the box and the top/bottom balance
  * the per-image and cross-image deltas

Every number here is measured on BOTH images before any build change.
"""
import os

import numpy as np
from PIL import Image

Q = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
       "03_ridger_regression_gradient_descent")
ORIG = os.path.join(VID, "unique_slides/slide_005.jpg")
REND = os.path.join(Q, "render_9.png")
SX, SY = 2001 / 960.0, 1125 / 540.0

# equation ink windows (frame px), interior to the cream box, no border contact
EQW = {
    "eq1": (90, 552, 105, 154),
    "eq2": (90, 637, 168, 218),
    "eq3": (90, 530, 225, 275),
}
CREAM_FILL = (251, 253, 229)  # FBFFE5


def load():
    o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
    r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
    return o, r


def ink_band(arr, win, sx, sy, thr=200):
    x0, x1, y0, y1 = win
    X0, X1, Y0, Y1 = int(x0 * sx), int(x1 * sx), int(y0 * sy), int(y1 * sy)
    sub = arr[Y0:Y1 + 1, X0:X1 + 1].mean(axis=2) < thr
    if not sub.any():
        return None
    ys, xs = np.nonzero(sub)
    return ((X0 + xs.min()) / sx, (Y0 + ys.min()) / sy,
            (X0 + xs.max()) / sx, (Y0 + ys.max()) / sy)


def cream_box(arr, sx, sy, tol):
    """Locate the upper cream box by its fill colour; return frame-px bounds.

    Cream FBFFE5 has G-B = 24; white canvas FFFFFF has G-B = 0 and the gray
    panel E9E9E7 has G-B = 2. Selecting on the G-B channel separates cream from
    both without relying on a tight RGB tolerance (JPEG shifts the fill).
    """
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    mask = ((g - b) >= 12) & (r >= 235) & (g >= 240)
    mask[int(300 * sy):, :] = False
    mask[:, int(850 * sx):] = False  # exclude the yellow badge (FDFD96)
    # Reject JPEG-noise rows/columns: fewer than 3 ink px is a phantom, not structure.
    rows = np.nonzero(mask.sum(axis=1) >= 3)[0]
    cols = np.nonzero(mask.sum(axis=0) >= 3)[0]
    if len(rows) == 0 or len(cols) == 0:
        return None
    return ((cols.min()) / sx, (rows.min()) / sy,
            (cols.max()) / sx, (rows.max()) / sy)


def report(tag, arr, sx, sy, tol):
    print(f"--- {tag} ---")
    bands = {}
    for k, w in EQW.items():
        b = ink_band(arr, w, sx, sy)
        bands[k] = b
        if b:
            print(f"  {k}: y {b[1]:7.2f} .. {b[3]:7.2f}   x {b[0]:7.2f} .. {b[2]:7.2f}"
                  f"   (h={b[3]-b[1]:6.2f})")
        else:
            print(f"  {k}: EMPTY")
    g12 = bands["eq2"][1] - bands["eq1"][3] if bands["eq1"] and bands["eq2"] else None
    g23 = bands["eq3"][1] - bands["eq2"][3] if bands["eq2"] and bands["eq3"] else None
    print(f"  gap eq1->eq2 = {g12:7.2f} px   gap eq2->eq3 = {g23:7.2f} px"
          f"   unevenness = {abs(g12-g23):.2f} px")
    box = cream_box(arr, sx, sy, tol)
    print(f"  cream box fill bbox: x {box[0]:.2f}..{box[2]:.2f}  y {box[1]:.2f}..{box[3]:.2f}")
    # border sits ~1 frame px outside the fill on each side
    top_b, bot_b = box[1] - 1.0, box[3] + 1.0
    if bands["eq1"] and bands["eq3"]:
        top_pad = bands["eq1"][1] - top_b
        bot_pad = bot_b - bands["eq3"][3]
        print(f"  padding top (box_top->eq1) = {top_pad:6.2f} px")
        print(f"  padding bottom (eq3->box_bot) = {bot_pad:6.2f} px")
        print(f"  top/bottom balance = {abs(top_pad-bot_pad):6.2f} px"
              f"  (smaller = better centred)")
    return {"bands": bands, "g12": g12, "g23": g23, "box": box}


def main():
    o, r = load()
    print("== TOP CREAM BOX: line pitch + vertical centering, BOTH images ==\n")
    O = report("ORIGINAL slide_005.jpg (960x540, frame px)", o, 1.0, 1.0, 42)
    print()
    R = report("RENDER render_9.png (2001x1125, rescaled to frame px)", r, SX, SY, 24)

    print("\n== CROSS-IMAGE DELTAS (render - original, frame px) ==")
    for k in ("eq1", "eq2", "eq3"):
        ob, rb = O["bands"][k], R["bands"][k]
        print(f"  {k}: dy0={rb[1]-ob[1]:+.2f}  dy1={rb[3]-ob[3]:+.2f}"
              f"  dx0={rb[0]-ob[0]:+.2f}  dx1={rb[2]-ob[2]:+.2f}")
    print(f"  gap eq1->eq2: orig {O['g12']:.2f}  render {R['g12']:.2f}"
          f"  delta {R['g12']-O['g12']:+.2f}")
    print(f"  gap eq2->eq3: orig {O['g23']:.2f}  render {R['g23']:.2f}"
          f"  delta {R['g23']-O['g23']:+.2f}")
    print(f"  unevenness:   orig {abs(O['g12']-O['g23']):.2f}"
          f"  render {abs(R['g12']-R['g23']):.2f}"
          f"  delta {abs(R['g12']-R['g23'])-abs(O['g12']-O['g23']):+.2f}")
    print(f"  cream box top:  orig {O['box'][1]:.2f}  render {R['box'][1]:.2f}"
          f"  delta {R['box'][1]-O['box'][1]:+.2f}")
    print(f"  cream box bot:  orig {O['box'][3]:.2f}  render {R['box'][3]:.2f}"
          f"  delta {R['box'][3]-O['box'][3]:+.2f}")
    print("\nTOL 8 frame px applies to the geometry deltas.")


if __name__ == "__main__":
    main()
