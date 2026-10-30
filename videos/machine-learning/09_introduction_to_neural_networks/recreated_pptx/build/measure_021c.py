"""Precise geometry of slide_021.jpg: red content frame, pink formula boxes, black bar, text bands."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
P = lambda px: px / 72.0

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== 1. RED CONTENT FRAME (original's own inset frame) ===")
red = (r > 110) & (r - g > 45) & (r - b > 45)
rowsum = red.sum(axis=1)
colsum = red.sum(axis=0)
print("  rows with red>400:", [(y, int(rowsum[y])) for y in range(H) if rowsum[y] > 400])
print("  rows with red>250:", [(y, int(rowsum[y])) for y in range(H) if rowsum[y] > 250][:12])
print("  cols with red>250:", [(x, int(colsum[x])) for x in range(W) if colsum[x] > 250][:12])
print("  cols with red>100:", [(x, int(colsum[x])) for x in range(W) if colsum[x] > 100][:20])

print("\n=== 2. PINK FORMULA BOX FILL (exact #FDE9E9-ish) ===")
fill = (np.abs(r - 253) < 8) & (np.abs(g - 233) < 10) & (np.abs(b - 233) < 10)
print("  total fill px:", int(fill.sum()))
# label connected column runs per row band
for label, y0, y1 in [("top-row boxes", 40, 108), ("bottom-row boxes", 285, 342)]:
    band = fill[y0:y1]
    cc = band.sum(axis=0)
    xs = np.where(cc > (y1 - y0) * 0.35)[0]
    seg = []; prev = None
    for x in xs:
        if prev is None or x - prev > 4:
            seg.append([x, x])
        else:
            seg[-1][1] = x
        prev = x
    print(f"  {label}: fill x-segments (px) -> in:")
    for s in seg:
        print(f"     [{s[0]},{s[1]}] -> in {P(s[0]):.3f}-{P(s[1]):.3f}  frac {s[0]/W:.4f}-{s[1]/W:.4f}")

print("\n=== 3. PINK BOX VERTICAL EXTENT (for each x column) ===")
for xprobe, name in [(200, "TL box"), (660, "TR box"), (200, "BL box"), (660, "BR box")]:
    pass
def vext(x0, x1, y0, y1, name):
    sub = fill[y0:y1, x0:x1]
    cc = sub.sum(axis=1)
    ys = np.where(cc > (x1 - x0) * 0.5)[0]
    if len(ys):
        print(f"  {name}: fill y [{ys.min()+y0},{ys.max()+y0}] -> in {P(ys.min()+y0):.3f}-{P(ys.max()+y0):.3f}"
              f"  frac {(ys.min()+y0)/H:.4f}-{(ys.max()+y0)/H:.4f}")
vext(120, 325, 30, 120, "TL pink")
vext(556, 750, 30, 120, "TR pink")
vext(100, 430, 275, 350, "BL pink")
vext(590, 815, 275, 350, "BR pink")

print("\n=== 4. RED BORDER OF PINK BOXES (find red near each pink box) ===")
for name, y0, y1, x0, x1 in [("TL", 35, 115, 100, 350), ("TR", 35, 115, 545, 765),
                             ("BL", 275, 350, 85, 445), ("BR", 275, 350, 575, 830)]:
    sub = red[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {name} red ink bbox px x[{xs.min()+x0},{xs.max()+x0}] y[{ys.min()+y0},{ys.max()+y0}]"
              f" -> in x {P(xs.min()+x0):.3f}-{P(xs.max()+x0):.3f} y {P(ys.min()+y0):.3f}-{P(ys.max()+y0):.3f}")

print("\n=== 5. BLACK BOTTOM BAR extents ===")
dark = (r < 70) & (g < 70) & (b < 70)
band = dark[518:540]
xs = np.where(band.sum(axis=0) > 15)[0]
print(f"  bar x [{xs.min()},{xs.max()}] -> in {P(xs.min()):.3f}-{P(xs.max()):.3f}  frac {xs.min()/W:.4f}-{xs.max()/W:.4f}")
ys = np.where(dark[:, 100:800].sum(axis=1) > 500)[0]
print(f"  bar y [{ys.min()},{ys.max()}] -> in {P(ys.min()):.3f}-{P(ys.max()):.3f}  frac {ys.min()/H:.4f}-{ys.max()/H:.4f}")

print("\n=== 6. GRAPH BOX BORDERS (blue) ===")
blue = (b > 100) & (b - r > 50) & (b - g > 25)
browsum = blue.sum(axis=1); bcolsum = blue.sum(axis=0)
cand_rows = [(y, int(browsum[y])) for y in range(H) if browsum[y] > 200]
cand_cols = [(x, int(bcolsum[x])) for x in range(W) if bcolsum[x] > 200]
print("  candidate border rows:", cand_rows)
print("  candidate border cols:", cand_cols)

print("\n=== 7. TEXT INK BANDS inside each formula box (black/red/blue/green) ===")
def bands(x0, x1, y0, y1, name):
    sub = a[y0:y1, x0:x1]
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    ink = (np.abs(sub - np.median(sub.reshape(-1, 3), axis=0)).max(axis=2) > 40)
    rs = ink.sum(axis=1)
    out = []
    for y in range(y1 - y0):
        if rs[y] > 1:
            out.append(y + y0)
    if not out:
        print(f"  {name}: no ink"); return
    seg = []; prev = None
    for y in out:
        if prev is None or y - prev > 3:
            seg.append([y, y])
        else:
            seg[-1][1] = y
        prev = y
    print(f"  {name} ink row bands: " + ", ".join(f"[{s[0]},{s[1]}]" for s in seg))
bands(115, 330, 56, 106, "TL formula")
bands(552, 760, 56, 106, "TR formula")
bands(96, 435, 284, 340, "BL formula")
bands(586, 818, 284, 340, "BR formula")

print("\n=== 8. GRAPH PLOT INNER GEOMETRY (axes positions) ===")
# For TL graph: find dark (black axis) rows/cols inside x 122..400, y 109..274
def axis_geom(x0, x1, y0, y1, name):
    sub = a[y0:y1, x0:x1]
    darkish = (sub.max(axis=2) < 140)
    rs = darkish.sum(axis=1); cs = darkish.sum(axis=0)
    ry = [(y + y0, int(rs[y])) for y in range(y1 - y0) if rs[y] > (x1 - x0) * 0.25]
    cx = [(x + x0, int(cs[x])) for x in range(x1 - x0) if cs[x] > (y1 - y0) * 0.25]
    print(f"  {name}: dark rows {ry[:6]}  dark cols {cx[:6]}")
axis_geom(124, 399, 112, 272, "TL graph")
axis_geom(566, 841, 112, 272, "TR graph")
axis_geom(124, 399, 349, 506, "BL graph")
axis_geom(566, 841, 349, 506, "BR graph")
