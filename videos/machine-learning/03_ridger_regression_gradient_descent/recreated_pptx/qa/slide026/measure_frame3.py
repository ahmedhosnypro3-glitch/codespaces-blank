#!/usr/bin/env python3
"""Pass-3: systematic Arial-metric fit of slide_026 rows + clean title measure
+ sensitive underline scan + per-word cumulative position verification.
"""
import numpy as np
from PIL import Image, ImageFont

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
AR = "/usr/share/fonts/TTF/Arial.TTF"
AB = "/usr/share/fonts/TTF/Arialbd.TTF"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red_ink = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
blue_ink = (b > 90) & ((b - r) > 40) & ((b - g) > 40)
dist_white = 255 - im.min(axis=2)
ink_white = dist_white > 28

def adv(t, s, bold=False):
    return ImageFont.truetype(AB if bold else AR, s).getlength(t)

# ---------- 1. clean TITLE measure (red only, exclude badge x>=850) ----------
print("== TITLE clean (red mask, y45..105, x70..849) ==")
tw = red_ink[45:105, 70:850]
ys, xs = np.where(tw)
y0, y1, x0, x1 = ys.min()+45, ys.max()+45, xs.min()+70, xs.max()+70
print(f"  red bbox y {y0}-{y1} (h={y1-y0+1}) x {x0}-{x1} (w={x1-x0+1}) center=({(x0+x1)/2:.1f},{(y0+y1)/2:.1f})")
# word runs of title
prof = tw.any(axis=0)
idx = np.where(prof)[0]
runs = []
if len(idx):
    s0 = p0 = idx[0]
    for i in idx[1:]:
        if i > p0 + 3:
            runs.append((s0+70, p0+70)); s0 = i
        p0 = i
    runs.append((s0+70, p0+70))
print("  title word runs:", [(a, c, c-a+1) for a, c in runs])
# title underline? scan rows 83..100 for red bars
print("  red-bar scan rows 83..100:")
for yy in range(83, 101):
    row = red_ink[yy, 200:840]
    if row.sum() > 50:
        print(f"    y{yy}: {row.sum()} red px")
# title size fit (bold): band h -> size; advance -> size
TITLE = "Gradient Descent Solution"
for s in range(18, 32):
    w_pred = adv(TITLE, s, True)
    print(f"  size {s}: bold adv={w_pred:.0f}px  band_pred={s*1.117:.1f}px")

# ---------- 2. underline sensitive scan ----------------------------------------
print("\n== sensitive underline scans (fill>=0.35, run>=12) ==")
def scan_bars(label, m, y0, y1, x0, x1, fill_min=0.35, wmin=12):
    hits = []
    for yy in range(y0, y1):
        row = m[yy, x0:x1]
        idx = np.where(row)[0]
        if not len(idx):
            continue
        s0 = p0 = idx[0]
        for i in idx[1:]:
            if i > p0:
                s0 = i
            else:
                p0 = i
        # simple contiguous runs
        rr = []
        idx = np.where(row)[0]
        s0 = p0 = idx[0]
        for i in idx[1:]:
            if i > p0 + 1:
                rr.append((s0, p0)); s0 = i
            p0 = i
        rr.append((s0, p0))
        for (a, c) in rr:
            w_ = c - a + 1
            fl = row[a:c+1].mean()
            if w_ >= wmin and fl >= fill_min:
                hits.append((yy, a+x0, c+x0, w_, fl))
    if hits:
        print(f"  {label}:")
        for h in hits:
            print(f"    y{h[0]} x {h[1]}-{h[2]} (w={h[3]}, fill={h[4]:.2f})")
    else:
        print(f"  {label}: none")

scan_bars("row B under-zone (blue)", blue_ink, 190, 202, 340, 520)
scan_bars("row B under-zone FULL (blue)", blue_ink, 186, 202, 140, 860)
scan_bars("row C under-zone (blue+red)", blue_ink | red_ink, 224, 238, 140, 700)
scan_bars("row D under-zone (blue)", blue_ink, 256, 270, 140, 860)
scan_bars("notes N1/N2 under-zone (dark)", im.sum(axis=2) < 400, 356, 372, 100, 780)
scan_bars("notes N3 under-zone (dark)", im.sum(axis=2) < 400, 455, 470, 100, 840)
scan_bars("notes N4 under-zone (dark)", im.sum(axis=2) < 400, 489, 500, 100, 320)
scan_bars("GD header under-zone (red)", red_ink, 128, 140, 100, 400)
scan_bars("Notes hdr under-zone (red)", red_ink, 322, 334, 100, 200)

# ---------- 3. per-row cumulative word-position verification at 17pt ----------
print("\n== cumulative word fit at candidate sizes ==")
# spec bold map (from recreation_brief); blue rows
B = True; R = False
rows = {
 "A": [("​", None)] }
# define segments: (text, bold) ; underline noted separately
SEG_A = [("[1] Start with initial ", R), ("Random Weights (W)", B)]
SEG_D = [("[3] Stop when the ", R), ("gradient", R, "u"), (" ", R), ("is", R), (" ", R), ("almost zero", B, "u"),
         (" ", R), ("(this is at the minimum value of the function)", R)]
L2 = "[2] Update the weights by moving along the direction of negative gradient of Loss function (w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)"
# hypothesis H1: wrap after "function"; row C = "(w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)"
# hypothesis H2: wrap after "(w.r.t. W)"
def segs_B_C(hyp):
    words = L2.split()
    if hyp == 1:
        cut = words.index("function") + 1  # after 'function'
        rB = " ".join(words[:cut]); rC = " ".join(words[cut:])
    else:
        cut = words.index("W)") + 1
        rB = " ".join(words[:cut]); rC = " ".join(words[cut:])
    return rB, rC

def split_runs(text, bold_set, underl_set, s):
    """cumulative x of each word given bold/underline word sets"""
    out = []
    x = 0.0
    for w in text.split(" "):
        bold = w in bold_set
        a = adv(w, s, bold)
        out.append((w, x, x + a, bold))
        x += a + adv(" ", s, False)
    return out

for hyp in (1, 2):
    rB, rC = segs_B_C(hyp)
    print(f"\n-- hyp {hyp}: rowB='{rB[-60:]}' rowC='{rC[:60]}'")
    for s in (16, 17, 18):
        wB = sum(adv(t, s, bd) for t, bd, *rest in
                 [(x, x in ("negative gradient", "Loss function", "w.r.t. W")) for x in [rB]] for t, bd in [(rB, False)])
        # simpler: compute full-advance honoring bold substrings
        def adv_mixed(text, s, bold_phrases):
            total = 0.0
            # tokenize by characters is overkill; approximate: strip bold phrases measuring separately
            rest = text
            for ph in bold_phrases:
                if ph in rest:
                    pre, rest2 = rest.split(ph, 1)
                    total += adv(pre, s, False) + adv(ph, s, True)
                    rest = rest2
            total += adv(rest, s, False)
            return total
        boldB = ["negative gradient", "Loss function", "w.r.t. W"]
        boldC = ["moving step is a hyper parameter", "AKA Learning Rate"]
        aB = adv_mixed(rB, s, boldB)
        aC_mixed = adv_mixed(rC, s, boldC)
        aC_allreg = adv(rC, s, False)
        print(f"  s={s}: rowB adv={aB:.0f} (meas 701)  rowC adv={aC_mixed:.0f} mixed / {aC_allreg:.0f} allreg (meas 544)")

# detailed word-position table for the chosen hypothesis at 17pt
print("\n== word-position verification, hyp1, s=17 ==")
rB, rC = segs_B_C(1)
BOLD_B_WORDS = {"negative", "gradient", "Loss", "function", "w.r.t.", "W)"}  # 'negative gradient','Loss function','w.r.t. W'
BOLD_C_WORDS = {"moving", "step", "hyper", "parameter,", "AKA", "Learning", "Rate"}
def word_table(text, boldw, s, x_start, label):
    print(f"  {label} (start x={x_start}):")
    x = float(x_start)
    for w in text.split(" "):
        a = adv(w, s, w in boldw)
        print(f"    '{w}': x {x:.0f}..{x+a:.0f} ({'bold' if w in boldw else 'reg'})")
        x += a + adv(" ", s, False)
word_table(rB, BOLD_B_WORDS, 17, 146, "rowB")
word_table(rC, BOLD_C_WORDS, 17, 146, "rowC (blue until 'parameter,', red 'AKA Learning Rate')")

# rows A and D at 17pt
def word_table_segs(segs, s, x_start, label):
    print(f"  {label} (start x={x_start}):")
    x = float(x_start)
    for seg in segs:
        t, bd = seg[0], seg[1]
        if t == "":
            continue
        a = adv(t, s, bd)
        print(f"    '{t[:40]}': x {x:.0f}..{x+a:.0f} ({'bold' if bd else 'reg'})")
        x += a
word_table_segs(SEG_A, 17, 146, "rowA")
word_table_segs(SEG_D, 17, 146, "rowD")

# notes rows at 17pt
N1 = "Least Squares Linear regression objective function is a convex function (even with"
N1b = ["is a convex function"]
N2 = "regularizer). This means it has ONE Minimum (good news )."
N2b = ["ONE Minimum"]
N3 = "GD will approximately find this minimum value but at a variable number of steps depending on the"
N3b = ["variable number of steps"]
N4 = "used Learning Rate"
N4b = ["Learning Rate"]
def adv_mixed(text, s, phrases):
    total = 0.0
    rest = text
    for ph in sorted(phrases, key=len, reverse=True):
        if ph in rest:
            pre, rest2 = rest.split(ph, 1)
            total += adv(pre, s, False) + adv(ph, s, True)
            rest = rest2
    total += adv(rest, s, False)
    return total
for nm, t, ph, meas in (("N1", N1, N1b, 660), ("N2", N2, N2b, 466), ("N3", N3, N3b, 727), ("N4", N4, N4b, 185)):
    a = adv_mixed(t, 17, ph)
    print(f"  {nm}: adv17={a:.0f} vs meas {meas}   (all-reg={adv(t,17,False):.0f})")

# GD header + Notes header at 17pt bold
print(f"  GD hdr: adv17 bold={adv('Gradient Descent (GD) Algorithm:', 17, True):.0f} vs meas 284 (reg={adv('Gradient Descent (GD) Algorithm:', 17, False):.0f})")
print(f"  Notes hdr: adv17 bold={adv('Notes:', 17, True):.0f} vs meas 51 (reg={adv('Notes:', 17, False):.0f})")
for s in (15, 16, 17, 18):
    print(f"  s={s}: GD hdr bold={adv('Gradient Descent (GD) Algorithm:', s, True):.0f}  Notes: bold={adv('Notes:', s, True):.0f}")

# ---------- 4. bullet disc measure ---------------------------------------------
print("\n== bullet disc (N1 window) ==")
win = ink_white[340:364, 88:106]
ys2, xs2 = np.where(win)
if len(ys2):
    print(f"  bullet ink y {ys2.min()+340}-{ys2.max()+340} x {xs2.min()+88}-{xs2.max()+88} (w={xs2.max()-xs2.min()+1}, h={ys2.max()-ys2.min()+1})")
win = ink_white[439:463, 88:106]
ys2, xs2 = np.where(win)
if len(ys2):
    print(f"  bullet ink (N3) y {ys2.min()+439}-{ys2.max()+439} x {xs2.min()+88}-{xs2.max()+88}")

# ---------- 5. baseline / band geometry per row (for valign placement) ----------
print("\n== per-row band tops (uniform pitch check) ==")
prof = ink_white[:, 85:861].sum(axis=1)
for y in range(95, 505):
    if prof[y] > 3 and (y == 95 or prof[y-1] <= 3):
        # band start
        yb = y
        while yb < 504 and prof[yb+1] > 3:
            yb += 1
        print(f"  band y {y}-{yb} (h={yb-y+1})")
