#!/usr/bin/env python3
"""Round-4 probes + OCR crop preparation for slide025 r26 adjudication."""
import numpy as np
from PIL import Image

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025"
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

rim = Image.open(f"{OUT}/render_cur.png").convert("RGB")
oim = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
r = np.asarray(rim).astype(int)
o = np.asarray(oim.resize((2001, 1125), Image.LANCZOS)).astype(int)
H, W = r.shape[:2]
sx, sy = W / 960.0, H / 540.0


def box(a, x0, y0, x1, y1):
    return a[int(y0 * sy):int(np.ceil(y1 * sy)), int(x0 * sx):int(np.ceil(x1 * sx))]


def is_red(px):
    R, G, B = px[..., 0], px[..., 1], px[..., 2]
    return (R > 140) & (G < 90) & (B < 90) & (R - G > 70)


def sat(px):
    return px.max(axis=2) - px.min(axis=2)


print("== D4 round4: BL surface extent (saturated px bbox) inside BL frame (x90-380, y345-520) ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 90, 345, 380, 520)
    m = sat(sub) > 45
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"  {label}: surface bbox x{90+xs.min()/sx:.0f}-{90+xs.max()/sx:.0f} y{345+ys.min()/sy:.0f}-{345+ys.max()/sy:.0f} sat px {int(m.sum())} ({100.0*m.mean():.1f}% of box)")

print("\n== D6 round4: stricter edge test (nonwhite = any channel <200) BR inner 3px strips ==")
for label, img in [("render", r), ("orig", o)]:
    q = box(img, 560, 340, 900, 535)
    m = is_red(q)
    ys, xs = np.nonzero(m)
    fl, fr = 560 + xs.min() / sx, 560 + xs.max() / sx
    ft, fb = 340 + ys.min() / sy, 340 + ys.max() / sy
    inner = box(img, fl + 2, ft + 2, fr - 2, fb - 2)
    nw = (inner < 200).any(axis=2)
    e = 3
    print(f"  {label}: frame x{fl:.0f}-{fr:.0f} y{ft:.0f}-{fb:.0f} | strict-nonwhite edge strips: top {int(nw[:e].sum())}/{e*inner.shape[1]} bottom {int(nw[-e:].sum())}/{e*inner.shape[1]} left {int(nw[:,:e].sum())}/{e*inner.shape[0]} right {int(nw[:,-e:].sum())}/{e*inner.shape[0]}")

print("\n== D1 round4: TR axes-box top edge + scale annotation row band (x620-720, y120-150), ink per row ==")
for label, img in [("render", r), ("orig", o)]:
    sub = box(img, 620, 120, 720, 150)
    ink = sub.sum(axis=2) < 330
    rows = ink.sum(axis=1)
    print(f"  {label}: ink px {int(ink.sum())}; rows with >3 ink px:", [(round(120+i/sy,1), int(v)) for i, v in enumerate(rows) if v > 3])

print("\n== crop pairs for vision OCR ==")
crops = {
    "r26_cropA_tr_axes": (615, 116, 710, 275),   # TR upper-left axes corner: x10^4 + z ticks
    "r26_cropB_tl_ticks": (80, 115, 140, 300),   # TL left tick labels
}
for name, (x0, y0, x1, y1) in crops.items():
    rc = rim.crop((int(x0 * sx), int(y0 * sy), int(np.ceil(x1 * sx)), int(np.ceil(y1 * sy))))
    oc = oim.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(f"{OUT}/{name}_render.png")
    oc.save(f"{OUT}/{name}_orig.png")
    print(f"  {name}: render {rc.size} orig {oc.size} (region x{x0}-{x1} y{y0}-{y1})")
