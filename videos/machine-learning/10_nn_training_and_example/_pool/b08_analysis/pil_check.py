#!/usr/bin/env python3
"""PIL closed-loop check: render (2000x1125 @150dpi) vs original frame (960x540).
1 render px = 1 pt; original px scale = 2000/960 = 2.0833 render px per orig px.
Reports ink-region bounding boxes and coarse region alignment."""
import sys
from PIL import Image
import numpy as np

def ink_mask(im, thresh=235):
    a = np.asarray(im.convert("L"), dtype=np.uint8)
    return a < thresh

def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (xs.min(), ys.min(), xs.max(), ys.max(), mask.sum())

def main(render_path, orig_path):
    r = Image.open(render_path)
    o = Image.open(orig_path)
    rm = ink_mask(r)
    om = ink_mask(o)
    print("render", r.size, "orig", o.size)
    print("render ink bbox (x0,y0,x1,y1,count):", bbox(rm))
    print("orig   ink bbox (x0,y0,x1,y1,count):", bbox(om))
    # resample orig ink mask to render scale
    om_up = np.asarray(Image.fromarray((om * 255).astype(np.uint8)).resize(r.size, Image.NEAREST)) > 0
    # coarse grid agreement: divide render into 12x7 cells, fraction of ink in each for both
    H, W = r.size[1], r.size[0]
    gh, gw = 7, 12
    print("cell ink-fraction agreement (render vs orig-upscaled), per row:")
    for gy in range(gh):
        row = []
        for gx in range(gw):
            y0, y1 = gy * H // gh, (gy + 1) * H // gh
            x0, x1 = gx * W // gw, (gx + 1) * W // gw
            fr = rm[y0:y1, x0:x1].mean()
            fo = om_up[y0:y1, x0:x1].mean()
            d = fr - fo
            row.append(f"{d:+.3f}")
        print(" ".join(row))
    # overall correlation of downsampled masks
    rs = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).resize((96, 54), Image.BILINEAR)) / 255.0
    os_ = np.asarray(Image.fromarray((om * 255).astype(np.uint8)).resize((96, 54), Image.BILINEAR)) / 255.0
    corr = np.corrcoef(rs.ravel(), os_.ravel())[0, 1]
    print(f"downsampled ink-mask correlation: {corr:.4f}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
