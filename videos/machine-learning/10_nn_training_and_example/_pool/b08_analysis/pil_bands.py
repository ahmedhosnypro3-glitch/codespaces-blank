#!/usr/bin/env python3
"""Row/column ink-band comparison, chrome excluded.
Compares content-region ink bands between render and original."""
import sys
from PIL import Image
import numpy as np

def profile(im, box, thresh=235):
    a = np.asarray(im.convert("L"), dtype=np.uint8)
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1]
    m = reg < thresh
    rows = m.mean(axis=1)
    cols = m.mean(axis=0)
    return m, rows, cols

def bands(v, thr=0.02):
    idx = np.where(v > thr)[0]
    out = []
    if len(idx) == 0:
        return out
    s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i - p > 3:
            out.append((s, p)); s = i
        p = i
    out.append((s, p))
    return out

def main(render_path, orig_path):
    r = Image.open(render_path); o = Image.open(orig_path)
    W, H = r.size
    # content region inside house frame (0.30in..13.03in x, 0.30..7.35 y) at 150dpi => 45..1954, 45..1102
    box_r = (50, 50, W - 50, H - 40)
    # original: skip outer margins 30px
    box_o = (30, 30, 930, 535)
    mr, rr, cr = profile(r, box_r)
    mo, ro, co = profile(o, box_o)
    print("RENDER row bands (content region y offsets):", bands(rr))
    print("ORIG   row bands (content region y offsets):", bands(ro))
    print()
    # normalize to fraction-of-region and print sampled row profile
    print("row profile comparison (normalized, 20 bands):")
    n = 20
    h_r = len(rr); h_o = len(ro)
    for i in range(n):
        a1 = rr[i*h_r//n:(i+1)*h_r//n].mean()
        b1 = ro[i*h_o//n:(i+1)*h_o//n].mean()
        print(f"band {i:2d} render={a1:.4f} orig={b1:.4f} diff={a1-b1:+.4f}")
    print()
    print("RENDER col bands:", bands(cr, 0.03))
    print("ORIG   col bands:", bands(co, 0.03))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
