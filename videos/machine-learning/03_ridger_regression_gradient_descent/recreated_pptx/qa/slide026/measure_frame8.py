#!/usr/bin/env python3
"""Pass-8 (resume worker w4-s026): CORRECTED word x-positions (pen in 1x units).
Match predicted word ink extents against measured runs for rows A-D and notes N1-N4
at 18pt Arial; also predict the GD/Notes header (red) positions and the underline
bar spans for rowB/rowD/N3."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
S = 4
AR = "/usr/share/fonts/TTF/Arial.TTF"
ARB = "/usr/share/fonts/TTF/Arialbd.TTF"

_cache = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(ARB if bold else AR, int(round(size * S)))
    return _cache[key]

def word_boxes(text, x0, size):
    f = font(size)
    out, pen = [], 0.0
    for i, w in enumerate(text.split(" ")):
        if i:
            pen += f.getlength(" ") / S
        img = Image.new("L", (int(size * S * len(w) * 2) + 200, size * S * 3), 0)
        d = ImageDraw.Draw(img)
        d.text((100, 100), w, font=f, fill=255)
        a = np.asarray(img)
        ys, xs = np.where(a > 40)
        li = (xs.min() - 100) / S if len(xs) else 0.0
        ri = (xs.max() - 100) / S if len(xs) else 0.0
        out.append((w, x0 + pen + li, x0 + pen + ri))
        pen += f.getlength(w) / S
    return out

def show(name, txt, x0, meas_runs, size=18):
    pred = word_boxes(txt, x0, size)
    print(f" -- {name} @18pt, start x={x0}")
    for w, a, b in pred:
        # find best-matching measured run
        best = min(meas_runs, key=lambda r: abs((r[0] + r[1]) / 2 - (a + b) / 2)) if meas_runs else None
        tag = ""
        if best:
            ov = min(b, best[1]) - max(a, best[0])
            tag = f"  ~ run[{best[0]}..{best[1]}] ov={ov:.0f}" if ov > 2 else "  (no run overlap)"
        print(f"     {w:16s} x {a:6.1f} .. {b:6.1f}{tag}")
    if pred:
        print(f"     TOTAL ink x {pred[0][1]:.1f} .. {pred[-1][2]:.1f}  (w={pred[-1][2]-pred[0][1]:.1f})")

print("== ROWS A-D @18pt (start x=146) ==")
A_RUNS = [(146, 166), (173, 208), (213, 247), (253, 296), (302, 434), (439, 469)]
B_RUNS = [(146, 166), (173, 227), (233, 255), (261, 320), (325, 344), (349, 716), (721, 737), (742, 777), (783, 846)]
C_RUNS = [(146, 188), (200, 224), (230, 296), (302, 334), (339, 352), (357, 366), (372, 419), (424, 512), (518, 559), (564, 640), (645, 689)]
D_RUNS = [(146, 166), (173, 207), (212, 253), (259, 281), (287, 473), (483, 516), (522, 533), (539, 552), (558, 580), (586, 660), (666, 706), (712, 728), (733, 755), (762, 830)]
show("rowA", "[1] Start with initial Random Weights (W)", 146, A_RUNS)
show("rowB", "[2] Update the weights by moving along the direction of negative gradient of Loss function", 146, B_RUNS)
show("rowC", "(w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)", 146, C_RUNS)
show("rowD", "[3] Stop when the gradient is almost zero (this is at the minimum value of the function)", 146, D_RUNS)

print("\n== HEADERS @18pt red bold? (GD hdr x109..392, Notes hdr x109..159) ==")
show("gd_hdr_reg", "Gradient Descent (GD) Algorithm:", 109, [], size=18)
show("gd_hdr_bold", "Gradient Descent (GD) Algorithm:", 109, [], size=18)

print("\n== NOTES @18pt (start x=109) ==")
N1_RUNS = [(109, 154), (159, 224), (229, 279), (284, 362), (373, 442), (448, 511), (522, 534), (539, 548), (554, 610), (615, 682), (688, 730), (736, 769)]
N2_RUNS = [(109, 202), (208, 241), (247, 295), (301, 311), (316, 341), (347, 385), (391, 466), (473, 516), (522, 560), (566, 575)]
N3_RUNS = [(109, 136), (141, 170), (176, 278), (283, 313), (319, 345), (351, 425), (430, 471), (477, 501), (507, 520), (525, 533), (538, 728), (733, 812), (818, 836)]
show("N1", "Least Squares Linear regression objective function is a convex function (even with", 109, N1_RUNS)
show("N2", "regularizer). This means it has ONE Minimum (good news ).", 109, N2_RUNS)
show("N3", "GD will approximately find this minimum value but at a variable number of steps depending on", 109, N3_RUNS)
show("N4", "the used Learning Rate", 109, [(111, 294)])

print("\n== UNDERLINE BARS (measured) vs predicted word spans ==")
print("  rowB bar y192..194 x350..716")
print("  rowD bar y258..259 x288..472")
print("  N3 bar1 y458 x190..276 ; N3 bar2 y458 x540..727")
for lbl, txt, x0, bars in [
    ("rowB", "[2] Update the weights by moving along the direction of negative gradient of Loss function", 146, [(350, 716)]),
    ("rowD", "[3] Stop when the gradient is almost zero (this is at the minimum value of the function)", 146, [(288, 472)]),
    ("N3", "GD will approximately find this minimum value but at a variable number of steps depending on", 109, [(190, 276), (540, 727)]),
]:
    print(f" -- {lbl}")
    for w, a, b in word_boxes(txt, x0, 18):
        for bs, be in bars:
            if min(b, be) - max(a, bs) > 3:
                print(f"     bar x{bs}..{be} covers word '{w}' (x {a:.0f}..{b:.0f})")
