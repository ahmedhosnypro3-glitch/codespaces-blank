"""Diagnostics: detect the ORIGINAL frame's own outer border ring, and use an exact
background-distance mask for the render (its background is exactly #E8E8E8)."""
import os

import numpy as np
from PIL import Image, ImageFilter

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = ["014", "016", "017", "023", "024"]


def strong_ink(img, thresh=40, radius=6):
    rgb = img.convert("RGB")
    a = np.asarray(rgb).astype(np.int16)
    bg = np.asarray(rgb.filter(ImageFilter.GaussianBlur(radius))).astype(np.int16)
    return np.abs(a - bg).max(axis=2) > thresh


def render_ink(img, tol=8):
    """Exact background-distance mask; render bg is #E8E8E8."""
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    bg = np.array([232, 232, 232], dtype=np.int16)
    return np.abs(a - bg).max(axis=2) > tol


def find_border(m, frac_rows=0.55, frac_cols=0.45):
    H, W = m.shape
    rows, cols = m.sum(1), m.sum(0)
    top = next((y for y in range(H) if rows[y] > W * frac_rows), None)
    bot = next((y for y in range(H - 1, -1, -1) if rows[y] > W * frac_rows), None)
    lef = next((x for x in range(W) if cols[x] > H * frac_cols), None)
    rig = next((x for x in range(W - 1, -1, -1) if cols[x] > H * frac_cols), None)
    return top, bot, lef, rig


if __name__ == "__main__":
    for n in SLIDES:
        o = Image.open(os.path.join(NS, "unique_slides", f"slide_{n}.jpg")).convert("RGB")
        r = Image.open(os.path.join(NS, "_pool/lo_geom_b_geom_3/out",
                                    f"slide_{n}_150.png")).convert("RGB")
        om = strong_ink(o)
        rm = render_ink(r)
        print(f"=== {n} ===")
        print("  ORIG strong-ink border:", find_border(om))
        # render: mask house frame ring, then re-find content extent
        H, W = rm.shape
        ex = np.zeros_like(rm)
        inset, band = int(round(0.15 * 150)), 7
        for t in (inset, W - 1 - inset):
            ex[max(0, t - band):t + band + 1, :] = True
        for t in (inset, H - 1 - inset):
            ex[:, max(0, t - band):t + band + 1] = True
        ex[int(0.16 * 150):int(0.94 * 150), int(12.34 * 150):int(13.10 * 150)] = True
        rm2 = rm & ~ex
        ys, xs = np.nonzero(rm2)
        print(f"  REND content bbox (render px): x {xs.min()}..{xs.max()} "
              f"y {ys.min()}..{ys.max()}  -> frame-scale x {xs.min()*960/2001:.1f}..{xs.max()*960/2001:.1f} "
              f"y {ys.min()*540/1125:.1f}..{ys.max()*540/1125:.1f}")
        # content below the house frame bottom?
        below = rm2[int(7.36 * 150):, :]
        print(f"  REND ink BELOW house frame (y>7.36in): {int(below.sum())} px")
