#!/usr/bin/env python3
"""ASCII structure map of an original frame: letterbox bands, red location, dark-ink
row bands, badge circle, and the black bottom strip."""
import sys
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def ascii_map(path, label):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    lum = a.mean(axis=2)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 120) & (r - g > 60) & (r - b > 60)
    dark = lum < 150
    print(f"--- {label} {im.size} ---")
    print("row  lum_mean  red%  dark%")
    for y in range(0, im.size[1], 6):
        sl = slice(y, y + 6)
        print(f"{y:4d}  {lum[sl].mean(axis=1 if False else 1)[0:6].mean():7.1f}  "
              f"{100*red[sl].mean(axis=1)[0:6].mean():5.1f}  {100*dark[sl].mean(axis=1)[0:6].mean():5.1f}")
    # red columns
    rfrac = red.mean(axis=0)
    rcols = np.where(rfrac > 0.5)[0]
    print("  red-heavy cols:", rcols[:20] if len(rcols) else "none", "..." if len(rcols) > 20 else "")
    dcol = dark.mean(axis=0)
    dcols = np.where(dcol > 0.5)[0]
    print("  dark-heavy cols:", dcols[:20] if len(dcols) else "none", "..." if len(dcols) > 20 else "")
    print("  red bbox", box(red), " dark bbox", box(dark))


def box(m):
    ys, xs = np.where(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(ys) else None


if __name__ == "__main__":
    for s in sys.argv[1:]:
        ascii_map(f"{VID}/unique_slides/slide_{s}.jpg", f"orig slide_{s}")
