#!/usr/bin/env python3
"""adj11c: tick-label-calibrated measurements for slide 050 att11 F2 (line) + F3 (+ve)."""
from PIL import Image
import numpy as np
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = f"{NS}/recreated_pptx/qa/slide050/w050_adj11c_raw.txt"

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

P("== 050 adj11c tick-calibrated ==")

for name in IMGS:
    # plot box = largest red component in chart window
    z, s = zone(name, 300, 835, 160, 495)
    _, red, _, _ = masks(z)
    lab, n = ndimage.label(red, structure=np.ones((3, 3)))
    sizes = ndimage.sum(red, lab, range(1, n+1))
    big = (lab == (np.argmax(sizes)+1))
    ys, xs = np.where(big)
    bx0, bx1, by0, by1 = 300+xs.min()/s, 300+xs.max()/s, 160+ys.min()/s, 160+ys.max()/s
    P(f"\n### {name}: plot box (largest red comp) x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}")

    # x tick labels: ink blobs below the box
    z2, s2 = zone(name, bx0-15, bx1+15, by1+2, by1+22)
    ink2, _, _, _ = masks(z2)
    lab2, n2 = ndimage.label(ink2, structure=np.ones((3, 3)))
    xt = []
    for i in range(1, n2+1):
        ys2, xs2 = np.where(lab2 == i)
        if len(ys2) < 8: continue
        xt.append((bx0-15+xs2.mean()/s2, by1+2+ys2.mean()/s2, len(ys2)))
    xt.sort()
    P(f" {name} x-tick labels (cx,cy,n): " + " ".join(f"({a:.0f},{b:.0f},{c})" for a, b, c in xt))

    # y tick labels: ink blobs left of the box
    z3, s3 = zone(name, bx0-28, bx0-4, by0-6, by1+6)
    ink3, _, _, _ = masks(z3)
    lab3, n3 = ndimage.label(ink3, structure=np.ones((3, 3)))
    yt = []
    for i in range(1, n3+1):
        ys3, xs3 = np.where(lab3 == i)
        if len(ys3) < 8: continue
        yt.append((bx0-28+xs3.mean()/s3, by0-6+ys3.mean()/s3, len(ys3)))
    yt.sort(key=lambda t: t[1])
    P(f" {name} y-tick labels (cx,cy,n): " + " ".join(f"({a:.0f},{b:.0f},{c})" for a, b, c in yt))

    # affine from ticks: x labels 0..8 left-to-right; y labels 7..0 top-to-bottom
    nx, ny = len(xt), len(yt)
    if nx >= 6 and ny >= 5:
        xvals = list(range(0, 2*nx, 2)) if nx == 5 else list(range(nx))
        yvals = list(range(7, -1, -1)) if ny == 8 else list(range(ny-1, -1, -1))
        ax = np.array([t[0] for t in xt]); dxv = np.array(xvals[:len(ax)], float)
        ay = np.array([t[1] for t in yt]); dyv = np.array(yvals[:len(ay)], float)
        (a1, a0), *_ = np.linalg.lstsq(np.vstack([ax, np.ones_like(ax)]).T, dxv, rcond=None)
        (b1, b0), *_ = np.linalg.lstsq(np.vstack([ay, np.ones_like(ay)]).T, dyv, rcond=None)
        P(f" {name} AFFINE: x_data={a1:.4f}*px+{a0:.2f}  y_data={b1:.4f}*py+{b0:.2f}")
        def D(fx, fy): return (a1*fx+a0, b1*fy+b0)
        P(f" {name} check: box corners in data: TL{D(bx0,by0)} TR{D(bx1,by0)} BL{D(bx0,by1)} BR{D(bx1,by1)}")

        # line: red px minus long h/v runs minus blobs, then trimmed fit
        zw, sw = zone(name, 300, 835, 160, 495)
        _, redw, _, _ = masks(zw)
        redc = redw.copy()
        for axis in (0, 1):
            labr, nr = ndimage.label(redc, structure=np.ones((1 if axis else 3, 3 if axis else 1)))
            # remove pixels in long horizontal (axis=0) / vertical (axis=1) runs
        # simple long-run removal:
        def drop_long(m, horizontal):
            out = m.copy()
            H, W = m.shape
            if horizontal:
                for rr in range(H):
                    row = m[rr]
                    idx = np.where(row)[0]
                    if len(idx) == 0: continue
                    splits = np.split(idx, np.where(np.diff(idx) > 2)[0]+1)
                    for sp in splits:
                        if len(sp) > 18: out[rr, sp] = False
            else:
                for cc in range(W):
                    col = m[:, cc]
                    idx = np.where(col)[0]
                    if len(idx) == 0: continue
                    splits = np.split(idx, np.where(np.diff(idx) > 2)[0]+1)
                    for sp in splits:
                        if len(sp) > 18: out[sp, cc] = False
            return out
        redl = drop_long(drop_long(redc, True), False)
        labl, nl = ndimage.label(redl, structure=np.ones((3, 3)))
        pts = []
        for i in range(1, nl+1):
            ysl, xsl = np.where(labl == i)
            if len(ysl) < 25: continue
            w, h = xsl.max()-xsl.min(), ysl.max()-ysl.min()
            if w > 16 and h > 16:            # diagonal-ish cluster = line candidate
                pts.append((300+xsl/sw, 160+ysl/sw))
        if pts:
            px = np.concatenate([p[0] for p in pts]); py = np.concatenate([p[1] for p in pts])
            for _ in range(5):
                A = np.vstack([px, np.ones_like(px)]).T
                (mfit, bfit), *_ = np.linalg.lstsq(A, py, rcond=None)
                keep = np.abs(py-(mfit*px+bfit)) < 8/sw*2
                px, py = px[keep], py[keep]
            (mfit, bfit), *_ = np.linalg.lstsq(np.vstack([px, np.ones_like(px)]).T, py, rcond=None)
            i_lo, i_hi = np.argmin(px), np.argmax(px)
            ex0, ey0 = D(px[i_lo], py[i_lo]); ex1, ey1 = D(px[i_hi], py[i_hi])
            sl = (ey1-ey0)/(ex1-ex0)
            # x-intercept in data
            xi = ex0 - ey0/((ey1-ey0)/(ex1-ex0))
            P(f" {name} LINE: npts={len(px)} frame x{px.min():.0f}..{px.max():.0f}  data ({ex0:.2f},{ey0:.2f})->({ex1:.2f},{ey1:.2f}) slope={sl:.3f} x@y0={xi:.2f}")
        else:
            P(f" {name} LINE: no diagonal cluster found")

        # +ve black-ink blobs inside box interior
        z4, s4 = zone(name, bx0+8, bx1-8, by0+8, by1-8)
        ink4, red4, blue4, pink4 = masks(z4)
        black = ink4 & ~red4 & ~blue4 & ~pink4
        lab4, n4 = ndimage.label(black, structure=np.ones((3, 3)))
        bl = []
        for i in range(1, n4+1):
            ys4, xs4 = np.where(lab4 == i)
            if len(ys4) < 10: continue
            fx, fy = bx0+8+xs4.mean()/s4, by0+8+ys4.mean()/s4
            bl.append((len(ys4), fx, fy, D(fx, fy)))
        bl.sort(key=lambda t: -t[0])
        for t in bl[:8]:
            P(f" {name} black-blob n={t[0]} frame({t[1]:.0f},{t[2]:.0f}) data=({t[3][0]:.2f},{t[3][1]:.2f})")

open(OUT, "w").write("\n".join(lines) + "\n")
print("\nbanked:", OUT)
