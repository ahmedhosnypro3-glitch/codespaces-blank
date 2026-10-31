#!/usr/bin/env python3
"""k17j fast BR search v2: analytic zoom (calibrate at zoom=1, scale, verify).
Stage A: geometry grid (azim, elev, zfac) with pad_lo=0.3.
Stage B: top-A x (pad_lo, vdepth) with winding path, full metrics.
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
OB = ORIG[Y0 + P:Y0 + BH - P, X0 + P:X0 + BW - P]


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~red


def jet_t(px):
    d = ((JET_LUT[None, :, :] - px[:, None, :].astype(np.float64)) ** 2).sum(2)
    return d.argmin(1) / 255.0


OM = colmask(OB)
OYS, OXS = np.nonzero(OM)
_iL, _iR, _iT, _iB = OXS.argmin(), OXS.argmax(), OYS.argmin(), OYS.argmax()
ORIG_REF = dict(
    bbox=[int(OXS.min()), int(OXS.max()), int(OYS.min()), int(OYS.max())],
    L=[int(OXS[_iL]), int(OYS[_iL])], R=[int(OXS[_iR]), int(OYS[_iR])],
    T=[int(OXS[_iT]), int(OYS[_iT])], B=[int(OXS[_iB]), int(OYS[_iB])],
    colored=float(OM.mean()),
    hist=np.histogram(jet_t(OB[OM]), bins=16, range=(0, 1))[0].tolist(),
)
bx0, bx1, by0, by1 = ORIG_REF["bbox"]
dg = np.abs((OXS - bx0) - (OYS - by0)) <= 2
_td = jet_t(OB[OYS[dg], OXS[dg]])
ORIG_REF["diag"] = dict(mean=float(_td.mean()), std=float(_td.std()),
                        min=float(_td.min()), max=float(_td.max()))
OMF = colmask(ORIG[Y0:Y0 + BH, X0:X0 + BW])
ORIG_REF["rowprof"] = (100.0 * OMF.mean(1)).tolist()
ORIG_REF["rowprof_range"] = [455 - Y0, 529 - Y0]
BAND = (672, 472, 816, 517)
OBAND = ORIG[BAND[1]:BAND[3], BAND[0]:BAND[2]]
with open(os.path.join(RJ, "search_k17j_orig_ref.json"), "w") as f:
    json.dump(ORIG_REF, f, indent=1)
ORIG_HIST = np.array(ORIG_REF["hist"], float); ORIG_HIST /= ORIG_HIST.sum()
print("orig ref: bbox=%s L=%s R=%s T=%s B=%s colored=%.4f diag=%s hist=%s" % (
    ORIG_REF["bbox"], ORIG_REF["L"], ORIG_REF["R"], ORIG_REF["T"], ORIG_REF["B"],
    ORIG_REF["colored"], ORIG_REF["diag"], ORIG_REF["hist"]), flush=True)

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


_ZG = {}
def get_Z(vdepth):
    if vdepth not in _ZG:
        _ZG[vdepth] = br_surface(_XG, _YG, vdepth)
    return _ZG[vdepth]


def render(azim, elev, zoom, zfac, pad_lo, vdepth=1.0, path=False):
    ZG = get_Z(vdepth)
    zmin, zmax = float(ZG.min()), float(ZG.max())
    rng = zmax - zmin
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
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
    ax.set_box_aspect((6, 6, rng * zfac), zoom=zoom)
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


def box_fracs(buf):
    m = surf_mask_buf(buf)
    ys, xs = np.nonzero(m)
    if not len(xs):
        return None
    return (xs.max() - xs.min() + 1) / buf.shape[1], (ys.max() - ys.min() + 1) / buf.shape[0]


def est_zoom(azim, elev, zfac, pad_lo, vdepth, capx=0.906, capy=0.899):
    buf = render(azim, elev, 1.0, zfac, pad_lo, vdepth)
    fr = box_fracs(buf)
    if fr is None:
        return 1.0
    fx, fy = fr
    if fx < 1e-3 or fy < 1e-3:
        return 1.0
    z = min(capx / fx, capy / fy) * 0.985
    return float(min(max(z, 0.05), 30.0))


def metrics(canvas):
    rb = canvas[Y0 + P:Y0 + BH - P, X0 + P:X0 + BW - P]
    m = colmask(rb)
    out = dict(colored=float(m.mean()), hist_dist=1.0, diag=None, fx=0, fy=0,
               bbox=None, L=None, R=None, T=None, B=None, band=1.0, prof_err=99.0,
               ext_err=999.0, col_err=1.0)
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
    a, b = ORIG_REF["rowprof_range"]
    out["prof_err"] = float(np.abs(rprof[a:b] - np.array(ORIG_REF["rowprof"][a:b])).mean())
    rband = canvas[BAND[1]:BAND[3], BAND[0]:BAND[2]]
    out["band"] = float((np.abs(OBAND - rband).sum(2) > 60).mean())
    e = 0.0
    for k in ("L", "R", "T", "B"):
        e += float(np.hypot(out[k][0] - ORIG_REF[k][0], out[k][1] - ORIG_REF[k][1]))
    out["ext_err"] = e
    out["col_err"] = abs(out["colored"] - ORIG_REF["colored"])
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


RES = os.path.join(RJ, "search_k17j2_results.txt")


def log(line):
    with open(RES, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def score_A(m):
    return (m["ext_err"] + 3.0 * m["prof_err"] + 60.0 * m["col_err"] + 150.0 * m["band"])


def score_B(m):
    d = m["diag"]
    return (30.0 * m["hist_dist"] + 60.0 * (abs(d["mean"] - ORIG_REF["diag"]["mean"])
            + abs(d["std"] - ORIG_REF["diag"]["std"]) + abs(d["min"] - ORIG_REF["diag"]["min"])
            + abs(d["max"] - ORIG_REF["diag"]["max"])))


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "A"
    if stage == "A":
        if os.path.exists(RES):
            os.remove(RES)
        results = []
        for azim in range(-105, -24, 15):
            for elev in range(15, 56, 10):
                for zfac in (0.7, 1.1, 1.5, 2.0, 2.6):
                    zoom = est_zoom(azim, elev, zfac, 0.3, 1.0)
                    buf = render(azim, elev, zoom, zfac, 0.3)
                    m = metrics(composite(buf))
                    s = score_A(m)
                    results.append((s, azim, elev, zfac, zoom, m))
                    log("A score=%.2f azim=%d elev=%d zfac=%.1f zoom=%.3f ext=%.1f prof=%.2f col=%.4f band=%.3f fx=%.3f fy=%.3f" % (
                        s, azim, elev, zfac, zoom, m["ext_err"], m["prof_err"], m["col_err"], m["band"], m["fx"], m["fy"]))
        results.sort(key=lambda r: r[0])
        with open(os.path.join(RJ, "search_k17j2_bestA.txt"), "w") as f:
            for s, azim, elev, zfac, zoom, m in results[:40]:
                f.write("score=%.2f azim=%d elev=%d zfac=%.2f zoom=%.4f bbox=%s L=%s R=%s T=%s B=%s colored=%.4f prof_err=%.2f band=%.3f ext=%.1f\n" % (
                    s, azim, elev, zfac, zoom, m["bbox"], m["L"], m["R"], m["T"], m["B"],
                    m["colored"], m["prof_err"], m["band"], m["ext_err"]))
        print("TOP A:")
        for s, azim, elev, zfac, zoom, m in results[:10]:
            print("  score=%.2f azim=%d elev=%d zfac=%.1f zoom=%.3f" % (s, azim, elev, zfac, zoom))
    elif stage == "B":
        bestA = []
        with open(os.path.join(RJ, "search_k17j2_bestA.txt")) as f:
            for line in f:
                if line.startswith("score="):
                    p = line.split()
                    bestA.append(dict(azim=int(p[1].split("=")[1]), elev=int(p[2].split("=")[1]),
                                      zfac=float(p[3].split("=")[1])))
        results = []
        for g in bestA[:10]:
            for pad_lo in (0.0, 0.1, 0.2, 0.3, 0.45):
                for vdepth in (1.0, 1.3, 1.6):
                    zoom = est_zoom(g["azim"], g["elev"], g["zfac"], pad_lo, vdepth)
                    buf = render(g["azim"], g["elev"], zoom, g["zfac"], pad_lo, vdepth, path=True)
                    canv = composite(buf)
                    m = metrics(canv)
                    w = wind(canv)
                    sB = score_B(m); sA = score_A(m)
                    results.append((sB, sA, g["azim"], g["elev"], g["zfac"], zoom, pad_lo, vdepth, m, w))
                    log("B scoreB=%.2f scoreA=%.2f azim=%d elev=%d zfac=%.1f zoom=%.3f pad=%.2f vd=%.1f hist=%.3f dmean=%.3f dstd=%.3f dmin=%.2f dmax=%.2f prof=%.2f band=%.3f col=%.4f ext=%.1f wind=%s" % (
                        sB, sA, g["azim"], g["elev"], g["zfac"], zoom, pad_lo, vdepth,
                        m["hist_dist"], m["diag"]["mean"], m["diag"]["std"], m["diag"]["min"], m["diag"]["max"],
                        m["prof_err"], m["band"], m["colored"], m["ext_err"], ("%.3f" % w) if w else "-"))
        results.sort(key=lambda r: r[0])
        with open(os.path.join(RJ, "search_k17j2_bestB.txt"), "w") as f:
            for sB, sA, azim, elev, zfac, zoom, pad_lo, vdepth, m, w in results[:40]:
                f.write("scoreB=%.2f scoreA=%.2f azim=%d elev=%d zfac=%.2f zoom=%.4f pad=%.2f vd=%.1f hist=%.3f diag=%.3f/%.3f/%.2f/%.2f prof=%.2f band=%.3f col=%.4f ext=%.1f wind=%s bbox=%s L=%s R=%s T=%s B=%s\n" % (
                    sB, sA, azim, elev, zfac, zoom, pad_lo, vdepth, m["hist_dist"],
                    m["diag"]["mean"], m["diag"]["std"], m["diag"]["min"], m["diag"]["max"],
                    m["prof_err"], m["band"], m["colored"], m["ext_err"], ("%.3f" % w) if w else "-",
                    m["bbox"], m["L"], m["R"], m["T"], m["B"]))
        print("TOP B:")
        for r in results[:10]:
            print("  B=%.2f A=%.2f azim=%d elev=%d zfac=%.1f zoom=%.3f pad=%.2f vd=%.1f wind=%s" % (
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], ("%.2f" % r[9]) if r[9] else "-"))
