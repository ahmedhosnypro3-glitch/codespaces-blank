#!/usr/bin/env python3
"""Render-side closed-loop self-check for slide 001 attempt 1 (resume worker, 2026-10-19) — v2.

v1 failed on its own window/mask bugs (padded per-line windows catching neighbor lines;
logo window spilling into the white canvas beyond the panel). Per the checker laws
(building.md): identical predicates/windows on BOTH images, probe boxes from the draw
code's CURRENT coordinates, and no windows that catch neighbors or canvas.

Method: run the SAME color masks on the 150dpi render AND the original JPEG frame,
extract row bands in the SAME slide-space regions, and compare 1:1. JPEG-antialias
bleed cancels on both sides. Tolerance: 4 frame px (8 render px, the pipeline standard).

Checks:
  1. FRAME CONTAINMENT: every content ink class inside the stroke-safe panel interior.
  2. BAND LIST MATCH: render band list == original band list (count, y-extents, x-extents).
  3. ONE-BAND-PER-ELEMENT: each expected text line appears as exactly one band in a
     midline-separated window (windows cut at adjacent-band midpoints so neighbors
     cannot intrude).
  4. LOGO BOX: logo ink (teal/white classes) inside its measured box x592..889 y456..533.
Equations/delimiters/tables: none on this slide (title slide) — N/A by spec.
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
R = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide001/render_1.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(f"{VID}/unique_slides/slide_001.jpg").convert("RGB")).astype(int)
H, W = R.shape[:2]
S = H / 540.0
fails = []
say_out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    say_out.append(s)

say(f"render {W}x{H} scale {S:.4f}; identical masks on render and original")

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    blue = (b > 120) & ((b - r) > 60) & ((b - g) > 60)
    teal = (r < 150) & (g > 150) & (b > 150)
    white = (r > 240) & (g > 240) & (b > 240)
    return red, blue, teal, white

redR, blueR, tealR, whiteR = masks(R)
redO, blueO, tealO, whiteO = masks(O)

# stroke-safe interior (frame px): strokes at x58.5/x901 and y538.5
IL, IR, IT, IB = 63, 896, 47, 534

def strip_strokes(mask, frame_h=540):
    """remove the three house strokes (render only; original strokes are same geometry)"""
    m = mask.copy()
    m[:, :int(IL * S)] = False
    m[:, int(IR * S):] = False
    m[int(IB * S):, :] = False
    return m

redR = strip_strokes(redR)
redO = strip_strokes(redO)
# original's JPEG text ink bleeds differently but the same dominance mask is applied.

def bands(mask, x0f, x1f, y0f, y1f, scale):
    x0, x1, y0, y1 = int(x0f * scale), int(x1f * scale), int(y0f * scale), int(y1f * scale)
    sub = mask[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) > 2)[0]
    if not len(rows):
        return []
    seg = []
    start = rows[0]; prev = rows[0]
    for y in rows[1:]:
        if y > prev + 3:
            seg.append((start, prev)); start = y
        prev = y
    seg.append((start, prev))
    out = []
    for a0, a1 in seg:
        cols = np.where(sub[a0:a1 + 1].sum(axis=0) > 0)[0]
        out.append(((y0 + a0) / scale, (y0 + a1) / scale, (x0 + cols.min()) / scale, (x0 + cols.max()) / scale))
    return out

# regions scanned in slide-space (frame px); identical on both images
REGIONS = [
    ("red text", redO, redR, (60, 895, 100, 534)),
    ("blue text", blueO, blueR, (60, 895, 300, 534)),
]

# --- 1. containment (render) ---
for name, mask in (("red", redR), ("blue", blueR)):
    ys, xs = np.where(mask)
    ok = xs.min() / S >= IL and xs.max() / S <= IR and ys.min() / S >= IT and ys.max() / S <= IB
    say(f"containment {name}: frame bbox x {xs.min()/S:.0f}..{xs.max()/S:.0f} y {ys.min()/S:.0f}..{ys.max()/S:.0f} "
        f"-> interior(x{IL}..{IR},y{IT}..{IB}): {'OK' if ok else 'OVERFLOW'}")
    if not ok:
        fails.append(f"{name} ink outside stroke-safe interior")

# --- 2. band-list match, region by region ---
TOL = 4.0
for name, mo, mr, (x0, x1, y0, y1) in REGIONS:
    bo = bands(mo, x0, x1, y0, y1, 1.0)     # original: frame px 1:1
    br = bands(mr, x0, x1, y0, y1, S)       # render: scaled
    say(f"{name}: original {len(bo)} bands vs render {len(br)} bands")
    if len(bo) != len(br):
        fails.append(f"{name}: band count orig {len(bo)} vs render {len(br)}")
    for i, (ob, rb) in enumerate(zip(bo, br)):
        d = [rb[k] - ob[k] for k in range(4)]
        bad = max(abs(v) for v in d) > TOL
        say(f"  band {i}: orig y {ob[0]:.0f}..{ob[1]:.0f} x {ob[2]:.0f}..{ob[3]:.0f} | "
            f"render y {rb[0]:.0f}..{rb[1]:.0f} x {rb[2]:.0f}..{rb[3]:.0f} | "
            f"d(y0,y1,x0,x1)=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) {'DRIFT>4' if bad else 'OK'}")
        if bad:
            fails.append(f"{name} band {i}: drift ({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})")

# --- 3. one-band-per-element with midline-separated windows ---
# expected line bands (frame px) — midpoints between adjacent same-class bands as cuts
LINES = {
    "title L1": ("red", (127, 171)),
    "title L2": ("red", (178, 219)),
    "title L3": ("red", (231, 274)),
    "preparedby": ("red", (354, 373)),
    "instr hdr": ("red", (422, 437)),
    "subtitle": ("blue", (314, 335)),
    "name ctr": ("blue", (378, 400)),
    "email ctr": ("blue", (404, 417)),
    "instr name1": ("blue", (449, 468)),
    "instr email1": ("blue", (472, 486)),
    "instr name2": ("blue", (494, 509)),
    "instr email2": ("blue", (516, 531)),
}
# midlines between consecutive red bands and consecutive blue bands (from measured lists)
RED_CUTS = [(171 + 178) / 2, (219 + 231) / 2, (323.5 + 354) / 2, (373 + 422) / 2]  # between L1/L2, L2/L3, title/pbd, pbd/hdr
BLUE_CUTS = [(335 + 378) / 2, (400 + 404) / 2, (418.5 + 449) / 2, (468 + 472) / 2, (486 + 494) / 2, (509 + 516) / 2]

def window(band, cuts):
    y0, y1 = band
    lo, hi = y0 - 16, y1 + 16
    for c in cuts:
        if lo < c < y0:
            lo = c
        if y1 < c < hi:
            hi = c
    return max(lo, 40), min(hi, 534)

for name, (cls, band) in LINES.items():
    mask = redR if cls == "red" else blueR
    cuts = RED_CUTS if cls == "red" else BLUE_CUTS
    y0w, y1w = window(band, cuts)
    xc = (60, 895)
    bs = bands(mask, xc[0], xc[1], y0w, y1w, S)
    if len(bs) != 1:
        fails.append(f"{name}: {len(bs)} bands in midline window (expected 1)")
        say(f"{name}: BAND COUNT {len(bs)} (expected 1) — window y {y0w:.0f}..{y1w:.0f}")
    else:
        say(f"{name}: 1 band OK (window y {y0w:.0f}..{y1w:.0f}, band y {bs[0][0]:.0f}..{bs[0][1]:.0f})")

# --- 4. logo box ---
# scan INSIDE the panel only (canvas beyond x903 is legitimately white); the logo
# neighborhood below/right of other content: x560..899, y445..537 (frame px)
LOGO_BOX = (592, 456, 889, 533)
for tag, im, teal, white, scale in (("render", R, tealR, whiteR, S), ("orig", O, tealO, whiteO, 1.0)):
    m = teal | white
    win = m[int(445 * scale):int(537 * scale), int(560 * scale):int(899 * scale)]
    ys, xs = np.where(win)
    y0f, y1f = 445 + ys.min() / scale, 445 + ys.max() / scale
    x0f, x1f = 560 + xs.min() / scale, 560 + xs.max() / scale
    say(f"logo {tag} ink bbox frame-px x {x0f:.0f}..{x1f:.0f} y {y0f:.0f}..{y1f:.0f}")
    if tag == "render":
        ok = x0f >= LOGO_BOX[0] - 2 and x1f <= LOGO_BOX[2] + 2 and y0f >= LOGO_BOX[1] - 2 and y1f <= LOGO_BOX[3] + 2
        say(f"logo render ink vs box x{LOGO_BOX[0]}..{LOGO_BOX[2]} y{LOGO_BOX[1]}..{LOGO_BOX[3]} (+2 chamfer): {'OK' if ok else 'OVERFLOW'}")
        if not ok:
            fails.append(f"logo ink outside box: x {x0f:.0f}..{x1f:.0f} y {y0f:.0f}..{y1f:.0f}")

say("")
if fails:
    say("SELFCHECK RENDER v2: FAIL")
    for f in fails:
        say("  -", f)
    raise SystemExit(1)
say("SELFCHECK RENDER v2: PASS (containment, band-list match, one-band-per-element, logo box)")
