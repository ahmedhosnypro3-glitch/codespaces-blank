#!/usr/bin/env python3
"""Adjudication harness for slide 044 legs (worker-slide044-legs2, 2026-10-24).

PIL-first adjudication of candidate judge findings against BOTH images.
Frame space 960x540, 1px=1pt. render_2.png downscaled to frame via LANCZOS
(matches Procedure B matched-scale approach). Phantom-measurement trap
enforced: a column/row counts as inked only with >=3 ink px.

Measures the pre-banked §9 claims so any FAIL/MINOR the judge raises is settled
with numbers, not vibes:
  - calc-area background median (confirm WHITE fix present on render_2)
  - per-band equation ink extents b1..b6 (orig vs render) -> ground-rule (e)
  - "Check classes of" ink y-range (typed-vs-handwritten <=3px)
  - class rule line x-extent (orig x508 vs render x492)
  - Initial-W bracket stack y-extent (orig y62..100 vs render y56..102)
  - red "Iteration 3" badge block + white glyph ink
"""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"

rim = np.asarray(Image.open(f"{QA}/render_2.png").convert("RGB")).astype(int)
oim = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
rim_f = np.asarray(Image.fromarray(rim.astype(np.uint8)).resize((960, 540), Image.LANCZOS)).astype(int)
print(f"render_2 {rim.shape[1]}x{rim.shape[0]} scale={rim.shape[1]/960:.4f} | orig {oim.shape[1]}x{oim.shape[0]}")


def inkbox(arr, y0, y1, x0, x1, dark_sum=420):
    """dark-ink bbox inside a region, phantom-safe (>=3 ink px per row/col)."""
    dark = (arr[y0:y1, x0:x1].sum(axis=2) < dark_sum)
    rc = dark.sum(axis=1)
    cc = dark.sum(axis=0)
    rows = [y0 + i for i, v in enumerate(rc) if v >= 3]
    cols = [x0 + i for i, v in enumerate(cc) if v >= 3]
    if not rows or not cols:
        return None
    return dict(x0=min(cols), x1=max(cols), y0=min(rows), y1=max(rows),
                ink=int(dark.sum()))


def med(arr, y0, y1, x0, x1):
    reg = arr[y0:y1, x0:x1].reshape(-1, 3)
    return tuple(int(np.median(reg[:, c])) for c in range(3))


print("\n== calc-area background medians (orig white ~254; v1 grey 233 was DEFECT, render_2 must be ~255) ==")
for name, arr in [("orig", oim), ("render_2", rim_f)]:
    print(f"[{name}] y150={med(arr,150,151,285,845)} y250={med(arr,250,251,285,845)} "
          f"y420={med(arr,420,421,285,845)} y500={med(arr,500,501,285,845)}")

print("\n== per-band equation ink extents in calc area (render narrower on right = ground-rule (e) 2D format) ==")
BANDS = {"b1": (145, 197), "b2": (209, 263), "b3": (274, 336), "b4": (342, 393), "b5": (407, 459), "b6": (474, 525)}
for name, arr in [("orig", oim), ("render_2", rim_f)]:
    row = []
    for b, (y0, y1) in BANDS.items():
        bb = inkbox(arr, y0, y1, 276, 851)
        row.append(f"{b}:x{bb['x0']}..{bb['x1']}" if bb else f"{b}:EMPTY")
    print(f"[{name}] " + "  ".join(row))

print("\n== 'Check classes of' black ink (typed-vs-handwritten; <=3px y-shift = MINOR (d)) ==")
for name, arr in [("orig", oim), ("render_2", rim_f)]:
    bb = inkbox(arr, 74, 96, 490, 592)
    print(f"[{name}] {bb}")

print("\n== class rule line extent (orig x508 vs render x492) ==")
for name, arr in [("orig", oim), ("render_2", rim_f)]:
    bb = inkbox(arr, 110, 128, 230, 520)
    print(f"[{name}] {bb}")

print("\n== Initial-W bracket stack (orig y62..100 vs render y56..102) ==")
for name, arr in [("orig", oim), ("render_2", rim_f)]:
    bb = inkbox(arr, 50, 110, 328, 360)
    print(f"[{name}] {bb}")

print("\n== red 'Iteration 3' badge (red block + white glyph ink inside) ==")
for name, arr in [("orig", oim), ("render_2", rim_f)]:
    red = (arr[:, :, 0] > 170) & (arr[:, :, 1] < 90) & (arr[:, :, 2] < 90)
    sub = red[275:308, 82:216]
    ys, xs = np.where(sub)
    blk = f"red bbox x{xs.min() if len(xs) else '-'}..{xs.max() if len(xs) else '-'} " \
          f"y{ys.min() if len(ys) else '-'}..{ys.max() if len(ys) else '-'} px={len(xs)}" if len(xs) else "none"
    # white glyphs inside the red block
    inner = (arr[277:306, 84:214].sum(axis=2) > 720)
    wy, wx = np.where(inner)
    gb = f"white-glyph x{wx.min() if len(wx) else '-'}..{wx.max() if len(wx) else '-'} " \
         f"y{wy.min() if len(wy) else '-'}..{wy.max() if len(wy) else '-'} px={len(wx)}" if len(wx) else "none"
    print(f"[{name}] {blk} | {gb}")

print("\ndone")
