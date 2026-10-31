from PIL import Image
from collections import defaultdict, deque

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
SW, SH = 13.33, 7.5
px = im.load()

PXA, PYA, PXB, PLB = 0.94, 1.93, 7.55, 5.36
PW, PH = PXB - PXA, PLB - PYA
x0, y0 = int(PXA / SW * w), int(PYA / SH * h)
x1, y1 = int(PXB / SW * w), int(PLB / SH * h)
W, H = x1 - x0, y1 - y0

def nx(xin): return round((xin - PXA) / PW, 3)
def ny(yin): return round((yin - PYA) / PH, 3)

def blobs(pred, minn=25, label=""):
    seen = [[False] * W for _ in range(H)]
    out = []
    for yy in range(H):
        for xx in range(W):
            if seen[yy][xx] or not pred(px[(x0 + xx, y0 + yy)]):
                continue
            q = deque([(xx, yy)]); seen[yy][xx] = True; pts = []
            while q:
                a, b = q.popleft(); pts.append((a, b))
                for da in range(-2, 3):
                    for db in range(-2, 3):
                        na, nb = a + da, b + db
                        if 0 <= na < W and 0 <= nb < H and not seen[nb][na] and pred(px[(x0 + na, y0 + nb)]):
                            seen[nb][na] = True; q.append((na, nb))
            if len(pts) >= minn:
                xs_ = [p[0] for p in pts]; ys_ = [p[1] for p in pts]
                out.append((len(pts), min(xs_), max(xs_), min(ys_), max(ys_)))
    out.sort(key=lambda b: (b[1], b[3]))
    print(f"== {label} ==")
    for n, xa, xb, ya, yb in out:
        cx = PXA + (xa + xb) / 2 / w * SW
        cy = PYA + (ya + yb) / 2 / h * SH
        print(f"  n={n:4d} center in=({cx:.2f},{cy:.2f}) norm=({nx(cx)},{ny(cy)}) size={(xb-xa)/w*SW:.2f}x{(yb-ya)/h*SH:.2f}")
    return out

# strong red (sigma glyphs, Net_j/O_j labels are also red)
strongred = lambda c: c[0] > 170 and c[0] - c[1] > 95 and c[0] - c[2] > 95
blobs(strongred, 20, "strong-red blobs (sigma + labels)")

blue = lambda c: c[2] > c[0] + 60 and c[2] > 120 and c[0] < 90
blobs(blue, 15, "blue blobs (col2 outlines / w_ji)")

green = lambda c: c[1] > c[0] + 60 and c[1] > c[2] + 60 and c[1] > 110
blobs(green, 15, "green blobs (col3 outlines / arrow)")

mag = lambda c: c[0] > 140 and c[0] - c[1] > 55 and c[2] - c[1] > 55 and c[0] > 140
blobs(mag, 12, "magenta blobs (input dots)")

pink = lambda c: 200 < c[0] < 240 and 140 < c[1] < 190 and 140 < c[2] < 190 and c[0] - c[1] > 30
blobs(pink, 30, "pink connection-line blobs")
