#!/usr/bin/env python3
"""Fresh-lane independent verification for slide 016 (worker judge016-fresh-lane-20261024).

Deliberately does NOT reuse the prior lane's measurement code: this is a second
independent implementation used to spot-check the banked conclusions before any
vision leg is spent.

Checks (960x540 frame space, 1px = 1pt; render 2001x1125 at scale H_render/540):
  A. all three original black underline segments present in the render;
  B. NO render ink stroke crosses the inner content-box border near x=830,
     and the wide runs near y=532 / y=538 are the box's purple bottom border
     and the red house bottom stroke (both present in the original);
  C. 12/12 body-text bands carry ink (the L7-L10 band included);
  D. house chrome: panel extent, left/right/bottom red strokes, NO top stroke,
     badge circle;
  E. Procedure B crop pairs are byte-reproducible from render_6 and the
     original at matched effective scale.

Usage: python3 verify_fresh_016.py
"""
import hashlib
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

QA = Path(__file__).resolve().parent
DECK = QA.parents[2]
ORIG = DECK / "unique_slides" / "slide_016.jpg"
RENDER = QA / "render_6.png"

ORIG_UNDERLINES = [(500, 446, 640), (500, 710, 806), (525, 110, 162)]
BODY_BANDS = [
    (104, 117), (129, 146), (179, 197), (230, 248), (256, 273),
    (281, 298), (332, 350), (357, 374), (408, 426), (434, 447),
    (484, 502), (510, 527),
]
REGIONS = [
    ("last_bullet", 80, 475, 820, 532),
    ("full_body", 80, 98, 815, 532),
]

failures = []
notes = []


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def dark(a):
    if a.ndim == 3:
        return a.mean(axis=2) < 150
    return a.mean(axis=1) < 150


def runs_in_row(mask_row, min_px):
    out, start = [], None
    for i, hit in enumerate(mask_row):
        if hit and start is None:
            start = i
        elif not hit and start is not None:
            if i - start >= min_px:
                out.append((start, i - 1))
            start = None
    if start is not None and len(mask_row) - start >= min_px:
        out.append((start, len(mask_row) - 1))
    return out


orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
rend = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
S = rend.shape[0] / orig.shape[0]
print(f"original {orig.shape[1]}x{orig.shape[0]}   render {rend.shape[1]}x{rend.shape[0]}   S={S:.4f}")
print(f"render md5 {md5(RENDER)}")

# ---------------------------------------------------------------- A + B
print("\n[A/B] black underline geometry, both images (frame px)")


def neutral(a):
    mx, mn = a.max(axis=2), a.min(axis=2)
    return (mx < 140) & ((mx - mn) <= 20)


def h_runs(a, scale, x0, x1, y0, y1, min_frame_px=12):
    seg = a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    m = neutral(seg)
    minpx = max(3, int(min_frame_px * scale))
    found = []
    for r in range(m.shape[0]):
        for s, e in runs_in_row(m[r], minpx):
            found.append((r / scale + y0, s / scale + x0, e / scale + x0))
    merged = []
    for y, a0, a1 in found:
        if merged and abs(merged[-1][0] - y) <= 1.6 and abs(merged[-1][2] - a0) < 6:
            p = merged[-1]
            merged[-1] = ((p[0] + y) / 2, min(p[1], a0), max(p[2], a1))
        else:
            merged.append((y, a0, a1))
    return merged


o_runs = h_runs(orig, 1.0, 80, 830, 470, 540)
r_runs = h_runs(rend, S, 80, 830, 470, 540)
print("  original neutral runs:")
for y, a0, a1 in o_runs:
    print(f"    y={y:6.1f} x={a0:6.1f}..{a1:6.1f} w={a1-a0:6.1f}")
print("  render neutral runs:")
for y, a0, a1 in r_runs:
    print(f"    y={y:6.1f} x={a0:6.1f}..{a1:6.1f} w={a1-a0:6.1f}")

for ey, ex0, ex1 in ORIG_UNDERLINES:
    hit = None
    for y, a0, a1 in r_runs:
        if abs(y - ey) <= 2.0:
            ov = min(a1, ex1) - max(a0, ex0)
            if ov > 0 and (hit is None or ov > hit[0]):
                hit = (ov, y, a0, a1)
    if hit is None:
        failures.append(f"underline y={ey} x={ex0}..{ex1} NOT found in render")
        print(f"  MISSING y={ey} x={ex0}..{ex1}")
    else:
        ov, y, a0, a1 = hit
        print(f"  FOUND   y={ey} x={ex0}..{ex1} -> y={y:.1f} x={a0:.1f}..{a1:.1f} overlap={ov:.1f}")
        if ov < 0.8 * (ex1 - ex0):
            failures.append(f"underline y={ey} overlap {ov:.1f}/{ex1-ex0}")

# inner border crossing: scan ALL dark-ish ink (not only neutral) in the
# last-bullet band and look for horizontal continuity crossing x=830.
print("\n[B] inner-border crossing test (x 820..845, y 470..540)")
for tag, a, s in (("original", orig, 1.0), ("render", rend, S)):
    print(f"  {tag}: any ink run in x820..845 that continues left of x820")
    seg = a[int(470 * s):int(540 * s), int(820 * s):int(846 * s)]
    m = dark(seg)
    for r in range(m.shape[0]):
        cols = np.where(m[r])[0]
        if len(cols):
            fy = r / s + 470
            fx0 = cols[0] / s + 820
            fx1 = cols[-1] / s + 820
            px = a[int(fy * s), int(fx0 * s):int(fx1 * s + 1)]
            print(f"    y={fy:6.1f} x={fx0:6.1f}..{fx1:6.1f} rgb={tuple(int(v) for v in px[len(px)//2])}")

# the wide runs at y~532 and y~538: identify their colour class
print("\n[B] colour class of wide runs near y=532 / y=538 (render)")
for yy in (531, 532, 533, 538, 539):
    row = rend[int(yy * S)]
    for x0, x1, lbl in ((200, 260, "mid-box"), (840, 880, "right-of-box")):
        px = row[int(x0 * S):int(x1 * S)]
        m = dark(px)
        if m.sum() > 5:
            vals = px[m]
            print(f"  y={yy} x~{x0}: {m.sum()} dark px, median rgb={tuple(int(v) for v in vals.mean(axis=0))}")

# ---------------------------------------------------------------- C
print("\n[C] body-text band ink (x88..828)")
for y0, y1 in BODY_BANDS:
    os_ = orig[y0:y1, 88:828]
    rs = rend[int(y0 * S):int(y1 * S), int(88 * S):int(828 * S)]
    oi = int((os_.mean(axis=2) < 170).sum())
    ri = int((rs.mean(axis=2) < 170).sum())
    ok = ri >= 500
    print(f"  y={y0:3d}..{y1:3d}: original={oi:5d} render={ri:5d} {'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(f"body band y={y0}..{y1} render ink {ri}")

# ---------------------------------------------------------------- D
print("\n[D] house chrome")
op = orig[45:540, 54:904]
print(f"  panel orig x54..903 gray: sample rgb={tuple(int(v) for v in orig[300, 700])}")
rp = rend[int(45 * S):int(540 * S), int(54 * S):int(904 * S)]
print(f"  panel render sample rgb={tuple(int(v) for v in rend[int(300 * S), int(700 * S)])}")
for tag, a, s in (("original", orig, 1.0), ("render", rend, S)):
    top = a[40:50, 60:900]
    red_top = int(((top[:, :, 0] > 140) & (top[:, :, 1] < 80) & (top[:, :, 2] < 80)).sum())
    print(f"  {tag}: red px in top band (y40..50) = {red_top} (house rule: no top stroke)")
    if tag == "render" and red_top > 0:
        failures.append(f"render has {red_top} red px in top band -> top stroke present")
    bottom = a[536:540, 60:900]
    red_bot = int(((bottom[:, :, 0] > 140) & (bottom[:, :, 1] < 80) & (bottom[:, :, 2] < 80)).sum())
    print(f"  {tag}: red px in bottom band (y536..540) = {red_bot}")

# ---------------------------------------------------------------- E
print("\n[E] Procedure B crop-pair reproducibility from render_6")
r_im = Image.open(RENDER).convert("RGB")
o_im = Image.open(ORIG).convert("RGB")
for name, x0, y0, x1, y1 in REGIONS:
    rb = (round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S))
    rc = r_im.crop(rb)
    oc = o_im.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    er = (rc.size[0] / (x1 - x0), rc.size[1] / (y1 - y0))
    eo = (oc.size[0] / (x1 - x0), oc.size[1] / (y1 - y0))
    scale_ok = abs(er[0] - eo[0]) < 0.01 and abs(er[1] - eo[1]) < 0.01
    print(f"  {name}: render-crop {rc.size} orig-up {oc.size} eff x={er[0]:.4f}/{eo[0]:.4f} "
          f"y={er[1]:.4f}/{eo[1]:.4f} matched={scale_ok}")
    if not scale_ok:
        failures.append(f"crop {name} effective scale mismatch")
    for kind, img in (("render", rc), ("orig", oc)):
        p = QA / f"crop_6_{name}_{kind}.png"
        if not p.exists():
            failures.append(f"missing crop {p.name}")
            continue
        bank = Image.open(p).convert("RGB")
        if bank.size != img.size:
            failures.append(f"crop {p.name} size {bank.size} != re-derived {img.size}")
            continue
        ba = np.asarray(bank).astype(int)
        na = np.asarray(img).astype(int)
        diff = int((np.abs(ba - na).max(axis=2) > 0).sum())
        print(f"    {p.name}: max-diff px vs re-derived = {diff}")
        if diff > 0:
            failures.append(f"crop {p.name} not pixel-identical to re-derivation ({diff} px differ)")

# ---------------------------------------------------------------- payloads
print("\n[F] payload byte-cleanliness")
for fn, exp in (("judge_prompt_6A.txt", "9387f5fbb94ef05a31db19f1e018dde1"),
                ("judge_prompt_6B.txt", "481172b034aa3336f54591d4e8e4bc98")):
    p = QA / fn
    got = md5(p)
    txt = p.read_text()
    print(f"  {fn}: md5 {got} expected {exp} match={got == exp} bytes={len(txt.encode())} "
          f"BLOC1ER={txt.count('BLOC1ER')} NNN={txt.count('NNN')} "
          f"Ktok={len(re.findall(r'K', txt))}")
    if got != exp:
        failures.append(f"{fn} md5 {got} != {exp}")
    if "BLOC1ER" in txt:
        failures.append(f"{fn} contains BLOC1ER")

print("\nRESULT")
if failures:
    for f in failures:
        print("  FAIL:", f)
    sys.exit(1)
print("  PASS: independent verification of render currency, underlines, border, bands, chrome, crops, payloads")
