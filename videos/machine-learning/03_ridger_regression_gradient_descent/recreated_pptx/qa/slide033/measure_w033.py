#!/usr/bin/env python3
"""PIL measurement of render_8.png vs unique_slides/slide_033.jpg for slide 033.

Independent verification for the w033-finish lane: validates the attempt-8 build's
claimed frame geometry against ORIGINAL ink, and measures curve ripple
(second-difference) on the render's plot region.

Render: 2001x1125 (SX=2001/960, SY=1125/540). Frame px = render px / scale.
"""
import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_033.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide033/render_8.png"

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
rend = np.asarray(Image.open(REND).convert("RGB")).astype(int)
OH, OW = orig.shape[:2]
RH, RW = rend.shape[:2]
SX, SY = RW / OW, RH / OH
print(f"orig {OW}x{OH}  render {RW}x{RH}  scale SX={SX:.6f} SY={SY:.6f}")


def to_frame(y, x):
    """render (row,col) -> frame (y,x)"""
    return y / SY, x / SX


def band_report(name, y0, y1, x0, x1, expected, both=True):
    """Report median colour of a band region on BOTH images and RGB distance."""
    out = [f"{name}  y{y0}-{y1} x{x0}-{x1}"]
    for tag, img, xsc, ysc in (("ORIG", orig, 1.0, 1.0), ("REND", rend, SX, SY)):
        oy0, ox0 = int(round(y0 * ysc)), int(round(x0 * xsc))
        oy1, ox1 = int(round(y1 * ysc)), int(round(x1 * xsc))
        blk = img[oy0:oy1, ox0:ox1].reshape(-1, 3)
        med = tuple(int(v) for v in np.median(blk, axis=0))
        out.append(f"  {tag}: median RGB {med}  (expected {expected})")
    if expected is not None:
        for tag, img in (("ORIG", orig), ("REND", rend)):
            oy0, ox0 = int(round(y0 * (1.0 if tag == "ORIG" else SY))), int(round(x0 * (1.0 if tag == "ORIG" else SX)))
            oy1, ox1 = int(round(y1 * (1.0 if tag == "ORIG" else SY))), int(round(x1 * (1.0 if tag == "ORIG" else SX)))
            blk = img[oy0:oy1, ox0:ox1].reshape(-1, 3)
            med = np.median(blk, axis=0)
            d = float(np.abs(med - np.array(expected)).max())
            out[-1] = out[-1] + f"  max-channel dev {d:.0f}"
    print("\n".join(out))


print("\n" + "=" * 70)
print("A. TABLE BAND FILLS (frame px, build claims vs measurement)")
print("=" * 70)
# interior of each band, away from separator lines and text rows
bands = [
    ("band1", 332, 348, 145, 300, (217, 226, 119)),
    ("band1_lower", 350, 367, 145, 300, (217, 226, 119)),
    ("band2", 375, 391, 145, 300, (214, 178, 248)),
    ("band3", 418, 434, 145, 300, (247, 221, 194)),
    ("slope_data", 460, 477, 160, 260, (222, 172, 149)),
    ("slope_label", 460, 477, 89, 140, (233, 255, 210)),
    ("nextx", 484, 501, 150, 300, (247, 190, 196)),
    ("cyan_insert", 334, 348, 670, 780, (139, 248, 171)),
]
for n, y0, y1, x0, x1, exp in bands:
    band_report(n, y0, y1, x0, x1, exp)

print("\n" + "=" * 70)
print("B. PARAMETER BOX (build claims white + navy border, 3 coloured rows)")
print("=" * 70)
for n, y0, y1, x0, x1, exp in [
    ("param_top_row", 256, 268, 82, 125, (233, 255, 212)),
    ("param_mid_row", 271, 283, 82, 125, (249, 187, 193)),
    ("param_bot_row", 286, 298, 82, 125, (253, 253, 0)),
    ("param_box_bg", 248, 252, 76, 175, (255, 255, 255)),
]:
    band_report(n, y0, y1, x0, x1, exp)

print("\n" + "=" * 70)
print("C. PLOT BOX (build claims white box x607..844 y62..311, teal curve)")
print("=" * 70)
for n, y0, y1, x0, x1, exp in [
    ("plot_bg", 70, 100, 620, 700, (255, 255, 255)),
    ("plot_bg_low", 280, 305, 700, 780, (255, 255, 255)),
]:
    band_report(n, y0, y1, x0, x1, exp)

print("\n" + "=" * 70)
print("D. EQUATION + ANNOTATION BOXES")
print("=" * 70)
band_report("eq_box", 184, 228, 451, 583, (255, 255, 255))
band_report("annot_box", 256, 297, 248, 594, (239, 255, 226))
band_report("callout_pink", 260, 292, 616, 696, (247, 201, 250))

print("\n" + "=" * 70)
print("E. CURVE — second-difference ripple check (render plot)")
print("=" * 70)


def find_curve(img, x0, x1, y0, y1, colors):
    """Return per-column row-centroid of pixels close to any target colour."""
    rows, cols = [], []
    sub = img[int(y0 * SY):int(y1 * SY), int(x0 * SX):int(x1 * SX)]
    mask = np.zeros(sub.shape[:2], bool)
    for c in colors:
        m = np.abs(sub - np.array(c)).max(axis=2) <= 90
        mask |= m
    for j in range(sub.shape[1]):
        idx = np.flatnonzero(mask[:, j])
        if len(idx):
            rows.append(float(idx.mean()))
            cols.append(j)
    return np.array(cols), np.array(rows)


# attempt-8 curve colour #2FA9AC, width ~2.6pt -> ~5.4 render px
cx, cy = find_curve(rend, 612, 832, 110, 264, [(47, 169, 172)])
if len(cx) > 8:
    ys = cy
    d2 = ys[2:] - 2 * ys[1:-1] + ys[:-2]
    span_ok = f"x range {cx.min() + 612}..{cx.max() + 612} ({cx.max() - cx.min()} cols)"
    gaps = int(np.sum(np.diff(cx) > 3))
    print(f"render curve columns: {len(cx)}  {span_ok}")
    print(f"  gaps (>3px column jumps): {gaps}")
    print(f"  ripple std(d2) = {d2.std():.3f} render-px = {d2.std() / SY:.3f} frame-px")
    print(f"  max |d2| = {np.abs(d2).max():.2f} render-px = {np.abs(d2).max() / SY:.2f} frame-px")
    # turning points
    tps = []
    for i in range(1, len(ys) - 1):
        a, b, c = ys[i - 1], ys[i], ys[i + 1]
        if (b - a) * (c - b) < 0:
            tps.append((int(cx[i] + 612), int(b / SY)))
    print(f"  turning points (frame x, y): {tps}")

# original curve ink for comparison
cxo, cyo = find_curve(orig, 612, 832, 110, 264, [(47, 169, 172)])
print(f"\noriginal curve columns matched: {len(cxo)}")

print("\n" + "=" * 70)
print("F. INK CENSUS — dark ink per region, ORIG vs REND (frame px)")
print("=" * 70)
regions = {
    "title": (100, 60, 530, 90),
    "sub1": (110, 92, 530, 112),
    "sub2": (180, 115, 470, 140),
    "param_box": (75, 245, 175, 310),
    "eq_box": (449, 182, 585, 230),
    "annot": (246, 254, 597, 299),
    "table": (86, 320, 869, 519),
    "plot": (607, 60, 845, 313),
}
for n, (x0, y0, x1, y1) in regions.items():
    o = orig[y0:y1, x0:x1]
    r = rend[int(y0 * SY):int(y1 * SY), int(x0 * SX):int(x1 * SX)]
    od = int((o.max(axis=2) < 110).sum())
    rd = int((r.max(axis=2) < 110).sum())
    print(f"{n:11s} orig dark px {od:7d}   render dark px {rd:7d}   ratio {rd / max(od, 1):.2f}")

print("\n" + "=" * 70)
print("G. CHROME (house template)")
print("=" * 70)
# panel + strokes + badge
print("panel edges: expect E9E9E7 from x54..903 y45..540")
print("  orig panel px (100,300):", orig[300, 100], " render:", rend[int(300 * SY), int(100 * SX)])
print("  orig outside panel (10,10):", orig[10, 10], " render:", rend[int(10 * SY), int(10 * SX)])
print("  orig bottom-left panel corner region:", orig[500, 60], " render:", rend[int(500 * SY), int(60 * SX)])
# badge at (876,73)
bx, by = int(876 * SX), int(73 * SY)
print(f"badge centre render px ({bx},{by}):", rend[by, bx])
# top stroke: must be absent
top = orig[45:52, 60:900]
rtop = rend[int(45 * SY):int(52 * SY), int(60 * SX):int(900 * SX)]
print("red px in top band ORIG:", int(((top[:, :, 0] > 140) & (top[:, :, 1] < 90) & (top[:, :, 2] < 90)).sum()),
      " REND:", int(((rtop[:, :, 0] > 140) & (rtop[:, :, 1] < 90) & (rtop[:, :, 2] < 90)).sum()))
