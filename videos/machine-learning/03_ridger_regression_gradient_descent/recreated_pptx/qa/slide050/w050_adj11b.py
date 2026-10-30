#!/usr/bin/env python3
"""adj11b: corrected per-image-scale adjudication of slide 050 judge_attempt_11.
Original 960x540 (scale 1.0); render_13 2001x1125 (scale 2.0844). F1/F2/F3."""
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide050/w050_adj11b_raw.txt"

IMGS = {}
for name, path in (("ORIG", f"{NS}/unique_slides/slide_050.jpg"),
                   ("RENDER", f"{NS}/recreated_pptx/qa/slide050/render_13.png")):
    im = Image.open(path).convert("RGB")
    IMGS[name] = (np.asarray(im).astype(int), im.size[0] / 960.0)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def zone(name, x0, x1, y0, y1):
    img, s = IMGS[name]
    return img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)], s

def masks(z):
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    pink = (R > 195) & (R-G > 25) & (R-B > 25) & (G > 130) & (B > 130)
    blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
    lum = 0.299*R+0.587*G+0.114*B
    return lum < 200, red, blue, pink

P("== 050 adj11b corrected, scales:", {k: round(v, 4) for k, v in [(n, IMGS[n][1]) for n in IMGS]})

# ---- F1: eta zone ----
P("\n## F1 eta zone x531..642 y58..84 (ink counts; would hold 'eta = 1' if present)")
for name in IMGS:
    z, s = zone(name, 531, 642, 58, 84)
    ink, red, blue, pink = masks(z)
    P(f" {name}: ink={int(ink.sum())} red={int(red.sum())} zone_px={z.shape[1]}x{z.shape[0]}")
P("\n## F1b red header-phrase extent (zone x420..535 y58..84)")
for name in IMGS:
    z, s = zone(name, 420, 535, 58, 84)
    _, red, _, _ = masks(z)
    cols = np.where(red.any(axis=0))[0]
    P(f" {name} red phrase x-extent: {420+cols[0]/s:.0f}..{420+cols[-1]/s:.0f}" if len(cols) else f" {name}: no red")
P("\n## F1c header ascii x495..660 y58..86 (ink, step2, char=2renderpx)")
for name in IMGS:
    z, s = zone(name, 495, 660, 58, 86)
    ink, _, _, _ = masks(z)
    P(f" {name} (zone {z.shape[1]}px wide):")
    for yy in range(0, ink.shape[0], 2):
        P("   " + "".join("#" if ink[yy, xx:xx+2].sum() > 0 else "." for xx in range(0, ink.shape[1], 2)))

# ---- F2: red components + line fit in chart window ----
CW = (300, 835, 160, 495)
P("\n## F2 red components (chart x300..835 y160..495)")
def comps_of(name):
    z, s = zone(name, *CW)
    _, red, _, _ = masks(z)
    lab, n = ndimage.label(red, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < 30: continue
        out.append(dict(n=len(ys), x0=CW[0]+xs.min()/s, x1=CW[0]+xs.max()/s,
                        y0=CW[2]+ys.min()/s, y1=CW[2]+ys.max()/s, mask=(lab == i)))
    return out

def line_fit(name):
    z, s = zone(name, *CW)
    _, red, _, _ = masks(z)
    H, W = red.shape
    pts_x, pts_y = [], []
    for cc in range(W):
        rows = np.where(red[:, cc])[0]
        if len(rows) == 0: continue
        runs = np.split(rows, np.where(np.diff(rows) > 2)[0]+1)
        thin = [r for r in runs if len(r) <= 8]
        if not thin: continue
        r = min(thin, key=lambda t: abs(len(t)-3))
        pts_x.append(CW[0]+cc/s); pts_y.append(CW[2]+np.mean(r)/s)
    px = np.array(pts_x); py = np.array(pts_y)
    for _ in range(4):
        if len(px) < 10: break
        A = np.vstack([px, np.ones_like(px)]).T
        (m, b), *_ = np.linalg.lstsq(A, py, rcond=None)
        keep = np.abs(py - (m*px+b)) < 10/s*2
        px, py = px[keep], py[keep]
    A = np.vstack([px, np.ones_like(px)]).T
    (m, b), *_ = np.linalg.lstsq(A, py, rcond=None)
    return m, b, px, py

def calib(name):
    z, s = zone(name, *CW)
    _, red, blue, pink = masks(z)
    anchors = []
    for cname, m, coords in (("blue", blue, [(0,2),(1,1),(2,1)]),
                             ("pink", pink, [(5,4),(6,5),(6,6)]),
                             ("redtri", red, [(0,0),(7,6)])):
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        cents = []
        for i in range(1, n+1):
            ys, xs = np.where(lab == i)
            if not (30 <= len(ys) <= 900): continue
            if xs.max()-xs.min() > 60 or ys.max()-ys.min() > 60: continue
            cents.append((CW[0]+xs.mean()/s, CW[2]+ys.mean()/s))
        cents.sort()
        for (fx, fy), (dx, dy) in zip(cents, coords):
            anchors.append((fx, fy, dx, dy))
    ax = np.array([a[0] for a in anchors]); ay = np.array([a[1] for a in anchors])
    dx = np.array([a[2] for a in anchors]); dy = np.array([a[3] for a in anchors])
    (a1, a0), *_ = np.linalg.lstsq(np.vstack([ax, np.ones_like(ax)]).T, dx, rcond=None)
    (b1, b0), *_ = np.linalg.lstsq(np.vstack([ay, np.ones_like(ay)]).T, dy, rcond=None)
    return dict(x=a1, xb=a0, y=b1, yb=b0), anchors

for name in IMGS:
    for c in sorted(comps_of(name), key=lambda c: -c["n"])[:8]:
        P(f" {name} comp n={c['n']} bbox x{c['x0']:.0f}..{c['x1']:.0f} y{c['y0']:.0f}..{c['y1']:.0f}")
    m, b, px, py = line_fit(name)
    P(f" {name} LINE thin-run fit: x-span {px.min():.0f}..{px.max():.0f} row = {m:.4f}*x + {b:.1f} (npts={len(px)})")
    cal, anchors = calib(name)
    P(f" {name} calib: " + " ".join(f"({fx:.0f},{fy:.0f})->({dx},{dy})" for fx, fy, dx, dy in anchors))
    x0d, y0d = cal["x"]*px.min()+cal["xb"], cal["y"]*py[np.argmin(px)]+cal["yb"]
    x1d, y1d = cal["x"]*px.max()+cal["xb"], cal["y"]*py[np.argmax(px)]+cal["yb"]
    ypx0 = (0-cal["yb"])/cal["y"]; xpx0 = (ypx0-b)/m
    P(f" {name} LINE data: ({x0d:.2f},{y0d:.2f}) -> ({x1d:.2f},{y1d:.2f}) slope_data={(y1d-y0d)/(x1d-x0d):.3f} x-intercept={cal['x']*xpx0+cal['xb']:.2f}")

# ---- F3: +ve centroid ----
P("\n## F3 +ve annotation, ink centroid in x410..540 y280..350")
for name in IMGS:
    z, s = zone(name, 410, 540, 280, 350)
    ink, red, blue, pink = masks(z)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    blobs = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < 12: continue
        blobs.append((len(ys), 410+xs.mean()/s, 280+ys.mean()/s))
    tot = sum(b[0] for b in blobs)
    if tot:
        cx = sum(b[0]*b[1] for b in blobs)/tot; cy = sum(b[0]*b[2] for b in blobs)/tot
        P(f" {name} centroid=({cx:.0f},{cy:.0f}) total_ink={tot} blobs={sorted([b[0] for b in blobs], reverse=True)[:6]}")
P("\n## F3b ascii x400..540 y285..345 (ink, step2)")
for name in IMGS:
    z, s = zone(name, 400, 540, 285, 345)
    ink, _, _, _ = masks(z)
    P(f" {name}:")
    for yy in range(0, ink.shape[0], 2):
        P("   " + "".join("#" if ink[yy, xx:xx+2].sum() > 0 else "." for xx in range(0, ink.shape[1], 2)))

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
