#!/usr/bin/env python3
"""Render the ten slide_023 equations as 2D composites.
Colors/structure measured from unique_slides/slide_023.jpg (pixel probes)."""
from eqcomp_023 import seg, save, write_manifest, DPI, _paste
import numpy as np
from PIL import Image

BLACK, RED, GREEN, BLUE = "#000000", "#CC0000", "#1E8C1E", "#3333CC"
FS = 14
PITCH = int(round(FS * DPI / 72 * 1.40))
ASC = int(round(FS * DPI / 72 * 0.78))
DESC = int(round(FS * DPI / 72 * 0.26))


def M(s, color=BLACK):
    return seg("math", s, color, FS)


def trim(img):
    a = np.asarray(img)
    ink = a[:, :, 3] > 8
    r = np.where(ink.any(axis=1))[0]
    c = np.where(ink.any(axis=0))[0]
    return Image.fromarray(a[r[0]:r[-1] + 1, c[0]:c[-1] + 1])


def _canvas(w, h, top_pad=8):
    return np.zeros((h + 2 * top_pad, w, 4), dtype=np.uint8), top_pad


def _place(cv, s, x, y):
    _paste(cv, s["img"], x, y)


def line(name, parts, gap=10, pad=12):
    segs = [M(*p) if isinstance(p, tuple) else p for p in parts]
    bs = max(s["base"] for s in segs)
    hs = max(s["img"].height - s["base"] for s in segs)
    w = sum(s["img"].width for s in segs) + gap * (len(segs) - 1) + 2 * pad
    cv, p0 = _canvas(w, bs + hs + 2)
    x = pad
    for s in segs:
        _place(cv, s, x, p0 + (bs - s["base"]))
        x += s["img"].width + gap
    save(trim(Image.fromarray(cv)), name)


def frac_parts(num, den):
    """num/den = (latex,color) tuples; stacked fraction, returns seg-like dict."""
    n = M(*num)
    dn = [M(*p) if isinstance(p, tuple) else p for p in den]
    dw = sum(s["img"].width for s in dn) + 10 * (len(dn) - 1)
    uw, w = n["img"].width, max(n["img"].width, dw)
    bar_h = max(3, int(round(FS * DPI / 72 * 0.045)))
    gap_up, gap_dn = 14, 10
    h = n["img"].height + gap_up + bar_h + gap_dn + max(s["img"].height for s in dn)
    cv, p0 = _canvas(w, h)
    ny = p0
    nx = (w - uw) // 2
    _place(cv, n, nx, ny)
    by = ny + n["img"].height + gap_up
    cv[by:by + bar_h, :, 0:3] = 0
    cv[by:by + bar_h, :, 3] = 255
    dy = by + bar_h + gap_dn
    x = (w - dw) // 2
    dbase = 0
    for s in dn:
        dbase = max(dbase, s["base"])
    for s in dn:
        _place(cv, s, x, dy + (dbase - s["base"]))
        x += s["img"].width + 10
    return {"img": trim(Image.fromarray(cv)), "base": dy + dbase}


def comb(name, parts, gap=12, pad=12):
    """Horizontal composition of segs (incl. frac_parts results)."""
    bs = max(s["base"] for s in parts)
    hs = max(s["img"].height - s["base"] for s in parts)
    w = sum(s["img"].width for s in parts) + gap * (len(parts) - 1) + 2 * pad
    cv, p0 = _canvas(w, bs + hs + 2)
    x = pad
    for s in parts:
        _place(cv, s, x, p0 + (bs - s["base"]))
        x += s["img"].width + gap
    save(trim(Image.fromarray(cv)), name)


def piecewise(name, label, c1, c2):
    br = M(r"\left\{\phantom{\frac{0}{0}}\right.", RED)
    th = ASC + PITCH + DESC
    sc = th / br["img"].height
    bw = int(round(br["img"].width * sc))
    br = {"img": br["img"].resize((bw, th), Image.LANCZOS),
          "base": int(round(br["base"] * sc))}
    lab = [M(*t) if isinstance(t, tuple) else t for t in label]
    v1, k1 = M(*c1[:2]), M(c1[2], c1[3])
    v2, k2 = M(*c2[:2]), M(c2[2], c2[3])
    lab_w = sum(s["img"].width for s in lab) + 10 * (len(lab) - 1)
    br_x = lab_w + 12
    v_x = br_x + bw + 12
    k1_x = v_x + v1["img"].width + 10
    k2_x = v_x + v2["img"].width + 10
    w = max(k1_x + k1["img"].width, k2_x + k2["img"].width) + 12
    cv, p0 = _canvas(w, ASC + PITCH + DESC)
    b1, b2 = p0 + ASC, p0 + ASC + PITCH
    x = 0
    for s in lab:
        _place(cv, s, x, p0 + (ASC - s["base"]))
        x += s["img"].width + 10
    _place(cv, br, br_x, p0)
    for s, bx, by in ((v1, v_x, b1), (k1, k1_x, b1), (v2, v_x, b2), (k2, k2_x, b2)):
        _place(cv, s, bx, by - s["base"])
    save(trim(Image.fromarray(cv)), name)


LBL = r"\mathbf{\mathrm{%s}}"
COND = r"\mathit{for}\ "
BN = r"f(x)="
BD = r"f'(x)="

piecewise("eq023_L1",
          [(BN, BLACK), (LBL % "Uni\\text{-}polar", RED),
           (r"\ \mathrm{Unit\ Step}=", BLACK)],
          (r"0", RED, COND + r"x<0", BLACK),
          (r"1", GREEN, COND + r"x\geq 0", GREEN))

piecewise("eq023_L2",
          [(BN, BLACK), (LBL % "Bi\\text{-}polar", RED),
           (r"\ \mathrm{Unit\ Step}=", BLACK)],
          (r"-1", RED, COND + r"x<0", BLACK),
          (r"1", GREEN, COND + r"x\geq 0", GREEN))

piecewise("eq023_R1",
          [(BD, BLACK)],
          (r"0", RED, COND + r"x\neq 0", BLACK),
          (r"?", RED, COND + r"x=0", GREEN))

comb("eq023_L3", [M(BN, BLACK), M(LBL % "Sigmoid", RED), M(r"(x)=", BLACK),
                  frac_parts((r"1", BLACK), [(r"1+e^{-x}", BLACK)])])

comb("eq023_R3", [M(r"f'(x)=f(x)", BLACK), M(r"(1-f(x))", BLUE)])

comb("eq023_L4", [M(BN, BLACK), M(LBL % "\\tanh", RED), M(r"(x)=", BLACK),
                  frac_parts((r"\sinh x", BLACK), [(r"\cosh x", BLACK)])])

comb("eq023_R4", [M(r"f'(x)=1-f(x)", BLACK), M(r"^{2}", BLUE)])
line("eq023_L5", [(BN, BLACK), M(r"\tan^{-1}(x)", BLACK)])
comb("eq023_R5", [M(BD, BLACK), frac_parts((r"1", BLACK), [(r"x^{2}+1", RED)])])

write_manifest("eq023_manifest.json")
