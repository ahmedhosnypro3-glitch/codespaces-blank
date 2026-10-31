#!/usr/bin/env python3
"""Lane G diag: dark-ink row profile to locate content bands, chrome excluded."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def dark_ink(arr):
    mx = arr.max(axis=2)
    mn = arr.min(axis=2)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    chromatic = (mx - mn) >= 40
    return ((lum < 150) & (~chromatic)) | ((lum < 150) & chromatic)


def profile(s):
    out = {}
    for tag, p in (("orig", f"{NS}/unique_slides/slide_{s}.jpg"),
                   ("rend", f"{NS}/_pool/tmp_geom_b_geom_2/{s}/render-1.png")):
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        h, w = a.shape[:2]
        m = dark_ink(a)
        # chrome mask (normalized): outer frame border + badge
        ys, xs = np.mgrid[0:h, 0:w]
        nx, ny = xs / w, ys / h
        chrome = ((nx < 0.0135) | (nx > 0.9865) | (ny < 0.023) | (ny > 0.977))
        chrome |= (nx > 0.935) & (nx < 0.973) & (ny > 0.038) & (ny < 0.114)
        m = m & ~chrome
        rows = m.sum(axis=1)
        out[tag] = (h, w, rows, m)
    return out


for s in ("008", "009", "010", "012", "013"):
    d = profile(s)
    print("=" * 70)
    print("SLIDE", s)
    for tag in ("orig", "rend"):
        h, w, rows, m = d[tag]
        nz = np.nonzero(rows > 0)[0]
        print(f"  {tag}: {w}x{h} ink_bg_rows=({nz.min() if len(nz) else -1},{nz.max() if len(nz) else -1}) "
              f"total_ink={int(m.sum())}")
        # print row bands compressed (every 10th row)
        step = max(1, h // 54)
        buf = []
        for y in range(0, h, step):
            v = int(rows[y:y + step].sum())
            buf.append(f"{y:4d}:{'#' * min(28, v // 60)}{v//30:>4d}")
        for i in range(0, len(buf), 3):
            print("      " + "  ".join(buf[i:i + 3]))
