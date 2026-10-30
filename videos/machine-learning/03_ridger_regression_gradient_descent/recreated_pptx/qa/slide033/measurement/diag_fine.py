#!/usr/bin/env python3
"""Fine ASCII dump of specific regions of the original frame."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)

def cls(pp):
    R, G, B = pp
    s = max(R, G, B) - min(R, G, B)
    if s < 25:
        if max(R, G, B) > 240: return ' '
        if max(R, G, B) < 110: return '#'
        return '.'
    if R == max(R, G, B):
        if G > 150 and B < 120: return 'Y'
        if G > 100 and B > 130: return 'P'
        return 'R'
    if G == max(R, G, B):
        return 'C' if B > 150 else 'G'
    return 'P' if R > 150 else 'B'

def dump(name, x0, y0, x1, y1, cell=5):
    print(f"=== {name}: x{x0}-{x1} y{y0}-{y1} (cell {cell}px) ===")
    hdr = "      " + "".join(str(((x0 + i * cell) // 100) % 10) for i in range((x1 - x0) // cell))
    print(hdr)
    for yy in range(y0, y1, cell):
        line = ""
        for xx in range(x0, x1, cell):
            blk = o[yy:yy + cell, xx:xx + cell].reshape(-1, 3)
            fg = Counter(cls(tuple(p)) for p in blk)
            # count background as whitespace
            n_fg = sum(v for k, v in fg.items() if k != ' ')
            n_dot = fg.get('.', 0)
            if n_fg == 0:
                line += ' ' if n_dot < len(blk) * 0.5 else '.'
            else:
                line += cls(tuple(blk[np.argmax(np.array([ (cls(tuple(p)) != ' ') for p in blk]))]))
        print(f"{yy:>5} {line}")
    print()

dump("TITLE+SUBTITLE area", 50, 55, 520, 150, 5)
dump("CENTER column (formula?)", 130, 115, 480, 305, 5)
dump("PLOT region", 600, 110, 935, 335, 5)
dump("PARAMETER BOX area", 50, 230, 200, 315, 5)
dump("TABLE top rows", 20, 320, 940, 380, 5)
dump("TABLE mid rows", 20, 375, 940, 460, 5)
dump("TABLE bottom rows", 20, 455, 940, 525, 5)
