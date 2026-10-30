#!/usr/bin/env python3
"""Fixed adjudication of slide 050 judge_attempt_10 (render_12) vs original.
Masks recalibrated to measured chart colors; F6 scale bug fixed; pink class added."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide050/w050_adj10b_raw.txt"

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
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)                       # dark/sat red line, markers
    pink = (R > 195) & (R-G > 25) & (R-B > 25) & (G > 130) & (B > 130)  # pale pink fills
    blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
    mag = (R > 150) & (B > 150) & (G < R-30) & (G < B-30)
    green = (G > 110) & (G-R > 25) & (G-B > 25)
    ink = lum(z) < 200
    return ink, red, blue, green, mag, pink

P("== 050 adj attempt-10 fixed, render scale", round(s, 4))

# ---- F1: eta zone ----
P("\n## F1 eta zone x531..642 y58..84")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 531, 642, 58, 84)
    ink, red, blue, green, mag, pink = masks(z)
    P(f" {name}: ink={int(ink.sum())} red={int(red.sum())} blue={int(blue.sum())}")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 426, 532, 58, 84)
    ink, red, blue, green, mag, pink = masks(z)
    cols = np.where(red.any(axis=0))[0]
    if len(cols):
        P(f" {name} red REPEAT-phrase x-extent: {426+cols[0]/s:.0f}..{426+cols[-1]/s:.0f}")

# ---- F2: Z-grid values ascii ----
P("\n## F2 Z-grid zone x630..712 y64..132 ascii (lum<200)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 630, 712, 64, 132)
    ink = lum(z) < 200
    P(f" {name}:")
    step = max(1, int(round(s)))
    for yy in range(0, ink.shape[0], step):
        row = "".join("#" if ink[yy, xx:xx+step].sum() > 0 else "." for xx in range(0, ink.shape[1], step))
        P(f"   {row}")

# ---- F3/F4: red blobs in chart window ----
P("\n## F3/F4 red-ish blobs (chart window x300..835 y160..495), area>=40px")
def blobs(img, label):
    z = zone(img, 300, 835, 160, 495)
    _, red, blue, green, mag, pink = masks(z)
    from scipy import ndimage
    for mname, m in (("RED", red), ("PINK", pink), ("MAGENTA", mag), ("NAVY", blue)):
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        for i in range(1, n+1):
            ys, xs = np.where(lab == i)
            if len(ys) < 40: continue
            cx, cy = 300 + xs.mean()/s, 160 + ys.mean()/s
            P(f" {label} {mname}: frame({cx:.0f},{cy:.0f}) n={len(ys)} bbox x{300+xs.min()/s:.0f}..{300+xs.max()/s:.0f} y{160+ys.min()/s:.0f}..{160+ys.max()/s:.0f}")
for name, img in (("ORIG", o), ("RENDER", r)):
    blobs(img, name)

# ---- F3b: (3,2) neighborhood ascii (red-ish) — locate via axis ticks, not assumed mapping
P("\n## F3b red-ish ascii around frame x500..540 y350..385 (claimed (3,2) spot)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 500, 540, 350, 385)
    ink, red, blue, green, mag, pink = masks(z)
    P(f" {name}:")
    step = max(1, int(round(s)))
    for yy in range(0, red.shape[0], step):
        P("   " + "".join("#" if red[yy, xx:xx+step].sum() > 0 else "." for xx in range(0, red.shape[1], step)))

# ---- F4b: stray-ink neighborhood ascii (red-ish) around frame x375..405 y300..335
P("\n## F4b red-ish ascii around frame x375..405 y300..335 (claimed stray (0.6,4.5))")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 375, 405, 300, 335)
    ink, red, blue, green, mag, pink = masks(z)
    P(f" {name}:")
    step = max(1, int(round(s)))
    for yy in range(0, red.shape[0], step):
        P("   " + "".join("#" if red[yy, xx:xx+step].sum() > 0 else "." for xx in range(0, red.shape[1], step)))

# ---- F5: (7,6) marker ascii (wider window, red+pink) ----
P("\n## F5 (7,6) marker ascii (frame x712..752 y228..262)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 712, 752, 228, 262)
    _, red, _, _, _, pink = masks(z)
    m = red | pink
    P(f" {name} (red={int(red.sum())} pink={int(pink.sum())}):")
    step = max(1, int(round(s)))
    for yy in range(0, m.shape[0], step):
        P("   " + "".join("#" if m[yy, xx:xx+step].sum() > 0 else "." for xx in range(0, m.shape[1], step)))

# ---- F6: W-panel fill samples (scale-aware) ----
P("\n## F6 W-panel fill samples (frame (770,200),(800,240),(780,300))")
for name, img in (("ORIG", o), ("RENDER", r)):
    pts = [(770, 200), (800, 240), (780, 300)]
    P(f" {name}: {[tuple(int(v) for v in zone(img, x, x+1, y, y+1)[0,0]) for x, y in pts]}")

# ---- F8: line end arrowhead ----
P("\n## F8 red-line right-end ink extent (frame x690..745 y225..265)")
for name, img in (("ORIG", o), ("RENDER", r)):
    z = zone(img, 690, 745, 225, 265)
    _, red, _, _, _, pink = masks(z)
    m = red | pink
    cols = np.where(m.any(axis=0))[0]
    rows = np.where(m.any(axis=1))[0]
    P(f" {name}: n={int(m.sum())} cols {(690+cols[0]/s):.0f}..{(690+cols[-1]/s):.0f} rows {(225+rows[0]/s):.0f}..{(225+rows[-1]/s):.0f}" if len(cols) else f" {name}: none")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
