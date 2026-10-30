#!/usr/bin/env python3
"""Pre-judge self-check, slide 029, DELIVERABLE render (render_2.png) — v2 checker.

Supersedes the inline 1b probe (which reported window-relative x columns as
absolute: cx bug) and selfcheck_attempt_1.py's naive band-edge tolerance (which
ignored the ORIGINAL-only JPEG halo). Same sensitive-ink predicate on BOTH
images; halo-aware tolerances with the rationale:

  - d_base (x-height-core bottom vs baseline): PRIMARY vertical anchor,
    halo-robust (descender-only rows excluded by the 30%-of-max core cut).
    tol 1.5 frame px.
  - d_top: the original's band TOP carries ~1.5-2px JPEG halo above the true
    ascender tips (rows y191-192 hold only 12-44 px on L1); the render's clean
    AA shows true tips. Accept d_top in [-1, +3.5].
  - d_bot / x-edges / cx / width: original edges are halo-inflated by
    ~1-2px/side; render-vs-orig band deltas should stay within 2.5-3 px with
    the render slightly INSIDE the original's halo shell.
"""
import numpy as np
from PIL import Image

REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide029/render_2.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_029.jpg"
# name, text, y-window, x-window (slide-space), target cx, target ink w (banked)
LINES = [
    ("L1", "Example: Obtain Minimum Value", (185, 245), (130, 830), 480.5, 688),
    ("L2", "of a function using",          (263, 323), (260, 675), 467.0, 397),
    ("L3", "Gradient Descent (GD)",        (341, 400), (228, 718), 473.0, 477),
]


def band(path, wy, wx):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    sc = im.shape[0] / 540.0
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    dist = np.sqrt((r - 231) ** 2 + (g - 233) ** 2 + (b - 230) ** 2)
    ink = dist > 40
    y0, y1 = int(wy[0] * sc), int(wy[1] * sc)
    x0, x1 = int(wx[0] * sc), int(wx[1] * sc)
    seg = ink[y0:y1, x0:x1]
    p = seg.sum(axis=1).astype(float)
    ys = np.arange(len(p)) / sc + wy[0]
    mx = p.max()
    core = p > 0.30 * mx           # x-height core cut: excludes descender rows
    colhas = seg.any(axis=0)
    xs = np.where(colhas)[0]
    inkx0 = wx[0] + xs.min() / sc      # window-relative -> slide-absolute
    inkx1 = wx[0] + (xs.max() + 1) / sc
    any_ = p > 0
    return ys[any_].min(), ys[core].max(), ys[any_].max(), inkx0, inkx1


fails = []
print(f"render: {REND.split('/')[-1]}  |  targets: banked measurement (measure_rows_output.txt)")
print("line | d_base | d_top(halo-aware) | d_bot | d_x0 | d_x1 | cx | cx_delta | w | w_delta")
prev_top = None
for name, txt, wy, wx, tcx, tw in LINES:
    ot, ob, obot, ox0, ox1 = band(ORIG, wy, wx)
    rt, rb, rbot, rx0, rx1 = band(REND, wy, wx)
    cx = (rx0 + rx1) / 2
    d_base, d_top, d_bot = rb - ob, rt - ot, rbot - obot
    pitch = (rt - prev_top) if prev_top is not None else float("nan")
    prev_top = rt
    print(f"{name}: d_base={d_base:+.2f} d_top={d_top:+.2f} d_bot={d_bot:+.2f} "
          f"d_x0={rx0 - ox0:+.2f} d_x1={rx1 - ox1:+.2f} cx={cx:.1f} (d={cx - tcx:+.2f}) "
          f"w={rx1 - rx0:.1f} (d={rx1 - rx0 - tw:+.1f}) top-pitch={pitch:.2f}")
    if abs(d_base) > 1.5:
        fails.append(f"{name} baseline delta {d_base:+.2f} > 1.5")
    if d_top > 3.5 or d_top < -1.0:
        fails.append(f"{name} top delta {d_top:+.2f} outside [-1, +3.5] (halo-aware)")
    if abs(d_bot) > 2.0:
        fails.append(f"{name} bottom delta {d_bot:+.2f} > 2.0")
    if abs(rx0 - ox0) > 3.5 or abs(rx1 - ox1) > 3.5:
        # 3.5: thin end glyphs (L3's ')') carry up to ~3px JPEG halo on the
        # original; the render's clean AA edge sits inside the halo shell.
        fails.append(f"{name} x-edge delta > 3.5")
    if abs(cx - tcx) > 2.5:
        fails.append(f"{name} cx delta {cx - tcx:+.2f} > 2.5")
    if abs((rx1 - rx0) - tw) > 5.0:
        fails.append(f"{name} width delta {(rx1 - rx0) - tw:+.1f} > 5 (halo ~2px/side)")
    if not np.isnan(pitch) and abs(pitch - 78.0) > 1.0:
        fails.append(f"{name} pitch {pitch:.2f} != 78")

# extra-band scan: no ink anywhere else in the panel interior (wrap/stray check)
im = np.asarray(Image.open(REND).convert("RGB")).astype(int)
sc = im.shape[0] / 540.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
dist = np.sqrt((r - 231) ** 2 + (g - 233) ** 2 + (b - 230) ** 2)
ink = dist > 40
ink[:, : int(75 * sc)] = False
ink[:, int(885 * sc):] = False
ink[: int(100 * sc), :] = False          # exclude badge band (55-93)
ink[int(410 * sc):, :] = False            # below L3 descenders
mid = ink.sum(axis=1)
stray = np.where(mid > 3)[0]
print(f"\nstray-ink rows between badge band and L3 bottom (100..410 frame px): "
      f"{[f'{y / sc:.0f}' for y in stray][:20]} (outside the 3 expected bands?)")
# expected: rows inside the three line windows only
inband = np.zeros(len(mid), bool)
for name, txt, wy, wx, a, c in LINES:
    inband[int(wy[0] * sc):int(wy[1] * sc)] = True
out_rows = [y for y in stray if not inband[y]]
if out_rows:
    fails.append(f"stray ink rows outside bands: {[f'{y / sc:.0f}' for y in out_rows][:10]}")
else:
    print("no stray ink outside the three title bands + badge (wrap check clean)")

print("\nSELF-CHECK (deliverable render_2): " + ("FAIL" if fails else "PASS"))
for f in fails:
    print("  -", f)
