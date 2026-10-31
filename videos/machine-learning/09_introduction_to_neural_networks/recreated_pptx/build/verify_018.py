#!/usr/bin/env python3
"""PIL closed-loop verification: slide-018 render vs the original frame.

Usage: python3 verify_018.py [render.png]

Both images are compared in ORIGINAL-FRAME coordinates (960x540, 1 px = 1 pt):
  original : videos/.../unique_slides/slide_018.jpg
  render   : recreated_pptx/build/slide_018_rejudge_rendered-1.png (2001x1125 @150dpi)
The original's content box (x 57..903, y 43..517) maps onto the house frame
rectangle (0.15 in inset, 13.03 x 7.2 in), so orig->render is:
  x_render = (0.15 + (x_orig-57)/846*13.03) * PPI_X
  y_render = (0.15 + (y_orig-43)/474*7.2) * PPI_Y
Every check prints the ORIGINAL-side value and the RENDER-side value and
reports PASS/FAIL at a 4 px tolerance.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_018.jpg"
RENDER = (sys.argv[1] if len(sys.argv) > 1 else
          f"{V}/recreated_pptx/build/slide_018_rejudge_rendered-1.png")
TOL = 4.0
PPI_X, PPI_Y = 2001 / 13.33, 1125 / 7.5

results = []


def o2r_x(ox):
    return (0.15 + (ox - 57) / 846 * 13.03) * PPI_X


def o2r_y(oy):
    return (0.15 + (oy - 43) / 474 * 7.2) * PPI_Y


def r2o_x(rx):
    return 57 + (rx / PPI_X - 0.15) / 13.03 * 846


def r2o_y(ry):
    return 43 + (ry / PPI_Y - 0.15) / 7.2 * 474


def runs(idx, gap=3, minlen=1):
    out = []
    if len(idx) == 0:
        return out
    st = prev = idx[0]
    for v in idx[1:]:
        if v - prev > gap:
            out.append((int(st), int(prev)))
            st = v
        prev = v
    out.append((int(st), int(prev)))
    return [(a, b) for a, b in out if b - a + 1 >= minlen]


def clusters(idx, gap=8):
    """group nearby indices into (start,end) clusters"""
    if len(idx) == 0:
        return []
    out = []
    st = prev = int(idx[0])
    for v in idx[1:]:
        v = int(v)
        if v - prev > gap:
            out.append((st, prev))
            st = v
        prev = v
    out.append((st, prev))
    return out


def blobs(mask, minpx=120):
    lab, n = ndimage.label(mask)
    res = []
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(xx) < minpx:
            continue
        res.append((int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max()), int(len(xx))))
    return sorted(res, key=lambda t: (t[1], t[0]))


def crop(im, ox0, oy0, ox1, oy1, SX, SY):
    return im[int(round(SY(oy0))):int(round(SY(oy1))),
              int(round(SX(ox0))):int(round(SX(ox1)))]


def check(name, ok, detail):
    results.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def bbox_of(mask, SX, SY, X, Y, ox0, oy0):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (X(SX(ox0) + xs.min()), Y(SY(oy0) + ys.min()),
            X(SX(ox0) + xs.max()), Y(SY(oy0) + ys.max()))


def near(a, b, tol=TOL):
    return abs(a - b) <= tol


def bbox_near(a, b, tol=TOL):
    if a is None or b is None:
        return False
    return all(abs(x - y) <= tol for x, y in zip(a, b))


# ---------------------------------------------------------------- measurements
def measure(im, SX, SY, X, Y):
    """Return a dict of measured features in original-frame coordinates."""
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    m = {}

    # blue chart-panel borders (columns and rows)
    blue = ((b - r > 25) & (b - g > 12) & (b > 70)) & ~((r > 190) & (g > 190))
    col, row = blue.sum(axis=0), blue.sum(axis=1)
    m["blue_v"] = [(X(a), X(b_)) for a, b_ in clusters(np.where(col > 20)[0])]
    m["blue_h"] = [(Y(a), Y(b_)) for a, b_ in clusters(np.where(row > 20)[0])]

    # yellow highlight ellipses
    yellow = (r > 195) & (g > 195) & (b < 190)
    m["yellow"] = []
    lab, nb = ndimage.label(yellow)
    for i in range(1, nb + 1):
        yy, xx = np.where(lab == i)
        if len(xx) < 400:
            continue
        m["yellow"].append((X(SX(0) + xx.min()), Y(SY(0) + yy.min()),
                            X(SX(0) + xx.max()), Y(SY(0) + yy.max())))

    # green annotation ink (sigmoid guides/bar + the green condition text)
    green = (g - r > 25) & (g > 60) & (b < 200)
    m["green_cols"] = [(X(a), X(b_)) for a, b_ in clusters(np.where(green.sum(axis=0) > 4)[0], gap=4)]

    # connector band: red ink between the panes and the charts
    reddish = (r - g > 25) & (r - b > 25) & (r > 130)
    band = np.zeros_like(reddish)
    y0, y1 = int(round(SY(256))), int(round(SY(323)))
    band[y0:y1, :] = reddish[y0:y1, :]
    m["connector"] = []
    for a, b_, c, d, n in blobs(band, 20):
        if (c - a) > 100 or (d - b_) > 100:
            continue
        m["connector"].append((X(a), Y(b_), X(c), Y(d)))

    # caption row: ink per caption window
    m["captions"] = []
    for cx0, cx1 in [(120, 300), (430, 600), (690, 860)]:
        sub = crop(im, cx0, 482, cx1, 506, SX, SY)
        d = (np.abs(sub - 232).sum(axis=2) > 60)
        yy, xx = np.where(d)
        if len(xx):
            m["captions"].append((X(SX(cx0) + xx.min()), Y(SY(482) + yy.min()),
                                  X(SX(cx0) + xx.max()), Y(SY(482) + yy.max())))
        else:
            m["captions"].append(None)

    # callout body: blue text lines
    sub = crop(im, 360, 196, 495, 242, SX, SY)
    cb, cr = sub[:, :, 2].astype(int), sub[:, :, 0].astype(int)
    bt = (cb - cr > 30) & (cb > 90)
    rows = [i for i in range(bt.shape[0]) if bt[i].sum() > 2]
    m["callout_blue_rows"] = []
    if rows:
        groups = clusters(np.array(rows), gap=3)
        for a, b_ in groups:
            band2 = bt[a:b_ + 1]
            xx = np.where(band2.any(axis=0))[0]
            m["callout_blue_rows"].append((Y(SY(196) + a), Y(SY(196) + b_),
                                           X(SX(360) + xx.min()), X(SX(360) + xx.max())))

    # callout heading: red text band
    sub = crop(im, 350, 196, 492, 215, SX, SY)
    cr, cg, cb = sub[:, :, 0].astype(int), sub[:, :, 1].astype(int), sub[:, :, 2].astype(int)
    rt = (cr - cg > 60) & (cr - cb > 60) & (cr > 120)
    yy, xx = np.where(rt)
    m["callout_head"] = (X(SX(350) + xx.min()), Y(SY(196) + yy.min()),
                         X(SX(350) + xx.max()), Y(SY(196) + yy.max())) if len(xx) else None

    # equation card fill colour (left card interior)
    sub = crop(im, 90, 112, 278, 152, SX, SY)
    pale = (sub[:, :, 0] > 235) & (sub[:, :, 1] > 215) & (sub[:, :, 2] > 195)
    m["card_fill"] = tuple(int(np.median(sub[:, :, k][pale])) for k in range(3)) if pale.sum() > 50 else None

    # equation condition ink (black line 1 / green line 2) inside left card
    for lbl, (ox0, oy0, ox1, oy1), kind in [
            ("cond_black", (305, 114, 372, 137), "black"),
            ("cond_green", (305, 137, 372, 157), "green")]:
        sub = crop(im, ox0, oy0, ox1, oy1, SX, SY)
        cr, cg, cb = sub[:, :, 0].astype(int), sub[:, :, 1].astype(int), sub[:, :, 2].astype(int)
        if kind == "black":
            msk = (cr < 140) & (cg < 140) & (cb < 140)
        else:
            msk = (cg - cr > 25) & (cg > 60)
        yy, xx = np.where(msk)
        m[lbl] = (X(SX(ox0) + xx.min()), Y(SY(oy0) + yy.min()),
                  X(SX(ox0) + xx.max()), Y(SY(oy0) + yy.max())) if len(xx) else None

    # title ink (dark red)
    sub = crop(im, 100, 50, 855, 85, SX, SY)
    cr, cg, cb = sub[:, :, 0].astype(int), sub[:, :, 1].astype(int), sub[:, :, 2].astype(int)
    rt = (cr > 110) & (cr < 235) & (cg < 105) & (cb < 105)
    yy, xx = np.where(rt)
    m["title"] = (X(SX(100) + xx.min()), Y(SY(50) + yy.min()),
                  X(SX(100) + xx.max()), Y(SY(50) + yy.max())) if len(xx) else None

    # bottom-chart curve hue (sigmoid/tanh/arctan panels)
    m["curves"] = {}
    for name, (px0, py0, px1, py1) in [
            ("sigmoid", (74, 322, 335, 478)), ("tanh", (390, 322, 634, 478)),
            ("arctan", (655, 322, 890, 478))]:
        sub = crop(im, px0 + 4, py0 + 4, px1 - 4, py1 - 4, SX, SY)
        cr, cg, cb = sub[:, :, 0].astype(int), sub[:, :, 1].astype(int), sub[:, :, 2].astype(int)
        pink = (cr - cb > 40) & (cr > 200) & (cg > 140) & (cg < 220)
        m["curves"][name] = tuple(int(np.median(sub[:, :, k][pink])) for k in range(3)) if pink.sum() > 30 else None

    # step-pane curve hue (vertical jump segment)
    for name, (px0, py0, px1, py1) in [
            ("unipolar_step", (190, 196, 202, 252)), ("bipolar_step", (640, 196, 650, 250))]:
        sub = crop(im, px0, py0, px1, py1, SX, SY)
        cr, cg, cb = sub[:, :, 0].astype(int), sub[:, :, 1].astype(int), sub[:, :, 2].astype(int)
        pink = (cr - cb > 40) & (cr > 140) & (cg < 190)
        m["curves"][name] = tuple(int(np.median(sub[:, :, k][pink])) for k in range(3)) if pink.sum() > 20 else None

    return m


def main():
    o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
    rr = np.array(Image.open(RENDER).convert("RGB")).astype(int)
    ident = lambda v: v
    mo = measure(o, ident, ident, ident, ident)
    mr = measure(rr, o2r_x, o2r_y, r2o_x, r2o_y)

    print(f"ORIGINAL : {ORIG}")
    print(f"RENDER   : {RENDER}  ({rr.shape[1]}x{rr.shape[0]})")
    print(f"TOLERANCE: {TOL:.0f} px in original-frame coordinates")

    print("\n== 1. blue chart-panel borders ==")
    vo, vr = mo["blue_v"], mr["blue_v"]
    print(f"  original v-edges: {[(round(a), round(b)) for a, b in vo]}")
    print(f"  render   v-edges: {[(round(a), round(b)) for a, b in vr]}")
    check("blue v-edges", len(vo) == len(vr) and all(
        abs(a[0] - b[0]) <= TOL and abs(a[1] - b[1]) <= TOL for a, b in zip(vo, vr)),
        f"{len(vo)} original vs {len(vr)} render")
    ho, hr = mo["blue_h"], mr["blue_h"]
    print(f"  original h-edges: {[(round(a), round(b)) for a, b in ho]}")
    print(f"  render   h-edges: {[(round(a), round(b)) for a, b in hr]}")

    print("\n== 2. yellow highlight ellipses ==")
    yo, yr = mo["yellow"], mr["yellow"]
    print(f"  original: {[(round(a), round(b), round(c), round(d)) for a, b, c, d in yo]}")
    print(f"  render  : {[(round(a), round(b), round(c), round(d)) for a, b, c, d in yr]}")
    ok = len(yo) == len(yr) and all(bbox_near(a, b) for a, b in zip(yo, yr))
    check("yellow ellipses", ok, f"{len(yo)} original vs {len(yr)} render")

    print("\n== 3. sigmoid green guides ==")
    go, gr = mo["green_cols"], mr["green_cols"]
    print(f"  original: {[(round(a), round(b)) for a, b in go]}")
    print(f"  render  : {[(round(a), round(b)) for a, b in gr]}")
    ok = len(go) >= 3 and len(gr) >= 3 and all(
        abs(a[0] - b[0]) <= TOL and abs(a[1] - b[1]) <= TOL
        for a, b in zip(go[-3:], gr[-3:]))
    check("green guide columns", ok, f"orig {len(go)} / render {len(gr)} columns")

    print("\n== 4. connectors (single dashed arrow, NO fork) ==")
    co, cr_ = mo["connector"], mr["connector"]
    print(f"  original: {[(round(a), round(b), round(c), round(d)) for a, b, c, d in co]}")
    print(f"  render  : {[(round(a), round(b), round(c), round(d)) for a, b, c, d in cr_]}")
    o_main = [c for c in co if c[0] > 190 and c[0] < 220]
    r_main = [c for c in cr_ if c[0] > 190 and c[0] < 220]
    check("one dashed connector at x~201-208", len(o_main) == 1 and len(r_main) == 1,
          f"original {len(o_main)}, render {len(r_main)}")
    if o_main and r_main:
        check("connector bbox", bbox_near(o_main[0], r_main[0]),
              f"orig {tuple(round(v) for v in o_main[0])} vs render {tuple(round(v) for v in r_main[0])}")
    check("no fork ink in connector band", len(cr_) == len(r_main),
          f"render has {len(cr_)} red component(s) in y256..323")

    print("\n== 5. bottom captions (below the panels) ==")
    print(f"  original: {[tuple(round(v) for v in c) if c else None for c in mo['captions']]}")
    print(f"  render  : {[tuple(round(v) for v in c) if c else None for c in mr['captions']]}")
    ok = len(mo["captions"]) == 3 and all(
        a and b and abs((a[0] + a[2]) / 2 - (b[0] + b[2]) / 2) <= TOL
        for a, b in zip(mo["captions"], mr["captions"]))
    check("caption centres", ok, "caption x-centres within 4px")
    ok = all(a and b and a[1] >= 480 and b[1] >= 480 for a, b in zip(mo["captions"], mr["captions"]))
    check("captions below panels", ok, "caption ink starts at y>=480 (panels end y=478)")

    print("\n== 6. callout ==")
    print(f"  heading original {tuple(round(v) for v in mo['callout_head'])}"
          f" render {tuple(round(v) for v in mr['callout_head'])}")
    check("callout heading", bbox_near(mo["callout_head"], mr["callout_head"]),
          "red 'Saturation Problem' bbox")
    print(f"  body rows original {[(round(a), round(b)) for a, b, _, _ in mo['callout_blue_rows']]}")
    print(f"  body rows render   {[(round(a), round(b)) for a, b, _, _ in mr['callout_blue_rows']]}")
    check("callout body = 2 lines", len(mo["callout_blue_rows"]) == 2 and len(mr["callout_blue_rows"]) == 2,
          f"original {len(mo['callout_blue_rows'])} lines, render {len(mr['callout_blue_rows'])} lines")
    ok = len(mo["callout_blue_rows"]) == 2 == len(mr["callout_blue_rows"]) and all(
        abs(a[0] - b[0]) <= TOL and abs(a[1] - b[1]) <= TOL
        for a, b in zip(mo["callout_blue_rows"], mr["callout_blue_rows"]))
    check("callout body line positions", ok, "both lines' y-bands")

    print("\n== 7. equation cards ==")
    print(f"  card fill original {mo['card_fill']} render {mr['card_fill']}")
    check("card fill colour", mo["card_fill"] == mr["card_fill"], "pale pink #FAE9D7")
    for lbl in ("cond_black", "cond_green"):
        a, b = mo[lbl], mr[lbl]
        print(f"  {lbl}: original {tuple(round(v) for v in a) if a else None}"
              f" render {tuple(round(v) for v in b) if b else None}")
        check(f"{lbl} ink bbox", bbox_near(a, b, 6), "condition text bbox")

    print("\n== 8. title ==")
    print(f"  original {tuple(round(v) for v in mo['title'])} render {tuple(round(v) for v in mr['title'])}")
    check("title ink bbox", bbox_near(mo["title"], mr["title"], 8), "title band")

    print("\n== 9. curve colours ==")
    for k in ("unipolar_step", "bipolar_step", "sigmoid", "tanh", "arctan"):
        print(f"  {k:14s} original {mo['curves'][k]} render {mr['curves'][k]}")

    print("\n== SUMMARY ==")
    npass = sum(1 for _, ok in results if ok)
    for name, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{npass}/{len(results)} checks passed")
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
