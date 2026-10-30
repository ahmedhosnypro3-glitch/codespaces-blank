#!/usr/bin/env python3
"""Corrected adjudication pass 2. Fixes three measurement errors in pass 1:
  - finding 7 was measured on the header's EMPTY label cell (ci=0) instead of
    the "X1" cell (ci=1);
  - finding 2's Again-box window (y360..520) missed the box (y270..316);
  - finding 5 only recovered ONE of each box's two text lines, so the
    left/centre conclusion was drawn from a single line.
Also runs a decisive is-it-a-real-red-element test for finding 1, using the
frame's own chroma-fringe signature as the control.
"""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/"
o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_012.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(QA + "render_3.png").convert("RGB")).astype(int)
S = r.shape[1] / o.shape[1]

print("=" * 76)
print("1a. DECISIVE: is the y250..252 x670..705 red band a real element?")
print("=" * 76)
R, G, B = o[:, :, 0], o[:, :, 1], o[:, :, 2]
rg = R - G
rb = R - B
print("Per-row red-dominance over x665..710 (original). A real red stroke should")
print("stand out sharply against neighbouring rows.")
for y in range(244, 258):
    rr = rg[y, 665:710].mean(); bb = rb[y, 665:710].mean()
    mark = "  <== RED-DOMINANT" if rr > 8 else ""
    print(f"  y={y}: R-G={rr:+6.1f}  R-B={bb:+6.1f}{mark}")
print("\nRows 260..276 (the same band ABOVE the callout, for contrast):")
for y in range(258, 270):
    print(f"  y={y}: R-G={rg[y,665:710].mean():+6.1f}  R-B={rb[y,665:710].mean():+6.1f}")
print("\nControl: red-dominance of chroma fringe on KNOWN horizontal edges.")
print("  test-table bottom border (y252, x740..800): R-G=%+.1f" % rg[250:255, 740:800].mean())
print("  middle-table top border (y265, x300..400) : R-G=%+.1f" % rg[263:268, 300:400].mean())
print("  question-box top border (y366, x700..800) : R-G=%+.1f" % rg[364:369, 700:800].mean())
print("\n  -> if all controls are BLUE-dominant and only the candidate band is")
print("     RED-dominant, the band is a real red element, not JPEG fringe.")

print("\n" + "=" * 76)
print("1b. Where exactly is that band's ink?")
print("=" * 76)
m = (R > G + 18) & (R > B + 18) & (R > 95)
for (y0, y1) in ((244, 246), (246, 250), (250, 253), (253, 257)):
    z = m[y0:y1, 660:715]
    ys, xs = np.nonzero(z)
    if len(xs):
        print(f"  y{y0}..{y1-1}: {z.sum():4d} loose-red px  x{660+xs.min()}..{660+xs.max()}")
    else:
        print(f"  y{y0}..{y1-1}:   0")

print("\n" + "=" * 76)
print("2. Again-box + question-box geometry, both images")
print("=" * 76)
for nm, a, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    mr = (a[:, :, 0] > 150) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    mb = (a[:, :, 2] > 120) & (a[:, :, 0] < 100) & (a[:, :, 1] < 100)
    wA = mr[int(265*sc):int(320*sc), int(700*sc):int(840*sc)]
    ys, xs = np.nonzero(wA)
    if len(ys):
        print(f"  {nm} Again box: x{700+xs.min()/sc:.0f}..{700+xs.max()/sc:.0f} "
              f"y{265+ys.min()/sc:.0f}..{265+ys.max()/sc:.0f}  "
              f"(w={(xs.max()-xs.min()+1)/sc:.0f} h={(ys.max()-ys.min()+1)/sc:.0f})")
    wQ = mb[int(360*sc):int(420*sc), int(590*sc):int(880*sc)]
    yq, xq = np.nonzero(wQ)
    if len(yq):
        print(f"  {nm} question box blue ink: x{590+xq.min()/sc:.0f}..{590+xq.max()/sc:.0f} "
              f"y{360+yq.min()/sc:.0f}..{360+yq.max()/sc:.0f}")
    # question-box BORDER, found as a 1pt rectangle: scan for a long vertical blue run
    print(f"  {nm} question box border scan:")
    for x in range(int(600*sc), int(875*sc)):
        col = mb[int(360*sc):int(420*sc), x]
        run = col.sum()
        if run > 25:
            print(f"      vertical blue run at x={600+x/sc:.0f} -> {run} px tall")
            break
    for y in range(int(360*sc), int(420*sc)):
        row = mb[y, int(600*sc):int(875*sc)]
        if row.sum() > 150:
            print(f"      horizontal blue run at y={360+y/sc:.0f} -> {row.sum()} px wide")
            break

print("\n" + "=" * 76)
print("5. Text alignment inside EVERY label box (both text lines recovered)")
print("=" * 76)
BOXES = {
    "Training Data": (68, 104, 197, 133),
    "Perfect Data":  (69, 175, 196, 221),
    "Outlier 1":     (69, 323, 196, 349),
    "Outlier 2":     (69, 445, 196, 471),
    "Again":         (707, 270, 835, 316),
}
for name, (bx0, by0, bx1, by1) in BOXES.items():
    bc = (bx0 + bx1) / 2
    bw = bx1 - bx0 + 1
    print(f"  {name} (box centre x={bc:.0f}, w={bw}):")
    for nm, a, sc in (("ORIG ", o, 1.0), ("REND ", r, S)):
        sub = a[int(by0*sc):int(by1*sc)+1, int(bx0*sc):int(bx1*sc)+1]
        # white-ish text on a saturated fill
        sat = sub.max(axis=2) - sub.min(axis=2)
        lum = sub.mean(axis=2)
        ink = (lum > 190) & (sat < 70)
        rows = np.nonzero(ink.any(axis=1))[0]
        if not len(rows):
            print(f"      {nm}: no white ink found")
            continue
        lines, start = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] - rows[i-1] > 1:
                lines.append((start, rows[i-1])); start = rows[i]
        lines.append((start, rows[-1]))
        for a0, a1 in lines:
            cs = np.nonzero(ink[a0:a1+1].any(axis=0))[0]
            if not len(cs):
                continue
            L = bx0 + cs.min()/sc; Rr = bx0 + cs.max()/sc
            ctr = (L + Rr) / 2
            insetL = L - bx0; insetR = bx1 - Rr
            print(f"      {nm}: y{by0+a0/sc:.0f}..{by0+a1/sc:.0f} x{L:.0f}..{Rr:.0f} "
                  f"centre={ctr:.0f} (box {bc:.0f}, {ctr-bc:+.0f})  "
                  f"insets L{insetL:.0f}/R{insetR:.0f}")

print("\n" + "=" * 76)
print("7. Header cell ci=1 (the 'X1' cell), not the empty label cell")
print("=" * 76)
for nm, a, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    # T1 header row y127..158, col ci=1 -> x244..285
    sub = a[int(127*sc):int(158*sc)+1, int(244*sc):int(285*sc)+1]
    lum = sub.mean(axis=2)
    ink = lum < 150
    full = ink.sum(axis=1) > 0.9 * ink.shape[1]
    rows = np.nonzero(ink.any(axis=1))[0]
    txt = rows[~full[rows]]
    print(f"  {nm} X1 header cell (x244..285 y127..158, h=31, centre=142.5):")
    if len(txt):
        print(f"      text rows y{127+txt.min()/sc:.0f}..{127+txt.max()/sc:.0f} "
              f"({(txt.max()-txt.min()+1)/sc:.0f}px) centre={127+(txt.min()+txt.max())/2/sc:.1f}")
    else:
        print(f"      no dark text ink (ink threshold)")
    grid = np.nonzero(full)[0]
    if len(grid):
        print(f"      grid rows at y: {[int(127+gg/sc) for gg in grid]}")
    # also the y-row and data rows for line-height reference
    for lbl, (y0, y1) in (("row X1 data", (158, 189)), ("row y", (219, 249))):
        s2 = a[int(y0*sc):int(y1*sc)+1, int(244*sc):int(285*sc)+1]
        l2 = s2.mean(axis=2); i2 = l2 < 150
        f2 = i2.sum(axis=1) > 0.9 * i2.shape[1]
        rr = np.nonzero(i2.any(axis=1))[0]; tt = rr[~f2[rr]]
        if len(tt):
            print(f"      {lbl}: text rows y{y0+tt.min()/sc:.0f}..{y0+tt.max()/sc:.0f} "
                  f"centre={y0+(tt.min()+tt.max())/2/sc:.1f}")
