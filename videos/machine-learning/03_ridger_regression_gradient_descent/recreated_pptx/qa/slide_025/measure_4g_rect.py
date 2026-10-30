import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
red = (R > 130) & (R - G > 55) & (R - B > 55)

# Label-box blue (strict)
blue = (B > 150) & (B - R > 100) & (B - G > 80) & (R < 130) & (G < 130)

QUADS = {"TL": (55, 105, 412, 292), "TR": (468, 105, 905, 320),
         "BL": (52, 292, 475, 540), "BR": (460, 320, 905, 539)}
for name, (x0, y0, x1, y1) in QUADS.items():
    sub = np.zeros_like(red); sub[y0:y1+1, x0:x1+1] = True
    m = red & sub & ~blue
    # top border: the row with the widest horizontal red run
    best_h, best_v = None, None
    for y in range(y0, y1+1):
        xs = np.where(m[y])[0]
        if len(xs) < 40:
            continue
        w = xs.max() - xs.min() + 1
        if best_h is None or w > best_h[3]:
            best_h = (y, xs.min(), xs.max(), w)
    for x in range(x0, x1+1):
        ys = np.where(m[:, x])[0]
        if len(ys) < 40:
            continue
        h = ys.max() - ys.min() + 1
        if best_v is None or h > best_v[3]:
            best_v = (x, ys.min(), ys.max(), h)
    # bottom border: lowest row with a wide run matching top's extent
    if best_h:
        ty, tx0, tx1, tw = best_h
        bot = None
        for y in range(y1, ty, -1):
            xs = np.where(m[y])[0]
            if len(xs) < 40:
                continue
            w = xs.max() - xs.min() + 1
            if w > 0.75 * tw:
                bot = (y, xs.min(), xs.max(), w)
                break
        left = best_v
        print("=== %s ===" % name)
        print("  top    border y=%d  x %d..%d (w %d)" % best_h)
        if bot:
            print("  bottom border y=%d  x %d..%d (w %d)" % bot)
        print("  longest vertical side: x=%d  y %d..%d (h %d)" % best_v)
        if bot:
            print("  => window approx x %d..%d  y %d..%d  (w %d, h %d)"
                  % (tx0, tx1, ty, bot[0], tx1 - tx0 + 1, bot[0] - ty + 1))
