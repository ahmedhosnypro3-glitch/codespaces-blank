#!/usr/bin/env python3
"""fresh3 FULL FAIL probe for slide015: measure (a) top eq-stack line pitch,
(b) deriv-block line positions, (c) LHS first-glyph hook on eq1 l1/l2,
(d) red Get-Best-W box + Remember box geometry — orig vs render, slide-space."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide015"
r = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_015.jpg").convert("RGB")).astype(int)
sc = r.shape[1] / 960.0

def lines(a, x0, x1, y0, y1, thr=600):
    s = a.shape[1] / 960.0
    sub = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    ink = sub.sum(axis=2) < thr
    rows = ink.sum(axis=1)
    out, inb = [], False
    for i, v in enumerate(rows):
        if v >= 3 and not inb:
            st = i; inb = True
        elif v < 3 and inb:
            out.append((y0 + st / s, y0 + i / s, int(rows[st:i].sum()))); inb = False
    if inb:
        out.append((y0 + st / s, y0 + len(rows) / s, int(rows[st:].sum())))
    return out

print("== (a) top eq stack text lines, x85-894, y100-270 ==")
for name, a in (("orig", o), ("render", r)):
    ls = lines(a, 85, 894, 100, 270)
    print(name, " ".join(f"y{t:.1f}-{b:.1f}(ink{i})" for t, b, i in ls))

print("== (b) lower block lines, x60-900, y270-540 ==")
for name, a in (("orig", o), ("render", r)):
    ls = lines(a, 60, 900, 270, 540)
    print(name, " ".join(f"y{t:.1f}-{b:.1f}(ink{i})" for t, b, i in ls))

print("== (c) eq1 LHS first glyph, band y106-152 (render) / y109-152 (orig), x85-130 ==")
for name, a, y0, y1 in (("orig", o, 109, 152), ("render", r, 106, 152)):
    s = a.shape[1] / 960.0
    sub = a[int(y0 * s):int(y1 * s), int(85 * s):int(130 * s)]
    ink = sub.sum(axis=2) < 600
    print(f"{name} ink={int(ink.sum())} rows:", "".join("#" if v >= 2 else ("+" if v else ".") for v in ink.sum(axis=1)))
    print(f"{name} cols:", "".join("#" if v >= 2 else ("+" if v else ".") for v in ink.sum(axis=0)))

print("== (d) red-box geometry: red-dominant px per row band y150-260, x60-900 ==")
for name, a in (("orig", o), ("render", r)):
    s = a.shape[1] / 960.0
    sub = a[int(150 * s):int(260 * s), int(60 * s):int(900 * s)]
    red = (sub[:, :, 0] > 120) & (sub[:, :, 0] > sub[:, :, 1] + 60) & (sub[:, :, 0] > sub[:, :, 2] + 60)
    cols = red.sum(axis=0)
    xs = np.where(cols > 2)[0]
    if len(xs):
        print(f"{name} red cols x{60 + xs.min()/s:.1f}-{60 + xs.max()/s:.1f} total={int(red.sum())}")
    else:
        print(f"{name} no red")
# Remember box: look for its border (dark) x-extent in band y150-230
for name, a in (("orig", o), ("render", r)):
    s = a.shape[1] / 960.0
    sub = a[int(150 * s):int(230 * s), int(600 * s):int(900 * s)]
    dark = sub.sum(axis=2) < 450
    cols = dark.sum(axis=0)
    xs = np.where(cols > 20)[0]
    if len(xs):
        print(f"{name} Remember-box verticals x{600 + xs.min()/s:.1f}-{600 + xs.max()/s:.1f}")
