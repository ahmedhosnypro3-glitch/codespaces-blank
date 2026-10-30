#!/usr/bin/env python3
"""Self-check for slide 008 attempt 1 (pre-judge, founder directive 2026-10-10).
Checks: full-frame ink census (no stray ink), frame containment, one-band-per-
element (no wrap), badge numeral ink, explicit lineSpacing present in XML.
Run: python3 selfcheck_attempt_1.py   (from project root)
"""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide008/"
r = np.asarray(Image.open(QA + "render_1.png").convert("RGB")).astype(int)
S = r.shape[0] / 540.0
fails = []

# --- 1. full-frame ink census -------------------------------------------------
bg = np.array([233, 233, 231])          # E9E9E7 panel
dist = np.abs(r - bg).sum(axis=2)
ink = dist > 90                          # clearly-not-panel ink
# exclude chrome: strokes (x 58.5 / 901 frame px), badge zone, bottom stroke row
W = r.shape[1]
m = np.ones(W, bool)
m[int(56*S):int(64*S)] = False           # left stroke column band
m[int(897*S):int(905*S)] = False         # right stroke column band
m[int(0*S):int(52*S)] = False            # canvas margin left of panel
m[int(906*S):int(W)] = False             # canvas margin right of panel
ink_clipped = ink.copy()
ink_clipped[:, ~m] = False
ink_clipped[int(536*S):, :] = False      # bottom stroke row band
ink_clipped[int(45*S):int(100*S), int(845*S):int(905*S)] = False  # badge zone
rows = np.where(ink_clipped.sum(axis=1) > 3)[0]
print(f"1. non-chrome ink rows: {rows.min()/S:.1f}..{rows.max()/S:.1f} (frame px)")
groups = []
if len(rows):
    cur = [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] > int(6*S):
            groups.append((cur[0]/S, cur[-1]/S)); cur = [y]
        else:
            cur.append(y)
    groups.append((cur[0]/S, cur[-1]/S))
print(f"   ink row-bands: {groups}")
# expected: title band ~230..264 AND subtitle ~301..329 only (bands may merge
# if within 6px gap; they are 37px apart so must be separate)
if len(groups) != 2:
    fails.append(f"unexpected ink band count {len(groups)}: {groups}")
else:
    print("   OK: exactly 2 content bands (title + subtitle), nothing stray")

# --- 2. frame containment -----------------------------------------------------
for name, (y0, y1, x0, x1) in {"title": (225, 270, 95, 830), "sub": (295, 335, 250, 675)}.items():
    win = ink[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    cols = np.where(win.sum(axis=0) > 0)[0]
    inside = (x0 + cols.min()/S) > 54 and (x0 + cols.max()/S) < 903
    print(f"2. {name}: ink cols {x0+cols.min()/S:.1f}..{x0+cols.max()/S:.1f} inside panel x54..903: {inside}")
    if not inside: fails.append(f"{name} ink outside panel")

# --- 3. one-band-per-element (no wrap) ----------------------------------------
# title: single contiguous band inside rows 215..285
w = ink[int(215*S):int(285*S), :]
rr = np.where(w.sum(axis=1) > 3)[0]
gaps = np.where(np.diff(rr) > int(6*S))[0]
print(f"3. title band gaps>6px: {len(gaps)} (0 = no wrap)")
if len(gaps): fails.append("title wrapped onto second line")
w2 = ink[int(290*S):int(345*S), :]
rr2 = np.where(w2.sum(axis=1) > 3)[0]
gaps2 = np.where(np.diff(rr2) > int(6*S))[0]
print(f"   subtitle band gaps>6px: {len(gaps2)} (0 = no wrap)")
if len(gaps2): fails.append("subtitle wrapped onto second line")

# --- 4. badge numeral ink ------------------------------------------------------
badge = r[int(58*S):int(90*S), int(858*S):int(895*S)]
dark = (badge.sum(axis=2) < 260)
print(f"4. badge dark-ink px (numeral '8'): {dark.sum()}")
if dark.sum() < 60: fails.append("badge numeral ink missing/too sparse")

# --- 5. lineSpacing pinned in XML ---------------------------------------------
import zipfile, re
z = zipfile.ZipFile("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_008_recreated.pptx")
xml = z.read("ppt/slides/slide1.xml").decode()
lns = re.findall(r'<a:lnSpc><a:spcPts val="(\d+)"/></a:lnSpc>', xml)
print(f"5. lineSpacing pins in slide XML: {lns}")
if len(lns) < 2: fails.append("lineSpacing not pinned on both text boxes")

print()
print("SELF-CHECK:", "FAIL -> " + "; ".join(fails) if fails else "ALL PASS")
