#!/usr/bin/env python3
"""BR-panel descent-path verification, render_14 vs orig, CORRECT per-image
scales (orig native 1.0x, render 2001/960). Banked pil_verify_a13fix_r14.py
applied the render scale to the orig (empty slices) — its ORIG rows are void."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{V}/recreated_pptx/qa/slide_025"

imgs = {
    "ORIG": (np.asarray(Image.open(f"{V}/unique_slides/slide_025.jpg").convert("RGB")).astype(int), 1.0),
    "REND14": (np.asarray(Image.open(f"{QA}/render_14.png").convert("RGB")).astype(int), 2001 / 960.0),
    "REND13": (np.asarray(Image.open(f"{QA}/render_13.png").convert("RGB")).astype(int), 2001 / 960.0),
}


def zone(a, sc, x0, y0, x1, y1):
    return a[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]


BX0, BY0, BX1, BY1 = 615, 344, 886, 538

for tag, (a, sc) in imgs.items():
    z = zone(a, sc, BX0, BY0, BX1, BY1)
    lum = z.sum(axis=2)
    vdark = lum < 220
    n = int(vdark.sum())
    print(f"=== {tag} BR x{BX0}..{BX1} y{BY0}..{BY1} (scale {sc:.5f}) ===")
    print(f"  very-dark(sum<220): {n} px ({100 * n / lum.size:.3f}%)")
    # ASCII map 48x24 of very-dark density
    H, W = z.shape[:2]
    gh, gw = 24, 48
    grid = np.zeros((gh, gw), dtype=int)
    for gy in range(gh):
        for gx in range(gw):
            cell = vdark[gy * H // gh:(gy + 1) * H // gh, gx * W // gw:(gx + 1) * W // gw]
            grid[gy, gx] = cell.sum()
    thr = max(1, grid.max() // 3)
    chars = "".join("".join("#" if grid[gy, gx] >= thr else ("." if grid[gy, gx] > 0 else " ")
                            for gx in range(gw)) + "\n" for gy in range(gh))
    print(chars)
    # margin bands (axes-free check)
    for btag, (y0, y1) in [("top", (BY0, 372)), ("bottom", (505, BY1))]:
        b = zone(a, sc, BX0, y0, BX1, y1)
        bl = b.sum(axis=2)
        print(f"  {btag}-band y{y0}..{y1} dark(sum<300): {int((bl < 300).sum())}")

# path ink profile along x for ORIG vs REND14 (very-dark columns)
for tag in ("ORIG", "REND14"):
    a, sc = imgs[tag]
    z = zone(a, sc, BX0, BY0, BX1, BY1)
    vdark = (z.sum(axis=2) < 220)
    colprof = vdark.sum(axis=0)
    W = colprof.shape[0]
    quarter = [int(colprof[i * W // 4:(i + 1) * W // 4].sum()) for i in range(4)]
    print(f"{tag}: very-dark per x-quarter {quarter}")
