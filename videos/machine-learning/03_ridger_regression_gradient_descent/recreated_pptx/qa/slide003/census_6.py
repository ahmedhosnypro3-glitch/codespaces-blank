#!/usr/bin/env python3
"""Slide 003 take-6 geometry census — original frame, precise bboxes.

Settles every open judge finding with PIL measurements. All coords frame px.
"""
import numpy as np
from PIL import Image
import os

B = None
for _root in ("/workspaces/codespaces-blank/ai_llm_slides",
              "/workspaces/codespace-blank/ai_llm_slides"):
    _cand = (_root + "/videos/machine-learning/"
             "03_ridger_regression_gradient_descent")
    if os.path.exists(_cand + "/unique_slides/slide_003.jpg"):
        B = _cand
        break
if B is None:
    raise SystemExit("original frame not found under either root")
ORIG = f"{B}/unique_slides/slide_003.jpg"
a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, Bc = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def m_red(t=45):
    return (R > 145) & (R - G > t) & (R - Bc > t)


def m_blue():
    return (Bc > 150) & (Bc - R > 60) & (G < 120)


def m_yellow():
    return (R > 240) & (G > 240) & (Bc < 190) & (Bc > 100)


def m_cyan():
    return (R < 225) & (G > 235) & (Bc > 235) & (G - R > 15)


def m_pink():
    return (R > 235) & (G > 140) & (G < 215) & (Bc > 165) & (Bc < 230) & (R - G > 30)


def m_dark():
    return (R < 110) & (G < 110) & (Bc < 110)


def m_gray(c=128, tol=35):
    return (np.abs(R - c) < tol) & (np.abs(G - c) < tol) & (np.abs(Bc - c) < tol)


def m_badge():
    return (R > 245) & (G > 245) & (Bc > 120) & (Bc < 210)


def bbox(m, win, label, minpx=30):
    x0, y0, x1, y1 = win
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) < minpx:
        print(f"  {label:34s} none ({len(ys)} px)")
        return None
    b = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    print(f"  {label:34s} x{b[0]}..{b[2]} y{b[1]}..{b[3]}  "
          f"(w {b[2]-b[0]+1}, h {b[3]-b[1]+1}, {len(ys)} px)")
    return b


def runs1d(vals, off, minlen=2):
    out, st = [], None
    for i, v in enumerate(vals):
        if v >= minlen and st is None:
            st = i
        elif v < minlen and st is not None:
            if i - st >= 1:
                out.append((off + st, off + i - 1))
            st = None
    if st is not None:
        out.append((off + st, off + len(vals) - 1))
    return out


print("== A. panel strokes (red) ==")
for name, win in (("left stroke x55..62", (55, 40, 63, 540)),
                  ("right stroke x896..906", (896, 40, 907, 540)),
                  ("bottom stroke y534..540", (40, 534, 920, 540)),
                  ("TOP BAND y44..52 (must be 0)", (40, 44, 920, 52))):
    x0, y0, x1, y1 = win
    print(f"  {name:34s} red px = {int(m_red()[y0:y1, x0:x1].sum())}")

print("\n== B. badge ==")
bbox(m_badge(), (840, 40, 915, 105), "badge disc")
sub = m_dark()[55:92, 858:894]
print(f"  badge numeral dark px = {int(sub.sum())}")

print("\n== C. title (y55..100) ==")
t = m_dark() | m_red() | m_blue()
sub = t[55:100, 55:905]
ys, xs = np.where(sub)
print(f"  title ink bbox x{xs.min()+55}..{xs.max()+55} y{ys.min()+55}..{ys.max()+55}")
rows = sub.sum(axis=1)
print(f"  title ink rows (nonzero): {[(55+i, int(v)) for i, v in enumerate(rows) if v > 0][:6]} ...")
# color split
for nm, mm in (("blue", m_blue()), ("red", m_red())):
    s2 = mm[60:95, 55:905]
    ys2, xs2 = np.where(s2)
    if len(ys2):
        print(f"  title {nm} ink x{xs2.min()+55}..{xs2.max()+55} y{ys2.min()+60}..{ys2.max()+60}")

print("\n== D. N Training Samples ==")
bbox(m_red(), (55, 100, 300, 215), "red label")

print("\n== E. top box ==")
bbox(m_blue(), (260, 95, 610, 310), "blue border strokes")
bbox(m_yellow(), (280, 110, 600, 300), "yellow band")
bbox(m_cyan(), (280, 110, 600, 300), "cyan band")
bbox(m_pink(), (280, 110, 600, 300), "pink band")
# ellipsis zone: gray dots between cyan and pink
bbox(m_gray(180, 45), (415, 115, 510, 300), "gray-ish dots (ellipsis col)")
# headers
hdr = m_dark()[113:140, 265:600]
cols = hdr.sum(axis=0)
print("  header dark column-runs (y113..140):", runs1d(cols, 265))
hdrr = m_red()[113:140, 265:600]
colsr = hdrr.sum(axis=0)
print("  header red column-runs:", runs1d(colsr, 265))
# y-labels
ylab = m_red()[268:302, 265:600]
cols = ylab.sum(axis=0)
print("  y-label red column-runs (y268..302):", runs1d(cols, 265))
# interior ink per band
for nm, mm, win in (("yellow", m_yellow(), (294, 336)),
                    ("cyan", m_cyan(), (372, 420)),
                    ("pink", m_pink(), (510, 552))):
    x0, x1 = win
    inner = m_dark()[145:270, x0 + 6:x1 - 6]
    print(f"  {nm} band interior dark px (y145..270) = {int(inner.sum())}")

print("\n== F. remember box ==")
bbox(m_blue(), (500, 140, 910, 235), "blue border (remember)")
# fill sample
print("  remember fill sample @(760,180):", a[180, 760].tolist())
sub = m_dark()[160:176, 650:700]
print(f"  'Remember' dark-ish px (red? check) red={int(m_red()[160:176, 650:700].sum())}")

print("\n== G. in general box ==")
bbox(m_dark(), (650, 260, 865, 300), "dark/gray border")
sub = m_red()[270:292, 660:855]
cols = sub.sum(axis=0)
print("  red text runs (y270..292):", runs1d(cols, 660))

print("\n== H. bottom-left box ==")
bbox(m_gray(128, 40), (70, 315, 545, 525), "gray border?")
bbox(m_red(), (70, 315, 545, 525), "red strokes/border")
bbox(m_yellow(), (80, 330, 530, 510), "yellow row band")
bbox(m_cyan(), (80, 330, 530, 510), "cyan row band")
bbox(m_gray(190, 40), (80, 330, 530, 510), "gray row band fill")
# per-column ink profile to locate bracket-like tall strokes
prof = (m_dark() | m_gray(128, 45))[330:505, 70:540].sum(axis=0)
tall = [(70 + i, int(v)) for i, v in enumerate(prof) if v > 90]
print("  tall vertical strokes (>90px) in y330..505:", tall)
# row profile for the bands
prof = (m_yellow() | m_cyan())[330:510, 80:530].sum(axis=1)
print("  colored row-bands (y330..510):", runs1d(prof, 330, 2000))
# dark text rows inside the bl box
prof = m_dark()[330:505, 85:525].sum(axis=1)
print("  dark text row-runs:", runs1d(prof, 330, 20))
# red in bl
prof = m_red()[330:505, 70:540].sum(axis=1)
print("  red row-runs in bl:", runs1d(prof, 330, 15))
colsr = m_red()[330:505, 70:540].sum(axis=0)
print("  red col-runs in bl:", runs1d(colsr, 70, 15))

print("\n== I. bottom-right box ==")
bbox(m_gray(128, 40), (560, 315, 770, 525), "gray border?")
bbox(m_red(), (560, 315, 770, 525), "red strokes")
prof = (m_dark() | m_red() | m_blue())[330:505, 575:755].sum(axis=1)
print("  text row-runs in br box:", runs1d(prof, 330, 10))

print("\n== J. arrow ==")
bbox(m_gray(128, 45), (520, 320, 585, 415), "gray arrow")
# arrow column profile (thin line?)
prof = m_gray(128, 45)[330:405, 525:585].sum(axis=0)
print("  arrow col-profile runs:", runs1d(prof, 525, 5))
