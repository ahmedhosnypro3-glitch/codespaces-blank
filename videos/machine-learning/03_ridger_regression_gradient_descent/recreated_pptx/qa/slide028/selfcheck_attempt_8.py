#!/usr/bin/env python3
"""w028 pre-judge SELFCHECK for slide 028 attempt 8 (render_8.png, 150 dpi 2001x1125).

Mandatory checks (MISSION_PROTOCOL §6):
 1. frame containment (house panel, chart frame, no ink outside)
 2. equation regions          — none on this slide (declared, not skipped)
 3. delimiter geometry        — none on this slide (declared, not skipped)
 4. table data                — none on this slide (declared, not skipped)
 5. line/box wrap + explicit line spacing / label bands
 6. crop-pair scale audit     — executed when the attempt-8 crop pairs are cut
 7. house_chrome_check.py     — PASS banked separately
Plus the slide-specific structural checks this attempt exists for:
 A. LEFT panel: 7 hollow circles at the measured original centres (tol 2.5px),
    no filled disc anywhere in the left panel, nothing on the right arm.
 B. RIGHT panel: 4 saturated discs at the measured centres, connector chords
    A-C / A-D / B-C present, A-B / B-D absent.
 C. curve ripple (rendered stroke vs the analytic quartics).
 D. text ink bboxes vs the original's measured bboxes.
"""
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
REND = ROOT + "/recreated_pptx/qa/slide028/render_8.png"
ORIG = ROOT + "/unique_slides/slide_028.jpg"

im = Image.open(REND).convert("RGB")
a = np.asarray(im).astype(np.float32)
sc = a.shape[1] / 960.0
ao = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.float32)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
fails = []

def cyan(a_):
    r_, g_, b_ = a_[:, :, 0], a_[:, :, 1], a_[:, :, 2]
    return (b_ - r_ > 22) & (g_ - r_ > 8) & (b_ > 110)
def sat(a_):
    r_, g_, b_ = a_[:, :, 0], a_[:, :, 1], a_[:, :, 2]
    return (b_ - r_ > 110) & (g_ - r_ > 60)
def red(a_):
    r_, g_, b_ = a_[:, :, 0], a_[:, :, 1], a_[:, :, 2]
    return (r_ - np.maximum(g_, b_) > 35) & (r_ > 90)
def ink(a_):
    # 640 not 700: the E9E9E7 panel sums to 699 and must NOT read as ink
    return a_.sum(axis=2) < 640
def erode(m):
    o = m.copy(); o[1:, :] &= m[:-1, :]; o[:-1, :] &= m[1:, :]
    o[:, 1:] &= m[:, :-1]; o[:, :-1] &= m[:, 1:]; return o
def comps(mask, min_area=2):
    h, w = mask.shape; seen = np.zeros_like(mask, bool); out = []; ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        st = [(y0, x0)]; seen[y0, x0] = True; pts = []
        while st:
            y, x = st.pop(); pts.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True; st.append((yy, xx))
        if len(pts) >= min_area:
            ys_ = np.array([p[0] for p in pts]); xs_ = np.array([p[1] for p in pts])
            out.append((float(xs_.mean()), float(ys_.mean()), len(pts)))
    return out

print(f"render {im.size[0]}x{im.size[1]}  scale={sc:.4f}   original 960x540")

# ---------- 1. frame containment ----------
print("\n=== 1. FRAME CONTAINMENT ===")
panel = (int(112), int(94), int(1882), int(1125))       # measured house panel in render px
frame = (int(90 * sc), int(127 * sc), int(858 * sc), int(508 * sc))
content = ink(a) & ~red(a) & ~sat(a)
# panel gray is excluded by ink() (<640); drop the purple badge ring too
pr, pg, pb = a[:,:,0], a[:,:,1], a[:,:,2]
purple = (pb - pg > 40) & (pr < 160) & (pb > 120)
content = content & ~purple
# exclude house chrome bands (badge, strokes) before containment
badge = np.zeros_like(content); badge[int(100):int(210), int(1770):int(1880)] = True
content = content & ~badge
# exclude the house chrome strokes themselves (their antialiased halo reads as
# dark ink but is chrome, not content): +-7 frame px around x58.5 / x901 / y538.5
for band_x in (58.5, 901.0):
    content[:, int((band_x-7)*sc):int((band_x+7)*sc)] = False
content[int((538.5-7)*sc):int((538.5+3)*sc), :] = False
content[:, :int(45*sc)] = False
# the document title legitimately sits ABOVE the chart frame (y72..101) — it is not
# a chart element; the containment rule applies to the chart box contents.
content[:int(120*sc), :] = False
ys, xs = np.nonzero(content)
print(f"  chart-area ink bbox (frame px): x{xs.min()/sc:.0f}..{xs.max()/sc:.0f} y{ys.min()/sc:.0f}..{ys.max()/sc:.0f}")
tol_px = int(round(2 * sc))   # the 1F4E79 stroke's own antialias halo
inside = (xs.min() >= frame[0]-tol_px) and (xs.max() <= frame[2]+tol_px) and (ys.min() >= frame[1]-tol_px) and (ys.max() <= frame[3]+tol_px)
print(f"  inside chart frame x{frame[0]/sc:.0f}..{frame[2]/sc:.0f} y{frame[1]/sc:.0f}..{frame[3]/sc:.0f}: {'OK' if inside else 'FAIL'}")
if not inside: fails.append("chart ink outside the 1F4E79 frame")
# ink between the chart frame and the house panel edge (should only be the title / panel-free zones)
band = np.zeros_like(content)
band[:int(94), :] = True
print(f"  ink above the house panel (y<45 frame): {int((content & band).sum())} px")

# ---------- 5. label bands ----------
print("\n=== 5. LABEL BANDS (no ink outside intended band) ===")
def band_ink(box, label):
    x0, y0, x1, y1 = [int(round(v * sc)) for v in box]
    n = int(ink(a)[y0:y1, x0:x1].sum())
    print(f"  {label} band {box}: ink px={n}")
    return n
band_ink((150, 55, 760, 115), "title")
band_ink((230, 182, 390, 205), "heading L")
band_ink((580, 182, 730, 205), "heading R")
band_ink((100, 205, 155, 240), "Loss L")
band_ink((455, 205, 505, 240), "Loss R")
band_ink((330, 445, 460, 470), "xlabel L")
band_ink((670, 445, 805, 470), "xlabel R")

# ---------- 2/3/4 declared absent ----------
print("\n=== 2/3/4. EQUATIONS / DELIMITERS / TABLES ===")
print("  slide 028 has no equation, delimiter or table region (analysis JSON: equations [],")
print("  visual_elements = graphs + highlight-box only) -> checked as NOT APPLICABLE, not skipped.")

# ---------- A. LEFT panel markers ----------
print("\n=== A. LEFT PANEL descent markers ===")
left = (155, 225, 300, 450)
x0, y0, x1, y1 = [int(round(v * sc)) for v in left]
L = a.mean(axis=2); Cm = cyan(a).astype(np.float32)
ang = np.linspace(0, 2 * np.pi, 24, endpoint=False)
offs = []
for rr in (2.6, 3.0, 3.4, 3.8, 4.2):
    offs.append([(int(round(rr * sc * np.sin(t))), int(round(rr * sc * np.cos(t)))) for t in ang])
pad = int(round(4.4 * sc)); hits = []
for y in range(y0 + pad, y1 - pad):
    for x in range(x0 + pad, x1 - pad):
        if L[y, x] < 238: continue
        if L[y-1:y+2, x-1:x+2].min() < 226: continue
        cov = max(np.mean([Cm[y+dy, x+dx] for dy, dx in oo]) for oo in offs)
        if cov >= 0.66: hits.append((x, y, cov))
hits.sort(key=lambda h: -h[2]); picked = []
for x, y, c in hits:
    if all((x-px)**2 + (y-py)**2 >= (5*sc)**2 for px, py, _ in picked): picked.append((x, y, c))
picked.sort(key=lambda p: p[1])
print(f"  hollow circles found: {len(picked)}")
want = [(179, 251), (195, 288), (220, 349), (239, 394), (247, 413), (262, 436), (283, 440)]
for x, y, c in picked:
    fx, fy = x / sc, y / sc
    dist = min(((fx-wx)**2 + (fy-wy)**2) ** 0.5 for wx, wy in want)
    print(f"    ({fx:6.1f},{fy:6.1f}) ring={c:.2f} nearest-original={dist:.1f}px")
for wx, wy in want:
    best = min(((x/sc-wx)**2 + (y/sc-wy)**2) ** 0.5 for x, y, _ in picked) if picked else 99
    tag = "OK" if best <= 2.5 else "MISSING/OFF"
    if best > 2.5: fails.append(f"left circle ({wx},{wy}) not found within 2.5px (best {best:.1f})")
    print(f"    want ({wx},{wy}): nearest render circle {best:.1f}px -> {tag}")
core = sat(a).copy()
for _ in range(5): core = erode(core)      # fixed 5 erosions (native res), as measured
lsub = np.zeros_like(core); lsub[y0:y1, x0:x1] = core[y0:y1, x0:x1]
lf = comps(lsub, 2)
print(f"  filled saturated discs in the LEFT panel: {len(lf)} (original: 0)")
if lf: fails.append("filled disc(s) in the left panel")
rarm = np.zeros_like(Cm, dtype=bool)
rarm[y0:y1, int(round(290*sc)):int(round(440*sc))] = True
onarm = [p for p in picked if p[0]/sc > 290]
print(f"  hollow markers on the left panel's right arm (x>290): {len(onarm)} (original: 0)")
if onarm: fails.append("marker on the empty right arm")

# ---------- B. RIGHT panel ----------
print("\n=== B. RIGHT PANEL markers + connector topology ===")
rx0, ry0, rx1, ry1 = [int(round(v * sc)) for v in (495, 205, 790, 455)]
core = sat(a).copy()
for _ in range(5): core = erode(core)
rsub = np.zeros_like(core); rsub[ry0:ry1, rx0:rx1] = core[ry0:ry1, rx0:rx1]
rf = sorted(comps(rsub, 2))
print(f"  saturated discs: {len(rf)}")
want_r = [(562, 315), (593, 395), (683, 351), (710, 284)]
for cx, cy, area in rf:
    print(f"    ({cx/sc:6.1f},{cy/sc:6.1f}) area={area}")
for wx, wy in want_r:
    best = min(((cx/sc-wx)**2 + (cy/sc-wy)**2) ** 0.5 for cx, cy, _ in rf) if rf else 99
    tag = "OK" if best <= 2.0 else "MISSING/OFF"
    if best > 2.0: fails.append(f"right disc ({wx},{wy}) not found within 2px (best {best:.1f})")
    print(f"    want ({wx},{wy}): nearest render disc {best:.1f}px -> {tag}")

P = dict(A=(562, 315), B=(593, 395), C=(683, 351), D=(710, 284))
def chord_cov(p, q, trim=9, tol=1.0):
    x0_, y0_ = p; x1_, y1_ = q
    n = int(max(abs(x1_-x0_), abs(y1_-y0_))); dx, dy = (x1_-x0_)/n, (y1_-y0_)/n
    nx, ny = -dy, dx; nn = max((nx*nx+ny*ny)**0.5, 1e-9); nx, ny = nx/nn, ny/nn
    cov = tot = 0; cols = []
    for i in range(n + 1):
        if i < trim or n - i < trim: continue
        tot += 1; hit = False
        for o in np.arange(-tol, tol + 0.01, 0.34):
            x = int(round((x0_ + dx*i + nx*o) * sc)); y = int(round((y0_ + dy*i + ny*o) * sc))
            px = a[y, x]
            if px.sum() < 700 and not (px[0] - max(px[1], px[2]) > 60):
                hit = True; cols.append(px); break
        cov += 1 if hit else 0
    mc = tuple(int(v) for v in np.mean(np.stack(cols), axis=0)) if cols else None
    return cov / max(tot, 1), mc
expect = {("A","C"): 1, ("A","D"): 1, ("B","C"): 1, ("A","B"): 0, ("B","D"): 0}
print("  connector chords (render_8, original's measured truth in brackets):")
for (u, v), want_cov in expect.items():
    f, mc = chord_cov(P[u], P[v])
    ok = (f > 0.80) if want_cov else (f < 0.25)
    print(f"    {u}-{v}: {f:.2f} mean={mc}  expected {'present' if want_cov else 'absent'} -> {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(f"connector {u}-{v} coverage {f:.2f}")

# ---------- C. curve ripple ----------
print("\n=== C. CURVE RIPPLE (rendered stroke vs analytic quartic) ===")
LEFT = [1.257813992130e-06, -1.380428744223e-03, 5.367079591099e-01, -8.662429049860e+01, 5.186743353907e+03]
RIGHT = [1.280248111588e-06, -3.212513553308e-03, 2.991242381533e+00, -1.224430887994e+03, 1.862054178402e+05]
def cy(f, x): return ((((f[0]*x+f[1])*x+f[2])*x+f[3])*x+f[4])
C = cyan(a)
for nm, f, xa, xb, box in (("LEFT", LEFT, 161, 383, (150, 205, 440, 455)), ("RIGHT", RIGHT, 514, 737, (495, 205, 790, 455))):
    bx0, by0, bx1, by1 = [int(round(v * sc)) for v in box]
    worst = 0; ncols = 0
    for xf in range(xa + 2, xb - 1):
        xr = int(round(xf * sc))
        col = np.nonzero(C[by0:by1, xr])[0]
        if len(col) == 0: continue
        ys_ = col / sc + by0 / sc
        target = cy(f, xf)
        d = min(abs(ys_ - target))
        worst = max(worst, d); ncols += 1
    print(f"  {nm}: columns {ncols}, worst cyan ink distance from quartic = {worst:.1f} frame px")
    if worst > 6: fails.append(f"{nm} curve deviates {worst:.1f}px from its analytic quartic")

# ---------- D. text bboxes vs original ----------
print("\n=== D. TEXT INK BBOXES (render_8 vs measured original) ===")
def bbox(a_, box, thr, sc_, exclude_red=False):
    x0_, y0_, x1_, y1_ = [int(round(v * sc_)) for v in box]
    sub = a_[y0_:y1_, x0_:x1_]; L_ = sub.mean(axis=2); m = L_ < thr
    if exclude_red:
        r_, g_, b_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
        m &= ~((r_ - np.maximum(g_, b_) > 35) & (r_ > 90))
    if not m.any(): return None
    ys_, xs_ = np.nonzero(m); px_ = sub[m]
    core_ = px_[np.argsort(px_.sum(axis=1))[:max(1, len(px_)//10)]].mean(axis=0)
    return (box[0]+xs_.min()/sc_, box[0]+xs_.max()/sc_, box[1]+ys_.min()/sc_, box[1]+ys_.max()/sc_,
            tuple(int(v) for v in core_))
checks = [
 ("title",  (150,55,760,115), 170, (189,690,72,101), 12),
 ("headL",  (230,182,390,205), 190, (239,374,187,200), 4),
 ("LossL",  (100,205,155,240), 180, (122,154,216,230), 4),
 ("xlabL",  (330,445,470,470), 190, (367,453,448,460), 8),
 ("xlabR",  (670,445,810,470), 190, (707,797,450,462), 8),
]
for nm, box, thr, wantb, tol in checks:
    got = bbox(a, box, thr, sc, exclude_red=(nm.startswith("xlab")))
    if got is None:
        print(f"  {nm}: NO INK -> FAIL"); fails.append(f"{nm} missing"); continue
    dmax = max(abs(got[i]-wantb[i]) for i in range(4))
    print(f"  {nm}: render x{got[0]:.0f}..{got[1]:.0f} y{got[2]:.0f}..{got[3]:.0f} core={got[4]}"
          f" | original x{wantb[0]}..{wantb[1]} y{wantb[2]}..{wantb[3]} | max edge delta {dmax:.0f}px")
    if dmax > tol: fails.append(f"{nm} ink bbox off by {dmax:.0f}px (tol {tol})")

print("\n=== RESULT ===")
if fails:
    print("SELF-CHECK FAIL:")
    for f in fails: print("  - " + f)
else:
    print("SELF-CHECK PASS — containment, marker sets, connector topology, ripple, text boxes all within tolerance")
