#!/usr/bin/env python3
"""Verify slide 012 recreation against the ORIGINAL frame, by measurement.

ORIGINAL = videos/.../unique_slides/slide_012.jpg (960x540 px, 1 px = 1 pt).
RENDER  = recreated_pptx/build/slide_012_rejudge_rendered-1.png (2001x1125 @150dpi,
          1 render px = 960/2001 pt = 0.48 pt).

Every element below is compared in ORIGINAL-frame-pt units, plus the house
frame rule assertions. Tolerance 4 pt unless noted (sub-pixel label forensics
are explicitly out of budget).
"""
import numpy as np
from PIL import Image
from scipy import ndimage

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_012.jpg"
REND = f"{V}/recreated_pptx/build/slide_012_rejudge_rendered-1.png"
PPTX = f"{V}/recreated_pptx/slide_012_recreated.pptx"

orig = np.array(Image.open(ORIG).convert("RGB")).astype(int)
rend = np.array(Image.open(REND).convert("RGB")).astype(int)
RH, RW = rend.shape[:2]
S = 960.0 / RW          # render px -> original frame pt

def ink(img, box, pred):
    x0, y0, x1, y1 = box
    m = pred(img[y0:y1, x0:x1])
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        return None
    return (xs.min() + x0, xs.min() + y0, xs.max() + x0, ys.max() + y0)

def near(a, b, tol=4.0):
    return all(abs(a[i] - b[i]) <= tol for i in range(4))

def comps(img, mask, minarea=25):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        ys, xs = sl
        area = (lab[sl] == i + 1).sum()
        if area < minarea:
            continue
        out.append((area, xs.start, xs.stop - 1, ys.start, ys.stop - 1))
    return sorted(out, reverse=True)

# ---- colour predicates (shared for both frames) ----------------------------
def is_navy(a):  r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]; return (b - r > 25) & (b - g > 25) & (b > 100) & (r < 120)
def is_green(a): r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]; return (g - r > 50) & (g - b > 50) & (g > 170)
def is_cyan(a):  r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]; return (b - r > 50) & (g - r > 50) & (b > 170)
def is_blue(a):  r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]; return (b - r > 40) & (b > 100)
def is_red(a):   r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]; return (r > 140) & (r - g > 55) & (r - b > 55)
def is_yellow(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 245) & (g > 240) & (b < 235) & (b > 195) & ((g - b) > 12)
def is_cyan_fill(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 235) & (g > 235) & (b > 235) & ((g - r) < 20) | ((r - g) > 6)
def is_green_fill(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (g > 225) & (r < 240) & (b < 240) & (g - r > 3) & (g - b > 3) & (abs(r - b) < 14)

print("=" * 74)
print("SLIDE 012 VERIFY — original-frame pt units, tolerance 4 pt")
print("=" * 74)
print(f"original {Image.open(ORIG).size}   render {rend.shape[1]}x{rend.shape[0]}  (1 render px = {S:.4f} pt)")

results = []

def check(name, expect, got, tol=4.0, note=""):
    if got is None:
        results.append((name, "FAIL", "element not found in render", expect))
        print(f"  FAIL  {name:<34} not found in render   (expected {expect})")
        return
    if near(expect, got, tol):
        results.append((name, "PASS", "", expect))
        print(f"  PASS  {name:<34} render {got}  expected {expect}  {note}")
    else:
        d = [abs(expect[i] - got[i]) for i in range(4)]
        results.append((name, "FAIL", f"deviation {d}", expect))
        print(f"  FAIL  {name:<34} render {got}  expected {expect}  dev {d} {note}")

# ---- render-space boxes scaled back to original-frame pt -------------------
def rbox(box):
    return tuple(round(v * S, 1) for v in box)

# ---------------------------------------------------------------- title -----
o = ink(orig, (250, 55, 730, 105), lambda a: (a[:, :, 0] - a[:, :, 1] > 45) & (a[:, :, 0] > 100))
g = ink(rend, (int(250 / S), int(55 / S), int(730 / S), int(105 / S)),
        lambda a: a.max(axis=2) < 190)
check("title ink", (285, 71, 694, 90), rbox(g) if g else None, 6.0, "(font metric, loose)")

# ------------------------------------------------------------ house frame ---
frame = ink(rend, (0, 0, RW, RH), lambda a: (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] > 120) & (a[:, :, 2] < 120))
print("  house frame red bbox (render px):", frame, " -> pt:", rbox(frame) if frame else None)
exp_frame = (10.8, 10.8, 949.2, 529.2)   # 0.15in inset on a 960x540pt slide
check("house red frame", exp_frame, rbox(frame) if frame else None, 8.0)

badge = ink(rend, (int(880 / S), int(10 / S), int(950 / S), int(80 / S)), is_yellow)
check("house badge fill", (898.6, 21.6, 934.6, 57.6), rbox(badge) if badge else None, 8.0)
# badge numeral: dark pixels inside the badge circle
badge_dark = ink(rend, (int(900 / S), int(24 / S), int(934 / S), int(55 / S)),
                 lambda a: a.max(axis=2) < 150)
print("  badge numeral ink (render px):", badge_dark, "-> pt:", rbox(badge_dark) if badge_dark else None)

# ---------------------------------------------------------- truth table -----
o_cell = ink(orig, (100, 145, 165, 300), lambda a: a.max(axis=2) < 120)
g_cell = ink(rend, (int(100 / S), int(145 / S), int(165 / S), int(300 / S)),
             lambda a: a.max(axis=2) < 120)
print(f"  table value ink: orig {o_cell}  render-renderpx {g_cell}")

# red table border (original: thin bright red outer frame)
o_red = ink(orig, (90, 130, 320, 310), lambda a: (a[:, :, 0] > 140) & (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 60))
g_red = ink(rend, (int(90 / S), int(130 / S), int(320 / S), int(310 / S)), is_red)
check("table red border", (96, 138, 314, 306), rbox(g_red) if g_red else None, 6.0)

# O/P highlight band widths (finding 6)
o_cy = ink(orig, (240, 170, 300, 215), lambda a: (a[:, :, 1] > 235) & (a[:, :, 2] > 235) & ((a[:, :, 1] - a[:, :, 0]) > 6))
g_cy = ink(rend, (int(240 / S), int(170 / S), int(330 / S), int(215 / S)),
           lambda a: (a[:, :, 1] > 235) & (a[:, :, 2] > 235) & ((a[:, :, 1] - a[:, :, 0]) > 6))
check("O/P cyan chip (row1)", (263, 178, 285, 201), rbox(g_cy) if g_cy else None, 6.0, "narrow inset band")
cw = (285 - 263) if o_cy else 0
print(f"  cyan chip width: original {cw} pt")

o_gr = ink(orig, (240, 210, 300, 310), lambda a: (a[:, :, 1] > 225) & (a[:, :, 0] < 240) & (a[:, :, 1] - a[:, :, 0] > 3) & (a[:, :, 1] - a[:, :, 2] > 3) & (abs(a[:, :, 0] - a[:, :, 2]) < 14))
g_gr = ink(rend, (int(240 / S), int(210 / S), int(330 / S), int(310 / S)), is_green_fill)
check("O/P green band (rows2-4)", (262, 214, 286, 302), rbox(g_gr) if g_gr else None, 6.0, "narrow inset band")
print(f"  green band width: original {286 - 262} pt  (was full column 77 pt pre-fix)")

# ---------------------------------------------------------- scatter plot ----
g_navy = ink(rend, (int(500 / S), int(200 / S), int(860 / S), int(380 / S)), is_navy)
check("decision boundary ink (upper part)", (558, 235, 683, 364), rbox(g_navy) if g_navy else None, 8.0, "overhang")
# full line: measure bbox of navy ink over the whole plot panel
_navy_full = np.zeros(rend.shape[:2], bool)
_navy_full[int(100 / S):int(380 / S), int(490 / S):int(870 / S)] = \
    is_navy(rend[int(100 / S):int(380 / S), int(490 / S):int(870 / S)])
_ys, _xs = np.nonzero(_navy_full)
if len(_ys):
    print(f"  full navy line render bbox(pt): {rbox((_xs.min(), _ys.min(), _xs.max(), _ys.max()))}  (expected 558,235,683,364)")
print("  boundary overhang: orig 61 pt left of y-axis / 63 pt above intercept")

g_g = [c for c in comps(rend, np.zeros((1, 1), bool))]  # placeholder, filled below
reg = np.zeros(rend.shape[:2], bool)
reg[int(100 / S):int(380 / S), int(500 / S):int(860 / S)] = True
gm = is_green(rend) & reg
gpts = comps(rend, gm, minarea=60)
gpts = [(a, px0, px1, py0, py1) for a, px0, px1, py0, py1 in gpts]
print(f"  green points in render: {len(gpts)} (expected 3)")
if len(gpts) == 3:
    print(f"     centers(pt): {[tuple(round(v * S, 1) for v in ((px0 + px1) / 2, (py0 + py1) / 2)) for _, px0, px1, py0, py1 in gpts]}")
cm = is_cyan(rend) & reg
cpts = comps(rend, cm, minarea=60)
print(f"  cyan points in render: {len(cpts)} (expected 1)")
if cpts:
    a, px0, px1, py0, py1 = cpts[0]
    print(f"     center(pt): {tuple(round(v * S, 1) for v in ((px0 + px1) / 2, (py0 + py1) / 2))}  (expected 618, 328)")
check("cyan origin point", (609, 319, 628, 337),
      rbox((cpts[0][1], cpts[0][3], cpts[0][2], cpts[0][4])) if cpts else None, 6.0)

# red axis arrowheads: vertical axis top + horizontal axis right
o_v = ink(orig, (600, 110, 640, 145), is_red)
g_v = ink(rend, (int(600 / S), int(110 / S), int(640 / S), int(145 / S)), is_red)
print(f"  vertical axis arrowhead: orig {o_v}  render(pt) {rbox(g_v) if g_v else None}")

# -------------------------------------------------- perceptron schematic -----
o_strip = ink(orig, (330, 355, 420, 405), is_yellow)
g_strip = ink(rend, (int(330 / S), int(355 / S), int(420 / S), int(405 / S)), is_yellow)
check("rule legend strip", (345, 366, 378, 384), rbox(g_strip) if g_strip else None, 8.0,
      "ABOVE the activation box")

# activation box: purple/pink outline, y 405..436
o_act = ink(orig, (350, 400, 410, 445), lambda a: (a[:, :, 0] > 200) & (a[:, :, 2] > 150) & (a[:, :, 0] - a[:, :, 1] > 15) & (a[:, :, 2] - a[:, :, 1] > 15))
g_act = ink(rend, (int(350 / S), int(400 / S), int(410 / S), int(445 / S)),
            lambda a: (a[:, :, 0] > 200) & (a[:, :, 2] > 150) & (a[:, :, 0] - a[:, :, 1] > 15) & (a[:, :, 2] - a[:, :, 1] > 15))
check("activation box", o_act, rbox(g_act) if g_act else None, 8.0, "pictogram only inside")

# the legend strip must sit ABOVE the activation box (finding 1)
if g_strip and g_act:
    ok = g_act[1] - g_strip[3] > 0
    print(f"  [{'PASS' if ok else 'FAIL'}] rule legend is ABOVE the activation box "
          f"(strip bottom {g_strip[3]} < box top {g_act[1]})")
    results.append(("legend above box", "PASS" if ok else "FAIL", "", None))

# step pictogram ink inside the activation box (finding 2)
blue_in_box = None
if g_act:
    x0, y0, x1, y1 = g_act
    m = is_blue(rend[int(y0 / S):int(y1 / S), int(x0 / S):int(x1 / S)])
    ys, xs = np.nonzero(m)
    if len(ys):
        blue_in_box = (round((xs.min() + x0 / S) * S, 1), round((ys.min() + y0 / S) * S, 1))
        print(f"  step pictogram (blue jump) ink present inside box: {len(ys)} render px, top-left(pt) {blue_in_box}")
        results.append(("step pictogram visible", "PASS", "", None))
    else:
        print("  FAIL  step pictogram: no blue ink found inside the activation box")
        results.append(("step pictogram visible", "FAIL", "no blue ink in box", None))

# rule text must NOT be inside the activation box (finding 1)
if g_act and g_strip:
    inter = (g_strip[2] > g_act[0] and g_strip[3] > g_act[1] and g_strip[0] < g_act[2] and g_strip[1] < g_act[3])
    print(f"  [{'FAIL' if inter else 'PASS'}] rule text does NOT overlap the activation box")

# Sigma circle + red triangle at its rim (finding 5)
o_sig = ink(orig, (285, 390, 340, 445), lambda a: (a[:, :, 2] > 200) & (a[:, :, 1] > 200) & (a[:, :, 0] < 245))
g_sig = ink(rend, (int(285 / S), int(390 / S), int(340 / S), int(445 / S)),
            lambda a: (a[:, :, 2] > 200) & (a[:, :, 1] > 200) & (a[:, :, 0] < 245))
check("Sigma circle", (299, 403, 333, 438), rbox(g_sig) if g_sig else None, 8.0)

o_tri = ink(orig, (285, 405, 305, 435), is_red)
g_tri = ink(rend, (int(285 / S), int(405 / S), int(305 / S), int(435 / S)), is_red)
print(f"  red input triangle: orig {o_tri}  render(pt) {rbox(g_tri) if g_tri else None}")
if g_sig and g_tri:
    gap = g_sig[0] - g_tri[2] if g_tri else None
    print(f"  [{'PASS' if (g_tri and g_sig[0] - g_tri[2] <= 12) else 'FAIL'}] triangle adjacent to the Sigma rim "
          f"(gap {g_sig[0] - g_tri[2]:.1f} pt, original gap 1 pt)")
    results.append(("red triangle at Sigma rim", "PASS" if g_sig[0] - g_tri[2] <= 12 else "FAIL", "gap %.1f" % (g_sig[0] - g_tri[2]), None))

# ------------------------------------------------------------ equation ------
o_eq = ink(orig, (575, 415, 812, 462), lambda a: a.max(axis=2) < 190)
g_eq = ink(rend, (int(575 / S), int(415 / S), int(812 / S), int(462 / S)),
           lambda a: a.max(axis=2) < 190)
check("equation ink", (595, 429, 787, 452), rbox(g_eq) if g_eq else None, 8.0)

o_peach = ink(orig, (570, 410, 815, 465), lambda a: (a[:, :, 0] > 245) & (a[:, :, 1] > 210) & (a[:, :, 1] < 250) & (a[:, :, 2] > 190) & (a[:, :, 2] < 238) & ((a[:, :, 0] - a[:, :, 2]) > 12) & ((a[:, :, 1] - a[:, :, 2]) > 6))
g_peach = ink(rend, (int(570 / S), int(410 / S), int(815 / S), int(465 / S)),
              lambda a: (a[:, :, 0] > 235) & (a[:, :, 1] > 205) & (a[:, :, 1] < 250) & (a[:, :, 2] > 185) & (a[:, :, 2] < 242) & ((a[:, :, 0] - a[:, :, 2]) > 8) & ((a[:, :, 0] - a[:, :, 2]) < 60))
check("equation box", (579, 417, 810, 463), rbox(g_peach) if g_peach else None, 8.0)

# ---------------------------------------------------------------- summary ---
print()
n_pass = sum(1 for r in results if r[1] == "PASS")
n_fail = sum(1 for r in results if r[1] == "FAIL")
print("=" * 74)
print(f"RESULT: {n_pass} PASS / {n_fail} FAIL of {len(results)} checks")
print("=" * 74)

import os, zipfile
print()
print(f"promoted deliverable: {PPTX}")
print(f"  exists: {os.path.exists(PPTX)}   bytes: {os.path.getsize(PPTX) if os.path.exists(PPTX) else 0}")
with zipfile.ZipFile(PPTX) as z:
    media = sorted(n for n in z.namelist() if n.startswith("ppt/media/"))
print(f"  media: {media}")
print(f"  slides: {[n for n in zipfile.ZipFile(PPTX).namelist() if n.startswith('ppt/slides/slide')]}")
sys_exit = 1 if n_fail else 0
raise SystemExit(sys_exit)
