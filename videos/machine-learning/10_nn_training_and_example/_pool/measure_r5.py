#!/usr/bin/env python3
"""PIL color/ink measurement of a recreation render vs its original frame.

Usage: measure_r5.py <NNN> <x0> <y0> <x1> <y1> [tag]
Region is given in ORIGINAL 960x540 frame pixels; the render is scaled to
that frame so both are measured on the same coordinate basis.
"""
import sys
from PIL import Image
import numpy as np

COLORS = {
    "red":    ((255, 0, 0), (204, 0, 0)),
    "blue":   ((0, 0, 204), (0, 0, 255)),
    "green":  ((0, 204, 0), (144, 238, 144)),
    "orange": ((255, 102, 0), (255, 218, 185)),
    "yellow": ((255, 255, 153), (255, 255, 224)),
    "pink":   ((255, 182, 193), (255, 153, 255)),
    "magenta":((204, 0, 204), (255, 0, 255)),
}


def frame(path, size=None):
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(int)


def stats(a, x0, y0, x1, y1, name):
    reg = a[y0:y1, x0:x1]
    h, w, _ = reg.shape
    flat = reg.reshape(-1, 3)
    out = {"name": name, "px": w * h}
    for label, variants in COLORS.items():
        n = 0
        for c in variants:
            n += int((np.abs(flat - np.array(c)).sum(axis=1) < 40).sum())
        out[label] = n
    # ink = pixels that are not near-background and not pale panel fill
    bg = (np.abs(flat - np.array([232, 232, 232])).sum(axis=1) < 18)
    pale = (flat.min(axis=1) > 205) & (flat.max(axis=1) - flat.min(axis=1) < 26)
    out["ink"] = int((~(bg | pale)).sum())
    out["ink_pct"] = round(100.0 * out["ink"] / (w * h), 2)
    return out


def main():
    n = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
    tag = sys.argv[6] if len(sys.argv) > 6 else ""
    base = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
    ren = frame(f"{base}/qa/slide{n}/rejudge/render-1.png")
    org = frame(f"{base}/unique_slides/slide_{n}.jpg")
    # render 2001x1125 -> original 960x540 basis
    ren_small = frame(f"{base}/qa/slide{n}/rejudge/render-1.png", size=(960, 540))
    r = stats(ren_small, x0, y0, x1, y1, "render")
    o = stats(org, x0, y0, x1, y1, "original")
    print(f"slide {n} region=({x0},{y0})-({x1},{y1}) {tag}")
    print(f"{'metric':10s} {'render':>10s} {'original':>10s} {'delta':>10s} {'orig/rend':>10s}")
    for k in r:
        if k in ("name", "px"):
            continue
        delta = o[k] - r[k]
        ratio = (o[k] / r[k]) if r[k] else float("inf")
        print(f"{k:10s} {r[k]:>10} {o[k]:>10} {delta:>10} {ratio:>10.2f}")


main()
