"""Test candidate strings for slide 030's right-endpoint label against the original frame.

Calibration: render candidate strings with matplotlib's STIX (Times-like) serif-italic
font at several point sizes, blur (emulating the video frame's soft 9-12pt render),
trim to ink, and compare with the ORIGINAL frame's label ink masks. Known labels
("(2, 10)" and "(5, 1)") calibrate the size; the ambiguous label is then scored
against candidate hypotheses.
"""
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use("Agg")
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_030.jpg"
g = np.array(Image.open(ORIG).convert("RGB")).astype(float).sum(axis=2) / 3.0

fp = FontProperties(family="stix", style="italic")


def render_text(s, size_px, blur=0.7, supersample=4):
    """Rasterise s as an ink mask (1=black) sized to its ink box, at size_px em."""
    tp = TextPath((0, 0), s, size=size_px * supersample, prop=fp)
    bb = tp.get_extents()
    pad = 4 * supersample
    w = int(bb.width) + 2 * pad
    h = int(bb.height) + 2 * pad
    im = Image.new("L", (max(w, 1), max(h, 1)), 0)
    d = ImageDraw.Draw(im)
    path = [(p[0] - bb.x0 + pad, p[1] - bb.y0 + pad) for p in tp.to_polygons(closed_only=True) for p in [p]]
    # draw each polygon
    for poly in tp.to_polygons(closed_only=True):
        if len(poly) < 3:
            continue
        pts = [(x - bb.x0 + pad, y - bb.y0 + pad) for x, y in poly]
        d.polygon(pts, fill=255)
    im = im.resize((max(1, w // supersample), max(1, h // supersample)), Image.LANCZOS)
    a = np.asarray(im).astype(float) / 255.0
    if blur:
        a = np.array(Image.fromarray((a * 255).astype(np.uint8)).filter(
            __import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(blur))).astype(float) / 255.0
    m = a > 0.25
    ys, xs = np.nonzero(m)
    if len(xs) < 2:
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def orig_mask(x0, x1, y0, y1, thr):
    sub = g[y0:y1, x0:x1]
    m = sub < thr
    ys, xs = np.nonzero(m)
    if len(xs) < 2:
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b):
    a = np.asarray(a, bool); b = np.asarray(b, bool)
    inter = np.logical_and(a, b).sum(); union = np.logical_or(a, b).sum()
    return inter / union if union else 0.0


def compare(mask, cand):
    """Best IoU over pad-aligned placements of cand on a canvas of mask's size+2px margin."""
    H, W = mask.shape
    if cand is None:
        return 0.0, (0, 0)
    canvas = np.zeros((H + 6, W + 6), bool)
    ch, cw = cand.shape
    best, bestpos = 0.0, (0, 0)
    for dy in range(0, 7):
        for dx in range(0, 7):
            if dy + ch > canvas.shape[0] or dx + cw > canvas.shape[1]:
                continue
            c = np.zeros_like(canvas)
            c[dy:dy + ch, dx:dx + cw] = cand
            m2 = np.zeros_like(canvas)
            m2[3:3 + H, 3:3 + W] = mask
            v = iou(m2, c)
            if v > best:
                best, bestpos = v, (dx, dy)
    return best, bestpos


LABELS = {
    "known_(2,10)": ((628, 662, 148, 160), "(2, 10)"),
    "known_(5,1)":  ((692, 728, 245, 259), "(5, 1)"),
    "AMBIG":        ((724, 760, 140, 155), None),
}

print("=== calibration: known labels vs their own text rendered at size N px ===")
for name, (box, text) in LABELS.items():
    if text is None:
        continue
    print(f"-- {name}  expected {text}")
    row = []
    for thr in (178, 188, 200):
        m = orig_mask(*box, thr)
        if m is None:
            continue
        for size in (10, 11, 12, 13):
            cand = render_text(text, size)
            if cand is None:
                continue
            v, pos = compare(m, cand)
            row.append(f"sz{size}:{v:.2f}")
    print("   " + " ".join(row))

CANDIDATES = ["(7, 7)", "(7,7)", "(7, 1)", "(7,1)", "(8, 10)", "(8,10)", "(?, ?)", "(?,?)",
              "(x, y)", "(x,y)", "(8, 8)", "(0, 0)", "(2, 10)", "(x+delta, y+delta)"]
print()
print("=== AMBIG label scored against candidates ===")
for thr in (178, 188, 200):
    m = orig_mask(*LABELS["AMBIG"][0], thr)
    if m is None:
        continue
    print(f"-- threshold {thr}, mask {m.shape[1]}x{m.shape[0]}")
    for size in (11, 12, 13):
        scores = []
        for c in CANDIDATES:
            cand = render_text(c, size)
            if cand is None:
                continue
            v, pos = compare(m, cand)
            scores.append((v, c))
        scores.sort(reverse=True)
        print(f"   size {size}: " + "  ".join(f"{c}={v:.2f}" for v, c in scores[:6]))
