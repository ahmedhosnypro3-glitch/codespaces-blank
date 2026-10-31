"""Lane G / b_geom_3 definitive geometry measurement.

Masks:
- render: exact distance from #E8E8E8 (the render background), then exclude the
  house chrome (red frame ring @0.15in, badge disc @12.48/0.30) and a 1px white
  PDF page border.
- original: exact distance from its own modal background, then exclude the
  original slide's own outer border ring and its own badge region.

Regions are per-slide horizontal bands from the slide's own layout structure.
All comparisons are done at 960x540 frame scale; tolerance 2px frame scale.
"""
import os

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = ["014", "016", "017", "023", "024"]
REND = "_pool/lo_geom_b_geom_3/out"
SCOPE = "b_geom_3"
TOL = 2.0
FW, FH = 960, 540

BANDS = {
    "014": [("title_block", 40, 110), ("diagram_body", 110, 480), ("footer_strip", 480, 540)],
    "016": [("title_block", 40, 110), ("diagram_body", 110, 480), ("footer_strip", 480, 540)],
    "017": [("title_block", 40, 110), ("diagram_body", 110, 480), ("footer_strip", 480, 540)],
    "023": [("title_block", 40, 100), ("flowchart_body", 100, 495), ("footer_strip", 495, 540)],
    "024": [("title_block", 40, 105), ("panel_upper", 105, 300),
            ("panel_lower", 300, 465), ("footer_strip", 465, 540)],
}


def modal_bg(a, step=3):
    h, w = a.shape[:2]
    s = a[::step, ::step].reshape(-1, 3)
    u, c = np.unique(s, axis=0, return_counts=True)
    return u[c.argmax()].astype(np.int16)


def render_masks(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(np.int16)
    bg = np.array([232, 232, 232], dtype=np.int16)
    m = np.abs(a - bg).max(axis=2) > 6
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = False
    H, W = m.shape
    ex = np.zeros_like(m)
    inset, band = int(round(0.15 * 150)), 8
    for t in (inset, W - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    for t in (inset, H - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    ex[int(0.16 * 150):int(0.94 * 150), int(12.34 * 150):int(13.10 * 150)] = True
    return m & ~ex


def orig_masks(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(np.int16)
    bg = modal_bg(a)
    m = np.abs(a - bg).max(axis=2) > 10
    H, W = m.shape
    ex = np.zeros_like(m)
    rows, cols, band = m.sum(1), m.sum(0), 12
    for y in list(range(int(H * 0.14))) + list(range(int(H * 0.86), H)):
        if rows[y] > W * 0.55:
            ex[max(0, y - band):y + band + 1, :] = True
    for x in list(range(int(W * 0.14))) + list(range(int(W * 0.86), W)):
        if cols[x] > H * 0.45:
            ex[:, max(0, x - band):x + band + 1] = True
    ex[int(0.08 * 540):int(0.32 * 540), int(0.88 * 960):FW] = True
    return m & ~ex


def bbox_in(m, y0, y1, x0, x1):
    y0, y1 = max(0, y0), min(m.shape[0] - 1, y1)
    x0, x1 = max(0, x0), min(m.shape[1] - 1, x1)
    sub = m[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None, 0
    return (int(xs.min()) + x0, int(ys.min()) + y0,
            int(xs.max()) + x0, int(ys.max()) + y0), int(sub.sum())


def main():
    sx, sy = FW / 2001.0, FH / 1125.0
    lines = []
    for n in SLIDES:
        om = orig_masks(os.path.join(NS, "unique_slides", f"slide_{n}.jpg"))
        rm = render_masks(os.path.join(NS, REND, f"slide_{n}_150.png"))
        lines.append(f"## slide {n}")
        lines.append(f"ink frac (chrome-masked): orig={om.mean():.4f} render={rm.mean():.4f}")
        for name, y0, y1 in BANDS[n]:
            ob, on = bbox_in(om, y0, y1, 0, FW - 1)
            rb, rn = bbox_in(rm, round(y0 / sy), round(y1 / sy), 0, 2000)
            if ob is None or rb is None:
                lines.append(f"- {name}: [SKIP] orig={ob} render={rb} (no ink on one side)")
                continue
            rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
            d = [ob[0] - rbf[0], ob[1] - rbf[1], ob[2] - rbf[2], ob[3] - rbf[3]]
            worst = max(abs(v) for v in d)
            verdict = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
            lines.append(
                f"- {name}: {verdict}\n"
                f"  orig box    {ob}  (w{ob[2]-ob[0]+1} h{ob[3]-ob[1]+1})\n"
                f"  render box  renderpx {rb} -> frame [{rbf[0]:.1f},{rbf[1]:.1f}]-"
                f"[{rbf[2]:.1f},{rbf[3]:.1f}]\n"
                f"  delta       dx0={d[0]:+.2f} dy0={d[1]:+.2f} dx1={d[2]:+.2f} dy1={d[3]:+.2f} "
                f"| dsize dw={d[2]-d[0]:+.2f} dh={d[3]-d[1]:+.2f} | worst={worst:.2f} "
                f"(tol {TOL})\n"
                f"  ink px      orig={on} render={rn}")
        lines.append("")
    out = os.path.join(NS, "_pool/geom_b_geom_3/measure_out.txt")
    open(out, "w").write("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
