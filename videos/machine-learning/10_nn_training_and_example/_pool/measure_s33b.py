#!/usr/bin/env python3
"""Structural analysis of slide 33 original: true colors of blobs + geometry."""
from PIL import Image
import collections

img = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_033.jpg').convert('RGB')
W, H = img.size
px = img.load()
IN = W / 13.33

# Classify each pixel
def classify(p):
    r, g, b = p
    mx, mn = max(p), min(p)
    sat = mx - mn
    if sat < 18:
        return 'gray' if mx > 200 else ('gray' if mx > 140 else 'dark')
    # hue
    if r > g and r > b:
        return 'red' if sat > 55 else 'pink'
    if r > 180 and g > 180 and b < g - 15:
        return 'yellow'
    if b > r + 15:
        return 'blue'
    if g > r + 15:
        return 'green'
    return 'other'

# Print coarse color map: 40 cols x 24 rows, dominant class
COLS, ROWS = 48, 27
print("=== CLASS MAP (48x27) ===")
for r in range(ROWS):
    y0, y1 = r * H // ROWS, (r + 1) * H // ROWS
    line = ''
    for c in range(COLS):
        x0, x1 = c * W // COLS, (c + 1) * W // COLS
        cnt = collections.Counter()
        for y in range(y0, y1, 2):
            for x in range(x0, x1, 2):
                cnt[classify(px[x, y])] += 1
        dom, n = cnt.most_common(1)[0]
        line += {'gray': '.', 'dark': '#', 'red': 'R', 'pink': 'p', 'yellow': 'Y',
                 'blue': 'B', 'green': 'G', 'other': '?'}.get(dom, '?')
    print(f"  y={r*H//ROWS:3d}-{ (r+1)*H//ROWS:3d} ({r*H//ROWS/IN:4.2f}in) {line}")
print("        x: 0    1    2    3    4    5    6    7    8    9    10   11   12")
print("           (each col = {:.2f}in)".format(13.33 / COLS))

# Now find actual pixel colors at representative points
print("\n=== SAMPLE COLORS ===")
for name, (x, y) in {
    'bg(20,20)': (20, 20),
    'title(180,73)': (180, 73),
    'badge(893,70)': (893, 70),
    'rule(400,90)': (400, 90),
}.items():
    print(f"  {name}: {px[x,y]}")

# Find strong-red pixel clusters (circles with red fill)
print("\n=== RED/PINK FILL BLOB BBOXES ===")
mask = [[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        c = classify(px[x, y])
        mask[y][x] = (c in ('red', 'pink'))
seen = [[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if not mask[y][x] or seen[y][x]:
            continue
        st = [(x, y)]
        seen[y][x] = True
        pts = []
        while st:
            cx, cy = st.pop()
            pts.append((cx, cy))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < W and 0 <= ny < H and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        st.append((nx, ny))
        if len(pts) >= 60:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            cx, cy = sum(xs)//len(xs), sum(ys)//len(ys)
            print(f"  n={len(pts):5d} x=[{min(xs)},{max(xs)}] y=[{min(ys)},{max(ys)}] "
                  f"center_in=({cx/IN:.2f},{cy/IN:.2f}) size_in=({(max(xs)-min(xs))/IN:.2f}x{(max(ys)-min(ys))/IN:.2f}) "
                  f"color={px[cx,cy]}")

print("\n=== YELLOW FILL BLOB BBOXES ===")
mask = [[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        mask[y][x] = (classify(px[x, y]) == 'yellow')
seen = [[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if not mask[y][x] or seen[y][x]:
            continue
        st = [(x, y)]
        seen[y][x] = True
        pts = []
        while st:
            cx, cy = st.pop()
            pts.append((cx, cy))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < W and 0 <= ny < H and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        st.append((nx, ny))
        if len(pts) >= 60:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            cx, cy = sum(xs)//len(xs), sum(ys)//len(ys)
            print(f"  n={len(pts):5d} x=[{min(xs)},{max(xs)}] y=[{min(ys)},{max(ys)}] "
                  f"center_in=({cx/IN:.2f},{cy/IN:.2f}) size_in=({(max(xs)-min(xs))/IN:.2f}x{(max(ys)-min(ys))/IN:.2f}) "
                  f"color={px[cx,cy]}")
