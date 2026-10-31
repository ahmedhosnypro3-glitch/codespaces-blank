#!/usr/bin/env python3
"""b17 closed-loop PIL check for slides 33/34.
Original frame is 960x540 px; render is 150dpi of a 13.33x7.5in slide (2001x1125).
Scale render px -> frame px by *72/150. Tolerance: 4 render px (approx 1.9 frame px).
Checks: red structural rectangles, badge circle, node circle centres.
"""
import sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TOL = 4.0 / 150 * 72  # px in frame coords


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


def red_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 110) & (r - g > 55) & (r - b > 55)


def rect_profiles(mask, min_frac=0.25):
    """Return long horizontal and vertical red runs -> rectangle borders."""
    h, w = mask.shape
    rows = []
    for y in range(h):
        xs = np.flatnonzero(mask[y])
        if xs.size < min_frac * w:
            continue
        runs, st = [], xs[0]
        for i in range(1, xs.size):
            if xs[i] != xs[i - 1] + 1:
                runs.append((st, xs[i - 1])); st = xs[i]
        runs.append((st, xs[-1]))
        runs = [(s, e) for s, e in runs if e - s > min_frac * w]
        if runs:
            rows.append(y)
    cols = []
    for x in range(w):
        ys = np.flatnonzero(mask[:, x])
        if ys.size < min_frac * h * 0.4:
            continue
        cols.append(x)
    return rows, cols


def group(vals, gap=3):
    out = []
    for v in sorted(vals):
        if out and v - out[-1][-1] <= gap:
            out[-1].append(v)
        else:
            out.append([v])
    return [int(round(float(np.mean(g)))) for g in out]


def circles(a, target, tol=40):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (np.abs(r - target[0]) < tol) & (np.abs(g - target[1]) < tol) & (np.abs(b - target[2]) < tol)
    ys, xs = np.nonzero(m)
    pts = {}
    for y, x in zip(ys, xs):
        k = (x // 6, y // 6)
        pts.setdefault(k, []).append((x, y))
    out = []
    for v in pts.values():
        if len(v) < 60:
            continue
        xs2 = [p[0] for p in v]; ys2 = [p[1] for p in v]
        w = max(xs2) - min(xs2); h = max(ys2) - min(ys2)
        if 6 <= w <= 60 and 6 <= h <= 60 and abs(w - h) <= max(6, w * 0.5):
            out.append((sum(xs2) / len(xs2), sum(ys2) / len(ys2), w))
    return out


def merge(cs, d=14):
    used = [False] * len(cs)
    out = []
    for i, c in enumerate(cs):
        if used[i]:
            continue
        ax, ay, aw = c
        pts = [(ax, ay, aw)]
        for j in range(i + 1, len(cs)):
            if used[j]:
                continue
            if abs(cs[j][0] - ax) < d and abs(cs[j][1] - ay) < d:
                used[j] = True
                pts.append(cs[j])
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; ws = [p[2] for p in pts]
        out.append((float(np.mean(xs)), float(np.mean(ys)), float(np.mean(ws))))
    return out


def frame_px(render_shape):
    return render_shape[1] * 72 / 150


def check(n):
    n = str(n).zfill(3)
    orig = load(f"{NS}/unique_slides/slide_{n}.jpg")
    ren = load(f"{NS}/qa/slide{n}/rejudge/render-1.png")
    sc = frame_px(ren.shape) / orig.shape[1]  # frame px -> render px
    print(f"===== slide {n}: orig {orig.shape[1]}x{orig.shape[0]} render {ren.shape[1]}x{ren.shape[0]} scale={sc:.4f} tol={TOL:.2f} frame px")
    ok = True

    # --- red rectangles: borders as row/col bands, scaled back to frame px
    for tag, img in (("orig", orig), ("render", ren)):
        m = red_mask(img)
        rows, cols = rect_profiles(m)
        r_b = group([r for r in rows])
        c_b = group([c for c in cols])
        k = 72 / 150 if tag == "render" else 1.0
        print(f" [{tag}] red row-bands(frame px): {r_b}")
        print(f" [{tag}] red col-bands(frame px): {c_b}")

    # --- node circles by fill colour
    for tag, target in (("yellow", (255, 249, 196)), ("orange", (255, 165, 0))):
        o = merge(circles(orig, target) + circles(orig, target, 60))
        r_ = merge(circles(ren, target) + circles(ren, target, 60))
        r_ = [(x / sc, y / sc, w / sc) for x, y, w in r_]
        print(f" [{tag}] orig circles: {[(round(x), round(y), round(w)) for x, y, w in o]}")
        print(f" [{tag}] rend circles: {[(round(x), round(y), round(w)) for x, y, w in r_]}")
        for oc in o:
            if not r_:
                print(f"    !! no render {tag} circle for orig {oc[0]:.0f},{oc[1]:.0f}")
                ok = False
                continue
            best = min(r_, key=lambda rc: (rc[0] - oc[0]) ** 2 + (rc[1] - oc[1]) ** 2)
            d = ((best[0] - oc[0]) ** 2 + (best[1] - oc[1]) ** 2) ** 0.5
            flag = "OK " if (d <= TOL and abs(best[2] - oc[2]) <= TOL * 1.5) else "BAD"
            if flag == "BAD":
                ok = False
            print(f"    {flag} orig({oc[0]:.0f},{oc[1]:.0f},d{oc[2]:.0f}) vs rend({best[0]:.0f},{best[1]:.0f},d{best[2]:.0f}) delta={d:.2f}px")
    print(f" RESULT slide {n}: {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    for n in sys.argv[1:]:
        check(n)
