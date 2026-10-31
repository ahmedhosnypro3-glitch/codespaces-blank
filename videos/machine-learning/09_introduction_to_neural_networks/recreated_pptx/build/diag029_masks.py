#!/usr/bin/env python3
"""Diagnostic: list color-mask components in ORIGINAL and RENDER for slide 029."""
import numpy as np
from PIL import Image
from scipy import ndimage

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_029.jpg"
REND = f"{V}/recreated_pptx/build/slide_029_rejudge_rendered-1.png"


def masks(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return {
        "paleyellow": (r > 248) & (g > 248) & (b > 200) & (b < 248),
        "magenta": (r > 180) & (r < 255) & (g > 100) & (g < 210) & (b > 180) & (b < 255),
        "darkred": (r > 140) & (g < 90) & (b < 90),
        "palegreen": (g > 222) & (g < 252) & (r > 190) & (r < 235) & (b > 190) & (b < 235),
        "white": (r > 248) & (g > 248) & (b > 248),
        "legendbeige": (np.abs(a - np.array([242, 228, 208])).sum(axis=2) < 24),
        "lightblue": (np.abs(a - np.array([221, 235, 247])).sum(axis=2) < 24),
        "lightgreen": (np.abs(a - np.array([226, 239, 218])).sum(axis=2) < 24),
    }


def comps(mask, minsize=40):
    lab, n = ndimage.label(mask)
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        npx = int((lab[sl] == i).sum())
        if npx < minsize:
            continue
        ys, xs = sl
        out.append((xs.start, ys.start, xs.stop - 1, ys.stop - 1, npx))
    out.sort(key=lambda z: (z[1], z[0]))
    return out


for path, label in [(ORIG, "ORIGINAL"), (REND, "RENDER")]:
    img = Image.open(path).convert("RGB")
    a = np.asarray(img).astype(int)
    h, w = a.shape[:2]
    ppi = w / 13.3333
    M = masks(a)
    print(f"\n########## {label}  {w}x{h}  ppi={ppi:.2f} ##########")
    for k, m in M.items():
        cs = comps(m, 40)
        if not cs:
            print(f"{k:12s}: none")
            continue
        print(f"{k:12s}: {len(cs)} component(s) >=40px (showing <=16)")
        for c in cs[:16]:
            print(f"    px {c[0]:4d},{c[1]:4d},{c[2]:4d},{c[3]:4d} | "
                  f"in x {c[0]/ppi:5.2f}-{c[2]/ppi:5.2f}  y {c[1]/ppi:5.2f}-{c[3]/ppi:5.2f}  n={c[4]}")
