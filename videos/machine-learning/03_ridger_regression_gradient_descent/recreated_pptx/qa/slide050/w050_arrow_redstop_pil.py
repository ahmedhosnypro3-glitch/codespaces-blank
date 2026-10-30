#!/usr/bin/env python3
"""Fine PIL probes: (1) +ve arrow zone both images; (2) redstop serif/italic check;
(3) pinkbox hairline border with corrected pale-pink mask. Coords in ORIG space."""
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{NS}/recreated_pptx/qa/slide050"
OUT = f"{QA}/w050_arrow_redstop_pil_raw.txt"

IMGS = {}
for name, path in (("ORIG", f"{NS}/unique_slides/slide_050.jpg"),
                   ("RENDER", f"{QA}/render_13.png")):
    im = Image.open(path).convert("RGB")
    IMGS[name] = (np.asarray(im).astype(int), im.size[0] / 960.0)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def zone(name, x0, x1, y0, y1):
    img, s = IMGS[name]
    return img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)], s

def redmask(z):
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    return (R > 110) & (R-G > 50) & (R-B > 40)

P("== arrow/redstop/pinkbox PIL probes")

P("\n## 1. +ve arrow zone x365..470 y282..342 — RED mask, ORIG 1px/char / RENDER 2renderpx/char")
for name, step in (("ORIG", 1), ("RENDER", 2)):
    z, s = zone(name, 365, 470, 282, 342)
    red = redmask(z)
    P(f" {name} (char={step/s:.2f} orig px; x365 y282):")
    for yy in range(0, red.shape[0], step):
        P(f"{282+yy/s:3.0f} " + "".join("#" if red[yy, xx:xx+step].any() else "." for xx in range(0, red.shape[1], step)))

P("\n## 2. REDSTOP x55..245 y265..405: ink inventory + text band ASCII")
for name in IMGS:
    z, s = zone(name, 55, 245, 265, 405)
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = redmask(z)
    lum = 0.299*R+0.587*G+0.114*B
    dark = lum < 120
    P(f" {name}: red_px={int(red.sum())} dark_px={int(dark.sum())} zone={z.shape[1]}x{z.shape[0]}")
    lab, n = ndimage.label(red)
    sizes = sorted([int((lab==i).sum()) for i in range(1,n+1)], reverse=True)[:5]
    P(f" {name}: top red blobs px={sizes}")
    # row profile of dark ink (text lines)
    rows = dark.sum(axis=1)
    bands, st = [], None
    for i, v in enumerate(rows > 0):
        if v and st is None: st = i
        if not v and st is not None:
            if i - st > 3: bands.append((265+st/s, 265+i/s))
            st = None
    if st is not None: bands.append((265+st/s, 265+len(rows)/s))
    P(f" {name}: dark-ink row bands (orig y): {[(round(a,1), round(b,1)) for a,b in bands]}")

P("\n## 2b. redstop text ASCII per band — ink=lum<140 OR red, per band from 2")
BANDS = {"ORIG": None, "RENDER": None}
# derive bands from ORIG, reuse for both (same layout intended)
z, s = zone("ORIG", 55, 245, 265, 405)
lum = 0.299*z[:,:,0]+0.587*z[:,:,1]+0.114*z[:,:,2]
dark = lum < 140
rows = dark.sum(axis=1)
bands, st = [], None
for i, v in enumerate(rows > 1):
    if v and st is None: st = i
    if not v and st is not None:
        if i - st > 4: bands.append((int(265+st/s), int(265+i/s)))
        st = None
P(f" ORIG bands used: {bands}")
for (by0, by1) in bands:
    for name, step in (("ORIG", 1), ("RENDER", 2)):
        z2, s2 = zone(name, 60, 240, by0-1, by1+1)
        R, G, B = z2[:,:,0], z2[:,:,1], z2[:,:,2]
        ink = redmask(z2) | (0.299*R+0.587*G+0.114*B < 140)
        cols = np.where(ink.any(axis=0))[0]
        if not len(cols):
            P(f"  band y{by0}..{by1} {name}: EMPTY"); continue
        P(f"  band y{by0}..{by1} {name} x60..240 (char={step/s2:.2f}px):")
        for yy in range(0, ink.shape[0], step):
            P("    " + "".join("#" if ink[yy, xx:xx+step].any() else "." for xx in range(0, ink.shape[1], step)))

P("\n## 3. PINKBOX border probe v2 — pale-pink fill mask x720..850 y40..190")
for name in IMGS:
    z, s = zone(name, 720, 850, 40, 190)
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    pale = (R > 205) & (R-G > 12) & (R-B > 8) & (G > 120) & (B > 120)
    ys, xs = np.where(pale)
    if len(ys) < 50:
        P(f" {name}: pale-pink px={len(ys)} — no box found"); continue
    bx0, bx1, by0, by1 = 720+xs.min()/s, 720+xs.max()/s, 40+ys.min()/s, 40+ys.max()/s
    P(f" {name}: pale bbox x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f} px={len(ys)}")
    med = np.median(z[pale].reshape(-1,3), axis=0).astype(int)
    P(f" {name}: fill median #{med[0]:02X}{med[1]:02X}{med[2]:02X}")
    lum0 = 0.299*z[:,:,0]+0.587*z[:,:,1]+0.114*z[:,:,2]
    ink = lum0 < 170
    iy0, iy1, ix0, ix1 = int(by0*s), int(by1*s), int(bx0*s), int(bx1*s)
    w_in, h_in = ix1-ix0, iy1-iy0
    for side, band in (("top", ink[max(0,iy0-3):iy0+3, ix0:ix1]),
                       ("bottom", ink[iy1-2:iy1+4, ix0:ix1]),
                       ("left", ink[iy0:iy1, max(0,ix0-3):ix0+3]),
                       ("right", ink[iy0:iy1, ix1-2:ix1+4])):
        frac = band.mean()
        P(f" {name}: {side} band ink fraction={frac:.3f} ({int(band.sum())}px of {band.size})")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
P(f"\n[saved {OUT}]")
