import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
R, G, B = orig[..., 0], orig[..., 1], orig[..., 2]
panel = (np.abs(R-233) < 14) & (np.abs(G-233) < 14) & (np.abs(B-231) < 14)
blue = (B > 150) & (B - R > 100) & (B - G > 80) & (R < 130) & (G < 130)

# content = not panel gray, not blue, inside the panel region
content = ~panel & ~blue
content[:45, :] = False; content[540:, :] = False
content[:, :54] = False; content[:, 904:] = False

QUADS = {"TL": (54, 45, 470, 291), "TR": (470, 45, 903, 311),
         "BL": (54, 291, 470, 539), "BR": (470, 311, 903, 539)}
for name, (x0, y0, x1, y1) in QUADS.items():
    print("=== %s: per-row CONTENT extent (excl panel-gray, excl blue boxes) ===" % name)
    for y in range(y0, y1+1, 12):
        xs = np.where(content[y, x0:x1])[0] + x0
        if not len(xs):
            print("  y=%3d  (none)" % y); continue
        # compress into runs >=4px
        o, s = [], xs[0]
        for i in range(1, len(xs)):
            if xs[i] != xs[i-1]+1: o.append((s, xs[i-1])); s = xs[i]
        o.append((s, xs[-1]))
        o = [q for q in o if q[1]-q[0]+1 >= 4]
        # merge runs with gaps < 3
        m = []
        for q in o:
            if m and q[0] - m[-1][1] <= 3: m[-1] = (m[-1][0], q[1])
            else: m.append(q)
        print("  y=%3d  %s" % (y, m))
