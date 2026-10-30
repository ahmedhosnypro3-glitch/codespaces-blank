"""Fine-grained element map for slide_028: connected components of saturated + dark ink."""
import numpy as np
from PIL import Image
from collections import Counter, deque

o = np.asarray(Image.open("../../unique_slides/slide_028.jpg").convert("RGB")).astype(int)

# The real slide occupies x 62..901, y 42..517 (letterbox margins around it).
X0, X1, Y0, Y1 = 62, 902, 42, 518
SL = o[Y0:Y1, X0:X1]
h, w, _ = SL.shape
r, g, b = SL[..., 0], SL[..., 1], SL[..., 2]
mx = SL.max(axis=2); mn = SL.min(axis=2); sat = mx - mn

# ink = anything that is not the light gray bg (231,233,230) and not near-white (254,255,253)
bgmask = (np.abs(SL - np.array([231, 233, 230])).max(axis=2) < 22) | \
         (np.abs(SL - np.array([254, 255, 253])).max(axis=2) < 12)
ink = ~bgmask

print("ink fraction of content region:", round(ink.mean(), 4))

def components(mask, minpx=25):
    lab = np.zeros(mask.shape, dtype=int)
    cur = 0
    H, W = mask.shape
    out = []
    for sy in range(H):
        for sx in range(W):
            if mask[sy, sx] and lab[sy, sx] == 0:
                cur += 1
                q = deque([(sy, sx)])
                lab[sy, sx] = cur
                pix = []
                while q:
                    y, x = q.popleft()
                    pix.append((y, x))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = y+dy, x+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny,nx] and lab[ny,nx]==0:
                            lab[ny,nx] = cur
                            q.append((ny,nx))
                if len(pix) >= minpx:
                    ys = [p[0] for p in pix]; xs = [p[1] for p in pix]
                    out.append((len(pix), min(xs), max(xs), min(ys), max(ys)))
    return sorted(out, key=lambda t: (t[3], t[1]))

# Focused: strong structural elements (large saturated blobs + black bars)
print("\n=== BLACK/NEAR-BLACK components (>=60px) ===")
blk = (mx < 105) & (sat < 70)
for n, x0, x1, y0, y1 in components(blk, 60):
    print("  n=%5d  x %3d..%3d  y %3d..%3d   (frame x %d..%d y %d..%d)" %
          (n, x0, x1, y0, y1, x0+X0, x1+X0, y0+Y0, y1+Y0))

print("\n=== SATURATED components (>=120px) ===")
satmask = (sat > 45) & ~((mx < 105))
for n, x0, x1, y0, y1 in components(satmask, 120):
    mid = SL[(y0+y1)//2, (x0+x1)//2]
    print("  n=%5d  x %3d..%3d  y %3d..%3d   (frame x %d..%d y %d..%d) mid=%s" %
          (n, x0, x1, y0, y1, x0+X0, x1+X0, y0+Y0, y1+Y0, tuple(mid)))
