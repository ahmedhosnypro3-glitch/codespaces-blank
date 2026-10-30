#!/usr/bin/env python3
"""Verify att13 fixes landed in render_14 (k13 bytes) PIL-first, and test
region pixel-identity for banked crop certificates."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{V}/recreated_pptx/qa/slide_025"
S = 2001 / 960.0

imgs = {
    "ORIG":    np.asarray(Image.open(f"{V}/unique_slides/slide_025.jpg").convert("RGB")).astype(int),
    "REND14":  np.asarray(Image.open(f"{QA}/render_14.png").convert("RGB")).astype(int),
    "REND13":  np.asarray(Image.open(f"{QA}/render_13.png").convert("RGB")).astype(int),
    "REND12":  np.asarray(Image.open(f"{QA}/render_12.png").convert("RGB")).astype(int),
}

def zone(a, x0, y0, x1, y1):
    return a[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]

def darkink(z):
    return z.sum(axis=2) < 300

print("=== 1. BR descent path: dark-ink volume x615..886 y344..538 ===")
for tag in ("ORIG", "REND13", "REND14"):
    z = zone(imgs[tag], 615, 344, 886, 538)
    d = darkink(z)
    print(f"  {tag}: total dark {int(d.sum()):6d}  ({100*d.mean():.2f}% of region)")

print("=== 2. BR axes-free check: dark ink in BR margin bands (outside surface) ===")
for tag in ("ORIG", "REND14"):
    top = zone(imgs[tag], 615, 344, 886, 372)
    bot = zone(imgs[tag], 615, 505, 886, 538)
    print(f"  {tag}: top-band dark {int(darkink(top).sum()):5d}  bottom-band dark {int(darkink(bot).sum()):5d}")

print("=== 3. BL bottom band: dark tick ink vs red border (y495..535, x83..383) ===")
for tag in ("ORIG", "REND13", "REND14"):
    z = zone(imgs[tag], 83, 495, 383, 535)
    d = darkink(z)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    red = (r > 110) & (r - g > 55) & (r - b > 55)
    prof_d, prof_r = d.sum(axis=1), red.sum(axis=1)
    rows = [(495 + i / S, int(prof_d[i]), int(prof_r[i])) for i in range(0, z.shape[0], 2)
            if prof_d[i] > 3 or prof_r[i] > 3]
    print(f"  -- {tag}: bottommost dark-ink row y={max((r0 for r0, _, _ in rows), default=None)}")
    for y0, dd, rr in rows[-4:]:
        print(f"     y{y0:6.1f}  dark {dd:4d}  red {rr:4d}")

print("=== 4. region pixel-identity for banked certificates ===")
def ident(tagA, tagB, x0, y0, x1, y1):
    a = zone(imgs[tagA], x0, y0, x1, y1).astype(int)
    b = zone(imgs[tagB], x0, y0, x1, y1).astype(int)
    if a.shape != b.shape:
        print(f"  {tagA} vs {tagB} {x0,y0,x1,y1}: SHAPE {a.shape} vs {b.shape}")
        return
    diff = np.abs(a - b).max(axis=2)
    print(f"  {tagA} vs {tagB} frame x{x0}..{x1} y{y0}..{y1}: maxdiff={diff.max()}  npix>8: {int((diff > 8).sum())} ({100*(diff>8).mean():.3f}%)")

print(" -- TL/TR (crop_12 certs on REND12; k13 claims unchanged) --")
ident("REND12", "REND14", 60, 110, 470, 292)
ident("REND12", "REND14", 472, 110, 901, 320)
print(" -- title + label boxes (crop_9 certs on REND9) --")
imgs["REND9"] = np.asarray(Image.open(f"{QA}/../slide025/render_9.png").convert("RGB")).astype(int) if False else imgs["REND14"]
try:
    imgs["REND9"] = np.asarray(Image.open(f"{QA}/render_9.png").convert("RGB")).astype(int)
    ident("REND9", "REND14", 58, 45, 904, 110)
    ident("REND9", "REND14", 266, 133, 412, 182)
    ident("REND9", "REND14", 470, 180, 616, 229)
    ident("REND9", "REND14", 470, 350, 616, 395)
    ident("REND9", "REND14", 378, 448, 522, 493)
except FileNotFoundError as e:
    print("  render_9 missing:", e)
