#!/usr/bin/env python3
"""Re-verification of the slide_003 findings with corrected measurement windows.

Frame space 960x540, 1px=1pt. Render_19 (2001x1125) LANCZOS-downscaled to 960x540
so both images share one coordinate system. Ink = min(R,G,B) < 160.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"

ROWS = (("row1", 366, 390), ("row2", 398, 421),
        ("row3", 430, 449), ("row4", 457, 480))


def load():
    o = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
    r = Image.open(QA + "/render_19.png").convert("RGB").resize((960, 540),
                                                                Image.LANCZOS)
    return np.asarray(o).astype(int), np.asarray(r).astype(int)


def glyphmap(a, x0, y0, x1, y1, thr=160):
    print(f"  x: {x0}..{x1-1}  y: {y0}..{y1-1}  thr={thr}")
    print("       " + "".join(str((x0 + i) // 10 % 10) for i in range(x1 - x0)))
    print("       " + "".join(str((x0 + i) % 10) for i in range(x1 - x0)))
    for y in range(y0, y1):
        print(f"  {y:4d} " + "".join("#" if a[y, x].min() < thr else "."
                                     for x in range(x0, x1)))


def colprofile(a, label, x0, x1, y0, y1):
    counts = [int(a[y0:y1, x].min(axis=1).lt(160).sum() if False else
                  (a[y0:y1, x] < 160).all(axis=1).sum()) for x in range(x0, x1)]
    out = " ".join(f"{x0+i}:{c}" for i, c in enumerate(counts) if c)
    print(f"  {label}: {out}")


def main():
    o, r = load()
    print("=" * 74)
    print("FINDING 1 — design-matrix first column (leading ones/intercept)")
    print("=" * 74)
    print("per-column ink counts, x=118..215, per matrix row band "
          "(LEFT=orig RIGHT=render):")
    for label, y0, y1 in ROWS:
        print(f"-- {label} y{y0}..{y1-1}")
        co = [int((o[y0:y1, x].min(axis=1) < 160).sum()) for x in range(118, 216)]
        cr = [int((r[y0:y1, x].min(axis=1) < 160).sum()) for x in range(118, 216)]
        po = " ".join(f"{118+i}:{c}" for i, c in enumerate(co) if c)
        pr = " ".join(f"{118+i}:{c}" for i, c in enumerate(cr) if c)
        print(f"   orig  : {po}")
        print(f"   render: {pr}")

    print("-- original row1 glyph map x192..228 y364..392 (expect '1' then x_11)")
    glyphmap(o, 192, 364, 228, 392)
    print("-- render row1 glyph map x172..228 y364..392 (expect first col x_11)")
    glyphmap(r, 172, 364, 228, 392)

    print()
    print("=" * 74)
    print("FINDING 2 — y-vector third-row cell (row3 band)")
    print("=" * 74)
    print("original y-vector row3 x98..140 y426..452:")
    glyphmap(o, 98, 426, 140, 452)
    print("render y-vector row3 x98..140 y426..452:")
    glyphmap(r, 98, 426, 140, 452)
    print("original matrix ELLIPSIS glyph (reference 3-dot style) "
          "x310..352 y432..452:")
    glyphmap(o, 310, 432, 352, 452)

    print()
    print("=" * 74)
    print("FINDING 3 — red 'b' emphasis")
    print("=" * 74)
    def redmask(a):
        return (a[..., 0] > 120) & (a[..., 1] < 90) & (a[..., 2] < 90)
    ro, rr = redmask(o), redmask(r)
    for label, x0, y0, x1, y1 in (("b-box x450..525 y345..375", 450, 345, 525, 375),
                                  ("b-box wide x420..540 y340..380", 420, 340, 540, 380)):
        print(f"  {label}: orig={int(ro[y0:y1, x0:x1].sum())} "
              f"render={int(rr[y0:y1, x0:x1].sum())}")
    ys, xs = np.nonzero(rr)
    print(f"  render red ink overall: n={int(rr.sum())} "
          f"bbox={(int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None}")
    ys, xs = np.nonzero(ro)
    print(f"  orig   red ink overall: n={int(ro.sum())} "
          f"bbox={(int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None}")


if __name__ == "__main__":
    main()
