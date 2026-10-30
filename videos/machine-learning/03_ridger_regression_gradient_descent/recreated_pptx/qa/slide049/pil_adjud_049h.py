#!/usr/bin/env python3
# PIL adjudication of judge_attempt_10 findings vs original frame (attempt-10 cycle).
# render_9.png (2001x1125 @150dpi) vs unique_slides/slide_049.jpg (960x540, 1px=1pt).
import numpy as np
from PIL import Image

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)
H, W = orig.shape[:2]
rh, rw = rend.shape[:2]
sx, sy = rw / W, rh / H
print(f"orig {W}x{H}  render {rw}x{rh}  sx={sx:.4f} sy={sy:.4f}")


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


def colprofile(ink, x0, x1, y0, y1, label, minpx=1):
    print(f"\n--- colprofile {label} x{x0}..{x1} y{y0}..{y1} ---")
    spans = []
    cur = None
    for x in range(x0, x1):
        n = int(ink[y0:y1, x].sum())
        if n >= minpx:
            if cur is None:
                cur = [x, x, n]
            else:
                cur[1] = x
                cur[2] += n
        else:
            if cur is not None:
                spans.append(cur)
                cur = None
    if cur is not None:
        spans.append(cur)
    for s in spans:
        print(f"  x{s[0]}..{s[1]} inkpx={s[2]}")


def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (r > 140) & (g < 110) & (b < 110)
    blue = (r < 120) & (g < 120) & (b > 140)
    green = (g > 100) & (g > r + 30) & (g > b + 30)
    dark = lum(a) < 110
    return red, blue, green, dark


o_red, o_blue, o_green, o_dark = masks(orig)
r_red, r_blue, r_green, r_dark = masks(rend)
rr_red = r_red[y0s][:, x0s]
rr_blue = r_blue[y0s][:, x0s]
rr_green = r_green[y0s][:, x0s]

# ---------- A: top table + Initial column (F1, F3) ----------
dump(o_ink, 70, 280, 48, 140, "A ORIG top table")
dump(r_ink, 70, 280, 48, 140, "A RENDER top table")

# ---------- B: d(x1) calc row structure (F2) ----------
colprofile(o_ink, 230, 700, 138, 208, "B ORIG row1 y138..208")
colprofile(r_ink, 230, 700, 138, 208, "B RENDER row1 y138..208")

# ---------- C: augmented table (F3) ----------
dump(o_ink, 78, 240, 222, 332, "C ORIG augmented table")
dump(r_ink, 78, 240, 222, 332, "C RENDER augmented table")

# ---------- D: legend colors (F6) ----------
print("\n--- D legend y105..130 ---")
for name, redm, bluem, greenm, dm in (("ORIG", o_red, o_blue, o_green, o_dark), ("RENDER", rr_red, rr_blue, rr_green, None)):
    spans = []
    cur = None
    for x in range(230, 430):
        nred = int(redm[105:130, x].sum())
        nblue = int(bluem[105:130, x].sum())
        ngreen = int(greenm[105:130, x].sum())
        ndark = int((olum[105:130, x] < 128).sum()) if name == "ORIG" else int((rmin[105:130, x] < 128).sum())
        cls = "R" if nred >= 2 else ("B" if nblue >= 2 else ("G" if ngreen >= 2 else ("k" if ndark >= 2 else " ")))
        if cls != " ":
            if cur is None:
                cur = [x, x, cls]
            else:
                cur[1] = x
                cur[2] += cls
        else:
            if cur is not None:
                spans.append(cur)
                cur = None
    if cur is not None:
        spans.append(cur)
    print(f"  {name}: " + "  ".join(f"x{s[0]}..{s[1]}[{s[2]}]" for s in spans))

# green-ink stats in legend tail (Zero is unaccepted) ORIG
tail = orig[105:130, 330:430]
tr, tg, tb = tail[:, :, 0], tail[:, :, 1], tail[:, :, 2]
tl = lum(tail)
dk = tl < 140
if dk.sum():
    px = tail[dk]
    print(f"  ORIG legend tail dark-ink n={dk.sum()} meanRGB=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) "
          f"minlum px={px[tl[dk].argmin()]}")
gt = ((tg > 100) & (tg > tr + 30) & (tg > tb + 30)).sum()
print(f"  ORIG legend tail green-mask px={gt}")

# ---------- E: red text in top zone (F4 Initia/l) ----------
print("\n--- E red-x-spans y50..135 x60..800 ---")
for name, m in (("ORIG", o_red), ("RENDER", rr_red)):
    colhit = m[50:135, :].sum(axis=0) > 0
    spans = []
    x = 60
    while x < 800:
        if colhit[x]:
            x2 = x
            while x2 < 799 and colhit[x2 + 1]:
                x2 += 1
            ys = np.where(m[50:135, x:x2 + 1].any(axis=1))[0]
            spans.append((x, x2, 50 + ys.min(), 50 + ys.max()))
            x = x2 + 1
        else:
            x += 1
    print(f"  {name}: " + "  ".join(f"x{s[0]}..{s[1]} y{s[2]}..{s[3]}" for s in spans) or f"  {name}: none")

# ---------- F: row-box verticals in calc region (F7) ----------
print("\n--- F tall verticals (run>=28) per calc row band, x300..790 ---")
bands = [(138, 208), (214, 268), (276, 328), (332, 384), (390, 440), (444, 500)]
for i, (y0, y1) in enumerate(bands, 1):
    line = f"  row{i} y{y0}..{y1}"
    for name, ink in (("ORIG", o_ink), ("RENDER", r_ink)):
        cols = []
        for x in range(300, 790):
            col = ink[y0:y1, x]
            run = best = 0
            for v in col:
                run = run + 1 if v else 0
                best = max(best, run)
            if best >= 28:
                cols.append(x)
        # collapse
        sp = []
        for c in cols:
            if sp and c == sp[-1][1] + 1:
                sp[-1][1] = c
            else:
                sp.append([c, c])
        line += f" | {name}: " + (",".join(f"x{s[0]}..{s[1]}" for s in sp) if sp else "none")
    print(line)

# ---------- G: REPEAT instruction (F5) ----------
dump(o_ink, 420, 650, 40, 95, "G ORIG REPEAT zone")
dump(r_ink, 420, 650, 40, 95, "G RENDER REPEAT zone")

# ---------- Z: check-classes grid (F3 Z columns) ----------
dump(o_ink, 545, 800, 48, 135, "Z ORIG check classes")
dump(r_ink, 545, 800, 48, 135, "Z RENDER check classes")
