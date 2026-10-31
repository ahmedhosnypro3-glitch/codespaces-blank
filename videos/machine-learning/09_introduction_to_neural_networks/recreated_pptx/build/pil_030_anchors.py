# extract original anchor geometry for a 13.33x7.5in rebuild
import numpy as np
from PIL import Image
from scipy import ndimage

a = np.asarray(Image.open("unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]   # 960 x 540
SW, SH = 13.33, 7.5

def px2in(v): return v / 960 * 13.33
def py2in(v): return v / 540 * 7.5

print("inch scale: 960px ->", px2in(960), " 540px ->", py2in(540))

loose_red = (a[:, :, 0] > 120) & (a[:, :, 0] - a[:, :, 1] > 45) & (a[:, :, 0] - a[:, :, 2] > 45)

print("== panel top/bottom border rows ==")
for y in range(250, 256):
    xs = np.where(loose_red[y])[0]
    grp = []
    if len(xs):
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > 3: grp.append((int(s), int(p))); s = x
            p = x
        grp.append((int(s), int(p)))
    print(f"  y={y}:", grp[:10])

print("== title rect (red) ==")
ys, xs = np.where(loose_red[40:100, 60:400])
print("  title red bbox px x", xs.min() + 60, xs.max() + 60, "y", ys.min() + 40, ys.max() + 40)

print("== white panel ==")
white = (a[:, :, 0] > 233) & (a[:, :, 1] > 233) & (a[:, :, 2] > 233)
lab, n = ndimage.label(white)
sizes = ndimage.sum(white, lab, range(1, n + 1))
for i in range(1, n + 1):
    if sizes[i - 1] > 50000:
        ys, xs = np.where(lab == i)
        print(f"  panel px x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}")
        print(f"  panel in  x {px2in(xs.min()):.2f}-{px2in(xs.max()):.2f} y {py2in(ys.min()):.2f}-{py2in(ys.max()):.2f}")

print("== node circles (cream/yellow + orange) ==")
cream = (a[:, :, 0] > 240) & (a[:, :, 1] > 228) & (a[:, :, 2] < 210)
for nm, m in [("cream", cream),
              ("orange", (a[:, :, 0] > 230) & (a[:, :, 1] > 150) & (a[:, :, 1] < 210) & (a[:, :, 2] > 100) & (a[:, :, 2] < 180))]:
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    for i in range(1, n + 1):
        if sizes[i - 1] > 100:
            ys, xs = np.where(lab == i)
            print(f"  {nm} px x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}"
                  f"  cx={px2in((xs.min()+xs.max())/2):.2f} cy={py2in((ys.min()+ys.max())/2):.2f}"
                  f" d={int(xs.max()-xs.min())}px = {(xs.max()-xs.min())/960*13.33:.2f}in")

print("== blue/green panel borders (rows with long runs) ==")
blue = (a[:, :, 2] > 120) & ((a[:, :, 2] - a[:, :, 0]) > 45) & ((a[:, :, 2] - a[:, :, 1]) > 45)
green = (a[:, :, 1] > 105) & ((a[:, :, 1] - a[:, :, 0]) > 38) & ((a[:, :, 1] - a[:, :, 2]) > 38)
for nm, m in [("blue", blue), ("green", green)]:
    rows = [y for y in range(H) if m[y].sum() > 200]
    print(f"  {nm} long rows:", rows[:20])
    cols = [x for x in range(W) if m[:, x].sum() > 80]
    print(f"  {nm} long cols:", cols[:20])
