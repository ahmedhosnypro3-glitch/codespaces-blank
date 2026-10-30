#!/usr/bin/env python3
"""Att5 adjudication round 3 — robust thresholds (handwriting is lighter in the
JPEG original); pink-box interior-only color census; word-level Best-W scan."""
from PIL import Image
import numpy as np

R = np.asarray(Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/render_4.png').convert('RGB'), dtype=int)
O = np.asarray(Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg').convert('RGB'), dtype=int)
S = 1125 / 540

def lum(img): return img.mean(axis=2)
def red_mask(img):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def frame(img, fx0, fy0, fx1, fy1):
    if img is R:
        return img[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)]
    return img[int(fy0):int(fy1), int(fx0):int(fx1)]

def clusters(mask_2d, fx0, scale, gap):
    cols = mask_2d.sum(axis=0)
    out, inb, z = [], False, 0
    for i, v in enumerate(cols):
        if v > 0:
            if not inb: s = i; inb = True
            z = 0
        elif inb:
            z += 1
            if z > gap: out.append((s, i - z)); inb = False
    if inb: out.append((s, len(cols) - 1))
    return [(round(fx0 + a/scale, 1), round(fx0 + b/scale, 1)) for a, b in out]

print("=== L1 column ink, luma<200 (handwriting-robust), 20-frame-px bins ===")
for name, img in (("ORIG", O), ("REND", R)):
    sub = frame(img, 90, 103, 800, 160)
    cols = (lum(sub) < 200).sum(axis=0)
    step = max(1, int(20 * S)) if img is R else 20
    bins = [int(cols[i:i+step].sum()) for i in range(0, len(cols), step)]
    print(f" {name}: {bins}")

print("=== CLAIM 6: pink-box INTERIOR (x80..700, y277..315) ===")
for name, img in (("ORIG", O), ("REND", R)):
    sub = frame(img, 80, 277, 700, 315)
    dark = lum(sub) < 170
    red = red_mask(sub)
    print(f" {name}: dark px={int(dark.sum())} red px={int(red.sum())}")
    # word clusters from dark text, then red/dark split per word
    words = clusters(dark, 80, S if img is R else 1.0, gap=int(6*S) if img is R else 6)
    reds = clusters(red, 80, S if img is R else 1.0, gap=int(6*S) if img is R else 6)
    print(f" {name} dark word clusters: {words}")
    print(f" {name} red clusters: {reds}")

print("=== L1-right doc-parse crops (rebuilt at matched crop scale) ===")
# Same output size for both: frame x395..800 y100..162 at 4x frame scale
o_crop = Image.fromarray(O[100:162, 395:800].astype(np.uint8)).resize(((800-395)*4, (162-100)*4), Image.LANCZOS)
r_crop = Image.fromarray(R[int(100*S):int(162*S), int(395*S):int(800*S)].astype(np.uint8)).resize(((800-395)*4, (162-100)*4), Image.LANCZOS)
o_crop.save('videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/att5_L1r_orig.png')
r_crop.save('videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/att5_L1r_render.png')
print(" saved matched-size crops:", o_crop.size, r_crop.size)
