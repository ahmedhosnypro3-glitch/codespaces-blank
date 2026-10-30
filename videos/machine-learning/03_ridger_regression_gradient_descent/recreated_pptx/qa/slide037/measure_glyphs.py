#!/usr/bin/env python3
"""Precise per-glyph ink extents in original vs render, from narrow column windows
so each window isolates one glyph."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_037.jpg"
R = np.asarray(Image.open(f"{QA}/render_3.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
s = R.shape[0] / 540.0


def ink(a):
    return (a.sum(axis=2) < 430)


IR, IO = ink(R), ink(O)


def gbox(mask, c0, c1, r0, r1, scale):
    sub = mask[int(r0 * scale):int(r1 * scale), int(c0 * scale):int(c1 * scale)]
    rows = np.where(sub.any(axis=1))[0]
    cols = np.where(sub.any(axis=0))[0]
    if not len(rows):
        return None
    return (
        round((rows.min() + r0 * scale) / scale, 1), round((rows.max() + r0 * scale) / scale, 1),
        round((cols.min() + c0 * scale) / scale, 1), round((cols.max() + c0 * scale) / scale, 1),
    )


# (label, col window, row band) — windows chosen to isolate single glyphs
PROBES_O = [
    ("head 'D'", 78, 91, 110, 145),
    ("head 'e' 1st", 99, 113, 110, 145),
    ("head delta", 160, 178, 110, 145),
    ("head 'a'", 138, 150, 110, 145),
    ("head 's'", 160, 178, 110, 145),
    ("impl1 'I'", 77, 90, 140, 180),
    ("impl1 'f'", 128, 145, 140, 180),
    ("impl1 'h'", 250, 268, 140, 180),
    ("impl1 'd'", 168, 180, 140, 180),
    ("impl2 'I'", 77, 90, 168, 200),
    ("impl2 'h'", 252, 272, 168, 200),
    ("p2head 'R'", 75, 92, 238, 265),
    ("p2head 'd'", 120, 136, 238, 265),
    ("p2head 'f'", 155, 172, 238, 265),
    ("sumline 'S'", 75, 92, 305, 332),
    ("sumline 'u'", 118, 134, 305, 332),
    ("p3head 'M'", 81, 100, 356, 388),
    ("p3head 'G'", 175, 195, 356, 388),
    ("p3head 'D'", 220, 240, 356, 388),
    ("p3head 'w'", 380, 400, 356, 388),
    ("upd1 'W'", 81, 100, 400, 445),
    ("upd1 'u'", 103, 120, 400, 445),
    ("upd2 'W'", 79, 100, 466, 508),
    ("title 'P'", 354, 372, 60, 90),
    ("title 'b'", 560, 578, 60, 90),
    ("title 'B'", 614, 630, 60, 90),
]
print("%-18s %-26s %-26s" % ("probe", "ORIGINAL (r0,r1,c0,c1)", "RENDER"))
for label, c0, c1, r0, r1 in PROBES_O:
    ob = gbox(IO, c0, c1, r0, r1, 1.0)
    rb = gbox(IR, c0, c1, r0, r1, s)
    oh = (ob[1] - ob[0] + 1) if ob else None
    rh = (rb[1] - rb[0] + 1) if rb else None
    ow = (ob[3] - ob[2] + 1) if ob else None
    rw = (rb[3] - rb[2] + 1) if rb else None
    print("%-18s o=%-22s h=%-5s w=%-5s  r=%-22s h=%-5s w=%-5s" % (label, ob, oh, ow, rb, rh, rw))
