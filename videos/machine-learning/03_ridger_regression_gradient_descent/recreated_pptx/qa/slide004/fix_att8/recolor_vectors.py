#!/usr/bin/env python3
"""Recolor slide 004 equation assets to match the original's ink colors.

Original (PIL-measured, unique_slides/slide_004.jpg):
  Yvec     lead-in "Let Y =" black x86..149; vector+subscript RED x158..208
  Yhatvec  lead-in "Let Yh =" black x432..494; vector+subscript RED x504..554
  formula  "Loss =" RED x94..131; body black x136..392

Asset cut points are in ASSET column space (assets have their own internal
layout; cuts sit in measured ink gaps):
  eq_004_Yvec.png     952x357  lead-in ink ends x410, vector starts x459 -> cut 435 (x>=435 red)
  eq_004_Yhatvec.png  894x433  lead-in ink ends x357, vector starts x405 -> cut 380 (x>=380 red)
  eq_004_formula.png  1841x168 "Loss =" ink ends x363, body starts x414  -> cut 388 (x<=388 red)

RGB -> (255,0,0); alpha bytes untouched.
"""
from hashlib import md5
from pathlib import Path

import numpy as np
from PIL import Image

A = Path(__file__).resolve().parents[3] / "build" / "assets"
OUT = Path(__file__).resolve().parent

JOBS = [
    ("eq_004_Yvec.png", 435, "right"),
    ("eq_004_Yhatvec.png", 380, "right"),
    ("eq_004_formula.png", 388, "left"),
]

RED = np.array([255, 0, 0], dtype=np.uint8)


def md5_of(p):
    return md5(p.read_bytes()).hexdigest()


def main():
    log = []
    for name, cut, side in JOBS:
        p = A / name
        before = md5_of(p)
        im = Image.open(p).convert("RGBA")
        a = np.asarray(im).copy()
        rgb, alpha = a[..., :3], a[..., 3]
        ink = alpha > 0
        cols = np.nonzero(ink.any(axis=0))[0]
        ink_before = int(ink.sum())
        if side == "right":
            sel = ink & (np.arange(a.shape[1])[None, :] >= cut)
        else:
            sel = ink & (np.arange(a.shape[1])[None, :] <= cut)
        rgb[sel] = RED
        out = Image.fromarray(a, "RGBA")
        out.save(p)
        after = md5_of(p)
        # post-save classification
        b = np.asarray(Image.open(p).convert("RGBA"))
        r, g, bl, al = b[..., 0].astype(int), b[..., 1].astype(int), b[..., 2].astype(int), b[..., 3]
        vis = al > 0
        redm = vis & (r > 150) & (g < 130) & (bl < 130)
        darkm = vis & ~redm
        rys, rxs = np.nonzero(redm)
        dys, dxs = np.nonzero(darkm)
        line = (
            f"{name}: cut={cut}({side}) md5 {before[:8]}..->{after[:8]}.. ink {ink_before}->{int(vis.sum())} "
            f"red n={int(redm.sum())}"
            + (f" x{rxs.min()}..{rxs.max()}" if redm.sum() else "")
            + f" | dark n={int(darkm.sum())}"
            + (f" x{dxs.min()}..{dxs.max()}" if darkm.sum() else "")
        )
        print(line)
        log.append(line)
    (OUT / "recolor_vectors.out.txt").write_text("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
