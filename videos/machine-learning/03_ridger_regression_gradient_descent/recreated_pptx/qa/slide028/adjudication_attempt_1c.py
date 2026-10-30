#!/usr/bin/env python3
"""Adjudicate judge_attempt_1.txt findings — colour + geometry facts.

Original frame (960x540) vs render_3.png (2001x1125, scale 2.0833).
"""
import numpy as np
from collections import Counter
from PIL import Image

ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/render_3.png'
o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(QA).convert('RGB')).astype(int)
S = r.shape[0] / 540.0
def cv(v): return int(round(v * S))

def nonbg(a, bg):
    return np.any(np.abs(a - np.array(bg)) > 26, axis=2)

# ---------- 1. "Loss" rotated label colour ----------
print("=== 'Loss' y-axis label colour ===")
for nm, a, sc in [('ORIG', o, 1.0), ('REND', r, S)]:
    for side, (x0, x1, y0, y1) in [('left', (118, 150, 214, 250)), ('right', (470, 502, 210, 246))]:
        sub = a[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
        bg = np.median(sub.reshape(-1, 3), axis=0)
        m = nonbg(sub, bg)
        px = sub[m] if m.any() else np.zeros((0, 3))
        if len(px):
            c = Counter(tuple(p) for p in px)
            top = c.most_common(3)
            mean = px.mean(axis=0).round(0)
            print(f"  {nm} {side}: n={m.sum():4d} bg={tuple(bg.round(0))} mean={tuple(mean)} top={top}")
        else:
            print(f"  {nm} {side}: no non-bg ink")

# ---------- 2. axis arrow colour + extent ----------
print("\n=== axis arrow colour (red components) ===")
def redm(a):
    return (a[:, :, 0] > 150) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110)
ro = redm(o); ro[:, :100] = False; ro[:, 885:] = False; ro[100:160, :] = False; ro[530:, :] = False
# exclude the title band y70..102 and the house strokes
ro[:int(103), :] = False
rr = redm(r)
rr[:, :cv(100)] = False; rr[:, cv(885):] = False; rr[:cv(160), cv(103):] = False; rr[cv(530):, :] = False
for nm, m, sc in [('ORIG', ro, 1.0), ('REND', rr, S)]:
    ys, xs = np.where(m)
    if not len(ys):
        print(f"  {nm}: no red axis ink"); continue
    print(f"  {nm}: red px={len(ys)} bbox x{xs.min()/sc:.0f}-{xs.max()/sc:.0f} y{ys.min()/sc:.0f}-{ys.max()/sc:.0f}")
    # vertical arrow shaft: columns with tall red runs
    colsum = m.sum(axis=0)
    tall = [round(x / sc) for x in np.where(colsum > 40)[0]]
    rowsum = m.sum(axis=1)
    wide = [round(y / sc) for y in np.where(rowsum > 10)[0]]
    print(f"    tall red cols (>=40px): {tall[:6]}{'...' if len(tall) > 6 else ''} (n={len(tall)})")
    print(f"    wide red rows (>=10px): {wide[:8]}{'...' if len(wide) > 8 else ''} (n={len(wide)})")

# ---------- 3. curve line width ----------
print("\n=== curve stroke width (blue 2E75B6 family) ===")
def bluem(a, tol=95):
    return (np.abs(a[:, :, 0] - 46) < tol) & (np.abs(a[:, :, 1] - 117) < tol) & (np.abs(a[:, :, 2] - 182) < tol)
for nm, a, sc, xr in [('ORIG left ', o, 1.0, (100, 470)),
                      ('REND left ', r, S, (cv(100), cv(470))),
                      ('ORIG right', o, 1.0, (478, 860)),
                      ('REND right', r, S, (cv(478), cv(860)))]:
    b = bluem(a); b[:, :xr[0]] = False; b[:, xr[1]:] = False
    b[int((40 if nm.startswith('ORIG') else 40) * sc):int(126 * sc), :] = False   # exclude title/badge band
    b[int(515 * sc):, :] = False
    colsum = b.sum(axis=0)
    nz = colsum[colsum > 0]
    print(f"  {nm}: px={b.sum():6d} cols-with-ink={len(nz)} median col height={np.median(nz):.0f} "
          f"max={nz.max()} mean row-run proxy={b.sum()/max(len(nz),1):.1f}")

# ---------- 4. extra black pointer at left valley ----------
print("\n=== black pointer near left valley (build draws a line + triangle ~x255..268 y428..443) ===")
dark_o = (o[:, :, 0] < 115) & (o[:, :, 1] < 115) & (o[:, :, 2] < 115)
dark_o[:, :100] = False; dark_o[:, 885:] = False
for band in [(225, 285, 415, 460), (240, 290, 200, 250), (300, 800, 430, 460)]:
    x0, x1, y0, y1 = band
    sub = dark_o[y0:y1, x0:x1]
    print(f"  ORIG dark ink x{x0}..{x1} y{y0}..{y1}: n={sub.sum()}", end='')
    if sub.sum():
        ys, xs = np.where(sub)
        print(f" bbox x{xs.min()+x0}-{xs.max()+x0} y{ys.min()+y0}-{ys.max()+y0}")
    else:
        print()
dark_r = (r[:, :, 0] < 115) & (r[:, :, 1] < 115) & (r[:, :, 2] < 115)
dark_r[:, :cv(100)] = False; dark_r[:, cv(885):] = False
x0, x1, y0, y1 = 225, 285, 415, 460
sub = dark_r[cv(y0):cv(y1), cv(x0):cv(x1)]
ys, xs = np.where(sub)
print(f"  REND dark ink x{x0}..{x1} y{y0}..{y1}: n={sub.sum()} bbox "
      f"x{xs.min()/S+x0:.0f}-{xs.max()/S+x0:.0f} y{ys.min()/S+y0:.0f}-{ys.max()/S+y0:.0f}")

# ---------- 5. right-panel oscillation: dot y-trajectory ----------
print("\n=== right-panel dot trajectory (largest filled markers) ===")
# dilate-free approach: for each column, the lowest blue y in the dot band vs curve band
b_o = bluem(o, 95); b_o[:, :478] = False; b_o[:, 862:] = False
b_o[:int(126), :] = False; b_o[int(516):, :] = False
prof_o = []
for x in range(478, 862, 12):
    col = np.where(b_o[:, x])[0]
    if len(col):
        prof_o.append((x, col.min(), col.max(), len(col)))
print("  ORIG right blue per column (x, ytop, ybot, count):")
print("   ", prof_o)
b_r = bluem(r, 95); b_r[:, :cv(478)] = False; b_r[:, cv(862):] = False
b_r[:cv(126), :] = False; b_r[cv(516):, :] = False
prof_r = []
for x in range(478, 862, 12):
    col = np.where(b_r[:, cv(x)])[0]
    if len(col):
        prof_r.append((x, round(col.min() / S), round(col.max() / S), len(col)))
print("  REND right blue per column (x, ytop, ybot, count):")
print("   ", prof_r)
