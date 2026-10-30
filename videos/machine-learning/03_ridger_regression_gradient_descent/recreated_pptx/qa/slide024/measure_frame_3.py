#!/usr/bin/env python3
"""Measure pass 3 for slide_024.jpg: font weight/size pinning by row-profile
simulation. Renders each candidate (Liberation Sans Bold/Regular at candidate
sizes) in C00000 on E9E9E7 with a JPEG-like blur, applies the SAME red mask
used on the original, and scores band bbox + per-row counts + total ink
against the measured original profiles. Also prints Liberation metric ratios.
"""
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_024.jpg"
ori = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

RED_INK = (192, 0, 0)       # C00000 nominal
BG = (231, 233, 230)        # E9E9E7

def red_mask(a):
    return (a[:, :, 0] > 90) & ((a[:, :, 0] - a[:, :, 1]) > 40) & ((a[:, :, 0] - a[:, :, 2]) > 10)

def profile_of(mask):
    rows = mask.sum(axis=1)
    cols = mask.sum(axis=0)
    rr = np.where(rows > 0)[0]
    cc = np.where(cols > 0)[0]
    if not len(rr):
        return None
    return {
        "y0": int(rr.min()), "y1": int(rr.max()), "x0": int(cc.min()), "x1": int(cc.max()),
        "h": int(rr.max() - rr.min() + 1), "w": int(cc.max() - cc.min() + 1),
        "peak": int(rows.max()), "total": int(mask.sum()), "rows": rows.tolist(),
    }

def render_text(text, fontpath, size, blur=0.55):
    f = ImageFont.truetype(fontpath, size)
    # big canvas, draw at margin
    img = Image.new("RGB", (1400, 400), BG)
    d = ImageDraw.Draw(img)
    d.text((100, 100), text, font=f, fill=RED_INK)
    img = img.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(img).astype(int)
    m = red_mask(a)
    return profile_of(m)

# ---- measured originals (from measure_frame.py / measure_frame_2.py) -------
# crop each band from the original, mask, profile — identical predicate both sides
MEAS = {}
for label, (ya, yb, xa, xb) in {
    "T": (215, 280, 100, 900), "S1": (285, 330, 100, 900), "S2": (340, 390, 100, 900),
}.items():
    m = red_mask(ori[ya:yb, xa:xb])
    p = profile_of(m)
    p["y0"] += ya; p["y1"] += ya; p["x0"] += xa; p["x1"] += xa
    MEAS[label] = p
    print(f"measured {label}: x {p['x0']}..{p['x1']} (w {p['w']})  y {p['y0']}..{p['y1']} (h {p['h']})  peak {p['peak']}  total {p['total']}")

TEXTS = {"T": "Gradient Descent (GD)", "S1": "and", "S2": "How to apply to minimize Loss function"}
FONTS = {
    "Bold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "Regular": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
}
SIZES = {"T": range(40, 50), "S1": range(29, 37), "S2": range(28, 36)}

def score(meas, sim):
    s = 0.0
    s += abs(sim["w"] - meas["w"]) * 2.0
    s += abs(sim["h"] - meas["h"]) * 1.0
    s += abs(sim["peak"] - meas["peak"]) / 12.0
    s += abs(sim["total"] - meas["total"]) / 60.0
    return s

print("\n=== simulation scores (lower = better) ===")
best = {}
for lab in ("T", "S1", "S2"):
    print(f"\n--- {lab}: '{TEXTS[lab]}' ---")
    rows = []
    for wname, fp in FONTS.items():
        for size in SIZES[lab]:
            sim = render_text(TEXTS[lab], fp, size)
            sc = score(MEAS[lab], sim)
            rows.append((sc, wname, size, sim))
    rows.sort(key=lambda r: r[0])
    for sc, wname, size, sim in rows[:5]:
        print(f"  {wname} {size}pt: score {sc:.2f}  sim w={sim['w']} h={sim['h']} peak={sim['peak']} total={sim['total']}"
              f"  (meas w={MEAS[lab]['w']} h={MEAS[lab]['h']} peak={MEAS[lab]['peak']} total={MEAS[lab]['total']})")
    best[lab] = rows[0]

print("\nbest:", {k: (v[1], v[2]) for k, v in best.items()})

print("\n=== Liberation glyph metric ratios (em=100) ===")
for wname, fp in FONTS.items():
    f33 = ImageFont.truetype(fp, 100)
    for ch in ("x", "H", "d"):
        bb = f33.getbbox(ch)
        print(f"{wname} '{ch}': bbox {bb}")
