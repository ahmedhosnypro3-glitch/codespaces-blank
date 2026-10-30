#!/usr/bin/env python3
"""Measure slide 33 original structure: colored node circles, text ink bands, rules."""
from PIL import Image
import sys

img = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_033.jpg')
W, H = img.size
px = img.convert('RGB').load()
IN = W / 13.33


def near(p, target, tol=30):
    return all(abs(p[i] - target[i]) <= tol for i in range(3))


def blobs(target, tol=30, region=None, min_size=8):
    """Return connected components of pixels near target color."""
    x0, y0, x1, y1 = region or (0, 0, W, H)
    seen = set()
    out = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen:
                continue
            if not near(px[x, y], target, tol):
                continue
            stack = [(x, y)]
            seen.add((x, y))
            pts = []
            while stack:
                cx, cy = stack.pop()
                pts.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in seen and near(px[nx, ny], target, tol):
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            if len(pts) >= min_size:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
    return out


print(f"IMAGE {W}x{H}  ({IN:.2f} px/in)")
print("\n=== YELLOW blobs (FFD700) ===")
for b in sorted(blobs((255, 215, 0), 35), key=lambda b: (b[1], b[0])):
    print(f"  x=[{b[0]},{b[2]}] y=[{b[1]},{b[3]}] n={b[4]} "
          f"center_in=({(b[0]+b[2])/2/IN:.2f},{(b[1]+b[3])/2/IN:.2f}) "
          f"size_in=({(b[2]-b[0])/IN:.2f}x{(b[3]-b[1])/IN:.2f})")

print("\n=== ORANGE blobs (FFA500) ===")
for b in sorted(blobs((255, 165, 0), 30), key=lambda b: (b[1], b[0])):
    print(f"  x=[{b[0]},{b[2]}] y=[{b[1]},{b[3]}] n={b[4]} "
          f"center_in=({(b[0]+b[2])/2/IN:.2f},{(b[1]+b[3])/2/IN:.2f}) "
          f"size_in=({(b[2]-b[0])/IN:.2f}x{(b[3]-b[1])/IN:.2f})")

print("\n=== BLUE blobs (0000FF/4169E1) ===")
for b in sorted(blobs((0, 0, 255), 60) + blobs((65, 105, 225), 30), key=lambda b: (b[1], b[0])):
    print(f"  x=[{b[0]},{b[2]}] y=[{b[1]},{b[3]}] n={b[4]} "
          f"center_in=({(b[0]+b[2])/2/IN:.2f},{(b[1]+b[3])/2/IN:.2f}) "
          f"size_in=({(b[2]-b[0])/IN:.2f}x{(b[3]-b[1])/IN:.2f})")

print("\n=== Dark ink row bands (text lines) ===")
for y in range(0, H):
    n = 0
    for x in range(0, W, 2):
        p = px[x, y]
        if sum(p) < 480:
            n += 1
    if n > 0:
        pass
# group consecutive rows with ink
rows = []
for y in range(0, H):
    n = sum(1 for x in range(0, W, 2) if sum(px[x, y]) < 480)
    rows.append(n)
band = None
for y, n in enumerate(rows):
    if n > 1 and band is None:
        band = [y, y]
    elif n > 1:
        band[1] = y
    elif band is not None:
        print(f"  ink rows y=[{band[0]},{band[1]}] ({band[0]/IN:.2f}in-{band[1]/IN:.2f}in)")
        band = None
if band:
    print(f"  ink rows y=[{band[0]},{band[1]}]")

print("\n=== Vertical red rules ===")
for x in range(0, W, 1):
    n = sum(1 for y in range(0, H, 3) if px[x, y][0] > 120 and px[x, y][1] < 90 and px[x, y][2] < 90)
    if n > 100:
        print(f"  x={x} ({x/IN:.2f}in) red_count={n}")
