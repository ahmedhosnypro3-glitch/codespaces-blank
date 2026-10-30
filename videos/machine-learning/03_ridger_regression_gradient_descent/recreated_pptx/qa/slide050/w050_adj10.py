#!/usr/bin/env python3
"""PIL adjudication of slide 050 judge_attempt_10 (render_12) vs original frame.
Measures the 4 MAJORs + key MINORs. Frame coords 960x540; render 2001px, s=2.0833."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide050/w050_adj10_raw.txt"

o = np.asarray(Image.open(f"{NS}/unique_slides/slide_050.jpg").convert("RGB")).astype(int)
r_im = Image.open(f"{NS}/recreated_pptx/qa/slide050/render_12.png").convert("RGB")
s = r_im.size[0] / 960.0
r = np.asarray(r_im).astype(int)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def zone(img, x0, x1, y0, y1):
    return img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)] if s > 1.01 else img[y0:y1, x0:x1]

def lum(z): return 0.299*z[:,:,0]+0.587*z[:,:,1]+0.114*z[:,:,2]
def masks(z):
    red = (z[:,:,0] > 140) & (z[:,:,0]-z[:,:,1] > 60) & (z[:,:,0]-z[:,:,2] > 60)
    blue = (z[:,:,2] > 120) & (z[:,:,2]-z[:,:,0] > 40) & (z[:,:,2]-z[:,:,1] > 20)
    green = (z[:,:,1] > 110) & (z[:,:,1]-z[:,:,0] > 25) & (z[:,:,1]-z[:,:,2] > 25)
    mag = (z[:,:,0] > 130) & (z[:,:,2] > 110) & (z[:,:,1] < 0.6*(z[:,:,0]+z[:,:,2])/2)
    ink = lum(z) < 200
    return ink, red, blue, green, mag

P("== 050 adj attempt-10, render scale", round(s,4))

# ---- F1: eta zone (orig refuted by w7; verify render matches orig = no eta in BOTH) ----
P("\n## F1 eta zone x531..642 y58..84 (between REPEAT-phrase end and Z labels)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 531, 642, 58, 84)
    ink, red, blue, green, mag = masks(z)
    P(f" {name}: ink={int(ink.sum())} red={int(red.sum())} blue={int(blue.sum())} green={int(green.sum())}")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 426, 532, 58, 84)
    _, red, *_ = masks(z)
    cols = np.where(red.any(axis=0))[0]
    if len(cols):
        P(f" {name} red REPEAT-phrase x-extent: {426+cols[0]/s:.0f}..{426+cols[-1]/s:.0f}")

# ---- F2: Z-grid values (z1,z2,z3) — read digits as ascii ----
P("\n## F2 Z-grid zone x630..712 y64..132 ascii (lum<200)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 630, 712, 64, 132)
    ink = lum(z) < 200
    P(f" {name}:")
    step = max(1, int(round(s)))
    for yy in range(0, ink.shape[0], step):
        row = "".join("#" if ink[yy, xx:xx+step].sum() > 0 else "." for xx in range(0, ink.shape[1], step))
        P(f"   {row}")

# ---- F3/F4: red marker census in chart window x312..830 y165..490 ----
P("\n## F3/F4 red saturated blobs (chart window), area>=30px")
def blobs(img, label):
    z = zone(img, 300, 835, 160, 495)
    _, red, blue, green, mag = masks(z)
    from scipy import ndimage
    for mname, m in (("RED", red), ("MAGENTA", mag), ("BLUE", blue)):
        lab, n = ndimage.label(m)
        for i in range(1, n+1):
            ys, xs = np.where(lab == i)
            if len(ys) < 30: continue
            cx, cy = 300 + xs.mean()/s, 160 + ys.mean()/s
            # data coords per w050_adjud5 mapping: x0=359,y0=432 origin; 52.8px/unit x, 31.8px/unit y
            dx, dy = (cx-359)/52.8, (432-cy)/31.8
            P(f" {label} {mname}: frame({cx:.0f},{cy:.0f}) n={len(ys)} data≈({dx:.2f},{dy:.2f}) bbox x{300+xs.min()/s:.0f}..{300+xs.max()/s:.0f} y{160+ys.min()/s:.0f}..{160+ys.max()/s:.0f}")
for name, img in (("ORIG", o), ("RENDER", r)):
    try:
        blobs(img, name)
    except Exception as e:
        P(" blob census error:", e)

# ---- F5: (7,6) marker orientation ascii ----
P("\n## F5 (7,6) marker ascii (frame x722..742 y236..254)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 722, 742, 236, 254)
    _, red, *_ = masks(z)
    P(f" {name}:")
    step = max(1, int(round(s)))
    for yy in range(0, red.shape[0], step):
        P("   " + "".join("#" if red[yy, xx:xx+step].sum() > 0 else "." for xx in range(0, red.shape[1], step)))

# ---- F6: W-panel fill sample ----
P("\n## F6 W-panel fill samples (frame (770,200),(800,240),(780,300))")
for name, img in (("ORIG", o), ("RENDER", r)):
    pts = [(770,200),(800,240),(780,300)]
    P(f" {name}: {[tuple(int(v) for v in img[int(y*s), int(x*s)]) for x,y in pts]}")

# ---- F8: line end arrowhead (red line right end near (7,6)) ----
P("\n## F8 red-line right-end ink extent (frame x690..740 y230..260)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 690, 740, 230, 260)
    _, red, *_ = masks(z)
    cols = np.where(red.any(axis=0))[0]
    P(f" {name}: red cols n={len(cols)} extent {(690+cols[0]/s):.0f}..{(690+cols[-1]/s):.0f}" if len(cols) else f" {name}: none")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
