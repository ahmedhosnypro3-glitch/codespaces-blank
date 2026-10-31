#!/usr/bin/env python3
"""Certify-and-merge sweeper loop for 08_performance_measure (budget-bounded).

Every ~90s, scan slides 1..37. For each slide NOT certified in
final_deck_ledger.json: find qa dir matching ^slide_?0*N$ under
recreated_pptx/qa/, newest render png mtime R, then require a
judge_attempt*.txt AND a judge_verify*.txt that both contain
'FINAL VERDICT: PASS' with mtime > R. If both exist, merge:
  1. flock-append one row to pool_run/verification_ledger.md
  2. python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
  3. sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"
Logs merges and scan summaries to pool_run/hygiene2.log (UTC).
Runs until budget (default 2h) ends or all 37 slides certified.
"""
import fcntl
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / 'recreated_pptx' / 'qa'
LEDGER_JSON = ROOT / 'final_deck_ledger.json'
VLEDGER = ROOT / 'pool_run' / 'verification_ledger.md'
VLOCK = ROOT / 'pool_run' / 'verification_ledger.md.lock'
DB = ROOT / 'pool_run' / 'mission.db'
LOG = ROOT / 'pool_run' / 'hygiene2.log'
DECK = '08-performance_final.pptx'
N_SLIDES = 37
SCAN_INTERVAL = 90
PASS_MARK = 'FINAL VERDICT: PASS'


def utcnow():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(msg):
    line = f'{utcnow()} {msg}'
    with open(LOG, 'a') as f:
        f.write(line + '\n')
    print(line, flush=True)


def certified_set():
    ledger = json.load(open(LEDGER_JSON))
    return {int(p['slide_num']) for p in ledger['pages'] if p['status'] == 'certified'}


def find_qa_dir(n):
    rx = re.compile(rf'^slide_?0*{n}$')
    for d in sorted(QA.iterdir()):
        if d.is_dir() and rx.match(d.name):
            return d
    return None


def newest_render_mtime(qdir):
    best = None
    for f in qdir.rglob('*.png'):
        if 'render' in f.name.lower():
            m = f.stat().st_mtime
            if best is None or m > best:
                best = m
    return best


def pass_files(qdir, pattern, after):
    out = []
    if qdir is None:
        return out
    for f in sorted(qdir.rglob(pattern)):
        if not f.is_file():
            continue
        if f.stat().st_mtime <= after:
            continue
        try:
            if PASS_MARK in f.read_text(errors='replace'):
                out.append(f)
        except OSError:
            continue
    return out


def vledger_has_certified_row(n):
    rx = re.compile(rf'^\|\s*{n}\s*\|')
    try:
        for line in open(VLEDGER, errors='replace'):
            if rx.match(line) and 'certified=yes' in line.replace(' ', ''):
                return True
            if rx.match(line) and re.search(r'\|\s*yes\s*\|', line):
                return True
    except OSError:
        pass
    return False


def append_vledger_row(n, attempt, verify, r_mtime):
    rel = lambda p: os.path.relpath(p, ROOT)
    row = (f'| {n} | `{rel(attempt)}` | `{rel(verify)}` | PASS / PASS (dual-read, both newer than newest render) '
           f'| `analysis/reanalysis/slide_{n:03d}_raw.json` | certified=yes | certify-merge sweeper-h3 {utcnow()} |\n')
    with open(VLOCK, 'w') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            if vledger_has_certified_row(n):
                return False
            with open(VLEDGER, 'a') as f:
                f.write(row)
            return True
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def merge_slide(n, attempt, verify, r_mtime):
    appended = append_vledger_row(n, attempt, verify, r_mtime)
    src = ROOT / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
    r = subprocess.run(
        [sys.executable, 'pool_run/merge_final_deck.py', 'update', str(n),
         f'recreated_pptx/slide_{n:03d}_recreated.pptx', DECK],
        cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        log(f'MERGE-FAIL slide={n} merge_final_deck rc={r.returncode} err={r.stderr.strip()[:300]}')
        return False
    con = sqlite3.connect(DB, timeout=30)
    try:
        con.execute("UPDATE scopes SET status='done' WHERE name=?", (f'slide-{n}',))
        con.commit()
    finally:
        con.close()
    log(f'MERGED slide={n} attempt={os.path.relpath(attempt, ROOT)} verify={os.path.relpath(verify, ROOT)} '
        f'verdict=PASS vledger_row={"appended" if appended else "already-present"} '
        f'src=recreated_pptx/slide_{n:03d}_recreated.pptx deck={DECK} scope=slide-{n}->done')
    return True


def scan_once():
    certified = certified_set()
    merged, candidates = [], []
    for n in range(1, N_SLIDES + 1):
        if n in certified:
            continue
        qdir = find_qa_dir(n)
        if qdir is None:
            continue
        r = newest_render_mtime(qdir)
        if r is None:
            continue
        attempts = pass_files(qdir, 'judge_attempt*.txt', r)
        verifies = pass_files(qdir, 'judge_verify*.txt', r)
        if attempts and verifies:
            candidates.append(n)
            merge_slide(n, attempts[-1], verifies[-1], r)
        elif attempts or verifies:
            candidates.append(f'{n}(single)')
    now = certified_set()
    pending = [n for n in range(1, N_SLIDES + 1) if n not in now]
    log(f'scan summary: scanned={N_SLIDES} certified={len(now)}/{N_SLIDES} '
        f'dual-PASS candidates={candidates} merged_this_pass={merged} pending={pending}')
    return len(now)


def main():
    budget_s = float(sys.argv[1]) if len(sys.argv) > 1 else 2 * 3600
    deadline = time.time() + budget_s
    log(f'sweeper-h3 start budget={budget_s:.0f}s deadline_utc={datetime.fromtimestamp(deadline, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    while time.time() < deadline:
        try:
            done = scan_once()
        except Exception as e:
            log(f'scan error: {e!r}')
            done = len(certified_set())
        if done >= N_SLIDES:
            log(f'ALL {N_SLIDES}/{N_SLIDES} certified — sweeper-h3 exiting')
            return
        remaining = deadline - time.time()
        time.sleep(min(SCAN_INTERVAL, max(0, remaining)))
    log(f'sweeper-h3 budget exhausted, certified={len(certified_set())}/{N_SLIDES}')


if __name__ == '__main__':
    main()
