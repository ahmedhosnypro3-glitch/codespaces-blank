#!/usr/bin/env python3
"""PIL adjudication of crop_13_chart judge findings (F1-F4, F6) + pinkbox border note.
Scales: ORIG 960x540 = 1.0, RENDER 2001x1125 = 2.0844. All coords printed in ORIG space.
Data->px: x_px = 363 + 52.6*d, y_px = 428.5 - 30.71*d (tick-calibrated, banked adj11b)."""
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{NS}/recreated_pptx/qa/slide050"
OUT = f"{QA}/w050_chartfix_pil_raw.txt"

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

def masks(z):
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    pink = (R > 195) & (R-G > 25) & (R-B > 25) & (G > 130) & (B > 130)
    lum = 0.299*R+0.587*G+0.114*B
    return lum < 200, red, pink

def red_blobs(name, x0, x1, y0, y1, minpx=8):
    z, s = zone(name, x0, x1, y0, y1)
    _, red, _ = masks(z)
    lab, n = ndimage.label(red)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) < minpx: continue
        out.append((x0+xs.min()/s, x1 if False else x0+xs.max()/s,
                    y0+ys.min()/s, y0+ys.max()/s, len(ys)))
    return out

P("== chart-fix PIL, scales:", {k: round(v,4) for k,v in [(n,IMGS[n][1]) for n in IMGS]})

P("\n## F1/F2 red blobs in window x350..500 y260..330 (orig coords: x0..x1 y0..y1 px) [spurious-triangle + doubled-stroke zone, data x -0.2..2.6 y 3.2..5.5]")
for name in IMGS:
    P(f" {name}:")
    for (bx0,bx1,by0,by1,npx) in red_blobs(name, 350, 500, 260, 330):
        P(f"   blob x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f} px={npx} data_x=({(bx0-363)/52.6:.2f}..{(bx1-363)/52.6:.2f}) data_y=({(428.5-by1)/30.71:.2f}..{(428.5-by0)/30.71:.2f})")

P("\n## F2b vertical red-run structure along the line, columns data x=0.5,0.7,0.9 (orig x 389.3/399.8/410.3), window y270..320")
for name in IMGS:
    img, s = IMGS[name]
    z, _ = zone(name, 380, 415, 270, 320)
    _, red, _ = masks(z)
    P(f" {name}:")
    for dx in (0.5, 0.7, 0.9):
        cx = int((363+52.6*dx-380)*s)
        col = red[:, max(0,cx-1):cx+2].any(axis=1)
        runs, st = [], None
        for i, v in enumerate(col):
            if v and st is None: st = i
            if not v and st is not None: runs.append((st, i-1)); st = None
        if st is not None: runs.append((st, len(col)-1))
        P(f"   x={dx}: runs(270+y) = {[(270+a, 270+b) for a,b in runs]}")

P("\n## F3 +ve label + arrow ascii, x355..560 y235..345 (red mask, ORIG step2 / RENDER step4)")
for name, step in (("ORIG", 2), ("RENDER", 4)):
    z, s = zone(name, 355, 560, 235, 345)
    _, red, _ = masks(z)
    P(f" {name} (each char={step/s:.1f} orig px; left=355 top=235):")
    for yy in range(0, red.shape[0], step):
        P("   " + "".join("#" if red[yy, xx:xx+step].any() else "." for xx in range(0, red.shape[1], step)))

P("\n## F4 diamond fill colors, centers (5,4)(6,5)(6,6) -> orig px (626.0,305.7)(678.6,275.0)(678.6,244.2); median RGB 7x7")
for cx, cy in ((626.0, 305.7), (678.6, 275.0), (678.6, 244.2)):
    row = []
    for name in IMGS:
        img, s = IMGS[name]
        px, py = int(cx*s), int(cy*s)
        patch = img[py-3:py+4, px-3:px+4].reshape(-1, 3)
        med = np.median(patch, axis=0).astype(int)
        row.append(f"{name}={tuple(med)} #{med[0]:02X}{med[1]:02X}{med[2]:02X}")
    P(f" d({cx:.0f},{cy:.0f}): " + "  ".join(row))

P("\n## F6 line-end arrowhead probe x640..740 y400..460 red px counts + max blob px")
for name in IMGS:
    z, s = zone(name, 640, 740, 400, 460)
    _, red, _ = masks(z)
    lab, n = ndimage.label(red)
    sizes = sorted([int((lab==i).sum()) for i in range(1,n+1)], reverse=True)[:3]
    P(f" {name}: total={int(red.sum())} top-blobs={sizes}")

P("\n## line thickness probe: red runs down column x=520 (data 2.99), y250..400")
for name in IMGS:
    img, s = IMGS[name]
    cx = int(520*s)
    col = (img[250:400, cx, :] @ [1,0,0] if False else None)
    z = img[250:400, cx-1:cx+2, :]
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = ((R > 110) & (R-G > 50) & (R-B > 40)).any(axis=1)
    P(f" {name}: red rows={int(red.sum())} (of 150)")

P("\n## PINKBOX border probe: pink bbox in x700..900 y30..200, then perimeter-band ink")
for name in IMGS:
    z, s = zone(name, 700, 900, 30, 200)
    _, _, pink = masks(z)
    ys, xs = np.where(pink)
    if not len(ys):
        P(f" {name}: NO pink"); continue
    bx0, bx1, by0, by1 = 700+xs.min()/s, 700+xs.max()/s, 30+ys.min()/s, 30+ys.max()/s
    P(f" {name}: pink bbox x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f} px={int(pink.sum())}")
    lum0 = 0.299*z[:,:,0]+0.587*z[:,:,1]+0.114*z[:,:,2]
    dark = lum0 < 150
    iy0, iy1, ix0, ix1 = int(by0*s), int(by1*s), int(bx0*s), int(bx1*s)
    top = dark[max(0,iy0-2):iy0+2, ix0:ix1].sum()
    bot = dark[iy1-1:iy1+3, ix0:ix1].sum()
    lef = dark[iy0:iy1, max(0,ix0-2):ix0+2].sum()
    rig = dark[iy0:iy1, ix1-1:ix1+3].sum()
    P(f" {name}: dark px on top/bottom/left/right 4px bands = {int(top)}/{int(bot)}/{int(lef)}/{int(rig)} (bands ~({ix1-ix0})x4 / 4x({iy1-iy0}))")
    if name == "ORIG" and (top or bot or lef or rig):
        samp = z[max(0,iy0-2):iy0+3, ix0:ix0+40][dark[max(0,iy0-2):iy0+3, ix0:ix0+40]]
        if len(samp): P(f" ORIG top-band dark sample RGB: {tuple(np.median(samp,axis=0).astype(int))}")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
P(f"\n[saved {OUT}]")
