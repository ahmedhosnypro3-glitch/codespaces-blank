#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure (one scan pass).

Per slide N in 1..37 NOT certified in final_deck_ledger.json:
  - qa dirs under recreated_pptx/qa/ matching regex slide_?0*N (fullmatch)
  - R = newest mtime of render*.png in the dir
  - candidate iff some judge_attempt*.txt AND some judge_verify*.txt both
    contain 'FINAL VERDICT: PASS' and have mtime > R (dual PASS newer than
    the newest render). Never merges on a single PASS or a stale PASS.
On candidate, from the namespace root:
  1. flock-append one row to pool_run/verification_ledger.md
  2. python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
  3. sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"
Every merge and every scan summary is logged to pool_run/hygiene2.log with a
UTC timestamp. Append-only; never deletes evidence; never touches other
namespaces. Run from anywhere; paths resolve to this namespace root.
"""
import fcntl
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(ROOT, 'recreated_pptx', 'qa')
LEDGER_JSON = os.path.join(ROOT, 'final_deck_ledger.json')
VLEDGER = os.path.join(ROOT, 'pool_run', 'verification_ledger.md')
VLOCK = VLEDGER + '.lock'
DB = os.path.join(ROOT, 'pool_run', 'mission.db')
LOG = os.path.join(ROOT, 'pool_run', 'hygiene2.log')
DECK = '08-performance_final.pptx'
N_SLIDES = 37


def ts():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(msg):
    line = f"{ts()} {msg}"
    with open(LOG, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
    print(line, flush=True)


def has_pass(path):
    try:
        with open(path, errors='replace') as f:
            return 'FINAL VERDICT: PASS' in f.read()
    except OSError:
        return False


def certified_pages():
    with open(LEDGER_JSON) as f:
        return {p['slide_num'] for p in json.load(f)['pages'] if p['status'] == 'certified'}


def find_candidate(n):
    """Return (dir, attempt, verify, R) for slide n or None."""
    pat = re.compile(r'slide_?0*' + re.escape(str(n)) + r'$')
    best = None
    for d in sorted(os.listdir(QA)):
        if not pat.fullmatch(d):
            continue
        dd = os.path.join(QA, d)
        if not os.path.isdir(dd):
            continue
        files = os.listdir(dd)
        renders = [f for f in files if f.startswith('render') and f.endswith('.png')]
        R = max((os.path.getmtime(os.path.join(dd, f)) for f in renders), default=0.0)
        att = [f for f in files
               if re.fullmatch(r'judge_attempt.*\.txt', f)
               and os.path.getmtime(os.path.join(dd, f)) > R
               and has_pass(os.path.join(dd, f))]
        ver = [f for f in files
               if re.fullmatch(r'judge_verify.*\.txt', f)
               and os.path.getmtime(os.path.join(dd, f)) > R
               and has_pass(os.path.join(dd, f))]
        if att and ver:
            a = max(att, key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            v = max(ver, key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            key = os.path.getmtime(os.path.join(dd, v))
            if best is None or key > best[4]:
                best = (d, a, v, R, key)
    return best


def append_ledger_row(n, d, att, ver):
    reanalysis = f'analysis/reanalysis/slide_{n:03d}_raw.json'
    cell = reanalysis if os.path.exists(os.path.join(ROOT, reanalysis)) else '-'
    row = (f"| {n} | recreated_pptx/qa/{d}/{att} | recreated_pptx/qa/{d}/{ver} | "
           f"PASS / PASS (dual-read, both PASS transcripts newer than newest render) | "
           f"{cell} | certified=yes | appended by dualpass sweeper {ts()} |")
    with open(VLOCK, 'a') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        with open(VLEDGER, 'a') as f:
            f.write(row + '\n')
        fcntl.flock(lf, fcntl.LOCK_UN)


def merge_update(n):
    src = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    r = subprocess.run([sys.executable, os.path.join('pool_run', 'merge_final_deck.py'),
                        'update', str(n), src, DECK],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def db_set_done(n):
    r = subprocess.run(['sqlite3', os.path.join('pool_run', 'mission.db'),
                        f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def main():
    os.chdir(ROOT)
    cert = certified_pages()
    merged = []
    pending = []
    for n in range(1, N_SLIDES + 1):
        if n in cert:
            continue
        cand = find_candidate(n)
        if not cand:
            pending.append(n)
            continue
        d, att, ver, R, _ = cand
        src = os.path.join(ROOT, 'recreated_pptx', f'slide_{n:03d}_recreated.pptx')
        if not os.path.exists(src):
            log(f"scan slide-{n}: dual PASS in qa/{d} ({att}, {ver}) but {src} missing — skip")
            pending.append(n)
            continue
        append_ledger_row(n, d, att, ver)
        ok, out = merge_update(n)
        if not ok:
            log(f"MERGE-FAILED slide-{n}: {out}")
            continue
        ok2, out2 = db_set_done(n)
        cert.add(n)
        merged.append(n)
        log(f"MERGED slide-{n} qa/{d}/{att} + qa/{d}/{ver} (both PASS, mtime>newest render) "
            f"-> {DECK} page {n}; scope slide-{n} done={ok2} {out if not ok else ''}{out2 if not ok2 else ''}".strip())
    log(f"scan summary: certified={len(cert)}/{N_SLIDES} merged_this_pass={merged or '[]'} "
        f"still_pending={pending}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
