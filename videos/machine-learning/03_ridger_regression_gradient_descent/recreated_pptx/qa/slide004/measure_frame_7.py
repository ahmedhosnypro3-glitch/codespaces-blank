#!/usr/bin/env python3
"""Targeted final measurement — pass 7.
Exact ink bboxes for every equation region and every text line, plus cap-height
bands for font sizing. 1px=1pt.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330


def bbox(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())


def report(name, mask, x0, x1, y0, y1):
    bb = bbox(mask, x0, x1, y0, y1)
    if bb:
        print(f"  {name}: x{bb[0]}..{bb[2]} (w{bb[2]-bb[0]+1}), y{bb[1]}..{bb[3]} (h{bb[3]-bb[1]+1})")
    else:
        print(f"  {name}: EMPTY")


print("=== BOX1 (x80..394,y99..222) split: equ region x82..226 vs captions x226..392 ===")
report("EQU combined (L)",  red | blue | dark, 82, 226, 104, 216)
report("EQU red part",       red,               82, 226, 104, 216)
report("EQU dark part",      dark,              82, 226, 104, 216)
report("cap ORIG LABELS red", red,  226, 392, 104, 216)
report("cap FROM TRAIN dark", dark, 226, 392, 150, 216)

print("\n=== BOX2 (x426..744,y99..222) split: equ x428..566 vs captions x566..742 ===")
report("EQU combined (L)", red | blue | dark, 428, 566, 104, 216)
report("EQU red part",     red,              428, 566, 104, 216)
report("EQU dark part",    dark,             428, 566, 104, 216)
report("cap PRED LABELS blue", blue, 566, 742, 104, 216)
report("cap FROM MODEL dark", dark, 566, 742, 150, 216)

print("\n=== Remember (x785..877,y102..151) ===")
report("Remember hdr red", red, 788, 874, 104, 120)
report("norm combined",    red | blue | dark, 788, 874, 120, 148)
report("norm dark",        dark, 788, 874, 120, 148)

print("\n=== Objective (x78..302,y243..301) text only ===")
report("OBJ text dark", dark, 82, 298, 248, 300)
report("OBJ text blue", blue, 82, 298, 248, 300)

print("\n=== Error (x78..486,y307..365) text only ===")
report("ERR dark", dark, 82, 482, 312, 360)
report("ERR blue", blue, 82, 482, 312, 360)
report("ERR red",  red,  82, 482, 312, 360)

print("\n=== PredWhere red box (x494..884,y232..371): 4 lines ===")
# line1 Ŷ=XW + Predicted, line2 Where:, line3 X..., line4 Y..., line5 W...
report("PW L1 (240..278)", red | blue | dark, 498, 880, 240, 278)
report("PW L2 (280..305)", red | blue | dark, 498, 880, 280, 305)
report("PW L3 (308..340)", red | blue | dark, 498, 880, 308, 340)
report("PW L4 (343..364)", red | blue | dark, 498, 880, 343, 364)
report("PW red part", red, 498, 880, 240, 364)
report("PW blue part", blue, 498, 880, 240, 364)

print("\n=== Define salmon (x78..655,y388..444) text ===")
report("DEFINE dark", dark, 82, 650, 392, 440)
report("DEFINE red",  red,  82, 650, 392, 440)
report("DEFINE blue", blue, 82, 650, 392, 440)

print("\n=== Formula blue box (x78..486,y462..522) text ===")
report("FORMULA dark", dark, 82, 482, 466, 518)
report("FORMULA red",  red,  82, 482, 466, 518)

print("\n=== TITLE precise color-split ===")
report("TITLE dark", dark, 280, 672, 60, 100)
report("TITLE red",  red,  280, 672, 60, 100)
report("TITLE blue", blue, 280, 672, 60, 100)
