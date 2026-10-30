from PIL import Image
import numpy as np, sys

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]


def fmt(v):
    r, g, b = int(v[0]), int(v[1]), int(v[2])
    return f"({r:3d},{g:3d},{b:3d})"


def rowscan(y, xs):
    out = []
    prev = None
    for x in xs:
        px = tuple(a[y, x])
        if px != prev:
            out.append((x, fmt(px)))
            prev = px
    return out


def colscan(x, ys):
    out = []
    prev = None
    for y in ys:
        px = tuple(a[y, x])
        if px != prev:
            out.append((y, fmt(px)))
            prev = px
    return out


for y in [44, 50, 88, 90, 246, 248, 504, 506]:
    print(f"\nrow y={y} transitions x=50..910:")
    print("  ", " ".join(f"{x}:{c}" for x, c in rowscan(y, range(50, 912, 1))[:120]))

for x in [56, 72, 76, 110, 160, 270, 272, 390, 500, 505, 700, 900, 904]:
    print(f"\ncol x={x} transitions y=40..520:")
    print("  ", " ".join(f"{y}:{c}" for y, c in colscan(x, range(40, 521, 1))[:80]))
