#!/usr/bin/env python3
"""Pre-judge self-check, slide 029 attempt 1 (mandatory checklist, 17_worker_instructions.md).

Closed-loop PIL comparison of the 150dpi render against the ORIGINAL frame's
banked measurements (measure_rows_output.txt), using the SAME sensitive-ink
predicate on both images so JPEG-halo-vs-clean-AA differences cancel.

Checks:
  1. exactly THREE title bands in the panel interior (no wrap spill, no extra ink)
  2. per-band y0/y1/x0/x1/cx vs targets (frame px, tolerance 3 frame px)
  3. band pitch == 78 frame px
  4. LINE/BOX WRAP: no ink outside the three expected bands + badge + chrome
  5. FRAME CONTAINMENT: title ink well inside the panel, clear of strokes
  6. badge numeral ink present
  7. one-band-per-element (each line renders as a single band, not split)
"""
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide029/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_029.jpg"

# targets: frame px from the ORIGINAL's banked measurement (measure_rows_output.txt)
TARGET = [
    dict(name="L1", y0=191, y1=236, x0=137, x1=824, cx=480.5, txt="Example: Obtain Minimum Value"),
    dict(name="L2", y0=269, y1=314, x0=269, x1=665, cx=467.0, txt="of a function using"),
    dict(name="L3", y0=347, y1=392, x0=235, x1=711, cx=473.0, txt="Gradient Descent (GD)"),
]
TOL = 3.0  # frame px

fails, notes = [], []


def bands_of(im, scale_note):
    """Sensitive ink bands in panel interior (same predicate as measure_rows.py)."""
    a = np.asarray(im.convert("RGB")).astype(int)
    H, W = a.shape[:2]
    sc = H / 540.0
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    bg_r, bg_g, bg_b = 231, 233, 230
    dist = np.sqrt((r - bg_r) ** 2 + (g - bg_g) ** 2 + (b - bg_b) ** 2)
    ink = dist > 40
    # panel interior window (frame px 75..885 x, 45..530 y), same as original script
    ink[:, : int(75 * sc)] = False
    ink[:, int(885 * sc):] = False
    ink[int(45 * sc):, :] = ink[int(45 * sc):, :]  # keep y from 45
    ink[: int(45 * sc), :] = False
    ink[int(530 * sc):, :] = False
    rows = ink.sum(axis=1)
    out, in_b = [], False
    for y in range(H):
        if rows[y] > 0 and not in_b:
            s = y; in_b = True
        elif rows[y] == 0 and in_b:
            out.append((s, y - 1)); in_b = False
    if in_b:
        out.append((s, H - 1))
    out = [bd for bd in out if ink[bd[0]:bd[1] + 1].sum() > 50 * sc * sc]
    res = []
    for (y0, y1) in out:
        seg = ink[y0:y1 + 1]
        xs = np.where(seg.any(axis=0))[0]
        res.append(dict(y0=y0 / sc, y1=(y1 + 1) / sc, x0=xs.min() / sc,
                        x1=(xs.max() + 1) / sc, ink=seg.sum()))
    return res, sc


rb, rsc = bands_of(Image.open(RENDER), "render")
ob, osc = bands_of(Image.open(ORIG), "orig")

print(f"render bands (frame-px units, scale {rsc:.4f}):")
for b in rb:
    print(f"  y {b['y0']:.1f}-{b['y1']:.1f}  x {b['x0']:.1f}-{b['x1']:.1f}  "
          f"cx={(b['x0'] + b['x1']) / 2:.1f}  ink={b['ink']}")
print(f"orig bands (re-derived with same predicate, scale {osc:.4f}):")
for b in ob:
    print(f"  y {b['y0']:.1f}-{b['y1']:.1f}  x {b['x0']:.1f}-{b['x1']:.1f}  "
          f"cx={(b['x0'] + b['x1']) / 2:.1f}  ink={b['ink']}")

# 1. exactly three title bands (badge sits at x>=856 which is outside the 75..885
# window? No: badge x 856-884 IS inside. Restrict title bands to y>150 to exclude
# badge band (y 55-93).)
rb_t = [b for b in rb if b["y0"] > 150]
ob_t = [b for b in ob if b["y0"] > 150]
if len(rb_t) != 3:
    fails.append(f"expected 3 title bands in render, got {len(rb_t)}")
for i, b in enumerate(rb_t):
    if b["y1"] - b["y0"] > 55 or b["y1"] - b["y0"] < 38:
        fails.append(f"render band {i} height {b['y1'] - b['y0']:.1f} unexpected (split/wrap?)")

# 2/3. per-band compare + pitch
print("\nper-band deltas (render vs banked target, frame px):")
for i, (b, t) in enumerate(zip(rb_t, TARGET)):
    d_y0 = b["y0"] - t["y0"]
    d_y1 = b["y1"] - t["y1"]
    d_x0 = b["x0"] - t["x0"]
    d_x1 = b["x1"] - t["x1"]
    cx = (b["x0"] + b["x1"]) / 2
    d_cx = cx - t["cx"]
    print(f"  {t['name']}: dy0={d_y0:+.1f} dy1={d_y1:+.1f} dx0={d_x0:+.1f} "
          f"dx1={d_x1:+.1f} cx={cx:.1f} (target {t['cx']}, d={d_cx:+.1f}) "
          f"w={b['x1'] - b['x0']:.1f} (target {t['x1'] - t['x0']})")
    for label, v in (("y0", d_y0), ("y1", d_y1), ("x0", d_x0), ("x1", d_x1), ("cx", d_cx)):
        if abs(v) > TOL:
            fails.append(f"{t['name']} {label} delta {v:+.1f} exceeds tol {TOL}")
pitches = [rb_t[1]["y0"] - rb_t[0]["y0"], rb_t[2]["y0"] - rb_t[1]["y0"]]
print(f"band pitch (top-to-top): {pitches[0]:.1f}, {pitches[1]:.1f} (target 78)")
if any(abs(p - 78) > TOL for p in pitches):
    fails.append(f"pitch {pitches} != 78")

# 4. LINE/BOX WRAP: no ink outside expected bands (between bands, above L1,
# below L3) within the interior window.
gaps_ok = True
for (a, b2) in zip(rb_t, rb_t[1:]):
    if b2["y0"] - a["y1"] < 20:
        gaps_ok = False
if not gaps_ok:
    fails.append("inter-band gap collapsed (wrap spill between lines?)")

# 5. FRAME CONTAINMENT: title ink inside panel with clearance to strokes
strokes = dict(left=58.5, right=901)
for i, b in enumerate(rb_t):
    if b["x0"] < 75 or b["x1"] > 885:
        fails.append(f"band {i} ink crosses the panel-interior window")
    clear_l = b["x0"] - strokes["left"]
    clear_r = strokes["right"] - b["x1"]
    clear_b = 530 - b["y1"]
    print(f"  band {i} clearance: L {clear_l:.1f}px, R {clear_r:.1f}px, bottom-of-window {clear_b:.1f}px")
    if clear_l < 10 or clear_r < 10:
        fails.append(f"band {i} too close to vertical stroke")

# 6. badge numeral: dark ink inside badge circle (render)
a = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
sc = a.shape[0] / 540.0
win = a[int((73 - 17) * sc): int((73 + 17) * sc), int((876 - 17) * sc): int((876 + 17) * sc)]
dark = (win.sum(axis=2) < 300).sum()
print(f"\nbadge numeral dark px in render: {dark} (need >= 12*scale^2={12 * sc * sc:.0f})")
if dark < 12 * sc * sc:
    fails.append(f"badge numeral ink sparse ({dark})")

# 7. cross-check re-derived original bands vs banked targets (predicate sanity)
print("\norig re-derived vs banked (predicate drift check):")
for b, t in zip(ob_t, TARGET):
    print(f"  {t['name']}: dy0={b['y0'] - t['y0']:+.1f} dy1={b['y1'] - t['y1']:+.1f} "
          f"dx0={b['x0'] - t['x0']:+.1f} dx1={b['x1'] - t['x1']:+.1f}")

print("\n" + ("SELF-CHECK: FAIL" if fails else "SELF-CHECK: PASS (all closed-loop bands within tol)"))
for f in fails:
    print("  -", f)
