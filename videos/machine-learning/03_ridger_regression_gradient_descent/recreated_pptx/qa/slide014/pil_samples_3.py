#!/usr/bin/env python3
"""Decisive per-row band sampler for slide_014.
For each sample y (frame-px), print every contiguous uniform colour run >=100
frame-px wide, for BOTH images. Frame space 960x540; render /2.084375.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")
S = 2001.0 / 960.0
MIN = 100  # frame-px

REGIONS = [
    ("RIDGE band", [250, 260, 275, 279]),
    ("OBJECTIVE band", [310, 315, 320, 333]),
    ("MID band1 (peach)", [355, 365, 375, 386]),
    ("MID band2/3", [405, 410, 420, 440]),
    ("LOWER blue", [470, 480, 500, 520, 524]),
    ("RIGHT BOX top", [110, 130, 200, 230]),
]


def runs_at(px, W, y, scale):
    out = []
    x = 0
    while x < W:
        c = px[x, y]
        x2 = x
        while x2 + 1 < W and (
            abs(px[x2 + 1, y][0] - c[0]) <= 5
            and abs(px[x2 + 1, y][1] - c[1]) <= 5
            and abs(px[x2 + 1, y][2] - c[2]) <= 5
        ):
            x2 += 1
        w = (x2 - x + 1) / scale
        if w >= MIN:
            out.append((round(x / scale, 1), round(x2 / scale, 1), round(w, 1), c))
        x = x2 + 1
    return out


def main():
    for label, ys in REGIONS:
        print("\n########## %s ##########" % label)
        for fy in ys:
            print("  --- frame y=%d ---" % fy)
            for name, path, sc in (("ORIG   ", SRC, 1.0), ("RENDER ", os.path.join(HERE, "render_3.png"), S)):
                im = Image.open(path).convert("RGB")
                px = im.load()
                W, H = im.size
                y = min(H - 1, int(fy * sc))
                rs = runs_at(px, W, y, sc)
                if not rs:
                    print("    %s (no run >=%d)" % (name, MIN))
                for (a, b, w, c) in rs:
                    print("    %s x %6.1f..%6.1f  w=%6.1f  fill=%s" % (name, a, b, w, c))
            im = None


if __name__ == "__main__":
    main()
