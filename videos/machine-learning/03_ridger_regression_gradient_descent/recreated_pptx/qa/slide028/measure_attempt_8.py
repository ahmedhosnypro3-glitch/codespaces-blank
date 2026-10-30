#!/usr/bin/env python3
"""w028 attempt-8 independent measurement: slide 028 curve panels.

PIL + numpy only (no scipy). Measures, for the ORIGINAL 960x540 frame and the
CURRENT render (render_7.png, 2001x1125):
  * cyan marker blobs (dots) in each panel: count, centroids, bbox, mean colour
  * connector-line presence between every candidate marker pair (ink coverage
    along the straight segment + mean colour), to recover the drawn TOPOLOGY
  * per-column curve trace (median cyan y) and valley position
  * red axis geometry
All coordinates are reported in FRAME px (960x540 space) for direct comparison.
"""
import numpy as np
from PIL import Image
import json, os

ROOT = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = os.path.join(ROOT, "unique_slides/slide_028.jpg")
REND = os.path.join(ROOT, "recreated_pptx/qa/slide028/render_7.png")

PANELS = {
    "L": (150, 205, 440, 455),   # frame px x0,y0,x1,y1 (generous around left panel)
    "R": (495, 205, 790, 455),
}

def load(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    return a

def to_frame(a, scale):
    """nearest-neighbour resample to 960x540 frame space"""
    return np.asarray(Image.fromarray(a.astype(np.uint8)).resize((960, 540), Image.BOX)).astype(np.int16)

def cyan_mask(a):
    r = a[:, :, 0]; g = a[:, :, 1]; b = a[:, :, 2]
    return (b.astype(int) - r.astype(int) > 18) & (g.astype(int) - r.astype(int) > 6) & (b > 120)

def red_mask(a):
    r = a[:, :, 0]; g = a[:, :, 1]; b = a[:, :, 2]
    return (r.astype(int) - np.maximum(g, b).astype(int) > 35) & (r > 90)

def dark_mask(a):
    return a.max(axis=2) < 150

def erode(m):
    out = m.copy()
    out[1:, :] &= m[:-1, :]; out[:-1, :] &= m[1:, :]
    out[:, 1:] &= m[:, :-1]; out[:, :-1] &= m[:, 1:]
    return out

def dilate(m):
    out = m.copy()
    out[1:, :] |= m[:-1, :]; out[:-1, :] |= m[1:, :]
    out[:, 1:] |= m[:, :-1]; out[:, :-1] |= m[:, 1:]
    return out

def components(mask, min_area=6):
    """simple flood-fill labelling (4-conn) on a small boolean mask"""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    comps = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]
        seen[y0, x0] = True
        pts = []
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        if len(pts) >= min_area:
            comps.append(pts)
    out = []
    for pts in comps:
        ys_ = np.array([p[0] for p in pts]); xs_ = np.array([p[1] for p in pts])
        out.append(dict(area=len(pts), cy=float(ys_.mean()), cx=float(xs_.mean()),
                        y0=int(ys_.min()), y1=int(ys_.max()), x0=int(xs_.min()),
                        x1=int(xs_.max()),
                        h=int(ys_.max() - ys_.min() + 1), w=int(xs_.max() - xs_.min() + 1)))
    return out

def blobs(a, region, kind="cyan", label=""):
    x0, y0, x1, y1 = region
    sub = a[y0:y1, x0:x1]
    m = cyan_mask(sub) if kind == "cyan" else red_mask(sub)
    # thick ink = mask survives 2 erosions (removes 1-3px strokes)
    thick = erode(erode(m))
    comps = components(thick, min_area=8)
    print(f"  [{label}] thick-{kind} blobs: {len(comps)}")
    res = []
    for c in sorted(comps, key=lambda c: c["cx"]):
        cx = c["cx"] + x0; cy = c["cy"] + y0
        # mean colour of the ORIGINAL thick blob pixels
        ys = np.arange(y0, y1); xs = np.arange(x0, x1)
        res.append((round(cx, 1), round(cy, 1), c["w"], c["h"], c["area"]))
        print(f"    blob cx={cx:6.1f} cy={cy:6.1f}  w={c['w']:2d} h={c['h']:2d} area={c['area']:3d}")
    return res

def seg_ink(a, p, q, trim=9):
    """coverage of 'ink' (deviation from the local background) along p->q,
    ignoring the first/last `trim` px around the markers."""
    x0, y0 = p; x1, y1 = q
    L = int(round(max(abs(x1 - x0), abs(y1 - y0))))
    if L <= 2 * trim:
        trim = max(1, L // 4)
    ts = np.linspace(0, 1, L + 1)
    cover = 0; total = 0; cols = []
    for t in ts:
        x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        if t * L < trim or (1 - t) * L < trim:
            continue
        total += 1
        # column band: look in a +/-1 px vertical window for any strongly non-white ink
        best = None
        for yy in range(int(round(y)) - 1, int(round(y)) + 2):
            px = a[yy, int(round(x))]
            dev = 255 * 3 - int(px.sum())
            if dev > 60:  # any visible ink
                if best is None or dev > best[0]:
                    best = (dev, tuple(int(v) for v in px))
        if best is not None:
            cover += 1
            cols.append(best[1])
    mean_col = tuple(int(np.mean([c[i] for c in cols])) for i in range(3)) if cols else None
    return cover, total, mean_col

def curve_trace(a, region):
    x0, y0, x1, y1 = region
    sub = a[y0:y1, x0:x1]
    m = cyan_mask(sub)
    xs = []; ys = []
    for x in range(m.shape[1]):
        yy = np.nonzero(m[:, x])[0]
        if len(yy) == 0:
            continue
        xs.append(x + x0); ys.append(float(np.median(yy)) + y0)
    xs = np.array(xs); ys = np.array(ys)
    i = int(np.argmax(ys))
    return dict(x_min=int(xs.min()), x_max=int(xs.max()),
                valley_x=float(xs[i]), valley_y=float(ys[i]),
                left_end_y=float(ys[0]), right_end_y=float(ys[-1]),
                n=int(len(xs)))

def axis_geo(a, region):
    x0, y0, x1, y1 = region
    sub = a[y0:y1, x0:x1]
    m = red_mask(sub)
    cols = m.sum(axis=0); rows = m.sum(axis=1)
    vx = int(np.argmax(cols)); hy = int(np.argmax(rows))
    return dict(vaxis_x=vx + x0, vaxis_px=int(cols[vx]),
                haxis_y=hy + y0, haxis_px=int(rows[hy]))

def panel_report(name, a, scale_note):
    print(f"\n================ {name} ({scale_note}) ================")
    region = PANELS["L"] if name.endswith("L") else PANELS["R"]
    print(f" region frame-px {region}")
    ax = axis_geo(a, region)
    print(f"  red axes: vertical x={ax['vaxis_x']} ({ax['vaxis_px']}px)  horizontal y={ax['haxis_y']} ({ax['haxis_px']}px)")
    ct = curve_trace(a, region)
    print(f"  cyan curve trace: x {ct['x_min']}..{ct['x_max']}  valley ({ct['valley_x']:.1f},{ct['valley_y']:.1f})"
          f"  end ys L={ct['left_end_y']:.1f} R={ct['right_end_y']:.1f}")
    markers = blobs(a, region, "cyan", f"{name} cyan")
    if len(markers) >= 2:
        print("  connector coverage matrix (ordered pairs, coverage fraction, mean colour):")
        for i, p in enumerate(markers):
            for j, q in enumerate(markers):
                if i == j:
                    continue
                cov, tot, mc = seg_ink(a, (p[0], p[1]), (q[0], q[1]))
                frac = cov / max(tot, 1)
                flag = "LINE " if frac > 0.75 else ("part " if frac > 0.35 else "none ")
                print(f"    {i}->{j}: {flag} {cov:3d}/{tot:3d} = {frac:4.2f}  mean={mc}")
    return markers, ct

def main():
    ao = load(ORIG)
    ar = load(REND)
    print(f"original {ao.shape[1]}x{ao.shape[0]}   render {ar.shape[1]}x{ar.shape[0]}  scale={ar.shape[1]/960:.4f}")
    for nm, a, s in (("ORIG", ao, "960x540 native"), ("REND", ar, "render_7 2001x1125")):
        if nm == "REND":
            a = to_frame(a, 1)
        for panel in ("L", "R"):
            panel_report(nm + "_" + panel, a, s)

if __name__ == "__main__":
    main()
