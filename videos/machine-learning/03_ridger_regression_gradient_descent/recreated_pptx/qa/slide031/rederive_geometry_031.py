# Fresh-lane re-derivation of all known prior geometry baselines against BOTH
# images: original lecture frame (960x540, 1px=1pt) and the CURRENT render
# (render_cur.png, md5 9d42391f0a5c948d355232f9cb130e62, currency-proven vs
# recreated_pptx/slide_031_recreated.pptx by independent re-render).
# Every mask is derived from its OWN image's pixel statistics.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
SX, SY = 2001 / 960.0, 1125 / 540.0
print("scale render->frame: %.6f px/frame-px per axis" % SX)

OV, RV = O.max(axis=2), R.max(axis=2)
# Original: white canvas=255, gray panel=233, plot bg ~240. Text/lines darker than 205.
O_ink = OV < 205
# Render: anti-aliased edges, so glyph cores < 210 on a 255 canvas
R_ink = RV < 210


def run(tag, o_band, r_band, note):
    print("\n=== %s ===" % tag)
    if note:
        print("   %s" % note)
    f0, f1 = o_band
    r0, r1 = int(f0 * SX), int(f1 * SX)
    # original
    cnt_o = O_ink[f0:f1, o_band[0]:0] if False else None
    return f0, f1, r0, r1


def band_rows(img, msk, y0, y1, x0, x1, scale, minpx=1):
    ys = range(y0, y1)
    out = []
    for y in ys:
        c = int(msk[y, x0:x1].sum())
        if c >= minpx:
            out.append((y / scale, c))
    return out


def summarize(tag, rows):
    if not rows:
        print("  %s: NO INK" % tag)
        return None
    ys = [r[0] for r in rows]
    print("  %s: ink rows frame %.1f..%.1f, total %d px" % (tag, min(ys), max(ys), sum(r[1] for r in rows)))
    return min(ys), max(ys), sum(r[1] for r in rows)


print("\n########## 1. TITLE  (frame y 55..95) ##########")
o = summarize("ORIG", band_rows(O, O_ink, 55, 96, 60, 620, 1.0))
r = summarize("REND", band_rows(R, R_ink, int(55 * SX), int(96 * SX), int(60 * SX), int(620 * SX), SX))
if o and r:
    print("  delta top %+d  delta bottom %+d  (prior baseline: render y64..84 vs frame 66..88)"
          % (r[0] - o[0], r[1] - o[1]))

print("\n########## 2. ANNOTATION text line 1 'X is in between 4.8 and 5.1' ##########")
o = summarize("ORIG", band_rows(O, O_ink, 244, 290, 250, 570, 1.0))
r = summarize("REND", band_rows(R, R_ink, int(244 * SX), int(290 * SX), int(250 * SX), int(570 * SX), SX))
if o and r:
    print("  delta top %+d  delta bottom %+d  (prior baseline: render y251..259 vs frame 247..261)"
          % (r[0] - o[0], r[1] - o[1]))

print("\n########## 3. ANNOTATION line 2 'f(x) is in between 1.04 and 1.01' ##########")
o = summarize("ORIG", band_rows(O, O_ink, 244, 292, 250, 810, 1.0))
r = summarize("REND", band_rows(R, R_ink, int(244 * SX), int(292 * SX), int(250 * SX), int(810 * SX), SX))
if o and r:
    print("  delta top %+d  delta bottom %+d  (prior baseline: render y267..277 vs frame 265..287)"
          % (r[0] - o[0], r[1] - o[1]))

print("\n########## 4. X-AXIS TICK LABELS (frame y 265..295, inside plot x574..808) ##########")
o = summarize("ORIG", band_rows(O, O_ink, 265, 296, 574, 809, 1.0))
r = summarize("REND", band_rows(R, R_ink, int(265 * SX), int(296 * SX), int(574 * SX), int(809 * SX), SX))
if o and r:
    print("  delta top %+d  delta bottom %+d  (prior baseline: render y272..277 vs frame 270..275)"
          % (r[0] - o[0], r[1] - o[1]))

print("\n########## 5. '(5,1)' LABEL green glyphs ##########")
# green mask per image
Og, Rg = O[:, :, 1], R[:, :, 1]
Om = (O[:, :, 1] > O[:, :, 0] + 15) & (O[:, :, 1] > O[:, :, 2] + 15)
Rm = (R[:, :, 1] > R[:, :, 0] + 15) & (R[:, :, 1] > R[:, :, 2] + 15)
for lab, a, sc, msk, x0, x1, y0, y1 in [("ORIG", O, 1.0, Om, 490, 545, 244, 265),
                                        ("REND", R, SX, Rm, int(490 * SX), int(545 * SX), int(244 * SX), int(265 * SX))]:
    sub = np.zeros_like(msk)
    sub[y0:y1, x0:x1] = msk[y0:y1, x0:x1]
    yy, xx = np.nonzero(sub)
    if len(yy):
        print("  %s green px=%d  frame bbox x%.1f..%.1f y%.1f..%.1f"
              % (lab, len(yy), xx.min() / sc, xx.max() / sc, yy.min() / sc, yy.max() / sc))
    else:
        print("  %s: NO GREEN" % lab)

print("\n########## 6. PARAM TABLE 6 CELL modal fills ##########")
def modal(img, x0, x1, y0, y1, q=0.25):
    reg = img[y0:y1, x0:x1].reshape(-1, 3)
    keep = reg[(reg.min(axis=1) >= 0)]
    return collections.Counter(map(tuple, keep // 8 * 8)).most_common(3)
import collections
# frame param table: build says x80..160 label / x160..240 value, y 175..214 in frame px
for i, ry in enumerate([175, 188, 201]):
    for lab, x0, x1 in [("label", 82, 158), ("value", 162, 238)]:
        y0, y1 = ry + 2, ry + 11
        mo = modal(O, x0, x1, y0, y1)
        mr = modal(R, int(x0 * SX), int(x1 * SX), int(y0 * SX), int(y1 * SX))
        print("  cell%d %-5s frame-modal %s | render-modal %s" % (i, lab, mo[0][0], mr[0][0]))
