#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure (h2 lane).

Every --interval seconds, scan slides 1..37. For each slide NOT certified in
final_deck_ledger.json: find qa dirs under recreated_pptx/qa/ matching
^slide_?0*N$, take newest render*.png mtime R, and look for judge_attempt*.txt
and judge_verify*.txt that contain 'FINAL VERDICT: PASS' with mtime > R.
If BOTH exist (dual PASS newer than newest render), merge:
  1. flock-append one row to pool_run/verification_ledger.md
  2. python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
  3. sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"
Each merge and each scan summary is logged to pool_run/hygiene2.log (UTC).
Never merges on a single PASS or a PASS older than the newest render.
"""
import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(ROOT, 'recreated_pptx', 'qa')
LEDGER_JSON = os.path.join(ROOT, 'final_deck_ledger.json')
VLEDGER = os.path.join(ROOT, 'pool_run', 'verification_ledger.md')
DB = os.path.join(ROOT, 'pool_run', 'mission.db')
HYG = os.path.join(ROOT, 'pool_run', 'hygiene2.log')
DECK = '08-performance_final.pptx'
N_SLIDES = 37


def utcnow():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def hlog(msg):
    line = f"{utcnow()} {msg}"
    with open(HYG, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
    print(line, flush=True)


def certified_set():
    try:
        with open(LEDGER_JSON) as f:
            d = json.load(f)
        return {p['slide_num'] for p in d['pages'] if p.get('status') == 'certified'}
    except Exception:
        return set()


def qa_dirs_for(n):
    pat = re.compile(r'slide_?0*%d$' % n)
    out = []
    if not os.path.isdir(QA):
        return out
    for d in sorted(os.listdir(QA)):
        if pat.fullmatch(d) and os.path.isdir(os.path.join(QA, d)):
            out.append(os.path.join(QA, d))
    return out


def has_pass(path):
    try:
        with open(path, errors='replace') as f:
            return 'FINAL VERDICT: PASS' in f.read()
    except OSError:
        return False


def find_dual_pass(n):
    """Return (qa_dir, attempt_file, verify_file) if dual PASS newer than newest render."""
    for dd in qa_dirs_for(n):
        try:
            files = os.listdir(dd)
        except OSError:
            continue
        renders = [f for f in files if f.startswith('render') and f.endswith('.png')]
        r = max((os.path.getmtime(os.path.join(dd, f)) for f in renders), default=0.0)
        att = [f for f in files
               if re.fullmatch(r'judge_attempt.*\.txt', f)
               and has_pass(os.path.join(dd, f))
               and os.path.getmtime(os.path.join(dd, f)) > r]
        ver = [f for f in files
               if re.fullmatch(r'judge_verify.*\.txt', f)
               and has_pass(os.path.join(dd, f))
               and os.path.getmtime(os.path.join(dd, f)) > r]
        if att and ver:
            att.sort(key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            ver.sort(key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            return dd, att[-1], ver[-1]
    return None


def merge(n, qa_dir, attempt, verify):
    rel_qa = os.path.relpath(qa_dir, ROOT)
    reanalysis = f'analysis/reanalysis/slide_{n:03d}_raw.json'
    if not os.path.exists(os.path.join(ROOT, reanalysis)):
        reanalysis = f'analysis/slide_{n:03d}_final.json'
    row = (f"| {n} | {rel_qa}/{attempt} | {rel_qa}/{verify} | "
           f"PASS (dual-read, original-first, both newer than newest render) | "
           f"{reanalysis} | certified=yes | sweeper-h2 {utcnow()} |")
    with open(VLEDGER, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
    hlog(f"ledger-row appended slide={n} attempt={rel_qa}/{attempt} verify={rel_qa}/{verify} verdict=PASS reanalysis={reanalysis} certified=yes")

    pptx_rel = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    p = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update', str(n),
                        pptx_rel, DECK], cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0 or n not in certified_set():
        hlog(f"MERGE-FAILED slide={n} rc={p.returncode} err={p.stderr.strip()[:300]}")
        return False
    hlog(f"MERGE slide={n} deck={DECK} source={pptx_rel} deck_ledger=certified")

    q = subprocess.run(['sqlite3', DB,
                        f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                       cwd=ROOT, capture_output=True, text=True)
    if q.returncode != 0:
        hlog(f"DB-FAILED slide={n} err={q.stderr.strip()[:200]}")
        return False
    hlog(f"DB slide-{n} status=done")
    return True


def scan_once():
    cert = certified_set()
    merged = []
    pending = []
    for n in range(1, N_SLIDES + 1):
        if n in cert:
            continue
        # re-check right before merging to avoid racing other sweepers
        found = find_dual_pass(n)
        if not found:
            pending.append(n)
            continue
        if n in certified_set():
            continue
        qa_dir, att, ver = found
        if merge(n, qa_dir, att, ver):
            merged.append(n)
            cert.add(n)
        else:
            pending.append(n)
    return cert, merged, pending


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--budget', type=int, default=7200, help='total loop budget seconds')
    ap.add_argument('--interval', type=int, default=90)
    ap.add_argument('--once', action='store_true')
    args = ap.parse_args()
    deadline = time.time() + args.budget
    hlog(f"sweeper-h2 start budget={args.budget}s interval={args.interval}s")
    while True:
        cert, merged, pending = scan_once()
        hlog(f"scan certified={len(cert)}/{N_SLIDES} merged={merged or '-'} "
             f"pending={pending if pending else '-'}")
        if len(cert) >= N_SLIDES:
            hlog(f"sweeper-h2 done: all {N_SLIDES} slides certified")
            return 0
        if args.once or time.time() >= deadline:
            hlog(f"sweeper-h2 stop budget_exhausted={not args.once} certified={len(cert)}/{N_SLIDES}")
            return 0
        time.sleep(max(1, min(args.interval, int(deadline - time.time()))))


if __name__ == '__main__':
    sys.exit(main())
