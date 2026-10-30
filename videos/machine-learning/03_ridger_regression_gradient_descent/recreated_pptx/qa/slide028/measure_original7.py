#!/usr/bin/env python3
"""Pass 7: band-residual dot detection on the left arm (expected curve band
from local slope vs measured band; peaks = dots)."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
blue = (b - r > 45) & (b > 110)


def bands_at(x, y0=150, y1=452):
    col = np.where(blue[y0:y1, x])[0] + y0
    if not len(col):
        return []
    out = []
    s = col[0]; p = col[0]
    for yy in col[1:]:
        if yy > p + 2:
            out.append((s, p)); s = yy
        p = yy
    out.append((s, p))
    return out


# --- LEFT ARM: collect band mid + height per column, x 160..270
xs_all, mid_all, h_all = [], [], []
for x in range(158, 272):
    bs = bands_at(x)
    if len(bs) == 1:
        xs_all.append(x)
        mid_all.append((bs[0][0] + bs[0][1]) / 2)
        h_all.append(bs[0][1] - bs[0][0] + 1)

xs_all = np.array(xs_all); mid_all = np.array(mid_all); h_all = np.array(h_all)
# smooth midline: moving median 9
sm = np.array([np.median(mid_all[max(0, i - 4):i + 5]) for i in range(len(mid_all))])
slope = np.gradient(sm, xs_all)
print("== LEFT ARM: x, band-h, slope, expected-h(3.5px stroke), excess ==")
excess = h_all - 3.5 * np.sqrt(1 + slope ** 2)
for i in range(0, len(xs_all)):
    mark = "  <== DOT?" if excess[i] > 3.5 else ""
    print(f"  x={xs_all[i]} mid={sm[i]:6.1f} h={h_all[i]:2d} slope={slope[i]:5.2f} "
          f"exp={3.5*np.sqrt(1+slope[i]**2):4.1f} excess={excess[i]:5.1f}{mark}")

# --- RIGHT ARM of LEFT curve: x 282..390
print("\n== RIGHT ARM of LEFT PANEL: x, band-h, slope, excess ==")
xs2, mid2, h2 = [], [], []
for x in range(280, 392):
    bs = bands_at(x)
    if len(bs) == 1:
        xs2.append(x)
        mid2.append((bs[0][0] + bs[0][1]) / 2)
        h2.append(bs[0][1] - bs[0][0] + 1)
xs2 = np.array(xs2); mid2 = np.array(mid2); h2 = np.array(h2)
sm2 = np.array([np.median(mid2[max(0, i - 4):i + 5]) for i in range(len(mid2))])
sl2 = np.gradient(sm2, xs2)
ex2 = h2 - 3.5 * np.sqrt(1 + sl2 ** 2)
for i in range(len(xs2)):
    mark = "  <== DOT?" if ex2[i] > 3.5 else ""
    print(f"  x={xs2[i]} mid={sm2[i]:6.1f} h={h2[i]:2d} slope={sl2[i]:5.2f} excess={ex2[i]:5.1f}{mark}")

# --- RIGHT PANEL left arm (dots 1,3 sit on it) for calibration of 'large dot' excess
print("\n== RIGHT PANEL LEFT ARM (calibration): x, h, excess ==")
xs3, mid3, h3 = [], [], []
for x in range(505, 630):
    bs = bands_at(x)
    if len(bs) == 1:
        xs3.append(x)
        mid3.append((bs[0][0] + bs[0][1]) / 2)
        h3.append(bs[0][1] - bs[0][0] + 1)
xs3 = np.array(xs3); mid3 = np.array(mid3); h3 = np.array(h3)
sm3 = np.array([np.median(mid3[max(0, i - 4):i + 5]) for i in range(len(mid3))])
sl3 = np.gradient(sm3, xs3)
ex3 = h3 - 3.5 * np.sqrt(1 + sl3 ** 2)
for i in range(len(xs3)):
    mark = "  <== BIGDOT?" if ex3[i] > 4 else ""
    print(f"  x={xs3[i]} mid={sm3[i]:6.1f} h={h3[i]:2d} slope={sl3[i]:5.2f} excess={ex3[i]:5.1f}{mark}")
