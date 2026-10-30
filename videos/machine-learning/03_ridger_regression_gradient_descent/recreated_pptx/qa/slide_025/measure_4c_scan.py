import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# strict label-box blue fill: strong pure blue
blue = (B > 150) & (B - R > 100) & (B - G > 80) & (R < 130) & (G < 130)
print("strict blue px: %d" % blue.sum())
for y in [150, 200, 370, 470]:
    xs = np.where(blue[y])[0]
    if len(xs):
        # compress to runs
        runs, s = [], xs[0]
        for i in range(1, len(xs)):
            if xs[i] != xs[i-1] + 1:
                runs.append((s, xs[i-1])); s = xs[i]
        runs.append((s, xs[-1]))
        runs = [r for r in runs if r[1] - r[0] > 5]
        print("y=%d blue runs: %s" % (y, runs))

# white runs per scanline (pure white only)
white = (R > 250) & (G > 250) & (B > 250)
def wruns(y, x0=54, x1=903):
    xs = np.where(white[y, x0:x1])[0] + x0
    if not len(xs):
        return []
    runs, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i-1] + 1:
            runs.append((s, xs[i-1])); s = xs[i]
    runs.append((s, xs[-1]))
    return [(r[0], r[1], r[1]-r[0]+1) for r in runs if r[1]-r[0] > 20]

print("\n--- white runs (len>20px) at body scanlines ---")
for y in [125, 150, 200, 250, 280, 320, 380, 440, 480, 520]:
    print("y=%3d: %s" % (y, wruns(y)))

print("\n--- white runs vertical at x=120, 200, 300, 700, 800 ---")
def vrun(x, y0=45, y1=540):
    ys = np.where(white[y0:y1, x])[0] + y0
    if not len(ys):
        return []
    runs, s = [], ys[0]
    for i in range(1, len(ys)):
        if ys[i] != ys[i-1] + 1:
            runs.append((s, ys[i-1])); s = ys[i]
    runs.append((s, ys[-1]))
    return [(r[0], r[1], r[1]-r[0]+1) for r in runs if r[1]-r[0] > 20]
for x in [120, 200, 300, 650, 750, 840]:
    print("x=%3d: %s" % (x, vrun(x)))
