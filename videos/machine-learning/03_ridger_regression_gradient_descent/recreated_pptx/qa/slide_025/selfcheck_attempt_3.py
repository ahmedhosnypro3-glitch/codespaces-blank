"""Slide 025 self-check: render_3 vs original frame (960x540 frame space).

Run:  python3 selfcheck_attempt_3.py
Prints every measured number for the worker report.
"""
import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_025.jpg"
REND = DECK + "/recreated_pptx/qa/slide_025/render_3.png"

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
ren = np.asarray(Image.open(REND).convert("RGB")).astype(int)
Ro, Go, Bo = orig[..., 0], orig[..., 1], orig[..., 2]
Rr, Gr, Br = ren[..., 0], ren[..., 1], ren[..., 2]
print("orig %s   render %s" % (orig.shape[1::-1], ren.shape[1::-1]))

sc = ren.shape[1] / 960.0          # render-px per frame-px
print("scale %.6f render-px/frame-px" % sc)

def down(img):
    """Render -> frame space (PIL BOX/area average to 960x540)."""
    from PIL import Image
    return np.asarray(Image.fromarray(img.astype(np.uint8)).resize(
        (960, 540), Image.BOX)).astype(int)

fr = down(ren).astype(int)          # 540 x 960
r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
print("frame-space render %s" % (fr.shape[1],))

# ---------- 1. frame containment: ink outside the gray panel ----------
panel = (np.abs(Ro - 233) < 12) & (np.abs(Go - 233) < 12) & (np.abs(Bo - 231) < 12)
out = np.zeros_like(panel); out[45:540, 54:903] = True
notpanel_o, notpanel_r = ~panel, ~((np.abs(r-233)<14)&(np.abs(g-233)<14)&(np.abs(b-231)<14))
ink_o = notpanel_o & out
ink_r = notpanel_r & out
print("\n[1] FRAME CONTAINMENT (content ink vs panel edges, frame px)")
print("  original ink at x<54: %d   x>902: %d   y<45: %d   y>538: %d"
      % (ink_o[:, :54].sum(), ink_o[:, 903:].sum(), ink_o[:45].sum(), ink_o[539:].sum()))
print("  render   ink at x<54: %d   x>902: %d   y<45: %d   y>538: %d"
      % (ink_r[:, :54].sum(), ink_r[:, 903:].sum(), ink_r[:45].sum(), ink_r[539:].sum()))

# ---------- 2. title ink ----------
def ink_bbox(mask, x0, x1, y0, y1):
    sub = np.zeros_like(mask); sub[y0:y1, x0:x1] = True
    ys, xs = np.where(mask & sub)
    if not len(xs): return None
    return xs.min(), xs.max(), ys.min(), ys.max()

red_o = (Ro > 130) & (Ro - Go > 55) & (Ro - Bo > 55)
red_r = (r > 120) & (r - g > 45) & (r - b > 45)
# title band only (above panel plots, y 50..110), excluding badge
tb_o = np.zeros_like(red_o); tb_o[50:110, :] = True; tb_o[50:100, 830:920] = True
tb_r = np.zeros_like(red_r); tb_r[50:110, :] = True; tb_r[50:100, 830:920] = True
to = ink_bbox(red_o & tb_o, 0, 960, 0, 540)
tr = ink_bbox(red_r & tb_r, 0, 960, 0, 540)
print("\n[2] TITLE INK (red, band y50..110)")
print("  original: %s" % (to,))
print("  render  : %s" % (tr,))
if to and tr:
    print("  dx_left %d  dx_right %d  dy_top %d  dy_bottom %d"
          % (tr[0]-to[0], tr[1]-to[1], tr[2]-to[2], tr[3]-to[3]))

# ---------- 3. blue label boxes ----------
blue_o = (Bo > 150) & (Bo - Ro > 100) & (Bo - Go > 80) & (Ro < 130) & (Go < 130)
blue_r = (b > 150) & (b - r > 90) & (b - g > 70) & (r < 140) & (g < 140)
print("\n[3] BLUE LABEL BOXES (fill px count + bbox via row bands)")
def boxes(mask, tag):
    rows = mask.sum(axis=1)
    bands, inb = [], False
    for y in range(130, 500):
        if rows[y] > 200 and not inb: inb, s = True, y
        elif rows[y] <= 200 and inb:
            inb = False
            if y - s > 10: bands.append((s, y-1))
    if inb: bands.append((s, 499))
    res = []
    for (y0, y1) in bands:
        sub = np.zeros_like(mask); sub[y0:y1+1, :] = True
        ys, xs = np.where(mask & sub)
        res.append((xs.min(), xs.max(), y0, y1, mask.sum() if False else (mask & sub).sum()))
    for (x0, x1, y0, y1, n) in res:
        print("  %-8s x %d..%d (w %d) y %d..%d (h %d) px %d" % (tag, x0, x1, x1-x0+1, y0, y1, y1-y0+1, n))
    return res
bo = boxes(blue_o, "orig"); br = boxes(blue_r, "render")
print("  count orig %d render %d" % (len(bo), len(br)))

# ---------- 4. white figure rects (plot boxes) ----------
white_o = (Ro > 248) & (Go > 248) & (Bo > 248) & ~blue_o
white_r = (r > 245) & (g > 245) & (b > 245) & ~blue_r
print("\n[4] PLOT WHITE-FIGURE INTERIORS (rows whose longest white run >= 60px)")
QUADS = {"TL": (54, 45, 470, 292), "TR": (470, 45, 903, 320),
         "BL": (54, 292, 470, 540), "BR": (470, 320, 903, 540)}
def runs(v, minlen):
    xs = np.where(v)[0]
    if not len(xs): return []
    o, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i-1]+1: o.append((s, xs[i-1])); s = xs[i]
    o.append((s, xs[-1]))
    return [q for q in o if q[1]-q[0]+1 >= minlen]
def figbox(white, x0, y0, x1, y1):
    xs_all, ys_all = [], []
    for y in range(y0, y1):
        rr = runs(white[y, x0:x1], 60)
        if rr:
            best = max(rr, key=lambda q: q[1]-q[0])
            xs_all += [best[0]+x0, best[1]+x0]; ys_all.append(y)
    if not ys_all: return None
    return min(xs_all), max(xs_all), min(ys_all), max(ys_all)
for name, (x0, y0, x1, y1) in QUADS.items():
    fo, fq = figbox(white_o, x0, y0, x1, y1), figbox(white_r, x0, y0, x1, y1)
    if fo and fq:
        print("  %s orig x%d..%d y%d..%d (w%d h%d) | render x%d..%d y%d..%d (w%d h%d) | dL%d dR%d dT%d dB%d"
              % (name, fo[0], fo[1], fo[2], fo[3], fo[1]-fo[0]+1, fo[3]-fo[2]+1,
                 fq[0], fq[1], fq[2], fq[3], fq[1]-fq[0]+1, fq[3]-fq[2]+1,
                 fq[0]-fo[0], fq[1]-fo[1], fq[2]-fo[2], fq[3]-fo[3]))
    else:
        print("  %s orig %s render %s" % (name, fo, fq))

# ---------- 5. red reference lines (pure horizontal runs) ----------
print("\n[5] RED HORIZONTAL REFERENCE LINES (>=60px runs, per quadrant)")
def hlines(mask, tag, x0, y0, x1, y1):
    sub = np.zeros_like(mask); sub[y0:y1+1, x0:x1+1] = True
    m = mask & sub & ~blue_o if tag == "orig" else mask & sub
    found = []
    for y in range(y0, y1+1):
        for (sx, ex) in runs(m[y], 60):
            found.append((y, sx, ex))
    # collapse adjacent rows
    out = []
    for (y, sx, ex) in found:
        if out and abs(out[-1][0]-y) <= 1 and abs(out[-1][1]-sx) < 8 and abs(out[-1][2]-ex) < 8:
            continue
        out.append((y, sx, ex))
    for o in out:
        print("  %-7s y=%d x %d..%d (w %d)" % (tag, o[0], o[1], o[2], o[2]-o[1]+1))
    return out
for name, (x0, y0, x1, y1) in QUADS.items():
    hlines(red_o, "orig", x0, y0, x1, y1)
    hlines(red_r, "render", x0, y0, x1, y1)

# ---------- 6. curve smoothness (second-difference ripple) on the render plots
print("\n[6] SURFACE RENDER DENSITY (jet-saturated px inside each measured figbox)")
sa_o = (orig.max(axis=2) - orig.min(axis=2)) > 45
sa_r = (fr.max(axis=2) - fr.min(axis=2)) > 45
FB = {"TL": (91, 122, 260, 282), "TR": (622, 122, 871, 310),
      "BL": (89, 296, 371, 521), "BR": (619, 347, 873, 528)}
for name, (x0, y0, x1, y1) in FB.items():
    so = np.zeros_like(sa_o); so[y0:y1+1, x0:x1+1] = True
    sr = np.zeros_like(sa_r); sr[y0:y1+1, x0:x1+1] = True
    print("  %s jet px orig %d  render %d  (box %dx%d)"
          % (name, (sa_o & so).sum(), (sa_r & sr).sum(), x1-x0+1, y1-y0+1))
