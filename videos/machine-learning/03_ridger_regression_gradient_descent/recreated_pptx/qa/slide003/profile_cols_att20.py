#!/usr/bin/env python3
"""Column/row ink profiles for slide 003, orig vs render, in 960x540 frame space."""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"

o = np.asarray(Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(QA + "/render_19.png").convert("RGB")
               .resize((960, 540), Image.LANCZOS)).astype(int)


def dark(a):
    return a.min(axis=2) < 110


def yellow(a):
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    return (R > 205) & (G > 205) & (Bc < 200)


def blue(a):
    R, G, Bc = a[..., 0], a[..., 1], a[..., 2]
    return (Bc > 150) & (R < 120) & (G < 150)


do, dr = dark(o), dark(r)
yo, yr = yellow(o), yellow(r)
bo, br = blue(o), blue(r)

print("=== DARK INK column profile, matrix row1 band y366..390 ===")
for x in range(120, 340, 2):
    co = int(do[366:390, x:x + 2].sum())
    cr = int(dr[366:390, x:x + 2].sum())
    if co or cr:
        print(f"  x{x:3d}-{x+1}: orig={co:3d} render={cr:3d}")

print("=== YELLOW BAND x-extent per matrix row band (orig / render) ===")
for label, y0, y1 in (("row1", 366, 390), ("row2", 396, 420),
                      ("row3", 426, 450), ("row4", 456, 480)):
    xo = np.nonzero(yo[y0:y1, :].sum(axis=0) >= 3)[0]
    xr = np.nonzero(yr[y0:y1, :].sum(axis=0) >= 3)[0]
    print(f"  {label}: orig x{ (xo.min(), xo.max()) if len(xo) else None }  "
          f"render x{ (xr.min(), xr.max()) if len(xr) else None }")

print("=== BLUE/BRACKET strokes, columns with blue ink (full matrix area) ===")
for name, m in (("orig", bo), ("render", br)):
    cols = np.nonzero(m[340:500, :].sum(axis=0) >= 3)[0]
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 2:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(f"  {name}: " + ", ".join(f"x{g[0]}-{g[-1]}" for g in groups))

print("=== DARK INK x-groups in matrix row1 band (glyph clusters) ===")
for name, m in (("orig", do), ("render", dr)):
    cols = np.nonzero(m[366:390, :].sum(axis=0) >= 2)[0]
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
    print(f"  {name}: " + ", ".join(f"x{g[0]}-{g[-1]}({sum(1 for c in cols if c in g)})"
                                    for g in groups))
