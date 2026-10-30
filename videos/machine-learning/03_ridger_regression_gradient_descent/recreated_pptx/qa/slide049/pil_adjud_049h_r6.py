#!/usr/bin/env python3
# Round 6: exact contiguous spans of rules/verticals (fix geometry) + top-table paren comps.
import numpy as np
from PIL import Image
from collections import deque

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
H, W = orig.shape[:2]
olum = (orig[:, :, 0] * 299 + orig[:, :, 1] * 587 + orig[:, :, 2] * 114) // 1000
o_ink = olum < 205


def spans(v, off, minlen=30):
    out = []
    x = 0
    n = len(v)
    while x < n:
        if v[x]:
            x2 = x
            gap = 0
            while x2 < n - 1 and gap <= 2:
                x2 += 1
                gap = gap + 1 if not v[x2] else 0
            x2 -= gap
            if x2 - x + 1 >= minlen:
                out.append((off + x, off + x2))
            x = x2 + 1
        else:
            x += 1
    return out


print("--- R6 rule spans (minlen 30, gap-tolerant 2) ---")
for y in (46, 54, 55, 56, 128, 129, 130, 140, 197, 206, 255, 263, 272, 329, 338, 395, 404, 461, 470, 509, 510, 527, 528):
    sp = spans(o_ink[y, 57:903], 57)
    if sp:
        print(f"  y{y}: " + "  ".join(f"x{a}..{b}" for a, b in sp))

print("--- R6 vertical spans (minlen 30) ---")
for x in (70, 71, 274, 275, 850, 851, 852, 853, 854, 855, 856):
    sp = spans(o_ink[40:515, x], 40)
    if sp:
        print(f"  x{x}: " + "  ".join(f"y{a}..{b}" for a, b in sp))


def cc_label(x0, x1, y0, y1, bridge=1):
    sub = o_ink[y0:y1, x0:x1]
    h, w = sub.shape
    d = sub.copy()
    for k in range(1, bridge + 1):
        d[:, k:] |= sub[:, :-k]
        d[:, :-k] |= sub[:, k:]
    seen = np.zeros((h, w), bool)
    comps = []
    for i in range(h):
        for j in range(w):
            if d[i, j] and not seen[i, j]:
                q = deque([(i, j)])
                seen[i, j] = True
                pix = []
                while q:
                    a, b = q.popleft()
                    pix.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < h and 0 <= nb < w and d[na, nb] and not seen[na, nb]:
                                seen[na, nb] = True
                                q.append((na, nb))
                ys = [p[0] for p in pix]
                xs = [p[1] for p in pix]
                comps.append((x0 + min(xs), x0 + max(xs), y0 + min(ys), y0 + max(ys), len(pix)))
    comps.sort(key=lambda c: (c[0], c[2]))
    return comps


print("--- R6 top-table comps x86..232 y74..127 (tall or wide) ---")
for (a, b, c, d, n) in cc_label(86, 232, 74, 127):
    w, h = b - a + 1, d - c + 1
    if h >= 12 or (w >= 6 and h >= 6):
        print(f"  x{a}..{b} y{c}..{d} (w{w} h{h} n{n})")

print("--- R6 aug-table header comps x86..235 y163..177 ---")
for (a, b, c, d, n) in cc_label(86, 235, 163, 177):
    print(f"  x{a}..{b} y{c}..{d} (w{b-a+1} h{d-c+1} n{n})")
