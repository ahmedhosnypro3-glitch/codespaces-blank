#!/usr/bin/env python3
# Round 2: augmented-table upper half, d(x1) expression ASCII, Initial-W zone,
# legend tail color, Iteration-2 box zone, low-threshold vertical census.
import numpy as np
from PIL import Image

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)
H, W = orig.shape[:2]
rh, rw = rend.shape[:2]
sx, sy = rw / W, rh / H


def lum(a):
    return (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) // 1000


olum = lum(orig)
rlum = lum(rend)
x0s = np.minimum((np.arange(W) * sx).astype(int), rw - 1)
y0s = np.minimum((np.arange(H) * sy).astype(int), rh - 1)
rmin_rows = np.minimum.reduceat(rlum, y0s, axis=0)
rmin = np.minimum.reduceat(rmin_rows, x0s, axis=1)
r_ink = rmin < 150
o_ink = olum < 205


def dump(ink, x0, x1, y0, y1, label):
    print(f"\n--- {label} frame x{x0}..{x1} y{y0}..{y1} ---")
    print("     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1)))
    print("     " + "".join("." if x % 10 else "+" for x in range(x0, x1)))
    for y in range(y0, y1):
        print(f"{y:4d} " + "".join("#" if ink[y, x] else "." for x in range(x0, x1)))


# 1) augmented table upper half
dump(o_ink, 78, 245, 128, 232, "R2 ORIG aug table upper")
dump(r_ink, 78, 245, 128, 232, "R2 RENDER aug table upper")

# 2) d(x1) expression row
dump(o_ink, 270, 560, 136, 210, "R2 ORIG d(x1) left")
dump(o_ink, 560, 705, 136, 210, "R2 ORIG d(x1) right")
dump(r_ink, 280, 560, 136, 210, "R2 RENDER d(x1) left")
dump(r_ink, 560, 700, 136, 210, "R2 RENDER d(x1) right")

# 3) Initial-W zone right of the top table
dump(o_ink, 255, 430, 48, 135, "R2 ORIG initialW zone")
dump(r_ink, 255, 430, 48, 135, "R2 RENDER initialW zone")

# 4) legend tail with per-column color classes (orig vs render), x380..540
o = orig
rsmall = rend[np.floor(np.arange(H) * sy).astype(int)][:, np.floor(np.arange(W) * sx).astype(int)]
print("\n--- R2 legend tail per-column class, y105..132 ---")
for name, img in (("ORIG", o), ("RENDER", rsmall)):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    red = (r > 140) & (g < 110) & (b < 110)
    blue = (r < 120) & (g < 120) & (b > 140)
    green = (g > 100) & (g > r + 30) & (g > b + 30)
    dark = lum(img) < 140
    out = []
    cur = None
    for x in range(380, 545):
        n = lambda m: int(m[105:132, x].sum())
        cls = "R" if n(red) >= 2 else ("B" if n(blue) >= 2 else ("G" if n(green) >= 2 else ("k" if n(dark) >= 2 else " ")))
        if cls != " ":
            if cur is None:
                cur = [x, x, cls]
            else:
                cur[1] = x
                cur[2] += cls
        else:
            if cur is not None:
                out.append(cur)
                cur = None
    if cur is not None:
        out.append(cur)
    print(f"  {name}: " + "  ".join(f"x{s[0]}..{s[1]}[{s[2]}]" for s in out))

# green RGB sample orig legend tail
tl = orig[105:132, 390:545]
tr, tg, tb = tl[:, :, 0], tl[:, :, 1], tl[:, :, 2]
gm = (tg > 100) & (tg > tr + 30) & (tg > tb + 30)
if gm.sum():
    px = tl[gm]
    print(f"  ORIG green px n={gm.sum()} meanRGB=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})")

# 5) Iteration-2 box zone y276..312
dump(o_ink, 78, 245, 276, 315, "R2 ORIG iter2 zone")
dump(r_ink, 78, 245, 276, 315, "R2 RENDER iter2 zone")

# 6) vertical census run>=15, calc rows, x230..800
print("\n--- R2 verticals run>=15 per row band, x230..800 ---")
bands = [(138, 208), (214, 268), (276, 328), (332, 384), (390, 440), (444, 500)]
for i, (y0, y1) in enumerate(bands, 1):
    line = f"  row{i} y{y0}..{y1}"
    for name, ink in (("ORIG", o_ink), ("RENDER", r_ink)):
        sp = []
        for x in range(230, 800):
            col = ink[y0:y1, x]
            run = best = 0
            for v in col:
                run = run + 1 if v else 0
                best = max(best, run)
            if best >= 15:
                if sp and x == sp[-1][1] + 1:
                    sp[-1][1] = x
                else:
                    sp.append([x, x])
        line += f" | {name}: " + (",".join(f"x{s[0]}..{s[1]}" for s in sp) if sp else "none")
    print(line)

# 7) horizontal separators: rows y135..505 where a long horizontal ink run exists, x300..780
print("\n--- R2 horizontal rules y135..505 (run>=150 within x300..780) ---")
for name, ink in (("ORIG", o_ink), ("RENDER", r_ink)):
    rows = []
    for y in range(135, 505):
        seg = ink[y, 300:780]
        run = best = 0
        for v in seg:
            run = run + 1 if v else 0
            best = max(best, run)
        if best >= 150:
            rows.append(y)
    # collapse
    rp = []
    for y in rows:
        if rp and y == rp[-1][1] + 1:
            rp[-1][1] = y
        else:
            rp.append([y, y])
    print(f"  {name}: " + (",".join(f"y{s[0]}..{s[1]}" for s in rp) if rp else "none"))
