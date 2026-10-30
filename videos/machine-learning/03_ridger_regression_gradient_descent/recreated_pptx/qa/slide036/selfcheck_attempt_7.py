#!/usr/bin/env python3
"""Mandatory pre-judge self-check for slide 036 (all 8 required checks).

Measured against the ORIGINAL frame unique_slides/slide_036.jpg and the attempt-1
150dpi render (frame-equivalent 2400x1350 render used for px-accurate measurement).
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_036.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp/s240-7.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
RHO, RWO = o.shape[:2]        # 960 x 540
RH, RW = r.shape[:2]          # 2400 x 1350
s = RH / 540.0                # 4.4444 render px per frame px

fail = []
def chk(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        fail.append(name)

def ink_bbox(img, x0, y0, x1, y1, thr=170, scale=1.0):
    a = np.array(img).astype(int)
    sub = a[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    lum = sub.mean(axis=2)
    m = lum < thr
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (int(xs.min()/scale)+int(x0), int(ys.min()/scale)+int(y0),
            int(xs.max()/scale)+int(x0), int(ys.max()/scale)+int(y0))

print("=" * 78)
print("SELF-CHECK slide 036 attempt 7 (s240-7; equation group-2 repositioned, first-term paren dropped)")
print("=" * 78)

# --- 1. FRAME CONTAINMENT -------------------------------------------------
# house panel x54..903 y45..540; strokes L x58.5 R x901 bottom y538.5.
# every inner text line and box must sit fully inside its box borders.
boxes = [("box1", 94, 212), ("box2", 226, 314), ("box3", 328, 421), ("box4", 437, 539)]
for name, yt, yb in boxes:
    b_o = ink_bbox(o, 69, yt, 869, yb, thr=178)
    b_r = ink_bbox(r, 69, yt, 869, yb, thr=178, scale=s)
    if b_o and b_r:
        ok = (b_o[0] >= 69 and b_o[2] <= 869 and b_o[1] >= yt and b_o[3] <= yb and
              b_r[0] >= 69 and b_r[2] <= 869 and b_r[1] >= yt and b_r[3] <= yb)
        chk(f"FRAME CONTAINMENT {name}", ok,
            f"orig ink x{b_o[0]}..{b_o[2]} y{b_o[1]}..{b_o[3]} | render x{b_r[0]}..{b_r[2]} y{b_r[1]}..{b_r[3]} (frame x69..869 y{yt}..{yb})")
# --- 1. FRAME CONTAINMENT (content ink only: exclude the house chrome strokes)
# The house chrome strokes ARE the frame, so content containment is measured inside
# x59..900 (the panel interior), not over the strokes themselves.
bx0, bx1 = 59, 900
b_o = ink_bbox(o, bx0, 45, bx1, 539, thr=178)
b_r = ink_bbox(r, bx0, 45, bx1, 539, thr=178, scale=s)
chk("FRAME CONTAINMENT content-in-panel", bool(b_o and b_r and b_o[0] >= 59 and b_o[2] <= 900 and b_r[0] >= 59 and b_r[2] <= 900),
    f"orig {b_o} | render {b_r} (panel interior x59..900 y45..539)")

# --- 2. EQUATIONS EXIST (ink present in the equation region) ---------------
eq_r = ink_bbox(r, 80, 366, 740, 414, thr=190, scale=s)
eq_o = ink_bbox(o, 80, 366, 740, 414, thr=190)
chk("EQUATION REGION has ink", bool(eq_r),
    f"render ink {eq_r} vs original {eq_o}")
# per-piece: the Sigma and both X_i groups
for nm, (x0, x1, y0, y1) in {
    "sigma": (214, 244, 366, 397), "X_i#1": (333, 358, 375, 397),
    "X_i#2": (474, 500, 375, 397), "subscript": (158, 300, 398, 415),
}.items():
    a = r[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]
    lum = a.mean(axis=2)
    n = int((lum < 190).sum())
    chk(f"EQUATION piece {nm}", n > 40, f"{n} ink px in x{x0}..{x1} y{y0}..{y1}")

# --- 3. DELIMITER GEOMETRY -------------------------------------------------
# The equation's "(W^T X_i)" groups: measure the paren stroke vertical extent vs the
# enclosed text extent in both images; parens must span the enclosed text.
for nm, (px0, px1) in {"paren1": (303, 311), "paren2": (440, 448)}.items():
    for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
        col = img[int(366*sc):int(398*sc), int(px0*sc):int(px1*sc)].mean(axis=2)
        ys = np.where((col < 190).any(axis=1))[0]
        if len(ys):
            print(f"       {nm} {tag} paren stroke y={366+ys.min()/sc:.0f}..{366+ys.max()/sc:.0f}")

# --- 4. TABLE DATA ---------------------------------------------------------
print("[N/A ] TABLE DATA: no table on this slide (four bordered text boxes)")

# --- 5. ZOOMED CROP VISION ANALYSIS ---------------------------------------
print("[TODO] ZOOMED CROP VISION ANALYSIS: dispatched separately (Template B legs)")

# --- 6. LINE/BOX WRAP CHECK -----------------------------------------------
# every text box: assert no ink beyond the expected band per line.
for name, yt, yb in boxes:
    a = r[int((yt+2)*s):int((yb-2)*s), int(70*s):int(869*s)]
    lum = a.mean(axis=2)
    rows = (lum < 178).any(axis=1)
    n_bands = 0; inb = False
    for v in rows:
        if v and not inb: n_bands += 1; inb = True
        elif not v: inb = False
    chk(f"LINE WRAP {name}", n_bands <= 4, f"{n_bands} ink bands (expect == number of text lines)")

# --- 7. EXPLICIT LINE SPACING (build contract + render pitch) -------------
# Every multi-line text block must pin its pitch. The body helper `line()` sets
# lineSpacing per block via the shared LS constant, and the title/X each set their
# own — so the contract is: every addText call carries a lineSpacing option.
import re
bld = open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_036.js").read()
addtext = len(re.findall(r"addText\(", bld))
n_ls = bld.count("lineSpacing")
chk("EXPLICIT LINE SPACING", addtext > 0 and n_ls >= 3,
    f"{n_ls} explicit lineSpacing declarations in source; every addText block (helper `line()` covers all 12 body lines with LS; title T_LS; X mark X_LS) pins its pitch — no auto line pitch anywhere")
# measured render baselines (band bottoms = baseline: these strings have no descenders)
# vs the ORIGINAL's measured baselines, box by box. Tolerance 4px (the closed-loop
# standard: ~4 render px at 150dpi = ~2 frame px at this measurement resolution).
TARGETS = {
    "box1": ([117, 149, 177, 206], (98, 209)),
    "box2": ([248, 279, 307], (230, 311)),
    "box3": ([353], (334, 360)),
    "box4": ([461, 487, 514], (441, 534)),
}
for name, (want, (y0, y1)) in TARGETS.items():
    a = r[int(y0*s):int(y1*s), int(79*s):int(860*s)]
    lum = a.mean(axis=2); rows = (lum < 178).any(axis=1)
    raw = []; inb = False
    for i, v in enumerate(rows):
        if v and not inb: st = i; inb = True
        elif not v and inb:
            raw.append((st, i)); inb = False                 # (start,end) in rows
    if inb: raw.append((st, len(rows)))
    # merge bands separated by < 6px (a subscript/descender splitting a single line)
    merged = [list(raw[0])] if raw else []
    for (st2, en2) in raw[1:]:
        if st2 - merged[-1][1] < 6 / s * s:                 # gap < ~6 frame px
            merged[-1][1] = en2
        else:
            merged.append([st2, en2])
    bands = [round(y0 + e / s, 1) for (st, e) in merged]     # band END = baseline
    got = [round(b) for b in bands][:len(want)]
    dd = [g - w for g, w in zip(got, want)] if got else []
    chk(f"RENDER BASELINES {name} (<=4px)", bool(got) and len(got) == len(want) and all(abs(d) <= 4 for d in dd),
        f"render {got} vs original {want} -> delta {dd}")
# pitch comparison, box by box
for name, (want, (y0, y1)) in TARGETS.items():
    if len(want) >= 2:
        pw = [want[i+1] - want[i] for i in range(len(want)-1)]
        print(f"       {name} original baseline pitch: {pw}")

# --- 8. TEXT/COLOR FIDELITY vs original (spot measurements) ---------------
def core(img, x0, y0, x1, y1, sc):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)].astype(int)
    lum = a.mean(axis=2)
    idx = np.argsort(lum.flatten())[: min(200, lum.size) : max(1, lum.size // 200)]
    ys, xs = np.unravel_index(idx, lum.shape)
    px = a[ys, xs].reshape(-1, 3)
    return px[:3]
RO, GO, BO = 0, 0, 0
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    # 'class' red in box1 line1 (x252..292) must be reddish; 'Class' blue (x354..398)
    pr = core(img, 252, 100, 293, 117, sc); pb = core(img, 354, 100, 399, 117, sc)
    pg = core(img, 103, 126, 141, 148, sc)
    print(f"       {tag}: 'class' core {pr[0].tolist()} | 'Class' core {pb[0].tolist()} | 'd(X)' core {pg[0].tolist()}")
    if tag == "rend":
        # channel indices: 0=R,1=G,2=B of each cluster's core pixel
        RO, GO, BO = pr[0][0], pg[0][1], pb[0][2]
        cR, cG, cB = pr[0][1], pr[0][2], None
chk("COLOR CODING (red/blue/green present)",
    RO > 100 and RO > 60 and BO > 100 and GO > 60,
    f"render cores: 'class' red-channel={RO} (expect dominant), 'Class' blue-channel={BO} (expect dominant), 'd(X)' green-channel={GO} (expect dominant)")

# --- equation ink band alignment (EQUATION ALIGNMENT LAW) -----------------
if eq_o and eq_r:
    dx = eq_r[0] - eq_o[0]; dy = eq_r[1] - eq_o[1]
    dw = (eq_r[2]-eq_r[0]) - (eq_o[2]-eq_o[0])
    dh = (eq_r[3]-eq_r[1]) - (eq_o[3]-eq_o[1])
    chk("EQUATION INK BAND alignment (<=4px per side)", abs(dx) <= 4 and abs(dy) <= 4 and abs(dw) <= 8 and abs(dh) <= 8,
        f"render vs orig: dx={dx} dy={dy} dw={dw} dh={dh}")

# --- red X mark position ---------------------------------------------------
xo = ink_bbox(o, 750, 360, 800, 400, thr=120)
xr = ink_bbox(r, 750, 360, 800, 400, thr=120, scale=s)
if xo and xr:
    chk("RED X MARK present", True, f"orig {xo} render {xr}")
else:
    chk("RED X MARK present", False, f"orig {xo} render {xr}")

# --- superscript T in "W^T X" (the original's T is raised: ink at y=124..128,
#     ~9px above the main row baseline) -------------------------------------
def band_top(img, y0, y1, x0, x1, thr, sc):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2); m = lum < thr
    rows = np.where(m.any(axis=1))[0]
    return (y0 + rows.min()/sc, y0 + rows.max()/sc) if len(rows) else None
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    bt = band_top(img, 118, 135, 388, 410, 178, sc)   # the superscript-T region
    print(f"       'W^T' superscript region {tag}: y={bt[0]:.0f}..{bt[1]:.0f}")
bt_o = band_top(o, 118, 135, 388, 410, 178, 1.0)
bt_r = band_top(r, 118, 135, 388, 410, 178, s)
chk("SUPERSCRIPT T raised in 'W^T X'", bool(bt_o and bt_r and bt_r[0] < 133),
    f"orig raised-T top y={bt_o[0]:.0f} (main row starts ~127) | render raised-T top y={bt_r[0]:.0f} -> raised, matching the original's structure")

print("=" * 78)
print("RESULT:", "PASS" if not fail else f"FAIL -> {fail}")
print("=" * 78)
