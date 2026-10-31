#!/usr/bin/env python3
"""Badge geometry + graph interior plot geometry (axes, tints) for slide_021."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# --- badge: yellow circle, restrict to y<110 so we exclude the graph frame
yellow = (R > 230) & (G > 230) & (B > 120) & (B < 200)
reg = yellow[0:110, 840:920]
ys, xs = np.nonzero(reg)
print("badge yellow bbox x", 840 + xs.min(), "..", 840 + xs.max(),
      " y", ys.min(), "..", ys.max(), "n=", len(xs))
cx = (840 + xs.min() + 840 + xs.max()) / 2
cy = (ys.min() + ys.max()) / 2
print("badge center", cx, cy, "w", 840 + xs.max() - 840 + xs.min() + 1, "h", ys.max() - ys.min() + 1)

# circle edge check: measure width at mid-height row
row = cy
sel = np.nonzero(yellow[int(row), 840:920])[0]
print("badge width at y=", int(row), ":", (840 + sel.max()) - (840 + sel.min()) + 1)

# --- dark numeral inside badge
dark = (R < 130) & (G < 130) & (B < 130)
reg2 = dark[int(cy - 12):int(cy + 13), int(cx - 14):int(cx + 15)]
ys2, xs2 = np.nonzero(reg2)
if len(xs2):
    print("numeral bbox x", int(cx - 14) + xs2.min(), "..", int(cx - 14) + xs2.max(),
          " y", int(cy - 12) + ys2.min(), "..", int(cy - 12) + ys2.max(), "n=", len(xs2))

# --- graph frames: interior plot area (inside the blue border)
FRAMES = {"TL": (121, 109, 400, 272), "TR": (563, 109, 842, 275),
          "BL": (121, 346, 400, 508), "BR": (564, 346, 842, 508)}
for name, (x0, y0, x1, y1) in FRAMES.items():
    # interior after 3px border + 2px white margin
    ix0, iy0, ix1, iy1 = x0 + 4, y0 + 4, x1 - 4, y1 - 4
    print(f"\n== {name} frame x{x0}..{x1} y{y0}..{y1} (w={x1-x0+1},h={y1-y0+1}) interior x{ix0}..{ix1} y{iy0}..{iy1}")

    # tick label text bands outside the plot: bottom rows/last cols
    sub = a[iy0:iy1 + 1, ix0:ix1 + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    red = (sr > 120) & (sr - sg > 45) & (sr - sb > 45)
    blackish = (sr < 120) & (sg < 120) & (sb < 120)
    gray = (abs(sr - sg) < 14) & (abs(sg - sb) < 14) & (sr > 130) & (sr < 250)

    ys_r, xs_r = np.nonzero(red)
    print(f"  red curve ink bbox x{ix0+xs_r.min()}..{ix0+xs_r.max()} y{iy0+ys_r.min()}..{iy0+ys_r.max()} n={len(xs_r)}" if len(xs_r) else "  red: none")

    # gray gridlines: columns with many gray px
    gcol = gray.sum(axis=0)
    grow = gray.sum(axis=1)
    print("  gray grid cols:", [(ix0 + i, int(gcol[i])) for i in range(len(gcol)) if gcol[i] > (iy1 - iy0) * 0.4])
    print("  gray grid rows:", [(iy0 + i, int(grow[i])) for i in range(len(grow)) if grow[i] > (ix1 - ix0) * 0.4])

    # black axis-ish lines: strong columns/rows
    bcol = blackish.sum(axis=0)
    brow = blackish.sum(axis=1)
    print("  black cols >40%:", [(ix0 + i, int(bcol[i])) for i in range(len(bcol)) if bcol[i] > (iy1 - iy0) * 0.4])
    print("  black rows >40%:", [(iy0 + i, int(brow[i])) for i in range(len(brow)) if brow[i] > (ix1 - ix0) * 0.4])

    # multi-color curves (ELU panel): look for blue/orange/green
    for cname, mask in [("blue", (sb - sr > 40) & (sb - sg > 30)),
                        ("orange", (sr > 180) & (sg > 90) & (sg < 190) & (sb < 110) & (sr - sb > 60)),
                        ("green", (sg - sr > 40) & (sg - sb > 25))]:
        ym, xm = np.nonzero(mask)
        if len(xm):
            print(f"  {cname} ink n={len(xm)} bbox x{ix0+xm.min()}..{ix0+xm.max()} y{iy0+ym.min()}..{iy0+ym.max()}")
