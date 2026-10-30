#!/usr/bin/env python3
"""adj11d: plot-area-calibrated line + '+ve' label measurement, both images."""
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide050/w050_adj11d_raw.txt"

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
    blue = (B > 90) & (B-R > 25) & (B-G > 10) & (G >= R)
    pink = (R > 195) & (R-G > 25) & (R-B > 25) & (G > 130) & (B > 130)
    lum = 0.299*R+0.587*G+0.114*B
    return lum < 200, red, blue, pink

for name in IMGS:
    # --- plot-area landmarks: dark long lines within chart window ---
    z, s = zone(name, 300, 835, 160, 500)
    ink, red, blue, pink = masks(z)
    colsum = ink.sum(axis=0); rowsum = ink.sum(axis=1)
    H, W = ink.shape
    vcands = [300+i/s for i in range(W) if colsum[i] > 0.55*H*0.7]
    hcands = [160+i/s for i in range(H) if rowsum[i] > 0.55*W*0.7]
    # cluster candidates
    def cl(v):
        out = []
        for t in v:
            if out and t-out[-1][-1] < 4/s: out[-1].append(t)
            else: out.append([t])
        return [sum(g)/len(g) for g in out]
    vlines, hlines = cl(vcands), cl(hcands)
    P(f"\n### {name}: long dark verticals x={[round(v,1) for v in vlines]}")
    P(f" {name}: long dark horizontals y={[round(h,1) for h in hlines]}")
    # plot area: assume innermost 4: y-axis=2nd vertical? Use known structure: axis left, right edge, top, bottom
    if len(vlines) >= 2 and len(hlines) >= 2:
        yax_x, redge_x = vlines[0], vlines[-1]
        top_y, bot_y = hlines[0], hlines[-1]
        def D(fx, fy): return ((fx-yax_x)/((redge_x-yax_x)/8.0), (bot_y-fy)/((bot_y-top_y)/7.0))
        P(f" {name} plot: yaxis x{yax_x:.1f} right x{redge_x:.1f} top y{top_y:.1f} bottom y{bot_y:.1f} -> xunit={(redge_x-yax_x)/8:.2f}px yunit={(bot_y-top_y)/7:.2f}px")

        # --- decision line: red, no long runs, diagonal clusters, trimmed fit ---
        def drop_long(m, horizontal):
            out = m.copy(); Hh, Ww = m.shape
            rng = range(Hh) if horizontal else range(Ww)
            for rr in rng:
                seg = m[rr] if horizontal else m[:, rr]
                idx = np.where(seg)[0]
                if len(idx) == 0: continue
                for sp in np.split(idx, np.where(np.diff(idx) > 2)[0]+1):
                    if len(sp) > 18:
                        if horizontal: out[rr, sp] = False
                        else: out[sp, rr] = False
            return out
        redl = drop_long(drop_long(red, True), False)
        labl, nl = ndimage.label(redl, structure=np.ones((3, 3)))
        pts = []
        for i in range(1, nl+1):
            ysl, xsl = np.where(labl == i)
            if len(ysl) < 25: continue
            if (xsl.max()-xsl.min()) > 16 and (ysl.max()-ysl.min()) > 16:
                pts.append((300+xsl/s, 160+ysl/s))
        if pts:
            px = np.concatenate([p[0] for p in pts]); py = np.concatenate([p[1] for p in pts])
            for _ in range(5):
                A = np.vstack([px, np.ones_like(px)]).T
                (mf, bf), *_ = np.linalg.lstsq(A, py, rcond=None)
                keep = np.abs(py-(mf*px+bf)) < 7/s
                px, py = px[keep], py[keep]
            (mf, bf), *_ = np.linalg.lstsq(np.vstack([px, np.ones_like(px)]).T, py, rcond=None)
            i_lo, i_hi = np.argmin(px), np.argmax(px)
            e0, e1 = D(px[i_lo], py[i_lo]), D(px[i_hi], py[i_hi])
            sl = (e1[1]-e0[1])/(e1[0]-e0[0])
            xi = e0[0]-e0[1]/sl
            P(f" {name} LINE: npts={len(px)} frame({px.min():.0f},{py[np.argmin(px)]:.0f})->({px.max():.0f},{py[np.argmax(px)]:.0f})")
            P(f" {name} LINE data: ({e0[0]:.2f},{e0[1]:.2f})->({e1[0]:.2f},{e1[1]:.2f}) slope={sl:.3f} x@y0={xi:.2f}")
        # marker spot-checks (marker centroids in data)
        for mname, m in (("blue", blue), ("pink", pink)):
            labm, nm = ndimage.label(m, structure=np.ones((3, 3)))
            cents = []
            for i in range(1, nm+1):
                ysm, xsm = np.where(labm == i)
                if not (30 <= len(ysm) <= 900): continue
                if xsm.max()-xsm.min() > 60 or ysm.max()-ysm.min() > 60: continue
                cents.append(D(300+xsm.mean()/s, 160+ysm.mean()/s))
            cents.sort()
            P(f" {name} {mname} markers (data): " + " ".join(f"({a:.2f},{b:.2f})" for a, b in cents))
        # --- '+ve' black text inside plot interior ---
        z4, s4 = zone(name, yax_x+6, redge_x-6, top_y+6, bot_y-6)
        ink4, red4, blue4, pink4 = masks(z4)
        black = ink4 & ~red4 & ~blue4 & ~pink4
        lab4, n4 = ndimage.label(black, structure=np.ones((3, 3)))
        found = False
        for i in range(1, n4+1):
            ys4, xs4 = np.where(lab4 == i)
            if len(ys4) < 15: continue
            fx, fy = yax_x+6+xs4.mean()/s4, top_y+6+ys4.mean()/s4
            d = D(fx, fy)
            P(f" {name} BLACK-blob n={len(ys4)} frame({fx:.0f},{fy:.0f}) data=({d[0]:.2f},{d[1]:.2f}) bbox x{yax_x+6+xs4.min()/s4:.0f}..{yax_x+6+xs4.max()/s4:.0f} y{top_y+6+ys4.min()/s4:.0f}..{top_y+6+ys4.max()/s4:.0f}")
            found = True
        if not found: P(f" {name}: no black text blobs inside plot interior")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
