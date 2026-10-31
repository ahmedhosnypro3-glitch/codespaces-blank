#!/usr/bin/env python3
"""k17j stage C: fine refine around stage-B winners (azim -65..-55, elev 25..40)."""
import os, sys
import numpy as np
import search_k17j4 as S

RJ = S.RJ
RES = os.path.join(RJ, "search_k17j5_results.txt")
BEST = os.path.join(RJ, "search_k17j5_best.txt")


def log(line):
    with open(RES, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


if __name__ == "__main__":
    if os.path.exists(RES):
        os.remove(RES)
    ref = S.ref
    results = []
    combos = []
    for azim in (-65, -60, -55):
        for elev in (25, 30, 35, 40):
            for zfac in (0.75, 1.0):
                for vd in (1.0, 1.4):
                    combos.append((azim, elev, zfac, vd))
    for azim, elev, zfac, vd in combos:
        if zfac == 1.0 and elev in (30, 40):
            combos.append((azim, elev, zfac, 1.8))
    seen = set()
    for azim, elev, zfac, vd in combos:
        key = (azim, elev, zfac, vd)
        if key in seen:
            continue
        seen.add(key)
        zoom, lo = S.zoom_for(azim, elev, zfac, 0.0, vd)
        buf = S.render(azim, elev, zoom, zfac, 0.0, vd, path=True)
        canv = S.composite(buf)
        m = S.metrics(canv)
        w = S.wind(canv)
        d = m["diag"]
        s = (30.0 * m["hist_dist"]
             + 60.0 * (abs(d["mean"] - ref["diag"]["mean"]) + abs(d["std"] - ref["diag"]["std"])
                       + abs(d["min"] - ref["diag"]["min"]) + abs(d["max"] - ref["diag"]["max"]))
             + 60.0 * abs(m["colored"] - ref["colored"]) + 150.0 * m["band"]
             + 0.5 * m["ext_err"] + 2.0 * m["env_err"] + 3.0 * m["prof_err"]
             + (3.0 * abs(w - 6.02) if w else 50.0))
        results.append((s, azim, elev, zfac, zoom, vd, m, w))
        log("C score=%.2f azim=%d elev=%d zfac=%.2f zoom=%.4f vd=%.1f hist=%.3f diag=%.3f/%.3f/%.2f/%.2f env=%.2f prof=%.2f band=%.3f col=%.4f ext=%.1f wind=%s bbox=%s" % (
            s, azim, elev, zfac, zoom, vd, m["hist_dist"],
            d["mean"], d["std"], d["min"], d["max"], m["env_err"], m["prof_err"],
            m["band"], m["colored"], m["ext_err"], ("%.3f" % w) if w else "-", m["bbox"]))
    results.sort(key=lambda r: r[0])
    with open(BEST, "w") as f:
        for s, azim, elev, zfac, zoom, vd, m, w in results[:30]:
            d = m["diag"]
            f.write("score=%.2f azim=%d elev=%d zfac=%.2f zoom=%.4f vd=%.1f hist=%.3f diag=%.3f/%.3f/%.2f/%.2f env=%.2f prof=%.2f band=%.3f col=%.4f ext=%.1f wind=%s bbox=%s\n" % (
                s, azim, elev, zfac, zoom, vd, m["hist_dist"],
                d["mean"], d["std"], d["min"], d["max"], m["env_err"], m["prof_err"],
                m["band"], m["colored"], m["ext_err"], ("%.3f" % w) if w else "-", m["bbox"]))
    print("TOP C:")
    for r in results[:10]:
        print("  score=%.2f azim=%d elev=%d zfac=%.2f zoom=%.3f vd=%.1f wind=%s col=%.3f band=%.3f" % (
            r[0], r[1], r[2], r[3], r[4], r[5], ("%.2f" % r[7]) if r[7] else "-", r[6]["colored"], r[6]["band"]))
