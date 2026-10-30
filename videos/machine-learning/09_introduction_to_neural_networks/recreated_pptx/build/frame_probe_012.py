#!/usr/bin/env python3
"""Compare the ORIGINAL lecture frames' own red border inset across slides,
and measure slide_012 / slide_013 region geometry robustly.

Frame geometry differs from content geometry: the deck's house frame is a
mandated 0.15in inset, but each ORIGINAL frame also carries the lecture
deck's own border. This script shows whether that border is shared.
"""
import sys
import numpy as np
from PIL import Image

SW, SH = 13.333, 7.5


def load(p):
    im = Image.open(p).convert("RGB")
    return np.array(im).astype(int), im.size[0], im.size[1]


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 125) & ((r - g) > 45) & ((r - b) > 45)


def frame_inset(path):
    a, W, H = load(path)
    R = redmask(a)
    vprof = R.sum(axis=0)
    hprof = R.sum(axis=1)
    # long vertical red runs (>=70% of height) and horizontal (>=70% of width)
    vs = [x for x in range(W) if vprof[x] > H * 0.70]
    hs = [y for y in range(H) if hprof[y] > W * 0.70]
    out = {}
    if vs:
        out["vcols_in"] = [round(vs[0] / W * SW, 3), round(vs[-1] / W * SW, 3)]
    if hs:
        out["hrows_in"] = [round(hs[0] / H * SH, 3), round(hs[-1] / H * SH, 3)]
    out["size"] = f"{W}x{H}"
    return out


def robust_bbox(a, x0f, y0f, x1f, y1f, mode):
    """Structure bbox inside a region: pixels differing from local bg."""
    H, W = a.shape[:2]
    x0, x1 = int(x0f * W), int(x1f * W)
    y0, y1 = int(y0f * H), int(y1f * H)
    reg = a[y0:y1, x0:x1]
    bg = np.median(reg.reshape(-1, 3), axis=0)
    diff = np.abs(reg - bg).max(axis=2)
    mask = diff > 28
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return (round((x0 + xs.min()) / W * SW, 3), round((y0 + ys.min()) / H * SH, 3),
            round((x0 + xs.max()) / W * SW, 3), round((y0 + ys.max()) / H * SH, 3),
            int(len(xs)))


if __name__ == "__main__":
    base = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
    print("=== ORIGINAL frames: lecture deck's own red border inset (in) ===")
    for n in [5, 9, 12, 13, 14]:
        p = f"{base}/unique_slides/slide_{n:03d}.jpg"
        try:
            print(f"  slide_{n:03d}: {frame_inset(p)}")
        except Exception as e:
            print(f"  slide_{n:03d}: ERROR {e}")

    for label, path in [("ORIG-012", f"{base}/unique_slides/slide_012.jpg"),
                        ("REND-012", f"{base}/recreated_pptx/build/slide_012_rendered-1.png"),
                        ("ORIG-013", f"{base}/unique_slides/slide_013.jpg"),
                        ("REND-013", f"{base}/recreated_pptx/build/slide_013_rendered.png")]:
        try:
            a, W, H = load(path)
        except Exception as e:
            print(f"{label}: load error {e}")
            continue
        print(f"\n=== {label} ({W}x{H}) region structure bboxes (in) ===")
        regions = {
            "title_band":  (0.02, 0.02, 0.98, 0.20),
            "table_zone":  (0.04, 0.18, 0.40, 0.62),
            "plot_zone":   (0.42, 0.06, 0.96, 0.72),
            "net_zone":    (0.04, 0.62, 0.56, 0.95),
            "eq_zone":     (0.50, 0.70, 0.96, 0.93),
        }
        for nm, (a0, b0, a1, b1) in regions.items():
            bb = robust_bbox(a, a0, b0, a1, b1, "diff")
            print(f"  {nm:<11} {bb}")
