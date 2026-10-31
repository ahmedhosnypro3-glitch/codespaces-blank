"""Lane G / b_geom_3 — geometry closed-loop PIL verification, slides 014,016,017,023,024.

For each slide: chrome-masked ink-bbox of slide-specific content in BOTH the LO
render (2001x1125 @150dpi) and unique_slides/slide_NNN.jpg (960x540), normalized
to frame scale, compared per region against ~2px frame-scale tolerance
(~4px @150dpi). House chrome (red frame @0.15in inset, yellow badge
x=12.48/y=0.30, title box y=0.28) is excluded and never reported.
"""
import os

import numpy as np
from PIL import Image, ImageFilter

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = ["014", "016", "017", "023", "024"]
REND = "_pool/lo_geom_b_geom_3/out"
SCOPE = "b_geom_3"
TOL_FRAME = 2.0
FW, FH = 960, 540

# region bands in frame-scale y, derived per-slide from each layout's structure
BANDS = {
    "014": {"title": (40, 105), "diagram_body": (105, 490), "footer": (490, 540)},
    "016": {"title": (40, 105), "diagram_body": (105, 490), "footer": (490, 540)},
    "017": {"title": (40, 105), "diagram_body": (105, 490), "footer": (490, 540)},
    "023": {"title": (40, 95), "flowchart_body": (95, 500), "footer": (500, 540)},
    "024": {"title": (40, 100), "panel_upper": (100, 300), "panel_lower": (300, 460),
            "footer": (460, 540)},
}


def ink_mask(img, thresh=14, radius=12):
    rgb = img.convert("RGB")
    a = np.asarray(rgb).astype(np.int16)
    bg = np.asarray(rgb.filter(ImageFilter.GaussianBlur(radius))).astype(np.int16)
    return np.abs(a - bg).max(axis=2) > thresh


def mask_render_chrome(m):
    """Mask house chrome in the 2001x1125 render: red frame ring + yellow badge."""
    H, W = m.shape
    ex = np.zeros_like(m)
    inset, band = int(round(0.15 * 150)), 8
    for t in (inset, W - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    for t in (inset, H - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    ex[int(0.18 * 150):int(0.92 * 150), int(12.36 * 150):int(13.08 * 150)] = True
    return m & ~ex


def mask_orig_chrome(m):
    """Mask the original frame's own outer border ring + its own badge region."""
    H, W = m.shape
    ex = np.zeros_like(m)
    rows, cols, band = m.sum(1), m.sum(0), 10
    for y in list(range(int(H * 0.12))) + list(range(int(H * 0.88), H)):
        if rows[y] > W * 0.55:
            ex[max(0, y - band):y + band + 1, :] = True
    for x in list(range(int(W * 0.12))) + list(range(int(W * 0.88), W)):
        if cols[x] > H * 0.45:
            ex[:, max(0, x - band):x + band + 1] = True
    # original badge lives near the top-right corner
    ex[int(0.10 * 540):int(0.30 * 540), int(0.90 * 960):FW] = True
    return m & ~ex


def bbox_in(m, y0, y1, x0, x1):
    y0, y1 = max(0, y0), min(m.shape[0] - 1, y1)
    x0, x1 = max(0, x0), min(m.shape[1] - 1, x1)
    sub = m[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None, 0
    return (int(xs.min()) + x0, int(ys.min()) + y0,
            int(xs.max()) + x0, int(ys.max()) + y0), int(sub.sum())


def fmt(b):
    return "none" if b is None else f"[{b[0]},{b[1]}]-[{b[2]},{b[3]}] (w{b[2]-b[0]+1} h{b[3]-b[1]+1})"


def main():
    sx, sy = FW / 2001.0, FH / 1125.0
    for n in SLIDES:
        oimg = Image.open(os.path.join(NS, "unique_slides", f"slide_{n}.jpg"))
        rimg = Image.open(os.path.join(NS, REND, f"slide_{n}_150.png"))
        assert tuple(rimg.size) == (2001, 1125), rimg.size
        om = mask_orig_chrome(ink_mask(oimg))
        rm = mask_render_chrome(ink_mask(rimg))
        print(f"### slide {n}  orig={oimg.size} render={rimg.size}")
        print(f"    inkfrac orig={om.mean():.4f} render={rm.mean():.4f}")
        for name, (y0, y1) in BANDS[n].items():
            ob, on = bbox_in(om, y0, y1, 0, FW - 1)
            ry0, ry1 = round(y0 / sy), round(y1 / sy)
            rb, rn = bbox_in(rm, ry0, ry1, 0, 2000)
            if ob is None or rb is None:
                print(f"    [n/a] {name}: orig={fmt(ob)} render={fmt(rb)}")
                continue
            rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
            d = (ob[0] - rbf[0], ob[1] - rbf[1], ob[2] - rbf[2], ob[3] - rbf[3])
            worst = max(abs(v) for v in d)
            flag = "PASS" if worst <= TOL_FRAME else "EXCEEDS-TOLERANCE"
            print(f"    [{flag}] {name}: orig={fmt(ob)} render_norm={fmt(rbf)} "
                  f"dx={d[0]:+.2f} dy={d[1]:+.2f} dw={d[2]-d[0]:+.2f} dh={d[3]-d[1]:+.2f} "
                  f"worst={worst:.2f} ink_o={on} ink_r={rn}")
        print()


if __name__ == "__main__":
    main()
