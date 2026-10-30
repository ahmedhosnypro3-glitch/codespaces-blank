import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"

im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]

panel = (np.abs(R - 233) < 12) & (np.abs(G - 233) < 12) & (np.abs(B - 231) < 12)
white = (R > 242) & (G > 242) & (B > 242)
blue = (B > 120) & (B - R > 60) & (B - G > 40)
red = (R > 140) & (R - G > 60) & (R - B > 60)

# Inside the panel only (x 54..903, y 45..540)
inside = np.zeros_like(panel)
inside[45:540, 54:903] = True

# White figure = white AND inside panel
wf = white & inside & ~panel
print("white-figure px inside panel: %d" % wf.sum())
print("blue px: %d   red px: %d" % (blue.sum(), red.sum()))

# quadrant white-figure bboxes (exclude blue box pixels)
QUADS = {
    "TL": (54, 45, 470, 300),
    "TR": (470, 45, 903, 300),
    "BL": (54, 300, 470, 540),
    "BR": (470, 300, 903, 540),
}
for name, (x0, y0, x1, y1) in QUADS.items():
    sub = np.zeros_like(wf)
    sub[y0:y1, x0:x1] = True
    m = wf & sub & ~blue
    ys, xs = np.where(m)
    if len(ys):
        print("%s white-fig bbox x %d..%d (w %d)  y %d..%d (h %d)  px %d"
              % (name, xs.min(), xs.max(), xs.max() - xs.min() + 1,
                 ys.min(), ys.max(), ys.max() - ys.min() + 1, m.sum()))
    else:
        print(name, "no white")

# ---- blue label box bboxes
ys, xs = np.where(blue)
print("\nblue ink bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
# split blue into 4 boxes by clustering rows
rows = np.zeros(H, int)
for y in range(H):
    rows[y] = blue[y].sum()
for y in range(45, 540):
    if rows[y] > 0:
        pass
# find row bands
def bands(mask1d, thr):
    out, inb = [], False
    for i, v in enumerate(mask1d):
        if v > thr and not inb:
            inb, s = True, i
        elif v <= thr and inb:
            inb = False
            out.append((s, i - 1))
    if inb:
        out.append((s, len(mask1d) - 1))
    return out
bb = bands(rows, 3)
print("blue row bands:", bb)
for (y0, y1) in bb:
    sub = np.zeros_like(blue)
    sub[y0:y1 + 1, :] = True
    m = blue & sub
    ys2, xs2 = np.where(m)
    print("  blue box y %d..%d -> x %d..%d (w %d) px %d"
          % (y0, y1, xs2.min(), xs2.max(), xs2.max() - xs2.min() + 1, m.sum()))
