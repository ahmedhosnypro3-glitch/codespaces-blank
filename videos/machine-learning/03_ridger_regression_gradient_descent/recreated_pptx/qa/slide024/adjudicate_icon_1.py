#!/usr/bin/env python3
"""Adjudication of the icon-crop FAIL (attempt 1), MAJOR #1 / #2.

Claim: IMG1 (recreation) is a "near-solid dark wedge/blob with little internal
separation", IMG2 (original) "preserves a thin outline/linear pen with internal
light separation; reads as nib + thin shaft + end"; IMG1 stroke/fill width
"2-3x IMG2's".

CLOSED-LOOP RULE: the SAME predicate on BOTH images, measured at the SAME scale.
The original is 960x540 (1 px = 1 slide pt); the 150dpi render is 2001x1125
(2.083 px per slide px). Both are resampled to the glyph's native original
resolution so no scale artifact can fabricate or erase interior structure.

Interior structure is measured as FILL RATIO: ink pixels inside the ink bbox /
bbox area. A thin outline reads low (~0.3-0.45); a solid glyph reads high
(>0.7). Plus an explicit "enclosed light pixel" count (light px fully surrounded
by ink), which is the only thing that can prove "internal separation".
"""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORI = f"{ROOT}/unique_slides/slide_024.jpg"
REN = f"{ROOT}/recreated_pptx/qa/slide024/render_1.png"
CROP_ORI = f"{ROOT}/recreated_pptx/qa/slide024/crop_1_icon_orig.png"
CROP_REN = f"{ROOT}/recreated_pptx/qa/slide024/crop_1_icon_render.png"

# embed box from gen_icon.py (slide px): x 462.5..480.04, y 504.5..524.06
BX0, BY0, BX1, BY1 = 462.5, 504.5, 480.04, 524.06


def lum(a):
    return a[:, :, 0] * 0.299 + a[:, :, 1] * 0.587 + a[:, :, 2] * 0.114


def ink_mask(a, thr=200.0):
    """Sensitive relative-ink mask: darker than thr of 255 luminance."""
    return lum(a) < thr


def enclosed_light(mask):
    """Light pixels strictly inside the ink bbox that have ink on all 4-neighbour
    sides somewhere along their row/column run (i.e. not touching the bbox edge)."""
    ys, xs = np.where(mask)
    if not len(ys):
        return 0, 0
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    light = ~sub
    # a light pixel is 'internal' only if ink exists to its left AND right in its
    # row, and above AND below in its column (within the bbox)
    row_has_l = np.zeros(sub.shape, bool)
    row_has_r = np.zeros(sub.shape, bool)
    col_has_u = np.zeros(sub.shape, bool)
    col_has_d = np.zeros(sub.shape, bool)
    H, W = sub.shape
    for i in range(H):
        cums = np.concatenate(([0], np.cumsum(sub[i])))
        left = cums[:-1] > 0
        right = (cums[-1] - cums[1:]) > 0
        row_has_l[i] = left
        row_has_r[i] = right
    for j in range(W):
        cums = np.concatenate(([0], np.cumsum(sub[:, j])))
        col_has_u[:, j] = cums[:-1] > 0
        col_has_d[:, j] = (cums[-1] - cums[1:]) > 0
    internal = light & row_has_l & row_has_r & col_has_u & col_has_d
    return int(internal.sum()), int(sub.size)


# --- 1. BOTH sides downsampled to the ORIGINAL's native glyph resolution ----
ori_full = Image.open(ORI).convert("RGB")
ren_full = Image.open(REN).convert("RGB")
oren_scale = 2001 / 960.0  # render px per original px (2.084)

# glyph window in ORIGINAL px (float-exact), rendered onto both sides with the
# identical box + identical output size => matched scale by construction.
box_o = (BX0, BY0, BX1 + 1, BY1 + 1)
gw = round((BX1 + 1 - BX0) * oren_scale)   # output width in render px
gh = round((BY1 + 1 - BY0) * oren_scale)
box_r = tuple(v * oren_scale for v in box_o)

ren_win = ren_full.crop((round(box_r[0]), round(box_r[1]),
                         round(box_r[2]), round(box_r[3]))).resize((gw, gh), Image.LANCZOS)
# original: 1:1 native (no interpolation at all)
ori_win = ori_full.crop((round(box_o[0]), round(box_o[1]),
                         round(box_o[2]), round(box_o[3])))
print(f"window: original {ori_win.size} (NATIVE, no resample)  render {ren_win.size}"
      f"  (both {gw}x{gh})")
ori_win.save("/tmp/adj_ori_native.png")
ren_win.save("/tmp/adj_ren_win.png")

mo = ink_mask(np.asarray(ori_win).astype(float))
mr = ink_mask(np.asarray(ren_win).astype(float))

for name, m in (("ORIGINAL(native)", mo), ("RENDER(2.083x)", mr)):
    ys, xs = np.where(m)
    bbox = (xs.min(), ys.min(), xs.max(), ys.max())
    w = bbox[2] - bbox[0] + 1
    h = bbox[3] - bbox[1] + 1
    sub = m[bbox[1]:bbox[3] + 1, bbox[0]:bbox[3] + 1]
    # careful: correct slice
    sub = m[bbox[1]:bbox[3] + 1, bbox[0]:bbox[2] + 1]
    fill = sub.sum() / sub.size
    enc, size = enclosed_light(m)
    print(f"{name:18s} ink bbox {w}x{h} at ({bbox[0]},{bbox[1]})  "
          f"fill-ratio {fill:.3f}  enclosed-light px {enc}/{size}  "
          f"ink total {int(m.sum())}")

# --- 2. same numbers straight off the banked zoomed crops (matched pair) -------
print("\n--- banked zoomed crop pair (crop_1_icon_*, same effective scale by "
      "construction) ---")
co = np.asarray(Image.open(CROP_ORI).convert("RGB")).astype(float)
cr = np.asarray(Image.open(CROP_REN).convert("RGB")).astype(float)
for name, a in (("crop ORIG", co), ("crop REN", cr)):
    m = ink_mask(a)
    ys, xs = np.where(m)
    bbox = (xs.min(), ys.min(), xs.max(), ys.max())
    sub = m[bbox[1]:bbox[3] + 1, bbox[0]:bbox[2] + 1]
    fill = sub.sum() / sub.size
    enc, size = enclosed_light(m)
    print(f"{name:10s} glyph {bbox[2]-bbox[0]+1}x{bbox[3]-bbox[1]+1}  "
          f"fill-ratio {fill:.3f}  enclosed-light {enc}/{size}  "
          f"vertical span {bbox[1]}..{bbox[3]} of 288")

# --- 3. shaft stroke weight, per-row ink counts, original native -------------
print("\n--- per-row ink counts through the shaft (native original vs render "
      "resampled to the same size) ---")
ao = np.asarray(ori_win).astype(float).mean(axis=2)
ar = np.asarray(ren_win).astype(float).mean(axis=2)
print("row : (darkest-px value, ink count)  ORIGINAL | RENDER")
for i in range(ao.shape[0]):
    ro = ao[i]
    rr = ar[i]
    do = int(ro.min()); dr = int(rr.min())
    no = int((ro < 200).sum()); nr = int((rr < 200).sum())
    if no or nr:
        print(f"  y{i:2d}: orig darkest {do:3d} n={no:2d} | ren darkest {dr:3d} n={nr:2d}")
