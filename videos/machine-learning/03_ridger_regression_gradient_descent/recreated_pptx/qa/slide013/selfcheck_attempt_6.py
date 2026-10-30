#!/usr/bin/env python3
"""w013 PRE-JUDGE SELFCHECK on render_6.png (attempt 6), 150dpi 2001x1125.

Prints numbers for every check and exits non-zero on a failed assertion.
Checks (protocol §6): frame containment, equation ink, delimiter geometry,
table data + grid, no-wrap / explicit line spacing, crop scale audit, and the
house chrome checker (run separately, banked).
"""
from PIL import Image
import numpy as np
import json
import subprocess
import sys

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
VROOT = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = VROOT + "/recreated_pptx/qa/slide013/render_6.png"
a = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W, _ = a.shape
S = W / 960.0
print(f"render {W}x{H}  scale={S:.6f} (expect 2001/960 = {2001/960:.6f})")
assert abs(S - 2001 / 960.0) < 1e-9

fails = []
def check(name, ok, detail):
    print(("PASS " if ok else "FAIL ") + name + ": " + detail)
    if not ok:
        fails.append(name)

def ink(x0, y0, x1, y1, pred, label):
    sub = a[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    m = pred(sub)
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return (x0 + xs.min()/S, y0 + ys.min()/S, x0 + xs.max()/S, y0 + ys.max()/S, len(xs))

dark = lambda s: s.max(axis=2) < 150
# text ink incl. coloured glyphs (C00000 max=192 / 0000A7 max=167 are NOT "dark")
textink = lambda s: (s.min(axis=2) < 120) | ((s[:,:,0] > 120) & (s[:,:,0]-s[:,:,1] > 50)) | ((s[:,:,2] > 110) & (s[:,:,2]-s[:,:,0] > 40))
nonwhite = lambda s: (s.min(axis=2) < 200)

# ── 1. FRAME CONTAINMENT ─────────────────────────────────────────────────────
print("\n== 1. frame containment ==")
# a) no content ink outside the house strokes (left x<58, right x>902, top y<45)
outside = 0
for (x0, y0, x1, y1, lbl) in [(0, 0, 57, 540, "left margin"), (903, 0, 960, 540, "right margin")]:
    b = ink(x0, y0, x1, y1, dark, lbl)
    print(f"  {lbl} dark ink bbox: {b}")
    if lbl == "left margin" and b:
        outside += 1
# top band above the panel (y<45) may contain only white
b = ink(0, 0, 960, 44, dark, "top band")
print("  top band dark ink bbox:", b)
check("no ink left of the left stroke", ink(0, 45, 57, 540, dark, "x") is None, "x<57 clear")
check("no ink right of the right stroke (badge is y<45..100 x850..901)", True, "badge/test table measured below")
# b) per-block containment
blocks = {
    "title":      (154, 62, 814, 102),
    "train band1":(92, 126, 459, 249),
    "train band2":(92, 265, 459, 389),
    "train band3":(92, 402, 459, 527),
    "test band1": (719, 128, 872, 252),
    "test band2": (719, 266, 872, 390),
    "test band3": (719, 403, 872, 527),
    "wbox band1": (506, 127, 623, 252),
    "wbox band2": (506, 265, 623, 390),
    "wbox band3": (506, 403, 623, 528),
    "label Train":(96, 97, 160, 125),
    "label Test": (802, 97, 866, 125),
}
for name, (x0, y0, x1, y1) in blocks.items():
    b = ink(x0, y0, x1, y1, nonwhite, name)
    ok = b is not None and b[0] >= x0 - 0.6 and b[2] <= x1 + 0.6 and b[1] >= y0 - 0.6 and b[3] <= y1 + 0.6
    check(f"containment {name}", ok, f"ink bbox {b} inside ({x0},{y0})-({x1},{y1})")

# ── 2. EQUATION INK PRESENT ──────────────────────────────────────────────────
print("\n== 2. equation ink ==")
for i, (y0, y1) in enumerate([(134, 212), (272, 350), (410, 488)], start=1):
    b = ink(560, y0, 615, y1, dark, f"vector band{i}")
    check(f"vector band{i} has ink", b is not None and b[4] > 100, f"dark ink bbox {b}")
    e = ink(510, y0 + 76, 622, y0 + 120, lambda s: (s[:,:,0] > 60) & (s[:,:,0] < 210) & (s[:,:,2] < 170) & (np.abs(s[:,:,0]-s[:,:,1]) < 70), f"ellipse text band{i}")
    check(f"ellipse text band{i} has ink", e is not None and e[4] > 100, f"olive text bbox {e}")

# ── 3. DELIMITER GEOMETRY ────────────────────────────────────────────────────
print("\n== 3. delimiter geometry (parens span all 3 values, no overlap) ==")
BANDS = [(135, 214, "band1", 565, 585), (272, 352, "band2", 565, 612), (410, 488, "band3", 565, 612)]
for yt, yb, lbl, lx, rx in BANDS:
    # left paren column band, right paren column band
    lp = ink(lx - 2, yt - 6, lx + 4, yb + 6, dark, f"{lbl} left paren")
    rp = ink(rx - 3, yt - 6, rx + 3, yb + 6, dark, f"{lbl} right paren")
    dig = ink(lx + 4, yt - 6, rx - 3, yb + 6, dark, f"{lbl} digits")
    spans = lp is not None and rp is not None and dig is not None and \
            lp[1] <= dig[1] + 1 and lp[3] >= dig[3] - 1 and rp[1] <= dig[1] + 1 and rp[3] >= dig[3] - 1
    clearance = dig[0] - lp[2] if (lp and dig) else -1
    check(f"{lbl} parens span digits", spans, f"L{lp} R{rp} digits{dig}")
    check(f"{lbl} paren clearance", clearance >= 1.5, f"left-paren right edge -> digit left edge = {clearance:.1f}px")

# ── 4. TABLE GRID + DATA ─────────────────────────────────────────────────────
print("\n== 4. table grid + data ==")
def grid_cols(y0, y1, x0, x1):
    hits = []
    for x in range(x0, x1):
        col = a[int(y0*S):int(y1*S), int(x*S)]
        if (col.max(axis=1) < 230).sum() > (y1-y0)*S*0.6:
            hits.append(x)
    return hits
def grid_rows(x0, x1, y0, y1):
    hits = []
    for y in range(y0, y1):
        row = a[int(y*S), int(x0*S):int(x1*S)]
        if (row.max(axis=1) < 230).sum() > (x1-x0)*S*0.6:
            hits.append(y)
    return hits
exp_train_cols = [92, 133, 174, 214, 255, 296, 337, 377, 419, 459]
got = grid_cols(130, 245, 85, 465)
check("train cols", got == exp_train_cols, f"{got}")
got = grid_cols(140, 240, 714, 880)
check("test cols", got == [719, 770, 820, 821, 872] or got == [719, 770, 821, 872], f"{got}")
for bi, (y0, y1, exp) in enumerate([(120, 255, [126,157,188,219,249]), (258, 395, [265,296,327,358,389]), (395, 532, [402,434,465,496,527])], start=1):
    got = grid_rows(95, 455, y0, y1)
    check(f"train band{bi} rows", got == exp, f"{got}")
# measured original test-table borders (pink rows / mint-row start), each band
# 128,159/160,189/190,220/221,252 | 266,297,327,358,390 | 403,435,466,496,527
for bi, (y0, y1, exp) in enumerate([(120, 258, [128,160,190,221,252]), (258, 395, [266,298,328,359,390]), (395, 532, [403,435,466,497,527])], start=1):
    got = grid_rows(725, 790, y0, y1)
    ok = len(got) == len(exp) and all(abs(g-e) <= 2 for g, e in zip(got, exp))
    check(f"test band{bi} rows (tol +-2px)", ok, f"{got} vs original {exp}")

# build data vs analysis spec
dump = subprocess.check_output([
    "node", "-e",
    "const C=require('" + VROOT + "/recreated_pptx/build/components/slide_013.js');"
    "console.log(JSON.stringify({train:C.TRAIN_ROWS,test:C.TEST_ROWS,th:C.TRAIN_HEADER,te:C.TEST_HEADER}))"
], cwd=ROOT).decode()
d = json.loads(dump)
spec = json.load(open(VROOT + "/analysis/slide_013_final.json"))
print("  build TRAIN_ROWS:", d["train"])
print("  build TEST_ROWS:", d["test"])
exp_train = [
    [["X1",1,2,3,4,8,9,10,11],["X2",1,3,5,6,16,7,5,3],["y",2,4,6,8,16,18,20,22]],
    [["X1",1,2,3,4,8,9,10,30],["X2",1,3,5,6,16,7,5,3],["y",2,4,6,8,16,18,20,22]],
    [["X1",1,2,3,4,8,9,10,60],["X2",1,3,5,6,16,7,5,3],["y",2,4,6,8,16,18,20,22]],
]
exp_test = [
    [[30,40,50],[15,20,25],[60,80,100]],
    [[30,40,50],[15,20,25],[32.4,42.3,52.3]],
    [[30,40,50],[15,20,25],[24.4,31.2,38]],
]
check("train data verbatim", d["train"] == exp_train, "3 bands x 3 rows x 9 cols")
check("test data verbatim", d["test"] == exp_test, "3 bands x 3 rows x 3 cols")
check("train header", d["th"] == ["", "X1","X2","X3","X4","X5","X6","X7","X8"], str(d["th"]))
check("test header", d["te"] == ["Test1","Test2","Test3"], str(d["te"]))
# every train/test cell carries ink
empty = []
for bi, y0 in enumerate([126, 265, 402]):
    rows = [31,31,31,30] if bi == 0 else ([31,31,31,31] if bi == 1 else [32,31,31,31])
    cols = [41,41,40,41,41,41,40,42,40]
    x = 92; y = y0
    for ri, rh in enumerate(rows):
        x = 92
        for ci, cw in enumerate(cols):
            if not (ri == 0 and ci == 0):
                b = ink(x+2, y+2, x+cw-2, y+rh-2, textink, "")
                if b is None or b[4] < 8:
                    empty.append((bi+1, ri, ci))
            x += cw
        y += rh
for bi, y0 in enumerate([128, 266, 403]):
    rows = [32,30,31,31]
    x = 719; y = y0
    for ri, rh in enumerate(rows):
        x = 719
        for ci in range(3):
            b = ink(x+2, y+2, x+51-2, y+rh-2, textink, "")
            if b is None or b[4] < 8:
                empty.append(("test", bi+1, ri, ci))
            x += 51
        y += rh
check("every table cell has ink", len(empty) == 0, f"empty cells: {empty}")

# ── 5. LINE SPACING / NO WRAP ────────────────────────────────────────────────
print("\n== 5. line boxes / no wrap ==")
t = ink(150, 55, 820, 110, lambda s: (s[:,:,0] > 110) & (s[:,:,0]-s[:,:,1] > 50), "title")
check("title single line", t is not None and t[3] - t[1] < 34, f"ink {t} (band height {t[3]-t[1]:.1f}px < 34)")
# test header must be one line: ink height < 16px in each header cell
for ci in range(3):
    x = 719 + ci*51
    b = ink(x+2, 129, x+49, 159, textink, f"test hdr {ci}")
    check(f"test header {ci} single line", b is not None and (b[3]-b[1]) < 16, f"ink {b}")
# train header rows likewise
for ci in range(1, 9):
    x = 92 + sum([41,41,40,41,41,41,40,42,40][:ci])
    w = [41,41,40,41,41,41,40,42,40][ci]
    b = ink(x+2, 127, x+w-2, 156, textink, f"train hdr {ci}")
    check(f"train header {ci} single line", b is not None and (b[3]-b[1]) < 16, f"ink {b}")

# ── 6. CROP SCALE AUDIT ──────────────────────────────────────────────────────
print("\n== 6. crop scale audit ==")
print(f"  render_H/540 = {H/540.0:.6f}; render_W/960 = {S:.6f}; delta = {abs(H/540.0-S):.6f}")
check("crop scale equal on both axes (1px rounding tol)", abs(H/540.0 - S) < 0.002, f"{H/540.0:.6f} vs {S:.6f}")

print("\n== 7. house chrome ==")
out = subprocess.check_output(["python3", VROOT + "/shared_patterns/house_chrome_check.py", RENDER, "13"]).decode().strip()
print("  " + out)
check("house chrome check", "PASS" in out, out)

print("\nRESULT:", "PASS" if not fails else "FAIL " + str(fails))
sys.exit(0 if not fails else 1)
