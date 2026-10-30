from PIL import Image
import numpy as np, sys

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 244) & (G > 244) & (B > 244)
ink = ~white


def vprobe(x0, x1, y0, y1, label):
    print(f"\n== {label}: region x[{x0}..{x1}] y[{y0}..{y1}] column ink counts ==")
    cols = []
    for x in range(x0, x1 + 1):
        n = int(ink[y0:y1 + 1, x].sum())
        cols.append(n)
    # report columns with ink above 20% of band height
    hgt = y1 - y0 + 1
    runs = []
    cur = None
    for i, n in enumerate(cols):
        x = x0 + i
        if n >= hgt * 0.5:
            if cur is None:
                cur = [x, x, n]
            else:
                cur[1] = x
        else:
            if cur is not None:
                runs.append(tuple(cur)); cur = None
    if cur:
        runs.append(tuple(cur))
    print("  tall ink columns (>=50% band):", runs)
    print("  per-col sample:", cols[:40])


def hprobe(x0, x1, y0, y1, label):
    print(f"\n== {label}: region x[{x0}..{x1}] y[{y0}..{y1}] row ink counts ==")
    rows = []
    for y in range(y0, y1 + 1):
        n = int(ink[y, x0:x1 + 1].sum())
        rows.append((y, n))
    # print contiguous row bands with ink
    band = None
    for y, n in rows:
        if n >= 5:
            if band is None:
                band = [y, y, n]
            else:
                band[1] = y; band[2] += n
        else:
            if band and band[1] - band[0] >= 2:
                print(f"   rows {band[0]}..{band[1]} totalink={band[2]}")
            band = None
    if band and band[1] - band[0] >= 2:
        print(f"   rows {band[0]}..{band[1]} totalink={band[2]}")


# find white panel rectangles
print("scanning for contiguous white blocks on rows y=120, y=200, y=300, y=440:")
for y in [120, 200, 300, 440, 480]:
    row = white[y]
    runs = []
    cur = None
    for x in range(50, 920):
        if row[x]:
            if cur is None:
                cur = [x, x]
            else:
                cur[1] = x
        elif cur:
            if cur[1] - cur[0] > 20:
                runs.append(tuple(cur))
            cur = None
    if cur and cur[1] - cur[0] > 20:
        runs.append(tuple(cur))
    print(f" y={y}: white runs ", runs)

vprobe(84, 424, 96, 240, "LEFT PANEL")
vprobe(528, 792, 96, 240, "RIGHT PANEL")
hprobe(84, 800, 246, 345, "MIDDLE BAND")
