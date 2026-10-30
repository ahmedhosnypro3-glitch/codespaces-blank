#!/usr/bin/env python3
"""Slide 009 — PIL adjudication of the attempt-2 Template A (full-slide) FAIL.

The judge (qa/slide009/judge_attempt_2.txt, banked) raised four findings:
  #1 MAJOR ~0.7  red measurement arrows are "double-headed" and the "long
                 vertical deviation arrow" + "perpendicular double arrow" are
                 missing; recreation substituted single diagonal arrows
  #2 MINOR-MAJOR rotated text labels beside those vertical arrows (would be 50.85/63.64)
  #3 MINOR 0.55  the red diamond marker is an ADDED element not in the source
  #4 MINOR 0.6   the original encloses each caption in a thin outlined rectangle;
                 the recreation draws only partial rules
Nothing is edited until every finding is measured against BOTH images here.

Method: pixel census in FRAME px (1px=1pt). ORIG = unique_slides/slide_009.jpg
(960x540). RENDER = render_2.png (2001x1125, scale 2.08438 x / 2.08333 y) — the
render is mapped back to frame px per axis so both images are measured in the
same coordinate space. Red = the annotation family (C00000 = 192,0,0); dark =
non-navy non-red glyph ink.
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = Image.open(os.path.join(DECK, "unique_slides", "slide_009.jpg")).convert("RGB")
REN = Image.open(os.path.join(HERE, "render_2.png")).convert("RGB")
OW, OH = ORIG.size
RW, RH = REN.size
SX, SY = RW / 960.0, RH / 540.0

A = np.asarray(ORIG).astype(int)
B = np.asarray(REN).astype(int)


def frame_px(img_arr, scale_x, scale_y):
    """Down-sample a render array back to frame resolution (area mean)."""
    h = 540
    w = int(round(img_arr.shape[1] * 540.0 / img_arr.shape[0]))
    im = Image.fromarray(img_arr.astype(np.uint8)).resize((w, h), Image.BOX)
    return np.asarray(im).astype(int)


Af = A  # original is already 960x540
Bf = frame_px(B, SX, SY)


def masks(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    grey = (np.abs(r - g) < 14) & (np.abs(g - b) < 14) & (np.abs(r - b) < 14)
    red = (r > 110) & (r - g > 55) & (r - b > 55)
    # pale-rose family: warm, r>g>b with a modest split (halos + pale strokes)
    rose = (r > 150) & (r - g > 18) & (r - b > 16) & (g > 90)
    navy = (b > 85) & (b - r > 45) & (b - g > 45)
    dark = (~grey) & (~red) & (~rose) & (~navy) & (r < 150) & (g < 150) & (b < 160)
    return grey, red, navy, dark, rose


gr, re_a, nv, dk, ro_a = masks(Af)
gr2, re_b, nv2, dk2, ro_b = masks(Bf)


def col_runs(mask, y0, y1, x0, x1, min_h):
    """columns inside the box whose masked-pixel run spans >= min_h rows."""
    sub = mask[y0:y1, x0:x1]
    h = sub.shape[0]
    cols, heights = [], []
    for cx in range(sub.shape[1]):
        col = sub[:, cx]
        # longest contiguous run
        best = cur = 0
        for v in col:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best >= min_h:
            cols.append(x0 + cx)
            heights.append(best)
    return cols, heights


def row_runs(mask, y0, y1, x0, x1, min_w):
    sub = mask[y0:y1, x0:x1]
    rows, widths = [], []
    for ry in range(sub.shape[0]):
        row = sub[ry, :]
        best = cur = 0
        for v in row:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best >= min_w:
            rows.append(y0 + ry)
            widths.append(best)
    return rows, widths


def components(mask, y0, y1, x0, x1, min_px):
    """coarse 4-connected components (numpy label via iterative flood)."""
    sub = mask[y0:y1, x0:x1].copy()
    H, W = sub.shape
    lab = np.zeros((H, W), dtype=int)
    out = []
    cur = 0
    for sy in range(H):
        for sx in range(W):
            if sub[sy, sx] and not lab[sy, sx]:
                cur += 1
                stack = [(sy, sx)]
                lab[sy, sx] = cur
                pix = 0
                minx = maxx = sx
                miny = maxy = sy
                while stack:
                    yy, xx = stack.pop()
                    pix += 1
                    minx, maxx = min(minx, xx), max(maxx, xx)
                    miny, maxy = min(miny, yy), max(maxy, yy)
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = yy + dy, xx + dx
                        if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = cur
                            stack.append((ny, nx))
                if pix >= min_px:
                    out.append((x0 + minx, y0 + miny, x0 + maxx, y0 + maxy, pix))
    return out


print("=" * 78)
print("ADJUDICATION — slide 009 attempt-2 Template A FAIL (both images, frame px)")
print("=" * 78)
print("original %dx%d   render_2 %dx%d -> frame px %s" % (OW, OH, RW, RH, Bf.shape[1:]))
print()

# ── FINDING 1: the "long vertical double-headed arrow" / "perpendicular double arrow"
# The build draws per panel: a 2pt pale-red DIAGONAL stroke, a diamond, one 3pt
# diagonal arrow with a triangular head. The original's panel layout:
#   LEFT chart interior  x98..463 y111..470 ; navy border x95..465.5 y107..473.5
#   RIGHT chart interior x489.5..867.5 y111..470
# A long vertical deviation arrow would be a red column run of large height.
print("FINDING 1 — 'missing long vertical double-headed arrow'")
for name, (x0, y0, x1, y1) in (("LEFT", (99, 112, 462, 469)), ("RIGHT", (491, 112, 866, 469))):
    ca, ha = col_runs(re_a, y0, y1, x0, x1, 60)
    cb, hb = col_runs(re_b, y0, y1, x0, x1, 60)
    print("  %s chart: red columns with run >= 60px" % name)
    print("    ORIG  : %s" % (list(zip(ca, ha))[:12],))
    print("    RENDER: %s" % (list(zip(cb, hb))[:12],))
print("  NOTE: the vertical axis (1pt, ~285px tall) appears in both by design;")
print("        a SECOND tall column present in ORIG but absent in RENDER would be")
print("        a real omission. Compare the lists above (paired per panel).")
print()

# total red ink census per chart (ink that exists on the frame)
print("  red-ink totals inside each chart interior (orig vs render):")
for name, (x0, y0, x1, y1) in (("LEFT", (99, 112, 462, 469)), ("RIGHT", (491, 112, 866, 469))):
    sa = re_a[y0:y1, x0:x1].sum()
    sb = re_b[y0:y1, x0:x1].sum()
    print("    %s  orig=%6d px   render=%6d px   (render-orig=%+d)" % (name, sa, sb, sb - sa))
print()
print("  PALE-ROSE census (the annotation-stroke family, incl. halos):")
for name, (x0, y0, x1, y1) in (("LEFT", (99, 112, 462, 469)), ("RIGHT", (491, 112, 866, 469))):
    sa = ro_a[y0:y1, x0:x1].sum()
    sb = ro_b[y0:y1, x0:x1].sum()
    print("    %s  orig=%6d px   render=%6d px   (render-orig=%+d)" % (name, sa, sb, sb - sa))
# vertical-structure census on the ROSE mask: a "long vertical arrow" would be a
# column with a long contiguous rose run, distinct from the axis column.
car, har = col_runs(ro_a, 112, 469, 99, 462, 50)
cbr, hbr = col_runs(ro_b, 112, 469, 99, 462, 50)
print("  LEFT rose columns with contiguous run >= 50px")
print("    ORIG  : %s" % (list(zip(car, har))[:12],))
print("    RENDER: %s" % (list(zip(cbr, hbr))[:12],))
car, har = col_runs(ro_a, 112, 469, 491, 866, 50)
cbr, hbr = col_runs(ro_b, 112, 469, 491, 866, 50)
print("  RIGHT rose columns with contiguous run >= 50px")
print("    ORIG  : %s" % (list(zip(car, har))[:12],))
print("    RENDER: %s" % (list(zip(cbr, hbr))[:12],))
print("  A BLOCKER 'missing vertical arrow' would show as a rose column present in")
print("  ORIG and absent in RENDER (paired above); a diffuse ink deficit alone is")
print("  halo/interpolation, not an omitted element.")
print()
print("  HORIZONTAL red run census (the claimed perpendicular/double arrows):")
for name, (x0, y0, x1, y1) in (("LEFT", (99, 112, 462, 469)), ("RIGHT", (491, 112, 866, 469))):
    ra, wa = row_runs(re_a, y0, y1, x0, x1, 40)
    rb, wb = row_runs(re_b, y0, y1, x0, x1, 40)
    print("    %s ORIG  rows w/ red run>=40: %s" % (name, list(zip(ra, wa))[:14]))
    print("    %s RENDER rows w/ red run>=40: %s" % (name, list(zip(rb, wb))[:14]))
print()
print("  Diagonal-stroke ink parity at the measured pale-red annotation strokes:")
for name, (x0, y0, x1, y1) in (("LEFT diag (199,198)-(232,241)", (196, 195, 236, 245)),
                               ("RIGHT diag (626,208)-(646,264)", (622, 204, 650, 268))):
    na = int((~gr[y0:y1, x0:x1]).sum())
    nb = int((~gr2[y0:y1, x0:x1]).sum())
    print("    %-34s orig non-neutral=%d  render=%d" % (name, na, nb))
print()

# ── FINDING 2: rotated labels beside the arrows (glyph ink outside the eq box)
# Equation boxes: LEFT x216..317 y148..175 ; RIGHT x631..734 y147..175.
print("FINDING 2 — 'rotated text labels beside the arrows'")
print("  dark (non-navy, non-red) glyph components inside each chart, EXCLUDING")
print("  the equation box, min 12px — orig vs render:")
boxL = (216, 148, 317, 175)
boxR = (631, 147, 734, 175)
for name, (x0, y0, x1, y1), box in (("LEFT", (99, 112, 462, 469), boxL), ("RIGHT", (491, 112, 866, 469), boxR)):
    m = dk.copy()
    m[box[1]:box[3] + 1, box[0]:box[2] + 1] = False
    ca = components(m, y0, y1, x0, x1, 12)
    m2 = dk2.copy()
    m2[box[1]:box[3] + 1, box[0]:box[2] + 1] = False
    cb = components(m2, y0, y1, x0, x1, 12)
    print("    %s ORIG  comps=%d %s" % (name, len(ca), sorted(ca)[:10]))
    print("    %s RENDER comps=%d %s" % (name, len(cb), sorted(cb)[:10]))
print()

# ── FINDING 3: the diamond marker — solid ink on the frame, or an arrowhead?
# LEFT diamond measured at cx187 cy155 d9; RIGHT cx602.5 cy149.5 d8.
print("FINDING 3 — diamond marker ink vs the original's mark at the same box")
for name, cx, cy, d in (("LEFT", 187, 155, 9), ("RIGHT", 602, 149, 8)):
    cx = int(round(cx)); cy = int(round(cy))
    r = int(d * 2.2)
    ya, yb = max(0, cy - r), min(540, cy + r)
    xa, xb = max(0, cx - r), min(960, cx + r)
    oa = re_a[ya:yb, xa:xb]
    ob = re_b[ya:yb, xa:xb]
    print("  %s  box x%d..%d y%d..%d: orig red=%d render red=%d"
          % (name, xa, xb, ya, yb, oa.sum(), ob.sum()))
    # rotation-symmetric check: rotate the ORIG patch by 45 deg; if the ink is an
    # axis-aligned diamond, the rotated patch keeps ~the same ink profile, while
    # a round dot ALSO survives — so also report the aspect ratio of the ink bbox.
    ys, xs = np.nonzero(oa)
    if len(xs):
        print("       orig ink bbox w=%d h=%d (diamond vs round disc shape)" % (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1))
print()

# ── FINDING 4: caption enclosure — rectangle (4 sides) vs rules only
# Caption band: LEFT text x~87..441 (centre 264), RIGHT x~494..850 (centre 671),
# caption rows ~476..534. Rose/annotation ink is NOT neutral-grey.
print("FINDING 4 — caption enclosure: rectangle (4 sides) or rules only")
for name, (x0, y0, x1, y1) in (("LEFT", (87, 476, 441, 534)), ("RIGHT", (494, 476, 850, 534))):
    # pass the FULL masks (row_runs/col_runs slice internally)
    ann_a, ann_b = ~gr, ~gr2
    ra, wa = row_runs(ann_a, y0, y1, x0, x1, 60)   # horizontal rules
    rb, wb = row_runs(ann_b, y0, y1, x0, x1, 60)
    ca, ha = col_runs(ann_a, y0, y1, x0, x1, 18)   # vertical strokes
    cb, hb = col_runs(ann_b, y0, y1, x0, x1, 18)
    # also count with a lower bar so thin (2px-tall) rules are caught reliably
    ra2, wa2 = row_runs(ann_a, y0, y1, x0, x1, 200)
    rb2, wb2 = row_runs(ann_b, y0, y1, x0, x1, 200)
    print("  %s caption bbox x%d..%d y%d..%d" % (name, x0, x1, y0, y1))
    print("    ORIG   horizontal rules (>=60px): %s" % list(zip(ra, wa)))
    print("    RENDER horizontal rules (>=60px): %s" % list(zip(rb, wb)))
    print("    ORIG   horizontal rules (>=200px): %s" % list(zip(ra2, wa2)))
    print("    RENDER horizontal rules (>=200px): %s" % list(zip(rb2, wb2)))
    print("    ORIG   vertical strokes (>=18px): %s" % list(zip(ca, ha)))
    print("    RENDER vertical strokes (>=18px): %s" % list(zip(cb, hb)))
print()
print("  A closed rectangle needs verticals at BOTH left and right edges AND a")
print("  top rule; an 'L'/'U' (one or two verticals + a bottom rule) is not a")
print("  rectangle. Compare the stroke lists per side.")
print()
print("(end of adjudication input — verdict written by the worker with these numbers)")
