#!/usr/bin/env python3
"""Refined slide_016 measurement: separate title red (#C00000) from frame red
(#8B0000), locate blue spans, badge, bottom strip, and report bboxes/cap heights.
"""
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"
REND = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_016_rendered-1.png"
OLD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/qa/slide016/render_4.png"


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


def masks(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    bg = (abs(r - 234) < 10) & (abs(g - 234) < 10) & (abs(b - 234) < 10)
    strong_red = (r > 165) & (g < 90) & (b < 90) & (r - g > 100) & (r - b > 100)
    frame_red = (r >= 100) & (r <= 165) & (g < 80) & (b < 80) & (r - g > 70)
    blue = (b > 90) & (b - r > 60) & (b - g > 60)
    black = (mx < 110)
    yellow = (r > 190) & (g > 165) & (b < 160) & (r - b > 55)
    return dict(bg=bg, strong_red=strong_red, frame_red=frame_red, blue=blue,
                black=black, yellow=yellow)


def bands(m, key, x0=0, x1=None, minpx=2):
    msk = m[key]
    h, w = msk.shape
    x1 = w if x1 is None else x1
    sub = msk[:, x0:x1]
    rows = [y for y in range(h) if int(sub[y].sum()) >= minpx]
    out = []
    if not rows:
        return out
    start = prev = rows[0]
    for y in rows[1:]:
        if y == prev + 1:
            prev = y
        else:
            out.append((start, prev))
            start = prev = y
    out.append((start, prev))
    return out


def bbox(m, key, y0, y1, x0=0, x1=None):
    msk = m[key]
    h, w = msk.shape
    x1 = w if x1 is None else x1
    sub = msk[y0:y1 + 1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        return None
    return (x0 + int(xs.min()), x0 + int(xs.max()), y0 + int(ys.min()), y0 + int(ys.max()))


def report(path, label, x0, x1):
    a = load(path)
    h, w = a.shape[:2]
    m = masks(a)
    print(f"\n=========== {label}  ({w}x{h})  interior x[{x0},{x1}] ===========")
    for key in ("strong_red", "blue", "black"):
        bs = bands(m, key, x0, x1)
        print(f"\n {key}: {len(bs)} bands")
        for (a0, b0) in bs:
            bb = bbox(m, key, a0, b0, x0, x1)
            print(f"   rows {a0}-{b0} (h={b0-a0+1})  x {bb[0]}-{bb[1]} (w={bb[1]-bb[0]+1})"
                  f"   inches y {a0/h*7.5:.2f}-{(b0+1)/h*7.5:.2f} x {bb[0]/w*13.33:.2f}-{(bb[1]+1)/w*13.33:.2f}")
    fr = bands(m, "frame_red", x0, x1)
    print(f"\n frame_red bands (interior): {fr[:6]}")
    # full-width frame detection (columns near edges)
    print("\n border check:")
    for name, key in (("top border", "frame_red"),):
        pass
    ys, xs = np.where(m["black"])
    if len(ys):
        # bottom strip rows
        rowcnt = [(y, int(m["black"][y].sum())) for y in range(h - 1, -1, -1)]
        strip = [y for y, c in rowcnt if c > w * 0.8]
        if strip:
            print(f"  bottom black strip rows {max(strip)}-{min(strip)} (h={min(strip)-max(strip)+1}, "
                  f"in {max(strip)/h*7.5:.2f}-{min(strip)/h*7.5:.2f})")
    ym = m["yellow"]
    ys, xs = np.where(ym)
    if len(xs):
        print(f"  yellow badge bbox: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} "
              f"(w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1}) inches x {xs.min()/w*13.33:.2f}-{xs.max()/w*13.33:.2f}")
    else:
        print("  yellow badge: NONE in this image")


report(ORIG, "ORIGINAL slide_016.jpg", 20, 940)
report(OLD, "BANKED render_4.png (judged by prior PASS)", 30, 1970)
report(REND, "FRESH render of delivered pptx", 30, 1970)
