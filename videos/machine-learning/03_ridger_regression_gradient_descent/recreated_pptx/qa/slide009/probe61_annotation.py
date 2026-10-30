# probe61_annotation.py — re-measure the slide 009 annotation regions from the
# ORIGINAL frame (founder findings 2026-10-25: label/arrow alignment, orthogonal
# projection on the blue line, arrowhead on the upper end, red line parallel to
# the blue line with no arrowhead).
# Masks: RED (C00000 family, excludes orange via g<90), ROSE (pale 240,190,200),
# BLUE (fitted line), BIGRED (238,49,69 disc). 8-connected components + moments.
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

MASKS = {
    "RED":   (r > 110) & (r - g > 50) & (r - b > 40) & (g < 90) & (b < 90),
    "ROSE":  (r > 195) & (g > 150) & (g < 228) & (b > 150) & (b < 232) & (r - b > 12) & (r - b < 70) & (r - g > 15),
    "BLUE":  (b > 110) & (r < 90) & (g < 90),
    "BIGRED":(r > 200) & (g > 25) & (g < 75) & (b > 45) & (b < 95),
}

def components(mask):
    lab = np.zeros(mask.shape, dtype=int)
    out = []
    from collections import deque
    cur = 0
    ys, xs = np.where(mask)
    maskset = mask
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        cur += 1
        q = deque([(y0, x0)])
        lab[y0, x0] = cur
        pix = []
        while q:
            y, x = q.popleft()
            pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and maskset[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur
                        q.append((ny, nx))
        P = np.array(pix)
        ys_, xs_ = P[:, 0], P[:, 1]
        area = len(P)
        cy, cx = ys_.mean(), xs_.mean()
        # second moments -> principal angle (image coords: x right, y down)
        dx = xs_ - cx; dy = ys_ - cy
        sxx = (dx * dx).mean(); syy = (dy * dy).mean(); sxy = (dx * dy).mean()
        theta = 0.5 * np.degrees(np.arctan2(2 * sxy, sxx - syy))
        out.append(dict(area=area, cx=round(float(cx), 1), cy=round(float(cy), 1),
                        x0=int(xs_.min()), x1=int(xs_.max()),
                        y0=int(ys_.min()), y1=int(ys_.max()),
                        w=int(xs_.max() - xs_.min() + 1), h=int(ys_.max() - ys_.min() + 1),
                        angle=round(float(theta), 1)))
    out.sort(key=lambda d: -d["area"])
    return out

REGIONS = {
    "LEFT":  dict(x0=150, x1=350, y0=110, y1=330),
    "RIGHT": dict(x0=560, x1=780, y0=110, y1=360),
}

report = {}
for name, R in REGIONS.items():
    sub = {}
    for mname, m in MASKS.items():
        win = np.zeros_like(m)
        win[R["y0"]:R["y1"], R["x0"]:R["x1"]] = m[R["y0"]:R["y1"], R["x0"]:R["x1"]]
        comps = [c for c in components(win) if c["area"] >= 4]
        sub[mname] = comps
    report[name] = sub

for name, sub in report.items():
    print(f"===== {name} region =====")
    for mname, comps in sub.items():
        print(f"  -- {mname}: {len(comps)} components (area>=4) --")
        for c in comps[:40]:
            print(f"     area={c['area']:5d}  c=({c['cx']:6.1f},{c['cy']:6.1f})  "
                  f"bbox x{c['x0']}..{c['x1']} y{c['y0']}..{c['y1']}  "
                  f"w{c['w']:3d} h{c['h']:3d}  axis={c['angle']:6.1f}")

# Blue fitted-line refit through all BLUE px in each panel interior
for name, xr in (("LEFT", (100, 460)), ("RIGHT", (492, 865))):
    win = np.zeros_like(MASKS["BLUE"])
    win[115:470, xr[0]:xr[1]] = MASKS["BLUE"][115:470, xr[0]:xr[1]]
    ys, xs = np.where(win)
    A = np.vstack([xs, np.ones_like(xs)]).T
    sol, res, _, _ = np.linalg.lstsq(A, ys, rcond=None)
    slope, icpt = sol
    print(f"BLUE LINE {name}: y = {slope:.5f} x + {icpt:.2f}  "
          f"(n={len(xs)})  angle={np.degrees(np.arctan(slope)):.2f} deg; "
          f"perp angle from vertical = {np.degrees(np.arctan(-1/slope)):.2f} deg")

with open("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/probe61_annotation.txt", "w") as f:
    import sys
    sys.stdout = f
    for name, sub in report.items():
        print(f"===== {name} region =====")
        for mname, comps in sub.items():
            print(f"  -- {mname}: {len(comps)} components (area>=4) --")
            for c in comps[:60]:
                print(f"     area={c['area']:5d}  c=({c['cx']:6.1f},{c['cy']:6.1f})  "
                      f"bbox x{c['x0']}..{c['x1']} y{c['y0']}..{c['y1']}  "
                      f"w{c['w']:3d} h{c['h']:3d}  axis={c['angle']:6.1f}")
    for name, xr in (("LEFT", (100, 460)), ("RIGHT", (492, 865))):
        win = np.zeros_like(MASKS["BLUE"])
        win[115:470, xr[0]:xr[1]] = MASKS["BLUE"][115:470, xr[0]:xr[1]]
        ys, xs = np.where(win)
        A = np.vstack([xs, np.ones_like(xs)]).T
        sol, res, _, _ = np.linalg.lstsq(A, ys, rcond=None)
        slope, icpt = sol
        print(f"BLUE LINE {name}: y = {slope:.5f} x + {icpt:.2f}  (n={len(xs)})")
