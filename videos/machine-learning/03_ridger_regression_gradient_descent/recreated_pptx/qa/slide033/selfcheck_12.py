#!/usr/bin/env python3
"""Attempt-11 self-check (re-targeted from render_6): verify the corrected band geometry in render_12.png
against the ORIGINAL frame (960x540, 1px=1pt).

Compares, per band, the modal colour and the y-extent on both sides, and checks
that the label column (x86-121) is filled on the render too.
"""
from PIL import Image
import numpy as np, collections

D = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{D}/unique_slides/slide_033.jpg"
REND = f"{D}/recreated_pptx/qa/slide033/render_12.png"
SX, SY = 2001 / 960, 1125 / 540

BANDS = [
    ("D9E275", 217, 226, 119, 334, 367),
    ("D6B2F5", 214, 178, 248, 376, 408),
    ("F7DDC2", 247, 221, 194, 420, 452),
    ("DEAC95", 222, 172, 149, 463, 472),
    ("F7BEC4", 247, 190, 196, 486, 500),
]
LABEL_E9FFD2 = (233, 255, 210)

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)


def modal(img, y0, y1, x0, x1):
    c = collections.Counter()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1, 2):
            c[tuple(img[y, x])] += 1
    return c.most_common(1)[0][0]


ok = True
for name, R, G, B, y0, y1 in BANDS:
    om = modal(o, y0, y1, 130, 860)
    # render: convert frame coords to render px
    ry0, ry1 = int(round(y0 * SY)), int(round((y1 + 1) * SY))
    rx0, rx1 = int(round(130 * SX)), int(round(860 * SX))
    rm = modal(r, ry0, ry1, rx0, rx1)
    d_data = max(abs(a - b) for a, b in zip(om, rm))
    # label column
    ol = modal(o, y0, y1, 90, 118)
    rl = modal(r, ry0, ry1, int(round(90 * SX)), int(round(118 * SX)))
    d_label = max(abs(a - b) for a, b in zip(ol, rl))
    want_label = LABEL_E9FFD2 if name == "DEAC95" else (R, G, B)
    d_lbl_want = max(abs(a - b) for a, b in zip(rl, want_label))
    status = "OK" if (d_data <= 6 and d_label <= 6) else "FAIL"
    if status == "FAIL": ok = False
    print(f"{name} y{y0}-{y1}: data orig {om} render {rm} |maxdiff {d_data}| ; "
          f"label orig {ol} render {rl} |maxdiff {d_label}| ; label-vs-expected {d_lbl_want}  -> {status}")

print()
print("SELFCHECK:", "PASS" if ok else "FAIL")
