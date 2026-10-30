# PIL probe: slide_019 original frame — read W-vector values + ink colors.
# Frame 960x540, 1px=1pt. Build geometry: NO REG x0=124, RIDGE 3 x0=384, RIDGE 10 x0=644.
import sys
from PIL import Image

im = Image.open("videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg").convert("RGB")
W, H = im.size
print("frame size", W, H)

def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    if mx > 200 and mx - mn < 25:
        return "."          # near-white bg
    if r > 140 and g < 110 and b < 110:
        return "R"          # red
    if b > 120 and b - r > 40 and b - g > 40:
        return "B"          # blue
    if g > 100 and g - r > 30 and g - b > 30:
        return "G"          # green
    if r > 200 and g > 180 and b < 140:
        return "Y"          # yellow band
    if mx < 110:
        return "#"          # black/dark ink
    if r > 200 and g < 190 and b < 190 and abs(r-g) < 60:
        return "y"          # faint tint (peach/cream/mint-ish)
    return "?"

def census(x0, y0, x1, y1, label):
    sub = im.crop((x0, y0, x1, y1))
    px = sub.load()
    w, h = sub.size
    hist = {}
    for yy in range(h):
        for xx in range(w):
            c = classify(px[xx, yy])
            hist[c] = hist.get(c, 0) + 1
    ink = {k: v for k, v in hist.items() if k not in (".",)}
    print(f"--- {label}  bbox=({x0},{y0},{x1},{y1}) ink={ink}")

def ascii_art(x0, y0, x1, y1, label, step=2):
    sub = im.crop((x0, y0, x1, y1))
    px = sub.load()
    w, h = sub.size
    print(f"=== ASCII {label} bbox=({x0},{y0},{x1},{y1}) step={step} ({w}x{h})")
    hdr = "".join(str((x0 + i) // 10 % 10) if (x0 + i) % 10 == 0 else " " for i in range(0, w, step))
    print("    " + hdr)
    for yy in range(0, h, step):
        row = "".join(classify(px[xx, yy]) for xx in range(0, w, step))
        print(f"{y0+yy:4d}{row}")

def ascii_art_double(x0, y0, x1, y1, label):
    # full-res (step 1) ascii with digits, only ink rows/cols trimmed
    sub = im.crop((x0, y0, x1, y1))
    px = sub.load()
    w, h = sub.size
    cols_with_ink = []
    rows_with_ink = []
    for yy in range(h):
        for xx in range(w):
            if classify(px[xx, yy]) not in (".",):
                rows_with_ink.append(yy)
                break
    for xx in range(w):
        for yy in range(h):
            if classify(px[xx, yy]) not in (".",):
                cols_with_ink.append(xx)
                break
    if not rows_with_ink:
        print(f"=== {label}: NO INK in bbox")
        return
    ry0, ry1 = min(rows_with_ink), max(rows_with_ink)
    cx0, cx1 = min(cols_with_ink), max(cols_with_ink)
    print(f"=== {label} ink rows y{y0+ry0}..{y0+ry1} cols x{x0+cx0}..{x0+cx1}")
    for yy in range(ry0, ry1 + 1):
        row = "".join(classify(px[xx, yy]) for xx in range(cx0, cx1 + 1))
        print(f"{y0+yy:4d} {row}")

# 1) VALUE READ: NO REG row2 W entries — build says x173..189, rows ~gy+6..gy+54 (gy=310)
ascii_art_double(160, 300, 210, 380, "NO REG row2 W cell (entries strip)")
# 2) VALUE READ: RIDGE 10 row3 W entries — build says x693..709, gy=420
ascii_art_double(680, 410, 730, 490, "RIDGE 10 row3 W cell (entries strip)")

# 3) COLOR census: W entries region for all 9 cells
for cname, x0 in [("NO REG", 124), ("RIDGE 3", 384), ("RIDGE 10", 644)]:
    for gi, gy in enumerate([205, 310, 420]):
        census(x0 + 45, gy + 2, x0 + 70, gy + 62, f"{cname} g{gi+1} W entries")
        census(x0 + 16, gy + 20, x0 + 40, gy + 40, f"{cname} g{gi+1} W= label")
        census(x0 + 6, gy + 66, x0 + 82, gy + 86, f"{cname} g{gi+1} norm label")
        v0 = x0 + 142
        gx1 = 380 if cname == "NO REG" else (640 if cname == "RIDGE 3" else 888)
        colW = (gx1 - v0) / 3
        for ti in range(3):
            census(int(v0 + ti * colW), gy + 4, int(v0 + (ti + 1) * colW), gy + 20, f"{cname} g{gi+1} Test header {ti+1}")
        census(int(v0), gy + 23, int(gx1), gy + 40, f"{cname} g{gi+1} x1 row")
        census(int(v0), gy + 43, int(gx1), gy + 62, f"{cname} g{gi+1} x2 row")
        census(int(v0), gy + 68, int(gx1), gy + 88, f"{cname} g{gi+1} y row")

# 4) z labels in Test Data box
for lx in (156, 246, 342):
    census(lx, 96, lx + 36, 122, f"z label x{lx}")

# 5) header band tint behind Ridge λ=3 header (x384..640, y172..203)
census(384, 172, 640, 203, "RIDGE 3 header band bg")
census(124, 172, 380, 203, "NO REG header band bg")
census(644, 172, 900, 203, "RIDGE 10 header band bg")
