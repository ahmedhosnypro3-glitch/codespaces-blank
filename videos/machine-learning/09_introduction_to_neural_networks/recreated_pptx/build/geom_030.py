# numpy/scipy geometry extraction for slide_030 (original + render)
import numpy as np
from PIL import Image
from scipy import ndimage

def masks(a):
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    m = {}
    m["red"] = (r > 140) & (g < 100) & (b < 100) & ((r - g) > 55)
    m["cream"] = (r > 240) & (g > 235) & (b < 210)   # badge FFF9C4
    m["pink"] = (r > 225) & (r < 255) & (g > 180) & (g < 220) & (b > 150) & (b < 195)
    m["yellow"] = (r > 215) & (g > 175) & (b < 180)
    m["orange"] = (r > 210) & (g > 135) & (g < 215) & (b < 185) & ~m["yellow"]
    m["blue"] = (b > 120) & ((b - r) > 45) & ((b - g) > 45)
    m["green"] = (g > 105) & ((g - r) > 38) & ((g - b) > 38)
    m["dark"] = (r + g + b) < 300
    return m

def comps(mask, minpx=40):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) >= minpx:
            out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
    return sorted(out, key=lambda t: -t[4])

for path, tag in [("unique_slides/slide_030.jpg", "ORIG"),
                  ("recreated_pptx/build/slide_030_rendered_v2-1.png", "REND")]:
    a = np.asarray(Image.open(path).convert("RGB"))
    H, W = a.shape[:2]
    m = masks(a)
    print(f"===== {tag} {W}x{H} =====")
    for k in ["red", "cream", "pink", "yellow", "orange", "blue", "green"]:
        cs = comps(m[k])
        top = cs[:6]
        print(f"{k}: n={len(cs)} top(px, x0..x1, y0..y1)")
        for c in top:
            print(f"    x {c[0]:4d}-{c[1]:4d} y {c[2]:4d}-{c[3]:4d} ({c[4]}px)  fn x{c[0]/W:.3f}-{c[1]/W:.3f} y{c[2]/H:.3f}-{c[3]/H:.3f}")
