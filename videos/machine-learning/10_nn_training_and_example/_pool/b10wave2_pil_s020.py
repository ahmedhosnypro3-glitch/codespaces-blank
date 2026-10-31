#!/usr/bin/env python3
"""Slide 020 closed-loop region check.
For each panel/element declared in build/slide_020.js, test that contained ink
lands inside the declared bounds and that expected ink density exists there."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
R = Image.open(f"{NS}/qa/slide020/b10wave2/render-1.png").convert("L")
O = Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")
IN = 2001 / 13.3333  # render px per inch

rr = np.array(R).astype(int)
oo = np.array(O).astype(int)
OI = oo < 128
RI = rr < 128

fails = []


def chk(name, x0, y0, x1, y1, min_ink, ink=None):
    """ink must exist inside the declared region (render px)."""
    a = ink if ink is not None else RI
    X0, Y0, X1, Y1 = (int(v * IN) for v in (x0, y0, x1, y1))
    sub = a[Y0:Y1, X0:X1]
    got = sub.sum() if sub.size else 0
    ok = got >= min_ink
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:<26} ink={got:7d} min={min_ink}")
    if not ok:
        fails.append(name)


print("=== RENDER: ink present inside each declared region ===")
chk("cyan dep-chain box", 0.66, 0.64, 5.36, 3.24, 4000)
chk("tan diagram canvas", 5.58, 0.66, 11.20, 3.26, 8000)
chk("error bar", 11.15, 0.78, 11.45, 3.14, 30000)
chk("class labels row", 11.52, 1.0, 12.4, 2.7, 1500)
chk("eq_mid1 band", 0.67, 3.42, 7.34, 3.86, 9000)
chk("eq_mid2 band", 0.67, 4.32, 7.48, 5.00, 12000)
chk("peach delta box", 0.80, 5.85, 6.13, 6.77, 6000)
chk("cream where strip", 0.67, 6.70, 8.93, 7.42, 2000)
chk("cream deriv panel", 9.07, 3.30, 12.67, 6.75, 12000)
chk("deriv line1", 9.22, 3.44, 10.31, 3.73, 300)
chk("deriv line2", 9.22, 4.26, 11.70, 4.71, 2000)
chk("deriv line3", 9.22, 5.08, 12.05, 5.43, 2500)
chk("deriv line4", 9.22, 5.93, 11.51, 6.36, 2200)
chk("badge circle", 12.48, 0.30, 12.98, 0.80, 3000)
chk("outer red frame", 0.15, 0.15, 13.18, 7.35, 30000)
chk("Node Mode caption", 5.70, 2.92, 7.0, 3.14, 60)

print("\n=== OVERFLOW: ink outside declared regions (must be ~0) ===")


def chk_no(name, x0, y0, x1, y1, max_ink):
    X0, Y0, X1, Y1 = (int(v * IN) for v in (x0, y0, x1, y1))
    sub = RI[Y0:Y1, X0:X1]
    got = sub.sum() if sub.size else 0
    ok = got <= max_ink
    print(f"  [{'PASS' if ok else 'FAIL'}] no-ink {name:<16} ink={got} max={max_ink}")
    if not ok:
        fails.append("overflow:" + name)


# slide must not carry ink outside the house frame (0.15..13.18 in)
X0, X1 = int(0.15 * IN), int(13.18 * IN)
for nm, yy in [("above frame", (0, int(0.15 * IN))),
               ("below frame", (int(7.35 * IN), 1125)),
               ("left of frame", (int(0.15 * IN), int(7.35 * IN)))]:
    if nm == "left of frame":
        sub = RI[yy[0]:yy[1], 0:X0]
    elif nm == "above frame":
        sub = RI[yy[0]:yy[1], :]
    else:
        sub = RI[yy[0]:yy[1], :]
    print(f"  ink {nm}: {sub.sum()}")
chk_no("right of frame", 13.18, 0.0, 13.3333, 7.5, 0)
chk_no("below house frame", 0.0, 7.35, 13.3333, 7.5, 0)
chk_no("between left panels and eq1", 7.34, 3.42, 7.48, 5.00, 0)
chk_no("betw eq2 band and delta box", 7.48, 4.32, 9.07, 5.0, 0)

print("\n=== ORIGINAL vs RENDER region alignment (ink center delta) ===")
S = 960 / 13.3333  # orig px per inch


def region_center(a, x0, y0, x1, y1, scale):
    X0, Y0, X1, Y1 = (int(v * scale) for v in (x0, y0, x1, y1))
    sub = a[Y0:Y1, X0:X1]
    if not sub.any():
        return None
    ys, xs = np.where(sub)
    return ((xs.min() + xs.max()) / 2 + X0, (ys.min() + ys.max()) / 2 + Y0,
            xs.max() - xs.min(), ys.max() - ys.min())


regions = {
    "canvas mid-equation 1": (0.9, 3.4, 7.3, 3.95),
    "canvas mid-equation 2": (0.9, 4.3, 7.4, 5.0),
    "delta box ink": (0.9, 5.85, 6.1, 6.8),
    "where strip ink": (0.8, 6.7, 8.9, 7.45),
    "cream panel ink": (9.1, 3.3, 12.6, 6.75),
}
for nm, (x0, y0, x1, y1) in regions.items():
    co = region_center(OI, x0, y0, x1, y1, S)
    cr = region_center(RI, x0, y0, x1, y1, IN)
    if co is None or cr is None:
        print(f"  [n/a] {nm}: orig={co} render={cr}")
        continue
    # convert orig px -> inches, render px -> inches
    coi = (co[0] / S, co[1] / S)
    cri = (cr[0] / IN, cr[1] / IN)
    print(f"  {nm}: orig center {coi[0]:.3f},{coi[1]:.3f} in  "
          f"render center {cri[0]:.3f},{cri[1]:.3f} in  "
          f"delta {abs(coi[0]-cri[0]):.3f},{abs(coi[1]-cri[1]):.3f} in "
          f"(extent {co[2]/S:.2f}x{co[3]/S:.2f} vs {cr[2]/IN:.2f}x{cr[3]/IN:.2f} in)")

print("\nFAILS:", fails if fails else "NONE")
