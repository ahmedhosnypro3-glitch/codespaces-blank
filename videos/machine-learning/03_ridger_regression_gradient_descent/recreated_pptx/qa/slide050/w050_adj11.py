#!/usr/bin/env python3
"""PIL adjudication of slide 050 judge_attempt_11 (render_13) vs original.
F1 eta-zone recheck; F2 red-line trajectory w/ per-image marker calibration; F3 +ve centroid."""
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide050/w050_adj11_raw.txt"

o = np.asarray(Image.open(f"{NS}/unique_slides/slide_050.jpg").convert("RGB")).astype(int)
r_im = Image.open(f"{NS}/recreated_pptx/qa/slide050/render_13.png").convert("RGB")
s = r_im.size[0] / 960.0
r = np.asarray(r_im).astype(int)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def zone(img, x0, x1, y0, y1):
    return img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)] if s > 1.01 else img[y0:y1, x0:x1]

def lum(z): return 0.299*z[:,:,0]+0.587*z[:,:,1]+0.114*z[:,:,2]
def masks(z):
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    pink = (R > 195) & (R-G > 25) & (R-B > 25) & (G > 130) & (B > 130)
    blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
    ink = lum(z) < 200
    return ink, red, blue, pink

P("== 050 adj attempt-11, render_13 scale", round(s, 4))

# ---- F1: eta zone (att11 #1: original allegedly has "eta = 1" right of "Step") ----
P("\n## F1 eta zone x531..642 y58..84 (ink/red counts)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 531, 642, 58, 84)
    ink, red, blue, pink = masks(z)
    P(f" {name}: ink={int(ink.sum())} red={int(red.sum())}")
P("\n## F1b red REPEAT-phrase x-extent (zone x426..532 y58..84)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 426, 532, 58, 84)
    _, red, _, _ = masks(z)
    cols = np.where(red.any(axis=0))[0]
    P(f" {name} red phrase x-extent: {426+cols[0]/s:.0f}..{426+cols[-1]/s:.0f}" if len(cols) else f" {name}: none")
P("\n## F1c header ascii x500..650 y58..84 (ink, step2)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 500, 650, 58, 84)
    ink, _, _, _ = masks(z)
    P(f" {name}:")
    for yy in range(0, ink.shape[0], 2):
        P("   " + "".join("#" if ink[yy, xx:xx+2].sum() > 0 else "." for xx in range(0, ink.shape[1], 2)))

# ---- F2: red components in chart window; line = widest ----
P("\n## F2 red components (chart x300..835 y160..495), line fit + endpoints")
CW = (300, 835, 160, 495)
def chart_components(img):
    z = zone(img, *CW)
    _, red, _, _ = masks(z)
    lab, n = ndimage.label(red, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < 30: continue
        comps.append(dict(n=len(ys),
                          x0=CW[0]+xs.min()/s, x1=CW[0]+xs.max()/s,
                          y0=CW[2]+ys.min()/s, y1=CW[2]+ys.max()/s,
                          mask=(lab == i)))
    return comps

def calib(img):
    # marker centroids -> data affine (blue squares, pink diamonds, red triangles)
    z = zone(img, *CW)
    _, red, blue, pink = masks(z)
    pts = {}
    for cname, m, want in (("blue", blue, 3), ("pink", pink, 3), ("redtri", red, 3)):
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        cents = []
        for i in range(1, n+1):
            ys, xs = np.where(lab == i)
            if not (30 <= len(ys) <= 900): continue
            w = xs.max()-xs.min(); h = ys.max()-ys.min()
            if w > 60 or h > 60: continue          # skip the line component
            cents.append((CW[0]+xs.mean()/s, CW[2]+ys.mean()/s))
        cents.sort()
        pts[cname] = cents[:want]
    # data anchors: blue (0,2)(1,1)(2,1); pink (5,4)(6,5)(6,6); redtri (0,0)(3,2)(7,6)
    anchors = []
    for (cname, coords) in (("blue", [(0,2),(1,1),(2,1)]), ("pink", [(5,4),(6,5),(6,6)]), ("redtri", [(0,0),(3,2),(7,6)])):
        for (fx, fy), (dx, dy) in zip(pts.get(cname, []), coords):
            anchors.append((fx, fy, dx, dy))
    if len(anchors) < 6:
        return None, anchors
    ax = np.array([a[0] for a in anchors]); ay = np.array([a[1] for a in anchors])
    dx = np.array([a[2] for a in anchors]); dy = np.array([a[3] for a in anchors])
    A = np.vstack([ax, np.ones_like(ax)]).T
    (a1, a0), res1, _, _ = np.linalg.lstsq(A, dx, rcond=None)
    B = np.vstack([ay, np.ones_like(ay)]).T
    (b1, b0), res2, _, _ = np.linalg.lstsq(B, dy, rcond=None)
    return dict(x=a1, xb=a0, y=b1, yb=b0), anchors

for name, img in (("ORIG", o), ("RENDER", r)):
    comps = chart_components(img)
    for c in sorted(comps, key=lambda c: -c["n"])[:6]:
        P(f" {name} comp n={c['n']} bbox x{c['x0']:.0f}..{c['x1']:.0f} y{c['y0']:.0f}..{c['y1']:.0f}")
    line = max(comps, key=lambda c: (c["x1"]-c["x0"]))
    cols = np.where(line["mask"].any(axis=0))[0]
    fit_rows = []
    for cc in cols:
        rr = np.where(line["mask"][:, cc])[0]
        fit_rows.append((cc, np.median(rr)))
    cx = np.array([CW[0]+c/s for c, _ in fit_rows])
    cy = np.array([CW[2]+v/s for _, v in fit_rows])
    A = np.vstack([cx, np.ones_like(cx)]).T
    (m, b), _, _, _ = np.linalg.lstsq(A, cy, rcond=None)
    P(f" {name} LINE: cols x{cx[0]:.0f}..{cx[-1]:.0f}  px-fit row = {m:.4f}*x + {b:.1f}  (n={len(cx)})")
    cal, anchors = calib(img)
    if cal:
        P(f" {name} calib anchors: " + " ".join(f"({fx:.0f},{fy:.0f})->({dx},{dy})" for fx, fy, dx, dy in anchors))
        x0d, y0d = cal["x"]*cx[0]+cal["xb"], cal["y"]*cy[0]+cal["yb"]
        x1d, y1d = cal["x"]*cx[-1]+cal["xb"], cal["y"]*cy[-1]+cal["yb"]
        slope_d = (y1d-y0d)/(x1d-x0d) if x1d != x0d else float("inf")
        xint = (0-y0d-b*0)/1  # placeholder replaced below
        # data x-intercept: y_data = 0 on the fitted px line
        # row(y_px) = m*x_px+b ; x_px where y_data=0 => y_px = (0-cal['yb'])/cal['y']
        ypx0 = (0-cal["yb"])/cal["y"]
        xpx0 = (ypx0-b)/m
        xint_d = cal["x"]*xpx0+cal["xb"]
        P(f" {name} LINE data: ({x0d:.2f},{y0d:.2f}) -> ({x1d:.2f},{y1d:.2f})  slope={slope_d:.3f}  x-intercept={xint_d:.2f}")

# ---- F3: +ve annotation centroid ----
P("\n## F3 +ve ink centroid (window x410..540 y280..350, interior above blue squares)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 410, 540, 280, 350)
    ink, red, blue, pink = masks(z)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    blobs = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < 12: continue
        blobs.append((len(ys), 410+xs.mean()/s, 280+ys.mean()/s,
                      410+xs.min()/s, 410+xs.max()/s, 280+ys.min()/s, 280+ys.max()/s))
    for bb in sorted(blobs, key=lambda t: -t[0])[:5]:
        P(f" {name} ink-blob n={bb[0]} c=({bb[1]:.0f},{bb[2]:.0f}) bbox x{bb[3]:.0f}..{bb[4]:.0f} y{bb[5]:.0f}..{bb[6]:.0f}")
    tot = sum(b[0] for b in blobs)
    if tot:
        cx = sum(b[0]*b[1] for b in blobs)/tot; cy = sum(b[0]*b[2] for b in blobs)/tot
        P(f" {name} window ink centroid=({cx:.0f},{cy:.0f}) total_ink={tot}")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
