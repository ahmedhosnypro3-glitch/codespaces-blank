# Slide 025 terrain census: jet-core blobs + dark ink structure (orig vs render_3).
# Run: python3 measure_6_terrain.py
import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
renF = np.asarray(Image.open(DECK + "/recreated_pptx/qa/slide_025/render_3.png").convert("RGB")).astype(int)
ren = np.asarray(Image.fromarray(renF.astype(np.uint8)).resize((960, 540), Image.BOX)).astype(int)

# known measured figure boxes (prior lane, frame px, inclusive)
BOX = {"TL": (85, 115, 265, 288), "TR": (616, 115, 879, 317),
       "BL": (83, 290, 376, 527), "BR": (615, 344, 880, 531)}
INSET = 8   # inside the red border + grid margin


def m_jetred(img):   # saturated red-orange-yellow jet top band (max channel = R)
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return (r > 150) & (r - g > 60) & (r - b > 60) & (g < 130)


def m_jetblue(img):  # jet bottom band (max channel = B)
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return (b > 110) & (b - r > 50) & (b - g > 30)


def m_dark(img):
    return (img.max(axis=2) < 105)


def label(mask, min_area=6):
    H, W = mask.shape
    seen = np.zeros((H, W), dtype=bool)
    out = []
    ys, xs = np.where(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]; seen[y0, x0] = True; pix = []
        while stack:
            y, x = stack.pop(); pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
        if len(pix) >= min_area:
            ys2 = [p[0] for p in pix]; xs2 = [p[1] for p in pix]
            out.append((len(pix), min(xs2), max(xs2), min(ys2), max(ys2)))
    return sorted(out, key=lambda t: -t[0])


for name, (x0, y0, x1, y1) in BOX.items():
    ix0, iy0, ix1, iy1 = x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET
    print("=== %s interior x%d..%d y%d..%d ===" % (name, ix0, iy0, ix1, iy1))
    for tag, img in (("orig", orig), ("render", ren)):
        jr = m_jetred(img)[iy0:iy1 + 1, ix0:ix1 + 1]
        jb = m_jetblue(img)[iy0:iy1 + 1, ix0:ix1 + 1]
        dk = m_dark(img)[iy0:iy1 + 1, ix0:ix1 + 1]
        rb = label(jr, 40); bb = label(jb, 40); db = label(dk, 20)
        print("  %-6s jetred px %5d (%d blobs)  jetblue px %5d (%d blobs)  dark px %4d (%d blobs)"
              % (tag, jr.sum(), len(rb), jb.sum(), len(bb), dk.sum(), len(db)))
        print("      red blobs  :", [(c[1] + ix0, c[2] + ix0, c[3] + iy0, c[4] + iy0, c[0]) for c in rb[:6]])
        print("      blue blobs :", [(c[1] + ix0, c[2] + ix0, c[3] + iy0, c[4] + iy0, c[0]) for c in bb[:6]])
        print("      dark blobs :", [(c[1] + ix0, c[2] + ix0, c[3] + iy0, c[4] + iy0, c[0]) for c in db[:12]])

print("\n=== BR interior hue-scan: red/blue crossings along vertical cuts ===")
x0, y0, x1, y1 = BOX["BR"]
for tag, img in (("orig", orig), ("render", ren)):
    for xc in (x0 + 70, x0 + 130, x0 + 190, x0 + 250):
        col = img[y0 + 10:y1 - 10, xc]
        r, g, b = col[:, 0], col[:, 1], col[:, 2]
        red = (r - g > 60) & (r - b > 60) & (r > 150)
        blue = (b - r > 50) & (b - g > 30) & (b > 110)
        # count transitions red<->blue along the column
        seq = []
        for i in range(len(col)):
            if red[i]:
                seq.append("R")
            elif blue[i]:
                seq.append("B")
        trans = sum(1 for i in range(1, len(seq)) if seq[i] != seq[i - 1] and seq[i] and seq[i - 1])
        print("  %-6s x=%d: red runs %d blue runs %d transitions %d (col h %d)"
              % (tag, xc, sum(1 for i in range(1, len(seq) + 1) if seq[i - 1:i] == ["R"] and (i == 1 or seq[i - 2] != "R")),
                 sum(1 for i in range(1, len(seq) + 1) if seq[i - 1:i] == ["B"] and (i == 1 or seq[i - 2] != "B")),
                 trans, len(col)))

print("\n=== BL annotation text: dark blob census (orig) ===")
x0, y0, x1, y1 = BOX["BL"]
dk = m_dark(orig)[y0 + 8:y1 - 8, x0 + 8:x1 - 8]
for c in label(dk, 12):
    print("   x%d..%d y%d..%d a=%d" % (c[1] + x0 + 8, c[2] + x0 + 8, c[3] + y0 + 8, c[4] + y0 + 8, c[0]))
