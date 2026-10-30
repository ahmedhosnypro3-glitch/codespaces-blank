#!/usr/bin/env python3
"""Objective pixel measurement of original slide_008.jpg — geometry, colors, hatching, clusters."""
import numpy as np
from PIL import Image
from scipy import ndimage
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = np.array(Image.open(f"{V}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

print("=" * 70)
print("PLOT RECTANGLE (border pixels)")
print("=" * 70)
L, R, T, B = 166, 797, 119, 507
print(f"  x=[{L},{R}] y=[{T},{B}]  width={R-L} height={B-T}")
print(f"  in inches (1px=1pt): x={L/72:.3f} y={T/72:.3f} w={(R-L)/72:.3f} h={(B-T)/72:.3f}")
print("  border core colors: top(120,400)", im[120, 400], " left(300,166)", im[300, 166])
print("  plot border ~ #642B3A on JPEG, spec says #c0392b")

print()
print("=" * 70)
print("HATCHING / REGION TINTS")
print("=" * 70)


def region_colors(y0, y1, x0, x1, label):
    px = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            px.append(tuple(im[y, x]))
    c = Counter(px)
    print(f"  {label} (x{x0}-{x1} y{y0}-{y1}) top colors:")
    for col, n in c.most_common(6):
        print(f"      #{col[0]:02X}{col[1]:02X}{col[2]:02X}  n={n}")


region_colors(140, 330, 200, 560, "GREEN region")
region_colors(240, 500, 560, 780, "BLUE region")
region_colors(330, 480, 250, 460, "RED region")


def hatch_pixels(y0, y1, x0, x1, base, label):
    """dark-local-min pixels relative to base tint = hatch strokes"""
    d = np.abs(im - np.array(base)).sum(axis=2)
    m = d > 40
    m[:T] = False
    m[B:] = False
    m[:, :L] = False
    m[:, R:] = False
    m[:y0] = False
    m[y1:] = False
    m[:, :x0] = False
    m[:, x1:] = False
    ys, xs = np.nonzero(m)
    print(f"  {label}: {len(xs)} hatch-ish px, bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
    if len(xs) < 50:
        return
    # PCA orientation of the stroke pixels
    P = np.stack([xs, ys], 1).astype(float)
    P = P - P.mean(0)
    cov = np.cov(P.T)
    w, v = np.linalg.eigh(cov)
    ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
    print(f"      stroke axis angle={ang:.1f} deg (0=horizontal, 90=vertical), "
          f"eigen ratio={w[1]/max(w[0],1e-9):.2f}")
    # spacing via count / span
    span = max(xs.ptp(), ys.ptp())
    print(f"      density: {(len(xs)/span):.3f} px per unit span")


hatch_pixels(140, 330, 200, 560, (229, 255, 228), "GREEN hatch")
hatch_pixels(240, 500, 560, 780, (227, 226, 255), "BLUE hatch")
hatch_pixels(330, 480, 250, 460, None, "RED hatch (base auto)")

print()
print("=" * 70)
print("CLASS DOTS — tight circle detection (dark-edge ring)")
print("=" * 70)


def dots(color, label, tol=120):
    d = np.abs(im - np.array(color)).sum(axis=2)
    m = d < tol
    m[:T] = False; m[B:] = False; m[:, :L] = False; m[:, R:] = False
    # dilate slightly then label round blobs
    m2 = ndimage.binary_dilation(m, np.ones((3, 3)))
    lab, n = ndimage.label(m2, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
        if 8 <= w <= 24 and 8 <= h <= 24 and w / h > 0.7:
            core = m[ys, xs].sum()
            if core < 0.25 * len(xs):
                continue
            out.append((len(xs), int(xs.mean()), int(ys.mean()), w, h, core))
    out.sort()
    print(f"  {label}: {len(out)} round blobs")
    for c in out:
        print(f"      n={c[0]:3d} center=({c[1]:3d},{c[2]:3d}) wh={c[3]}x{c[4]} corefrac={c[5]/ (c[3]*c[4]):.2f}")
    if out:
        cx = np.array([c[1] for c in out]); cy = np.array([c[2] for c in out])
        print(f"      centroid=({cx.mean():.0f},{cy.mean():.0f}) spread=({cx.std():.1f},{cy.std():.1f}) "
          f"bbox x[{cx.min()},{cx.max()}] y[{cy.min()},{cy.max()}]")
    return out


dots((46, 204, 113), "GREEN (C1)")
dots((41, 128, 185), "BLUE (C2)")
dots((192, 57, 43), "RED (C3)")

print()
print("=" * 70)
print("TEXT / LABEL REGIONS")
print("=" * 70)
# dark ink (black text) clusters inside plot
ink = (im.max(axis=2) < 130)
ink[:T] = False; ink[B:] = False; ink[:, :L] = False; ink[:, R:] = False
lab, n = ndimage.label(ink, np.ones((3, 3)))
comps = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(xs) < 12:
        continue
    comps.append((len(xs), int(xs.mean()), int(ys.mean()), xs.min(), xs.max(), ys.min(), ys.max()))
comps.sort(key=lambda c: (c[5], c[1]))
print("  dark-ink clusters inside plot (y-ordered):")
for c in comps:
    print(f"      n={c[0]:4d} c=({c[1]:3d},{c[2]:3d}) bbox x[{c[3]}..{c[4]}] y[{c[5]}..{c[6]}]")

# title band dark ink
sub = im[55:110, 200:760]
ink2 = (sub.max(axis=2) < 170)
rows = ink2.sum(axis=1)
print("  TITLE ink rows:", [(55 + i, v) for i, v in enumerate(rows) if v > 0])

print()
print("=" * 70)
print("OUTSIDE-PLOT ELEMENTS")
print("=" * 70)
pur = (b > 200) & (r > 180) & (g < 210)
ys, xs = np.nonzero(pur)
print("  PURPLE-ish bbox (New Class):", xs.min(), xs.max(), ys.min(), ys.max(), "n=", len(xs))
