#!/usr/bin/env python3
"""Correctly-scaled band profile for render_2 (frame-px coordinates) + fill
color of each full-width band, compared to the original."""
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
QA = NS + "recreated_pptx/qa/slide014/"
RV = np.asarray(Image.open(QA + "render_2.png").convert("RGB")).astype(int)
OG = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
SC = RV.shape[1] / 960.0


def prof(img, scale, label):
    print(f"--- {label} ---")
    nz = (np.abs(img - 255).max(axis=2) > 12)
    state = None
    for y in range(40, 540):
        ry = int(round(y * scale))
        if ry >= img.shape[0]:
            break
        row = nz[ry, :]
        c = int(row.sum())
        s = "BAND" if c > 400 else ("ink" if c > 15 else "empty")
        if s != state:
            cols = np.where(row)[0]
            fx = lambda v: v / scale
            ext = f"x {fx(cols.min()):.1f}..{fx(cols.max()):.1f}" if len(cols) else "-"
            print(f"  y={y:4d} {s:5s} count={c:4d} {ext}")
            state = s


prof(OG, 1.0, "ORIGINAL")
print()
prof(RV, SC, "RENDER_2")

print("\n=== fill color of a text-free horizontal strip per band ===")
def strip(img, scale, y0, y1, x0, x1, label):
    a = img[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)].reshape(-1, 3)
    q = (a // 8) * 8
    keys, counts = np.unique(q, axis=0, return_counts=True)
    top = keys[counts.argmax()] + 4
    print(f"  {label:22s} #{top[0]:02X}{top[1]:02X}{top[2]:02X} ({counts.max()/len(a)*100:.0f}%)")
    return top

print("render:")
strip(RV, SC, 252, 258, 300, 500, "ridge")
strip(RV, SC, 295, 302, 300, 500, "objective")
strip(RV, SC, 386, 396, 300, 500, "define_loss?")
strip(RV, SC, 400, 405, 700, 850, "define_loss right")
strip(RV, SC, 513, 519, 300, 500, "final")
strip(RV, SC, 455, 465, 300, 400, "loss_term_box")
strip(RV, SC, 455, 465, 700, 850, "reg_term_box")
print("original:")
strip(OG, 1.0, 252, 258, 300, 500, "ridge")
strip(OG, 1.0, 295, 302, 300, 500, "objective")
strip(OG, 1.0, 386, 396, 300, 500, "define_loss?")
strip(OG, 1.0, 400, 405, 700, 850, "define_loss right")
strip(OG, 1.0, 513, 519, 300, 500, "final")
strip(OG, 1.0, 455, 465, 300, 400, "loss_term_box")
strip(OG, 1.0, 455, 465, 700, 850, "reg_term_box")

print("\n=== title extent + color split ===")
def title_info(img, scale, label):
    band = img[int(55*scale):int(100*scale), int(60*scale):int(740*scale)]
    nz = (np.abs(band - 255).max(axis=2) > 20)
    rows = np.where(nz.sum(axis=1) > 0)[0]
    cols = np.where(nz.sum(axis=0) > 0)[0]
    blue = (band[:, :, 2] > 100) & (band[:, :, 2] - band[:, :, 0] > 40)
    dark = band.max(axis=2) < 90
    print(f"  {label}: rows 55+{rows.min()/scale:.0f}..55+{rows.max()/scale:.0f} "
          f"(h={ (rows.max()-rows.min())/scale:.0f}px) cols 60+{cols.min()/scale:.0f}..60+{cols.max()/scale:.0f} "
          f"blue={blue.sum()} dark={dark.sum()}")
title_info(OG, 1.0, "original")
title_info(RV, SC, "render_2")
