#!/usr/bin/env python3
"""r5 promoter poll: every 120s scan pil_k17*_out.txt for a FULL PASS set.

Full pass = CHECK1 PASS + CHECK2 PASS + CHECK3 PASS + wind-ratio in [4,7]
+ markers PASS, on a 4-file assets_k17* set whose 4 md5s all differ from
assets_k15. On first full pass writes FULLPASS_r5.txt naming the set and
keeps logging (does not promote). Deadline 2.5h from start.
"""
import hashlib
import os
import re
import sys
import time

RJ = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025"
LOG = os.path.join(RJ, "watch_r5.log")
FLAG = os.path.join(RJ, "FULLPASS_r5.txt")
K15 = os.path.join(RJ, "assets_k15")
DEADLINE = 2.5 * 3600
NAMES = ["tl", "tr", "bl", "br"]


def log(s):
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + s
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def assets_for(pilname):
    base = os.path.basename(pilname)
    core = base[len("pil_"):]
    core = re.sub(r"_out.*$", "", core)
    for cand in (core, core + "2"):
        d = os.path.join(RJ, "assets_" + cand)
        if os.path.isdir(d):
            return d
    return None


def evaluate(pilfile):
    """Return (ok, detail) for a pil_k17*_out.txt."""
    try:
        text = open(pilfile).read()
    except OSError:
        return False, "unreadable"
    if os.path.basename(pilfile).endswith((".bak", ".bank")):
        return False, "bak"
    adir = assets_for(pilfile)
    if not adir:
        return False, "no assets dir"
    files = [os.path.join(adir, "plot_025_%s.png" % n) for n in NAMES]
    if not all(os.path.isfile(f) for f in files):
        return False, "not a 4-file set (%s)" % os.path.basename(adir)
    k15md5 = {n: md5(os.path.join(K15, "plot_025_%s.png" % n)) for n in NAMES}
    alldiff = all(md5(f) != k15md5[n] for f, n in zip(files, NAMES))
    lines = text.splitlines()

    def check(tag):
        has_pass = any(re.search(tag + r"[^\n]*PASS", l, re.I) for l in lines)
        has_fail = any(re.search(tag + r"[^\n]*FAIL", l, re.I) for l in lines)
        return has_pass and not has_fail

    c1, c2, c3 = check("CHECK1"), check("CHECK2"), check("CHECK3")
    wind_vals = [float(m) for m in re.findall(r"wind-ratio[=: ]+([0-9]+\.?[0-9]*)", text)]
    if not wind_vals:
        for l in lines:
            if "winding" in l.lower() and "target" not in l.lower():
                m = re.search(r"([0-9]+\.[0-9]+)", l)
                if m:
                    wind_vals.append(float(m.group(1)))
    winding_ok = any(4.0 <= v <= 7.0 for v in wind_vals)
    mlines = [l for l in lines if "marker" in l.lower()]
    m_pass = any(re.search(r"PASS", l, re.I) for l in mlines)
    m_fail = any(re.search(r"FAIL", l, re.I) for l in mlines)
    markers_ok = m_pass and not m_fail
    ok = c1 and c2 and c3 and winding_ok and markers_ok and alldiff
    detail = "c1=%s c2=%s c3=%s wind=%s(%s) markers=%s alldiff=%s" % (
        c1, c2, c3, winding_ok, wind_vals, markers_ok, alldiff)
    return ok, detail


def main():
    start = time.time()
    log("r5 poll start; deadline 2.5h; scanning %s/pil_k17*_out.txt" % RJ)
    seen_pass = False
    while time.time() - start < DEADLINE:
        pils = sorted(
            os.path.join(RJ, f) for f in os.listdir(RJ)
            if f.startswith("pil_k17") and f.endswith(".txt")
        )
        for p in pils:
            ok, detail = evaluate(p)
            log("scan %s -> %s [%s]" % (os.path.basename(p), "FULLPASS" if ok else "no", detail))
            if ok and not seen_pass:
                seen_pass = True
                adir = assets_for(p)
                with open(FLAG, "w") as f:
                    f.write("set=%s\npil=%s\nassets=%s\ntime=%s\n"
                            % (os.path.basename(adir), p, adir,
                               time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
                log("*** FULLPASS DETECTED: %s (pil %s) — flag written %s" % (adir, p, FLAG))
        if not seen_pass and os.path.exists(FLAG):
            seen_pass = True
        time.sleep(120)
    log("r5 poll deadline reached (2.5h); flag=%s" % (os.path.exists(FLAG)))


if __name__ == "__main__":
    main()
