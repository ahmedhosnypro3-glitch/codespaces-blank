"""Closed-loop PIL verification of the attempt-5 fixes on render_5.png
vs unique_slides/slide_004.jpg (1 frame px == 1 pt == 1/200 in @150dpi).
"""
from PIL import Image
import numpy as np

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_004.jpg"
REND = DECK + "/recreated_pptx/qa/slide004/render_5.png"
SX = 2001 / 960.0
SY = 1125 / 540.0

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
oa = np.asarray(o).astype(int)
ra = np.asarray(r).astype(int)
oink = (oa[..., 0] < 170) | (oa[..., 1] < 170) | (oa[..., 2] < 170)
rink = (ra[..., 0] < 170) | (ra[..., 1] < 170) | (ra[..., 2] < 170)


def X(v): return int(round(v * SX))
def Y(v): return int(round(v * SY))


def runs(mask, x0, x1, y0, y1, axis, gap=3, minink=1):
    m = mask[y0:y1, x0:x1]
    cs = m.sum(axis=axis)
    idx = np.nonzero(cs >= minink)[0]
    out = []
    if not len(idx):
        return out
    cur = [idx[0], idx[0]]
    for v in idx[1:]:
        if v - cur[1] <= gap:
            cur[1] = v
        else:
            out.append(tuple(cur)); cur = [v, v]
    out.append(tuple(cur))
    return out


def frx(a, b): return (round(a / SX, 1), round(b / SX, 1))
def fry(a, b): return (round(a / SY, 1), round(b / SY, 1))


def show(tag, mask, x0, x1, y0, y1):
    print(f"{tag}: x{x0/SX:.0f}..{x1/SX:.0f} y{y0/SY:.0f}..{y1/SY:.0f}")
    for rb in runs(mask, x0, x1, y0, y1, axis=1):
        ya, yb = rb[0] + y0, rb[1] + y0
        cb = runs(mask, x0, x1, rb[0], rb[1] + 2, axis=0)
        print(f"   y{ya/SY:.1f}..{yb/SY:.1f} cols "
              f"{[(round(a/SX,1), round(b/SX,1)) for a, b in cb]}")


print("=" * 74)
print("1. TOP-BOX ARRANGEMENT — render_5 vs measured original")
print("=" * 74)
print("\n--- ORIGINAL left box (recorded from adjud5_defects.py) ---")
print("   'Let Y=' x87..148 y145..157 | matrix x165..209 y115..203")
print("   'Original Labels' x246..371 y136..153 | 'from Training Samples' x215..388 y159..177")
print("\n--- RENDER_5 left box ---")
show("LEFT", rink, X(84), X(392), Y(103), Y(219))
print("\n--- ORIGINAL right box ---")
print("   'Let Yh=' x432..494 y145..163 | matrix x511..547 y114..208")
print("   'Predicted Labels' x587..722 y137..150 | 'from Model Yh=XW' x565..735 y163..183")
print("\n--- RENDER_5 right box ---")
show("RIGHT", rink, X(431), X(742), Y(103), Y(219))

print()
print("=" * 74)
print("2. UNDERLINES — render_5")
print("=" * 74)
# 'from Model Yh=XW' line: expect a 1-2px bar under the W glyph ~x650..672, y~176
print("RIGHT-box 'from' line (expect underline under W near y176-178):")
for rb in runs(rink, X(560), X(740), Y(160), Y(185), axis=1):
    print(f"   y{fry(rb[0]+Y(160), rb[1]+Y(160))} cols "
          f"{[frx(a+X(560), b+X(560)) for a, b in runs(rink, X(560), X(740), rb[0]+Y(160), rb[1]+Y(160)+1, axis=0)]}")
print()
print("WHERE-box first line (expect underlines under Yh and W):")
for rb in runs(rink, X(498), X(880), Y(244), Y(274), axis=1):
    print(f"   y{fry(rb[0]+Y(244), rb[1]+Y(244))} cols "
          f"{[frx(a+X(498), b+X(498)) for a, b in runs(rink, X(498), X(880), rb[0]+Y(244), rb[1]+Y(244)+1, axis=0)]}")
print()
print("OBJECTIVE box (must now have NO underline bar):")
for rb in runs(rink, X(84), X(298), Y(244), Y(298), axis=1):
    print(f"   y{fry(rb[0]+Y(244), rb[1]+Y(244))} cols {[frx(a+X(84), b+X(84)) for a, b in runs(rink, X(84), X(298), rb[0]+Y(244), rb[1]+Y(244)+1, axis=0)]}")

print()
print("=" * 74)
print("3. VERBATIM TEXT (pdftotext) — content must be unchanged")
print("=" * 74)
import subprocess, os
env = dict(os.environ)
env["TMPDIR"] = DECK + "/scratch/tmp"
txt = subprocess.run(["pdftotext", "-layout", DECK + "/qa/slide004/slide_004_recreated.pdf", "-"],
                     capture_output=True, text=True, env=env).stdout
need = ["Concept of", "LOSS", "Function", "Original Labels", "from Training Samples",
        "Predicted Labels", "from Model", "Remember", "Objective is", "If", "There is an",
        "Error (Loss)", "Predicted", "Where:", "is a matrix", "Given", "labels vector",
        "Model Parameter", "Required", "Define", "Loss", "function as", "squared distance",
        "between", "and", "Loss ="]
missing = [n for n in need if n not in txt]
print("missing tokens:", missing if missing else "NONE — all verbatim tokens present")
print()
print(txt)
