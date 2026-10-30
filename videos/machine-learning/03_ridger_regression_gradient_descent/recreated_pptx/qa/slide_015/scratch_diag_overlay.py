"""Prove/disprove: does the coloured-fragment overlay introduce ink that is NOT
in the black base render (a MISLOCATED overlay = spurious duplicate glyphs)?"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_eq_015 as B
from PIL import Image

ASSETS = B.ASSETS
K = B.DPI / 72.0

def asset_alpha(tag):
    im = Image.open(os.path.join(ASSETS, f"eq_015_{tag}.png")).convert("RGBA")
    return np.asarray(im)

def composite_from_base(tag):
    fs, tex, parts = B.EQ[tag]
    base, _ = B.render_canvas(tex, fs, B.BLACK)
    return base, parts, fs

for tag in ["eq1_l1", "eq1_l2", "eq1_l3", "deriv_l1", "deriv_l2", "normal", "solution"]:
    base, parts, fs = composite_from_base(tag)
    comp = asset_alpha(tag)
    base_ink = base[:, :, 3] > 8
    comp_ink = comp[:, :, 3] > 8
    # the asset is a TIGHT crop of the composite; recover its offset in the canvas
    # by matching the composite's ink bbox: crop starts at (cols[0]-PAD, rows[0]-PAD)
    rows = np.where(base_ink.any(axis=1))[0]; cols = np.where(base_ink.any(axis=0))[0]
    x0 = max(int(cols[0]) - B.PAD, 0); y0 = max(int(rows[0]) - B.PAD, 0)
    x1 = min(int(cols[-1]) + 1 + B.PAD, base.shape[1]); y1 = min(int(rows[-1]) + 1 + B.PAD, base.shape[0])
    base_crop = base[y0:y1, x0:x1]
    base_ink_c = base_crop[:, :, 3] > 8
    comp_ink_c = comp_ink
    if base_crop.shape[:2] != comp.shape[:2]:
        print(f"{tag}: crop shape {base_crop.shape[:2]} != asset {comp.shape[:2]} SKIP")
        continue
    extra = comp_ink_c & ~base_ink_c
    rgb = comp[:, :, :3].astype(int)
    blue = (rgb[:,:,2] > 90) & (rgb[:,:,0] < 90) & comp_ink_c
    green = (rgb[:,:,1] > 90) & (rgb[:,:,0] < 80) & comp_ink_c
    # spurious = coloured pixels that do NOT lie on base ink
    blue_extra = int((blue & ~base_ink_c).sum())
    green_extra = int((green & ~base_ink_c).sum())
    total_extra = int(extra.sum())
    print(f"{tag:10s} fs={fs:2d} extra_ink={total_extra:6d}  blue_on_base={int((blue&base_ink_c).sum()):6d} blue_off_base={blue_extra:6d}  green_on_base={int((green&base_ink_c).sum()):6d} green_off_base={green_extra:6d}")
    if blue_extra:
        ys, xs = np.nonzero(blue & ~base_ink_c)
        print(f"           SPURIOUS BLUE: {blue_extra} px, asset-px bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} -> frame x{xs.min()/K:.1f}..{xs.max()/K:.1f} y{ys.min()/K:.1f}..{ys.max()/K:.1f}")
    if green_extra:
        ys, xs = np.nonzero(green & ~base_ink_c)
        print(f"           SPURIOUS GREEN: {green_extra} px, asset-px bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
