#!/usr/bin/env python3
"""Paren-direction probe: middle-band extremum test.

For each delimiter, take the middle third of the ink rows in a window that
contains only that paren. A '(' has its belly (extreme ink) on the LEFT of its
full span in the middle band (tips point right/inner); a ')' has its belly on
the RIGHT. mid_center < full_center => '(' ; mid_center > full_center => ')'.
Mirrored delimiters show the opposite of the expected side.
"""
import sys
import numpy as np
from PIL import Image

S = 8.3333  # 600dpi band images: img px per slide px (958/115)


def img_x(slide_x, x0=507.0):
    return (slide_x - x0) * S


def probe_rgba(path, windows, y0_img=40, y1_img=760, label=""):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)[:, :, 3].astype(int)
    out = []
    for wname, (wx0, wx1) in windows.items():
        x0, x1 = int(round(wx0)), int(round(wx1))
        win = a[y0_img:y1_img + 1, x0:x1 + 1]
        ink_cols = np.where(win.max(axis=0) > 64)[0]
        if len(ink_cols) == 0:
            out.append(f"  {wname}: NO INK")
            continue
        ink_rows = np.where(win.max(axis=1) > 64)[0]
        r0, r1 = ink_rows.min(), ink_rows.max()
        mid0 = r0 + (r1 - r0) // 3
        mid1 = r0 + 2 * (r1 - r0) // 3
        mid = win[mid0:mid1 + 1]
        mcols = np.where(mid.max(axis=0) > 64)[0]
        mid_c = (mcols.min() + mcols.max()) / 2.0 + x0
        full_c = (ink_cols.min() + ink_cols.max()) / 2.0 + x0
        side = "LEFT" if mid_c < full_c else "RIGHT"
        out.append(
            f"  {wname}: rows[{r0}..{r1}] full_x[{ink_cols.min()+x0}..{ink_cols.max()+x0}] "
            f"mid_x[{mcols.min()+x0}..{mcols.max()+x0}] mid_c={mid_c:.1f} full_c={full_c:.1f} "
            f"belly->{side} => {'(' if side=='LEFT' else ')'}")
    print(f"{path} {label}")
    print("\n".join(out))


def probe_jpg(path, windows, label=""):
    im = Image.open(path).convert("L")
    a = np.array(im, dtype=float)
    print(f"{path} {label}")
    for wname, (wx0, wx1, wy0, wy1) in windows.items():
        x0, x1, y0, y1 = int(round(wx0)), int(round(wx1)), int(round(wy0)), int(round(wy1))
        win = a[y0:y1 + 1, x0:x1 + 1]
        ink = win < 150
        cols = np.where(ink.any(axis=0))[0]
        if len(cols) == 0:
            print(f"  {wname}: NO INK")
            continue
        rows = np.where(ink.any(axis=1))[0]
        r0, r1 = rows.min(), rows.max()
        mid0 = r0 + (r1 - r0) // 3
        mid1 = r0 + 2 * (r1 - r0) // 3
        mcols = np.where(ink[mid0:mid1 + 1].any(axis=0))[0]
        mid_c = (mcols.min() + mcols.max()) / 2.0 + x0
        full_c = (cols.min() + cols.max()) / 2.0 + x0
        side = "LEFT" if mid_c < full_c else "RIGHT"
        print(
            f"  {wname}: rows[{r0+y0}..{r1+y0}] full_x[{cols.min()+x0}..{cols.max()+x0}] "
            f"mid_x[{mcols.min()+x0}..{mcols.max()+x0}] mid_c={mid_c:.1f} full_c={full_c:.1f} "
            f"belly->{side} => {'(' if side=='LEFT' else ')'}")


# ---------- certified media: slide 017 (extracted from pptx) ----------
w17 = {
    "lparen": (img_x(557.0), img_x(562.5)),
    "rparen": (img_x(601.5), img_x(607.5)),
}
for i in (1, 2, 3):
    probe_rgba(f"scratch/tmp_paren017/ppt/media/image-1-{i}.png", w17,
               label="  [017 certified media]")

# ---------- certified media: slide 013 ----------
w13 = {
    "lparen": (img_x(563.8), img_x(568.5)),
    "rparen_b1": (img_x(582.0), img_x(587.5)),
    "rparen_b23": (img_x(608.5), img_x(613.5)),
}
import glob
for p in sorted(glob.glob("scratch/tmp_paren013/ppt/media/*.png")):
    probe_rgba(p, w13, label="  [013 certified media]")

# ---------- on-disk assets: slide 018 ----------
w18 = {
    "lparen": (img_x(557.0), img_x(562.5)),
    "rparen": (img_x(603.0), img_x(608.5)),
}
for i in (1, 2, 3):
    probe_rgba(f"videos/machine-learning/03_ridger_regression_gradient_descent/"
               f"recreated_pptx/build/assets/wbox018_band{i}.png", w18,
               label="  [018 on-disk asset]")

# ---------- originals (ground truth) ----------
ys17 = [(136, 215), (274, 350), (412, 487)]
for n in ("017", "018"):
    wins = {}
    for bi, (yt, yb) in enumerate(ys17, 1):
        wins[f"b{bi}_lparen"] = (556.8, 562.5, yt, yb)
        wins[f"b{bi}_rparen"] = (601.0, 608.0, yt, yb)
    probe_jpg(f"videos/machine-learning/03_ridger_regression_gradient_descent/"
              f"unique_slides/slide_{n}.jpg", wins, label="  [ORIGINAL frame]")

ys13 = [(135, 214), (272, 352), (410, 488)]
wins13 = {}
for bi, (yt, yb) in enumerate(ys13, 1):
    wins13[f"b{bi}_lparen"] = (563.8, 568.5, yt, yb)
    wins13[f"b{bi}_rparen_b1"] = (582.0, 587.5, yt, yb)
    wins13[f"b{bi}_rparen_b23"] = (608.5, 613.5, yt, yb)
probe_jpg("videos/machine-learning/03_ridger_regression_gradient_descent/"
          "unique_slides/slide_013.jpg", wins13, label="  [ORIGINAL frame]")
