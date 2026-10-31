#!/usr/bin/env python3
"""verify_005.py — closed-loop geometry/colour check for slide 005.

Compares the rendered recreation (150 dpi, 2001x1125) against the original
lecture frame (960x540, 1 px = 1 pt). Every element keeps its measured
original-frame box; the render is scaled back down to 960x540 before
measuring, so the reported deltas are in original px (1 px = 1 pt).

Usage: python3 verify_005.py
"""
from PIL import Image
import numpy as np
import sys

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
B = V + "recreated_pptx/build/"
RENDER = B + "slide_005_rejudge_rendered-1.png"
ORIG = V + "unique_slides/slide_005.jpg"

TOL = 4  # original px (=1pt) tolerated at 150 dpi

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r_full = Image.open(RENDER)
if r_full.size != (2001, 1125):
    print(f"WARNING render is {r_full.size}, expected 2001x1125")
r = np.asarray(r_full.resize((960, 540), Image.LANCZOS)).astype(int)


def ink(a, thr=60):
    return np.abs(a - 255).max(axis=2) > thr


def bbox_of(mask, x0, x1, y0, y1, region=None):
    """Bounding box of ink inside (x0,x1,y0,y1) in original px."""
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())


def cat_classify(a):
    """Classify each pixel: R=red, B=blue, K=black/ink, .=white."""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (r > 110) & (r - g > 25) & (r - b > 25)
    blue = (b > 90) & (b - r > 50) & (g < 170)
    dark = (r < 150) & (g < 150) & (b < 150) & (np.abs(a - 255).max(axis=2) > 60)
    return red, blue, dark


# ---------------------------------------------------------------------------
# element checks: (label, category, original bbox, search window)
# category: "red" | "blue" | "dark" | "any"
CHECKS = [
    # top-left panel
    ("X = #1 (x87)",            "any",  (87, 113, 160, 173), (82, 140, 155, 180)),
    ("vector1 brackets",        "any",  (116, 140, 116, 223), (110, 148, 110, 232)),
    ("vector1 rows",            "any",  (122, 135, 122, 229), (118, 140, 115, 232)),
    ("red => arrow",            "red",  (178, 194, 161, 170), (172, 200, 155, 176)),
    ("X = #2 (x219)",           "any",  (219, 245, 160, 173), (214, 252, 155, 180)),
    ("augmented '1' red",       "red",  (258, 265, 107, 120), (252, 270, 102, 125)),
    ("augmented vec brackets",  "any",  (248, 273, 107, 231), (243, 280, 102, 236)),
    ("Augmented Vector label",  "blue", (298, 406, 161, 175), (290, 412, 155, 180)),
    # top-right panel
    ("W (red)",                 "red",  (560, 575, 159, 174), (554, 580, 153, 179)),
    ("W-vec 'b' (blue)",        "blue", (602, 611, 106, 120), (596, 616, 100, 125)),
    ("W-vec brackets",          "any",  (592, 620, 107, 231), (586, 626, 102, 236)),
    ("Model Weights label",     "blue", (670, 761, 161, 175), (664, 767, 155, 180)),
    # banner
    ("equation ink",            "any",  (88, 522, 283, 305), (82, 530, 278, 310)),
    ("red X in d(X)",           "red",  (108, 122, 287, 302), (102, 130, 282, 307)),
    ("red b*1",                 "red",  (426, 457, 287, 301), (420, 462, 282, 306)),
    ("red => (banner)",         "red",  (503, 522, 287, 298), (498, 528, 282, 303)),
    ("rule bracket left",       "any",  (543, 546, 263, 330), (539, 551, 258, 335)),
    ("rule bracket right",      "any",  (748, 750, 263, 330), (744, 754, 258, 335)),
    ("rule text lines",         "blue", (555, 739, 267, 325), (550, 745, 262, 330)),
    # caption
    ("caption line 1",          "any",  (656, 791, 407, 418), (650, 797, 402, 443)),
    ("caption line 2",          "any",  (684, 760, 423, 436), (650, 797, 402, 443)),
    ("caption box",             "any",  (629, 818, 400, 441), (625, 822, 396, 445)),
    # bottom diagram
    ("input column",            "any",  (252, 264, 357, 499), (246, 270, 352, 504)),
    ("weight column",           "blue", (290, 305, 359, 498), (284, 310, 354, 503)),
    ("bias '1' (red)",          "red",  (252, 257, 489, 499), (246, 264, 484, 504)),
    ("Sigma circle",            "any",  (407, 443, 403, 439), (402, 448, 398, 444)),
    ("step box",                "any",  (461, 513, 406, 439), (456, 518, 401, 444)),
    ("red arrow sum->box",      "red",  (444, 466, 417, 425), (439, 471, 412, 430)),
    ("red arrow box->O/P",      "red",  (509, 573, 417, 425), (504, 578, 412, 430)),
    ("O/P label",               "any",  (582, 604, 416, 425), (576, 610, 411, 430)),
]


def mask_for(name, cat):
    if cat == "red":
        return red
    if cat == "blue":
        return blue
    if cat == "dark":
        return dark
    return ink(np.zeros_like(o))  # unused


# build masks for both images
o_red, o_blue, o_dark = cat_classify(o)
r_red, r_blue, r_dark = cat_classify(r)
o_ink = ink(o)
r_ink = ink(r)

fails = []
print(f"{'element':28s} {'orig bbox':26s} {'rendered bbox':26s} delta")
print("-" * 100)
for label, cat, obox, win in CHECKS:
    if cat == "red":
        om, rm = o_red, r_red
    elif cat == "blue":
        om, rm = o_blue, r_blue
    elif cat == "dark":
        om, rm = o_dark, r_dark
    else:
        om, rm = o_ink, r_ink
    ob = bbox_of(om, *win)
    rb = bbox_of(rm, *win)
    if ob is None and rb is None:
        print(f"{label:28s} {'(absent)':26s} {'(absent)':26s}")
        continue
    if ob is None or rb is None:
        print(f"{label:28s} {str(ob):26s} {str(rb):26s} MISSING")
        fails.append(label)
        continue
    # compare bboxes: allowed to be wider (sub-sampling blur), so use the
    # original box as the reference and measure offset + whether the render
    # x-range overlaps the original's within tolerance
    dx0 = abs(ob[0] - rb[0])
    dx1 = abs(ob[1] - rb[1])
    dy0 = abs(ob[2] - rb[2])
    dy1 = abs(ob[3] - rb[3])
    ok = dx0 <= TOL and dx1 <= TOL and dy0 <= TOL and dy1 <= TOL
    flag = "" if ok else "  <-- OUT"
    if not ok:
        fails.append(label)
    print(f"{label:28s} {str(ob):26s} {str(rb):26s} "
          f"d=({dx0},{dx1},{dy0},{dy1}){flag}")

# ---------------------------------------------------------------------------
# colour census: red / blue / black pixel counts per region
print("\nColour census (ink pixels per category):")
regions = {
    "top-left panel":  (82, 419, 87, 246),
    "top-right panel": (528, 793, 88, 246),
    "banner":          (81, 767, 254, 342),
    "diagram":         (227, 613, 349, 508),
    "caption":         (629, 818, 400, 441),
}
for name, (x0, x1, y0, y1) in regions.items():
    row = []
    for lbl, om, rm in (("red", o_red, r_red), ("blue", o_blue, r_blue),
                        ("dark", o_dark, r_dark)):
        no = int(om[y0:y1, x0:x1].sum())
        nr = int(rm[y0:y1, x0:x1].sum())
        row.append(f"{lbl} orig={no} new={nr}")
    print(f"  {name:16s} " + "  ".join(row))

print()
if fails:
    print("FAIL: %d element(s) out of tolerance: %s" % (len(fails), ", ".join(fails)))
    sys.exit(1)
print(f"PASS: all {len(CHECKS)} elements within {TOL} px")
