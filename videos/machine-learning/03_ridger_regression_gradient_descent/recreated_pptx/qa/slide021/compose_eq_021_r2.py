#!/usr/bin/env python3
"""Per-segment multi-colour mathtext composer (slide 021, rejudge r2).

Rebuilds a certified-composer asset from its JSON sidecar: each segment is
rendered at 600 dpi on a shared baseline and composited left-to-right by the
segment's advance width, then trimmed to ink + 8 px pad. Writes the PNG and
updates the sidecar's pixel fields. Usage:

  python3 compose_eq_021_r2.py <asset.json> [--validate]

--validate re-renders with the sidecar's CURRENT segments and only checks
pixel dimensions against the embedded certified PNG (no writes).
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8
FIG = (10, 4)


PEN_X = 0.02  # fig fraction; pen x = PEN_X * canvas width in every canvas


def render_string(latex, fontsize, color="black", probe=False):
    fig = plt.figure(figsize=FIG, dpi=DPI)
    fig.patch.set_alpha(0.0)
    t = fig.text(PEN_X, 0.5, f"${latex}$", fontsize=fontsize, color=color,
                 ha="left", va="baseline")
    pb = None
    if probe:
        p = fig.text(0.9, 0.5, "x", fontsize=fontsize, color=color,
                     ha="center", va="baseline")
        pb = p.get_window_extent(renderer=fig.canvas.get_renderer())
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    ext = t.get_window_extent(renderer=ren)
    if probe:
        pb = p.get_window_extent(renderer=ren)
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    base_row = None
    if probe:
        ink = buf[:, :, 3] > 8
        base_row = int(np.where(ink[:, int(pb.x0):int(pb.x1)].any(axis=1))[0][-1])
    plt.close(fig)
    return buf, ext, base_row


def compose(segments, fontsize):
    n = len(segments)
    latex = [s["mathtext"] for s in segments]
    colors = ["#" + s["color"].lstrip("#") for s in segments]
    # pen x (canvas px) where each segment starts in the FULL-string layout,
    # from prefix renders so inter-segment kerning/spacing is preserved
    pen = FIG[0] * DPI * PEN_X
    pen_starts = []
    prefix = ""
    for k in range(n):
        pen_starts.append(pen)
        prefix += latex[k]
        _, ext, _ = render_string(prefix, fontsize)
        pen = ext.x1
    base = None
    parts = []
    for k in range(n):
        buf, ext, base_row = render_string(latex[k], fontsize, colors[k], probe=True)
        parts.append((buf, base_row))
        base = base_row if base is None else max(base, base_row)
    total_w = int(pen_starts[-1] + 400)
    W = total_w + PAD_PX + 64
    H = FIG[1] * DPI
    out = np.zeros((H, W, 4), dtype=np.uint8)
    for k, (buf, base_row) in enumerate(parts):
        dx = int(round(pen_starts[k])) - int(round(FIG[0] * DPI * PEN_X))
        dy = base - base_row
        h, w = buf.shape[:2]
        ys, xs = max(dy, 0), max(dx, 0)
        ye, xe = min(dy + h, H), min(dx + w, W)
        sub = buf[ys - dy:ye - dy, xs - dx:xe - dx]
        dst = out[ys:ye, xs:xe]
        a = sub[:, :, 3:4].astype(np.uint16)
        dst[:, :, :3] = (sub[:, :, :3] * a + dst[:, :, :3] * (255 - a)) // 255
        dst[:, :, 3] = np.maximum(dst[:, :, 3], sub[:, :, 3])
    ink = out[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit("no ink")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, H)
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, W)
    img = Image.fromarray(out[y0:y1, x0:x1])
    info = {"w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5),
            "baseline_px": int(base - y0),
            "baseline_frac": round((base - y0) / (y1 - y0), 5), "dpi": DPI}
    return img, info


def main():
    path = sys.argv[1]
    validate = "--validate" in sys.argv
    spec = json.load(open(path))
    img, info = compose(spec["segments"], spec["fontsize_pt"])
    print(json.dumps(info))
    if validate:
        ref = Image.open(spec["_ref_png"])
        print("ref", ref.size, "match" if ref.size == (info["w_px"], info["h_px"]) else "MISMATCH")
        return
    img.save(path.replace(".json", ".png"))
    spec.update(info)
    spec["path"] = path.replace(".json", ".png")
    json.dump(spec, open(path, "w"), indent=1)
    print("wrote", spec["path"])


if __name__ == "__main__":
    main()
