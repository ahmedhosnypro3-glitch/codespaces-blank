#!/usr/bin/env python3
"""Backup-promoter watch for slide 025 k17 asset sets (agent-278 is primary).

Polls every ~3 min up to ~2h for any of assets_k17{a,b2,c,e,f,g} under
slide025/ containing 4 PNGs whose md5s all differ from assets_k15 AND a
pil_k17*_out.txt reporting CHECK1<50%, CHECK2 pass, CHECK3 present,
winding ~6.0. Also re-checks the progress DB each round: if slide 25 is
already passed/PASS, writes ALREADY_PASSED.txt and stops.
"""
import hashlib
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide025"
LOG = f"{D}/promoter_k17b_watch.log"
WIN = f"{D}/K17B_WINNER.txt"
DONE = f"{D}/ALREADY_PASSED.txt"
DB = f"{NS}/slides_progress.db"

K15 = {
    "5acfb177d1e4d640b2fd7a08a1f21eda",  # bl
    "500287a3f4fe98a32ee0cac44e5bd5f8",  # br
    "73cbaec1d8f2d9a6faf3aca1841b213e",  # tl
    "375a2d7bef424fe275a6c27647d09756",  # tr
}
CANDS = ["assets_k17a", "assets_k17b2", "assets_k17c", "assets_k17e", "assets_k17f", "assets_k17g"]
HANDLED = {"assets_k17g"}  # promoted 2026-10-31 ~07:15Z; legs FAILed PIL-confirmed — do not re-fire
PNGS = ["plot_025_tl.png", "plot_025_tr.png", "plot_025_bl.png", "plot_025_br.png"]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{now()} {msg}\n")


def db_state():
    try:
        con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=20)
        row = con.execute(
            "SELECT gen_status, visual_check FROM slides WHERE slide_id=25"
        ).fetchone()
        con.close()
        return row
    except Exception as e:
        return ("err", str(e))


def parse_pil(path):
    """Return (ok, detail) for CHECK1<50%, CHECK2 pass, CHECK3 present, winding ~6.0."""
    try:
        t = open(path, errors="replace").read()
    except Exception as e:
        return False, f"unreadable {e}"
    checks = {}
    for m in re.finditer(r"CHECK(\d)[^\n]*", t):
        checks.setdefault(m.group(1), m.group(0))
    c1, c2, c3 = checks.get("1", ""), checks.get("2", ""), checks.get("3", "")
    # CHECK1: percent < 50 and/or PASS on the CHECK1 line
    pcts = [float(x) for x in re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*%", c1)]
    c1_ok = ("PASS" in c1.upper()) and (not pcts or min(pcts) < 50.0)
    c2_ok = "PASS" in c2.upper()
    c3_ok = ("PASS" in c3.upper()) or ("PRESENT" in c3.upper())
    w = re.findall(r"wind(?:ing)?[- ]?ratio?[=:\s]*([0-9]+(?:\.[0-9]+)?)", t, re.I)
    wv = [float(x) for x in w]
    wind_ok = any(5.0 <= v <= 7.0 for v in wv)
    if not wind_ok:
        w2 = re.findall(r"wind(?:ing)?[^0-9]{0,20}([0-9]\.[0-9]+)", t, re.I)
        wind_ok = any(5.0 <= float(v) <= 7.0 for v in w2)
    ok = c1_ok and c2_ok and c3_ok and wind_ok
    detail = (f"CHECK1={'PASS' if c1_ok else 'FAIL'}(pcts={pcts}) "
              f"CHECK2={'PASS' if c2_ok else 'FAIL'} CHECK3={'ok' if c3_ok else 'no'} "
              f"winding={wv} -> {'OK' if wind_ok else 'no'}")
    return ok, detail


def qualify(dirpath):
    md5s = {}
    for n in PNGS:
        p = os.path.join(dirpath, n)
        if not os.path.isfile(p):
            return None
        m = md5(p)
        if m in K15:
            return None
        md5s[n] = m
    if len(set(md5s.values())) < 4:
        return None
    pils = sorted(
        (f for f in os.listdir(dirpath) if re.match(r"pil_k17.*_out\.txt$", f)),
        key=lambda f: os.path.getmtime(os.path.join(dirpath, f)),
    )
    suffix = os.path.basename(dirpath).replace("assets_", "")
    parent_pil = os.path.join(D, f"pil_{suffix}_out.txt")
    if os.path.isfile(parent_pil):
        pils.append(os.path.basename(parent_pil))
    if not pils:
        return None
    pil = max((os.path.join(D, p) for p in set(pils)),
              key=lambda p: os.path.getmtime(p))
    ok, detail = parse_pil(pil)
    if not ok:
        return None
    return {"dir": os.path.basename(dirpath), "md5s": md5s, "pil": pils[-1], "detail": detail}


def main():
    log(f"promoter watch start pid={os.getpid()} cands={CANDS}")
    deadline = time.time() + 2 * 3600 + 300
    while time.time() < deadline:
        row = db_state()
        if row and row[0] == "passed" and row[1] == "PASS":
            log(f"DB slide25 already passed/PASS ({row}) — stopping watch")
            with open(DONE, "w") as f:
                f.write(f"{now()} slide25 gen_status=passed visual_check=PASS — another promoter landed it\n")
            return 0
        found = []
        for c in CANDS:
            if c in HANDLED:
                continue
            dp = os.path.join(D, c)
            if os.path.isdir(dp):
                q = qualify(dp)
                if q:
                    found.append(q)
        if found:
            log("QUALIFYING SETS: " + "; ".join(f"{q['dir']} ({q['detail']})" for q in found))
            with open(WIN, "w") as f:
                f.write(f"{now()} WINNER dir={found[0]['dir']}\n")
                for q in found:
                    f.write(f"  {q['dir']}: pil={q['pil']} {q['detail']}\n")
                    for n, m in q["md5s"].items():
                        f.write(f"    {n} {m}\n")
            log(f"WROTE {WIN}")
            return 0
        # one-line status
        stat = []
        for c in CANDS:
            dp = os.path.join(D, c)
            if os.path.isdir(dp):
                np_ = sum(1 for n in PNGS if os.path.isfile(os.path.join(dp, n)))
                pil = [f for f in os.listdir(dp) if re.match(r"pil_k17.*_out\.txt$", f)]
                stat.append(f"{c}:pngs={np_}/4 pil={len(pil)}")
            else:
                stat.append(f"{c}:-")
        log("poll db=" + str(row) + " | " + " ".join(stat))
        time.sleep(180)
    log("WATCH TIMEOUT (2h) — no qualifying k17 set")
    return 1


if __name__ == "__main__":
    sys.exit(main())
