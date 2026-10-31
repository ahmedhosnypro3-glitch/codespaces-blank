#!/usr/bin/env python3
"""One sweeper pass for 08_performance_measure.

For each slide N in 1..37 not yet certified in final_deck_ledger.json:
  - qa dirs matching recreated_pptx/qa/slide_?0*N
  - newest render*.png mtime R (across matching dirs)
  - judge_attempt_*.txt with verdict PASS and mtime > R
  - newest judge_verify_*.txt: if its verdict is FAIL -> skip slide
  - else a judge_verify_*.txt with verdict PASS and mtime > R
Qualifying slides are merged: flock-append ledger row, merge_final_deck.py
update, mission.db scope done, confirm ledger. Prints one line per action.
"""
import fcntl
import glob
import json
import os
import re
import subprocess
import sys
import time

NS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(NS)
sys.path.insert(0, os.path.join(NS, "pool_run"))
from verdict import verdict  # noqa: E402

QA = os.path.join(NS, "recreated_pptx", "qa")
LEDGER = os.path.join(NS, "pool_run", "verification_ledger.md")
MERGE = os.path.join(NS, "pool_run", "merge_final_deck.py")
DB = os.path.join(NS, "pool_run", "mission.db")
DECK = "08-performance_final.pptx"


def certified_set():
    with open(os.path.join(NS, "final_deck_ledger.json")) as fh:
        d = json.load(fh)
    return {p["slide_num"] for p in d["pages"] if p["status"] == "certified"}


def qa_dirs(n):
    pat = re.compile(r"slide_?0*%d$" % n)
    return [os.path.join(QA, sd) for sd in sorted(os.listdir(QA))
            if pat.match(sd) and os.path.isdir(os.path.join(QA, sd))]


def scan():
    cert = certified_set()
    found = []
    for n in range(1, 38):
        if n in cert:
            continue
        dirs = qa_dirs(n)
        renders, attempts, verifies = [], [], []
        for dp in dirs:
            renders += glob.glob(os.path.join(dp, "render*.png"))
            attempts += [f for f in glob.glob(os.path.join(dp, "judge_attempt_*.txt"))
                         if f.endswith(".txt")]
            verifies += [f for f in glob.glob(os.path.join(dp, "judge_verify_*.txt"))
                         if f.endswith(".txt")]
        if not renders:
            continue
        newest = max(renders, key=os.path.getmtime)
        R = os.path.getmtime(newest)
        ap = [f for f in attempts
              if verdict(f) == "PASS" and os.path.getmtime(f) > R]
        vers = sorted(verifies, key=os.path.getmtime)
        if not vers:
            continue
        if verdict(vers[-1]) == "FAIL":
            continue  # newest verify FAIL -> slide re-opened, skip
        vp = [f for f in vers
              if verdict(f) == "PASS" and os.path.getmtime(f) > R]
        if not ap or not vp:
            continue
        found.append((n, max(ap, key=os.path.getmtime),
                      max(vp, key=os.path.getmtime), newest))
    return found, cert


def source_path(n):
    for p in (f"analysis/reanalysis/slide_{n:03d}_raw.json",
              f"analysis/slide_{n:03d}_raw.json",
              f"analysis/slide_{n:03d}_final.json"):
        if os.path.exists(os.path.join(NS, p)):
            return p
    return "-"


def append_ledger(row):
    with open(LEDGER, "a") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(row + "\n")
        fcntl.flock(fh, fcntl.LOCK_UN)


def merge(n):
    src = os.path.join(NS, "recreated_pptx", f"slide_{n:03d}_recreated.pptx")
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    if not os.path.exists(src):
        append_ledger(f"| {n} | — | — | — | {source_path(n)} | no | "
                      f"merge skipped by sweeper-pm08 {ts}: {src} missing |")
        print(f"slide {n}: MISSING pptx, ledger row recorded")
        return False
    r = subprocess.run([sys.executable, MERGE, "update", str(n), src, DECK],
                       capture_output=True, text=True, cwd=NS)
    ok = r.returncode == 0 and "updated" in (r.stdout or "")
    confirm = n in certified_set()
    if ok:
        subprocess.run(["sqlite3", DB,
                        f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                       check=False)
    row = (f"| {n} | `{attempt}` | `{verify}` | PASS / PASS | "
           f"{source_path(n)} | {'yes' if confirm else 'no'} | "
           f"sweeper-pm08 {ts} merge={'OK' if ok else 'FAILED: ' + (r.stderr or r.stdout).strip()[:200]} "
           f"ledger_confirmed={confirm} |")
    append_ledger(row)
    print(f"slide {n}: merge={'OK' if ok else 'FAILED'} confirmed={confirm} "
          f"attempt={os.path.basename(attempt)} verify={os.path.basename(verify)}")
    return confirm


if __name__ == "__main__":
    found, cert = scan()
    if not found:
        print(f"pass {time.strftime('%H:%M:%S')}: certified={len(cert)}/37, "
              f"no new qualifying slides")
    for n, attempt, verify, newest in found:
        globals()["attempt"], globals()["verify"] = attempt, verify
        merge(n)
    cert = certified_set()
    print(f"pass {time.strftime('%H:%M:%S')}: certified={len(cert)}/37")
    if len(cert) == 37:
        print("ALL37")
