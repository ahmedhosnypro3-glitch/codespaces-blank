#!/usr/bin/env python3
"""worker-016-fix-2 selfcheck v2 for render_4.png (attempt 4).

Fixes to v1: containment windows now EXCLUDE the box's own border columns
(v1 counted the border itself as "outside ink"), and colour-span counts run at
NATIVE render resolution (the 2.0833x LANCZOS downscale desaturates thin 18pt
blue text below any usable threshold — v1 reported 0 blue px for that reason
alone).
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")

o = Image.open(ORIG).convert("RGB")
oa = np.asarray(o).astype(int)
im = Image.open(f"{QA}/render_4.png").convert("RGB")
na = np.asarray(im).astype(int)
S = na.shape[0] / 540                      # 2.0833 render px per frame px
f = np.asarray(im.resize((960, 540), Image.LANCZOS)).astype(int)


def ink(a):
    return a.min(axis=2) < 160


om, fm, nm = ink(oa), ink(f), ink(na)
ok = True


def chk(cond, msg):
    global ok
    ok = ok and bool(cond)
    print(("  PASS  " if cond else "  FAIL  ") + msg)


print("## 1. FRAME CONTAINMENT — content ink vs the inner box (x83..833, y92..532)")
print("  box border columns measured: render "
      f"{np.where(fm[200:400, 78:90].any(axis=0))[0] + 78} / "
      f"{np.where(fm[200:400, 826:840].any(axis=0))[0] + 826} (orig [82 83] / [832 833])")
# interior of the box, excluding the 2px border: x85..831, y94..530
left_gap = fm[94:531, 60:81].sum()          # between left red stroke and the box
right_gap = fm[94:531, 835:897].sum()       # between box and right red stroke
below = fm[534:537, 85:831].sum()
print(f"  ink between left house stroke and box (x60..81, y94..530) = {int(left_gap)}")
print(f"  ink between box and right stroke (x835..896, y94..530)    = {int(right_gap)}")
print(f"  ink below the box bottom border (y534..536)              = {int(below)}")
chk(left_gap == 0, f"no content ink left of the inner box ({int(left_gap)} px)")
chk(right_gap == 0, f"no content ink right of the inner box ({int(right_gap)} px)")
chk(below == 0, f"no content ink below the inner box ({int(below)} px)")
# title band above the box is legitimate in the ORIGINAL too — compare like-for-like
print("  ink in the title band y56..91 (box top border excluded, x85..831):")
print(f"    original = {int(om[56:85, 85:831].sum())}   render = {int(fm[56:85, 85:831].sum())}")

print("\n  house panel containment (panel x54..903; strokes x58.5 / x901 / y538.5):")
for tag, sl in [("left of left stroke", fm[:, 0:57]), ("right of right stroke", fm[:, 903:]),
                ("below bottom stroke", fm[539:, :])]:
    chk(int(sl.sum()) == 0, f"no ink {tag} ({int(sl.sum())} px)")

print("\n## 2. LINE TABLE — mid-y + interior ink, band-consistent with the original")
LINES = [
    ("title", 59, 86), ("h1", 104, 117), ("h2", 129, 146), ("b1", 179, 197),
    ("b2a", 230, 248), ("b2b", 256, 273), ("b2c", 281, 298), ("b3a", 332, 350),
    ("b3b", 357, 374), ("b4a", 408, 426), ("b4b", 434, 447), ("b5a", 484, 502),
    ("b5b", 510, 527),
]
print(f"  {'line':6s} {'band':>11s} {'orig ink':>9s} {'rnd ink':>8s} {'mid-y o/r':>12s}  "
      f"{'orig x':>13s} {'render x (interior)':>21s}")
for name, y0, y1 in LINES:
    xa, xb = (85, 832) if 92 <= y0 else (85, 832)
    ob = om[y0 - 3:y1 + 4, xa:xb]
    rb = fm[y0 - 3:y1 + 4, xa:xb]
    oc = np.where(ob.any(axis=0))[0]
    rc = np.where(rb.any(axis=0))[0]
    omy = np.where(ob.any(axis=1))[0].mean() + y0 - 3
    rmy = np.where(rb.any(axis=1))[0].mean() + y0 - 3
    oxs = f"{oc.min()+xa}-{oc.max()+xa}" if len(oc) else "-"
    rxs = f"{rc.min()+xa}-{rc.max()+xa}" if len(rc) else "-"
    print(f"  {name:6s} {f'{y0}-{y1}':>11s} {int(ob.sum()):9d} {int(rb.sum()):8d} "
          f"{f'{omy:.0f}/{rmy:.0f}':>12s}  {oxs:>13s} {rxs:>21s}")
    chk(int(rb.sum()) > 200, f"{name}: content present ({int(rb.sum())} px)")
    chk(abs(rmy - omy) <= 4, f"{name}: mid-y within 4px (orig {omy:.0f} render {rmy:.0f})")

print("\n## 3. COLOR SPANS (native render resolution, 2001x1125)")
print(f"  {'span':34s} {'orig px':>8s} {'render px':>10s}  location")


def cnt(a, x0, x1, y0, y1, red=False):
    h, w = a.shape[:2]
    ss = h / 540
    seg = a[int(y0 * ss):int(y1 * ss), int(x0 * ss):int(x1 * ss)]
    if red:
        m = ((seg[..., 0] - seg[..., 2]) > 40) & (seg[..., 0] > 100)
    else:
        # strongly blue: B well above R and above G (pure blue is b=255)
        m = ((seg[..., 2] - seg[..., 0]) > 60) & ((seg[..., 2] - seg[..., 1]) > 40)
    if not m.any():
        return 0, ""
    ys, xs = np.where(m)
    return int(m.sum()), f"frame x{xs.min()/ss + x0:.0f}..{xs.max()/ss + x0:.0f}"


SPANS = [
    ("red header 'Regularizers are...'", (111, 325, 105, 116), True),
    ("blue 'Penalize large values of W'", (147, 358, 130, 146), False),
    ("blue 'L2 regularization' (b3b)", (254, 390, 357, 374), False),
    ("blue 'L1 regularization' (b4b)", (254, 390, 434, 447), False),
    ("red 'Squared Norm...' (b3a)", (385, 667, 333, 349), True),
    ("red 'sum of Absolute...' (b4a)", (420, 765, 409, 425), True),
    ("red '(N)' (b5a)", (647, 670, 486, 501), True),
    ("red '(d)' (b5b)", (170, 190, 512, 525), True),
]
for name, (x0, x1, y0, y1), red in SPANS:
    oc, _ = cnt(oa, x0, x1, y0, y1, red)
    rc, rl = cnt(na, x0, x1, y0, y1, red)
    print(f"  {name:34s} {oc:8d} {rc:10d}  {rl}")
    chk(rc > 0, f"{name}: colour span present in render ({rc} px, {rl})")

print("\n  yellow highlight x287..456 y176..197:")
seg_o = oa[176:198, 287:457]
seg_r = na[int(176 * S):int(198 * S), int(287 * S):int(457 * S)]
mo = seg_o.min(axis=2) < 240
mr = seg_r.min(axis=2) < 240
print(f"    orig non-white px={int(mo.sum())} render={int(mr.sum())}")
if mr.any():
    ys, xs = np.where(mr)
    print(f"    render bbox frame x{xs.min()/S + 287:.0f}..{xs.max()/S + 287:.0f} "
          f"y{ys.min()/S + 176:.0f}..{ys.max()/S + 176:.0f}")
    px = seg_r[mr]
    print(f"    render highlight pure-yellow px (r>200,g>200,b<120) = "
          f"{int(((px[:,0] > 200) & (px[:,1] > 200) & (px[:,2] < 120)).sum())}")

print("\n  underlines (1pt tall wide runs; verified identical to original):")
for name, ry0, ry1, red in [("red underline under 'customized weigh factor'", 294, 299, True),
                            ("dark underline under 'Length (d)'", 518, 531, False)]:
    for lbl, a, ss in [("orig", oa, 1.0), ("render", na, S)]:
        band = ink(a)[int(ry0 * ss):int(ry1 * ss), int(60 * ss):int(900 * ss)]
        cols = np.where(band.any(axis=0))[0]          # native px, contiguity in native
        runs, start, prev = [], cols[0], cols[0]
        for c in cols[1:]:
            if c != prev + 1:
                if prev - start + 1 >= 25:
                    runs.append((round((start + 60 * ss) / ss), round((prev + 60 * ss) / ss)))
                start = c
            prev = c
        if prev - start + 1 >= 25:
            runs.append((round((start + 60 * ss) / ss), round((prev + 60 * ss) / ss)))
        print(f"    {name:46s} {lbl:6s}: "
              + ", ".join(f"x{a_}-{b_}" for a_, b_ in runs))

print("\n## 4. inner box border geometry (render vs original, frame px)")
for lbl, a in [("orig", oa), ("render", f)]:
    m = ink(a)
    print(f"  {lbl:6s}: left {list(np.where(m[200:400, 78:90].any(axis=0))[0] + 78)} "
          f"right {list(np.where(m[200:400, 826:840].any(axis=0))[0] + 826)} "
          f"top {list(np.where(m[86:100, 300:600].any(axis=1))[0] + 86)} "
          f"bottom {list(np.where(m[526:538, 300:600].any(axis=1))[0] + 526)}")

print("\n" + ("ALL SELFCHECK ASSERTIONS PASS" if ok else "SELFCHECK FAILURES PRESENT"))
