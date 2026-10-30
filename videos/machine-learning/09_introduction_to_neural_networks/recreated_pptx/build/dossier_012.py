#!/usr/bin/env python3
"""Slide 012 fidelity dossier: original frame vs fresh render, region by region.

Every measurement is expressed in slide inches (13.333 x 7.5) so the 960x540
original and the 2001x1125 render compare directly.
Regions are derived from the ORIGINAL's own ink, not from the build script.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

SW, SH = 13.333, 7.5


def load(p):
    im = Image.open(p).convert("RGB")
    return np.array(im).astype(int), im.size[0], im.size[1]


def comps(mask, min_px):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px:
            continue
        out.append((int(len(xs)), int(xs.min()), int(ys.min()),
                    int(xs.max()), int(ys.max()),
                    float(xs.mean()), float(ys.mean())))
    out.sort(key=lambda t: -t[0])
    return out


def I(x, y, W, H):
    return round(x / W * SW, 3), round(y / H * SH, 3)


def bbox_str(c, W, H):
    x0, y0 = I(c[1], c[2], W, H)
    x1, y1 = I(c[3], c[4], W, H)
    return f"({x0},{y0})-({x1},{y1}) {round(x1-x0,3)}w x {round(y1-y0,3)}h"


def dossier(path, label):
    a, W, H = load(path)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    print(f"\n{'#'*72}\n# {label}   raster {W}x{H}\n{'#'*72}")

    red = (r > 135) & ((r - g) > 50) & ((r - b) > 50)

    # ---------- 1. TITLE ----------
    # red ink in the top band, excluding the house-frame verticals
    tb = np.zeros_like(red)
    ys_, xs_ = np.nonzero(red)
    sel = (ys_ < int(H * 0.22)) & (xs_ > int(W * 0.03)) & (xs_ < int(W * 0.97))
    tb[ys_[sel], xs_[sel]] = True
    cs = comps(tb, 25)
    if cs:
        x0 = min(c[1] for c in cs); x1 = max(c[3] for c in cs)
        y0 = min(c[2] for c in cs); y1 = max(c[4] for c in cs)
        print(f"[TITLE] ink bbox {bbox_str((0,x0,y0,x1,y1),W,H)}  "
              f"glyph_components={len(cs)}")
        xs_all = sorted(c[1] for c in cs)
        gaps = []
        for i in range(1, len(xs_all)):
            if xs_all[i] - xs_all[i-1] > W * 0.02:
                gaps.append((xs_all[i-1], xs_all[i]))
        print(f"[TITLE] word-gaps(px): {[(round(p[0]/W*SW,2), round(p[1]/W*SW,2)) for p in gaps]}")

    # ---------- 2. TRUTH TABLE (top-left quadrant) ----------
    q = red.copy()
    q[int(H*0.25):, :] = False
    q[:, int(W*0.42):] = False
    cs = comps(q, 200)
    if cs:
        c = cs[0]
        print(f"[TABLE] red-block bbox {bbox_str(c,W,H)} (n={c[0]})")
        tx0, tx1 = c[1], c[3]
        ty0, ty1 = c[2], c[4]
        # interior red rows/cols inside the block
        blk = red[ty0:ty1+1, tx0:tx1+1]
        rowsum = blk.sum(axis=1)
        colsum = blk.sum(axis=0)
        rl = [ty0+i for i,v in enumerate(rowsum) if v > blk.shape[1]*0.75]
        cl = [tx0+i for i,v in enumerate(colsum) if v > blk.shape[0]*0.75]
        def g(idx):
            o=[]
            for i in idx:
                if o and i-o[-1][-1] <= 2: o[-1].append(i)
                else: o.append([i])
            return [(p[0],p[-1]) for p in o]
        print(f"[TABLE] interior h-lines(in): {[round(np.mean(p)/H*SH,3) for p in g(rl)]}")
        print(f"[TABLE] interior v-lines(in): {[round(p[0]/W*SW,3) for p in g(cl)]}")
        # cell fill colors: sample the middle of each cell
        if len(g(rl)) >= 2 and len(g(cl)) >= 2:
            hgr = g(rl); vgr = g(cl)
            print(f"[TABLE] cell fills (row,col)->RGB at cell center:")
            for ri in range(len(hgr)-1):
                cy = (hgr[ri][0] + hgr[ri][1])//2
                row_out=[]
                for ci in range(len(vgr)-1):
                    cx = (vgr[ci][0] + vgr[ci][1])//2
                    y = min(cy, H-2); x = min(cx, W-2)
                    patch = a[max(0,y-2):y+3, max(0,x-2):x+3].reshape(-1,3).mean(axis=0)
                    row_out.append(tuple(int(v) for v in patch))
                print(f"   row{ri}: {row_out}")

    # ---------- 3. PLOT PANEL (white box, right of table) ----------
    white = (r > 243) & (g > 243) & (b > 243)
    qx0 = int(W * 0.40)
    qw = white[:int(H * 0.75), qx0:]
    lab, n = ndimage.label(qw)
    if n:
        sizes = ndimage.sum(qw, lab, range(1, n+1))
        k = int(np.argmax(sizes)) + 1
        ys, xs = np.nonzero(lab == k)
        px0, py0, px1, py1 = xs.min()+qx0, ys.min(), xs.max()+qx0, ys.max()
        print(f"[PLOT] white panel {bbox_str((0,px0,py0,px1,py1),W,H)}  px={int(sizes[k-1])}")
        # markers inside this panel only
        for nm, m in (("GREEN",(g>165)&(r<150)&(b<150)), ("CYAN",(g>185)&(b>185)&(r<160))):
            mm = np.zeros_like(m)
            mm[py0:py1+1, px0:px1+1] = m[py0:py1+1, px0:px1+1]
            cs = comps(mm, 30)
            if cs:
                for c in cs[:6]:
                    cx, cy = I(c[5], c[6], W, H)
                    print(f"[PLOT] {nm} blob n={c[0]:<5} centroid=({cx},{cy}) "
                          f"bbox {bbox_str(c,W,H)}")
        # blue decision line inside panel
        blue = (b > 140) & (r < 160) & (g < 160)
        bb = np.zeros_like(blue)
        bb[py0:py1+1, px0:px1+1] = blue[py0:py1+1, px0:px1+1]
        cs = comps(bb, 25)
        for c in cs[:4]:
            print(f"[PLOT] BLUE blob n={c[0]:<5} bbox {bbox_str(c,W,H)}")
        # red axis pixels inside panel
        rr = np.zeros_like(red)
        rr[py0:py1+1, px0:px1+1] = red[py0:py1+1, px0:px1+1]
        cs = comps(rr, 40)
        for c in cs[:6]:
            print(f"[PLOT] RED(axes) blob n={c[0]:<5} bbox {bbox_str(c,W,H)}")

    # ---------- 4. NET DIAGRAM (bottom-left) ----------
    bl = slice(int(H*0.60), int(H*0.97))
    lc = slice(int(W*0.04), int(W*0.55))
    reg = a[bl, lc]
    ink = (reg.max(axis=2) < 165)
    cs = comps(ink, 40)
    if cs:
        print(f"[NET] dark-ink blobs in bottom-left (top 8):")
        for c in cs[:8]:
            c2 = (c[0], c[1]+int(W*0.04), c[2]+int(H*0.60), c[3]+int(W*0.04), c[4]+int(H*0.60), c[5], c[6])
            print(f"   n={c[0]:<6} bbox {bbox_str(c2,W,H)}")
    # sigma circle light blue
    lblue = (r > 150) & (r < 220) & (g > 195) & (b > 220)
    mm = np.zeros_like(lblue); mm[bl, lc] = lblue[bl, lc]
    for c in comps(mm, 40)[:3]:
        c2 = (c[0], c[1]+int(W*0.04), c[2]+int(H*0.60), c[3]+int(W*0.04), c[4]+int(H*0.60), c[5], c[6])
        print(f"[NET] lightblue(Sigma) n={c[0]:<5} bbox {bbox_str(c2,W,H)}")
    # plum step box
    plum = (r > 180) & (r < 250) & (g > 130) & (g < 200) & (b > 180) & (b < 245)
    mm = np.zeros_like(plum); mm[bl, lc] = plum[bl, lc]
    for c in comps(mm, 25)[:4]:
        c2 = (c[0], c[1]+int(W*0.04), c[2]+int(H*0.60), c[3]+int(W*0.04), c[4]+int(H*0.60), c[5], c[6])
        print(f"[NET] plum(step box) n={c[0]:<5} bbox {bbox_str(c2,W,H)}")
    # red border rect around net
    rr = np.zeros_like(red); rr[bl, lc] = red[bl, lc]
    for c in comps(rr, 200)[:3]:
        c2 = (c[0], c[1]+int(W*0.04), c[2]+int(H*0.60), c[3]+int(W*0.04), c[4]+int(H*0.60), c[5], c[6])
        print(f"[NET] red(border) n={c[0]:<5} bbox {bbox_str(c2,W,H)}")

    # ---------- 5. EQUATION BOX (bottom-right) ----------
    br = slice(int(H*0.68), int(H*0.95))
    rc = slice(int(W*0.45), W)
    peach = (r > 246) & (g > 208) & (g < 243) & (b > 172) & (b < 220)
    mm = np.zeros_like(peach); mm[br, rc] = peach[br, rc]
    cs = comps(mm, 150)
    if cs:
        c = cs[0]
        c2 = (c[0], c[1]+int(W*0.45), c[2]+int(H*0.68), c[3]+int(W*0.45), c[4]+int(H*0.68), c[5], c[6])
        print(f"[EQ] peach box {bbox_str(c2,W,H)} n={c[0]}")
        # equation ink inside
        reg = a[c2[2]:c2[4]+1, c2[1]:c2[3]+1]
        dark = (reg.max(axis=2) < 140)
        ys, xs = np.nonzero(dark)
        if len(xs):
            print(f"[EQ] equation ink bbox in-slide "
                  f"({round((c2[1]+xs.min())/W*SW,3)},{round((c2[2]+ys.min())/H*SH,3)})-"
                  f"({round((c2[1]+xs.max())/W*SW,3)},{round((c2[2]+ys.max())/H*SH,3)}) "
                  f"n={len(xs)}")
    else:
        print("[EQ] peach box: NOT FOUND in bottom-right")

    # ---------- 6. BADGE ----------
    yellow = (r > 228) & (g > 222) & (b > 160) & (b < 220)
    mm = np.zeros_like(yellow)
    mm[:int(H*0.15), int(W*0.88):] = yellow[:int(H*0.15), int(W*0.88):]
    cs = comps(mm, 30)
    if cs:
        c = cs[0]
        print(f"[BADGE] yellow {bbox_str(c,W,H)} n={c[0]}")


if __name__ == "__main__":
    dossier(sys.argv[1], "ORIGINAL")
    dossier(sys.argv[2], "RENDER")
