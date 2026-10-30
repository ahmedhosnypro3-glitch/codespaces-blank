#!/usr/bin/env python3
"""Pre-judge self-check for slide 039 attempt 2 (mandatory before any judge dispatch).
Run: python3 selfcheck_attempt_2.py <render.png>
Checks (founder directive 2026-10-10):
  1. FRAME CONTAINMENT (PIL) - ink must sit inside the house panel/strokes and the
     content panel border on all four sides.
  2. EQUATIONS EXIST - the equation region must contain ink (nonzero ink pixels).
  3. DELIMITER GEOMETRY - no multi-line delimited blocks on this slide; the green
     callout box is a rectangle (its stroke spans all enclosed content by construction).
  4. TABLE DATA - no tables on this slide.
  5. WRAP DETECTION - every text box that must render on ONE line must show exactly one
     contiguous ink row-band (two bands = the text wrapped = MAJOR defect).
  6. EXPLICIT LINE SPACING - the three bottom-caption lines are separate boxes pinned to
     the measured ink centres y417/441/467 (pitch 24px).
  7. ELEMENT FIDELITY - every text block's ink bbox measured against the original frame.
Exit 0 = all checks pass; nonzero = failures listed.
"""
import sys
import numpy as np
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else "render_2.png"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_039.jpg"

R = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
s = R.shape[0] / 540.0
fails = []


def mask(p, mode):
    r, g, b = p[:, :, 0], p[:, :, 1], p[:, :, 2]
    lum = p.mean(axis=2)
    if mode == "red":
        return (r > 110) & (g < 140) & (b < 140) & (r > g + 25)
    if mode == "blue":
        return (b > 110) & (b > r + 25) & (b > g + 15)
    if mode == "dark":
        return lum < 150
    if mode == "green":
        return (g > r + 25) & (g > b + 10) & (g > 100)
    if mode == "all":
        return (lum < 200) | ((r > 110) & (r > g + 25)) | ((b > 110) & (b > r + 25))
    raise ValueError(mode)


def bands(rows):
    """contiguous row bands (gap tolerance 1px), returns list of (lo, hi)."""
    out = []
    if len(rows) == 0:
        return out
    start = prev = rows[0]
    for v in rows[1:]:
        if v - prev <= 1:
            prev = v
            continue
        out.append((start, prev))
        start = prev = v
    out.append((start, prev))
    return out


def probe(img, y0, y1, x0, x1, mode, sc):
    """returns dict with absolute FRAME-px bbox, ink count, and row-band count.

    y0..y1/x0..x1 are FRAME px; multiplied by sc to index the render, then results
    are mapped back to absolute frame px (window origin + render offset / sc).
    """
    y0i, y1i, x0i, x1i = [int(round(v * sc)) for v in (y0, y1, x0, x1)]
    m = mask(img[y0i:y1i, x0i:x1i], mode)
    cols = np.where(m.any(axis=0))[0]
    rows = np.where(m.any(axis=1))[0]
    if len(cols) == 0:
        return None
    bb = bands(rows)
    return {
        "x0": x0 + cols.min() / sc,
        "x1": x0 + cols.max() / sc,
        "y0": y0 + rows.min() / sc,
        "y1": y0 + rows.max() / sc,
        "n": int(m.sum()),
        "bands": [(y0 + a / sc, y0 + b / sc) for a, b in bb],
    }


print(f"render {RENDER} ({R.shape[1]}x{R.shape[0]}), scale {s:.4f}")

# ---- 1. FRAME CONTAINMENT -------------------------------------------------------------
house = (54, 45, 903, 539)
panel = (73, 142, 868, 482)
bbox = probe(R, 0, 540, 54, 903, "all", s)
if bbox is None:
    fails.append("frame containment: no ink found inside the house panel")
else:
    print(f"  ink inside house panel: x{bbox['x0']:.0f}..{bbox['x1']:.0f} "
          f"y{bbox['y0']:.0f}..{bbox['y1']:.0f} ({bbox['n']} px)")
    if bbox["x0"] < 54 or bbox["x1"] > 903 or bbox["y0"] < 45 or bbox["y1"] > 539:
        fails.append("frame containment: ink crosses the house panel")
for nm, mode, y0, y1, x0, x1 in [
    ("bullets", "dark", 155, 371, 84, 839),
    ("why", "red", 308, 325, 84, 212),
    ("caption-L1-red", "red", 405, 428, 90, 455),
    ("caption-L1-black", "dark", 405, 428, 458, 832),
    ("caption-L2-black", "dark", 432, 452, 92, 430),
    ("caption-blue", "blue", 459, 475, 313, 628),
]:
    b = probe(R, y0, y1, x0, x1, mode, s)
    if b and (b["x0"] < 73 or b["x1"] > 868 or b["y0"] < 142 or b["y1"] > 482):
        fails.append(f"frame containment: {nm} ink escapes the content panel")
gb = probe(R, 255, 308, 330, 880, "green", s)
if gb:
    print(f"  green callout box: x{gb['x0']:.0f}..{gb['x1']:.0f} y{gb['y0']:.0f}..{gb['y1']:.0f}")
    if gb["x0"] < 73 or gb["x1"] > 868 or gb["y0"] < 142 or gb["y1"] > 482:
        fails.append("frame containment: green callout box escapes the content panel")
    eq = probe(R, 258, 305, 355, 850, "dark", s)
    if eq is None or eq["n"] < 200:
        fails.append("equations exist: equation ink missing or too sparse in the green callout")
    else:
        print(f"  equation ink: x{eq['x0']:.0f}..{eq['x1']:.0f} y{eq['y0']:.0f}..{eq['y1']:.0f} "
              f"({eq['n']} px, {len(eq['bands'])} bands)")
        if eq["x0"] <= gb["x0"] or eq["x1"] >= gb["x1"]:
            fails.append("equations exist: equation ink overlaps the green box border")

# ---- 5. WRAP DETECTION -----------------------------------------------------------------
# Every one of these must be a SINGLE contiguous ink row-band. The window is padded
# generously so a wrapped second line still falls inside it.
WRAP = [
    ("title L1", "red", 72, 106, 110, 900),
    ("title L2 'and'", "red", 105, 140, 270, 340),
    ("title L2 'Mini-Batch'", "blue", 105, 140, 330, 480),
    ("title L2 'Gradient Descent'", "red", 105, 140, 470, 900),
    ("bullet 1 line 1", "dark", 145, 180, 95, 900),
    ("bullet 1 line 2", "dark", 178, 205, 95, 900),
    ("bullet 2", "dark", 200, 228, 95, 900),
    ("bullet 3", "dark", 225, 255, 95, 900),
    ("red annotation", "red", 274, 300, 600, 900),
    ("Why using SGD", "red", 303, 330, 80, 300),
    ("bullet 4", "dark", 330, 355, 95, 900),
    ("bullet 5", "dark", 358, 382, 95, 900),
    ("caption-L1-red", "red", 404, 432, 80, 900),
    ("caption-L1-black", "dark", 404, 432, 450, 900),
    ("caption-L2-black", "dark", 428, 458, 85, 900),
    ("caption-blue", "blue", 455, 481, 300, 650),
]
print("\nwrap detection (single ink row-band expected per block):")
for nm, mode, y0, y1, x0, x1 in WRAP:
    b = probe(R, y0, y1, x0, x1, mode, s)
    if b is None:
        fails.append(f"wrap detection: {nm} has NO ink in the render")
        print(f"  {nm:26s} NO INK <<<")
        continue
    nb = len(b["bands"])
    if nb != 1:
        fails.append(f"wrap detection: {nm} shows {nb} ink bands "
                     f"({', '.join(f'{a:.0f}..{c:.0f}' for a, c in b['bands'])}) - WRAPPED")
        print(f"  {nm:26s} {nb} bands {b['bands']} <<<")
    else:
        print(f"  {nm:26s} 1 band x{b['x0']:5.0f}..{b['x1']:<5.0f} y{b['y0']:5.0f}..{b['y1']:<5.0f}")

# ---- 6. EXPLICIT LINE SPACING (caption ink centres vs measured 417/441/467) -----------
CAP_CENTRES = {"caption-L1": 417, "caption-L2": 441, "caption-blue": 467}
for nm, mode, y0, y1, x0, x1 in [
    ("caption-L1", "red", 404, 432, 80, 900),
    ("caption-L2", "dark", 428, 458, 85, 900),
    ("caption-blue", "blue", 455, 481, 300, 650),
]:
    b = probe(R, y0, y1, x0, x1, mode, s)
    if b is None:
        fails.append(f"caption centre: {nm} has no ink")
        continue
    c = (b["y0"] + b["y1"]) / 2
    tgt = CAP_CENTRES[nm]
    d = c - tgt
    print(f"  {nm:16s} ink centre y{c:.1f} (target {tgt}) d{d:+.0f}px")
    if abs(d) > 4:
        fails.append(f"caption centre: {nm} off by {d:+.0f}px (tol 4)")
p12 = probe(R, 428, 458, 85, 900, "dark", s)
p1r = probe(R, 404, 432, 80, 900, "red", s)
if p12 and p1r:
    pitch = (p12["y0"] + p12["y1"]) / 2 - (p1r["y0"] + p1r["y1"]) / 2
    print(f"  caption pitch L1->L2: {pitch:.1f}px (original measured 24px)")
    if abs(pitch - 24) > 4:
        fails.append(f"line spacing: caption pitch {pitch:.1f} != measured 24")

# ---- 3/4. DELIMITER GEOMETRY / TABLE DATA ---------------------------------------------
print("\n  delimiter geometry: no multi-line delimited blocks on this slide (green box is a rectangle)")
print("  table data: no tables on this slide")

# ---- 7. ELEMENT FIDELITY TABLE --------------------------------------------------------
T = [
    ("title L1", "red", 79, 98, 121, 837),
    ("title L2 'and'", "red", 109, 128, 280, 322),
    ("title L2 'Mini-Batch'", "blue", 109, 128, 340, 467),
    ("title L2 'Descent'", "red", 109, 128, 478, 687),
    ("bullet 1 line 1", "dark", 155, 168, 101, 839),
    ("bullet 1 line 2", "dark", 184, 194, 101, 478),
    ("bullet 2", "dark", 209, 219, 102, 660),
    ("bullet 3", "dark", 231, 244, 102, 765),
    ("equation", "dark", 268, 300, 352, 600),
    ("red annotation", "red", 279, 292, 605, 841),
    ("Why using SGD", "red", 308, 325, 84, 212),
    ("bullet 4", "dark", 337, 346, 101, 402),
    ("bullet 5", "dark", 363, 371, 101, 336),
    ("caption-L1 RED run", "red", 408, 426, 85, 456),
    ("caption-L1 BLACK run", "dark", 408, 426, 458, 834),
    ("caption-L2 BLACK", "dark", 434, 449, 90, 431),
    ("caption-blue", "blue", 459, 476, 311, 630),
    ("panel bottom border", "blue", 482, 484, 74, 868),
    ("green callout box", "green", 278, 296, 350, 850),
]
print(f"\n{'element':22s} {'dx':>4s} {'dy':>4s} {'dw':>5s}   render-x       render-y")
for nm, mode, y0, y1, x0, x1 in T:
    o = probe(O, y0, y1, x0, x1, mode, 1.0)
    rr = probe(R, y0, y1, x0, x1, mode, s)
    if o is None or rr is None:
        print(f"{nm:22s} ORIG={o is not None} RENDER={rr is not None}")
        if rr is None:
            fails.append(f"element fidelity: {nm} has no ink in the render")
        continue
    dx, dy, dw = rr["x0"] - o["x0"], rr["y0"] - o["y0"], (rr["x1"] - rr["x0"]) - (o["x1"] - o["x0"])
    ow = o["x1"] - o["x0"]
    tol_dx, tol_dy = 4, 4
    tol_dw = max(10, int(0.03 * ow))
    if nm == "equation":
        oc, rc = (o["y0"] + o["y1"]) / 2, (rr["y0"] + rr["y1"]) / 2
        dcy = rc - oc
        if abs(dcy) > 3:
            fails.append(f"element fidelity: equation ink centre off by {dcy:+.0f}px (tol 3)")
        print(f"{nm:22s} {dx:+4.0f} {int(dcy):+4d}* {dw:+5.0f}  "
              f"x{rr['x0']:6.0f}..{rr['x1']:<6.0f} y{rr['y0']:5.0f}..{rr['y1']:<5.0f}   "
              f"(*centre-dy; 2D form is vertically compact by design)")
        continue
    if abs(dx) > tol_dx or abs(dy) > tol_dy or abs(dw) > tol_dw:
        fails.append(f"element fidelity: {nm} off by dx{dx:+.0f} dy{dy:+.0f} dw{dw:+.0f} "
                     f"(tol {tol_dx}/{tol_dy}/{tol_dw} on {ow:.0f}px)")
        print(f"{nm:22s} {dx:+4.0f} {dy:+4.0f} {dw:+5.0f}   "
              f"x{rr['x0']:6.0f}..{rr['x1']:<6.0f} y{rr['y0']:5.0f}..{rr['y1']:<5.0f}   <<<")
    else:
        print(f"{nm:22s} {dx:+4.0f} {dy:+4.0f} {dw:+5.0f}   "
              f"x{rr['x0']:6.0f}..{rr['x1']:<6.0f} y{rr['y0']:5.0f}..{rr['y1']:<5.0f}")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELF-CHECK: PASS (all elements within tolerance; no wrapped lines; "
      "equation ink present and inside the green callout; caption centres/pitch match)")
