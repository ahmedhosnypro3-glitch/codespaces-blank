#!/usr/bin/env python3
"""Slide 014 v2 build measurements: panel boxes, eq line bands, label/icon bboxes, colors."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
SX, SY = 13.333 / W, 7.5 / H
print(f"image {W}x{H}  scale in/px x={SX:.6f} y={SY:.6f}")


def px2in(x, y):
    return (round(x * SX, 3), round(y * SY, 3))


def bbox(mask, label, minpx=30):
    lab, n = ndimage.label(mask)
    if n == 0:
        print(f"  {label}: NONE")
        return []
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    out = []
    for i in np.argsort(sizes)[::-1]:
        if sizes[i] < minpx:
            break
        ys, xs = np.where(lab == i + 1)
        out.append((xs.min(), ys.min(), xs.max(), ys.max(), int(sizes[i])))
    return out


# --- 1. panel fills: sample gray levels inside vs outside outer red frame
print("\n=== fill samples (px->in) ===")
for (x, y, nm) in [(30, 300, "outside frame left"), (700, 200, "inside panel, empty"),
                   (100, 480, "panel lower-left empty"), (500, 130, "white diag box bg"),
                   (700, 400, "yellow inset bg"), (5, 5, "slide bg corner")]:
    print(f"  {nm}: ({x},{y})={tuple(a[y, x])}  in={px2in(x, y)}")

# --- 2. outer red content rectangle: red border lines
red = (a[:, :, 0] > 120) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
colsum = red.sum(axis=0)
rowsum = red.sum(axis=1)
cand_x = [i for i in range(W) if colsum[i] > 300]
cand_y = [i for i in range(H) if rowsum[i] > 300]
print(f"\n=== long red vertical lines x: {cand_x[:6]} ... {cand_x[-6:] if cand_x else ''}")
print(f"=== long red horizontal lines y: {cand_y[:6]} ... {cand_y[-6:] if cand_y else ''}")

# --- 3. white diagram box
white = (a[:, :, 0] > 240) & (a[:, :, 1] > 240) & (a[:, :, 2] > 240)
lab, n = ndimage.label(white)
sizes = ndimage.sum(white, lab, range(1, n + 1))
print("\n=== white regions (top 6) ===")
for i in np.argsort(sizes)[::-1][:6]:
    ys, xs = np.where(lab == i + 1)
    print(f"  x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={int(sizes[i])} "
          f"in=({px2in(xs.min(), ys.min())}..{px2in(xs.max(), ys.max())})")

# --- 4. yellow inset box
yellow = (a[:, :, 0] > 230) & (a[:, :, 1] > 230) & (a[:, :, 2] > 140) & (a[:, :, 2] < 225)
print("\n=== yellow inset box ===")
for b in bbox(yellow, "yellow", 2000)[:3]:
    print(f"  x[{b[0]}..{b[2]}] y[{b[1]}..{b[3]}] in=({px2in(b[0], b[1])}..{px2in(b[2], b[3])})")

# --- 5. teal nodes
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
teal = (g > 120) & (b > 120) & (abs(g - b) < 60) & (r < g - 20)
print("\n=== teal Σ nodes ===")
for bl in bbox(teal, "teal", 500)[:6]:
    cx, cy = (bl[0] + bl[2]) // 2, (bl[1] + bl[3]) // 2
    m = a[bl[1]:bl[3], bl[0]:bl[2]].reshape(-1, 3)
    print(f"  x[{bl[0]}..{bl[2]}] y[{bl[1]}..{bl[3]}] ctr=({cx},{cy}) in={px2in(cx, cy)} "
          f"w={round((bl[2]-bl[0])*SX,3)} h={round((bl[3]-bl[1])*SY,3)}")

# --- 6. numbered circles 1,2,3 : pink/red filled, white numeral
pink = (r > 180) & (g < 130) & (b < 150) & (g > 60)
print("\n=== pink filled circles ===")
for bl in bbox(pink, "pink", 150)[:8]:
    cx, cy = (bl[0] + bl[2]) // 2, (bl[1] + bl[3]) // 2
    print(f"  x[{bl[0]}..{bl[2]}] y[{bl[1]}..{bl[3]}] ctr_in={px2in(cx, cy)} "
          f"d={round((bl[2]-bl[0])*SX,3)}x{round((bl[3]-bl[1])*SY,3)} px={bl[4]}")

# --- 7. equation text row bands (region x 80..575, y 320..480)
sub = a[320:485, 75:575]
dark = sub.sum(axis=2) < 330
rows = dark.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 3 and not inb:
        start = i; inb = True
    elif v <= 3 and inb:
        bands.append((start + 320, i + 320)); inb = False
if inb:
    bands.append((start + 320, 484))
print("\n=== equation text row bands (px) ===")
for y0, y1 in bands:
    seg = dark[y0 - 320:y1 - 320]
    xs = np.where(seg.any(axis=0))[0]
    print(f"  y[{y0}..{y1}] h={y1-y0}px={round((y1-y0)*SY,3)}in  x[{xs.min()+75}..{xs.max()+75}] "
          f"in=({px2in(xs.min()+75, y0)}..{px2in(xs.max()+75, y1)})")

# --- 8. blue "Still Linear Equation"
blue = (b > 110) & (b > r + 40) & (b > g + 30)
print("\n=== blue text (Still Linear Equation) ===")
for bl in bbox(blue, "blue", 150)[:3]:
    print(f"  x[{bl[0]}..{bl[2]}] y[{bl[1]}..{bl[3]}] in=({px2in(bl[0], bl[1])}..{px2in(bl[2],bl[3])})")

# --- 9. main-diagram internals: dark label blobs inside diagram box (x 70..550, y 95..305)
print("\n=== main diagram labels (dark blobs, in=) ===")
dg = a[95:305, 70:550]
dd = dg.sum(axis=2) < 300
for bl in bbox(dd, "lbl", 25)[:24]:
    xs0, ys0, xs1, ys1, _ = bl
    print(f"  x[{xs0+70}..{xs1+70}] y[{ys0+95}..{ys1+95}] "
          f"in=({px2in(xs0+70, ys0+95)}..{px2in(xs1+70, ys1+95)}) px={bl[4]}")

# --- 10. green cells in diagram (arrows / labels)
green = (g > r + 25) & (g > b + 25)
print("\n=== green cells in diagram box ===")
for bl in bbox(green, "green", 60)[:10]:
    m = a[bl[1]:bl[3], bl[0]:bl[2]].reshape(-1, 3).mean(axis=0).astype(int)
    print(f"  x[{bl[0]}..{bl[2]}] y[{bl[1]}..{bl[3]}] in=({px2in(bl[0], bl[1])}) "
          f"mean=#{m[0]:02X}{m[1]:02X}{m[2]:02X} px={bl[4]}")
redd = (r > g + 30) & (r > b + 30)
print("\n=== red cells in diagram box ===")
for bl in bbox(redd, "red", 60)[:10]:
    m = a[bl[1]:bl[3], bl[0]:bl[2]].reshape(-1, 3).mean(axis=0).astype(int)
    print(f"  x[{bl[0]}..{bl[2]}] y[{bl[1]}..{bl[3]}] in=({px2in(bl[0], bl[1])}) "
          f"mean=#{m[0]:02X}{m[1]:02X}{m[2]:02X} px={bl[4]}")
