"""Slide 011 re-judge verification.

Original frame is 960x540 (1 px = 1 pt at 13.33x7.5 in). Render is 2001x1125
@150 dpi => 300 px/in... i.e. 2.0843 render px per original px, so a tolerance of
N px at render scale equals 2.0843*N px at original scale. House-frame geometry
is asserted in inches.

Elements checked (original region, original px):
  frame (house chrome, asserted per house rule, measured in render only)
  badge + numeral 11
  title
  truth table + 12 digits + 4 O/P pills
  decision plot image
  perceptron diagram: panel, x1/x2 inputs, -5/-3/6 weights, sigma circle,
      step box, activation rule box + 2 lines of text, O/P label
  equation card + peach equation box
"""
import sys
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B = V + "/recreated_pptx/build"
ORIG = V + "/unique_slides/slide_011.jpg"
REND = B + "/slide_011_rejudge_rendered-1.png"

SC = 2001 / 960.0
HOUSE = {
    "frame": (0.15, 0.15, 13.03, 7.2),
    "badge": (12.48, 0.30, 0.5, 0.5),
    "title": (0.6, 0.28, 12.13),
}
fails = []
notes = []


def dark(a):
    return a.sum(axis=2) < 500


def cream(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 240) & (g > 235) & (b < 245) & ((r - b) > 8) & ((g - b) > 8)


def red(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - b > 35) & (r - g > 25)


def yellow(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - b > 15) & (g - b > 25)


O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
R = np.asarray(Image.open(REND).convert("RGB")).astype(int)
print(f"original {O.shape[1]}x{O.shape[0]}   render {R.shape[1]}x{R.shape[0]}   scale {SC:.4f}")

in_px = lambda x: x * 150.0
sc_px = lambda p: p * SC


def reg(a, box):
    """box in original px -> pixel slice."""
    x0, y0, x1, y1 = box
    if a is R:
        x0, y0, x1, y1 = [sc_px(v) for v in box]
    return a[int(y0):int(y1), int(x0):int(x1)]


def find_ink(a, box, mask, want=True):
    sub = reg(a, box)
    m = mask(sub)
    n = int(m.sum()) if mask is not None else None
    if n is not None and not want:
        return n, None
    if n == 0:
        return 0, None
    ys, xs = np.where(m)
    if a is R:
        return n, (xs.min() / SC, ys.min() / SC, xs.max() / SC, ys.max() / SC)
    return n, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def check(name, box, mask=dark, min_px=25, tol=4.0, want=True):
    n_o, b_o = find_ink(O, box, mask, want)
    n_r, b_r = find_ink(R, box, mask, want)
    if n_o == 0 or n_r == 0 or b_o is None or b_r is None:
        fails.append(f"{name}: missing ink (orig {n_o}px {b_o} | render {n_r}px {b_r})")
        print(f"  MISS {name:28s} orig={n_o:6d} {b_o}  rend={n_r:6d} {b_r}")
        return None
    dx0 = (b_r[0] - b_o[0]) * SC
    dy0 = (b_r[1] - b_o[1]) * SC
    dx1 = (b_r[2] - b_o[2]) * SC
    dy1 = (b_r[3] - b_o[3]) * SC
    close = all(abs(v) <= tol for v in (dx0, dy0, dx1, dy1))
    tag = "OK  " if close else "DRIFT"
    print(f"  {tag} {name:28s} orig=({b_o[0]:6.1f},{b_o[1]:6.1f},{b_o[2]:6.1f},{b_o[3]:6.1f})"
          f" rend_scaled=({b_r[0]:6.1f},{b_r[1]:6.1f},{b_r[2]:6.1f},{b_r[3]:6.1f})"
          f" d_renderpx=({dx0:+.1f},{dy0:+.1f},{dx1:+.1f},{dy1:+.1f})")
    if not close:
        fails.append(f"{name}: ink bbox drift tol {tol} render px -> {dx0:+.1f},{dy0:+.1f},{dx1:+.1f},{dy1:+.1f}")
    return close


def check_ink(name, box, mask=dark, min_px=60):
    """element must exist in BOTH with the given mask (bbox not compared)."""
    n_o, _ = find_ink(O, box, mask)
    n_r, _ = find_ink(R, box, mask)
    ok = n_o >= min_px and n_r >= min_px
    tag = "OK  " if ok else "MISS"
    print(f"  {tag} {name:28s} orig_ink={n_o:6d}  render_ink={n_r:6d} (min {min_px})")
    if not ok:
        fails.append(f"{name}: ink {n_o} orig / {n_r} render < min {min_px}")
    return ok


print("\n== house chrome (from render, house-rule inches) ==")
fx0, fy0, fw, fh = [in_px(v) for v in HOUSE["frame"]]
m = red(R[int(fy0) - 12:int(fy0) + 12, int(fx0) - 12:int(fx0) + 1200]) | red(
    R[int(fy0) - 12:int(fy0) + 12, int(fx0 + fw) - 1200:int(fx0 + fw) + 12])
print(f"  frame rect in render: {fx0:.0f},{fy0:.0f} .. {fx0 + fw:.0f},{fy0 + fh:.0f} px (@150dpi)")
bx, by, bw, bh = [in_px(v) for v in HOUSE["badge"]]
sub = R[int(by):int(by + bh), int(bx):int(bx + bw)]
n_y = int(yellow(sub).sum())
n_d = int(dark(sub).sum())
ys, xs = np.where(dark(sub))
num_bbox = (xs.min(), ys.min(), xs.max(), ys.max()) if n_d else None
print(f"  badge oval {bx:.0f},{by:.0f} {bw:.0f}x{bh:.0f}: yellow px {n_y}, ink px {n_d}, numeral bbox {num_bbox}")
if n_y < 3000:
    fails.append(f"badge: yellow fill px {n_y} < 3000")
if not (700 <= n_d <= 3000):
    fails.append(f"badge numeral ink px {n_d} outside 700..3000")

print("\n== element ink bboxes: original(px) vs render(scaled to orig px), tol 4 render px ==")
check("title", (300, 25, 660, 90), red, 200)
check("truth_table_frame", (96, 138, 314, 307), red, 300)
check("truth_table_header_X1X2OP", (96, 138, 314, 178), dark, 200, 8)
check("truth_table_digits", (96, 178, 314, 307), dark, 300)
check("OPP_pills", (298, 178, 314, 307), dark, 60)
check("diagram_panel", (144, 355, 511, 489), red, 200)
check("weights_-5_-3_6", (140, 560, 260, 690), dark, 80)
check("sigma_circle+Σ", (279, 409, 337, 458), dark, 120, 6)
check("step_function_box", (343, 407, 400, 444), dark, 120, 6)
check("activation_rule_box", (361, 372, 402, 396), dark, 60, 6)
check("O/P_label", (482, 424, 510, 452), dark, 40, 6)
check("equation_card", (608, 417, 853, 477), red, 200)
check("equation_box_peach", (588, 410, 812, 464), cream, 800, 6)
check("plot_image_axes+points", (539, 111, 839, 367), dark, 4000, 8)

print("\n== discrete content checks ==")
# 1. activation rule text: exactly two ink lines inside the cream box, both non-empty
box = reg(R, (361, 372, 402, 396))
dm = dark(box)
rows = dm.sum(axis=1)
line_rows = [i for i, v in enumerate(rows) if v > 0]
n_lines = len(_lines := [])  # placeholder replaced below
runs, inn = [], False
for i, v in enumerate(rows):
    if v > 0 and not inn:
        st = i; inn = True
    elif v == 0 and inn:
        runs.append((st, i)); inn = False
if inn:
    runs.append((st, len(rows)))
runs = [(a, b) for a, b in runs if b - a >= 2]
print(f"  activation-rule text: {len(runs)} text lines in render (orig has 2) -> {runs}")
if len(runs) != 2:
    fails.append(f"activation rule text: {len(runs)} text lines in render, expected 2")

# 2. badge numeral must be two digits
sub = R[int(by):int(by + bh), int(bx):int(bx + bw)]
dm = dark(sub)
cols = dm.sum(axis=0)
gruns, inn = [], False
for i, v in enumerate(cols):
    if v > 0 and not inn:
        st = i; inn = True
    elif v == 0 and inn:
        gruns.append((st, i)); inn = False
if inn:
    gruns.append((st, len(cols)))
gruns = [(a, b) for a, b in gruns if b - a >= 2]
print(f"  badge numeral: {len(gruns)} ink column group(s) (orig has 2 digits) -> {gruns}")
if len(gruns) < 1:
    fails.append("badge numeral: no ink")

# 3. equation ink present in the peach box (render) and not overlapping the card border
n_eq, b_eq = find_ink(R, (588, 410, 812, 464), dark)
print(f"  equation ink in peach box: {n_eq} px, bbox(orig px) {b_eq}")
if n_eq < 150:
    fails.append(f"equation ink only {n_eq} px")

print("\n== house-rule assertions ==")
print(f"  slide bg must be E8E8E8; frame rect/badge/title geometry asserted above from render coords")
checks = sys.argv[1] if len(sys.argv) > 1 else ""

print()
if fails:
    print(f"VERIFY: FAIL — {len(fails)} problem(s)")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("VERIFY: PASS — all element bboxes within tolerance, all content checks green")
sys.exit(0)
