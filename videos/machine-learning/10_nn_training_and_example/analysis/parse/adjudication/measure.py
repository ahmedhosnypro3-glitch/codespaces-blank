#!/usr/bin/env python3
"""PIL/numpy measurement rig for doc-parse adjudication of lecture frames.

Numbers only - emits text evidence, never image bytes.
Usage: measure.py <jpg> [parse.md] [json]
"""
import sys, os, json, re
import numpy as np
from PIL import Image
from scipy import ndimage

W, H = 960, 540


def load(path):
    im = Image.open(path).convert("L")
    a = np.asarray(im).astype(np.int16)
    return a


def bg_estimate(a):
    hist, edges = np.histogram(a, bins=64, range=(0, 256))
    k = int(edges[np.argmax(hist)])
    return k


def ink_mask(a, tol=28, bg=None):
    if bg is None:
        bg = bg_estimate(a)
    return (np.abs(a - bg) > tol)


def rgb_stats(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    out = {}
    out["unique_colors_top"] = [
        {"hex": "#%02X%02X%02X" % tuple(int(x) for x in c[:3]), "px": int(n)}
        for c, n in zip(*np.unique(a.reshape(-1, 3), axis=0, return_counts=True))
        if True
    ]
    out["unique_colors_top"] = sorted(
        out["unique_colors_top"], key=lambda d: -d["px"]
    )[:10]
    return out


def bands(mask, min_run=3, gap=4, min_ink=8):
    """Row-bands of ink; column-bands of ink (merged across gaps <= gap px)."""
    rb = {}
    rows = mask.sum(axis=1)
    y0, inband = None, False
    out = []
    for y in range(mask.shape[0]):
        if rows[y] >= min_run:
            if not inband:
                y0, inband = y, True
        elif inband and y - y0 > 0:
            if y - y0 >= min_ink:
                out.append((y0, y))
            inband = False
    if inband and mask.shape[0] - y0 >= min_ink:
        out.append((y0, mask.shape[0]))
    # merge bands separated by <= gap empty rows
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b) if False else (b[0], b[1]))
    return [tuple(m) for m in merged]


def col_bands(mask, min_run=3, gap=6, min_ink=8):
    cols = mask.sum(axis=0)
    out = []
    x0, inb = None, False
    for x in range(mask.shape[1]):
        if cols[x] >= min_run:
            if not inb:
                x0, inb = x, True
        elif inb:
            if x - x0 >= min_ink:
                out.append((x0, x))
            inb = False
    if inb and mask.shape[1] - x0 >= min_ink:
        out.append((x0, mask.shape[1]))
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append((b[0], b[1]))
    return merged


def components(mask, min_px=20):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        px = int((lab[sl] == i + 1).sum())
        if px >= min_px:
            out.append((sl[1].start, sl[0].start, w, h, px))
    out.sort(key=lambda t: (t[1], t[0]))
    return out, n


def region_ink(mask, box):
    x0, y0, x1, y1 = box
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    if sub.size == 0:
        return 0, 0.0, 0, 0
    px = int(sub.sum())
    frac = px / sub.size
    ys, xs = np.where(sub)
    bbox = (
        (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0))
        if px
        else None
    )
    return px, frac, *((bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1) if bbox else (0, 0))


def ink_profile(mask, nx=24, ny=24):
    """Coarse grid of ink density -> 'block map' of where content lives."""
    h, w = mask.shape
    rows = []
    for gy in range(ny):
        r = []
        for gx in range(nx):
            sub = mask[gy * h // ny:(gy + 1) * h // ny, gx * w // nx:(gx + 1) * w // nx]
            r.append(int(round(100 * sub.sum() / sub.size)))
        rows.append(r)
    return rows


def svg_blocks(mask):
    """Connected ink blocks aggregated into visual panels: 12x12 cells joined by dilation."""
    big = ndimage.binary_dilation(mask, np.ones((5, 15)))
    lab, n = ndimage.label(big, structure=np.ones((3, 3)))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        x0, y0, x1, y1 = sl[1].start, sl[0].start, sl[1].stop, sl[0].stop
        sub = mask[y0:y1, x0:x1]
        px = int(sub.sum())
        if px < 200:
            continue
        out.append({"box": (int(x0), int(y0), int(x1), int(y1)), "ink_px": px})
    out.sort(key=lambda d: (d["box"][1], d["box"][0]))
    return out


TOKENTXT = re.compile(r"^(?:<x_[\d.]+><y_[\d.]+>|<x_[\d.]+>)")
CLASS_RE = re.compile(r"<class_([A-Za-z-]+)>")


def extract_text_tokens(md):
    """Every distinct literal string token in the parse with no coords (diagram labels)."""
    lines = [l.strip() for l in md.split("\n") if l.strip()]
    return lines


def coord_points(md):
    pts = []
    for m in re.finditer(r"<x_([\d.]+)><y_([\d.]+)>", md):
        pts.append((float(m.group(1)), float(m.group(2))))
    return pts


def main():
    path = sys.argv[1]
    md_path = sys.argv[2] if len(sys.argv) > 2 else None
    js_path = sys.argv[3] if len(sys.argv) > 3 else None
    print("FILE %s" % path)
    im = Image.open(path)
    print("DIM %dx%d mode=%s" % (im.size[0], im.size[1], im.mode))
    g = load(path)
    bg = bg_estimate(g)
    print("BG_LEVEL %d (dominant gray)" % bg)
    m = ink_mask(g, tol=28, bg=bg)
    print("INK_PX %d / %d = %.4f" % (m.sum(), m.size, m.sum() / m.size))
    rs = rgb_stats(path)
    print("TOP_COLORS " + " ".join("%s:%d" % (c["hex"], c["px"]) for c in rs["unique_colors_top"]))
    rb = bands(m)
    print("ROW_BANDS n=%d" % len(rb))
    for b in rb:
        px, frac, bw, bh = region_ink(m, (0, b[0], W, b[1]))
        print("  band y=%d..%d h=%d ink=%d frac=%.3f" % (b[0], b[1], b[1] - b[0], px, frac))
    cb = col_bands(m)
    print("COL_BANDS n=%d" % len(cb))
    for b in cb:
        print("  colband x=%d..%d w=%d" % (b[0], b[1], b[1] - b[0]))
    bl = svg_blocks(m)
    print("VISUAL_BLOCKS n=%d" % len(bl))
    for b in bl:
        x0, y0, x1, y1 = b["box"]
        print("  block x=%d..%d y=%d..%d w=%d h=%d ink=%d" % (x0, x1, y0, y1, x1 - x0, y1 - y0, b["ink_px"]))
    # badge probe (house chrome): yellow circle top-right
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    yellow = (np.abs(a[:, :, 0] - 249) < 40) & (np.abs(a[:, :, 1] - 249) < 40) & (np.abs(a[:, :, 2] - 196) < 40)
    ys, xs = np.where(yellow)
    if len(ys):
        print("BADGE_YELLOW x=%d..%d y=%d..%d px=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), len(ys)))
    else:
        print("BADGE_YELLOW none")
    red = (np.abs(a[:, :, 0] - 192) < 45) & (np.abs(a[:, :, 1]) < 70) & (np.abs(a[:, :, 2]) < 70)
    ys, xs = np.where(red)
    if len(ys):
        print("FRAME_RED x=%d..%d y=%d..%d px=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), len(ys)))
    print("GRID")
    for r in ink_profile(m):
        print("  " + " ".join("%3d" % v for v in r))
    if md_path and os.path.exists(md_path):
        md = open(md_path).read()
        pts = coord_points(md)
        print("COORD_TOKENS n=%d" % len(pts))
        for (x, y) in pts:
            px, py = int(round(x * W)), int(round(y * H))
            ipx, frac, bw, bh = region_ink(m, (max(0, px - 60), max(0, py - 20), min(W, px + 60), min(H, py + 20)))
            print("  (<x_%s><y_%s>) -> px=(%d,%d) ink_in_120x40win=%d frac=%.3f" % (x, y, px, py, ipx, frac))
        for cm in CLASS_RE.finditer(md):
            print("  CLASS_%s" % cm.group(1))
    if js_path and os.path.exists(js_path):
        try:
            j = json.load(open(js_path))
            print("ENVELOPE finish_reason=%s output_tokens=%s content_len=%d" % (
                j.get("finish_reason"), (j.get("usage") or {}).get("output_tokens"), len(j.get("content") or "")))
        except Exception as e:
            print("ENVELOPE parse-error %s" % e)
    print("END")


if __name__ == "__main__":
    main()
