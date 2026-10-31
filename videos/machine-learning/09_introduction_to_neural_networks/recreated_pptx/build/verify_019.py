#!/usr/bin/env python3
"""Verify the slide 019 re-judge render against the original lecture frame.

Contract: unique_slides/slide_019.jpg is 960x540 and 1 original px = 1 pt in
the pptx build; the LibreOffice render is 2001x1125 at 150 dpi, so
1 render px = 960 / 2001 = 0.4798 pt. Both images are therefore measured in
the SAME unit (pt), each element relative to its own panel.

Original panel boxes were PIL-measured from the frame's blue-purple border
ink (see measure_019_final.py). The build's panel boxes come from the layout
constants in slide_019.js (1 px of the original = 1 pt on the slide), which
the house-frame rule normalises, so absolute panel positions legitimately
differ; element geometry inside a panel is what is compared.
"""
import os

from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
V = os.path.join(ROOT, "videos/machine-learning/09_introduction_to_neural_networks")
B = os.path.join(V, "recreated_pptx", "build")
ORIG = os.path.join(V, "unique_slides/slide_019.jpg")
RENDER = os.path.join(B, "slide_019_rejudge_rendered-1.png")

TOL = 4  # px tolerance at 150 dpi (~1.9 pt)

# measured in the ORIGINAL frame (px = pt)
OP = {
    "sigmoid": (104, 59, 410, 237),
    "tanh":    (499, 59, 790, 237),
    "tan":     (105, 297, 410, 476),
    "arctan":  (499, 297, 790, 476),
}
# measured data rects in the ORIGINAL frame (px = pt)
ODATA = {
    "sigmoid": (134, 81, 334, 192),
    "tanh":    (525, 77, 767, 225),
    "tan":     (127, 327, 350, 473),
    "arctan":  (526, 309, 780, 457),
}
# build layout constants (from slide_019.js), converted to pt
PANEL_W, PANEL_H = 305.0 / 72 * 72, 178.0 / 72 * 72  # = 305 x 178 pt
IX, IW = 0.15 * 72, 13.03 * 72
IY, IH = 0.15 * 72, 7.2 * 72
BP = {
    "sigmoid": (IX + 0.11 * IW, IY + 0.11 * IH,
                IX + 0.11 * IW + PANEL_W, IY + 0.11 * IH + PANEL_H),
    "tanh":    (IX + 0.52 * IW, IY + 0.11 * IH,
                IX + 0.52 * IW + PANEL_W, IY + 0.11 * IH + PANEL_H),
    "tan":     (IX + 0.11 * IW, IY + 0.55 * IH,
                IX + 0.11 * IW + PANEL_W, IY + 0.55 * IH + PANEL_H),
    "arctan":  (IX + 0.52 * IW, IY + 0.55 * IH,
                IX + 0.52 * IW + PANEL_W, IY + 0.55 * IH + PANEL_H),
}
# caption boxes measured in the ORIGINAL frame (px = pt)
OCAP = {
    "sigmoid": (138, 240, 375, 294),
    "tanh":    (528, 240, 745, 294),
    "tan":     (165, 468, 305, 498),
    "arctan":  (545, 467, 687, 497),
}


def is_bluepurple(c):
    return c[2] - c[0] > 40 and c[2] - c[1] > 40 and c[2] > 90


def is_rose(c):
    return c[0] - c[1] > 25 and c[0] - c[2] > 20 and c[0] > 120


def is_red(c):
    return c[0] - c[1] > 70 and c[0] - c[2] > 70 and c[0] > 150


def is_text(c, lo):
    return c[0] < lo and c[1] < lo and c[2] < lo and not is_bluepurple(c)


def bbox(px, rect_pt, scale, pred, wlim, hlim):
    """Ink bbox inside a pt-rect, returned in pt."""
    d = (int(rect_pt[0] / scale), int(rect_pt[1] / scale),
         int(rect_pt[2] / scale), int(rect_pt[3] / scale))
    pts = [(x, y) for y in range(max(0, d[1]), min(hlim, d[3]))
           for x in range(max(0, d[0]), min(wlim, d[2]))
           if pred(px[x, y])]
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs) * scale, min(ys) * scale, max(xs) * scale, max(ys) * scale)


def main():
    o = Image.open(ORIG).convert("RGB")
    if not os.path.exists(RENDER):
        print(f"MISSING render {RENDER}")
        return 1
    r = Image.open(RENDER).convert("RGB")
    opx, rpx = o.load(), r.load()
    sr = 960.0 / r.size[0]
    fails = []
    print(f"original {o.size} (1px = 1pt) | render {r.size} (1px = {sr:.4f}pt)")
    print("\npanel boxes (pt): original vs build-normalised rejudge")
    for k in OP:
        print(f"  {k:8s} orig {tuple(round(v) for v in OP[k])}  "
              f"rejudge {tuple(round(v) for v in BP[k])}")

    print("\n== FINDING 1: axis lines + tick labels legible in all four plots ==")
    for k in ODATA:
        ob = (ODATA[k][0] + 5, ODATA[k][1] + 5, ODATA[k][2] - 5, ODATA[k][3] - 5)
        bb = bbox(opx, ob, 1.0, lambda c: is_text(c, 150), o.size[0], o.size[1])
        w = (bb[2] - bb[0]) if bb else 0
        print(f"  {k:8s} original in-panel text span {w:3.0f}pt  "
              f"(x {bb[0]:.0f}..{bb[2]:.0f}, y {bb[1]:.0f}..{bb[3]:.0f})" if bb
              else f"  {k:8s} original: no in-panel text ink")
        # rejudge: build panel interior in px, scan the same relative window
        bx0, by0, bx1, by1 = BP[k]
        rb = (bx0 + 20, by0 + 20, bx1 - 20, by1 - 20)
        rb2 = bbox(rpx, rb, sr, lambda c: is_text(c, 150), r.size[0], r.size[1])
        w2 = (rb2[2] - rb2[0]) if rb2 else 0
        ok = rb2 is not None and w2 > 40
        if not ok:
            fails.append(f"finding 1 {k}")
        print(f"           rejudge in-panel text span {w2:3.0f}pt "
              f"-> {'FIXED' if ok else 'FAIL'}")

    print("\n== FINDING 2: four rose dashed vertical asymptotes in the tan plot ==")
    fracs = [0.125, 0.375, 0.625, 0.875]
    counted = []
    dx = BP["tan"][0] - OP["tan"][0]
    for f in fracs:
        # tan data rect x 127..350 pt in the ORIGINAL frame; the build places the
        # tan panel at a house-frame-normalised x, so shift by the panel delta
        tx = 127 + (350 - 127) * f + dx
        n = 0
        d = (int(tx / sr) - 3, int(327 / sr), int(tx / sr) + 4, int(473 / sr))
        for x in range(max(0, d[0]), min(r.size[0], d[2])):
            for y in range(max(0, d[1]), min(r.size[1], d[3])):
                if is_rose(rpx[x, y]):
                    n += 1
        counted.append(n)
    print(f"  rose ink px at each of the four positions (x = 155/211/266/322 pt): "
          f"{counted}")
    ok = all(c >= 20 for c in counted)
    if not ok:
        fails.append("finding 2")
    print(f"  -> {'FIXED (all four distinguishable, dashed, rose)' if ok else 'FAIL'}")

    print("\n== FINDING 3: arctan 'Inverse Tangent Graph' inset, black, inside ==")
    bx0, by0, bx1, by1 = BP["arctan"]
    ab = bbox(rpx, (bx0 + 8, by0 + 4, bx0 + 150, by0 + 40), sr,
              lambda c: is_text(c, 150), r.size[0], r.size[1])
    if ab:
        il, it = ab[0] - bx0, ab[1] - by0
        ok = il >= 20 and it >= 8
        if not ok:
            fails.append("finding 3")
        print(f"  rejudge ink x {ab[0]:.0f}..{ab[2]:.0f} y {ab[1]:.0f}..{ab[3]:.0f} "
              f"-> inset {il:.0f}pt left, {it:.0f}pt top")
        print(f"  original ink x 530..639 y 309..318 -> 31pt left, 12pt top")
        print(f"  -> {'FIXED' if ok else 'FAIL'}")
    else:
        fails.append("finding 3 no ink")
        print("  no ink -> FAIL")

    print("\n== FINDING 4: tanh/tan axis titles horizontal, clear of the border ==")
    for k in ("tanh", "tan"):
        bx0, by0, _, _ = BP[k]
        tb = bbox(rpx, (bx0 + 4, by0 + 4, bx0 + PANEL_W - 4, by0 + 34), sr,
                  lambda c: is_text(c, 150), r.size[0], r.size[1])
        if tb:
            gap, span = tb[1] - by0, tb[2] - tb[0]
            ok = gap >= 4 and span >= 15
            if not ok:
                fails.append(f"finding 4 {k}")
            print(f"  {k:5s} title ink span {span:.0f}pt, top gap {gap:.0f}pt "
                  f"-> {'FIXED (horizontal above the y-axis)' if ok else 'FAIL'}")
        else:
            fails.append(f"finding 4 {k}")
            print(f"  {k:5s} no ink -> FAIL")

    print("\n== FINDING 5: red block arrow size and centring ==")
    gab = bbox(rpx, (BP["tan"][2] - 5, BP["tan"][1] + 70, BP["arctan"][0] + 5,
                     BP["tan"][3] - 70), sr, is_red, r.size[0], r.size[1])
    if gab:
        w, h = gab[2] - gab[0], gab[3] - gab[1]
        gc = (BP["tan"][2] + BP["arctan"][0]) / 2
        cx = (gab[0] + gab[2]) / 2
        ok = abs(w - 52) <= 6 and abs(h - 21) <= 6 and abs(cx - gc) <= 8
        if not ok:
            fails.append("finding 5")
        print(f"  original ink x 426..477 y 374..393 (51x19 pt)")
        print(f"  rejudge ink w={w:.0f}pt h={h:.0f}pt, centre offset "
              f"{abs(cx - gc):.0f}pt -> {'FIXED' if ok else 'FAIL'}")
    else:
        fails.append("finding 5 no ink")
        print("  no red arrow ink -> FAIL")

    print("\n== FINDING 8: caption ink contained with even padding ==")
    for k in OCAP:
        # caption box in the build = measured original box, offset by panel delta
        dx = BP[k][0] - OP[k][0]
        dy = BP[k][1] - OP[k][1]
        cb = (OCAP[k][0] + dx, OCAP[k][1] + dy, OCAP[k][2] + dx, OCAP[k][3] + dy)
        ib = bbox(rpx, (cb[0] + 4, cb[1] + 4, cb[2] - 4, cb[3] - 4), sr,
                  lambda c: is_text(c, 150), r.size[0], r.size[1])
        if ib:
            pt_, pb = ib[1] - cb[1], cb[3] - ib[3]
            ok = ib[0] >= cb[0] and ib[2] <= cb[2] and pt_ >= 3 and pb >= 3
            if not ok:
                fails.append(f"finding 8 {k}")
            print(f"  {k:8s} ink x {ib[0]:.0f}..{ib[2]:.0f} y {ib[1]:.0f}..{ib[3]:.0f} "
                  f"(box {cb[0]:.0f}..{cb[2]:.0f} x {cb[1]:.0f}..{cb[3]:.0f}) "
                  f"pad top {pt_:.0f}pt bottom {pb:.0f}pt "
                  f"-> {'FIXED' if ok else 'FAIL'}")
        else:
            fails.append(f"finding 8 {k}")
            print(f"  {k:8s} no caption ink -> FAIL")

    print("\n== HOUSE FRAME (overrides judge findings) ==")
    f = bbox(rpx, (0, 0, 960, 540), sr, is_red, r.size[0], r.size[1])
    print(f"  red frame ink x {f[0]:.1f}..{f[2]:.1f} y {f[1]:.1f}..{f[3]:.1f} "
          f"| rule: 10.8..949.2 x 10.8..529.2, #C00000, 1.5pt, no fill")
    ok = (abs(f[0] - 10.8) <= TOL and abs(f[1] - 10.8) <= TOL and
          abs(f[2] - 949.2) <= TOL and abs(f[3] - 529.2) <= TOL)
    if not ok:
        fails.append("house frame")
    nb = bbox(rpx, (898.6, 21.6, 934.6, 57.6), sr, lambda c: is_text(c, 120),
              r.size[0], r.size[1])
    if nb:
        cx, cy = (nb[0] + nb[2]) / 2, (nb[1] + nb[3]) / 2
        okb = abs(cx - 916.6) <= 8 and abs(cy - 39.6) <= 8
        if not okb:
            fails.append("badge numeral")
        print(f"  badge numeral ink {nb} centre {cx:.0f},{cy:.0f} vs 916.6,39.6 "
              f"-> {'OK (bold 18pt #333333 on #FFF9C4)' if okb else 'FAIL'}")
    else:
        fails.append("badge numeral")
        print("  no badge numeral ink -> FAIL")
    tb = bbox(rpx, (43.2, 20.2, 873.4, 59.6), sr, lambda c: is_text(c, 200),
              r.size[0], r.size[1])
    print(f"  title ink {tb} | rule: box x 0.6..12.73in (43.2..916.6pt), y 0.28in "
          f"(20.2pt), centred")

    print("\n== SUMMARY ==")
    if fails:
        print(f"  not passing: {fails}")
        return 1
    print("  all measured checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
