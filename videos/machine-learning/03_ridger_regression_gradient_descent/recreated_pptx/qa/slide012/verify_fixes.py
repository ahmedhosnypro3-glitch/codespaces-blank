#!/usr/bin/env python3
"""Verify the two attempt-3 fixes (test-table colour phase; arrow anchor) in
qa/slide012/render_3.png against the original frame. Both fixes were derived
from measurement, so the acceptance test is measurement again."""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_012.jpg"
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
S = 2001 / o.shape[1]

ok = True


def hue(a, x0, y0, x1, y1, scale):
    sub = a[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    flat = sub.reshape(-1, 3)
    R, G, B = flat[:, 0], flat[:, 1], flat[:, 2]
    b = flat.max(axis=1) - flat.min(axis=1)
    red = int(((R > G + 25) & (R > B + 25) & (b > 30) & (R > 120)).sum())
    blue = int(((B > R + 25) & (B > G + 25) & (b > 30) & (B > 120)).sum())
    return "RED" if red > blue else ("BLUE" if blue > red else "tie")


for tag, rend_path, sc in (("render_2 (pre-fix)", "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/render_2.png", S),
                           ("render_3 (post-fix)", "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/render_3.png", S)):
    r = np.asarray(Image.open(rend_path).convert("RGB")).astype(int)
    TX = [719, 770, 821, 871]
    TY = [128, 160, 190, 221, 252]
    orig_phase = [hue(o, TX[c]+4, TY[0]+4, TX[c+1]-4, TY[1]-4, 1.0) for c in range(3)]
    rend_phase = [hue(r, TX[c]+4, TY[0]+4, TX[c+1]-4, TY[1]-4, sc) for c in range(3)]
    print(f"{tag}: ORIGINAL test-table header phase {orig_phase}   RENDER {rend_phase}")

    # arrow: strict-red bbox strictly inside the gap x575..706
    Rr, Gr, Br = r[:, :, 0], r[:, :, 1], r[:, :, 2]
    strict = (Rr > 150) & (Gr < 90) & (Br < 90)
    z = strict[int(244*sc):int(258*sc), int(575*sc):int(706*sc)]
    ys, xs = np.nonzero(z)
    if len(xs):
        print(f"{tag}: render arrow-mask bbox (y244..258 window) "
              f"x{575+xs.min()/sc:.0f}..{575+xs.max()/sc:.0f} y{244+ys.min()/sc:.0f}..{244+ys.max()/sc:.0f}")
    else:
        print(f"{tag}: no arrow ink in y244..258 window")

# The original's arrow: strict red = 0 px in the gap (it is a faint JPEG
# hairline); measured geometry was y250..251, x670..705 with head fringe at
# x669..670 y246..249.
Rr, Gr, Br = o[:, :, 0], o[:, :, 1], o[:, :, 2]
loose = (Rr > Gr + 18) & (Rr > Br + 18) & (Rr > 95)
ys, xs = np.nonzero(loose[244:258, 575:706])
print(f"\nORIGINAL arrow (loose mask, y244..257 x575..705): bbox x{575+xs.min()}..{575+xs.max()} "
      f"y{244+ys.min()}..{244+ys.max()}  px={len(xs)}")
print("TARGET: render must place its arrow head near x670 and its stroke at y~250, "
      "within the callout-to-table gap.")

r3 = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/render_3.png").convert("RGB")).astype(int)
Rr, Gr, Br = r3[:, :, 0], r3[:, :, 1], r3[:, :, 2]
strict = (Rr > 150) & (Gr < 90) & (Br < 90)
whole = strict[int(240*sc):int(330*sc), int(560*sc):int(715*sc)]
ys, xs = np.nonzero(whole)
print(f"render_3 arrow strict-red bbox (y240..330, x560..715): "
      f"x{560+xs.min()/sc:.0f}..{560+xs.max()/sc:.0f} y{240+ys.min()/sc:.0f}..{240+ys.max()/sc:.0f}")
print("\n=== ARROW PLUS FIX CHECK ===")
# head must be near x670, stroke near y250.5, and the stroke must not run to x571
head_near = abs((560 + xs.min()) / sc - 670) <= 14
stroke_y = (240 + ys.min() / sc)
print(f"head left edge near x670 (tol 14px): {head_near}   stroke top y={stroke_y:.0f} (orig 246)")
