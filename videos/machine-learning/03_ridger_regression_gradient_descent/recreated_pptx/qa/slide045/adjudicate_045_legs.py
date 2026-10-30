#!/usr/bin/env python3
"""Slide 045 PIL-first adjudication helper (legs-on run).

Given a judge finding (region + claimed defect), measure BOTH images at 960x540
slide space (1px = 1pt) so a FAIL/MINOR can be refuted with banked numbers before
any build change. Prints facts, never conclusions.

Usage: python3 adjudicate_045_legs.py <region-name>
Regions: badge, brackets, calcs, toppanel, augtable, redframe, containment, all
"""
import sys
from PIL import Image

NS = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide045"
ORIG = NS + "/unique_slides/slide_045.jpg"
RENDER = QA + "/render_1.png"

o = Image.open(ORIG).convert("RGB")
r = Image.open(RENDER).convert("RGB")
RO = o.load()
RR = r.load()
RW, RH = r.size
S = RH / 540.0   # 2.0833


def luma(p):
    return (p[0] * 299 + p[1] * 587 + p[2] * 114) // 1000


def is_red(p):
    return p[0] > 120 and p[1] < 90 and p[2] < 90


def is_yellow(p):
    return p[0] > 200 and p[1] > 200 and p[2] < 190


def is_purple(p):
    return p[0] > 70 and p[0] < 150 and p[1] < 110 and p[2] > 130


def ocrop(x0, y0, x1, y1):
    """Sample the original at native 960x540."""
    return [[RO[x, y] for y in range(y0, y1)] for x in range(x0, x1)]


def rcrop(x0, y0, x1, y1):
    """Sample the render at frame coords (mapped by scale)."""
    return [[RR[int(round(x * S)), int(round(y * S))] for y in range(y0, y1)]
            for x in range(x0, x1)]


def ink(px):
    return sum(1 for row in px for p in row if luma(p) < 128)


def report(name):
    print("=" * 66)
    print("REGION:", name)
    print("=" * 66)
    if name in ("all", "redframe"):
        # House chrome strokes — LEFT x58.5, RIGHT x901, BOTTOM y538.5, NO TOP
        for lbl, im, fn in (("ORIGINAL", RO, RO), ("RENDER", RR, RR)):
            ys = range(60, 540)
            top = [x for x in range(56, 63) for y in range(40, 60) if is_red(fn[x, y])]
            top2 = [x for x in range(897, 905) for y in range(40, 60) if is_red(fn[x, y])]
            tot = sum(1 for x in range(0, 960) for y in range(0, 540) if is_red(fn[x, y]))
            print("[%s] red px total=%d" % (lbl, tot))
            print("   top band y40..59 red px: left-edge=%d right-edge=%d (must be 0 outside x56..62/897..904)"
                  % (len(top), len(top2)))
    if name in ("all", "badge"):
        def badge_pts(fn, scale):
            pts = []
            if scale == 1.0:
                for x in range(840, 916):
                    for y in range(45, 105):
                        if is_yellow(fn[x, y]):
                            pts.append((x, y))
            else:
                for x in range(int(840 * scale), int(916 * scale)):
                    for y in range(int(45 * scale), int(105 * scale)):
                        if is_yellow(fn[x, y]):
                            pts.append((x, y))
            return pts
        po = badge_pts(RO, 1.0)
        pr = badge_pts(RR, S)
        for lbl, pts, scale in (("ORIGINAL", po, 1.0), ("RENDER", pr, S)):
            if pts:
                xsr = [p[0] for p in pts]; ysr = [p[1] for p in pts]
                cx = sum(xsr) / len(xsr); cy = sum(ysr) / len(ysr)
                w = (max(xsr) - min(xsr) + 1) / scale
                h = (max(ysr) - min(ysr) + 1) / scale
                print("[%s] badge yellow bbox x%d..%d y%d..%d n=%d centroid=(%.1f,%.1f)"
                      % (lbl, min(xsr), max(xsr), min(ysr), max(ysr), len(pts), cx, cy))
                print("   FRAME-px w=%.1f h=%.1f d~%.1f (target ~35 centered 876,73)"
                      % (w, h, (w + h) / 2))
            else:
                print("[%s] badge: no yellow px found" % lbl)
    for region, bx in (("calcs", (266, 131, 861, 536)),
                       ("toppanel", (60, 46, 727, 137)),
                       ("augtable", (62, 132, 254, 263))):
        if name in ("all", region):
            x0, y0, x1, y1 = bx
            op = ocrop(x0, y0, x1, y1)
            rp = rcrop(x0, y0, x1, y1)
            print("[%s] frame bbox x%d..%d y%d..%d (%dx%d)"
                  % (region.upper(), x0, x1, y0, y1, x1 - x0, y1 - y0))
            print("   ORIGINAL ink px=%d   RENDER ink px=%d" % (ink(op), ink(rp)))
            # frame containment: ink strictly outside the region
            print("   frame-px area=%d" % ((x1 - x0) * (y1 - y0)))


REGIONS = {"badge", "brackets", "calcs", "toppanel", "augtable", "redframe",
           "containment", "all"}
which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which not in REGIONS:
    print("usage: adjudicate_045_legs.py {%s}" % "|".join(sorted(REGIONS)))
    sys.exit(2)
report(which)
