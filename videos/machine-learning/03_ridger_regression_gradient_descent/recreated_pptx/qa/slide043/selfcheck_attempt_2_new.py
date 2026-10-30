#!/usr/bin/env python3
"""Self-check for 043 attempt 2 (post-fix): sliver gone, '=' clearance, ink presence."""
from PIL import Image
import numpy as np

Q = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide043"
ren = np.asarray(Image.open(f"{Q}/render_2.png").convert("RGB")).astype(int)
ren1 = np.asarray(Image.open(f"{Q}/render_1.png").convert("RGB")).astype(int)
rs = ren.shape[0] / 540.0
ok = True

# 1. sliver zone must be panel gray now
zone = ren[int(529 * rs):int(537 * rs), int(300 * rs):int(850 * rs)]
lum = zone.mean(axis=2)
white = (lum > 240).mean()
mean = lum.mean()
print(f"1. sliver zone y529..537: meanlum {mean:.1f} whitefrac {white:.3f} "
      f"-> {'OK (gray, sliver deleted)' if white < 0.05 else 'FAIL (still white)'}")
ok &= white < 0.05

# 2. '=' clearance: horizontal runs (>=4 render-px) STARTING left of the paren
#    bulge (bulge ink starts ~x328.1) must end before x327.5
ends = []
for sy in range(80, 90):
    row = ren[int(sy * rs):int((sy + 1) * rs), int(306 * rs):int(334 * rs)].mean(axis=2)
    dark = (row[0] < 170).astype(int)
    cur = 0
    start = None
    for i, v in enumerate(dark):
        if v:
            if cur == 0:
                start = 306 + i / rs
            cur += 1
        else:
            if cur >= 4 and start < 327:
                ends.append(306 + i / rs)
            cur = 0
    if cur >= 4 and start is not None and start < 327:
        ends.append(306 + len(dark) / rs)
eq_end = max(ends) if ends else 0

print(f"2. '=' bars end x{eq_end:.1f} (paren bulge ~328.1) -> "
      f"{'OK' if eq_end < 327.5 else 'FAIL'}")
ok &= eq_end < 327.5

# 3. changed value row: d(x2) '= -14' region must carry ink (band a=231, x414..470)
zone = ren[int(224 * rs):int(238 * rs), int(414 * rs):int(470 * rs)]
l = zone.mean(axis=2)
ink = int((l < 120).sum())
print(f"3. d(x2) value region ink px: {ink} -> {'OK' if ink > 30 else 'FAIL (empty?)'}")
ok &= ink > 30

# 4. frame containment: ink bbox inside house panel
l = ren.mean(axis=2)
inkmask = l < 200
ys, xs = np.where(inkmask)
print(f"4. ink bbox render px x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} "
      f"(slide x {xs.min()/rs:.0f}..{xs.max()/rs:.0f} y {ys.min()/rs:.0f}..{ys.max()/rs:.0f}) -> "
      f"{'OK' if xs.min() > 100 and xs.max() < 1895 and ys.min() > 80 and ys.max() < 1122 else 'CHECK'}")

# 5. diff vs render_1 (what the fix changed)
d = int((np.abs(ren - ren1).sum(2) > 0).sum())
print(f"5. render_1 vs render_2 changed px: {d} ({100.0*d/ren.shape[0]/ren.shape[1]:.2f}% of frame)")

print("SELF-CHECK:", "PASS" if ok else "FAIL")
