#!/usr/bin/env python3
"""Slide 003 attempt-8 closed-loop selfcheck: render_8.png vs the original.

Checks every take-6 agreed fix actually landed in the new render, in frame px.
"""
import os
import numpy as np
from PIL import Image

B = None
for r in ("/workspaces/codespaces-blank/ai_llm_slides",
          "/workspaces/codespace-blank/ai_llm_slides"):
    c = r + "/videos/machine-learning/03_ridger_regression_gradient_descent"
    if os.path.exists(c + "/unique_slides/slide_003.jpg"):
        B = c
        break
QA = B + "/recreated_pptx/qa/slide003"
ORIG = B + "/unique_slides/slide_003.jpg"
RENDER = QA + "/render_8.png"
S = 2001 / 960.0  # render px per frame px (150dpi)

a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r8 = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
rs = r8.shape[0] / 540.0
print(f"orig {a.shape[1]}x{a.shape[0]}  render {r8.shape[1]}x{r8.shape[0]} scale {rs:.4f}")


def frac(ao, m, win):
    x0, y0, x1, y1 = [int(v) for v in win]
    return m[y0:y1, x0:x1].mean()


def report(name, win, fr_orig, fr_render, tol=0.02):
    ok = abs(fr_orig - fr_render) <= tol
    print(f"  {'OK ' if ok else 'FAIL'} {name:44s} orig={fr_orig:.3f} render={fr_render:.3f}")
    return ok


R, G, Bc = a[:, :, 0], a[:, :, 1], a[:, :, 2]
Rr, Gr, Br = r8[:, :, 0], r8[:, :, 1], r8[:, :, 2]


def m_red(A):
    return (A[:, :, 0] > 145) & (A[:, :, 0] - A[:, :, 1] > 45) & (A[:, :, 0] - A[:, :, 2] > 45)


def m_dark(A):
    return (A[:, :, 0] < 110) & (A[:, :, 1] < 110) & (A[:, :, 2] < 110)


def m_yellow(A):
    return (A[:, :, 0] > 240) & (A[:, :, 1] > 240) & (A[:, :, 2] < 190) & (A[:, :, 2] > 100)


def m_cyan(A):
    return (A[:, :, 0] < 225) & (A[:, :, 1] > 235) & (A[:, :, 2] > 235) & (A[:, :, 1] - A[:, :, 0] > 15)


def m_pink(A):
    return (A[:, :, 0] > 235) & (A[:, :, 1] > 140) & (A[:, :, 1] < 215) & (A[:, :, 2] > 165) & \
           (A[:, :, 2] < 230) & (A[:, :, 0] - A[:, :, 1] > 30)


def m_gray(A):
    return (np.abs(A[:, :, 0] - 128) < 45) & (np.abs(A[:, :, 1] - 128) < 45) & (np.abs(A[:, :, 2] - 128) < 45)


def win_r8(win):
    return tuple(int(round(v * rs)) for v in win)


results = []
print("\n== title: one line band, blue+red ==")
# ink rows in y60..95 must be ONE band in both
for nm, A, w in (("orig", a, 1.0), ("render", r8, rs)):
    sub = (m_dark(A) | m_red(A))[int(60 * w):int(96 * w), int(60 * w):int(905 * w)]
    rows = sub.sum(axis=1)
    nz = np.where(rows > 0)[0]
    print(f"  {nm}: ink rows y{60 + nz.min() / w:.0f}..{60 + nz.max() / w:.0f}")
print("\n== top box ==")
for nm, mm in (("yellow band", m_yellow), ("cyan band", m_cyan), ("pink band", m_pink)):
    for lbl, A, w in (("orig", a, 1.0), ("render", r8, rs)):
        win = (280, 110, 600, 300) if lbl == "orig" else win_r8((280, 110, 600, 300))
        sub = mm(A)[win[1]:win[3], win[0]:win[2]]
        ys, xs = np.where(sub)
        if len(ys):
            print(f"  {nm:11s} {lbl:6s}: x{(win[0] + xs.min()) / w:.0f}..{(win[0] + xs.max()) / w:.0f} "
                  f"y{(win[1] + ys.min()) / w:.0f}..{(win[1] + ys.max()) / w:.0f}")
        else:
            print(f"  {nm:11s} {lbl:6s}: NONE")
# interior entries inside each band (dark ink fraction)
for nm, win in (("yellow interior", (302, 150, 328, 268)),
                ("cyan interior", (378, 150, 410, 268)),
                ("pink interior", (521, 150, 549, 268))):
    fo = frac(a, m_dark(a), win)
    fr = frac(r8, m_dark(r8), win_r8(win))
    results.append(report(nm + " dark-ink frac", win, fo, fr, 0.06))
print("\n== ellipsis column x415..479 y115..300 ==")
for nm, mm in (("gray ink", m_gray), ("any ink dark", m_dark)):
    fo = frac(a, mm(a), (418, 115, 477, 300))
    fr = frac(r8, mm(r8), win_r8((418, 115, 477, 300)))
    results.append(report(nm, (418, 115, 477, 300), fo, fr, 0.08))
print("\n== bl box ==")
for nm, win in (("red border left strip", (78, 330, 84, 510)),
                ("yellow row band", (150, 368, 430, 390)),
                ("cyan row band", (150, 397, 430, 423)),
                ("pink row band", (150, 456, 430, 478)),
                ("gray bracket zone", (430, 360, 445, 484)),
                ("dim labels row", (80, 470, 530, 505)),
                ("w-vector entries", (455, 330, 525, 480))):
    fo = frac(a, m_dark(a), win)
    fr = frac(r8, m_dark(r8), win_r8(win))
    results.append(report(nm + " dark-ink frac", win, fo, fr, 0.05))
print("\n== br box: three text lines ==")
for nm, win in (("Y=XW line", (580, 355, 750, 385)),
                ("where line 1", (580, 400, 750, 435)),
                ("where line 2", (580, 450, 750, 480))):
    fo = frac(a, m_dark(a) | m_red(a), win)
    fr = frac(r8, m_dark(r8) | m_red(r8), win_r8(win))
    results.append(report(nm + " ink frac", win, fo, fr, 0.05))
print("\n== arrow (thin gray line x538..572 y388..396) ==")
fo = frac(a, m_gray(a), (536, 386, 574, 398))
fr = frac(r8, m_gray(r8), win_r8((536, 386, 574, 398)))
results.append(report("arrow gray frac", (536, 386, 574, 398), fo, fr, 0.35))

print(f"\nSELFCHECK: {'PASS' if all(results) else 'FAIL'} ({sum(results)}/{len(results)} checks)")
