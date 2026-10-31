from PIL import Image
from collections import defaultdict

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
SW, SH = 13.33, 7.5
px = im.load()

# Panel x 0.94-7.55 in, y 1.93-5.36 in
PXA, PYA, PXB, PLB = 0.94, 1.93, 7.55, 5.36
PW, PH = PXB - PXA, PLB - PYA

x0, y0 = int(PXA / SW * w), int(PYA / SH * h)
x1, y1 = int(PXB / SW * w), int(PLB / SH * h)

def norm_x(xin):
    return round((xin - PXA) / PW, 3)

def norm_y(yin):
    return round((yin - PYA) / PH, 3)

white = lambda c: min(c) > 240

print("== white circle detection (contiguous white blobs) ==")
seen = [[False] * (x1 - x0) for _ in range(y1 - y0)]
from collections import deque
blobs = []
for yy in range(y1 - y0):
    for xx in range(x1 - x0):
        if not seen[yy][xx] and white(px[(x0 + xx, y0 + yy)]):
            q = deque([(xx, yy)])
            seen[yy][xx] = True
            pts = []
            while q:
                a, b = q.popleft()
                pts.append((a, b))
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2)):
                    na, nb = a + da, b + db
                    if 0 <= na < x1 - x0 and 0 <= nb < y1 - y0 and not seen[nb][na] and white(px[(x0 + na, y0 + nb)]):
                        seen[nb][na] = True
                        q.append((na, nb))
            if len(pts) > 60:
                xs_ = [p[0] for p in pts]; ys_ = [p[1] for p in pts]
                blobs.append((len(pts), min(xs_), max(xs_), min(ys_), max(ys_)))
blobs.sort(key=lambda b: (round(b[1] / 40), -b[0]))
for n, xa, xb, ya, yb in blobs:
    cx, cy = PXA + (xa + xb) / 2 / w * SW, PYA + (ya + yb) / 2 / h * SH
    print(f"  blob n={n:5d} px x {xa}-{xb} y {ya}-{yb} -> center in=({cx:.2f},{cy:.2f}) norm=({norm_x(cx)}, {norm_y(cy)}) diam={ (xb-xa)/w*SW:.2f}x{(yb-ya)/h*SH:.2f} in")
