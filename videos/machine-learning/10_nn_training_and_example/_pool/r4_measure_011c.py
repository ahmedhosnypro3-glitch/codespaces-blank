#!/usr/bin/env python3
"""scope_r4 adjudication part 3 — slide 011 decisive measurements."""
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
DPI = 150
R = np.asarray(Image.open(f"{VID}/qa/slide011/rejudge/render-1.png").convert("RGB")).astype(int)
Ot = np.asarray(Image.open(f"{VID}/unique_slides/slide_011.jpg").convert("RGB")
                .resize((2001, 1125), Image.LANCZOS)).astype(int)


def box(a, x0, y0, x1, y1):
    return a[int(y0 * DPI):int(y1 * DPI), int(x0 * DPI):int(x1 * DPI)]


def near(a, rgb, tol):
    return np.abs(a - np.array(rgb)).max(axis=2) <= tol


def bb(m):
    ys, xs = np.nonzero(m)
    return None if len(xs) == 0 else (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


print("### M1c: title TEXT span (no frame/badge) vs yellow-word position ###")
for tag, ob in (("RENDER", R), ("ORIGINAL", Ot)):
    t = box(ob, 0.30, 0.24, 12.20, 0.95)
    red = near(t, (192, 0, 0), 90)
    yel = near(t, (255, 215, 0), 70)
    rb, yb = bb(red), bb(yel)
    print(f"{tag}: red title span x {(0.30 + rb[0]/DPI):.2f}-{(0.30 + rb[2]/DPI):.2f}in "
          f"(w={(rb[2]-rb[0])/DPI:.2f}in), y {(0.24+rb[1]/DPI):.2f}-{(0.24+rb[3]/DPI):.2f}in")
    if yb:
        w = (yb[2] - yb[0] + 1) * (yb[3] - yb[1] + 1)
        print(f"        yellow word x {(0.30+yb[0]/DPI):.2f}-{(0.30+yb[2]/DPI):.2f}in "
              f"y {(0.24+yb[1]/DPI):.2f}-{(0.24+yb[3]/DPI):.2f}in  "
              f"fill={int(yel.sum())/w*100:.0f}% of bbox  (100%=solid highlight block)")

print("\n### M2c: does the red 'Sigmoid' overlay destroy equation glyphs? ###")
eq3 = Image.open(f"{VID}/recreated_pptx/build/eq_slide_011/eq3.png").convert("RGBA")
bgim = Image.new("RGBA", eq3.size, (253, 245, 230, 255))
eq3 = Image.alpha_composite(bgim, eq3).convert("L").resize((1176, 35), Image.LANCZOS)
asset = np.asarray(eq3).astype(float)
crop = box(R, 0.5, 6.65, 8.34167, 6.88333).mean(axis=2).astype(float)
a_dark = (asset < 200).sum(axis=0)          # ink pixels per column in the asset
r_dark = (crop < 200).sum(axis=0)           # ink pixels per column in the render
red_cols = (int((5.51 - 0.5) * DPI), int((6.13 - 0.5) * DPI))
print(f"overlay column range in crop: {red_cols} (x 5.51-6.13in)")
for tag, lo, hi in (("under overlay", *red_cols),
                    ("left of overlay", 0, red_cols[0]),
                    ("right of overlay", red_cols[1], len(a_dark))):
    print(f"  {tag}: asset ink px={int(a_dark[lo:hi].sum())}  render ink px={int(r_dark[lo:hi].sum())}  "
          f"retention={r_dark[lo:hi].sum()/max(a_dark[lo:hi].sum(),1)*100:.0f}%")
print(f"  asset ink under overlay: {int(a_dark[red_cols[0]:red_cols[1]].sum())} px "
      f"-> content present in source asset but covered by the red overlay in the render")

print("\n### M3b: clean inter-column wire bands (labels excluded) ###")
bgc = np.array([253, 245, 230])
for tag, ob in (("RENDER", R), ("ORIGINAL", Ot)):
    vals = []
    for x0, x1 in ((4.30, 5.45), (6.35, 7.15), (8.05, 8.95)):
        b = box(ob, x0, 2.6, x1, 5.8)
        m = (np.abs(b - bgc).max(axis=2) > 55) if tag == "RENDER" else (b.mean(axis=2) < 150)
        vals.append(int(m.sum()))
    print(f"{tag}: wire-band ink px = {vals}  (band area each {int(1.15*150)*int(3.2*150)} px)")
