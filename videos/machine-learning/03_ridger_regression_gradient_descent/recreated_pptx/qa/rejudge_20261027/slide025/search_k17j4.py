#!/usr/bin/env python3
"""k17j v4: scale-invariant silhouette-shape search.

For each (azim, elev, zfac) render once at fixed zoom, compute the surface
silhouette extremes L/R/T/B normalized to its own bbox (invariant to zoom),
plus bottom-taper descriptors (row width at 3 depths), and match to orig.
Then compute zoom analytically to hit the orig bbox size, render, full metrics.
"""
import os, sys, json
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.interpolate import CubicSpline
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
BW, BH = 265, 187
X0, Y0 = 615, 344
DPI = 120
JET_LUT = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255.0)
P = 8


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~red


def jet_t(px):
    d = ((JET_LUT[None, :, :] - px[:, None, :].astype(np.float64)) ** 2).sum(2)
    return d.argmin(1) / 255.0


ref = json.load(open(os.path.join(RJ, "search_k17j_orig_ref.json")))
ORIG_HIST = np.array(ref["hist"], float); ORIG_HIST /= ORIG_HIST.sum()
OMF = colmask(ORIG[Y0:Y0 + BH, X0:X0 + BW])
# orig silhouette in panel coords (266x188)
oys, oxs = np.nonzero(OMF)
OB_ = (oxs.min(), oxs.max(), oys.min(), oys.max())
oiL, oiR, oiT, oiB = oxs.argmin(), oxs.argmax(), oys.argmin(), oys.argmax()
OW, OH = OB_[1] - OB_[0] + 1, OB_[3] - OB_[2] + 1
ORIG_SHAPE = dict(
    L=((oxs[oiL] - OB_[0]) / OW, (oys[oiL] - OB_[2]) / OH),
    R=((oxs[oiR] - OB_[0]) / OW, (oys[oiR] - OB_[2]) / OH),
    T=((oxs[oiT] - OB_[0]) / OW, (oys[oiT] - OB_[2]) / OH),
    B=((oxs[oiB] - OB_[0]) / OW, (oys[oiB] - OB_[2]) / OH),
    wfrac=[float((np.nonzero(OMF[y])[0].max() - np.nonzero(OMF[y])[0].min() + 1) / OW)
           if OMF[y].any() else 0.0 for y in range(BH)],
)
# bottom taper: row width fraction at rows near bottom (local y 120..180)
ORIG_TAPER = ORIG_SHAPE["wfrac"][120:181]
ORIG_REF = ref
BAND = (672, 472, 816, 517)
OBAND = ORIG[BAND[1]:BAND[3], BAND[0]:BAND[2]]

_N = 90
_X = np.linspace(-3, 3, _N)
_XG, _YG = np.meshgrid(_X, _X)
WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def br_surface(X, Y, vdepth=1.0):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * vdepth * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * vdepth * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * vdepth * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


_ZG = {1.0: br_surface(_XG, _YG, 1.0)}


def render(azim, elev, zoom, zfac, pad_lo, vdepth=1.0, path=False):
    ZG = _ZG.setdefault(vdepth, br_surface(_XG, _YG, vdepth))
    zmin, zmax = float(ZG.min()), float(ZG.max())
    rng = zmax - zmin
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d", proj_type="ortho")
    ax.view_init(elev=elev, azim=azim)
    norm = Normalize(zmin - pad_lo * rng, zmax)
    ax.plot_surface(_XG, _YG, ZG, cmap=plt.get_cmap("jet"), norm=norm, shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    if path:
        t = np.linspace(0, 1, len(WAYPOINTS))
        ts = np.linspace(0, 1, 240)
        sx = CubicSpline(t, WAYPOINTS[:, 0])(ts)
        sy = CubicSpline(t, WAYPOINTS[:, 1])(ts)
        sz = np.array([float(br_surface(np.array(a), np.array(b), vdepth)) for a, b in zip(sx, sy)]) + 0.12
        ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, 6.0 * zfac), zoom=zoom)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


def surf_mask_buf(buf, border=2):
    m = colmask(buf)
    m[:border] = False; m[-border:] = False; m[:, :border] = False; m[:, -border:] = False
    return m


def composite(buf):
    im = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[45:540, 54:904] = np.array([233, 233, 231], np.int32)
    canvas[Y0:Y0 + BH, X0:X0 + BW] = np.asarray(im).astype(np.int32)
    return canvas


def shape_of(buf):
    """scale-invariant silhouette shape from a raw render buf"""
    m = surf_mask_buf(buf)
    ys, xs = np.nonzero(m)
    if len(xs) < 50:
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    W, H = x1 - x0 + 1, y1 - y0 + 1
    iL, iR, iT, iB = xs.argmin(), xs.argmax(), ys.argmin(), ys.argmax()
    wf = []
    for y in range(m.shape[0]):
        xx = np.nonzero(m[y])[0]
        wf.append((xx.max() - xx.min() + 1) / W if len(xx) else 0.0)
    return dict(L=((xs[iL] - x0) / W, (ys[iL] - y0) / H),
                R=((xs[iR] - x0) / W, (ys[iR] - y0) / H),
                T=((xs[iT] - x0) / W, (ys[iT] - y0) / H),
                B=((xs[iB] - x0) / W, (ys[iB] - y0) / H),
                wfrac=wf, W=W, H=H, fx=W / buf.shape[1], fy=H / buf.shape[0])


def shape_err(sh):
    e = 0.0
    for k in ("L", "R", "T", "B"):
        e += float(np.hypot(sh[k][0] - ORIG_SHAPE[k][0], sh[k][1] - ORIG_SHAPE[k][1]))
    # taper: compare row-width profile over bottom 40% rows
    H = sh["H"]
    y0 = int(0.60 * len(sh["wfrac"]))
    a = np.array(sh["wfrac"][y0:])
    b = np.array(ORIG_SHAPE["wfrac"][y0:])
    n = min(len(a), len(b))
    e += 8.0 * float(np.abs(a[:n] - b[:n]).mean())
    return e


def zoom_for(azim, elev, zfac, pad_lo, vdepth, tfx=0.906, tfy=0.899):
    """binary search zoom to match figure fracs (ortho => linear, 5 iters enough)"""
    lo, hi = 0.05, 30.0
    for _ in range(5):
        zm = np.sqrt(lo * hi)
        buf = render(azim, elev, zm, zfac, pad_lo, vdepth)
        sh = shape_of(buf)
        if sh is None:
            lo = zm; continue
        if sh["fx"] < tfx and sh["fy"] < tfy:
            lo = zm
        else:
            hi = zm
    return np.sqrt(lo * hi), lo


def metrics(canvas):
    rb = canvas[Y0 + P:Y0 + BH - P, X0 + P:X0 + BW - P]
    m = colmask(rb)
    out = dict(colored=float(m.mean()), hist_dist=1.0, diag=None, ext_err=999.0,
               band=1.0, prof_err=99.0, env_err=999.0, col_err=1.0,
               bbox=None, L=None, R=None, T=None, B=None, fx=0, fy=0)
    if m.sum() < 50:
        return out
    ys, xs = np.nonzero(m)
    out["bbox"] = [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())]
    iL, iR, iT, iB = xs.argmin(), xs.argmax(), ys.argmin(), ys.argmax()
    out["L"] = [int(xs[iL]), int(ys[iL])]; out["R"] = [int(xs[iR]), int(ys[iR])]
    out["T"] = [int(xs[iT]), int(ys[iT])]; out["B"] = [int(xs[iB]), int(ys[iB])]
    out["fx"] = (xs.max() - xs.min() + 1) / m.shape[1]
    out["fy"] = (ys.max() - ys.min() + 1) / m.shape[0]
    t = jet_t(rb[ys, xs])
    h = np.histogram(t, bins=16, range=(0, 1))[0]; h = h / h.sum()
    out["hist_dist"] = float(0.5 * np.abs(h - ORIG_HIST).sum())
    bx0, bx1, by0, by1 = out["bbox"]
    dgm = np.abs((xs - bx0) - (ys - by0)) <= 2
    td = t[dgm] if dgm.sum() > 10 else t
    out["diag"] = dict(mean=float(td.mean()), std=float(td.std()),
                       min=float(td.min()), max=float(td.max()))
    rm = colmask(canvas[Y0:Y0 + BH, X0:X0 + BW])
    rprof = 100.0 * rm.mean(1)
    omp = OMF.copy(); omp[:8]=False; omp[-8:]=False; omp[:,:8]=False; omp[:,-8:]=False
    a, b = ref["rowprof_range"]
    out["prof_err"] = float(np.abs(rprof[a:b] - np.array(ref["rowprof"][a:b])).mean())
    rw = np.zeros(BH); co = np.zeros(BW)
    for y in range(BH):
        xx = np.nonzero(rm[y])[0]
        rw[y] = (xx.max() - xx.min() + 1) if len(xx) else 0
    for x in range(BW):
        yy = np.nonzero(rm[:, x])[0]
        co[x] = (yy.max() - yy.min() + 1) if len(yy) else 0
    orw = np.zeros(BH); oco = np.zeros(BW)
    for y in range(BH):
        xx = np.nonzero(omp[y])[0]
        orw[y] = (xx.max() - xx.min() + 1) if len(xx) else 0
    for x in range(BW):
        yy = np.nonzero(omp[:, x])[0]
        oco[x] = (yy.max() - yy.min() + 1) if len(yy) else 0
    out["env_err"] = float((np.abs(rw - orw).mean() + np.abs(co - oco).mean()) / 2)
    rband = canvas[BAND[1]:BAND[3], BAND[0]:BAND[2]]
    out["band"] = float((np.abs(OBAND - rband).sum(2) > 60).mean())
    e = 0.0
    for k in ("L", "R", "T", "B"):
        e += float(np.hypot(out[k][0] - ref[k][0], out[k][1] - ref[k][1]))
    out["ext_err"] = e
    out["col_err"] = abs(out["colored"] - ref["colored"])
    return out


def wind(canvas):
    br = canvas[Y0 + P:Y0 + BH - P, X0 + P:X0 + BW - P]
    lum = 0.299 * br[:, :, 0] + 0.587 * br[:, :, 1] + 0.114 * br[:, :, 2]
    dm = (lum < 100) & ((br.max(2) - br.min(2)) < 80)
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 15:
            continue
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs, ys)
    if best is None:
        return None
    _, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    return seg / max(straight, 1.0)


RES = os.path.join(RJ, "search_k17j4_results.txt")


def log(line):
    with open(RES, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "A"
    if stage == "A":
        if os.path.exists(RES):
            os.remove(RES)
        results = []
        for azim in range(-100, -19, 10):
            for elev in range(10, 71, 10):
                for zfac in (0.15, 0.3, 0.5, 0.75, 1.0, 1.4):
                    buf = render(azim, elev, 0.9, zfac, 0.3)
                    sh = shape_of(buf)
                    if sh is None:
                        continue
                    e = shape_err(sh)
                    results.append((e, azim, elev, zfac, sh))
                    log("A shape_err=%.4f azim=%d elev=%d zfac=%.2f L=(%.2f,%.2f) R=(%.2f,%.2f) T=(%.2f,%.2f) B=(%.2f,%.2f)" % (
                        e, azim, elev, zfac, sh["L"][0], sh["L"][1], sh["R"][0], sh["R"][1],
                        sh["T"][0], sh["T"][1], sh["B"][0], sh["B"][1]))
        results.sort(key=lambda r: r[0])
        print("orig shape: L=(%.2f,%.2f) R=(%.2f,%.2f) T=(%.2f,%.2f) B=(%.2f,%.2f)" % (
            ORIG_SHAPE["L"][0], ORIG_SHAPE["L"][1], ORIG_SHAPE["R"][0], ORIG_SHAPE["R"][1],
            ORIG_SHAPE["T"][0], ORIG_SHAPE["T"][1], ORIG_SHAPE["B"][0], ORIG_SHAPE["B"][1]))
        with open(os.path.join(RJ, "search_k17j4_bestA.txt"), "w") as f:
            for e, azim, elev, zfac, sh in results[:40]:
                f.write("shape_err=%.4f azim=%d elev=%d zfac=%.2f\n" % (e, azim, elev, zfac))
        print("TOP A shape:")
        for e, azim, elev, zfac, sh in results[:12]:
            print("  err=%.4f azim=%d elev=%d zfac=%.2f" % (e, azim, elev, zfac))
    elif stage == "B":
        bestA = []
        with open(os.path.join(RJ, "search_k17j4_bestA.txt")) as f:
            for line in f:
                if line.startswith("shape_err="):
                    p = line.split()
                    bestA.append(dict(azim=int(p[1].split("=")[1]), elev=int(p[2].split("=")[1]),
                                      zfac=float(p[3].split("=")[1])))
        results = []
        for g in bestA[:8]:
            for pad_lo in (0.0, 0.2, 0.4):
                for vdepth in (1.0, 1.4):
                    zoom, lo = zoom_for(g["azim"], g["elev"], g["zfac"], pad_lo, vdepth)
                    buf = render(g["azim"], g["elev"], zoom, g["zfac"], pad_lo, vdepth, path=True)
                    canv = composite(buf)
                    m = metrics(canv)
                    w = wind(canv)
                    d = m["diag"]
                    sB = (30.0 * m["hist_dist"] + 60.0 * (abs(d["mean"] - ref["diag"]["mean"])
                            + abs(d["std"] - ref["diag"]["std"]) + abs(d["min"] - ref["diag"]["min"])
                            + abs(d["max"] - ref["diag"]["max"])))
                    sA = m["ext_err"] + 2.0 * m["env_err"] + 3.0 * m["prof_err"] + 150.0 * m["band"] + 60.0 * m["col_err"]
                    results.append((sB, sA, g["azim"], g["elev"], g["zfac"], zoom, pad_lo, vdepth, m, w))
                    log("B scoreB=%.2f scoreA=%.2f azim=%d elev=%d zfac=%.2f zoom=%.3f pad=%.2f vd=%.1f hist=%.3f diag=%.3f/%.3f/%.2f/%.2f env=%.2f prof=%.2f band=%.3f col=%.4f ext=%.1f wind=%s" % (
                        sB, sA, g["azim"], g["elev"], g["zfac"], zoom, pad_lo, vdepth, m["hist_dist"],
                        d["mean"], d["std"], d["min"], d["max"], m["env_err"], m["prof_err"],
                        m["band"], m["colored"], m["ext_err"], ("%.3f" % w) if w else "-"))
        results.sort(key=lambda r: r[0])
        with open(os.path.join(RJ, "search_k17j4_bestB.txt"), "w") as f:
            for sB, sA, azim, elev, zfac, zoom, pad_lo, vdepth, m, w in results[:40]:
                d = m["diag"]
                f.write("scoreB=%.2f scoreA=%.2f azim=%d elev=%d zfac=%.2f zoom=%.4f pad=%.2f vd=%.1f hist=%.3f diag=%.3f/%.3f/%.2f/%.2f env=%.2f prof=%.2f band=%.3f col=%.4f ext=%.1f wind=%s bbox=%s L=%s R=%s T=%s B=%s\n" % (
                    sB, sA, azim, elev, zfac, zoom, pad_lo, vdepth, m["hist_dist"],
                    d["mean"], d["std"], d["min"], d["max"], m["env_err"], m["prof_err"],
                    m["band"], m["colored"], m["ext_err"], ("%.3f" % w) if w else "-",
                    m["bbox"], m["L"], m["R"], m["T"], m["B"]))
        print("TOP B:")
        for r in results[:12]:
            print("  B=%.2f A=%.2f azim=%d elev=%d zfac=%.2f zoom=%.3f pad=%.2f vd=%.1f wind=%s band=%.3f env=%.1f" % (
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], ("%.2f" % r[9]) if r[9] else "-",
                r[8]["band"], r[8]["env_err"]))
