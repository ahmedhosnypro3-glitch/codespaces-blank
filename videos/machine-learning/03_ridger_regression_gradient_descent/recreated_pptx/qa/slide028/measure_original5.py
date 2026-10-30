#!/usr/bin/env python3
"""Pass 5: curve-subtraction -> clean dot/segment geometry; parabola fits;
font-size empirical match."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
blue = (b - r > 45) & (b > 110)


def col_bands(mask, x, x0, x1, y0, y1):
    seg = mask[y0:y1, x]
    col = np.where(seg)[0] + y0
    if not len(col):
        return []
    bands = []
    s = col[0]; p = col[0]
    for yy in col[1:]:
        if yy > p + 2:
            bands.append((s, p)); s = yy
        p = yy
    bands.append((s, p))
    return bands


def fit_parabola(mask, x0, x1, y0, y1, maxband=7):
    pts = []
    for x in range(x0, x1):
        bands = col_bands(mask, x, x0, x1, y0, y1)
        if len(bands) == 1 and (bands[0][1] - bands[0][0] + 1) <= maxband:
            pts.append((x, (bands[0][0] + bands[0][1]) / 2))
    pts = np.array(pts)
    # parabola y = A x^2 + B x + C
    A, B, C = np.polyfit(pts[:, 0], pts[:, 1], 2)
    resid = pts[:, 1] - (A * pts[:, 0] ** 2 + B * pts[:, 0] + C)
    return A, B, C, pts, np.abs(resid).max(), np.abs(resid).mean()


L = fit_parabola(blue, 150, 480, 150, 448)
R = fit_parabola(blue, 480, 850, 150, 448)
print(f"LEFT  fit: y = {L[0]:.6f}x^2 + {L[1]:.4f}x + {L[2]:.2f}  "
      f"n={len(L[3])} maxres={L[4]:.1f} meanres={L[5]:.2f}")
vx = -L[1] / (2 * L[0]); vy = L[0] * vx**2 + L[1] * vx + L[2]
print(f"      vertex=({vx:.1f},{vy:.1f})")
print(f"RIGHT fit: y = {R[0]:.6f}x^2 + {R[1]:.4f}x + {R[2]:.2f}  "
      f"n={len(R[3])} maxres={R[4]:.1f} meanres={R[5]:.2f}")
vx = -R[1] / (2 * R[0]); vy = R[0] * vx**2 + R[1] * vx + R[2]
print(f"      vertex=({vx:.1f},{vy:.1f})")

for label_, fit, rx0, rx1 in [("LEFT", L, 150, 480), ("RIGHT", R, 480, 850)]:
    A, B, C = fit[0], fit[1], fit[2]
    xs = np.arange(rx0, rx1)
    yc = A * xs**2 + B * xs + C
    # remainder: blue pixels farther than 3.2px from fitted curve
    rem = blue.copy()
    rem[:150, :] = False; rem[450:, :] = False
    yy_grid = np.arange(150, 450)
    dist = np.abs(yy_grid[:, None] - yc[None, :])
    near = dist <= 3.2
    rem[150:450, rx0:rx1] &= ~near
    lbl, n = ndimage.label(rem)
    print(f"\n== {label_} REMAINDER components (dots & segments) ==")
    comps = []
    for i in range(1, n + 1):
        ys, xs2 = np.where(lbl == i)
        if len(ys) < 12:
            continue
        x0, x1_, y0, y1_ = xs2.min(), xs2.max(), ys.min(), ys.max()
        w_, h_ = x1_ - x0 + 1, y1_ - y0 + 1
        fill = len(ys) / (w_ * h_)
        kind = "DOT?" if 0.7 <= w_ / h_ <= 1.4 and fill > 0.5 else "stroke"
        comps.append((len(ys), x0, x1_, y0, y1_, w_, h_, fill))
    comps.sort(key=lambda t: (t[4], t[1]))
    for size, x0, x1_, y0, y1_, w_, h_, fill in comps:
        print(f"  n={size} x {x0}-{x1_} y {y0}-{y1_} w={w_} h={h_} fill={fill:.2f} "
              f"cx={(x0+x1_)/2:.1f} cy={(y0+y1_)/2:.1f}")

print("\n== FONT MATCH ==")
import glob
bold_ = glob.glob("/usr/share/fonts/**/LiberationSans-Bold.ttf", recursive=True)
reg = glob.glob("/usr/share/fonts/**/LiberationSans-Regular.ttf", recursive=True)
if not bold_:
    print("  Liberation not found; listing sans fonts:")
    print(glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)[:20])


def ink(text, path, size):
    f = ImageFont.truetype(path, size)
    img = Image.new("L", (1500, 200), 255)
    dr = ImageDraw.Draw(img)
    dr.text((20, 40), text, font=f, fill=0)
    a = np.asarray(img)
    ys, xs = np.where(a < 128)
    return xs.max() - xs.min() + 1, ys.min() + 40, ys.max() + 40


if bold_:
    t = "Effect of small and large Learning Rate"
    for s in (20, 22, 24, 26, 28):
        w, y0, y1 = ink(t, bold_[0], s)
        print(f"  TITLE bold {s}: w={w} ytop={y0} ybot={y1} (target w=499 y 72-101)")
    for s in (12, 13, 14, 15):
        w, y0, y1 = ink("Small Learning Rate", bold_[0], s)
        print(f"  HEADING bold {s}: w={w} ytop={y0} ybot={y1} (target w=134 y 188-199)")
    if reg:
        for s in (9, 10, 11, 12):
            w, y0, y1 = ink("Value of weight", reg[0], s)
            print(f"  VoW reg {s}: w={w} ytop={y0} ybot={y1} (target w=88 y 451-459)")
            w2, y02, y12 = ink("Loss", reg[0], s)
            print(f"  Loss reg {s}: w={w2} ytop={y02} ybot={y12} (target w=23 y 223-229)")
