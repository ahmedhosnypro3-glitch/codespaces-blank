#!/usr/bin/env python3
"""Lane G diag v2: contiguous content bands (rows/cols) in slide-inch coordinates."""
import numpy as np
from PIL import Image
from scipy import ndimage

import importlib.util
spec = importlib.util.spec_from_file_location(
    "m", "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/bgeom2_measure.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"

for s in ("008", "009", "010", "012", "013"):
    print("=" * 74)
    print("SLIDE", s)
    for tag, path, kind in (("ORIG", f"{NS}/unique_slides/slide_{s}.jpg", "orig"),
                            ("REND", f"{NS}/_pool/tmp_geom_b_geom_2/{s}/render-1.png", "rend")):
        arr, mask, ts, size = m.build(path, kind)
        h, w = mask.shape
        ys, xs = np.nonzero(mask)
        sx0, sx1 = ts["x"](xs.min()), ts["x"](xs.max())
        sy0, sy1 = ts["y"](ys.min()), ts["y"](ys.max())
        print(f"  {tag} {w}x{h} ALL ink bbox x[{sx0:.2f},{sx1:.2f}] y[{sy0:.2f},{sy1:.2f}] n={mask.sum()}")
        # row bands (gap >= 0.25in closes a band)
        rows = mask.sum(axis=1)
        gap = max(2, int(0.25 / (ts["y"](1) - ts["y"](0))))
        bands, cur, last = [], None, -10**9
        for y in range(h):
            if rows[y] > 0:
                if cur is None:
                    cur = y
                last = y
            else:
                if cur is not None and y - last > gap:
                    bands.append((cur, last)); cur = None
        if cur is not None:
            bands.append((cur, last))
        for (a, b) in bands:
            sub = mask[a:b + 1]
            ys2, xs2 = np.nonzero(sub)
            print(f"      rowband y[{ts['y'](a):5.2f},{ts['y'](b):5.2f}] x[{ts['x'](xs2.min()):6.2f},"
                  f"{ts['x'](xs2.max()):6.2f}] ink={int(sub.sum())} h={(b-a+1)/size[1]*7.5:.2f}in")
