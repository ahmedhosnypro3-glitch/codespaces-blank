"""selfcheck_attempt_5 — closed-loop numbers for slide 004 attempt 5.

Run from the deck namespace. 1 frame px == 1 pt == 1/200 in at 150 dpi.
Checks (all must pass before a judge dispatch): body text present, equations
have ink (none empty), no ink crosses the 8 inner boxes, no collision between the
matrices and their label captions, house chrome (separate checker), verbatim
pdftotext tokens.
"""
import os
import subprocess
from PIL import Image
import numpy as np

DECK = os.getcwd()
QA = DECK + "/recreated_pptx/qa/slide004/"
REND = QA + "render_6.png"
PDF = QA + "/slide_004_recreated.pdf"
SX = 2001 / 960.0
SY = 1125 / 540.0

r = Image.open(REND).convert("RGB")
ra = np.asarray(r).astype(int)
ink = (ra[..., 0] < 170) | (ra[..., 1] < 170) | (ra[..., 2] < 170)


def X(v): return int(round(v * SX))
def Y(v): return int(round(v * SY))


ALG = np.asarray(Image.open(DECK + "/unique_slides/slide_004.jpg").convert("RGB")).astype(int)
OAL = (ALG[..., 0] < 170) | (ALG[..., 1] < 170) | (ALG[..., 2] < 170)


def BB(x0, x1, y0, y1, M=None):
    M = ink if M is None else M
    ys, xs = np.nonzero(M[Y(y0):Y(y1), X(x0):X(x1)])
    if not len(ys):
        return None
    return ((xs.min() + X(x0)) / SX, (xs.max() + X(x0)) / SX,
            (ys.min() + Y(y0)) / SY, (ys.max() + Y(y0)) / SY)


def col(x0, x1, y0, y1, M=None):
    M = ink if M is None else M
    return int(M[Y(y0):Y(y1), X(x0):X(x1)].sum())


fails = []
log = []


def ck(name, ok, detail):
    log.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        fails.append(name)


# 1. body text present (every text box yields ink)
boxes = {
    "title": (240, 680, 66, 96),
    "letY_equation": (86, 224, 131, 182),
    "label_original": (245, 355, 136, 151),
    "from_training": (214, 343, 158, 178),
    "letYh_equation": (432, 560, 130, 192),
    "label_predicted": (587, 706, 137, 149),
    "from_model": (565, 670, 162, 175),
    "remember": (787, 872, 102, 146),
    "objective": (84, 250, 260, 280),
    "error": (84, 440, 310, 360),
    "where_first": (500, 625, 246, 262),
    "where_l2": (500, 800, 314, 330),
    "where_l3": (500, 800, 344, 360),
    "define": (82, 640, 390, 445),
    "formula": (171, 500, 482, 500),
}
for n, (x0, x1, y0, y1) in boxes.items():
    c = col(x0, x1, y0, y1)
    ck(f"ink:{n}", c > 200, f"{c} ink px in x{x0}..{x1} y{y0}..{y1}")

# 2. equations have ink and are 2D stacked (multi-row structure)
e1 = BB(86, 224, 131, 182)
e2 = BB(432, 560, 130, 192)
ck("eq:Yvec_ink", e1 is not None and (e1[3] - e1[2]) > 30,
   f"ink x{e1[0]:.1f}..{e1[1]:.1f} y{e1[2]:.1f}..{e1[3]:.1f} (height {e1[3]-e1[2]:.1f}px, stacked)")
ck("eq:Yhatvec_ink", e2 is not None and (e2[3] - e2[2]) > 30,
   f"ink x{e2[0]:.1f}..{e2[1]:.1f} y{e2[2]:.1f}..{e2[3]:.1f} (height {e2[3]-e2[2]:.1f}px, stacked)")

# 3. containment — no ink in the true gutters between neighbouring elements.
#    Gutter bands are chosen to sit strictly BETWEEN the measured border strokes
#    so they cannot catch a neighbour's correctly-placed border or the title's
#    descender (both verified on the fresh render):
#      title ink ends y96.5 ; LEFT/RIGHT box top border starts y98.4
#      OBJ bottom border 300.5..301.0 ; ERR top border 305.3..305.8
#      ERR bottom border 364.3..364.8 ; WHERE top border 231.4 (different x)
bxs = {
    "LEFT": (80, 395, 99, 222), "RIGHT": (427, 745, 99, 222),
    "REMEMBER": (784, 881, 100, 153), "OBJ": (78, 302, 242, 301),
    "ERR": (78, 486, 306, 365), "WHERE": (494, 884, 232, 371),
    "DEFINE": (75, 660, 387, 448), "FORMULA": (78, 486, 464, 522),
}
# per-box explicit gutter bands (x0,x1,y0,y1) that must hold zero ink
gutters = {
    "LEFT":   [(82, 393, 97, 98), (82, 393, 223, 225), (398, 401, 101, 220), (76, 78, 101, 220)],
    "RIGHT":  [(429, 743, 97, 98), (429, 743, 223, 225), (748, 751, 101, 220), (423, 425, 101, 220)],
    "REMEMBER": [(786, 879, 96, 98), (786, 879, 154, 156), (884, 887, 102, 151), (781, 783, 102, 151)],
    "OBJ":    [(80, 300, 302, 304), (80, 300, 237, 239), (305, 307, 244, 299), (74, 77, 244, 299)],
    "ERR":    [(80, 484, 302, 304), (80, 484, 367, 369), (489, 492, 308, 363), (74, 77, 308, 363)],
    "WHERE":  [(496, 882, 229, 231), (496, 882, 372, 374), (887, 890, 234, 369), (490, 493, 234, 369)],
    "DEFINE": [(77, 658, 384, 385), (77, 658, 450, 452), (663, 666, 389, 447), (71, 74, 389, 447)],
    "FORMULA": [(80, 484, 461, 463), (80, 484, 523, 525), (489, 492, 466, 521), (74, 77, 466, 521)],
}
for n, bands in gutters.items():
    n_out = sum(col(x0, x1, y0, y1) for (x0, x1, y0, y1) in bands)
    ck(f"containment:{n}", n_out == 0,
       f"{n_out} ink px in the {len(bands)} gutter bands around x{bxs[n][0]}..{bxs[n][1]} y{bxs[n][2]}..{bxs[n][3]}")

# 4. matrix <-> caption geometry vs the ORIGINAL (the fixed MAJOR).
#    The ORIGINAL's own measured relationship is the reference, not a fixed
#    tolerance: caption-centre sits 12..18 px above the matrix centre in the
#    original too (hand-drawn matrices are taller than the typed equations).
GEO = {
    "LEFT":  dict(m=(86, 224, 131, 182), c=(245, 353, 136, 151),
                  om=(165, 209, 115, 203), oc=(246, 371, 136, 153)),
    "RIGHT": dict(m=(432, 560, 130, 192), c=(587, 706, 137, 149),
                  om=(511, 547, 114, 208), oc=(587, 722, 137, 150)),
}
for nm, g in GEO.items():
    m, c = BB(*g["m"]), BB(*g["c"])
    omcy = (g["om"][2] + g["om"][3]) / 2
    occy = (g["oc"][2] + g["oc"][3]) / 2
    ogap = g["oc"][0] - g["om"][1]
    gap = c[0] - m[1]
    d_off = (c[2] + c[3]) / 2 - (m[2] + m[3]) / 2
    o_off = occy - omcy
    ok = (c[0] > m[1] and abs(gap - ogap) <= 25 and abs(d_off - o_off) <= 6)
    ck(f"alignment:{nm}", ok,
       f"caption ink starts x{c[0]:.1f} RIGHT of matrix ink end x{m[1]:.1f} "
       f"(gap {gap:.1f}px vs original {ogap:.1f}px); caption-cy offset "
       f"{d_off:+.1f}px vs original {o_off:+.1f}px -> "
       f"{'MATCHES ORIGINAL' if ok else 'DEVIATES'}")

# 5. 'from' line sits UNDER its caption
fL, cL = BB(214, 343, 158, 178), BB(245, 353, 136, 151)
fR, cR = BB(565, 670, 162, 175), BB(587, 706, 137, 149)
ck("from_under:LEFT", fL[2] > cL[3] - 2, f"from top y{fL[2]:.1f} vs caption bottom y{cL[3]:.1f}")
ck("from_under:RIGHT", fR[2] > cR[3] - 2, f"from top y{fR[2]:.1f} vs caption bottom y{cR[3]:.1f}")

# 6. emphasis underlines present where the original has them
for nm, (x0, x1, y0, y1, gx0, gx1, gy0, gy1) in {
    "W in from_model": (655, 672, 173, 177, 650, 670, 171, 173),
    "Yh in where L1": (497, 512, 260, 265, 501, 511, 246, 260),
    "W in where L1": (537, 556, 260, 265, 540, 554, 246, 260),
}.items():
    ck(f"underline:{nm}", col(x0, x1, y0, y1) >= 15,
       f"bar ink {col(x0, x1, y0, y1)} px at x{x0}..{x1} y{y0}..{y1}")

# 7. the refuted Objective-box underline is gone
ck("no:objective_blank_underline", col(250, 275, 281, 288) == 0,
   f"{col(250, 275, 281, 288)} px in the old underline band x250..275 y281..288")

# 8. verbatim tokens (text layer; the bottom Loss equation is a PNG image, so it
#    is asserted by ink instead — see 'ink:formula' above)
txt = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True,
                     text=True, env=dict(os.environ, TMPDIR=DECK + "/scratch/tmp")).stdout
tokens = ["Concept of", "LOSS", "Function", "Original Labels", "from Training Samples",
          "Predicted Labels", "from Model", "Remember", "Objective is", "If",
          "There is an", "Error (Loss)", "Predicted", "Where:", "is a matrix", "Given",
          "labels vector", "Model Parameter", "Required", "Define", "Loss", "function as",
          "squared distance", "between", "and"]
missing = [t for t in tokens if t not in txt]
ck("verbatim_tokens", not missing, f"missing={missing if missing else 'none'}")

print("selfcheck_attempt_5 — slide 004 / attempt 5 / render_6.png")
print("=" * 72)
for l in log:
    print(l)
print("=" * 72)
print(f"RESULT: {'ALL PASS' if not fails else 'FAILED: ' + ', '.join(fails)}")
print()
print("pdftotext layout dump:")
print(txt)
