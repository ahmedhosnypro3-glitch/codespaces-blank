#!/usr/bin/env python3
"""Lane G (b_geom_4): per-region geometry verification.

Method
------
The recreation's build scripts declare element geometry in SOURCE-FRAME px of the
960x540 capture, which maps linearly onto the 13.33x7.5in canvas (PX = 13.33/960).
The LO render is that pptx at 150dpi (2001x1125), so:

    render_px * 960 / render_width  ==  source px  ==  original JPEG px

Both images are reduced to a 960x540 SOURCE-FRAME grid and the ink bounding box
of each named region is measured in each, then compared.

House chrome is excluded from BOTH sides before measuring:
  - render: red frame (0.15in inset), yellow badge, title box band
  - original: its own outer border ring + white video letterbox + title band
so only slide-specific content edges are compared.

Tolerance: ~4px at 150dpi == ~2px at source-frame scale, per LANE_PROTOCOL.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SCOPE = "b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]
TOL = 2.0      # source-frame px

O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
R_IN, R_OUT = 26, 1975
R_BADGE = (1872, 45, 1947, 120)
R_TITLE = (90, 42, 1910, 130)

# Named regions, source-frame px, declared in / measured from the build scripts.
REGIONS = {
    "025": [
        ("title_block",            (38, 43, 922, 100)),
        ("header_long_chain",      (38, 100, 430, 130)),
        ("eq_boxes_left",          (38, 130, 430, 305)),
        ("nn_diagram",             (430, 100, 922, 305)),
        ("error_bar_class",        (820, 130, 922, 305)),
        ("charts_bottom",          (38, 305, 922, 520)),
    ],
    "026": [
        ("title_block",            (38, 43, 922, 105)),
        ("subtitle_line1",         (38, 200, 922, 285)),
        ("subtitle_line2",         (38, 285, 922, 380)),
        ("lower_blank",            (38, 380, 922, 540)),
    ],
    "027": [
        ("title_block",            (38, 43, 922, 100)),
        ("nn_diagram",             (170, 100, 866, 262)),
        ("forward_header",         (38, 262, 650, 280)),
        ("calc_box1",              (50, 280, 370, 425)),
        ("green_box_a",            (640, 280, 897, 425)),
        ("calc_box2",              (50, 432, 610, 532)),
    ],
    "029": [
        ("title_block",            (38, 43, 922, 100)),
        ("red_diagram_box",        (140, 200, 834, 400)),
        ("input_col_vector",       (160, 230, 215, 340)),
        ("target_col_vector",      (650, 238, 695, 318)),
    ],
    "032": [
        ("title_block",            (38, 43, 922, 100)),
        ("top_panel",              (98, 87, 827, 290)),
        ("bottom_panel",           (98, 328, 827, 530)),
    ],
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


def bbox(m, ox=0, oy=0):
    rr = np.where(m.any(axis=1))[0]
    cc = np.where(m.any(axis=0))[0]
    if len(rr) == 0:
        return None
    return int(cc[0]) + ox, int(rr[0]) + oy, int(cc[-1]) + ox, int(rr[-1]) + oy


def measure(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    om = ink(o, fast_bg(o, O_BOX))
    om[: O_BOX[1], :] = om[O_BOX[3]:, :] = False
    om[:, : O_BOX[0]] = om[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING:
        om[y0:y1, x0:x1] = False
    rm = ink(r, fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30)))
    rm[:R_IN, :] = rm[1099:, :] = False
    rm[:, :R_IN] = rm[:, R_OUT:] = False
    rm[R_BADGE[1]:R_BADGE[3], R_BADGE[0]:R_BADGE[2]] = False
    rm[R_TITLE[1]:R_TITLE[3], R_TITLE[0]:R_TITLE[2]] = False
    fx, fy = 960.0 / r.shape[1], 540.0 / r.shape[0]
    return om, rm, fx, fy, r.shape


def main():
    print(f"# Lane G {SCOPE} — per-region ink-edge deltas (source-frame px, "
          f"tol {TOL})")
    for n in SLIDES:
        om, rm, fx, fy, rshape = measure(n)
        print(f"\n## slide {n}  render {rshape[1]}x{rshape[0]}")
        for name, (x0, y0, x1, y1) in REGIONS[n]:
            ob = bbox(om[y0:y1, x0:x1], x0, y0)
            ry0, ry1 = int(round(y0 / fy)), int(round(y1 / fy))
            rx0, rx1 = int(round(x0 / fx)), int(round(x1 / fx))
            rb = bbox(rm[ry0:ry1, rx0:rx1], rx0, ry0)
            if ob is None and rb is None:
                print(f"  {name:20s} EMPTY in both (no ink — no finding)")
                continue
            if rb is None:
                print(f"  {name:20s} ORIG {ob} REND none -> MISSING CONTENT")
                continue
            if ob is None:
                print(f"  {name:20s} ORIG none REND {rb} -> EXTRA CONTENT")
                continue
            # render box -> source-frame px
            s = (round(rb[0] * fx, 1), round(rb[1] * fy, 1),
                 round(rb[2] * fx, 1), round(rb[3] * fy, 1))
            d = (round(ob[0] - s[0], 1), round(ob[1] - s[1], 1),
                 round(ob[2] - s[2], 1), round(ob[3] - s[3], 1))
            worst = max(abs(d[0]), abs(d[1]), abs(d[2]), abs(d[3]))
            verdict = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
            print(f"  {name:20s} ORIG x{ob[0]}-{ob[2]} y{ob[1]}-{ob[3]} | "
                  f"REND(f) x{s[0]}-{s[2]} y{s[1]}-{s[3]} | "
                  f"d L{d[0]} T{d[1]} R{d[2]} B{d[3]} | worst {worst} => {verdict}")


if __name__ == "__main__":
    main()
