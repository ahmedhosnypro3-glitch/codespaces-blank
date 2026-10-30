#!/usr/bin/env python3
"""worker-016-fix-2: PIL verification of the two banked defects against the
CURRENT banked render (render_3.png, built from the fixed build/slide_016.js).

Defect A (banked BLOCKER): render_1.png was missing 4 of 12 body text lines
(original L7-L10, y332..447) incl. both blue key terms "L2"/"L1 regularization";
banked measurement: original 6904 ink px vs render 0 px in x88..828 / y330..455.

Defect B (banked MAJOR): the build's 2nd black underline spanned x675..877 frame
px, crossing the inner white box's right border at x830.

All measurements in 960x540 frame space (1px=1pt). The render (2001x1125, 150dpi)
is downscaled 2001x1125 -> 960x540 LANCZOS (scale 2.0833) for band comparison;
native-resolution counts are taken on the un-downscaled render too.
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
RENDERS = {
    "render_1 (banked FAIL)": f"{QA}/render_1.png",
    "render_2 (fixed)": f"{QA}/render_2.png",
    "render_3 (current, == pptx)": f"{QA}/render_3.png",
}


def frame(im):
    return im.resize((960, 540), Image.LANCZOS)


def ink_mask(arr):
    """Dark ink: any channel well below mid on a near-white field."""
    return arr.min(axis=2) < 160


def band_ink(mask, y0, y1, x0, x1):
    return int(mask[y0:y1, x0:x1].sum())


def blue_ink(arr):
    """Blue text: B clearly exceeds R, and the pixel is darkish."""
    r, g, b = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)
    return (b - r > 40) & (b < 200)


o = Image.open(ORIG).convert("RGB")
oa = np.asarray(o)
om = ink_mask(oa)
ob = blue_ink(oa)

print(f"ORIGINAL {o.size}")
print("=" * 78)

# ---- Defect A: the L7-L10 band -------------------------------------------------
print("\n## DEFECT A — L7-L10 body band (x88..828, y330..455)")
for label, path in RENDERS.items():
    im = Image.open(path).convert("RGB")
    f = np.asarray(frame(im))
    fm = ink_mask(f)
    n = band_ink(fm, 330, 455, 88, 828)
    print(f"  {label:32s} frame-space ink px = {n}")
print(f"  {'ORIGINAL':32s} frame-space ink px = {band_ink(om, 330, 455, 88, 828)}")

print("\n  blue-ink evidence (the two key-term runs 'L2/L1 regularization'):")
for label, path in RENDERS.items():
    im = Image.open(path).convert("RGB")
    f = np.asarray(frame(im))
    fb = blue_ink(f)
    cols = np.where(fb[330:455, 88:828].any(axis=0))[0]
    rows = np.where(fb[330:455, 88:828].any(axis=1))[0]
    if len(cols):
        print(f"  {label:32s} blue px={int(fb[330:455, 88:828].sum())} "
              f"x={cols.min()+88}..{cols.max()+88} y={rows.min()+330}..{rows.max()+330}")
    else:
        print(f"  {label:32s} blue px=0 (no blue key terms)")
print(f"  {'ORIGINAL':32s} blue px={int(ob[330:455, 88:828].sum())}")

# native-resolution count for the decisive verdict (banked used native px)
print("\n  native-resolution ink in the same frame-scaled bbox:")
for label, path in RENDERS.items():
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    s = a.shape[0] / 540
    reg = a[int(330 * s):int(455 * s), int(88 * s):int(828 * s)]
    print(f"  {label:32s} native ink px = {int(ink_mask(reg).sum())}")
nreg = oa[330:455, 88:828]
print(f"  {'ORIGINAL':32s} native ink px = {int(ink_mask(nreg).sum())}")

# per-line band table (original's 12 lines)
print("\n  per-band ink px (frame rows), original vs current render:")
cur = np.asarray(frame(Image.open(RENDERS["render_3 (current, == pptx)"]).convert("RGB")))
cm = ink_mask(cur)
BANDS = [(59, 86, "title"), (104, 117, "L1 hdr"), (129, 146, "L2 hdr"),
         (179, 197, "b1"), (230, 248, "b2a"), (256, 273, "b2b"), (281, 298, "b2c"),
         (332, 350, "b3a"), (357, 374, "b3b"), (408, 426, "b4a"), (434, 447, "b4b"),
         (484, 502, "b5a"), (510, 527, "b5b")]
for y0, y1, name in BANDS:
    print(f"    {name:8s} y{y0:3d}-{y1:3d}  orig={band_ink(om, y0, y1, 88, 828):6d}  "
          f"render_3={band_ink(cm, y0, y1, 88, 828):6d}")

# ---- Defect B: underline overrun past the inner box border x830 ---------------
print("\n## DEFECT B — 2nd underline crossing the inner box border x830")
print("  (banked: black underline x675..877 in render_1; original's own dark")
print("   underline sits at x109..163 y525, fully inside the box x83..833)")
for label, path in RENDERS.items():
    f = np.asarray(frame(im := Image.open(path).convert("RGB")))
    fm = ink_mask(f)
    # dark-ink columns in the row band of the underlines (y518..530) and the
    # red-underline band (y294..298)
    for (ry0, ry1, tag) in [(294, 299, "red-underline band y294-298"),
                            (518, 531, "dark-underline band y518-530")]:
        seg = fm[ry0:ry1, :]
        cols = np.where(seg.any(axis=0))[0]
        if len(cols):
            # report contiguous runs wider than 30px (real strokes, not glyph bits)
            runs, start = [], cols[0]
            prev = cols[0]
            for c in cols[1:]:
                if c != prev + 1:
                    if prev - start + 1 >= 30:
                        runs.append((start, prev))
                    start = c
                prev = c
            if prev - start + 1 >= 30:
                runs.append((start, prev))
            rs = ", ".join(f"x{a}..{b}" for a, b in runs)
            print(f"    {label:32s} {tag:30s} wide runs: {rs}")
        else:
            print(f"    {label:32s} {tag:30s} (none)")

print("\n  right-border crossing test — any ink beyond the inner box right edge x833")
print("  (white box interior ends x833; house panel stroke at x901):")
for label, path in RENDERS.items():
    f = np.asarray(frame(Image.open(path).convert("RGB")))
    fm = ink_mask(f)
    for (ry0, ry1, tag) in [(294, 299, "y294-298"), (518, 531, "y518-530")]:
        seg = fm[ry0:ry1, 834:900]
        cols = np.where(seg.any(axis=0))[0]
        print(f"    {label:32s} {tag} ink px in x834..899 = {int(seg.sum())}"
              + (f"  cols x{cols.min()+834}..{cols.max()+834}" if len(cols) else ""))
print(f"    {'ORIGINAL':32s} "
      f"y294-298 ink px in x834..899 = {int(om[294:299, 834:900].sum())}  "
      f"y518-530 = {int(om[518:531, 834:900].sum())}")
