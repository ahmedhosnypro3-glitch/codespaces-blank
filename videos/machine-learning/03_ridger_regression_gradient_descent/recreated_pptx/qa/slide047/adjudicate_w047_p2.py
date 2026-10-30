#!/usr/bin/env python3
"""Slide 047 adjudication part 2: class-row colours, augmented row count, W vector."""
import numpy as np
from PIL import Image

P = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
LUM = (R + G + B) / 3
out = []


def say(*ls):
    for ln in ls:
        out.append(ln)


def runs(mask, min_len=1):
    res, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            if j - i + 1 >= min_len:
                res.append((i, j))
            i = j + 1
        else:
            i += 1
    return res


def cluster_cols(x0, x1, y0, y1, min_gap=6):
    """Group ink columns into clusters separated by >= min_gap blank px."""
    prof = LUM[y0 : y1 + 1, x0 : x1 + 1].min(axis=0) < 220
    rs = runs(prof)
    groups, cur = [], None
    for s, e in rs:
        if cur is None:
            cur = [s, e]
        elif s - cur[1] - 1 < min_gap:
            cur[1] = e
        else:
            groups.append(tuple(cur))
            cur = [s, e]
    if cur:
        groups.append(tuple(cur))
    return [(x0 + s, x0 + e) for s, e in groups]


def cluster_rows(x0, x1, y0, y1, min_gap=3):
    prof = LUM[y0 : y1 + 1, x0 : x1 + 1].min(axis=1) < 220
    rs = runs(prof)
    groups, cur = [], None
    for s, e in rs:
        if cur is None:
            cur = [s, e]
        elif s - cur[1] - 1 < min_gap:
            cur[1] = e
        else:
            groups.append(tuple(cur))
            cur = [s, e]
    if cur:
        groups.append(tuple(cur))
    return [(y0 + s, y0 + e) for s, e in groups]


def core(x0, x1, y0, y1):
    band = a[y0 : y1 + 1, x0 : x1 + 1].reshape(-1, 3)
    lum = LUM[y0 : y1 + 1, x0 : x1 + 1].ravel()
    thr = np.percentile(lum, 10)
    sel = band[lum <= max(thr, 1)]
    if sel.size == 0:
        return None
    return tuple(int(v) for v in np.median(sel, axis=0))


# ---- 1. top-left class row: cluster the 6 label cells, colour each
say("## A. TOP-LEFT class row: cluster columns in the class band, core colour per cluster")
for (s, e) in cluster_cols(84, 222, 112, 124, min_gap=7):
    c = core(s, e, 112, 124)
    hue = "RED" if c and c[0] - c[1] > 30 and c[0] - c[2] > 40 else (
        "BLUE" if c and c[2] - c[0] > 20 else "?")
    say(f"  x{s}..{e} (w{e - s + 1}): core={c} -> {hue}")

# ---- 2. augmented matrix: cluster text rows in the interior only
say("\n## B. AUGMENTED matrix interior (x84..240, y141..255): row clusters")
rows = cluster_rows(84, 240, 141, 255, min_gap=4)
for (s, e) in rows:
    say(f"  y{s}..{e} (h{e - s + 1})")
say(f"  => {len(rows)} row clusters")

# ---- 2b. augmented class band colour clusters
say("\n## B2. AUGMENTED class row (y226..246): column clusters + colours")
for (s, e) in cluster_cols(84, 240, 228, 244, min_gap=7):
    c = core(s, e, 228, 244)
    hue = "RED" if c and c[0] - c[1] > 30 and c[0] - c[2] > 40 else (
        "BLUE" if c and c[2] - c[0] > 20 else "?")
    say(f"  x{s}..{e}: core={c} -> {hue}")

# ---- 3. W vector: profile the DIGIT column only (inside parens)
say("\n## C. INITIAL W vector: row clusters of the digit column x333..349, y58..106")
for (s, e) in cluster_rows(333, 349, 58, 106, min_gap=3):
    say(f"  y{s}..{e} (h{e - s + 1})")
say("  plus paren extents: left paren col profile x322..332:")
prof = LUM[56:110, 322:333].min(axis=0) < 220
say(f"    ink col runs x322..332: {[(322 + s, 322 + e) for s, e in runs(prof)]}")

# ---- 4. header glyph check for top-left matrix (x1..x6 lowercase italic?)
say("\n## D. TOP-LEFT matrix header band y60..72 x84..222 ASCII")
t = LUM[60:74, 84:224]
for yy in range(14):
    say(f"  y{60+yy:3d}|" + "".join("#" if t[yy, xx] < 200 else "." for xx in range(140)) + "|")

# ---- 5. badge + panel + strokes sanity (house chrome, quick)
say("\n## E. quick chrome sanity")
say(f"  panel sample (200,300): {tuple(a[300, 200])}")
say(f"  left stroke col x57..60 at y300: {[tuple(a[300, xx]) for xx in range(57, 61)]}")
say(f"  right stroke col x900..903 at y300: {[tuple(a[300, xx]) for xx in range(900, 904)]}")
say(f"  bottom row y536..539 at x500: {[tuple(a[yy, 500]) for yy in range(536, 540)]}")
say(f"  top band y46..48 at x500 (must NOT be red): {[tuple(a[yy, 500]) for yy in range(46, 49)]}")

open("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/adjudicate_w047_p2.txt", "w").write("\n".join(out))
print("\n".join(out))
