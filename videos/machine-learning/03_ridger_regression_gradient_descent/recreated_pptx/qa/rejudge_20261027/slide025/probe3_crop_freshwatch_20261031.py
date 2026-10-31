#!/usr/bin/env python3
"""Slide025 crop-leg BLOCKER probe: bowl-vs-saddle topology + z-tick ink, crop PNGs direct."""
import numpy as np
from PIL import Image

RJ = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027"
S = f"{RJ}/slide025"
R = np.asarray(Image.open(f"{S}/crop_dense_render.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(f"{S}/crop_dense_orig.png").convert("RGB")).astype(int)
print("crop sizes:", R.shape, O.shape)
if R.shape != O.shape:
    O = np.asarray(Image.open(f"{S}/crop_dense_orig.png").convert("RGB").resize((R.shape[1], R.shape[0]), Image.LANCZOS)).astype(int)
H, W = R.shape[:2]

def stats(name, a):
    sat = a.max(axis=2) - a.min(axis=2)
    colored = sat > 60
    g = a.sum(axis=2)
    dark = g < 240
    # left-spine zone: x in [0, 12% W], full height — z-axis + tick labels live there
    spine = slice(0, int(W*0.12))
    print(f"{name}: size {a.shape[1]}x{a.shape[0]} colored%={100*colored.mean():.1f} "
          f"dark<240={int(dark.sum())} left-spine dark={int(dark[:, spine].sum())} "
          f"center meanRGB=({a[H//2-10:H//2+10, W//2-10:W//2+10, 0].mean():.0f},{a[H//2-10:H//2+10, W//2-10:W//2+10, 1].mean():.0f},{a[H//2-10:H//2+10, W//2-10:W//2+10, 2].mean():.0f})")
    return colored, dark

cR, dR = stats("render", R)
cO, dO = stats("orig  ", O)

# topology: brightness of colored surface vs position. A bowl = dark/blue center, bright rim.
# A saddle = two opposite bright lobes + two dark lobes (diagonal pattern).
def lobe_profile(name, a, colored):
    g = a.sum(axis=2)
    # only colored px
    mask = colored & (g < 700)
    ys, xs = np.where(mask)
    if len(ys) < 100:
        print(name, "too few surface px"); return
    # quadrant means of green channel (jet: low=blue dark, high=yellow bright)
    gh, gw = H//2, W//2
    q = {}
    for k, (yy, xx) in {"TL": (slice(0,gh), slice(0,gw)), "TR": (slice(0,gh), slice(gw,W)),
                        "BL": (slice(gh,H), slice(0,gw)), "BR": (slice(gh,H), slice(gw,W))}.items():
        m = mask[yy, xx]
        q[k] = float(a[yy, xx, 1][m].mean()) if m.sum() else float("nan")
    print(f"{name}: surface green-channel quadrant means TL={q['TL']:.0f} TR={q['TR']:.0f} BL={q['BL']:.0f} BR={q['BR']:.0f} "
          f"(saddle: TL~BR one extreme, TR~BL the other; bowl: center dark, rim bright)")
    # center vs rim
    cy, cx = H//2, W//2
    center = a[cy-15:cy+15, cx-15:cx+15, 1].mean()
    rim = np.concatenate([a[:20, :, 1].ravel(), a[-20:, :, 1].ravel(), a[:, :20, 1].ravel(), a[:, -20:, 1].ravel()]).mean()
    print(f"{name}: center green={center:.0f} rim green={rim:.0f} (bowl: center LOW, rim HIGH)")

lobe_profile("render", R, cR)
lobe_profile("orig  ", O, cO)

# z-tick label ink: small dark clusters in left spine zone, count connected rows with dark ink
def tick_rows(name, dark):
    sp = dark[:, :int(W*0.12)]
    rows = np.where(sp.sum(axis=1) > 0)[0]
    # cluster rows
    clusters = 0
    prev = -10
    for r in rows:
        if r - prev > 3:
            clusters += 1
        prev = r
    print(f"{name}: left-spine dark-ink row clusters (tick/label bands) = {clusters}, total dark px = {int(sp.sum())}")
tick_rows("render", dR)
tick_rows("orig  ", dO)
