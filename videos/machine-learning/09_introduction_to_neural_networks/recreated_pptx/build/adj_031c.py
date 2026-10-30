#!/usr/bin/env python3
"""Left-edge ink analysis of equation PNGs (detect clipped first glyph) + ink bbox."""
from PIL import Image
import numpy as np, os

B = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
for f in ["eq_net3","eq_net4","eq_net5","eq_net6","eq_net7","eq_O3","eq_O4","eq_O5","eq_O6","eq_O7",
          "eq_Net3","eq_Net6"]:
    p = f"{B}/{f}.png"
    if not os.path.exists(p): continue
    im = Image.open(p).convert("RGBA")
    a = np.array(im)
    alpha = a[...,3]
    ink = alpha > 25
    ys, xs = np.where(ink)
    if len(xs)==0:
        print(f, "EMPTY"); continue
    # left 12 columns ink counts
    left = ink[:, :12].sum(axis=0)
    print(f"{f:10s} size={im.size} inkbbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] "
          f"leftcols={left.tolist()} rightcols={ink[:, -12:].sum(axis=0).tolist()}")
