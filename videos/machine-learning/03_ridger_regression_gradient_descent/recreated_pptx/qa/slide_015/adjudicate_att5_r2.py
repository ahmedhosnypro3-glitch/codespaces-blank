#!/usr/bin/env python3
"""Att5 adjudication round 2 — corrected scalers; claim 1 crops for doc-parse,
claim 3 proper J(W) census, claim 6 precise Best-W color census."""
from PIL import Image
import numpy as np

R = np.asarray(Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/render_4.png').convert('RGB'), dtype=int)
O = np.asarray(Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg').convert('RGB'), dtype=int)
S = 1125 / 540

def lum(img): return img.mean(axis=2)
def red_mask(img):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    return (r > 120) & (r - g > 60) & (r - b > 60)
def green_mask(img):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    return (g > 100) & (g - r > 40) & (g - b > 40)

def frame(img, fx0, fy0, fx1, fy1):
    if img is R:
        return img[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)]
    return img[int(fy0):int(fy1), int(fx0):int(fx1)]

def row_bands(img, fx0, fx1, fy0, fy1, thr=120, minpx=4):
    sub = frame(img, fx0, fy0, fx1, fy1)
    ink = (lum(sub) < thr).sum(axis=1)
    out, inb = [], False
    for i, v in enumerate(ink):
        if v >= minpx and not inb: s = i; inb = True
        elif v < minpx and inb: out.append((fy0 + s/S if img is R else fy0 + s, fy0 + i/S if img is R else fy0 + i)); inb = False
    if inb: out.append((fy0 + s/S if img is R else fy0 + s, fy0 + len(ink)/S if img is R else fy0 + len(ink)))
    return [(round(a,1), round(b,1)) for a, b in out]

def col_clusters(img, fx0, fx1, fy0, fy1, mask, gap=3):
    sub = frame(img, fx0, fy0, fx1, fy1)
    m = mask(sub)
    cols = m.sum(axis=0)
    out, inb, z = [], False, 0
    for i, v in enumerate(cols):
        if v > 0:
            if not inb: s = i; inb = True
            z = 0
        elif inb:
            z += 1
            if z > gap:
                out.append((fx0 + s/S if img is R else fx0 + s, fx0 + (i-z)/S if img is R else fx0 + (i-z))); inb = False
    if inb: out.append((fx0 + s/S if img is R else fx0 + s, fx0 + (len(cols)-1)/S if img is R else fx0 + (len(cols)-1)))
    return [(round(a,1), round(b,1)) for a, b in out]

print("=== CLAIM 3 (J(W) clusters per line, x90..430 = leading J(W) zone) ===")
for name, img in (("ORIG", O), ("REND", R)):
    for li, (fy0, fy1) in enumerate([(100, 160), (160, 216), (216, 270)], 1):
        print(f" {name} L{li} dark rows x90..800:", row_bands(img, 90, 800, fy0, fy1))

print("=== CLAIM 1: locate second '=' in L1, cut right-half crops for doc-parse ===")
# L1 band in frame space: ORIG y~103..160. Column ink to find '=' gaps.
for name, img in (("ORIG", O), ("REND", R)):
    sub = frame(img, 90, 103, 800, 160)
    cols = (lum(sub) < 130).sum(axis=0)
    # print coarse column profile in 20-frame-px bins to locate the second '='
    bins = [int(cols[i:i+int(20*S) if img is R else 20].sum()) for i in range(0, len(cols), int(20*S) if img is R else 20)]
    print(f" {name} L1 col-ink bins (20px): {bins}")

# cut right-half crops (x400..800) of L1 for both, upscale x4, save for doc-parse
for name, img, path in (("orig", O, 'unique_slides/slide_015.jpg'), ("render", R, None)):
    if img is R:
        crop = Image.fromarray(R[int(100*S):int(162*S), int(395*S):int(800*S)].astype(np.uint8))
    else:
        crop = Image.fromarray(O[100:162, 395:800].astype(np.uint8))
    big = crop.resize((crop.width*4, crop.height*4), Image.LANCZOS)
    out = f"videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/att5_L1r_{name}.png"
    big.save(out); print(" saved", out, big.size)

print("=== CLAIM 6: Best-W region — full pink-box text band color census ===")
for name, img in (("ORIG", O), ("REND", R)):
    print(f" {name} pinkbox red col clusters (x76..706, y270..322):", col_clusters(img, 76, 706, 270, 322, red_mask))
    print(f" {name} pinkbox dark col clusters:", len(col_clusters(img, 76, 706, 270, 322, lambda s: lum(s) < 120)))
