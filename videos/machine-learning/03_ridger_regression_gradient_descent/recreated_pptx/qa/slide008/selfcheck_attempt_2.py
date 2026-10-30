"""Mandatory pre-judge self-check for slide 008 attempt 1 (render_1.png).

Frame measurements from unique_slides/slide_008.jpg (960x540 px, 1px = 1pt):
  house chrome: white canvas + E9E9E7 panel x54..903 y45..540 + C00000 strokes
  left x58.5 / right x901 / bottom y538.5 (NO top stroke) + badge center (876,73) d~35
  FDFD96 fill / 6A5ACD ring / Arial bold 18pt numeral 333333 = 8.
  content: 2 text bands only, no bullets/equations/imagery.
    TITLE    rows 231..263  cols 107..817  center 462.0  core C00000 (164,21,36 JPEG-dark)
    SUBTITLE rows 302..328  cols 261..664  center 462.5  core 0000CC (16,1,165 JPEG-dark)
"""
from PIL import Image
import numpy as np

RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide008/render_1.png"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_008.jpg"
SCALE = 150 / 72  # render px per frame px

r_im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = r_im.shape[:2]
sc = H / 540.0
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
print(f"render {W}x{H} px  scale {sc:.4f} px/frame-px (150dpi = {SCALE:.4f})")

def bands(arr, scale):
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    strong = ((r + g + b) < 360) | ((r > 110) & (g < 90) & (b < 90)) | ((b > 110) & (r < 90))
    m = strong.copy()
    if scale > 1:
        m[:, int(54.5 * scale):int(63.5 * scale)] = False
        m[:, int(896.5 * scale):int(906 * scale)] = False
        m[int(534.5 * scale):, :] = False
        m[:int(46 * scale), :] = False
        m[int(48 * scale):int(100 * scale), int(843 * scale):int(912 * scale)] = False
    else:
        m[:, 55:63] = False
        m[:, 896:906] = False
        m[535:, :] = False
        m[:46, :] = False
        m[48:100, 843:912] = False
    rows = np.where(m.sum(axis=1) > 0)[0]
    out = []
    s = p = rows[0]
    for y in rows[1:]:
        if y - p > 3 * scale:
            out.append((s, p)); s = y
        p = y
    out.append((s, p))
    res = []
    for (y0, y1) in out:
        sub = m[y0:y1 + 1, :]
        # prune JPEG-halo rows: a row must carry visible ink to count
        densities = sub.sum(axis=1)
        keep = np.where(densities >= 7 * scale * scale)[0]
        if not len(keep):
            continue
        y0k, y1k = y0 + keep.min(), y0 + keep.max()
        sub2 = m[y0k:y1k + 1, :]
        xx = np.where(sub2.sum(axis=0) > 0)[0]
        res.append((y0k / scale, y1k / scale, xx.min() / scale, xx.max() / scale))
    return res

bo, br = bands(o, 1.0), bands(r_im, sc)
names = ["title", "subtitle"]
fails = []
print("\nband comparisons (frame px):")
for i, nm in enumerate(names):
    y0o, y1o, x0o, x1o = bo[i]
    y0r, y1r, x0r, x1r = br[i]
    ho, hr = y1o - y0o + 1, y1r - y0r + 1
    print(f"  {nm:8s} ORIG rows {y0o:.0f}..{y1o:.0f} cols {x0o:.0f}..{x1o:.0f} h={ho} | "
          f"RENDER rows {y0r:.1f}..{y1r:.1f} cols {x0r:.1f}..{x1r:.1f} h={hr:.1f}")
    for label, a, b, tol in (("left", x0o, x0r, 3), ("right", x1o, x1r, 3),
                             ("top", y0o, y0r, 3), ("bottom", y1o, y1r, 3)):
        if abs(a - b) > tol:
            fails.append(f"{nm} {label}: orig {a} vs render {b} (tol {tol})")

# vertical gap between bands: measure the whitespace
print(f"\ninter-band gap: ORIG {bo[1][0] - bo[0][1]:.0f} px  RENDER {br[1][0] - br[0][1]:.1f} px")
if abs((bo[1][0] - bo[0][1]) - (br[1][0] - br[0][1])) > 4:
    fails.append(f"inter-band gap orig {bo[1][0]-bo[0][1]:.0f} vs render {br[1][0]-br[0][1]:.1f}")

# no top stroke
top = r_im[:int(46 * sc), :, :]
redp = ((top[:, :, 0] > 90) & (top[:, :, 1] < 100) & (top[:, :, 2] < 100)).sum()
print(f"top-band red px (must be 0): {redp}")
if redp:
    fails.append(f"top stroke present: {redp} red px")

# content ink count parity (rough density check)
def count(arr, scale):
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    strong = ((r + g + b) < 360) | ((r > 110) & (g < 90) & (b < 90)) | ((b > 110) & (r < 90))
    m = strong.copy()
    if scale > 1:
        m[:, int(54.5 * scale):int(63.5 * scale)] = False
        m[:, int(896.5 * scale):int(906 * scale)] = False
        m[int(534.5 * scale):, :] = False
        m[:int(46 * scale), :] = False
        m[int(48 * scale):int(100 * scale), int(843 * scale):int(912 * scale)] = False
    return m.sum()

co, cr = count(o, 1.0), count(r_im, sc)
print(f"content ink px: ORIG {co}  RENDER {cr}  ratio {cr/(co*sc*sc):.3f} (JPEG-thin orig expected ~0.9-1.05)")

# frame containment: no content ink outside panel x54..903
print("\nframe containment:")
r, g, b = r_im[:, :, 0], r_im[:, :, 1], r_im[:, :, 2]
strong = ((r + g + b) < 360) | ((r > 110) & (g < 90) & (b < 90)) | ((b > 110) & (r < 90))
outside = strong.copy()
outside[:, int(54 * sc):int(904 * sc)] = False
outside[int(535 * sc):, :] = False
n_out = outside.sum()
print(f"  content ink outside panel: {n_out} px (must be 0)")
if n_out:
    yy, xx = np.where(outside)
    fails.append(f"frame containment: {n_out} px outside panel, rows {yy.min()/sc:.0f}..{yy.max()/sc:.0f} cols {xx.min()/sc:.0f}..{xx.max()/sc:.0f}")

print("\n" + ("SELF-CHECK: ALL PASS" if not fails else "SELF-CHECK FAILURES: " + "; ".join(fails)))
