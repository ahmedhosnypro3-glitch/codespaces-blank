#!/usr/bin/env python3
"""PIL check of judge_2's residual MINORs + verify the two colour changes I made.

A) ORIGINAL ||W||² label colour (NO REG column — the one place colour classifies)
B) ORIGINAL W-vector numeral colour (mean RGB of darkest px: neutral == black)
C) ORIGINAL z-label colour (frame x156..190, y98..120)
D) render_2: any GREEN ink in the middle (lambda=3) column x2 row?
E) render_2: is the RIDGE-3 header band tinted (FAE0C8) or white?
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{NS}/recreated_pptx/qa/slide019/render_2.png").convert("RGB")).astype(int)
SY = r.shape[0] / 540.0
SX = r.shape[1] / 960.0

print("A) ORIGINAL ||W||² (all 3 columns, darkest-15% mean RGB)")
for ci, x0 in enumerate([124, 384, 644]):
    for gi, gy in enumerate([205, 310, 420]):
        sub = o[gy + 68:gy + 84, x0 + 6:x0 + 82]
        lum = sub.sum(axis=2) / 3
        p = sub[lum < np.percentile(lum, 15)]
        print(f"   col{ci} g{gi}: ({p[:,0].mean():.0f},{p[:,1].mean():.0f},{p[:,2].mean():.0f})"
              f"  -> {'BLUE' if p[:,2].mean()-p[:,0].mean() > 25 else ('RED' if p[:,0].mean()-p[:,2].mean() > 25 else 'NEUTRAL')}")

print("\nB) ORIGINAL W-vector numerals (darkest-20% mean RGB, entry strip only)")
for ci, x0 in enumerate([124, 384, 644]):
    for gi, gy in enumerate([205, 310, 420]):
        sub = o[gy + 2:gy + 58, x0 + 46:x0 + 66]
        lum = sub.sum(axis=2) / 3
        p = sub[lum < np.percentile(lum, 20)]
        d = p[:, 0].mean() - p[:, 2].mean()
        print(f"   col{ci} g{gi}: ({p[:,0].mean():.0f},{p[:,1].mean():.0f},{p[:,2].mean():.0f})"
              f"  r-b={d:+.0f} -> {'RED' if d > 25 else ('BLUE' if d < -25 else 'NEUTRAL/black')}")

print("\nC) ORIGINAL z-label cluster (x150..195, y95..120)")
for gi, (x0, x1) in enumerate([(150, 195), (240, 285), (336, 381)]):
    sub = o[95:120, x0:x1]
    lum = sub.sum(axis=2) / 3
    p = sub[lum < np.percentile(lum, 12)]
    d = p[:, 0].mean() - p[:, 2].mean()
    print(f"   z{gi+1}: ({p[:,0].mean():.0f},{p[:,1].mean():.0f},{p[:,2].mean():.0f})"
          f"  r-b={d:+.0f} -> {'RED' if d > 25 else ('BLUE' if d < -25 else 'NEUTRAL/black')}")

print("\nD) render_2: GREEN ink census in lambda=3 column x2 row (y=gy+45..gy+58)")
for gi, gy in enumerate([205, 310, 420]):
    sub = r[int((gy + 45) * SY):int((gy + 58) * SY), int((384 + 142) * SX):int((384 + 286) * SX)]
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    grn = ((gg > 105) & (rr < 125) & (bb < 105) & (gg - bb > 35)).sum()
    red = ((rr > 120) & (gg < 105) & (bb < 105) & (rr - gg > 45)).sum()
    print(f"   g{gi}: green {grn}, red {red} px  (build paints these x2 values BLACK)")

print("\nE) render_2 + ORIGINAL RIDGE-3 header band colour (x400..620, y175..200)")
for nm, img, sfx, sfy in (("render", r, SX, SY), ("orig", o, 1.0, 1.0)):
    sub = img[int(175 * sfy):int(200 * sfy), int(400 * sfx):int(620 * sfx)]
    print(f"   {nm}: mean RGB ({sub[:,:,0].mean():.0f},{sub[:,:,1].mean():.0f},{sub[:,:,2].mean():.0f})"
          f"  (FAE0C8 = 250,224,200 / white = 255,255,255)")
