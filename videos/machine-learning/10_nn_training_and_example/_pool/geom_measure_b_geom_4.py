#!/usr/bin/env python3
"""Lane G (b_geom_4): per-region ink-edge measurement, original frame vs render.

Both sides are reduced to 960x540 SOURCE-FRAME px:
  - original JPEG  : already 960x540 (slide pixels x38..921, y43..538)
  - render PNG     : 2001x1125 at 150dpi; frame_px = render_px * 960/2001
    (= render_px * 72.02/150, i.e. 150dpi -> frame scale)
The recreation's build scripts declare content in source px, so this is the
correct comparison space (verified: slide 029 red box, orig y202-397).

Chrome (house red frame, yellow badge, title-box anchors, the original's own
outer border and video letterbox) is masked out of BOTH sides before measuring,
so only slide-specific content is compared.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SCOPE = "b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]

# original slide interior (inside its own border, outside white letterbox)
O_BOX = (38, 43, 922, 539)
# original's own thin outer border ring (its chrome analogue)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
# render house red frame at 0.15in inset => 0.15*150 = 22.5 render px
R_BOX = (26, 26, 1975, 1099)
# render house badge: x12.48in,y0.30in, 0.5in => *150
R_BADGE = (1872, 45, 1947, 120)
# render house title box: x0.6in,y0.28in,w12.13in,h~0.55in => *150
R_TITLE = (90, 42, 1910, 130)

# region definitions in source-frame px, per slide
REGIONS = {
    "025": {
        "title_block":            (38, 43, 922, 78),
        "header_long_chain":      (38, 78, 400, 120),
        "eq_boxes_left":          (38, 120, 400, 300),
        "nn_diagram":             (400, 78, 922, 300),
        "bottom_charts":          (38, 300, 922, 520),
    },
    "026": {
        "title_block":            (38, 43, 922, 78),
        "subtitle_line1":         (150, 215, 810, 285),
        "subtitle_line2":         (150, 285, 810, 365),
    },
    "027": {
        "title_block":            (38, 43, 922, 78),
        "nn_diagram":             (170, 78, 866, 255),
        "forward_header":         (38, 255, 650, 278),
        "calc_box1":              (50, 276, 370, 422),
        "green_boxes_right":      (644, 276, 897, 422),
        "calc_box2":              (50, 433, 610, 529),
    },
    "029": {
        "title_block":            (38, 43, 922, 78),
        "red_diagram_box":        (140, 200, 834, 400),
        "input_column_vector":    (160, 232, 214, 336),
        "target_column_vector":   (650, 240, 692, 315),
    },
    "032": {
        "title_block":            (38, 43, 922, 78),
        "top_panel":              (98, 87, 827, 288),
        "bottom_panel":           (98, 328, 827, 528),
    },
}


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def ink(a, bg, thr=45):
    return np.abs(a - bg).sum(axis=2) > thr


def bbox(mask, ox=0, oy=0):
    """Ink bounding box in GLOBAL coords (mask is a slice)."""
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return None
    return int(cols[0]) + ox, int(rows[0]) + oy, int(cols[-1]) + ox, int(rows[-1]) + oy


def masks(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    obg = fast_bg(o, O_BOX)
    om = ink(o, obg)
    om[: O_BOX[1], :] = False
    om[O_BOX[3]:, :] = False
    om[:, : O_BOX[0]] = False
    om[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING:
        om[y0:y1, x0:x1] = False
    rbg = fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30))
    rm = ink(r, rbg)
    rm[: R_BOX[1], :] = False
    rm[R_BOX[3]:, :] = False
    rm[:, : R_BOX[0]] = False
    rm[:, R_BOX[2]:] = False
    rm[R_BADGE[1]:R_BADGE[3], R_BADGE[0]:R_BADGE[2]] = False
    rm[R_TITLE[1]:R_TITLE[3], R_TITLE[0]:R_TITLE[2]] = False
    return om, rm, r.shape[1], r.shape[0]


def main():
    for n in SLIDES:
        om, rm, RW, RH = masks(n)
        fx = 960.0 / RW
        fy = 540.0 / RH
        print(f"===== slide {n}  render {RW}x{RH}  scale x{fx:.5f} y{fy:.5f}")
        for name, (x0, y0, x1, y1) in REGIONS[n].items():
            ob = bbox(om[y0:y1, x0:x1], x0, y0)
            # render region: frame px -> render px
            rx0, rx1 = int(round(x0 / fx)), int(round(x1 / fx))
            ry0, ry1 = int(round(y0 / fy)), int(round(y1 / fy))
            rb = bbox(rm[ry0:ry1, rx0:rx1], rx0, ry0)
            if ob is None and rb is None:
                print(f"  {name:24s} EMPTY both")
                continue
            def f(v):
                return "None" if v is None else f"x{v[0]}-{v[2]} y{v[1]}-{v[3]}"
            print(f"  {name:24s} ORIG {f(ob)} | REND {f(rb)}")
            if ob is not None and rb is not None:
                # render box -> frame scale, then compare with the original box
                b = [round(rb[i] * fx, 1) for i in range(4)]
                b[1] = round(rb[1] * fy, 1)
                b[3] = round(rb[3] * fy, 1)
                d = [round(ob[0] - b[0], 1), round(ob[1] - b[1], 1),
                     round(ob[2] - b[2], 1), round(ob[3] - b[3], 1)]
                print(f"      rend box in frame px: x{b[0]}-{b[2]} y{b[1]}-{b[3]} | "
                      f"delta L{d[0]} T{d[1]} R{d[2]} B{d[3]}")


if __name__ == "__main__":
    main()
