#!/usr/bin/env python3
"""Closed-loop PIL verification for slide 029: ORIGINAL frame vs RECREATION render.

Original: unique_slides/slide_029.jpg, 960x540  -> 72 px/in (1 px = 1 pt)
Render:   build/slide_029_rejudge_rendered-1.png, 2001x1125 -> 150.075 px/in

Every feature is located by (a) an exact target RGB with a per-image colour
tolerance, (b) a region window in inches that isolates that feature from every
other element of the same colour family, and (c) a minimum fill area.  Reported
deviations are in px @150 dpi; tolerance is 4 px @150 dpi = 0.0267 in.

Colour targets come from analysis/slide_029_final.json's `colors` block, which is
the contract for this recreation (the video frame's JPEG/projector hexes deviate
a few units from it - e.g. magenta measures #F59AF8, error bar #9F0000 - and the
spec, not the capture, wins).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_029.jpg"
REND = f"{V}/recreated_pptx/build/slide_029_rejudge_rendered-1.png"

TOL_PX = 4.0                 # px @150 dpi
TOL_IN = TOL_PX / 150.0
FRAME_BOTTOM = 7.35          # house red frame inner bottom, inches

failures = []


def load(path):
    img = Image.open(path).convert("RGB")
    a = np.asarray(img).astype(int)
    ppi = a.shape[1] / 13.3333
    return a, ppi


O, OPPI = load(ORIG)
R, RPPI = load(REND)
print(f"ORIGINAL {O.shape[1]}x{O.shape[0]} -> {OPPI:.2f} px/in")
print(f"RENDER   {R.shape[1]}x{R.shape[0]} -> {RPPI:.2f} px/in")
print(f"TOLERANCE: {TOL_PX:.0f} px @150 dpi ({TOL_IN:.4f} in)\n")


def find(a, ppi, rgb, tol, region, min_area_in2, minsize=0):
    """Connected components of the target colour inside region (x0,y0,x1,y1, in).

    Returns list of (x0,y0,x1,y1) in PIXELS.
    """
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (np.abs(a - np.array(rgb)).sum(axis=2) <= tol)
    x0, y0, x1, y1 = region
    xs = np.arange(a.shape[1], dtype=float) / ppi
    ys = np.arange(a.shape[0], dtype=float) / ppi
    m &= (xs[None, :] >= x0) & (xs[None, :] <= x1)
    m &= (ys[:, None] >= y0) & (ys[:, None] <= y1)
    lab, _ = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        if sl is None:
            continue
        ys_, xs_ = sl
        if (lab[sl] == i).sum() < max(minsize, min_area_in2 * ppi * ppi):
            continue
        out.append((xs_.start, ys_.start, xs_.stop - 1, ys_.stop - 1))
    out.sort(key=lambda z: (z[1], z[0]))
    return out


def inches(box, ppi):
    return tuple(round(v / ppi, 3) for v in box)


def dev_px(o, r, oppi, rppi):
    return max(abs(a / oppi - b / rppi) for a, b in zip(o, r)) * 150.0


def report(name, o_boxes, r_boxes, oppi, rppi, expect=None):
    print(f"--- {name} ---")
    print(f"    ORIGINAL : {len(o_boxes)} " + str([inches(b, oppi) for b in o_boxes]))
    print(f"    RENDER   : {len(r_boxes)} " + str([inches(b, rppi) for b in r_boxes]))
    if expect is not None and (len(o_boxes) != expect or len(r_boxes) != expect):
        failures.append(f"{name}: count original={len(o_boxes)} render={len(r_boxes)} expected={expect}")
        print(f"    COUNT    : original={len(o_boxes)} render={len(r_boxes)} expected={expect}  MISMATCH")
    else:
        print(f"    COUNT    : {'OK' if expect is not None else 'n/a'}")
    used = set()
    for ob in o_boxes:
        best, bestd = None, 1e9
        for i, rb in enumerate(r_boxes):
            if i in used:
                continue
            d = dev_px(ob, rb, oppi, rppi)
            if d < bestd:
                best, bestd = i, d
        if best is None:
            failures.append(f"{name}: original element {inches(ob, oppi)} has no render counterpart")
            print(f"    POSITION : original {inches(ob, oppi)} UNMATCHED")
            continue
        used.add(best)
        rb = r_boxes[best]
        status = "OK" if bestd <= TOL_PX else "OUT"
        print(f"    POSITION : orig {inches(ob, oppi)} vs rend {inches(rb, rppi)} -> "
              f"{bestd:5.1f}px @150dpi  {status}")
        if bestd > TOL_PX:
            failures.append(f"{name}: deviation {bestd:.1f}px > {TOL_PX:.0f}px "
                            f"(orig {inches(ob, oppi)}, rend {inches(rb, rppi)})")
    print()
    return r_boxes


# ---------------------------------------------------------------- features
TOTAL = 13.33

FEATURES = [
    # name, rgb, orig tol, rend tol, region, min area in^2, expected count
    ("pale-yellow formula boxes (bottom row)", (255, 253, 231), 40, 14,
     (0.5, 5.9, 12.8, 7.5), 0.30, 3),
    ("dark-red 'Error Error Error' bar", (192, 0, 0), 45, 45,
     (7.55, 1.90, 8.10, 5.40), 0.15, 1),
    ("pale-green class boxes", (217, 234, 211), 55, 20,
     (7.90, 1.90, 9.20, 5.40), 0.08, 3),
    ("magenta Input Sample / Target Label boxes", (230, 160, 230), 45, 25,
     (0.60, 1.10, 9.80, 2.00), 0.08, 2),
    ("beige legend box", (242, 228, 208), 25, 25,
     (8.90, 1.60, 12.60, 3.60), 0.50, 1),
    ("white node-count note box", (255, 255, 255), 30, 30,
     (8.50, 3.60, 12.50, 4.60), 0.40, 1),
    ("light-blue 'Previous Layer' callout", (221, 235, 247), 25, 25,
     (2.80, 5.30, 4.60, 6.40), 0.10, 1),
    ("light-green 'Current Layer' callout", (226, 239, 218), 75, 20,
     (5.00, 5.30, 7.00, 6.40), 0.10, 1),
    ("white section header boxes (bottom row)", (255, 255, 255), 30, 30,
     (0.60, 5.60, 12.50, 6.50), 0.15, 2),
]

for name, rgb, to, tr, region, minarea, expect in FEATURES:
    ob = find(O, OPPI, rgb, to, region, minarea)
    rb = find(R, RPPI, rgb, tr, region, minarea)
    report(name, ob, rb, OPPI, RPPI, expect=expect)

# ------------------------------------------------- beige network panel
# (isolated by colour/brightness: beige only, no other slide element in region)
def beige_mask(a, ppi):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 195) & (r > g) & (g > b) & ((r - b) > 8) & ((r - b) < 48) & (r < 250)


def region_apply(m, a, ppi, region):
    x0, y0, x1, y1 = region
    xs = np.arange(a.shape[1], dtype=float) / ppi
    ys = np.arange(a.shape[0], dtype=float) / ppi
    m &= (xs[None, :] >= x0) & (xs[None, :] <= x1)
    m &= (ys[:, None] >= y0) & (ys[:, None] <= y1)
    return m


PANEL_REGION = (0.50, 1.50, 8.60, 6.00)


def panel(a, ppi):
    m = region_apply(beige_mask(a, ppi), a, ppi, PANEL_REGION)
    lab, _ = ndimage.label(m)
    best = None
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        if sl is None:
            continue
        npx = int((lab[sl] == i).sum())
        if npx < 20000:
            continue
        if best is None or npx > best[4]:
            ys_, xs_ = sl
            best = (xs_.start, ys_.start, xs_.stop - 1, ys_.stop - 1, npx)
    return [best[:4]] if best else []


report("beige network-diagram panel",
        panel(O, OPPI), panel(R, RPPI), OPPI, RPPI, expect=1)

# ------------------------------------------------- frame containment
def paleyellow_boxes(a, ppi):
    return find(a, ppi, (255, 253, 231), 50, (0.5, 5.9, 12.8, 7.5), 0.30)


o_py = paleyellow_boxes(O, OPPI)
r_py = paleyellow_boxes(R, RPPI)
print("--- house-frame containment of the bottom formula row ---")
o_b = max((b[3] for b in o_py), default=0) / OPPI
r_b = max((b[3] for b in r_py), default=0) / RPPI
r_t = min((b[1] for b in r_py), default=0) / RPPI
r_l = min((b[0] for b in r_py), default=0) / RPPI
r_r = max((b[2] for b in r_py), default=0) / RPPI
print(f"    bottom formula row in render: x {r_l:.2f}-{r_r:.2f} in, y {r_t:.2f}-{r_b:.2f} in")
print(f"    house frame interior       : x 0.15-13.18 in, y 0.15-7.35 in")
print(f"    original lowest yellow ink : {o_b:.3f} in | render {r_b:.3f} in "
      f"-> {abs(r_b - o_b) * 150:.1f}px @150dpi")
ok = r_b <= FRAME_BOTTOM + 0.004
print(f"    inside frame bottom (7.35in): {'YES' if ok else 'NO - OVERFLOW'}")
print(f"    right edge inside 13.18in   : {'YES' if r_r <= 13.18 else 'NO'}")
if not ok:
    failures.append(f"bottom formula row overflows house frame: {r_b:.3f} in > {FRAME_BOTTOM} in")
if abs(r_b - o_b) * 150 > TOL_PX:
    failures.append(f"bottom-row bottom edge deviation {abs(r_b - o_b) * 150:.1f}px")
print()

# ------------------------------------------------- wording / line counts
def text_rows(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1 + 1, x0:x1 + 1]
    prof = (sub.sum(axis=2) < 470).sum(axis=1)
    runs, run = [], 0
    for v in prof:
        if v > 0:
            run += 1
        elif run:
            runs.append(run)
            run = 0
    if run:
        runs.append(run)
    return len(runs)


o_mg = find(O, OPPI, (230, 160, 230), 45, (0.60, 1.10, 9.80, 2.00), 0.08)
r_mg = find(R, RPPI, (230, 160, 230), 25, (0.60, 1.10, 9.80, 2.00), 0.08)
print('--- "Input Sample" / "Target Label" wording (must be TWO lines each) ---')
names = ("Input Sample", "Target Label")
for i, tag in enumerate(names):
    if i >= len(o_mg) or i >= len(r_mg):
        failures.append(f"{tag}: box missing")
        continue
    tro, trr = text_rows(O, o_mg[i]), text_rows(R, r_mg[i])
    print(f"    {tag:13s} original text rows={tro} | render text rows={trr} "
          f"{'OK' if tro == trr else 'MISMATCH'}")
    if tro != trr:
        failures.append(f"{tag}: text line count original={tro} render={trr}")
print()

# ------------------------------------------------- duplicate scan
print("--- duplicate scan (component census across each element family) ---")
FAMS = [("dark-red error bar", (192, 0, 0), (7.55, 1.90, 8.10, 5.40), 0.05, 45, 45),
        ("pale-green class box", (217, 234, 211), (7.90, 1.90, 9.20, 5.40), 0.03, 55, 20),
        ("pale-yellow formula box", (255, 253, 231), (0.5, 5.9, 12.8, 7.5), 0.05, 40, 14),
        ("light-green fill (nodes+callout)", (226, 239, 218), (0.5, 1.5, 12.8, 7.5), 0.03, 75, 20),
        ("light-blue fill", (221, 235, 247), (0.5, 1.5, 12.8, 7.5), 0.03, 25, 25)]
EXP = {"dark-red error bar": 1, "pale-green class box": 3, "pale-yellow formula box": 3}
for label, rgb, region, minarea, to, tr in FAMS:
    oc = find(O, OPPI, rgb, to, region, minarea)
    rc = find(R, RPPI, rgb, tr, region, minarea)
    exp = EXP.get(label)
    note = f" (expected {exp})" if exp else " (context only)"
    print(f"    {label:32s} original={len(oc)} render={len(rc)}{note}")
    if exp is not None and len(rc) != exp:
        failures.append(f"{label}: {len(rc)} components in render, expected {exp}")
print()

print("=" * 78)
if failures:
    print(f"VERIFY RESULT: {len(failures)} FAILURE(S)")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("VERIFY RESULT: PASS - every measured feature matches the original "
      f"within {TOL_PX:.0f} px @150 dpi")
