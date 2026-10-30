import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(DECK + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
r = Image.open(DECK + "/recreated_pptx/qa/slide_025/render_3.png").convert("RGB").resize((960, 540), Image.BOX)
r = np.asarray(r).astype(int)

def redm(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 120) & (R - G > 45) & (R - B > 45)

mo, mr = redm(o), redm(r)

def rl(mask, y, x0, x1):
    xs = np.where(mask[y, x0:x1])[0] + x0
    if not len(xs): return []
    out, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i-1]+1: out.append((s, xs[i-1])); s = xs[i]
    out.append((s, xs[-1]))
    return [q for q in out if q[1]-q[0]+1 >= 15]

REGIONS = {
    "TL": (54, 110, 470, 290), "TR": (470, 110, 903, 315),
    "BL": (54, 290, 470, 539), "BR": (470, 315, 903, 539),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    print("=== %s : horizontal red runs (>=15px) ===" % name)
    for tag, m in (("orig", mo), ("rend", mr)):
        rows = []
        for y in range(y0, y1):
            rr = rl(m, y, x0, x1)
            for (s, e) in rr:
                rows.append((y, s, e))
        # collapse: same x-roughly, adjacent rows
        col = []
        for (y, s, e) in rows:
            if col and abs(col[-1][0]-y) <= 2 and abs(col[-1][1]-s) < 12 and abs(col[-1][2]-e) < 12:
                continue
            col.append((y, s, e))
        print("  %s:" % tag, col)
