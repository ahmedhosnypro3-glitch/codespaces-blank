#!/usr/bin/env python3
"""PIL-first adjudication harness for slide 003 judge verdicts (lane att20).

Frame space 960x540, 1px=1pt. Render (2001x1125, 2.0833 px/frame-px) is
LANCZOS-downscaled to frame space so both images share one coordinate system.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"


def load():
    o = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
    r = (Image.open(QA + "/render_19.png").convert("RGB")
         .resize((960, 540), Image.LANCZOS))
    return np.asarray(o).astype(int), np.asarray(r).astype(int)


def ch(px):
    r, g, b = px
    mn, mx = min(r, g, b), max(r, g, b)
    if mn < 100:
        return "#"
    if r > 150 and g < 120 and b < 120:
        return "R"
    if b > 150 and r < 120 and g < 150:
        return "B"
    if r > 205 and g > 205 and b < 200:
        return "y"
    if g > 195 and b > 195 and 175 < r < 220:
        return "c"
    if r > 235 and 160 <= g <= 205 and 185 <= b <= 218:
        return "m"
    if mn > 235:
        return "."
    if mx - mn < 24 and 150 < r < 238:
        return ","
    return " "


def dark(a):
    return a.min(axis=2) < 110


def red(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 120) & (g < 90) & (b < 90)


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None, 0
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), int(mask.sum())


def report(title):
    print("=" * 72)
    print(title)
    print("=" * 72)
    o, r = load()
    do, dr = dark(o), dark(r)

    # Finding: claimed missing intercept/ones column strip x132..192
    print("--- ones/intercept strip x132..192, per matrix row band ---")
    for label, y0, y1 in (("row1", 369, 392), ("row2", 399, 419),
                          ("row3", 429, 449), ("row4", 459, 478)):
        s = np.zeros((8, 0))
        cols = []
        for x in range(132, 193, 8):
            wo = int(do[y0:y1, x:x + 8].sum())
            wr = int(dr[y0:y1, x:x + 8].sum())
            cols.append((x, wo, wr))
        txt = " ".join(f"x{x}:{wo}/{wr}" for x, wo, wr in cols)
        tot_o = sum(c[1] for c in cols)
        tot_r = sum(c[2] for c in cols)
        print(f"{label} y{y0}-{y1}: {txt}   TOT orig={tot_o} render={tot_r}")

    # first real glyph cluster after the strip (both images)
    print("--- first data cluster x196..230, row1 band ---")
    for x in range(196, 231, 4):
        print(f"  x{x}: orig={int(do[369:392, x:x + 4].sum())} "
              f"render={int(dr[369:392, x:x + 4].sum())}")

    # y-vector third-row cell vs the original's own ellipsis glyph
    print("--- y-vector row3 cell (x110..125, y405..420) ---")
    print("  orig   :", bbox(do[405:420, 110:125]),
          " ellipsis glyph x278..304 y440..452:", bbox(do[440:452, 278:304]))
    print("  render :", bbox(dr[405:420, 110:125]))

    # red-ink census in the b-cell box
    print("--- red census b-box x455..520 y349..374 ---")
    print(f"  orig={int(red(o)[349:374, 455:520].sum())} "
          f"render={int(red(r)[349:374, 455:520].sum())}")


def window(x0, y0, x1, y1, sx=3, sy=3):
    o, r = load()
    ao = [[ch(o[y:y + sy, x:x + sx].reshape(-1, 3).mean(axis=0))
           for x in range(x0, x1, sx)] for y in range(y0, y1, sy)]
    ar = [[ch(r[y:y + sy, x:x + sx].reshape(-1, 3).mean(axis=0))
           for x in range(x0, x1, sx)] for y in range(y0, y1, sy)]
    w = max(len(x) for x in ao + ar)
    print(f"win=({x0},{y0},{x1},{y1}) sx={sx} sy={sy}  LEFT=ORIG RIGHT=render")
    for i in range(max(len(ao), len(ar))):
        lo = ao[i] if i < len(ao) else ""
        lr = ar[i] if i < len(ar) else ""
        print(f"{y0 + i * sy:3d} {''.join(lo):<{w}} | {''.join(lr)}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 5:
        window(*[int(v) for v in sys.argv[1:5]],
               *(int(v) for v in sys.argv[5:7]))
    else:
        report("SLIDE 003 PIL ADJUDICATION BASELINE (att20)")
