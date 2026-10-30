#!/usr/bin/env python3
"""Composite equation renderer for slide 048: builds a 600dpi transparent PNG
from segments, supporting inline mathtext runs and stacked column vectors.

Segment spec (JSON on argv[1]):
  {"segments": [
     {"t": "d(x_1) = "},
     {"row": ["1","1","1"], "colors": ["000000","FF0000","000000"]},  # inline row vector
     {"t": " \\cdot "},
     {"col": ["4","-2","-2"], "colors": ["000000","FF0000","FF0000"]},  # stacked column
     {"t": " = 0"}],
   "fontsize": 14, "color": "000000"}

Emits the same sidecar JSON contract as render_eq.py:
  {w_px,h_px,w_in,h_in,baseline_px,baseline_frac,dpi,fontsize_pt,color}
baseline_frac*h_in = inches from image TOP down to the math baseline.
"""
import json, sys, subprocess, tempfile, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8


def render_text(latex, fontsize, color):
    """Render one mathtext run -> (RGBA array, baseline_row_in_crop, w, h)."""
    fig = plt.figure(figsize=(12, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    txt = fig.text(0.05, 0.5, f"${latex}$", fontsize=fontsize, color=color,
                   ha="left", va="baseline")
    probe = fig.text(0.02, 0.5, "x", fontsize=fontsize, color=color,
                     ha="left", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    baseline_row = int(np.where(ink[:, px0:px1].any(axis=1))[0][-1])
    ink[:, :px1 + 20] = False       # drop the probe (through its right edge)
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    plt.close(fig)
    crop = buf[y0:y1, x0:x1]
    return crop, baseline_row - y0, (x1 - x0), (y1 - y0)


def render_entries(entries, fontsize, color, colors=None, gap_frac=0.42):
    """Stacked column vector entries -> (array, baseline_row, w, h).
    If colors list provided, color each entry individually."""
    runs = []
    for i, e in enumerate(entries):
        c = colors[i] if colors and i < len(colors) else color
        # Ensure # prefix for matplotlib
        if not c.startswith('#'):
            c = '#' + c
        a, bl, w, h = render_text(e, fontsize, c)
        runs.append((a, bl, w, h))
    gap = int(round(max(r[3] for r in runs) * gap_frac))
    wmax = max(r[2] for r in runs)
    total_h = sum(r[3] for r in runs) + gap * (len(runs) - 1)
    out = np.zeros((total_h, wmax, 4), dtype=np.uint8)
    y = 0
    baselines = []
    for a, bl, w, h in runs:
        xoff = (wmax - w) // 2
        out[y:y + h, xoff:xoff + w] = a
        baselines.append(y + bl)
        y += h + gap
    return out, baselines, wmax, total_h


def render_row(entries, fontsize, color, colors=None):
    """Inline row vector as single mathtext run with per-entry coloring.
    Renders each entry as separate text, composes horizontally with spacing."""
    import numpy as _np
    entry_runs = []
    for i, e in enumerate(entries):
        c = colors[i] if colors and i < len(colors) else color
        if not c.startswith('#'):
            c = '#' + c
        a, bl, w, h = render_text(e, fontsize, c)
        entry_runs.append((a, bl, w, h))
    gap = int(round(max(r[3] for r in entry_runs) * 0.55))
    wmax = max(r[2] for r in entry_runs)
    total_h = max(r[3] for r in entry_runs)
    # Width: parens + entries + gaps
    paren_w = max(int(round(fontsize * 1.6)), 4)
    total_w = paren_w * 2 + sum(r[2] for r in entry_runs) + gap * (len(entry_runs) - 1) + 12
    out = _np.zeros((total_h, total_w, 4), dtype=_np.uint8)
    baselines = []
    x = paren_w + 6
    for a, bl, w, h in entry_runs:
        yoff = (total_h - h) // 2
        out[yoff:yoff + h, x:x + w] = a
        baselines.append(yoff + bl)
        x += w + gap
    # Draw parens: left and right as tall curved strokes
    mid_bl = baselines[len(baselines) // 2]
    ytop = min(r[0] for r in [(rr[3], 0) for rr in entry_runs])
    y0, y1 = 0, total_h
    bw = max(int(round(fontsize * 0.6)), 3)
    serif = max(int(round(fontsize * 0.5)), 3)
    y_span_top = 2
    y_span_bot = total_h - 2
    # left paren strokes
    out[y_span_top:y_span_bot, 0:bw, 3] = 255
    out[y_span_top:y_span_top + bw, 0:serif, 3] = 255
    out[y_span_bot - bw:y_span_bot, 0:serif, 3] = 255
    out[y_span_top:y_span_bot, 0:bw, 0:3] = 0
    out[y_span_top:y_span_top + bw, 0:serif, 0:3] = 0
    out[y_span_bot - bw:y_span_bot, 0:serif, 0:3] = 0
    # right paren
    rx = total_w - bw
    out[y_span_top:y_span_bot, rx:rx + bw, 3] = 255
    out[y_span_top:y_span_top + bw, rx + bw - serif:rx + bw, 3] = 255
    out[y_span_bot - bw:y_span_bot, rx + bw - serif:rx + bw, 3] = 255
    out[y_span_top:y_span_bot, rx:rx + bw, 0:3] = 0
    out[y_span_top:y_span_top + bw, rx + bw - serif:rx + bw, 0:3] = 0
    out[y_span_bot - bw:y_span_bot, rx + bw - serif:rx + bw, 0:3] = 0
    return out, baselines[len(baselines) // 2], total_w, total_h


def main():
    spec = json.loads(sys.argv[1])
    out_path = sys.argv[2]
    fs = spec.get("fontsize", 14)
    color = "#" + spec.get("color", "000000").lstrip("#")
    segs = spec["segments"]

    # entry font slightly smaller than the line font for column vectors
    efs = fs * 0.92

    rendered = []
    for seg in segs:
        if "t" in seg:
            a, bl, w, h = render_text(seg["t"], fs, color)
            rendered.append({"kind": "text", "arr": a, "baseline": bl,
                             "w": w, "h": h, "gap_frac": None})
        elif "row" in seg:
            # inline row vector with per-entry coloring
            a, bl, w, h = render_row(seg["row"], fs, color, seg.get("colors"))
            rendered.append({"kind": "text", "arr": a, "baseline": bl,
                             "w": w, "h": h, "gap_frac": None})
        elif "col" in seg:
            a, bls, w, h = render_entries(seg["col"], efs, color, seg.get("colors"))
            rendered.append({"kind": "col", "arr": a, "baseline": bls,
                             "w": w, "h": h, "gap_frac": 0.42})
        else:
            raise SystemExit(f"bad segment {seg}")

    # common math baseline: text segments sit on it; a column vector's MIDDLE
    # entry sits on it (measured from the original frames).
    text_bls = [r["baseline"] for r in rendered if r["kind"] == "text"]
    col_mids = [r["baseline"][len(r["baseline"]) // 2]
                for r in rendered if r["kind"] == "col"]
    base_bl = max(text_bls) if text_bls else (max(col_mids) if col_mids else 0)

    def anchor(r):
        return r["baseline"] if r["kind"] == "text" else \
            r["baseline"][len(r["baseline"]) // 2]

    above = [anchor(r) for r in rendered]
    below = [r["h"] - anchor(r) for r in rendered]
    line_y = PAD_PX + (max(above) if above else 0)
    H = line_y + (max(below) if below else 0) + PAD_PX

    # measure each part and lay out horizontally into draw ops
    ops = []          # (kind, payload)
    x = 0
    for r in rendered:
        if r["kind"] == "text":
            ops.append(("text", x, r))
            x += r["w"]
        else:
            # left bracket | entries | right bracket
            bw = max(int(round(fs * 0.62)), 5)      # stroke thickness
            serif = max(int(round(fs * 0.55)), 5)   # serif horizontal run
            bx_l = x
            bx_r = x + bw + 2 + r["w"] + 2
            ops.append(("col", bx_l, bx_r, bw, serif, r))
            x = bx_r + bw
    total_w = x + 2 * PAD_PX

    canvas = np.zeros((H, total_w, 4), dtype=np.uint8)

    def paste(arr, x0, y0):
        h, w = arr.shape[:2]
        if y0 < 0 or y0 + h > H:
            raise SystemExit(f"paste out of range: y0={y0} h={h} H={H}")
        canvas[y0:y0 + h, x0:x0 + w] = arr

    for op in ops:
        if op[0] == "text":
            _, px, r = op
            paste(r["arr"], px + PAD_PX, line_y - r["baseline"])
        else:
            _, bx_l, bx_r, bw, serif, r = op
            mid = r["baseline"][len(r["baseline"]) // 2]
            y_entries = line_y - mid
            paste(r["arr"], bx_l + bw + 2 + PAD_PX, y_entries)
            # PARENTHESES span the full entry stack (per original slide)
            top = y_entries
            bot = y_entries + r["h"]
            lx = bx_l + PAD_PX
            rx = bx_r + PAD_PX
            # Left parenthesis: vertical stroke + top/bottom serifs curving right
            strokes = [
                (slice(top, bot), slice(lx, lx + bw)),  # vertical
                (slice(top, top + bw), slice(lx, lx + serif)),  # top serif
                (slice(bot - bw, bot), slice(lx, lx + serif)),  # bottom serif
                # Right parenthesis: vertical stroke + top/bottom serifs curving left
                (slice(top, bot), slice(rx, rx + bw)),  # vertical
                (slice(top, top + bw), slice(rx + bw - serif, rx + bw)),  # top serif
                (slice(bot - bw, bot), slice(rx + bw - serif, rx + bw)),  # bottom serif
            ]
            for sy, sx in strokes:
                canvas[sy, sx, 0:3] = 0
                canvas[sy, sx, 3] = 255

    # crop tightly
    alpha = canvas[:, :, 3] > 8
    rows = np.where(alpha.any(axis=1))[0]
    cols = np.where(alpha.any(axis=0))[0]
    y0, y1 = rows[0], rows[-1] + 1
    x0, x1 = cols[0], cols[-1] + 1
    canvas = canvas[y0:y1, x0:x1]

    # optional uniform rescale to a measured slide width (frame-px fidelity):
    # the composite is generated, so resizing it is a render-at-size, not a
    # rescale of fixed-size glyphs.
    tw = spec.get("target_w_in")
    th = spec.get("target_h_in")
    if tw or th:
        from PIL import Image as _I
        im = _I.fromarray(canvas)
        cur_w, cur_h = im.size
        if tw and th:
            nw, nh = int(round(tw * DPI)), int(round(th * DPI))
        elif tw:
            nw = int(round(tw * DPI))
            nh = max(1, int(round(cur_h * (nw / cur_w))))
        else:
            nh = int(round(th * DPI))
            nw = max(1, int(round(cur_w * (nh / cur_h))))
        im = im.resize((nw, nh), _I.LANCZOS)
        canvas = np.asarray(im)
        Image.fromarray(canvas).save(out_path)
        h = canvas.shape[0]
        new_base = int(round(line_y * nh / (y1 - y0)))
        info = {"path": out_path, "w_px": canvas.shape[1], "h_px": int(h),
                "w_in": round(canvas.shape[1] / DPI, 5),
                "h_in": round(h / DPI, 5),
                "baseline_px": int(new_base),
                "baseline_frac": round(new_base / h, 5),
                "dpi": DPI, "fontsize_pt": fs,
                "color": spec.get("color", "000000")}
        print(json.dumps(info))
        return

    Image.fromarray(canvas).save(out_path)

    h = y1 - y0
    # baseline re-expressed in the tightly-cropped frame
    new_base = line_y - y0
    info = {"path": out_path, "w_px": int(x1 - x0), "h_px": int(h),
            "w_in": round((x1 - x0) / DPI, 5), "h_in": round(h / DPI, 5),
            "baseline_px": int(new_base),
            "baseline_frac": round(new_base / h, 5),
            "dpi": DPI, "fontsize_pt": fs, "color": spec.get("color", "000000")}
    print(json.dumps(info))


if __name__ == "__main__":
    main()