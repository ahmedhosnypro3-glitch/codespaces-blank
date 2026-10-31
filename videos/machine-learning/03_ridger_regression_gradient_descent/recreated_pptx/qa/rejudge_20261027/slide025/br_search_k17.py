#!/usr/bin/env python3
"""k17c: extended BR panel view search for slide 025.

Wider than k15: azim -120..0, elev 15..50, zoom 1.4..2.2, achieved fx/fy across
0.6..1.0, plus a color-norm low pad (pad_lo) to push more dark-blue low-t area
(orig jet-t main-diag mean 0.55 std 0.125; k15 render mean 0.70 min 0.43).

Scoring per candidate (all in slide-px space, BR box pasted at 615,344 265x187):
  band_diff : fraction of band x672..816 y472..517 with |diff|sum>60 (target <0.50)
  prof_err  : mean |row colored%| diff vs orig rows 455..528 over x615..880
  hist_dist : 0.5*sum|hist_r - hist_o| over 16 jet-t bins (orig from
              pil_k15_orig_groundtruth.txt section C)
  diag_err  : |mean-0.55| + |std-0.125| of jet-t on the surf-bbox main diagonal
score = 100*band_diff + prof_err + 25*hist_dist + 40*diag_err   (lower = better)

Stage 1: grid over (azim, elev, zoom, pad_lo).
Stage 2: cap-based zoom binary search (zoom in 1.4..2.2) for fx/fy caps in
         0.6..1.0 around the top stage-1 geometries.
Writes ranked lines to br_search_k17_results.txt (append) and at the end
br_search_best2.txt + br_cand_best2.png.
"""
import os
import re
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
DPI = 120
BOX = dict(x0=615, y0=344, w=265, h=187)
BW, BH = BOX["w"], BOX["h"]
JET = plt.get_cmap("jet")
JET_LUT = (JET(np.linspace(0, 1, 256))[:, :3] * 255.0)

# orig references
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
P = 8
ob = orig[BOX["y0"] + P:BOX["y0"] + BH - P, BOX["x0"] + P:BOX["x0"] + BW - P]


def colmask(a, border=2):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 60) & (mx > 90) & ~red
    if border > 0:
        m[:border, :] = False; m[-border:, :] = False
        m[:, :border] = False; m[:, -border:] = False
    return m


OM = colmask(ob, border=0)
OROW = 100.0 * OM.mean(1)  # over box rows (pad-8 crop)
# orig row profile over full box cols x615..880 rows 455..528 (slide space)
OMF = colmask(orig[344:531, 615:880], border=0)
OPROF_FULL = 100.0 * OMF.mean(1)

ORIG_HIST = np.array([1647, 0, 0, 555, 813, 0, 1140, 5098, 3272, 3597, 4, 1517,
                      2066, 401, 72, 1127], dtype=np.float64)
ORIG_HIST /= ORIG_HIST.sum()

BAND = dict(x0=672, y0=472, x1=816, y1=517)
OBAND = orig[BAND["y0"]:BAND["y1"], BAND["x0"]:BAND["x1"]]




def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


_X = np.linspace(-3, 3, 100)
_XG, _YG = np.meshgrid(_X, _X)
_ZG = br_surface(_XG, _YG)
_ZMIN, _ZMAX = float(_ZG.min()), float(_ZG.max())
_ZRNG = _ZMAX - _ZMIN


def blended_lut(w):
    """jet blended toward white by w — matches the orig's pastel surface."""
    return (JET_LUT * (1.0 - w) + 255.0 * w)


def render(azim, elev, zoom, pad_lo=0.3, zfac=1.3, whiten=0.0):
    if whiten > 0:
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list(
            "bjet", [tuple(c / 255.0) for c in blended_lut(whiten)])
    else:
        cmap = JET
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    norm = Normalize(_ZMIN - pad_lo * _ZRNG, _ZMAX)
    ax.plot_surface(_XG, _YG, _ZG, cmap=cmap, norm=norm, shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_zlim(_ZMIN - 0.5, _ZMAX + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, _ZRNG * zfac), zoom=zoom)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


_JET_SQ = (JET_LUT ** 2).sum(1)


def jet_t(px, lut=None):
    """px: (N,3) int -> t in 0..1 via nearest LUT entry (squared-dist trick)."""
    if lut is None:
        lut = JET_LUT
    lsq = (lut ** 2).sum(1)
    p = px.astype(np.float64)
    d = lsq[None, :] - 2.0 * (p @ lut.T) + (p * p).sum(1)[:, None]
    return d.argmin(1) / (len(lut) - 1)


def diag_stats(buf265, lut=None):
    m = colmask(buf265, border=2)
    ys, xs = np.nonzero(m)
    if len(xs) < 50:
        return None
    t = jet_t(buf265[ys, xs], lut)
    x0, y0 = xs.min(), ys.min()
    diag = np.abs((xs - x0) - (ys - y0)) <= 2
    if diag.sum() <= 10:
        return None
    td = t[diag]
    return float(td.mean()), float(td.std())


_od = diag_stats(orig[344:344 + 187, 615:615 + 265])
ORIG_DIAG = dict(mean=_od[0], std=_od[1])


def box_slide(buf):
    """resize box render to slide px (265x187)"""
    im = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    return np.array(im).astype(np.int32)


def metrics(bs, whiten=0.0):
    """bs: 265x187 slide-px box. Returns dict of metrics."""
    lut = blended_lut(whiten) if whiten > 0 else None
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[BOX["y0"]:BOX["y0"] + BH, BOX["x0"]:BOX["x0"] + BW] = bs
    rb = canvas[BAND["y0"]:BAND["y1"], BAND["x0"]:BAND["x1"]]
    band_diff = float((np.abs(OBAND - rb).sum(2) > 60).mean())
    rprof_full = 100.0 * colmask(canvas[344:531, 615:880], border=0).mean(1)
    prof_err = float(np.abs(rprof_full[455 - 344:529 - 344] - OPROF_FULL[455 - 344:529 - 344]).mean())
    # jet stats on the full box (pad 2 border, same mask family as orig GT)
    m = colmask(bs, border=2)
    out = dict(band=band_diff, prof=prof_err, hist=1.0, dmean=0.55, dstd=0.125, fx=0.0, fy=0.0)
    if m.sum() < 50:
        return out
    ys, xs = np.nonzero(m)
    t = jet_t(bs[ys, xs], lut)
    hist, _ = np.histogram(t, bins=16, range=(0, 1))
    hist = hist / hist.sum()
    out["hist"] = float(0.5 * np.abs(hist - ORIG_HIST).sum())
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    out["fx"] = (x1 - x0 + 1) / bs.shape[1]
    out["fy"] = (y1 - y0 + 1) / bs.shape[0]
    d = diag_stats(bs, lut)
    if d is not None:
        out["dmean"], out["dstd"] = d
    return out


def score_of(m):
    return (100.0 * m["band"] + m["prof"] + 25.0 * m["hist"]
            + 40.0 * (abs(m["dmean"] - ORIG_DIAG["mean"]) + abs(m["dstd"] - ORIG_DIAG["std"])))


results = []
RES = os.path.join(RJ, "br_search_k17_results.txt")


def evaluate(azim, elev, zoom, pad_lo, zfac=1.3, whiten=0.0, tag=""):
    buf = render(azim, elev, zoom, pad_lo, zfac, whiten)
    bs = box_slide(buf)
    m = metrics(bs, whiten)
    s = score_of(m)
    rec = (s, m["band"], m["prof"], m["hist"], m["dmean"], m["dstd"], m["fx"], m["fy"],
           azim, elev, zoom, pad_lo, zfac, whiten)
    results.append(rec)
    line = ("score=%.4f band=%.3f prof=%.2f hist=%.3f dmean=%.3f dstd=%.3f fx=%.3f fy=%.3f "
            "azim=%d elev=%d zoom=%.4f pad_lo=%.2f zfac=%.1f whiten=%.2f %s\n" % (rec + (tag,)))
    with open(RES, "a") as f:
        f.write(line)
    print(line, end="", flush=True)
    return buf, rec


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "1"
    if stage == "1" and os.path.exists(RES):
        os.remove(RES)
    if stage == "2" and os.path.exists(RES):
        # reload stage-1 results so stage 2 can refine the top geometries
        with open(RES) as f:
            for ln in f:
                v = dict(re.findall(r"(score|band|prof|hist|dmean|dstd|fx|fy|azim|elev|zoom|pad_lo|zfac)=([-\d.]+)", ln))
                if "score" not in v:
                    continue
                rec = (float(v["score"]), float(v["band"]), float(v["prof"]), float(v["hist"]),
                       float(v["dmean"]), float(v["dstd"]), float(v["fx"]), float(v["fy"]),
                       int(float(v["azim"])), int(float(v["elev"])), float(v["zoom"]),
                       float(v["pad_lo"]), float(v["zfac"]))
                results.append(rec)
        print("loaded %d prior results" % len(results), flush=True)
    if stage in ("1", "all"):
        print("== stage 1: grid (with whiten) ==", flush=True)
        for azim in range(-120, 1, 20):
            for elev in (15, 25, 35, 45):
                for zi in range(5):
                    zoom = 1.4 + zi * 0.2
                    for pad_lo in (0.0, 0.3, 0.6):
                        for whiten in (0.0, 0.35, 0.55):
                            evaluate(azim, elev, zoom, pad_lo, whiten=whiten)
        results.sort()
        print("stage1 best:", results[0], flush=True)
    if stage in ("2", "all"):
        print("== stage 2: cap-based zoom refine ==", flush=True)
        results.sort()
        seen = set()
        for rec in results[:8]:
            key = (rec[8], rec[9], rec[11], rec[13])  # azim, elev, pad_lo, whiten
            if key in seen:
                continue
            seen.add(key)
            azim, elev, pad_lo, whiten = rec[8], rec[9], rec[11], rec[13]
            for fxc in (0.6, 0.75, 0.9, 1.0):
                for fyc in (0.6, 0.75, 0.9, 1.0):
                    lo, hi = 1.4, 2.2
                    for _ in range(6):
                        zm = 0.5 * (lo + hi)
                        buf = render(azim, elev, zm, pad_lo, whiten=whiten)
                        m = metrics(box_slide(buf), whiten)
                        if m["fx"] <= fxc and m["fy"] <= fyc:
                            lo = zm
                        else:
                            hi = zm
                    evaluate(azim, elev, lo, pad_lo, whiten=whiten,
                             tag="cap fx=%.2f fy=%.2f" % (fxc, fyc))
    results.sort()
    best = results[0]
    with open(os.path.join(RJ, "br_search_best2.txt"), "w") as f:
        f.write("# k17c extended search — ranked (score band prof hist dmean dstd fx fy azim elev zoom pad_lo zfac whiten)\n")
        for r in results[:80]:
            f.write("score=%.4f band=%.3f prof=%.2f hist=%.3f dmean=%.3f dstd=%.3f fx=%.3f fy=%.3f "
                    "azim=%d elev=%d zoom=%.4f pad_lo=%.2f zfac=%.1f whiten=%.2f\n" % r)
    buf = render(best[8], best[9], best[10], best[11], best[12], best[13])
    Image.fromarray(buf.astype(np.uint8)).save(os.path.join(RJ, "br_cand_best2.png"))
    print("BEST2:", best, flush=True)
    print("wrote br_search_best2.txt br_cand_best2.png", flush=True)
