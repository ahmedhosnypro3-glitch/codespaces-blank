#!/usr/bin/env python3
r"""Banked equation builder for slide 023 (deck 03).

Equation (verbatim from analysis/slide_023_final.json):
    W = (X^T X + lambda I)^(-1) X^T Y        [underscore = underline]

MEASURED from unique_slides/slide_023.jpg (960x540, 1px = 1pt = 1/72 in):
  ink bbox            x104..429  y150..186   (w 325, h 37)
  W   x104..131 y157..179  + underline bar y180..181 x104..131   BLACK
  =   x152..166 y164..172                                        BLACK
  (   x178..196 y150..186                                        BLACK
  X   x191..210 y157..178   T sup x215..225 y150..162
  X   x230..251 y157..178
  +   x266..281 y160..175
  lam x294..311 y156..179   GREEN   core (8..20, 130..138, 4..22) ~ 008000
  I   x317..329 y157..178   GREEN
  )   x333..354 y150..186                                        BLACK
  -1  x347..363 y150..162   RED     core (133,3,15)  ~ C00000 (family nominal)
  X   x370..391 y157..178   T sup x394..404 y150..163
  Y   x409..429 y157..181   + underline bar y180..181 x410..429   BLACK

METHOD (per-symbol colors, one picture):
  render_eq.py takes ONE color, so the picture is composited:
    1. base = the full mathtext with the coloured parts PHANTOMED
       (metrics preserved: phantom occupies the same box).
    2. full = the same mathtext, all black -> slot = ink(full) & ~ink(base)
       = exactly the coloured regions, in the base's own pixel grid.
    3. render `\\lambda I` in 008000 and `^{-1}` in C00000 at the SAME
       fontsize; paste each with its ink-left edge on the slot's left edge
       and its baseline row on the base's baseline row (identical font/size
       => identical glyph boxes => exact coincidence).
  Placement: image tight-bbox lands on ink x104..429, y150..186.
  Calibration: fs 32.5 -> ink 320.6 x 34.3 pt vs measured 325 x 37 px
  (width -1.4%, height -7%: mathtext's parenthesis stack is shorter than
  the original's; content/glyph shapes and colours are the priority and
  sibling-verified close). \underline reproduces both measured underline
  bars (immediately under W and Y).
"""
import json, subprocess, sys, os
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
ASSETS = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets")
TMP = os.path.join(ROOT, "scratch/tmp")
FS = "32.5"
MATHTEXT = "\\underline{W} = \\left( X^T X + \\lambda I \\right)^{-1} X^T \\underline{Y}"
# NOTE: phantom ONLY the lambda/I. Phantom-ing the -1 superscript as well
# measurably SHRINKS the closing delimiter (mathtext sizes the delimiter from the
# real ink, not the phantom box) -> the paren no longer matches the frame. With
# lambda/I only, the enclosed content height is unchanged, so both delimiters
# keep their real height and the -1 keeps its real position; the red -1 is then
# pasted exactly over the black one (identical mathtext box).
PHANTOMED = "\\underline{W} = \\left( X^T X + \\phantom{\\lambda I} \\right)^{-1} X^T \\underline{Y}"
BLACK, GREEN, RED = "#000000", "#008000", "#C00000"

def render(tex, out, color):
    p = subprocess.run(["python3", os.path.join(ROOT, "scripts/render_eq.py"), tex, out, FS, color],
                       capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        raise SystemExit(f"render failed for {tex!r}: {p.stderr[-500:]}")
    return json.loads(p.stdout)

def ink_mask(rgba, thr=40):
    return rgba[:, :, 3] > thr

def main():
    os.makedirs(ASSETS, exist_ok=True)
    base = render(PHANTOMED, f"{TMP}/eq023_base.png", BLACK)
    full = render(MATHTEXT,   f"{TMP}/eq023_full.png", BLACK)
    green = render("\\lambda I", f"{TMP}/eq023_green.png", GREEN)
    red   = render("^{-1}",      f"{TMP}/eq023_red.png",   RED)

    ba = np.array(Image.open(base["path"]).convert("RGBA"))
    fa = np.array(Image.open(full["path"]).convert("RGBA"))
    assert ba.shape == fa.shape, "canvas mismatch between base and full renders"
    bi, fi = ink_mask(ba), ink_mask(fa)
    slot = fi & ~bi
    cols = np.where(slot.sum(axis=0) > 0)[0]
    groups, prev = [], None
    for c in cols:
        if prev is None or c - prev > 3:
            groups.append([int(c), int(c)])
        else:
            groups[-1][1] = int(c)
        prev = c
    # classify the slot groups by vertical extent: lambda + I are cap-height
    # (tall); the -1 superscript sits above the baseline and is short.
    shaped = []
    for g in groups:
        rr = np.where(slot[:, g[0]:g[1] + 1].sum(axis=1) > 0)[0]
        shaped.append({"g": g, "r0": int(rr.min()), "r1": int(rr.max())})
        print(f"  slot x{g[0]}..{g[1]} rows{rr.min()}..{rr.max()} h={rr.max()-rr.min()+1}")
    green_slots = [s for s in shaped if s["r1"] - s["r0"] > 20]
    assert green_slots, f"slot classification failed (no lambda/I slot): {shaped}"
    green_x = green_slots[0]["g"][0]      # left edge of lambda
    # The -1 keeps its REAL black ink in the base (phantom-ing it shrinks the
    # closing delimiter, measured), so it is located by template-matching the
    # identical mathtext superscript and then overwritten by the red render of
    # the same mathtext -> pixel-exact coincidence with the black underneath.
    tmpl_info = render("^{-1}", f"{TMP}/eq023_sup_black.png", BLACK)
    tim = np.array(Image.open(tmpl_info["path"]).convert("RGBA"))
    tmask = ink_mask(tim)
    tys, txs = np.where(tmask)
    tx0, ty0 = int(txs.min()), int(tys.min())
    T = tmask[int(tys.min()):int(tys.max()) + 1, tx0:int(txs.max()) + 1]
    th, tw = T.shape
    print(f"  superscript template {tw}x{th}")

    def coarse_anchor(f=4):
        def ds(m):
            img = Image.fromarray((m * 255).astype(np.uint8)).resize(
                (max(1, m.shape[1] // f), max(1, m.shape[0] // f)), Image.BOX)
            return np.array(img) > 60
        Bc, Tc = ds(bi), ds(T)
        bh, bw = Bc.shape
        best = (-1.0, 0, 0)
        for y in range(0, bh - Tc.shape[0] + 1):
            band = Bc[y:y + Tc.shape[0], :]
            for x in range(0, bw - Tc.shape[1] + 1):
                w = band[:, x:x + Tc.shape[1]]
                inter = (w & Tc).sum()
                if inter == 0:
                    continue
                s = inter / (w | Tc).sum()
                if s > best[0]:
                    best = (s, x * f, y * f)
        return best

    bs, bx, by = coarse_anchor()
    best = (-1.0, 0, 0)
    ink_total = float(T.sum())
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            y0 = by + dy - ty0
            x0 = bx + dx - tx0
            if y0 < 0 or x0 < 0 or y0 + th > bi.shape[0] or x0 + tw > bi.shape[1]:
                continue
            w = bi[y0:y0 + th, x0:x0 + tw]
            s = float((w & T).sum()) / ink_total
            if s > best[0]:
                best = (s, x0 + tx0, y0 + ty0)
    print(f"  superscript anchor: coarse={bs:.3f}@{bx},{by} refined={best[0]:.4f}@x{best[1]} y{best[2]}")
    red_x = best[1]
    assert best[0] > 0.9, f"superscript not located in the base render (score {best[0]:.3f})"

    out = ba.copy()
    def paste(piece_info, img_path, slot_x):
        pim = np.array(Image.open(img_path).convert("RGBA"))
        pm = ink_mask(pim)
        ys, xs = np.where(pm)
        # align ink-left edge with the slot's left edge; baselines coincide
        dx = slot_x - int(xs.min())
        dy = int(base["baseline_px"] - piece_info["baseline_px"])
        h, w = out.shape[:2]
        pasted = 0
        for y in range(pim.shape[0]):
            Y = y + dy
            if Y < 0 or Y >= h:
                continue
            for x in range(pim.shape[1]):
                X = x + dx
                if 0 <= X < w and pim[y, x, 3] > 20:
                    out[Y, X] = pim[y, x]
                    pasted += 1
        print(f"  pasted {img_path.split('/')[-1]}: dx={dx} dy={dy} inkpx={pasted}")

    paste(green, green["path"], green_x)
    # the -1 slot is pasted over the BLACK -1 that is already in the base: the
    # same mathtext box, so the red lands exactly on it.
    paste(red,   red["path"],   red_x)

    # tighten to the ink bbox (same rule as render_eq.py: PAD 8)
    om = ink_mask(out)
    rows = np.where(om.sum(axis=1) > 0)[0]; ccols = np.where(om.sum(axis=0) > 0)[0]
    PAD = 8
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, out.shape[0])
    x0, x1 = max(ccols[0] - PAD, 0), min(ccols[-1] + PAD, out.shape[1])
    tight = out[y0:y1, x0:x1]
    png = os.path.join(ASSETS, "eq_023_main.png")
    Image.fromarray(tight).save(png)

    # baseline recomputed on the TIGHT crop (baseline row = the 'x' probe row; the
    # probe shares the equation baseline, and the tight crop shifted it by y0)
    baseline_row = int(base["baseline_px"] - y0)
    h_px, w_px = tight.shape[0], tight.shape[1]
    sidecar = {
        "path": png,
        "w_px": w_px, "h_px": h_px,
        "w_in": round(w_px / 600, 5), "h_in": round(h_px / 600, 5),
        "baseline_px": baseline_row,
        "baseline_frac": round(baseline_row / h_px, 5),
        "dpi": 600, "fontsize_pt": float(FS),
        "color": "000000",
        "mathtext": MATHTEXT,
        "symbol_colors": {"default": "000000", "lambda": "008000", "I": "008000", "sup_-1": "C00000"},
        "measured_ink_frame_px": {"x": [104, 429], "y": [150, 186]},
        "notes": "composite: black base (phantom slots) + green \\lambda I + red ^{-1}; "
                 "both W and Y underlined per frame measurement",
    }
    json.dump(sidecar, open(os.path.join(ASSETS, "eq_023_main.json"), "w"), indent=1)
    print(json.dumps(sidecar, indent=1))

    # ---- verification: colours per group on the composite -------------------
    x0c = x0
    im = Image.open(png).convert("RGBA"); arr = np.array(im)
    a = arr[:, :, 3]
    rgb = arr[:, :, :3].astype(int)
    H, Wp = a.shape
    def probe(name, x0, x1):
        X0, X1 = max(int(x0 - x0c), 0), min(int(x1 - x0c), Wp)
        if X1 <= X0:
            print(f"  {name}: EMPTY WINDOW"); return
        reg = rgb[:, X0:X1]; al = a[:, X0:X1]
        ys, xs = np.where(al > 40)
        sel = reg[ys, xs]
        lum = sel.sum(axis=1)
        k = np.argsort(lum)[:max(20, len(lum) // 20)]
        print(f"  {name}: n={len(ys)} darkest core {tuple(int(v) for v in sel[k].mean(axis=0))}")
    probe("W (black)", 8, 340)
    probe("lambda (green)", green_slots[0]["g"][0], green_slots[0]["g"][1])
    probe("I (green)", green_slots[-1]["g"][0], green_slots[-1]["g"][1])
    probe("sup -1 (red)", green_slots[-1]["g"][1] + 60, 2290)
    probe("Y (black)", 2330, 2690)

if __name__ == "__main__":
    main()
