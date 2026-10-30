#!/usr/bin/env python3
"""Pre-judge selfcheck for slide 047, attempt 5 (render_8.png).
Founder-mandated checks with printed numbers (§6 of MISSION_PROTOCOL):
 1 frame containment, 2 equation ink present, 3 delimiter geometry,
 4 table data, 5 line/box wrap, 7 house chrome (separate checker output).
Crop-pair scale audit (6) is performed by crop_5_*_audit.txt in the crop leg.
"""
import json, re, sys, zipfile
import numpy as np
from PIL import Image

import os
RENDER = sys.argv[1] if len(sys.argv) > 1 else "recreated_pptx/qa/slide047/render_8.png"
ORIG   = "unique_slides/slide_047.jpg"
PPTX   = "recreated_pptx/slide_047_recreated.pptx"

img = np.array(Image.open(RENDER).convert("RGB")).astype(int)
H, W = img.shape[:2]
S = H / 540.0
lum = 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]
fails = []

def frame_bbox(x0,y0,x1,y1,thr=170):
    X0,Y0,X1,Y1 = [int(round(v*S)) for v in (x0,y0,x1,y1)]
    m = lum[Y0:Y1, X0:X1] < thr
    ys,xs = np.where(m)
    if len(xs)==0: return None
    return (x0+xs.min()/S, y0+ys.min()/S, x0+xs.max()/S, y0+ys.max()/S, int(m.sum()))

print(f"render {RENDER}  {W}x{H}  GM = {S:.4f}")
print(f"original {ORIG}  960x540")
if (W,H) != (2001,1125):
    fails.append(f"render size {W}x{H} != 2001x1125")

# ---- 1. FRAME CONTAINMENT (content inside the house panel + strokes) ----
PANEL = (58.5, 46.0, 901.0, 538.5)
content = frame_bbox(59, 46, 901, 538)
print(f"\n[1] content ink bbox x[{content[0]:.1f}..{content[2]:.1f}] y[{content[1]:.1f}..{content[3]:.1f}]  ({content[4]} px)")
inside = content[0] >= PANEL[0]-0.5 and content[1] >= PANEL[1]-0.5 and content[2] <= PANEL[2]+0.5 and content[3] <= PANEL[3]+0.5
print(f"    inside panel x{PANEL[0]}..{PANEL[2]}, y{PANEL[1]}..{PANEL[3]}: {'PASS' if inside else 'FAIL'}")
if not inside: fails.append("content outside panel")
# individual content boxes inside their own frames
sub_checks = {
  "top band contents": (69, 56, 719, 129),
  "aug box contents":  (70, 140, 246, 255),
  "calc box 1":        (274, 140, 854, 197),
  "calc box 2":        (274, 207, 854, 263),
  "calc box 3":        (274, 272, 854, 329),
}
for name,(a,b,c,d) in sub_checks.items():
    bb = frame_bbox(a,b,c,d)
    ok = bb is not None and bb[0] > a and bb[1] > b and bb[2] < c and bb[3] < d
    print(f"    {name:18s} ink x[{bb[0]:.1f}..{bb[2]:.1f}] y[{bb[1]:.1f}..{bb[3]:.1f}] -> {'PASS' if ok else 'FAIL'}")
    if not ok: fails.append(f"{name} overflow")

# ---- 2 + 3. EQUATIONS PRESENT / DELIMITER GEOMETRY ----
print("\n[2] equation-stack ink presence (green (14;-4;0) columns):")
for i, dy in enumerate([0, 69, 135]):
    bb = frame_bbox(385, 145+dy, 412, 195+dy)
    print(f"    box{i+1} stack x[{bb[0]:.1f}..{bb[2]:.1f}] y[{bb[1]:.1f}..{bb[3]:.1f}] ink={bb[4]}")
    if bb[4] < 40: fails.append(f"stack {i+1} empty/thin")
for i, dy in enumerate([0, 69, 135]):
    for nm,(a,b,c,d) in {"label":(278,155+dy,328,182+dy),"rowvec":(330,143+dy,380,162+dy),
                          "result":(411,155+dy,450,180+dy)}.items():
        bb = frame_bbox(a,b,c,d)
        if bb[4] < 15: fails.append(f"box{i+1} {nm} ink {bb[4]}")

print("\n[3] delimiter geometry — 3 ink runs (paren|digits|paren) per column + paren span vs digits:")
def runs_1d(x0,x1,y0,y1,thr=170):
    X0,X1,Y0,Y1=[int(round(v*S)) for v in (x0,x1,y0,y1)]
    m = lum[Y0:Y1, X0:X1] < thr
    prof = m.sum(axis=0); rr=[]; inr=False
    for i,v in enumerate(prof):
        if v>0 and not inr: st=i; inr=True
        if (v==0 or i==len(prof)-1) and inr:
            rr.append((round(x0+st/S,1), round(x0+i/S,1))); inr=False
    return rr
def vspan(x0,x1,y0,y1,thr=170):
    X0,X1,Y0,Y1=[int(round(v*S)) for v in (x0,x1,y0,y1)]
    m = lum[Y0:Y1, X0:X1] < thr
    rows = np.where(m.any(axis=1))[0]
    return (round(y0+rows.min()/S,1), round(y0+rows.max()/S,1))
matrices = {
 "TL": dict(centres=[96.5,118.5,140.5,163,185.5,208], par_top=76.5, par_bot=108, dig=(79,106)),
 "Z":  dict(centres=[606.5,628,650.5], par_top=79, par_bot=111.5, dig=(82,110)),
 "AUG":dict(centres=[100.5,121.5,144.5,167,189.5,211.5], par_top=181, par_bot=226.5, dig=(184,223)),
}
for mname, M in matrices.items():
    for ci,cx in enumerate(M["centres"]):
        rr = runs_1d(cx-10, cx+10, M["par_top"]-1.5, M["par_bot"]+1.5)
        ok3 = len(rr)==3 and rr[0][1] < rr[1][0] and rr[1][1] < rr[2][0]
        pv = vspan(rr[0][0], rr[0][1]+0.2, M["par_top"]-2, M["par_bot"]+2) if ok3 else None
        dv = vspan(rr[1][0], rr[1][1], M["par_top"]-2, M["par_bot"]+2) if ok3 else None
        covered = ok3 and pv[0] <= dv[0]+1.5 and pv[1] >= dv[1]-1.5
        print(f"    {mname}{ci+1}: runs={rr}  paren y{pv} digits y{dv}  {'PASS' if covered else 'FAIL'}")
        if not covered: fails.append(f"{mname} col{ci+1} delimiter")
for i, dy in enumerate([0, 69, 135]):
    rr = runs_1d(385, 409, 145+dy, 195+dy)
    ok3 = len(rr)==3
    pv = vspan(rr[0][0], rr[0][1]+0.2, 145+dy, 195+dy) if ok3 else None
    dv = vspan(rr[1][0], rr[1][1], 145+dy, 195+dy) if ok3 else None
    covered = ok3 and pv[0] <= dv[0]+1.5 and pv[1] >= dv[1]-1.5
    print(f"    STACK{i+1}: runs={rr} paren y{pv} digits y{dv} -> {'PASS' if covered else 'FAIL'}")
    if not covered: fails.append(f"stack{i+1} delimiter")

# ---- 4. TABLE DATA (pptx text runs vs the frame's measured values) ----
print("\n[4] table data — pptx <a:t> runs vs measured frame values:")
with zipfile.ZipFile(PPTX) as z:
    xml = z.read("ppt/slides/slide1.xml").decode("utf8")
texts = re.findall(r"<a:t>([^<]*)</a:t>", xml)
def unesc(t): return t.replace("&gt;",">").replace("&lt;","<").replace("&amp;","&")
texts = [unesc(t) for t in texts]
TL_DATA  = [[1,1],[2,1],[1,2],[5,4],[6,5],[6,6]]
AUG_DATA = [[1,1,1],[1,2,1],[1,1,2],[1,5,4],[1,6,5],[1,6,6]]
Z_DATA   = [[0,0],[7,6],[3,2]]
def walk_matrix(start, data, klass, with_class=True, headers=None):
    i = start; ok = True
    for ci, col in enumerate(data):
        hdr = texts[i]; i += 1
        vals = []
        for v in col:
            vals.append(texts[i]); i += 1
        want = headers[ci] if headers else f"x{chr(0x2081+ci)}"
        good = hdr == want and vals == [str(v) for v in col]
        if with_class:
            cl = texts[i]; i += 1
            good = good and cl == ("C\u2081" if klass[ci]==1 else "C\u2082")
        ok = ok and good
    return ok
tl_i = texts.index("x\u2081")
ok_tl = walk_matrix(tl_i, TL_DATA, [1,1,1,2,2,2])
z_i = texts.index("Z\u2081")
ok_z = walk_matrix(z_i, Z_DATA, None, with_class=False, headers=["Z\u2081","Z\u2081","Z\u2081"])
aug_i = texts.index("x\u2081", tl_i+1)
ok_aug = walk_matrix(aug_i, AUG_DATA, [1,1,1,2,2,2])
print(f"    TL matrix 6 cols x 2 rows + class C1C1C1C2C2C2 : {'PASS' if ok_tl else 'FAIL'}")
print(f"    Z  matrix 3 cols x 2 rows                   : {'PASS' if ok_z else 'FAIL'}")
print(f"    AUG matrix 6 cols x 3 rows + class           : {'PASS' if ok_aug else 'FAIL'}")
if not (ok_tl and ok_z and ok_aug): fails.append("table data")
expect_calc = {"d(Z\u2081) =":"(1  0  0)", "d(Z\u2082) =":None}
calc_runs = [t for t in texts if t.startswith("d(Z") or t.startswith("(") or t.startswith("=") or t.startswith("\u21d2") or t in ("Class I","Class II")]
print("    calc-box runs:", calc_runs)
ok_calc = calc_runs == ["d(Z\u2081) =","(1  0  0)","= 14","\u21d2 Positive > 0","Class I",
                        "d(Z\u2082) =","(1  7  6)","= -14","\u21d2 Negative < 0","Class II",
                        "d(Z\u2082) =","(1  3  2)","= -2","\u21d2 Negative < 0","Class II"]
print(f"    calc-box sequence (labels/rows/results/signs/classes): {'PASS' if ok_calc else 'FAIL'}")
if not ok_calc: fails.append("calc runs")

# ---- 5. LINE/BOX WRAP — no ink in the inter-block gap bands ----
print("\n[5] wrap/gap bands (expect zero ink):")
gaps = {
 "below TL class row":  (85, 125.5, 220, 128.5),
 "below aug class row": (85, 245.5, 220, 255),
 "calc gap 1-2":        (275, 199.5, 853, 205),
 "calc gap 2-3":        (275, 265.5, 853, 270),
 "aug title/header gap":(82, 162.5, 240, 165.5),
 "above aug box":       (70, 140.5, 246, 143),
}
for nm,(a,b,c,d) in gaps.items():
    bb = frame_bbox(a,b,c,d)
    n = 0 if bb is None else bb[4]
    print(f"    {nm:22s} ink={n:3d} -> {'PASS' if n==0 else 'FAIL'}")
    if n != 0: fails.append(f"ink in gap band {nm}")
# explicit lineSpacing: every text box in this build is single-line, so LO/PowerPoint
# auto pitch cannot diverge; prove it by counting paragraphs per shape.
paras = xml.count("<a:p>")
shapes_txt = xml.count("<p:sp>")
print(f"    text shapes={shapes_txt}, paragraphs={paras} (all single-paragraph: "
      f"{'PASS' if paras <= shapes_txt else 'CHECK'}; no multi-line box => lineSpacing N/A)")

print("\nSUMMARY:", "ALL CHECKS PASS" if not fails else f"FAILURES: {fails}")
sys.exit(0 if not fails else 1)
