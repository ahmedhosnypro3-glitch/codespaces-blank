#!/usr/bin/env python3
"""Definitive paren-direction probe.

Per 600-dpi band image: auto-detect the two tall thin paren clusters by
ink-row count, exclude horizontal-bar rows (eq lines) from the belly
estimate, then compare tip x vs belly x. '(' => tips RIGHT of belly.
')' => tips LEFT of belly. Reports per media file with its slide y-offset
parsed from the pptx XML.
"""
import glob
import re
import sys
import zipfile
import numpy as np
from PIL import Image
from xml.etree import ElementTree as ET

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def media_map(pptx, slide_xml="ppt/slides/slide1.xml"):
    """[(media_path, off_y_emu)] for every pic on the slide, in document order."""
    out = []
    with zipfile.ZipFile(pptx) as z:
        root = ET.fromstring(z.read(slide_xml))
        rels = ET.fromstring(z.read("ppt/slides/_rels/slide1.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        for pic in root.iter(f"{{{NS['p']}}}pic"):
            blip = pic.find(f".//{{{NS['a']}}}blip")
            off = pic.find(f".//{{{NS['a']}}}off")
            rid = blip.get(f"{{{NS['r']}}}embed") if blip is not None else None
            y = int(off.get("y")) if off is not None else -1
            tgt = rmap.get(rid, "?")
            import posixpath
            tgt = posixpath.normpath(posixpath.join("ppt/slides", tgt))
            out.append((tgt, y))
    return out


def probe_asset(path, label):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)[:, :, 3].astype(int)
    H, W = a.shape
    colcount = (a > 64).sum(axis=0)
    tall = np.where(colcount > 0.45 * H)[0]  # paren strokes span >=45% of height
    if len(tall) == 0:
        print(f"{label}: no tall ink clusters")
        return
    clusters, start = [], tall[0]
    for i in range(1, len(tall)):
        if tall[i] != tall[i - 1] + 1:
            clusters.append((start, tall[i - 1]))
            start = tall[i]
    clusters.append((start, tall[-1]))
    clusters = [c for c in clusters if c[1] - c[0] <= 60]  # thin strokes only
    verdicts = []
    for cx0, cx1 in clusters:
        win = a[:, cx0:cx1 + 1]
        rows = np.where(win.max(axis=1) > 64)[0]
        r0, r1 = rows.min(), rows.max()
        # eq-bar rows: ink extending well beyond this cluster's columns
        row_maxcol = np.array([np.where(win[y] > 64)[0].max() if (win[y] > 64).any() else -1
                               for y in range(H)])
        bar_rows = set(np.where(row_maxcol > (cx1 - cx0) + 6)[0])
        span = r1 - r0
        mid0, mid1 = r0 + span // 3, r0 + 2 * span // 3
        belly_rows = [y for y in range(mid0, mid1 + 1) if y not in bar_rows]
        tip_rows = list(range(r0, min(r0 + 8, r1))) + list(range(max(r1 - 8, r0), r1 + 1))
        tip_rows = [y for y in tip_rows if y not in bar_rows]
        if not belly_rows or not tip_rows:
            verdicts.append(f"x[{cx0}..{cx1}]: UNRESOLVED (bar overlap)")
            continue
        bx = [np.where(win[y] > 64)[0].mean() for y in belly_rows]
        tx = [np.where(win[y] > 64)[0].mean() for y in tip_rows]
        bc, tc = float(np.mean(bx)) + cx0, float(np.mean(tx)) + cx0
        shape = "(" if tc > bc + 2.5 else (")" if tc < bc - 2.5 else "??")
        verdicts.append(
            f"x[{cx0}..{cx1}] rows[{r0}..{r1}] belly_c={bc:.1f} tip_c={tc:.1f} => {shape}"
            f"{'  <-- MIRRORED' if (cx0 < W / 2 and shape == ')') or (cx0 > W / 2 and shape == '(') else ''}")
    print(f"{label}:")
    for v in verdicts:
        print("  " + v)


def probe_original(path, label):
    im = Image.open(path).convert("L")
    a = np.array(im, dtype=float)
    ink = a < 200
    colcount = ink.sum(axis=0)
    H = a.shape[0]
    out = []
    for x0, x1, tag in [(553, 565, "L"), (598, 612, "R")]:
        sub = colcount[x0:x1 + 1]
        cols = np.where(sub >= 40)[0] + x0  # paren = >=40 ink rows in its columns
        if len(cols) == 0:
            out.append(f"  {tag}: no tall column in x[{x0}..{x1}]")
            continue
        cx0, cx1 = cols.min(), cols.max()
        win = ink[:, cx0:cx1 + 1]
        rows = np.where(win.any(axis=1))[0]
        # keep the longest contiguous row run (the paren stroke)
        runs, s = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] != rows[i - 1] + 1:
                runs.append((s, rows[i - 1]))
                s = rows[i]
        runs.append((s, rows[-1]))
        r0, r1 = max(runs, key=lambda t: t[1] - t[0])
        span = r1 - r0
        mid0, mid1 = r0 + span // 3, r0 + 2 * span // 3
        row_maxcol = np.array([np.where(win[y])[0].max() if win[y].any() else -1 for y in range(H)])
        bar_rows = set(np.where(row_maxcol > (cx1 - cx0) + 4)[0])
        belly_rows = [y for y in range(mid0, mid1 + 1) if y not in bar_rows]
        tip_rows = [y for y in list(range(r0, r0 + 4)) + list(range(r1 - 3, r1 + 1)) if y not in bar_rows]
        if not belly_rows or not tip_rows:
            out.append(f"  {tag} x[{cx0}..{cx1}] rows[{r0}..{r1}]: UNRESOLVED")
            continue
        bx = float(np.mean([np.where(win[y])[0].mean() for y in belly_rows])) + cx0
        tx = float(np.mean([np.where(win[y])[0].mean() for y in tip_rows])) + cx0
        shape = "(" if tx > bx + 1.0 else (")" if tx < bx - 1.0 else "??")
        out.append(f"  {tag} x[{cx0}..{cx1}] rows[{r0}..{r1}] belly_c={bx:.2f} tip_c={tx:.2f} => {shape}"
                   f"{'  <-- MIRRORED' if (tag == 'L' and shape == ')') or (tag == 'R' and shape == '(') else ''}")
    print(f"{label}:")
    print("\n".join(out))


if __name__ == "__main__":
    base = "videos/machine-learning/03_ridger_regression_gradient_descent"
    for n in ("017", "018", "013"):
        pptx = f"{base}/recreated_pptx/slide_{n}_recreated.pptx"
        print(f"=== slide {n} certified pptx media ===")
        for media, y_emu in media_map(pptx):
            with zipfile.ZipFile(pptx) as z:
                data = z.read(media)
            tmp = f"scratch/tmp_media_{n}_{media.split('/')[-1]}"
            open(tmp, "wb").write(data)
            y_slide = y_emu / 914400 * 600 if y_emu >= 0 else -1
            probe_asset(tmp, f"  {media.split('/')[-1]} off_y={y_slide:.1f} slide px")
    print("=== originals ===")
    for n in ("013", "017", "018"):
        probe_original(f"{base}/unique_slides/slide_{n}.jpg", f"  slide_{n}.jpg")
