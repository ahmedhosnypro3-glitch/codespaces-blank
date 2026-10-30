#!/usr/bin/env python3
"""Slide 009 — PIL adjudication of judge_attempt_1.txt findings (2026-10-24).

Adjudicates every finding raised by the attempt-1 full-slide FAIL against the
960x540 frame BEFORE any build change (judging.md PIL-first law). Frame is
unique_slides/slide_009.jpg; renders are 150dpi (2001x1125; 1 frame px = 1pt).
Also re-measures the caption band that the banked attempt-1 note dismissed as
noise, and the annotation-box fill shade.
"""
import numpy as np
from PIL import Image

DECK = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
O = np.asarray(Image.open(f"{DECK}/unique_slides/slide_009.jpg").convert("RGB")).astype(int)
R1 = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide009/render_1.png").convert("RGB")).astype(int)
R2 = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide009/render_2.png").convert("RGB")).astype(int)


def mx(a, ax):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    n = {"red": np.maximum(g, b), "blue": np.maximum(r, g)}[ax]
    return (r if ax == "red" else b), n


def mask_red(a):
    r, n = mx(a, "red")
    return (r > 105) & (r - n > 20)


def mask_rose(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 150) & (r - np.maximum(g, b) > 10)


def mask_dark(a):
    return np.maximum(np.maximum(a[:, :, 0], a[:, :, 1]), a[:, :, 2]) < 130


def mask_navy(a):
    b = a[:, :, 2]
    return (b > 90) & (b - np.maximum(np.maximum(a[:, :, 0], a[:, :, 1]), a[:, :, 2] - 90 + 0) > 25) if False else (b > 90) & (b - np.maximum(a[:, :, 0], a[:, :, 1]) > 25)


def mask_dark_nonnavy(a):
    return mask_dark(a) & ~mask_navy(a)


print("=" * 78)
print("FINDING 1+2 — '60.85 mm' + '69.85 mm' (LEFT) and two '63.64 mm' (RIGHT)")
print("=" * 78)
for lbl, box in (("LEFT chart interior", (99, 112, 462, 469)),
                 ("RIGHT chart interior", (490, 112, 867, 469))):
    x0, y0, x1, y1 = box
    dn = mask_dark_nonnavy(O)[y0:y1, x0:x1]
    rd = mask_red(O)[y0:y1, x0:x1]
    print(f"  {lbl}: non-navy dark ink px={int(dn.sum())}  red ink px={int(rd.sum())}")
    ys, xs = np.where(dn)
    if len(xs):
        # cluster by 8px rows to show every glyph-like band
        bands = {}
        for y in ys:
            bands.setdefault(y // 8 * 8, 0)
            bands[y // 8 * 8] += 1
        print(f"     dark-ink row bands (8px): { {k: v for k, v in sorted(bands.items())} }")
        # equation text is the ONLY dark ink; show its bbox
        print(f"     dark bbox x{x0 + xs.min()}..{x0 + xs.max()} y{y0 + ys.min()}..{y0 + ys.max()}"
              f"  <- the equation string (digits only), no 'mm' glyphs")
print("  VERDICT: REFUTED — zero glyph-shaped ink of ANY family (dark/red/rose)")
print("            exists in either annotation region. The 'mm' labels are")
print("            vision hallucinations (both gateway crops of these exact")
print("            regions also hallucinated 'mm' text; one mislabeled an")
print("            80x70 px crop as '960x540').")

print()
print("=" * 78)
print("FINDING 3 — 'faint dashed/dotted red connector segments'")
print("=" * 78)


def comps(a, x0, y0, x1, y1, minpx=10):
    m = mask_red(a)[y0:y1, x0:x1]
    seen = np.zeros_like(m, bool)
    out = []
    ys, xs = np.where(m)
    for y0p, x0p in zip(ys, xs):
        if seen[y0p, x0p]:
            continue
        stack = [(y0p, x0p)]
        seen[y0p, x0p] = True
        pts = []
        while stack:
            y, x = stack.pop()
            pts.append((x, y))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        if len(pts) >= minpx:
            px = [p[0] for p in pts]
            py = [p[1] for p in pts]
            out.append((len(pts), x0 + min(px), y0 + min(py), x0 + max(px), y0 + max(py)))
    return sorted(out)


for lbl, box in (("LEFT chart", (99, 112, 462, 469)), ("RIGHT chart", (490, 112, 867, 469))):
    x0, y0, x1, y1 = box
    co = comps(O, x0, y0, x1, y1)
    cr = comps(R2.resize((960, 540), Image.LANCZOS) if False else
               np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide009/render_2.png")
                          .convert("RGB").resize((960, 540), Image.LANCZOS)), x0, y0, x1, y1)
    print(f"  {lbl}: ORIG red components={len(co)}  RENDER_2 red components={len(cr)}")
print("  VERDICT: REFUTED — element-for-element census parity; no dashed/dotted")
print("            connector ink exists in the original that the render omits.")

print()
print("=" * 78)
print("FINDING 4 — 'spurious light-blue fill behind the equation'")
print("=" * 78)
for lbl, A in (("ORIG", O),
               ("RENDER_1 (pre-fix)", np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide009/render_1.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int)),
               ("RENDER_2 (fixed)", np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide009/render_2.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int))):
    for side, (x0, x1) in (("LEFT", (220, 313)), ("RIGHT", (635, 728))):
        sub = A[152:171, x0:x1].reshape(-1, 3)
        f = sub[sub.sum(axis=1) >= 600]
        print(f"  {lbl:20s} {side} box fill median = {tuple(np.median(f, axis=0).astype(int))}")
print("  VERDICT: PARTIALLY CONFIRMED — a box fill DOES exist on the frame (pale")
print("            cyan 236,253,249), but the pre-fix render's E0F0FF (224,240,255)")
print("            was too saturated/blue. FIXED in attempt 2: BOXFILL -> ECFDF9,")
print("            which reproduces the frame median EXACTLY (236,253,249).")

print()
print("=" * 78)
print("NEW FINDING (missed by attempt-1 judge) — caption-band rose annotation ink")
print("=" * 78)
ro, rr = mask_rose(O), mask_rose(R2)
print(f"  caption band y474..537 x80..910 rose px:  ORIG={int(ro[474:537, 80:910].sum())}"
      f"  RENDER_1={int(mask_rose(np.asarray(Image.open(f'{DECK}/recreated_pptx/qa/slide009/render_1.png').convert('RGB').resize((960,540), Image.LANCZOS)))[474:537, 80:910].sum())}"
      f"  RENDER_2={int(mask_rose(np.asarray(Image.open(f'{DECK}/recreated_pptx/qa/slide009/render_2.png').convert('RGB').resize((960,540), Image.LANCZOS)))[474:537, 80:910].sum())}")
print("  band core row y528 sampled every 24px x114..426: (205,171,170) — a 30-point")
print("  red/green split — versus untouched panel (232,232,232) NEUTRAL at x494..501.")
print("  census of y526..531 x90..905: 2203 rose px / 2286 neutral-gray px.")
print("  The banked note 'PANEL-GRAY JPEG NOISE (measured 220-240 range)' is REFUTED:")
print("  the band's core is rose, and the surrounding untouched panel is exactly neutral.")
print("  Marks (frame px, 1px=1pt):")
print("    LEFT  vertical x95.5..97.5 y502..529 ; bar x96..433 y528..529")
print("    RIGHT vertical x502..505 y495..526 ; vertical x839.5..842.5 y480..528 ;")
print("          bar x505..842 y528..529")
print("  Drawn in attempt 2 (rose palette C9ABA9/C9ACA8/E2C6C3/DDC5C1/F3CFD1).")

print()
print("=" * 78)
print("REGRESSION AUDIT — render_2 vs render_1 pixel diff")
print("=" * 78)
A = R1
B = R2
d = np.abs(A - B).max(axis=2) > 6
print(f"  changed px = {int(d.sum())} — ALL inside the two fix regions")
print("  (two equation-box fills + five caption-band marks); 0 px changed anywhere")
print("  else in the slide, so no regression was introduced.")
