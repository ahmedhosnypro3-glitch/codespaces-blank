#!/usr/bin/env python3
"""measure_icon_2.py — precise PIL measurement of the slide-024 pen glyph.

Governing law (judging.md): the judge's findings are HYPOTHESES; PIL measures
the real gap before any fix. This script measures BOTH sides at the SAME native
glyph resolution:

  * the ORIGINAL frame region at 1:1 native (no resample);
  * the 150dpi render region resampled DOWN to the same output size (so no
    scale artifact can fabricate or erase interior structure);
  * the CURRENT asset (icon_024_pen.png) at its own 600dpi resolution.

Everything is printed as bankable numbers: ink bboxes, fill ratios, enclosed
light pixel counts, per-row ink counts (stroke weight), vertical spans mapped
back to SLIDE space, and an ASCII ink map of each side.
"""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORI = f"{ROOT}/unique_slides/slide_024.jpg"
REN = f"{ROOT}/recreated_pptx/qa/slide024/render_1.png"
ASSET = f"{ROOT}/recreated_pptx/build/assets/icon_024_pen.png"

# embed box from build/slide_024.js (slide px): x 462.5..480.04, y 504.5..524.06
BX0, BY0, BX1, BY1 = 462.5, 504.5, 480.04, 524.06
REN_SCALE = 1125 / 540.0   # render px per frame px (150 dpi)


def lum(a):
    return a[:, :, 0] * 0.299 + a[:, :, 1] * 0.587 + a[:, :, 2] * 0.114


def ink_mask(a, thr=200.0):
    """Sensitive relative-ink mask: darker than thr of 255 luminance.
    Panel fill measures ~(233,233,231) -> lum ~231.6, so thr=200 keeps JPEG
    halos while rejecting the fill (same predicate on both sides)."""
    return lum(a) < thr


def ascii_map(m, step=1):
    """Compact ASCII ink map: '#' = ink core (<120), '+' = halo (120..200)."""
    lines = []
    for y in range(0, m.shape[0], step):
        row = []
        for x in range(0, m.shape[1], step):
            v = False
            for dy in range(step):
                for dx in range(step):
                    yy, xx = y + dy, x + dx
                    if yy < m.shape[0] and xx < m.shape[1] and m[yy, xx]:
                        v = True
            row.append("#" if v else ".")
        lines.append("".join(row))
    return lines


def stats(name, m, frame_x0, frame_y0, eff):
    """m: ink mask in NATIVE frame px (1 unit = 1 slide px). eff: px per slide px (1 for native)."""
    ys, xs = np.where(m)
    if not len(ys):
        print(f"{name}: NO INK")
        return None
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
    w, h = x1 - x0 + 1, y1 - y0 + 1
    sub = m[y0:y1 + 1, x0:x1 + 1]
    fill = sub.sum() / sub.size
    rows = m.sum(axis=1)
    cols = m.sum(axis=0)
    print(f"{name}: ink bbox {w}x{h} slide-px  at bbox-local ({x0},{y0})")
    print(f"   slide-space ink: x {frame_x0 + x0:.2f}..{frame_x0 + x1:.2f}  "
          f"y {frame_y0 + y0:.2f}..{frame_y0 + y1:.2f}")
    print(f"   fill-ratio (ink/bbox area) {fill:.3f}   ink total {int(m.sum())}")
    print(f"   per-row ink counts: {[int(r) for r in rows[y0:y1 + 1]]}")
    print(f"   per-col ink counts: {[int(c) for c in cols[x0:x1 + 1]]}")
    return (x0, y0, x1, y1, fill)


print("=" * 78)
print("1. ORIGINAL glyph at NATIVE resolution (1 px = 1 slide px, no resample)")
print("=" * 78)
ori = Image.open(ORI).convert("RGB")
OW, OH = ori.size
assert (OW, OH) == (960, 540)
# window in original px: the embed box rounded outward, native integer crop
ox0, oy0 = int(np.floor(BX0)), int(np.floor(BY0))
ox1, ey1 = int(np.ceil(BX1)), int(np.ceil(BY1))
ori_win = ori.crop((ox0, oy0, ox1 + 1, ey1 + 1))
mo = ink_mask(np.asarray(ori_win).astype(float))
print(f"window: original crop ({ox0},{oy0})..({ox1},{ey1}) size {ori_win.size} (NATIVE)")
o_stats = stats("ORIGINAL", mo, ox0, oy0, 1.0)
print("\nASCII ink map (native, '#'=ink <200 lum):")
for ln in ascii_map(mo):
    print("   " + ln)

print()
print("=" * 78)
print("2. RENDER glyph resampled DOWN to the same native output size")
print("=" * 78)
ren = Image.open(REN).convert("RGB")
RW, RH = ren.size
print(f"render {RW}x{RH} (scale {REN_SCALE:.5f} render px per frame px)")
# float-exact box in render px covering the SAME slide-space window, then LANCZOS
# downscale to exactly the native window size (ow x oh) => matched by construction
rbox = (ox0 * REN_SCALE, oy0 * REN_SCALE, (ox1 + 1) * REN_SCALE, (ey1 + 1) * REN_SCALE)
ren_win = ren.resize(ori_win.size, Image.LANCZOS, box=rbox)
mr = ink_mask(np.asarray(ren_win).astype(float))
r_stats = stats("RENDER", mr, ox0, oy0, 1.0)
print("\nASCII ink map (render, downsampled to native):")
for ln in ascii_map(mr):
    print("   " + ln)

print()
print("=" * 78)
print("3. CURRENT ASSET (icon_024_pen.png) at its own 600dpi canvas")
print("=" * 78)
asset = Image.open(ASSET).convert("RGBA")
aw, ah = asset.size
print(f"asset canvas {aw}x{ah} png px (600dpi -> {aw/600*72:.2f} x {ah/600*72:.2f} slide px)")
alpha = np.asarray(asset)[:, :, 3]
ink_a = alpha > 40
ay, ax = np.where(ink_a)
if len(ay):
    print(f"asset alpha-ink bbox {ax.max()-ax.min()+1}x{ay.max()-ay.min()+1} png px "
          f"at ({ax.min()},{ay.min()}) -> slide-space "
          f"x {BX0 + ax.min()/(600/72):.2f}..{BX0 + ax.max()/(600/72):.2f}  "
          f"y {BY0 + ay.min()/(600/72):.2f}..{BY0 + ay.max()/(600/72):.2f}")
    print(f"asset ink fill-ratio within bbox: "
          f"{ink_a[ay.min():ay.max()+1, ax.min():ax.max()+1].sum()/ink_a[ay.min():ay.max()+1, ax.min():ax.max()+1].size:.3f}")

print()
print("=" * 78)
print("4. SIDE-BY-SIDE delta (native window, same predicate, same size)")
print("=" * 78)
if o_stats and r_stats:
    ox0b, oy0b, ox1b, oy1b, ofill = o_stats
    rx0b, ry0b, rx1b, ry1b, rfill = r_stats
    print(f"ORIGINAL ink: x {ox0b}..{ox1b} ({ox1b-ox0b+1} px)  y {oy0b}..{oy1b} ({oy1b-oy0b+1} px)  fill {ofill:.3f}")
    print(f"RENDER   ink: x {rx0b}..{rx1b} ({rx1b-rx0b+1} px)  y {ry0b}..{ry1b} ({ry1b-ry0b+1} px)  fill {rfill:.3f}")
    print(f"delta    dx={(rx0b+rx1b)/2-(ox0b+ox1b)/2:+.2f}  dy={(ry0b+ry1b)/2-(oy0b+oy1b)/2:+.2f}  "
          f"d_w={(rx1b-rx0b)-(ox1b-ox0b):+d}  d_h={(ry1b-ry0b)-(oy1b-oy0b):+d}  d_fill={rfill-ofill:+.3f}")
    # vertical spans as % of the crop used by the attempt-1 zoomed pair (y491..536)
    print("\nVertical position vs the attempt-1 icon crop window (frame y491..536, 46 px):")
    print(f"  ORIGINAL ink spans crop %: {(oy0b+1)/46*100:.1f}% .. {(oy1b+1)/46*100:.1f}%  (bottom edge at {oy1b+1}/46)")
    print(f"  RENDER   ink spans crop %: {(ry0b+1)/46*100:.1f}% .. {(ry1b+1)/46*100:.1f}%  (bottom edge at {ry1b+1}/46)")
