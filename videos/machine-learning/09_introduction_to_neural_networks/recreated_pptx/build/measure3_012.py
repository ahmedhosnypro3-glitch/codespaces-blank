#!/usr/bin/env python3
"""Component-level ground truth for slide_012: original frame vs fresh render.

Uses connected components so each red/ink structure is isolated instead of
being merged by min/max over scattered antialiased pixels.
All geometry reported in slide inches (13.333 x 7.5).
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
        out.append(dict(n=int(len(xs)), x0=int(xs.min()), x1=int(xs.max()),
                        y0=int(ys.min()), y1=int(ys.max()),
                        cx=float(xs.mean()), cy=float(ys.mean())))
    out.sort(key=lambda d: -d["n"])
    return out


def inch(x, y, W, H):
    return round(x / W * SW, 3), round(y / H * SH, 3)


def report(path, label):
    a, W, H = load(path)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    print(f"\n{'='*70}\n{label}  ({W}x{H} raster)")

    red = (r > 140) & ((r - g) > 55) & ((r - b) > 55)
    print("RED components (top 14 by area) — x0,y0,x1,y1 in inches:")
    for c in comps(red, 60)[:14]:
        x0, y0 = inch(c["x0"], c["y0"], W, H)
        x1, y1 = inch(c["x1"], c["y1"], W, H)
        w = round(c["x1"] - c["x0"] + 1, 1)
        h = round(c["y1"] - c["y0"] + 1, 1)
        print(f"  n={c['n']:<6} bbox=({x0},{y0})-({x1},{y1})  {w}x{h}px")

    # --- truth table: red grid inside top-left quadrant ---
    q = red[:int(H * 0.65), :int(W * 0.45)]
    hs = q.sum(axis=1)
    vs = q.sum(axis=0)
    hthr = q.shape[1] * 0.12
    vthr = q.shape[0] * 0.10
    hruns = [i for i, v in enumerate(hs) if v > hthr]
    vruns = [i for i, v in enumerate(vs) if v > vthr]

    def group(idx):
        out = []
        for i in idx:
            if out and i - out[-1][-1] <= 2:
                out[-1].append(i)
            else:
                out.append([i])
        return out

    gh, gv = group(hruns), group(vruns)
    print(f"TABLE grid h-lines (in): {[round(np.mean(p)/H*SH,3) for p in gh]}")
    print(f"TABLE grid v-lines (in): {[round(p[0]/W*SW,3) for p in gv]}")
    if gv:
        print(f"  table x-span: {gv[0][0]/W*SW:.3f} .. {gv[-1][-1]/W*SW:.3f} in")
    if gh:
        print(f"  table y-span: {gh[0][0]/H*SH:.3f} .. {gh[-1][-1]/H*SH:.3f} in")
        if len(gh) >= 2:
            rows = [(gh[i][0] + gh[i][-1]) / 2 for i in range(len(gh))]
            print(f"  row pitch (in): {[round((rows[i+1]-rows[i])/H*SH,3) for i in range(len(rows)-1)]}")

    # --- plot panel: white region right of the table ---
    white = (r > 243) & (g > 243) & (b > 243)
    qx0 = int(W * 0.42)
    qw = white[:int(H * 0.72), qx0:]
    lab, n = ndimage.label(qw)
    sizes = ndimage.sum(qw, lab, range(1, n + 1))
    if len(sizes):
        k = int(np.argmax(sizes)) + 1
        ys, xs = np.nonzero(lab == k)
        x0, y0 = inch(xs.min() + qx0, ys.min(), W, H)
        x1, y1 = inch(xs.max() + qx0, ys.max(), W, H)
        print(f"PLOT white panel (largest comp, in): ({x0},{y0})-({x1},{y1})  "
              f"{round(x1-x0,3)}w x {round(y1-y0,3)}h in   px={int(sizes[k-1])}")

    # --- markers ---
    green = (g > 165) & (r < 145) & (b < 145)
    cyan = (g > 185) & (b > 185) & (r < 155)
    for nm, m in (("GREEN", green), ("CYAN", cyan)):
        mm = np.zeros_like(m)
        mm[:int(H * 0.08), :] = False
        mm[int(H * 0.75):, :] = False
        mm[:, :int(W * 0.42)] = False
        cs = comps(mm, 40)
        if not cs:
            print(f"{nm}: none")
            continue
        print(f"{nm} marker blobs (in, cx,cy):")
        for c in cs[:8]:
            cx, cy = inch(c["cx"], c["cy"], W, H)
            x0, y0 = inch(c["x0"], c["y0"], W, H)
            x1, y1 = inch(c["x1"], c["y1"], W, H)
            print(f"   n={c['n']:<5} centroid=({cx},{cy}) bbox=({x0},{y0})-({x1},{y1})")

    # --- blue decision line inside plot panel only ---
    blue = (b > 150) & (r < 150) & (g < 150)
    bb = np.zeros_like(blue)
    bb[:int(H * 0.08), :] = False
    bb[int(H * 0.75):, :] = False
    bb[:, :int(W * 0.42)] = False
    cs = comps(bb, 40)
    for c in cs[:5]:
        x0, y0 = inch(c["x0"], c["y0"], W, H)
        x1, y1 = inch(c["x1"], c["y1"], W, H)
        print(f"BLUE comp n={c['n']:<5} bbox=({x0},{y0})-({x1},{y1})")

    # --- peach equation box (exact fill) ---
    peach = (r > 246) & (g > 210) & (g < 242) & (b > 175) & (b < 218)
    cs = comps(peach, 200)
    if cs:
        c = cs[0]
        x0, y0 = inch(c["x0"], c["y0"], W, H)
        x1, y1 = inch(c["x1"], c["y1"], W, H)
        print(f"PEACH eq-box (in): ({x0},{y0})-({x1},{y1})  {round(x1-x0,3)}w x {round(y1-y0,3)}h  n={c['n']}")
    else:
        print("PEACH eq-box: not found")

    # --- light-blue sigma circle ---
    lblue = (r > 150) & (r < 215) & (g > 195) & (b > 220)
    cs = comps(lblue, 60)
    for c in cs[:4]:
        x0, y0 = inch(c["x0"], c["y0"], W, H)
        x1, y1 = inch(c["x1"], c["y1"], W, H)
        print(f"SIGMA lightblue comp n={c['n']:<5} bbox=({x0},{y0})-({x1},{y1})")

    # --- plum step box ---
    plum = (r > 185) & (r < 245) & (g > 135) & (g < 195) & (b > 185) & (b < 240)
    cs = comps(plum, 40)
    for c in cs[:4]:
        x0, y0 = inch(c["x0"], c["y0"], W, H)
        x1, y1 = inch(c["x1"], c["y1"], W, H)
        print(f"PLUM step-box comp n={c['n']:<5} bbox=({x0},{y0})-({x1},{y1})")

    # --- title ink (red text in top band, excluding frame) ---
    tb = np.zeros_like(red)
    tb[int(H * 0.05):int(H * 0.16), int(W * 0.05):int(W * 0.90)] = red[int(H * 0.05):int(H * 0.16), int(W * 0.05):int(W * 0.90)]
    ys, xs = np.nonzero(tb)
    if len(xs):
        x0, y0 = inch(xs.min(), ys.min(), W, H)
        x1, y1 = inch(xs.max(), ys.max(), W, H)
        print(f"TITLE red ink (in): ({x0},{y0})-({x1},{y1})")

    # --- dark bottom bar ---
    dark = (r < 70) & (g < 70) & (b < 70)
    prow = dark.sum(axis=1)
    rows = [i for i, v in enumerate(prow) if v > W * 0.5]
    if rows:
        print(f"DARK bottom bar y (in): {rows[0]/H*SH:.3f} .. {rows[-1]/H*SH:.3f}")
    else:
        print("DARK bottom bar: none")


if __name__ == "__main__":
    report(sys.argv[1], "ORIGINAL")
    report(sys.argv[2], "RENDER")
