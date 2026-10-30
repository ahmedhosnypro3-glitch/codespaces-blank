#!/usr/bin/env python3
"""Rebuild eq_004_Yvec/Yhatvec from the ORIGINAL's measured geometry (attempt 9).

Adjudication evidence (qa/slide004, probe8k/8e/8l + this script's measurements):
  - delimiters are thin straight VERTICAL BARS (orig x158-160/x183-185 left,
    x504-505/x529-531 right), not parentheses -> att8 let_boxes MAJOR-1
  - lead symbol carries a black hairline underline (Y y159-160 x121-135,
    Yhat y165 x466-477) -> att8 let_boxes MAJOR-2
  - dimension subscript reads uppercase N x 1, BLACK ink (not red)
  - original matrix is ~104-106 frame px tall (entry pitch ~25px) vs the
    mathtext substack's ~50px -> uniform scaling cannot match both glyph size
    and pitch, so the asset is PIL-COMPOSED at measured positions:
    lead-in + underline (mathtext piece), bars (drawn lines), entries
    (individually placed mathtext pieces), subscript (mathtext piece).
Output: assets/eq_004_{Yvec,Yhatvec}.png + .json (600dpi, placement contract
w=w_px/600*72? no - frame px = pt: place at x=origin_x/72 in, w=canvas_w/72 in).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "build"))
import render_eq  # noqa: E402  (certified mathtext->PNG renderer)

DECK = Path(__file__).resolve().parents[3]
ORIG = DECK / "unique_slides" / "slide_004.jpg"
ASSETS = DECK / "recreated_pptx" / "build" / "assets"
DPI = 600
S = DPI / 72.0  # asset px per frame px (frame px == pt)

RED = (255, 0, 0)
BLACK = (0, 0, 0)

im = np.asarray(Image.open(ORIG).convert("RGB"))
g = im.astype(int).sum(axis=2)


def ink_runs_rows(x0, x1, y0, y1, thr=690, gap=3):
    rows = np.where((g[y0:y1, x0:x1] < thr).any(axis=1))[0] + y0
    runs = []
    if len(rows):
        s = p = rows[0]
        for r in rows[1:]:
            if r > p + gap:
                runs.append((int(s), int(p)))
                s = r
            p = r
        runs.append((int(s), int(p)))
    return runs


def ink_cols(y0, y1, x0, x1, thr=690, gap=4):
    cols = np.where((g[y0:y1, x0:x1] < thr).any(axis=0))[0] + x0
    runs = []
    if len(cols):
        s = p = cols[0]
        for c in cols[1:]:
            if c > p + gap:
                runs.append((int(s), int(p)))
                s = c
            p = c
        runs.append((int(s), int(p)))
    return runs


def render_piece(latex, fontsize, color):
    """mathtext piece -> tight RGBA np array + ink bbox, at DPI."""
    c01 = tuple(v / 255.0 for v in color[:3])
    info = render_eq.render(latex, "/tmp/_piece_004.png", fontsize, c01)
    a = np.asarray(Image.open("/tmp/_piece_004.png").convert("RGBA"))
    alpha = a[:, :, 3]
    rows = np.where((alpha > 8).any(axis=1))[0]
    cols = np.where((alpha > 8).any(axis=0))[0]
    return a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1], info


def fit_piece(latex, color, target_w=None, target_h=None, fs_lo=6.0, fs_hi=30.0):
    """bisect fontsize so the piece's tight ink height (or width) hits target."""
    best = None
    for _ in range(18):
        fs = (fs_lo + fs_hi) / 2
        a, info = render_piece(latex, round(fs, 2), color)
        h = a.shape[0] / S
        w = a.shape[1] / S
        best = (round(fs, 2), a, w, h)
        if target_h is not None:
            if h < target_h:
                fs_lo = fs
            else:
                fs_hi = fs
        else:
            if w < target_w:
                fs_lo = fs
            else:
                fs_hi = fs
    return best


def paste(canvas, piece, cx_frame, cy_frame):
    """paste piece ink centered at (cx, cy) frame coords (relative to canvas)."""
    ph, pw = piece.shape[:2]
    x0 = int(round(cx_frame * S - pw / 2))
    y0 = int(round(cy_frame * S - ph / 2))
    ah, aw = canvas.shape[:2]
    xs0, ys0 = max(x0, 0), max(y0, 0)
    xs1, ys1 = min(x0 + pw, aw), min(y0 + ph, ah)
    if xs1 <= xs0 or ys1 <= ys0:
        raise SystemExit("piece fully outside canvas")
    sub = piece[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    a = sub[:, :, 3:4].astype(float) / 255.0
    canvas[ys0:ys1, xs0:xs1, :3] = (
        sub[:, :, :3] * a + canvas[ys0:ys1, xs0:xs1, :3] * (1 - a)
    ).astype(np.uint8)
    canvas[ys0:ys1, xs0:xs1, 3:] = np.maximum(
        canvas[ys0:ys1, xs0:xs1, 3:], sub[:, :, 3:]
    )


def draw_paren(canvas, x_apex_frame, x_end_frame, y0_frame, y1_frame):
    """Thin curved delimiter: 2-frame-px stroke, bow = x_end - x_apex.
    '(' apex (leftmost) at mid-span; ')' apex (rightmost) at mid-span —
    matches the original's measured profiles (L box: 160@104→158@156→160@208)."""
    y0a, y1a = int(round(y0_frame * S)), int(round(y1_frame * S))
    ymid, half = (y0a + y1a) / 2.0, (y1a - y0a) / 2.0
    xa, xe = x_apex_frame * S, x_end_frame * S
    stroke = max(2, int(round(2 * S)))
    H, W = canvas.shape[:2]
    for ya in range(y0a, y1a + 1):
        t = (ya - ymid) / half
        xi = int(round(xa + (xe - xa) * t * t))
        for xx in range(xi, min(xi + stroke, W)):
            if 0 <= xx < W:
                canvas[ya, xx, 0] = RED[0]
                canvas[ya, xx, 1] = RED[1]
                canvas[ya, xx, 2] = RED[2]
                canvas[ya, xx, 3] = 255


def build_box(tag, lead_tex, entries, bars_x, box, sub_black=True, sub_box=None,
              lead_x0=None):
    """Compose one Let-box asset. box = (x0,y0,x1,y1) frame-px canvas bounds.
    sub_box = measured subscript bbox (dynamic search is polluted by the
    caption text sharing the band right of the bars)."""
    x0, y0, x1, y1 = box
    cw, ch = int(round((x1 - x0) * S)), int(round((y1 - y0) * S))
    canvas = np.zeros((ch, cw, 4), dtype=np.uint8)

    # --- measured geometry from the original ---
    # lead-in ink bbox (search left of the first bar)
    lead_cols = ink_cols(y0 + 30, y1 - 10, lead_x0 if lead_x0 else x0,
                         min(bars_x[0] - 6, x1), gap=6)
    lx0, lx1 = lead_cols[0][0], lead_cols[-1][1]
    lead_rows = ink_runs_rows(lx0, lx1, y0, y1)
    ly0 = min(r[0] for r in lead_rows)
    ly1 = max(r[1] for r in lead_rows)
    print(f"[{tag}] lead ink x{lx0}..{lx1} y{ly0}..{ly1} (w={lx1-lx0} h={ly1-ly0})")

    # matrix bars vertical extent (column band around each bar)
    bar_spans = []
    for bx in bars_x:
        rr = ink_runs_rows(bx - 2, bx + 3, y0 + 2, y1 - 2, gap=6)
        span = max(rr, key=lambda r: r[1] - r[0])
        bar_spans.append(span)
    my0 = min(s[0] for s in bar_spans)
    my1 = max(s[1] for s in bar_spans)
    print(f"[{tag}] bars at x{bars_x} span y{my0}..{my1}")

    # entry rows between the bars
    er = ink_runs_rows(bars_x[0] + 4, bars_x[1] - 4, my0, my1, gap=4)
    print(f"[{tag}] entry rows {er}")

    # subscript bbox — measured on the original (see sub_box docstring);
    # ink there is RED (darkest (137,52,57)/(143,49,67)), same red family
    # as bars/entries — the earlier BLACK claim is contradicted by the frame
    sx0, sy0, sx1, sy1 = sub_box
    print(f"[{tag}] subscript (measured) x{sx0}..{sx1} y{sy0}..{sy1}")

    # --- lead piece (black, includes underline) ---
    fs, lead, lw, lh = fit_piece(lead_tex, BLACK, target_h=(ly1 - ly0))
    print(f"[{tag}] lead fontsize {fs} natural {lw:.1f}x{lh:.1f} frame px")
    paste(canvas, lead, (lx0 - x0 + lw / 2), (ly0 - y0 + lh / 2))

    # --- delimiters: round parentheses (measured bow ~2px; the att8
    # "straight bars" reading is refuted by the 1px profile map) ---
    for k, (bx, span) in enumerate(zip(bars_x, bar_spans)):
        by0, by1 = span
        if k == 0:    # '(' apex leftmost at middle
            draw_paren(canvas, bx - 1 - x0, bx + 1 - x0, by0 - y0, by1 - y0)
        else:         # ')' apex rightmost at middle
            draw_paren(canvas, bx + 1 - x0, bx - 1 - x0, by0 - y0, by1 - y0)

    # --- entries (red) ---
    for (run, tex) in zip(er, entries):
        cyc = (run[0] + run[1]) / 2 - y0
        if "cdots" in tex:
            fs_e, piece, pw, ph = fit_piece(tex, RED, target_w=14.0)
        else:
            fs_e, piece, pw, ph = fit_piece(tex, RED, target_h=run[1] - run[0])
        excx = (bars_x[0] + bars_x[1]) / 2 - x0
        paste(canvas, piece, excx, cyc)
        print(f"[{tag}] entry {tex!r} fs={fs_e} {pw:.1f}x{ph:.1f} at row {run}")

    # --- subscript (red, per frame measurement); fit by WIDTH so the piece
    # stays inside the measured box and never crosses the right bar
    # (mathtext "N \times 1" is proportionally wider than the original's
    # rendering — fit-by-height at fs 16.3 rendered 40px wide vs orig 25) ---
    fs_s, sub, sw, sh = fit_piece(r"N \times 1", RED, target_w=(sx1 - sx0))
    scx = (sx0 + sx1) / 2 - x0
    scy = (sy0 + sy1) / 2 - y0
    paste(canvas, sub, scx, scy)
    print(f"[{tag}] subscript fs={fs_s} {sw:.1f}x{sh:.1f} centered ({scx:.0f},{scy:.0f}) rel")

    out = ASSETS / f"eq_004_{tag}.png"
    Image.fromarray(canvas).save(out)
    manifest = {
        "path": str(out),
        "w_px": cw, "h_px": ch, "dpi": DPI,
        "w_in": round(cw / DPI, 5), "h_in": round(ch / DPI, 5),
        "frame_x": x0, "frame_y": y0,
        "ink_w_frame_px": cw / S, "ink_h_frame_px": ch / S,
        "color": "mixed(black lead / red bars+entries / red subscript)",
        "fontset": "dejavusans",
        "mathtext": f"COMPOSED: {lead_tex} | drawn parens {bars_x} | pieces {entries} | N x 1",
        "renderer": "qa/slide004/gen_letbox_assets_att9.py (PIL composition, measured)",
        "notes": "place at x=frame_x/72 in, y=frame_y/72 in, w=w_in, h=h_in (1:1 with original ink)",
    }
    (ASSETS / f"eq_004_{tag}.json").write_text(json.dumps(manifest, indent=1))
    print(f"[{tag}] wrote {out} canvas {cw}x{ch} place at ({x0},{y0}) "
          f"w={cw/72:.5f} h={ch/72:.5f}")
    return manifest


# LEFT box (Yvec): canvas covers lead+matrix+subscript with 2px pad
left_box = (84, 102, 262, 210)
build_box("Yvec", r"Let \ \underline{\mathbf{Y}}\ =",
          [r"y_1", r"y_2", r"\cdots", r"y_n"],
          bars_x=[159, 184], box=left_box, sub_box=(186, 193, 211, 205))

# RIGHT box (Yhatvec)
right_box = (428, 104, 566, 219)
build_box("Yhatvec", r"Let \ \underline{\mathbf{\hat{Y}}}\ =",
          [r"\widehat{y}_1", r"\widehat{y}_2", r"\cdots", r"\widehat{y}_n"],
          bars_x=[504, 530], box=right_box, sub_box=(532, 199, 557, 210),
          lead_x0=430)

print("DONE")
