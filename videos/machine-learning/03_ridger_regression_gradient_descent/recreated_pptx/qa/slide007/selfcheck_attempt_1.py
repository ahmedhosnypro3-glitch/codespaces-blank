#!/usr/bin/env python3
"""Mandatory pre-judge self-check for slide 007 attempt 1 (render_4.png).
Frame measurements from unique_slides/slide_007.jpg (960x540 px = 1px = 1pt):
  house chrome: white canvas + E9E9E7 panel x54..903 y45..540 + C00000 strokes
  left x58.5 / right x901 / bottom y538.5 (NO top stroke) + badge center (876,73) d~35
  FDFD96 fill / 6A5ACD ring / Arial bold 18pt numeral 333333 = 7.
  title: red ink x242..677, y78..100 (30pt bold)
  blue content box: outer x78..885, y120..513
  body text lines (ink-top / ink-x-range / font size):
    1 intro  y154, x90..807  ~18pt  (dark red/maroon)
    2 header y202, x90..560  ~20pt  (#0000FF bold, underlined rows y220-221)
    3 bullet1 y249, x92..308 ~22pt  (#0000FF bold)
    4 bullet2 y294, x92..554 ~22pt  (#0000FF bold + #C00000 italic paren)
    5 bullet3 y348, x92..630 ~22pt  (#0000FF bold + #C00000 italic paren)
    6 bullet4 y397, x92..858 ~22pt  (#0000FF bold + #C00000 italic paren)
  inter-line pitch (ink-top to ink-top): 48, 47, 45, 54, 49 (pt).
  FRAME-vs-SPEC deviations resolved PIL-first:
    - intro line has NO underline in the frame (rows y173-175 carry only ~90 px of
      descender ink vs the header underline's 472 px) -> drawn without underlines.
    - header underline IS present in the frame -> drawn (via pptxgenjs underline).
    - bullet glyph in the frame is a small filled arrowhead (x93..~110, 18px tall);
      pptxgenjs U+27A2 renders ~34px tall in LO -> drawn as an explicit triangle.
"""
from PIL import Image
import numpy as np

R = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide007/render_6.png"
O = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_007.jpg"
r = Image.open(R).convert("RGB")
ra = np.array(r).astype(int)
Hh, Ww, _ = ra.shape
S = Ww / 960.0  # render px per pt
fails = []
print(f"render {Ww}x{Hh} px @150dpi (scale {S:.4f} px/pt)")

# ---------- house chrome (house_chrome_check.py already PASSED separately) ----------
print(f"canvas corners: {tuple(ra[3,3])} {tuple(ra[3,Ww-4])} {tuple(ra[Hh-4,3])} {tuple(ra[Hh-4,Ww-4])} (expect 255,255,255)")
# panel E9E9E7 sample inside panel but outside content box: y=60pt -> row 125, x=700pt
print(f"panel sample (700pt,60pt)=({int(700*S)},{int(60*S)}): {tuple(ra[int(60*S), int(700*S)])} (expect ~233,233,231)")
print(f"badge center (876pt,73pt): {tuple(ra[int(73*S), int(876*S)])} (expect FDFD96-ish)")

# ---------- helpers ----------
white = (ra[:, :, 0] > 240) & (ra[:, :, 1] > 240) & (ra[:, :, 2] > 235)
ink = ~white
red = (ra[:, :, 0] > 150) & (ra[:, :, 1] < 90) & (ra[:, :, 2] < 90)
blue = (ra[:, :, 2] > (ra[:, :, 0] + ra[:, :, 1]) / 2 + 40) & (ra[:, :, 2] > 120)

def rows_in(mask, y0, y1, x0, x1, thr=3):
    w = np.zeros_like(mask); w[y0:y1, x0:x1] = True
    s = mask & w
    c = s.sum(axis=1)
    rs = [y for y in range(y0, y1) if c[y] > thr]
    if not rs:
        return []
    out, start, prev = [], rs[0], rs[0]
    for y in rs[1:]:
        if y > prev + 3:
            out.append((start, prev)); start = y
        prev = y
    out.append((start, prev))
    res = []
    for (a, b) in out:
        xs = np.where(s[a:b + 1].any(axis=0))[0]
        if len(xs):
            res.append((a / S, b / S, xs.min() / S, xs.max() / S))
    return res

# ---------- 1. FRAME CONTAINMENT ----------
print("\n[1] containment: all BODY ink strictly inside the blue box")
# Body ink = blue or red-dominant (the box's own border is blue, its fill is white).
# The house chrome (panel/strokes/badge) is excluded by testing only text-like colors
# inside the slide's content area and asserting nothing lands outside the box band.
tb = red | blue
# drop the box's own border stroke pixels so they never count as body ink
tb[:, 160:166] = False; tb[:, 1841:1846] = False
tb[248:253, :] = False; tb[1066:1072, :] = False
# house chrome strokes are C00000-red too: exclude the left/right vertical stroke columns
# (x58.5 and x901 -> render px 122..125 / 1878..1881) and the bottom stroke row.
tb[:, 120:128] = False; tb[:, 1876:1884] = False
tb[1118:1126, :] = False
# box borders measured in render px: L x160..164, R x1842..1845, T y248..251, B y1067..1070
out = tb.copy()
out[:248, :] = False; out[1071:, :] = False
out[:, :159] = False; out[:, 1847:] = False
out[248:1071, 159:1847] = False
ys, xs = np.where(out)
print(f"    text-colored ink outside box band: {len(ys)} px")
if len(ys):
    print(f"    -> x_pt {xs.min()/S:.1f}..{xs.max()/S:.1f} y_pt {ys.min()/S:.1f}..{ys.max()/S:.1f}")
    fails.append(f"containment: {len(ys)} px text-colored ink outside the box")
# box-interior text-ink bbox
inter = tb.copy()
inter[:248, :] = False; inter[1071:, :] = False
inter[:, :159] = False; inter[:, 1847:] = False
ys, xs = np.where(inter)
print(f"    box-interior text-ink bbox: x {xs.min()/S:.1f}..{xs.max()/S:.1f} y {ys.min()/S:.1f}..{ys.max()/S:.1f}")
if xs.min()/S < 80 or xs.max()/S > 882 or ys.min()/S < 122 or ys.max()/S > 512:
    fails.append("box-interior text-ink crosses box border")

# ---------- 2. TEXT LINES + PITCH ----------
print("\n[2] text lines / pitch (orig expected tops: 154,202,249,294,348,397)")
bands = [("intro", 300, 385), ("header", 410, 460), ("bullet1", 505, 555),
         ("bullet2", 598, 655), ("bullet3", 713, 770), ("bullet4", 818, 875)]
exp = [154, 202, 249, 294, 348, 397]
got = {}
for (name, y0, y1) in bands:
    # text lines: use blue for header/bullets, red for intro
    m = red if name == "intro" else blue
    ls = rows_in(m, y0, y1, 168, 1838)
    # keep only the widest line (the text, not a stray stroke)
    ls = [l for l in ls if (l[3]-l[2]) > 20]
    print(f"    {name:8s}: " + " | ".join(f"y{a:.1f}..{b:.1f} x{c:.1f}..{d:.1f}" for (a,b,c,d) in ls))
    if ls:
        got[name] = ls[0]
tops = [got[n][0] for n in ["intro","header","bullet1","bullet2","bullet3","bullet4"] if n in got]
print("    tops:", [f"{t:.1f}" for t in tops])
names = ["intro","header","bullet1","bullet2","bullet3","bullet4"]
for i in range(len(tops)):
    d = abs(tops[i] - exp[i])
    print(f"      {names[i]:8s} top {tops[i]:.1f} vs orig {exp[i]} -> Δ{d:.1f}")
    if d > 4: fails.append(f"{names[i]} top off by {d:.1f}")
for i in range(1, len(tops)):
    p = tops[i]-tops[i-1]; e = exp[i]-exp[i-1]
    print(f"      pitch {names[i-1]}->{names[i]}: {p:.1f} vs {e} -> Δ{abs(p-e):.1f}")
    if abs(p-e) > 3: fails.append(f"pitch {names[i]} off by {abs(p-e):.1f}")

# ---------- 3. UNDERLINES ----------
print("\n[3] underlines (frame: header has one at y220-221; intro has NONE)")
# header underline = blue strokes BELOW the text baseline, wide, thin
hb = rows_in(blue, int(215*S), int(238*S), int(168*S), int(1838*S), thr=100)
wide = [l for l in hb if (l[3]-l[2]) > 300]
print(f"    header underline strokes below baseline: {len(wide)} (expect 1)")
if not wide: fails.append("header underline missing")
# intro: assert NO red stroke below the intro baseline (y>170pt)
rb = rows_in(red, int(169*S), int(196*S), int(168*S), int(1838*S))
wide_r = [l for l in rb if (l[3]-l[2]) > 60]
print(f"    intro stray red strokes below baseline: {len(wide_r)} (expect 0)")
if wide_r: fails.append(f"intro has unexpected underline strokes: {wide_r}")

# ---------- 4. INK PRESENCE / NO EMPTY REGION ----------
print("\n[4] ink presence")
for (name, y0, y1) in bands:
    n = ink[y0:y1, int(168*S):int(1838*S)].sum()
    print(f"    {name:8s}: {n} px")
    if n < 100: fails.append(f"{name} nearly empty")

# ---------- 5. BULLET GLYPH ----------
print("\n[5] bullet arrowheads (frame: small filled arrowhead, ~18pt tall)")
for (name, y0, y1) in [("bullet1", 505, 555), ("bullet2", 600, 650),
                       ("bullet3", 715, 765), ("bullet4", 820, 870)]:
    ls = rows_in(blue, y0, y1, int(88*S), int(120*S))
    if ls:
        a,b,c,d = ls[0]
        print(f"    {name:8s}: x_pt {c:.1f}..{d:.1f} y_pt {a:.1f}..{b:.1f} (h {b-a:.1f})")
    else:
        print(f"    {name:8s}: NO arrowhead ink in x88..120 band")

# ---------- 6. NO STRAY MARKS BELOW BULLET4 ----------
print("\n[6] region below bullet4 (frame has nothing below y~430 in the box)")
below = rows_in(tb, int(432*S), min(int(1062*S), Hh-1), int(168*S), int(1838*S))
print(f"    ink rows below y430pt: {len(below)} (expect 0)")
if below: fails.append(f"unexpected ink below bullet4: {below}")

print("\nSELFCHECK " + ("FAIL: " + "; ".join(fails) if fails else "PASS"))
print("__DONE__")
