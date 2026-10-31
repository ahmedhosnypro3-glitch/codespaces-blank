#!/usr/bin/env python3
"""Lane G (b_geom_4): colour-classified element measurement.

Both sides are reduced to the 960x540 SOURCE-FRAME grid:
  - original JPEG : 960x540 directly
  - render PNG    : 2001x1125 at 150dpi -> frame px = render_px * 960/2001
The recreation's build scripts declare geometry in source px of this same 960x540
grid (PX = 13.33/960), so the two grids are the same coordinate space.

Elements are isolated by COLOUR on each side independently, so the comparison
is element-vs-element and not biased by a shared search window.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    return o, r


def bbox(m, ox=0, oy=0):
    rr = np.where(m.any(axis=1))[0]
    cc = np.where(m.any(axis=0))[0]
    if len(rr) == 0:
        return None
    return int(cc[0]) + ox, int(rr[0]) + oy, int(cc[-1]) + ox, int(rr[-1]) + oy


def near(a, rgb, tol):
    return np.abs(a - np.array(rgb)).sum(axis=2) <= tol


def frame_render(r):
    """Resample render to the 960x540 frame grid."""
    return np.asarray(Image.fromarray(r.astype("uint8")).resize((960, 540), Image.BOX)).astype(int)


def report(n, items):
    o, r = load(n)
    rf = frame_render(r)
    print(f"##### slide {n}   (frame grid 960x540)")
    for label, col, tol, src in items:
        if src == "orig":
            m = near(o, col, tol)
            box = bbox(m)
            note = ""
        else:
            m = near(r, col, tol)
            b = bbox(m)
            box = None if b is None else (round(b[0] * 960 / r.shape[1], 1),
                                          round(b[1] * 540 / r.shape[0], 1),
                                          round(b[2] * 960 / r.shape[1], 1),
                                          round(b[3] * 540 / r.shape[0], 1))
            note = ""
        print(f"  {label:26s} {box} {note}")


ITEMS = {
    "025": [
        ("peach_eq_box_1", (255, 230, 204), 30, "orig"),
        ("cream_eq_box_2", (255, 242, 204), 30, "orig"),
        ("blue_header_text", (0, 0, 255), 90, "orig"),
        ("red_error_bar", (192, 0, 0), 60, "orig"),
        ("red_section_head", (192, 0, 0), 70, "orig"),
    ],
    "026": [
        ("red_title_text", (185, 60, 70), 110, "orig"),
        ("blue_subtitle", (67, 59, 193), 110, "orig"),
        ("dark_title_text", (74, 74, 74), 40, "orig"),
    ],
}


def main():
    for n in ["025", "026"]:
        report(n, ITEMS[n])


if __name__ == "__main__":
    main()
