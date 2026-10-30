#!/usr/bin/env python3
"""w028 attempt-8b: precise marker + connector measurement (PIL/numpy only).

Left panel  : original markers are HOLLOW circles (white core + cyan ring); the
              right panel's are FILLED discs. Two detectors:
                - ring_score(): template score for a hollow circle (bright core,
                  cyan annulus at r=3)
                - disc_core()  : distance-transform cores (>=3 erosions) = filled discs
Connectors  : chord ink-coverage test between every marker pair (thin light
              grey-blue strokes; the curve is also cyan so chords that merely
              follow the curve are reported separately).
All coordinates in FRAME px (960x540).
"""
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = ROOT + "/unique_slides/slide_028.jpg"
REND = ROOT + "/recreated_pptx/qa/slide028/render_7.png"

def load_frame(path):
    im = Image.open(path).convert("RGB")
    if im.width != 960:
        im = im.resize((960, 540), Image.BOX)
    return np.asarray(im).astype(np.float32)

def cyan(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (b - r > 18) & (g - r > 6) & (b > 110)

def ink(a):
    """any visible non-white ink"""
    return a.sum(axis=2) < 690

def erode(m):
    o = m.copy()
    o[1:, :] &= m[:-1, :]; o[:-1, :] &= m[1:, :]
    o[:, 1:] &= m[:, :-1]; o[:, :-1] &= m[:, 1:]
    return o

def comps(mask, min_area=4):
    h, w = mask.shape; seen = np.zeros_like(mask, bool); out = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        st = [(y0, x0)]; seen[y0, x0] = True; pts = []
        while st:
            y, x = st.pop(); pts.append((y, x))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                yy, xx = y+dy, x+dx
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True; st.append((yy, xx))
        if len(pts) >= min_area:
            ys_ = np.array([p[0] for p in pts]); xs_ = np.array([p[1] for p in pts])
            out.append(dict(area=len(pts), cx=float(xs_.mean()), cy=float(ys_.mean()),
                            y0=int(ys_.min()), y1=int(ys_.max()),
                            x0=int(xs_.min()), x1=int(xs_.max())))
    return out

def disc_detect(a, box, label):
    x0, y0, x1, y1 = box
    m = cyan(a)
    mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    core = mm
    levels = [int(core.sum())]
    for i in range(4):
        core = erode(core); levels.append(int(core.sum()))
    cs = comps(erode(erode(core)), min_area=2)   # >= 5 erosions total
    print(f"  [{label}] cyan erosion levels {levels} -> disc cores: {len(cs)}")
    res = []
    for c in sorted(cs, key=lambda c: c['cx']):
        print(f"      FILLED disc cx={c['cx']:6.1f} cy={c['cy']:6.1f} bbox x{c['x0']}..{c['x1']} y{c['y0']}..{c['y1']} area={c['area']}")
        res.append((c['cx'], c['cy']))
    return res

def ring_detect(a, box, label, r=3.2, core_thr=232, ring_thr=6, min_sep=4):
    """hollow-circle template: bright core (3x3 mean > core_thr) + cyan at r~3."""
    x0, y0, x1, y1 = box
    lum = a.mean(axis=2)
    cm = cyan(a).astype(np.float32)
    ang = np.linspace(0, 2*np.pi, 16, endpoint=False)
    ring_off = [(int(round(r*np.sin(t))), int(round(r*np.cos(t)))) for t in ang]
    best = []
    for y in range(y0+1, y1-1):
        for x in range(x0+1, x1-1):
            if lum[y, x] < core_thr:
                continue
            core = lum[y-1:y+2, x-1:x+2].mean()
            if core < core_thr:
                continue
            ring = np.mean([cm[y+dy, x+dx] for dy, dx in ring_off])
            if ring >= 0.40:
                best.append((ring, x, y))
    best.sort(reverse=True)
    picked = []
    for s, x, y in best:
        if all((x-px)**2 + (y-py)**2 >= min_sep**2 for px, py in picked):
            picked.append((float(x), float(y)))
    picked.sort()
    print(f"  [{label}] hollow-circle detections: {len(picked)} (ring score>=0.40)")
    for x, y in picked:
        print(f"      HOLLOW cx={x:6.1f} cy={y:6.1f}")
    return picked

def chord(a, p, q, trim, tol=2):
    """ink fraction along p->q (excluding `trim` px at both ends), scanning a
    +/-tol perpendicular band. Returns (cover_pts, total_pts, frac, mean colour)."""
    x0, y0 = p; x1, y1 = q
    L = max(abs(x1-x0), abs(y1-y0))
    n = max(int(L), 8)
    dx, dy = (x1-x0)/n, (y1-y0)/n
    nx, ny = -dy, dx
    nn = max((nx*nx+ny*ny) ** 0.5, 1e-6); nx, ny = nx/nn, ny/nn
    cov = 0; tot = 0; cols = []
    for i in range(n+1):
        t = i
        if t < trim or n - t < trim:
            continue
        tot += 1
        hit = None
        for o in range(-tol, tol+1):
            x = int(round(x0 + dx*t + nx*o)); y = int(round(y0 + dy*t + ny*o))
            if 0 <= y < a.shape[0] and 0 <= x < a.shape[1]:
                px = a[y, x]
                if px.sum() < 690 and not (px[0] - max(px[1], px[2]) > 60):
                    if hit is None or px.sum() < hit.sum():
                        hit = px
        if hit is not None:
            cov += 1; cols.append(hit)
    mc = tuple(int(round(c[i].mean())) if len(c) else None for i in range(3)) if cols else None
    return cov, tot, cov/max(tot,1), mc

def chord_matrix(a, pts, names, trim, label):
    print(f"  [{label}] chord ink coverage (trim {trim}px, +/-2px band):")
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            c, t, f, mc = chord(a, pts[i], pts[j], trim)
            flag = "LINE" if f > 0.80 else ("part" if f > 0.40 else "none")
            print(f"      {names[i]}-{names[j]}: {flag:4s} {c:3d}/{t:3d} = {f:4.2f} mean={mc}")

def main():
    ao = load_frame(ORIG); ar = load_frame(REND)
    print("original 960x540; render_7 box-downsampled to 960x540 for frame-space comparison")

    print("\n=== LEFT PANEL frame px x150..440 y205..455 ===")
    print("ORIGINAL:")
    lo = ring_detect(ao, (155, 225, 300, 450), "orig-left hollow", r=3.0)
    print("RENDER_7:")
    lr = ring_detect(ar, (155, 225, 400, 450), "rend-left hollow", r=3.0)
    lfr = disc_detect(ar, (150, 205, 440, 455), "rend-left filled")
    lfo = disc_detect(ao, (150, 205, 440, 455), "orig-left filled")

    print("\n=== RIGHT PANEL frame px x495..790 y205..455 ===")
    ro = disc_detect(ao, (495, 205, 790, 455), "orig-right discs")
    rr = disc_detect(ar, (495, 205, 790, 455), "rend-right discs")
    names = ["A", "B", "C", "D"]
    if len(ro) == 4:
        print("ORIGINAL right chords (A=leftmost):")
        chord_matrix(ao, ro, names, trim=9, label="orig-right")
    if len(rr) == 4:
        print("RENDER right chords:")
        chord_matrix(ar, rr, names, trim=9, label="rend-right")

if __name__ == "__main__":
    main()
