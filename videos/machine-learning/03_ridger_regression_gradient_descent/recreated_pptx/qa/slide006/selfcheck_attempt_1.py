#!/usr/bin/env python3
"""Self-check for slide 006, attempt 1.

Compares the 150dpi render (2001x1125) against PIL measurements of the ORIGINAL
frame unique_slides/slide_006.jpg (960x540, 1px=1pt).

MEASURED FROM ORIGINAL (frame px):
  Title    red C00000 bold Arial: ink x175..798, y247..290 (em-box top ~250), ctr x486
  Subtitle blue 0000FF italic Arial: ink x241..731, y295..329 (em-box top ~300), ctr x486
  Panel E9E9E7 x54..903 y45..540; strokes C00000 L x58.5 / R x901 / B y538.5 (NO top).
  Badge center (876,73) d~35, fill FDFD96, ring 6A5ACD, numeral "6" bold 18pt 333333.

Font calibration (Liberation Sans = metric-compatible Arial substitute used by LO):
  Title  42pt bold  -> ink w 621 vs original 623
  Subtitle 36pt italic -> ink w 492 vs original 490
"""
import sys
import numpy as np
from PIL import Image

RENDER = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide006/render_1.png"
ORIGINAL = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_006.jpg"

# Original-frame reference ink bboxes (frame px), measured above:
TITLE = (175, 798, 247, 290)   # x0, x1, y0, y1
SUB = (241, 731, 295, 329)

def main():
    rimg = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
    _ = np.asarray(Image.open(ORIGINAL).convert("RGB")).astype(int)
    Rh, Rw = rimg.shape[:2]
    sx, sy = Rw / 960.0, Rh / 540.0
    print(f"Render {Rw}x{Rh}; scale x={sx:.4f} y={sy:.4f}")
    TOL = 14  # render px (~6.7 frame px); Liberation Sans side-bearings vs the
              # original's font render ±12 px on single glyph edges without any
              # real size error — ink-width deltas stay < 10 frame px.
    fails = []
    Rr, Rg, Rb = rimg[:, :, 0], rimg[:, :, 1], rimg[:, :, 2]

    # --- 1. TITLE red ink (exclude left/right strokes at render x~122/1877 and below y700) ---
    red = (Rr > 90) & ((Rr - Rg) > 40) & ((Rr - Rb) > 10)
    red[:, :130] = False
    red[:, 1860:] = False
    red[700:, :] = False
    yt, xt = np.where(red)
    if not len(yt):
        fails.append("Title red ink not found")
    else:
        got = (xt.min(), xt.max(), yt.min(), yt.max())
        exp = (TITLE[0] * sx, TITLE[1] * sx, TITLE[2] * sy, TITLE[3] * sy)
        print(f"Title ink render x{got[0]}..{got[1]} y{got[2]}..{got[3]} (n={len(yt)})")
        print(f"  expected     x{exp[0]:.0f}..{exp[1]:.0f} y{exp[2]:.0f}..{exp[3]:.0f}")
        for nm, g_, e_ in zip(("left", "right", "top", "bottom"), got, exp):
            d = abs(g_ - e_)
            flag = "OK " if d <= TOL else "OFF"
            print(f"    {flag} {nm}: {g_} vs {e_:.0f} (diff {d:.0f})")
            if d > TOL:
                fails.append(f"Title {nm} off by {d:.0f} render px (> {TOL})")
        samp = rimg[yt.mean().astype(int), xt.mean().astype(int)]
        print(f"  color sample RGB={tuple(samp)} (want 192,0,0)")
        if not (abs(samp[0] - 192) < 14 and samp[1] < 45 and samp[2] < 45):
            fails.append(f"Title color not C00000 family: {tuple(samp)}")
        if len(yt) < 12000:
            fails.append(f"Title ink sparse ({len(yt)}) — expected ~32k at 42pt bold")

    # --- 2. SUBTITLE blue ink (exclude badge ring window render x1790..1880 y110..190) ---
    blue = (Rb > 150) & (Rr < 80) & (Rb - Rg > 100)
    blue[:, :130] = False
    blue[:, 1790:1885] = False
    blue[110:195, :] = False
    blue[700:, :] = False
    ys, xs = np.where(blue)
    if not len(ys):
        fails.append("Subtitle blue ink not found")
    else:
        got = (xs.min(), xs.max(), ys.min(), ys.max())
        exp = (SUB[0] * sx, SUB[1] * sx, SUB[2] * sy, SUB[3] * sy)
        print(f"Subtitle ink render x{got[0]}..{got[1]} y{got[2]}..{got[3]} (n={len(ys)})")
        print(f"  expected       x{exp[0]:.0f}..{exp[1]:.0f} y{exp[2]:.0f}..{exp[3]:.0f}")
        for nm, g_, e_ in zip(("left", "right", "top", "bottom"), got, exp):
            d = abs(g_ - e_)
            flag = "OK " if d <= TOL else "OFF"
            print(f"    {flag} {nm}: {g_} vs {e_:.0f} (diff {d:.0f})")
            if d > TOL:
                fails.append(f"Subtitle {nm} off by {d:.0f} render px (> {TOL})")
        samp = rimg[ys.mean().astype(int), xs.mean().astype(int)]
        print(f"  color sample RGB={tuple(samp)} (want 0,0,255)")
        if not (samp[2] > 150 and samp[0] < 70 and samp[1] < 70):
            fails.append(f"Subtitle color not 0000FF family: {tuple(samp)}")

    # --- 3. FRAME CONTAINMENT: all text ink inside the house panel ---
    # Panel render px: x 54*sx .. 903*sx, y 45*sy .. slide bottom.
    pl, pr, pt = 54 * sx, 903 * sx, 45 * sy
    for nm, (x0, x1, y0, y1) in (("title", (xt.min(), xt.max(), yt.min(), yt.max())) if len(yt) else (),
                                 ("subtitle", (xs.min(), xs.max(), ys.min(), ys.max())) if len(xs) else ()):
        if x0 < pl - TOL or x1 > pr + TOL or y0 < pt - TOL:
            fails.append(f"{nm} ink outside panel: x{x0}..{x1} y{y0}..{y1} vs panel x{pl:.0f}..{pr:.0f} y{pt:.0f}+")
        else:
            print(f"{nm} ink inside panel (panel x{pl:.0f}..{pr:.0f} y{pt:.0f}+)")

    # --- 4. Badge numeral "6" ink present in the badge disc ---
    bcx, bcy, bd = 876 * sx, 73 * sy, 17 * sx
    win = rimg[int(bcy - bd):int(bcy + bd), int(bcx - bd):int(bcx + bd)]
    dark = win.sum(axis=2) < 300
    print(f"Badge numeral ink pixels: {int(dark.sum())} (window cx{bcx:.0f} cy{bcy:.0f} d{bd:.0f})")
    if dark.sum() < 12:
        fails.append(f"Badge numeral ink too sparse ({int(dark.sum())})")

    # --- 5. Vertical gap title-bottom -> subtitle-top (original 290 -> 295 = 5 frame px) ---
    if len(yt) and len(xs):
        gap = ys.min() - yt.max()
        exp_gap = (SUB[2] - TITLE[3]) * sy
        print(f"Title-bottom -> subtitle-top gap: {gap} px (expected {exp_gap:.0f})")
        if abs(gap - exp_gap) > TOL * 2:
            fails.append(f"Title/subtitle gap {gap} vs expected {exp_gap:.0f} (tol {TOL*2})")

    if fails:
        print("\nSELF-CHECK: FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print("\nSELF-CHECK: PASS")
    print("  Title (C00000 bold 42pt) + subtitle (0000FF italic 36pt) ink geometry match")
    print("  the original frame within tol; all ink inside the house panel; badge numeral present.")
    return 0

if __name__ == "__main__":
    sys.exit(main())