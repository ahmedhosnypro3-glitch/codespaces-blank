import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]

white = (R > 248) & (G > 248) & (B > 248)
blue = (B > 150) & (B - R > 100) & (B - G > 80) & (R < 130) & (G < 130)
white = white & ~blue

def runs(v, minlen):
    xs = np.where(v)[0]
    if not len(xs):
        return []
    out, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i-1] + 1:
            out.append((s, xs[i-1])); s = xs[i]
    out.append((s, xs[-1]))
    return [r for r in out if r[1]-r[0]+1 >= minlen]

# per quadrant: rows whose LONGEST white run is >= 60px -> those rows belong to
# the figure interior. Take the union bbox of those runs.
QUADS = {"TL": (54, 45, 470, 292), "TR": (470, 45, 903, 320),
         "BL": (54, 292, 470, 540), "BR": (470, 320, 903, 540)}
for name, (x0, y0, x1, y1) in QUADS.items():
    xs_all, ys_all, longruns = [], [], []
    for y in range(y0, y1):
        rr = runs(white[y, x0:x1], 60)
        if rr:
            best = max(rr, key=lambda r: r[1]-r[0])
            longruns.append((y, best[0]+x0, best[1]+x0))
            xs_all += [best[0]+x0, best[1]+x0]
            ys_all.append(y)
    if not ys_all:
        print(name, "NO white figure found")
        continue
    x0f, x1f = min(xs_all), max(xs_all)
    y0f, y1f = min(ys_all), max(ys_all)
    print("=== %s ===" % name)
    print("  white interior bbox: x %d..%d (w %d)  y %d..%d (h %d)" % (x0f, x1f, x1f-x0f+1, y0f, y1f, y1f-y0f+1))
    print("  -> red-bordered figure box (interior + 1px border): x %d..%d  y %d..%d  (w %d, h %d)"
          % (x0f-1, x1f+1, y0f-1, y1f+1, x1f-x0f+3, y1f-y0f+3))
    print("  rows with long white runs: %d..%d (%d rows)" % (y0f, y1f, len(longruns)))
