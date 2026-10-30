import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
red = (R > 140) & (R - G > 60) & (R - B > 60)

def runs1d(v, minlen=2):
    xs = np.where(v)[0]
    if not len(xs):
        return []
    out, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i-1] + 1:
            out.append((s, xs[i-1])); s = xs[i]
    out.append((s, xs[-1]))
    return [(r[0], r[1], r[1]-r[0]+1) for r in out if r[1]-r[0]+1 >= minlen]

# For each quadrant: rows with long horizontal red runs (reference lines) and
# columns with tall vertical red runs (rectangle sides).
QUADS = {"TL": (58, 110, 407, 299), "TR": (473, 110, 902, 299),
         "BL": (57, 300, 469, 539), "BR": (470, 300, 902, 539)}
for name, (x0, y0, x1, y1) in QUADS.items():
    print("=== %s (x%d..%d y%d..%d) ===" % (name, x0, x1, y0, y1))
    sub = np.zeros_like(red); sub[y0:y1+1, x0:x1+1] = True
    m = red & sub
    print("  red px: %d" % m.sum())
    # horizontal runs >= 20px  (reference lines / rect top-bottom)
    hr = []
    for y in range(y0, y1+1):
        for (sx, ex, ln) in runs1d(m[y], 20):
            hr.append((y, sx, ex, ln))
    # group consecutive rows with similar runs
    print("  HORIZONTAL red runs >=20px:")
    seen = set()
    for (y, sx, ex, ln) in hr:
        key = (sx // 5, ex // 5, ln // 5)
        if key in seen:
            continue
        # count rows sharing this run
        cnt = sum(1 for (y2, sx2, ex2, ln2) in hr
                  if abs(sx2 - sx) < 6 and abs(ex2 - ex) < 6)
        seen.add(key)
        print("    y=%3d x %d..%d (w %d) rows~%d" % (y, sx, ex, ln, cnt))
    # vertical runs >= 20px (rect sides)
    vr = []
    for x in range(x0, x1+1):
        for (sy, ey, ln) in runs1d(m[:, x], 20):
            vr.append((x, sy, ey, ln))
    print("  VERTICAL red runs >=20px (count %d):" % len(vr))
    seen = set()
    for (x, sy, ey, ln) in vr:
        key = (sy // 5, ey // 5)
        if key in seen:
            continue
        cnt = sum(1 for (x2, sy2, ey2, ln2) in vr
                  if abs(sy2 - sy) < 6 and abs(ey2 - ey) < 6)
        seen.add(key)
        print("    x=%3d y %d..%d (h %d) cols~%d" % (x, sy, ey, ln, cnt))
