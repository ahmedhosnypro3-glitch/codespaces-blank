#!/usr/bin/env python3
"""PIL adjudication of the seven MINOR findings in judge_attempt_3.txt.

Every finding is measured against BOTH images (original 960x540, 1px=1pt;
render_3 2001x1125, S=2001/960). Findings 1, 2, 3, 5 and 7 are actionable;
4 was already adjudicated in a prior turn; 6 is self-declared as unconfirmed.
"""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/"
o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_012.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(QA + "render_3.png").convert("RGB")).astype(int)
S = r.shape[1] / o.shape[1]


def crop(a, x0, y0, x1, y1, sc=1.0):
    return a[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]


print("=" * 76)
print("1. 'Added red left-pointing arrow — not present in IMG2' (MINOR, high)")
print("=" * 76)
R, G, B = o[:, :, 0], o[:, :, 1], o[:, :, 2]
loose = (R > G + 18) & (R > B + 18) & (R > 95)
print("Raw colours along y246..256 in the gap row x668..708 (original frame):")
for y in range(246, 257):
    row = [tuple(o[y, x]) for x in range(668, 709, 6)]
    print(f"  y={y}: " + " ".join(f"{c[0]:3d},{c[1]:3d},{c[2]:3d}" for c in row[:7]))
print("\nIs there a DARK core (arrow shaft) or only a pink wash (JPEG chroma")
print("fringe from a nearby horizontal edge)?")
band = o[244:258, 665:712]
lum = band.mean(axis=2)
print(f"  luminance min={lum.min():.0f} max={lum.max():.0f} mean={lum.mean():.0f}")
print(f"  red-minus-green mean={band[:,:,0].mean()-band[:,:,1].mean():+.1f}  "
      f"red-minus-blue mean={band[:,:,0].mean()-band[:,:,2].mean():+.1f}")
# Is the pink band bounded left/right, or does it follow the panel?
print(f"  panel gray reference (x600,y245): {tuple(o[245,600])}")
# Does the pink band align EXACTLY with a dark horizontal edge at y252 spanning x670..705?
dark = o[246:258, 660:715].mean(axis=2) < 200
print(f"  pixels darker than 200 in y246..257 x660..715: {dark.sum()}")
ys, xs = np.nonzero(dark)
if dark.sum():
    print(f"    bbox x{660+xs.min()}..{660+xs.max()} y{246+ys.min()}..{246+ys.max()}")
# Compare with a KNOWN real horizontal edge (test table bottom border y252) fringing
print("\nControl — same test on the test table's bottom border (x740..800, y246..258):")
tb = o[244:260, 740:800]
print(f"  red-minus-green mean={tb[:,:,0].mean()-tb[:,:,1].mean():+.1f}  "
      f"red-minus-blue mean={tb[:,:,0].mean()-tb[:,:,2].mean():+.1f}  "
      f"lum min={tb.mean(axis=2).min():.0f}")

print("\n" + "=" * 76)
print("2. 'Again box sits lower than in the original' (MINOR, medium)")
print("=" * 76)
for nm, a, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    m = (a[:, :, 0] > 150) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    z = m[int(360*sc):int(520*sc), int(690*sc):int(880*sc)]
    ys, xs = np.nonzero(z)
    if len(ys):
        print(f"  {nm}: red box bbox x{690+xs.min()/sc:.0f}..{690+xs.max()/sc:.0f} "
              f"y{360+ys.min()/sc:.0f}..{360+ys.max()/sc:.0f}")
    # question box: blue border
    mb = (a[:, :, 2] > 120) & (a[:, :, 0] < 100) & (a[:, :, 1] < 100)
    zq = mb[int(360*sc):int(420*sc), int(595*sc):int(875*sc)]
    yq, xq = np.nonzero(zq)
    if len(yq):
        print(f"  {nm}: blue box bbox x{595+xq.min()/sc:.0f}..{595+xq.max()/sc:.0f} "
              f"y{360+yq.min()/sc:.0f}..{360+yq.max()/sc:.0f}")
print("  -> the two boxes' relative vertical offset is the finding.")

print("\n" + "=" * 76)
print("3. Question-box line break differs (MINOR, high)")
print("=" * 76)
for nm, a, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    # blue text rows inside the question box x604..868 y366..414
    sub = a[int(366*sc):int(414*sc), int(604*sc):int(868*sc)]
    R_, G_, B_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    ink = (B_ > R_ + 25) & (B_ > G_ + 25) & (B_ > 110)
    rows = np.nonzero(ink.any(axis=1))[0]
    if len(rows):
        # group contiguous rows into lines
        lines, start = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] - rows[i-1] > 2:
                lines.append((start, rows[i-1])); start = rows[i]
        lines.append((start, rows[-1]))
        desc = []
        for a0, a1 in lines:
            cs = np.nonzero(ink[a0:a1+1].any(axis=0))[0]
            desc.append(f"line y{366+a0/sc:.0f}..{366+a1/sc:.0f} "
                        f"({(a1-a0+1)/sc:.0f}px tall) x{604+cs.min()/sc:.0f}..{604+cs.max()/sc:.0f} "
                        f"({(cs.max()-cs.min()+1)/sc:.0f}px wide)")
        print(f"  {nm}: {len(lines)} text lines -> " + "; ".join(desc))
    else:
        print(f"  {nm}: no blue ink found")

print("\n" + "=" * 76)
print("5. Two-line red boxes: recreation left-aligned vs original centered (MINOR, med)")
print("=" * 76)
for nm, a, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    for label, (bx0, by0, bx1, by1) in (("Perfect Data box", (69, 175, 196, 221)),
                                        ("Again box", (707, 270, 835, 316))):
        sub = a[int(by0*sc):int(by1*sc), int(bx0*sc):int(bx1*sc)]
        # white text on a red fill
        lumw = sub.mean(axis=2)
        ink = lumw > 200
        rows = np.nonzero(ink.any(axis=1))[0]
        if len(rows):
            lines, start = [], rows[0]
            for i in range(1, len(rows)):
                if rows[i] - rows[i-1] > 2:
                    lines.append((start, rows[i-1])); start = rows[i]
            lines.append((start, rows[-1]))
            parts = []
            for a0, a1 in lines:
                cs = np.nonzero(ink[a0:a1+1].any(axis=0))[0]
                L = bx0 + cs.min()/sc; Rr = bx0 + cs.max()/sc
                ctr = (L + Rr) / 2
                parts.append(f"line y{by0+a0/sc:.0f}..{by0+a1/sc:.0f}: x{L:.0f}..{Rr:.0f} "
                             f"w={Rr-L+1:.0f} centre={ctr:.0f}")
            bw = bx1 - bx0 + 1
            print(f"  {nm} {label} (box centre x={(bx0+bx1)/2:.0f}, w={bw}):")
            for p in parts:
                print(f"      {p}")

print("\n" + "=" * 76)
print("7. Header row looks taller / labels ride higher (MINOR, low-medium)")
print("=" * 76)
TC = [203, 244, 285, 326, 367, 407, 448, 489, 529, 571]
for nm, a, sc in (("ORIGINAL", o, 1.0), ("RENDER", r, S)):
    print(f"  {nm} T1 header cell (x203..244, y127..158):")
    sub = a[int(127*sc):int(158*sc), int(203*sc):int(244*sc)]
    lum = sub.mean(axis=2)
    ink = lum < 150
    rows = np.nonzero(ink.any(axis=1))[0]
    if len(rows):
        # exclude the grid lines (full-width dark rows)
        full = (ink.sum(axis=1) > 0.9 * ink.shape[1])
        txt = rows[~full[rows]]
        if len(txt):
            print(f"      text ink rows y{127+txt.min()/sc:.0f}..{127+txt.max()/sc:.0f} "
                  f"({(txt.max()-txt.min()+1)/sc:.0f}px tall) inside cell y127..158 (h=31)")
            print(f"      text vertical centre={(127+(txt.min()+txt.max())/2/sc):.1f} vs cell centre=142.5")
    full_rows = np.nonzero(ink.sum(axis=1) > 0.9*ink.shape[1])[0]
    print(f"      full-width grid rows: {[int(127+rr/sc) for rr in full_rows]}")
