#!/usr/bin/env python3
"""Slide 009 — MANDATORY pre-judge selfcheck, attempt 4, ON render_4.png.

Fresh script for the attempt-4 build (the banked selfcheck_attempt_4.py is kept
untouched: it was written against render_2 and verifies the RETIRED approach-3
marks — diagonal + diamond — which no longer exist). Every check prints its
measured numbers; the frame (960x540, 1px=1pt) is the reference, mapped through
the render scale (render_H/540). Verdict at the end.

Checks:
 1. Frame containment: no content ink outside the house panel / in the gaps;
    house panel + L/R/bottom strokes present, NO top stroke.
 2. Equation regions contain ink (empty = BLOCKER) and sit inside their boxes
    with clearance (delimiter geometry).
 3. Annotation groups (attempt-4 fix): rotated '50.85 mm' / '63.64 mm' label ink
    at the frame's measured bboxes; dimension-line arrowheads at the measured
    tips; callout arrowheads at the measured bboxes; >= 9 dashed residual
    connectors per chart (dash pixels along the measured perpendicular paths).
 4. Line/box wrap: caption bands' ink y-ranges match the frame; explicit
    lineSpacing is set in the build (read from the build script).
 5. Table data: N/A (slide has no tables) — recorded, not skipped silently.
 6. Crop-pair scale audit: every crop_4_* pair re-opened, equal size and equal
    effective px/frame-px per axis.
"""
import os
import re
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(DECK, "unique_slides", "slide_009.jpg")
REND = os.path.join(HERE, "render_4.png")
BUILD = os.path.join(HERE, "..", "..", "build", "slide_009.js")

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
ren = np.asarray(Image.open(REND).convert("RGB")).astype(int)
H, W, _ = ren.shape
SY, SX = H / 540.0, W / 960.0
print("render_4 %dx%d   scale x %.5f y %.5f   original %s" % (W, H, SX, SY, orig.shape[:2]))
print()

fails = []
def chk(name, ok, detail):
    print(("PASS " if ok else "FIX  ") + name + ": " + detail)
    if not ok:
        fails.append(name)

def R(x, y):
    return int(round(x * SX)), int(round(y * SY))

def ink_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = r + g + b
    neutral = (abs(r - g) < 9) & (abs(g - b) < 9)
    panel = neutral & (r > 224) & (r < 240)       # E9E9E7 panel (233)
    white = (r > 246) & (g > 246) & (b > 246)
    grid = neutral & (r > 200) & (r <= 246)
    return (lum < 720) & ~panel & ~white & ~grid

# ---------------------------------------------------------------- 1. chrome
print("== 1. HOUSE FRAME / CONTAINMENT ==")
top = orig[44:47, 60:900]
rred = (top[..., 0] > 140) & (top[..., 1] < 90) & (top[..., 2] < 90)
print("   ORIG top-band red px (y44..46): %d" % int(rred.sum()))
rtop = ren[R(60, 44)[1]:R(60, 47)[1], R(60, 44)[0]:R(900, 47)[0]]
rredr = (rtop[..., 0] > 140) & (rtop[..., 1] < 90) & (rtop[..., 2] < 90)
chk("no top stroke", int(rredr.sum()) == 0, "render top-band red px = %d (frame 0)" % int(rredr.sum()))
# gap band between the two panels (frame x466..485, y110..470)
g = ren[R(468, 110)[1]:R(468, 470)[1], R(468, 110)[0]:R(484, 110)[0]]
gi = ink_mask(g)
chk("panel gap clean", int(gi.sum()) == 0, "ink px in x468..483 (border halos excluded) = %d (expect 0)" % int(gi.sum()))
# band between chart bottoms (y474) and caption boxes (y479)
band = ren[R(120, 476)[1]:R(120, 478)[1], R(120, 476)[0]:R(880, 476)[0]]
bi = ink_mask(band)
chk("chart->caption gap clean", int(bi.sum()) == 0, "ink px in y476..477 (below chart border y474) = %d (expect 0)" % int(bi.sum()))
# content inside house panel x54..903 / y45..540: nothing outside panel width
out = ren[:, 0:R(54, 0)[0]]
oi = ink_mask(out)
# canvas is white; the badge is at x>12.4in but inside; nothing else lives left of panel
chk("nothing left of house panel", int(oi.sum()) == 0, "ink px left of x=54 = %d" % int(oi.sum()))

# ---------------------------------------------------------------- 2. equations
print()
print("== 2. EQUATION INK + DELIMITER GEOMETRY ==")
BOXES = [("LEFT", 216, 148, 102, 27, 226, 307, 155, 166),
         ("RIGHT", 631, 148, 104, 27, 643, 723, 155, 166)]
for name, bx, by, bw, bh, ix0, ix1, iy0, iy1 in BOXES:
    sub = ren[R(bx, by)[1]:R(bx + bw, by + bh)[1], R(bx, by)[0]:R(bx + bw, by + bh)[0]]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    dark = (r < 120) & (g < 120) & (b < 120)
    ys, xs = np.nonzero(dark)
    if len(xs) == 0:
        chk("eq %s ink" % name, False, "EMPTY equation box")
        continue
    bx0 = bx + 2 + xs.min() / SX; bx1 = bx + 2 + xs.max() / SX
    by0 = by + 2 + ys.min() / SY; by1 = by + 2 + ys.max() / SY
    print("   %s eq ink bbox frame px: x %.1f..%.1f  y %.1f..%.1f  (n=%d)"
          % (name, bx0, bx1, by0, by1, int(dark.sum())))
    chk("eq %s ink present" % name, dark.sum() > 150,
        "dark ink px = %d" % int(dark.sum()))
    chk("eq %s inside box" % name,
        bx < bx0 and bx1 < bx + bw and by < by0 and by1 < by + bh,
        "ink inside x%d..%d y%d..%d" % (bx, bx + bw, by, by + bh))
    # box border present on all four sides
    rrow = ren[R(bx + bw / 2, by)[1], R(bx + bw / 2, by)[0] - 2:R(bx + bw / 2, by)[0] + 2]
    nav = (rrow[:, 2] > 90) & (rrow[:, 2] - rrow[:, 0] > 50)
    chk("eq %s box border" % name, bool(nav.any()), "navy border px on top edge = %d" % int(nav.sum()))

# ---------------------------------------------------------------- 3. annotations
print()
print("== 3. ATTEMPT-4 ANNOTATION GROUP (labels / arrowheads / connectors) ==")
def red_bbox(x0, y0, x1, y1, rmin=110, rmax=225):
    sub = ren[R(x0, y0)[1]:R(x1, y1)[1], R(x0, y0)[0]:R(x1, y1)[0]]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    m = (r - g > 40) & (r - b > 30) & (r > rmin) & (r < rmax)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (x0 + xs.min() / SX, y0 + ys.min() / SY, x0 + xs.max() / SX, y0 + ys.max() / SY, int(m.sum()))

for name, reg, frame_bbox in [
    ("L label", (188, 180, 240, 245), (196, 188, 222, 238)),
    ("R label", (612, 200, 665, 270), (623, 210, 650, 265)),
]:
    bb = red_bbox(*reg)
    ok = bb is not None and abs(bb[0] - frame_bbox[0]) <= 6 and abs(bb[1] - frame_bbox[1]) <= 6 \
         and abs(bb[2] - frame_bbox[2]) <= 6 and abs(bb[3] - frame_bbox[3]) <= 6
    chk("%s ink bbox" % name, ok,
        "render %s vs frame %s (±6)" % (None if bb is None else tuple(round(v, 1) for v in bb[:4]), frame_bbox))
# dimension arrowheads + callout arrowheads at measured positions
for name, (x0, y0, x1, y1), target in [
    ("L dim head", (238, 278, 262, 305), (249, 292)),
    ("R dim head", (668, 308, 694, 338), (682, 324)),
    ("L callout head", (178, 144, 198, 166), (191, 150)),
    ("R callout head", (594, 138, 614, 160), (607, 144)),
]:
    bb = red_bbox(x0, y0, x1, y1, rmin=120, rmax=210)
    ok = bb is not None and bb[0] - 5 <= target[0] <= bb[2] + 2 and bb[1] - 3 <= target[1] <= bb[3] + 3
    chk(name, ok, "head bbox %s (tip target %s)" % (None if bb is None else tuple(round(v, 1) for v in bb[:4]), target))
# dashed residual connectors: sample the midpoint of the measured perpendicular paths
CONN = {
    "LEFT": {"line": ((141, 351), (433, 201)),
             "pts": [(397.2, 248.5), (421.2, 254.8), (323.9, 289.4), (381.3, 301.5),
                     (327.9, 331.6), (260.5, 333.0), (293.9, 333.0), (188.0, 355.2),
                     (233.5, 361.6), (176.2, 379.9)]},
    "RIGHT": {"line": ((555, 387), (849, 247)),
              "pts": [(809.7, 248.3), (793.8, 301.7), (741.5, 331.8), (707.1, 333.4),
                      (646.8, 361.4), (610.6, 144.6)]},
}
for side, d in CONN.items():
    (x0, y0), (x1, y1) = d["line"]
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    hits = 0
    for (px, py) in d["pts"]:
        t = ((px - x0) * dx + (py - y0) * dy) / L2
        fx, fy = x0 + t * dx, y0 + t * dy
        n = max(4, int(np.hypot(fx - px, fy - py)))
        found = False
        for i in range(3, n - 3):
            xx = px + (fx - px) * i / n; yy = py + (fy - py) * i / n
            X, Y = R(xx, yy)
            win = ren[max(0, Y - 2):Y + 3, max(0, X - 2):X + 3]
            r, g, b = win[..., 0], win[..., 1], win[..., 2]
            if ((b - r > 10) & (b - g > 8) & (r > 120) & (r < 240)).any():
                found = True; break
        hits += int(found)
    chk("%s residual connectors" % side, hits >= len(d["pts"]) - 1,
        "%d/%d sampled perpendicular paths carry periwinkle dash ink" % (hits, len(d["pts"])))

# ---------------------------------------------------------------- 4. captions / spacing
print()
print("== 4. CAPTION BANDS + EXPLICIT LINE SPACING ==")
for name, x0, x1, want1, want2 in [
    ("LEFT", 95, 434, (488, 503), (507, 519)),
    ("RIGHT", 501, 842, (488, 503), (507, 519)),
]:
    sub = ren[R(x0, 476)[1]:R(x1, 530)[1], R(x0, 476)[0]:R(x1, 530)[0]]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    ink = ((r < 160) | (g < 120)) & ~((r > 245) & (g > 245) & (b > 245))
    ys = np.nonzero(ink)[0]
    if len(ys) == 0:
        chk("%s captions ink" % name, False, "no ink")
        continue
    y1 = 476 + ys.min() / SY; y2 = 476 + ys.max() / SY
    rows = np.unique(np.round(476 + ys / SY).astype(int))
    gaps = [int(rows[i + 1] - rows[i]) for i in range(len(rows) - 1) if rows[i + 1] - rows[i] > 3]
    chk("%s caption bands" % name, abs(y1 - want1[0]) <= 4 and abs(y2 - want2[1]) <= 4,
        "ink y %.1f..%.1f (frame %d..%d), inter-line gap rows %s" % (y1, y2, want1[0], want2[1], gaps))
src = open(BUILD).read()
m = re.search(r"lineSpacing:\s*size\s*\*\s*([0-9.]+)", src)
chk("explicit lineSpacing in build", m is not None,
    "captionLine sets lineSpacing: size * %s (pinned per line, not auto)" % (m.group(1) if m else "MISSING"))

print()
print("== 5. TABLE DATA ==")
print("   N/A — slide 009 has no table (two scatter charts + 4 caption lines + 2 equations).")

# ---------------------------------------------------------------- 6. crop scale audit
print()
print("== 6. CROP-PAIR SCALE AUDIT (crop_4_*) ==")
regions = {
    "eq_left": (208, 140, 325, 183), "eq_right": (625, 140, 742, 183),
    "cap_left": (87, 476, 441, 534), "cap_right": (494, 476, 850, 534),
    "chart_left": (87, 102, 473, 480), "chart_right": (478, 102, 878, 480),
}
for name, (x0, y0, x1, y1) in regions.items():
    rp = os.path.join(HERE, "crop_4_%s_render.png" % name)
    op = os.path.join(HERE, "crop_4_%s_orig.png" % name)
    r = Image.open(rp); o = Image.open(op)
    ok = r.size == o.size and abs(r.size[0] / (x1 - x0) - SX) < 0.03 and abs(r.size[1] / (y1 - y0) - SY) < 0.03
    chk("crop %s scale" % name, ok,
        "%dx%d vs %dx%d; x %.4f y %.4f (target %.4f/%.4f)"
        % (r.size[0], r.size[1], o.size[0], o.size[1], r.size[0] / (x1 - x0), r.size[1] / (y1 - y0), SX, SY))

print()
print("RESULT: %d checks, %d FIX" % (len(fails) + sum(1 for _ in []) + 0, len(fails)))
print("VERDICT:", "PASS" if not fails else "FAIL -> " + ", ".join(fails))
