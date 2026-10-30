"""probe_adj10_discs.py — disc-size census for `chain_full` MINOR 2.

The crop judge claimed "IMG1's first (top) descent dot is markedly larger than the
following dots, creating a strong size step-down" while IMG2's top dot is closer in size to
the others. The build draws all nine discs with `x: px(cx-6.5), y: px(cy-6.5), w: px(13),
h: px(13)` -- identical by construction -- so this census measures the violet-ink extent
inside a +-11 fpx window around each of the nine measured centres in BOTH images
(dots 8/9 read wider in width only because the neighbouring dot's ink falls inside the
window, which is why their width column is larger).

Run from the project root:
  TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp python3 <this file>
Output: probe_adj10_discs_output.txt
  ORIG 9 discs: 13.0..14.0 w / 14.0..15.0 h fpx (uniform)
  REND 9 discs: 14.4..14.9 w / 14.4..14.9 h fpx (uniform; 18.8 w for dots 8/9 = merged
          neighbour ink)
"""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
CENT = [(263.12, 263.41), (283.64, 309.88), (306.85, 341.79), (331.65, 366.36), (354.26, 381.00),
        (373.91, 390.45), (392.40, 396.74), (410.77, 401.75), (428.21, 405.90)]


def load(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(float)
    return a, a.shape[1] / 960.0


for tag, p in (("ORIG", ORIG), ("REND", QA + "render_10.png")):
    im, s = load(p)
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    m = (B > 140) & (B - R > 40) & (G < 150)
    print(f"### {tag} (scale {s:.4f}) -- violet-disc extents around the 9 measured centres")
    for i, (cx, cy) in enumerate(CENT, 1):
        y0, y1 = int((cy - 11) * s), int((cy + 11) * s)
        x0, x1 = int((cx - 11) * s), int((cx + 11) * s)
        sub = m[max(0, y0):y1, max(0, x0):x1]
        if not sub.any():
            print(f"  dot {i}: none")
            continue
        ys, xs = np.where(sub)
        print(f"  dot {i}: bbox x{xs.min()/s+cx-11:.1f}..{xs.max()/s+cx-11:.1f} "
              f"y{ys.min()/s+cy-11:.1f}..{ys.max()/s+cy-11:.1f} -> "
              f"w {xs.max()/s-xs.min()/s+1:.1f} h {ys.max()/s-ys.min()/s+1:.1f} fpx, n={int(sub.sum())}")
print("\n(the build draws all nine discs at w=h=px(13) = 13.0 fpx, identical by construction)")
