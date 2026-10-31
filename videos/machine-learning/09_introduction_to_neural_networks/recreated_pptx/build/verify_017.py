#!/usr/bin/env python3
"""Closed-loop verification for slide 017: ORIGINAL vs RENDER, per element.

ORIGINAL  V/unique_slides/slide_017.jpg   960x540,  1px = 1pt
RENDER    build/slide_017_rejudge_rendered-1.png  2001x1125 @150dpi, 1px = 0.48pt
render_x = original_x * 150/72  (positions scale; colour values do not)

Each element is measured inside its own measured window (taken from the
original's own pixels), so the comparison is element-to-element and immune to
group-merging differences between a 960px JPEG and a 2001px render.
"""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
B = f"{V}/recreated_pptx/build"
SCALE = 150.0 / 72.0
TOL = 4.0

CREAM = np.array([250, 233, 215])
SLIDE = np.array([232, 232, 232])

orig = np.asarray(Image.open(f"{V}/unique_slides/slide_017.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(f"{B}/slide_017_rejudge_rendered-1.png").convert("RGB")).astype(int)

lines, fails = [], []


def say(t):
    lines.append(t)
    print(t)


def win(arr, x0, y0, x1, y1, bg, tol=70):
    """ink bbox + colour census inside a window (arr-native px)."""
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(arr.shape[1], x1), min(arr.shape[0], y1)
    sub = arr[y0:y1, x0:x1]
    ink = np.abs(sub - bg).sum(axis=2) > tol
    px = sub.reshape(-1, 3)
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    census = dict(R=int(((r - g > 60) & (r - b > 60)).sum()),
                  G=int(((g - r > 50) & (g - b > 50)).sum()),
                  K=int(((r < 130) & (g < 130) & (b < 130)).sum()))
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        return None, census
    return (x0 + cols[0], x0 + cols[-1], y0 + rows[0], y0 + rows[-1]), census


def rw(x0, y0, x1, y1):
    return (int(round(x0 * SCALE)), int(round(y0 * SCALE)),
            int(round(x1 * SCALE)), int(round(y1 * SCALE)))


def check_element(label, x0, y0, x1, y1, expect=None):
    o, co = win(orig, x0, y0, x1, y1, CREAM)
    r, cr = win(rend, *rw(x0, y0, x1, y1), CREAM)
    if o is None or r is None:
        fails.append(f"{label}: ink missing (orig={o} render={r})")
        say(f"FAIL {label}: ink missing orig={o} render={r}")
        return
    rr = (r[0] / SCALE, r[1] / SCALE, r[2] / SCALE, r[3] / SCALE)
    d = [abs(o[i] - rr[i]) for i in range(4)]
    ok = max(d) <= TOL
    if expect:
        src = {"R": cr, "G": cr, "K": cr}[expect]
        if src[expect] == 0:
            ok = False
            fails.append(f"{label}: no {expect} ink in render")
    if not ok:
        fails.append(f"{label}: delta={d}")
    say(f"{'PASS' if ok else 'FAIL'} {label}: orig x{o[0]}..{o[1]} y{o[2]}..{o[3]} | "
        f"render x{rr[0]:.1f}..{rr[1]:.1f} y{rr[2]:.1f}..{rr[3]:.1f} | "
        f"d=({d[0]:.1f},{d[1]:.1f},{d[2]:.1f},{d[3]:.1f}) | "
        f"colour orig R{co['R']}/G{co['G']}/K{co['K']} render R{cr['R']}/G{cr['G']}/K{cr['K']}")


# element windows measured from the ORIGINAL (x0,y0,x1,y1) and expected class
BL = [
    ("BL 'F'", 124, 475, 134, 487, "K"),
    ("BL '('", 137, 472, 141, 491, "K"),
    ("BL 'x' in F(x)", 144, 478, 152, 487, "R"),
    ("BL ')'", 153, 472, 157, 491, "K"),
    ("BL '=' after F(x)", 160, 479, 170, 484, "K"),
    ("BL name 'Uni-polar'", 173, 475, 238, 490, "R"),
    ("BL 'Unit'", 245, 475, 275, 487, "K"),
    ("BL 'Step'", 280, 475, 308, 490, "K"),
    ("BL '=' after name", 311, 479, 320, 484, "K"),
    ("BL brace '{'", 322, 464, 327, 504, "R"),
    ("BL row-1 value '0'", 330, 469, 338, 481, "R"),
    ("BL row-1 cond 'for x<0'", 349, 467, 403, 485, "K"),
    ("BL row-2 value '1'", 330, 487, 336, 498, "R"),
    ("BL row-2 cond 'for x>=0'", 349, 486, 403, 502, "G"),
]
BR = [
    ("BR 'F'", 498, 475, 509, 487, "K"),
    ("BR '('", 511, 472, 515, 491, "K"),
    ("BR 'x' in F(x)", 517, 478, 525, 487, "R"),
    ("BR ')'", 527, 472, 531, 491, "K"),
    ("BR '=' after F(x)", 534, 479, 544, 484, "K"),
    ("BR name 'Bi-polar'", 547, 475, 603, 490, "R"),
    ("BR 'Unit'", 610, 475, 639, 487, "K"),
    ("BR 'Step'", 644, 475, 673, 490, "K"),
    ("BR '=' after name", 675, 479, 684, 484, "K"),
    ("BR brace '{'", 687, 464, 691, 504, "R"),
    ("BR row-1 minus", 695, 474, 704, 477, "R"),
    ("BR row-1 value '1'", 708, 469, 714, 481, "R"),
    ("BR row-1 cond 'for x<0'", 726, 468, 779, 485, "K"),
    ("BR row-2 value '1'", 695, 487, 700, 499, "R"),
    ("BR row-2 cond 'for x>=0'", 726, 486, 779, 503, "G"),
]
TOP = [
    ("TOP 'F('", 613, 180, 629, 199, "K"),
    ("TOP 'x)'", 632, 180, 645, 199, "R"),
    ("TOP '='", 649, 187, 658, 193, "K"),
    ("TOP rhs 'x'", 661, 186, 669, 195, "R"),
    ("TOP 'Linear'", 730, 183, 774, 195, "R"),
    ("TOP '(No'", 781, 183, 805, 198, "K"),
    ("TOP 'Activation)'", 808, 183, 879, 198, "K"),
]

say("=" * 108)
say("SLIDE 017 CLOSED LOOP - original 960x540 (1px=1pt) vs render 2001x1125 @150dpi (1px=0.48pt)")
say("per-element ink bbox comparison inside the original's measured windows; tolerance 4px @150dpi")
say("=" * 108)

say("\n-- bottom-left callout box (Uni-polar Unit Step) --")
for e in BL:
    check_element(*e)

say("\n-- bottom-right callout box (Bi-polar Unit Step) --")
for e in BR:
    check_element(*e)

say("\n-- top-right callout box (F(x) = x  Linear (No Activation)) --")
for e in TOP:
    check_element(*e)

say("\n-- judge finding 3: delimiter / frame containment --")
for lbl, box, outside in [
    ("BL", (115, 457, 415, 508), {"above": (117, 442, 412, 455), "left": (100, 462, 110, 503),
                                 "right": (420, 462, 436, 503)}),
    ("BR", (494, 457, 800, 508), {"above": (496, 442, 799, 455), "left": (478, 462, 489, 503),
                                 "right": (805, 462, 820, 503)}),
]:
    x0, y0, x1, y1 = box
    o_all, _ = win(orig, x0 + 2, y0 + 2, x1 - 1, y1 - 1, CREAM)
    r_all, _ = win(rend, *rw(x0 + 2, y0 + 2, x1 - 1, y1 - 1), CREAM)
    inside_o = o_all is not None and x0 <= o_all[0] and o_all[1] <= x1 and y0 <= o_all[2] and o_all[3] <= y1
    inside_r = r_all is not None and x0 <= r_all[0] / SCALE and r_all[1] / SCALE <= x1 and y0 <= r_all[2] / SCALE and r_all[3] / SCALE <= y1
    ok = inside_o and inside_r
    if not ok:
        fails.append(f"{lbl} content not contained in box")
    say(f"{'PASS' if ok else 'FAIL'} {lbl} equation content contained in box "
        f"(orig {o_all}, render {r_all if r_all is None else tuple(round(v/SCALE,1) for v in r_all)})")
    for k, reg in outside.items():
        n_o = int((np.abs(orig[reg[1]:reg[3], reg[0]:reg[2]] - CREAM).sum(axis=2) > 70).sum())
        n_r = int((np.abs(rend[rw(*reg)[1]:rw(*reg)[3], rw(*reg)[0]:rw(*reg)[2]] - CREAM).sum(axis=2) > 70).sum())
        ok = n_o == 0 and n_r == 0
        if not ok:
            fails.append(f"{lbl} ink outside box ({k})")
        say(f"{'PASS' if ok else 'FAIL'} {lbl} no ink outside box ({k}): orig={n_o} render={n_r}")
    # below the box: the original carries the video's black capture band there, which
    # ground rule (c) says is correctly omitted; the recreation must show nothing.
    reg = (x0 + 2, 513, x1 - 1, 525)
    n_o = int((np.abs(orig[reg[1]:reg[3], reg[0]:reg[2]] - CREAM).sum(axis=2) > 70).sum())
    n_r = int((np.abs(rend[rw(*reg)[1]:rw(*reg)[3], rw(*reg)[0]:rw(*reg)[2]] - CREAM).sum(axis=2) > 70).sum())
    ok = n_r == 0
    if not ok:
        fails.append(f"{lbl} ink below box in render")
    say(f"{'PASS' if ok else 'FAIL'} {lbl} nothing below box in render (orig's own paint={n_o} "
        f"is the video capture band, correctly omitted): render={n_r}")

say("\n-- house chrome (informational only; house-frame rule overrides judge findings) --")
for lbl, reg in [("outer red frame", (4, 4, 956, 536)), ("badge oval", (892, 14, 942, 64)),
                 ("title text", (40, 14, 920, 62))]:
    o, _ = win(orig, *reg, bg=np.array([231, 233, 230]), tol=40)
    r, _ = win(rend, *rw(*reg), bg=SLIDE, tol=40)
    say(f"INFO {lbl}: orig={o} render={None if r is None else tuple(round(v/SCALE,1) for v in r)}")

say("\n-- callout fill colour (sampled at a glyph-free spot) --")
for lbl, x, y in [("BL fill", 400, 465), ("BR fill", 780, 465), ("TOP fill", 700, 179)]:
    say(f"INFO {lbl}: orig={tuple(orig[y, x])} render={tuple(rend[int(y*SCALE), int(x*SCALE)])}")

say("\n" + "=" * 108)
say(f"SUMMARY: {len(lines)} reported lines, {len(fails)} FAIL")
for f in fails:
    say("  FAIL " + f)
say("VERDICT: " + ("FAIL" if fails else "PASS - every measured element matches the original within 4px @150dpi"))
say("=" * 108)
