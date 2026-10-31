#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure.

Loop every ~90s (2h budget): scan slides 1..37. For each slide NOT certified in
final_deck_ledger.json, find qa dirs matching regex slide_?0*N under
recreated_pptx/qa/, newest render*.png mtime R, then require BOTH a
judge_attempt*.txt and a judge_verify*.txt containing 'FINAL VERDICT: PASS'
with mtime > R. Only then merge:
  1. flock-append one row to pool_run/verification_ledger.md
  2. python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx (from namespace root)
  3. sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"
Every merge and every scan summary is logged to pool_run/hygiene2.log with a
UTC timestamp. Never merges on a single PASS or a PASS older than the newest
render. Never deletes evidence.

Usage: sweep_certmerge.py [--dry-run] [--once] [--budget-seconds N] [--interval N]
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
DB_REL = 'pool_run/mission.db'
DECK_REL = '08-performance_final.pptx'
LOG = os.path.join(ROOT, 'pool_run', 'hygiene2.log')
N_SLIDES = 37


def ts():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(msg):
    line = f'{ts()} {msg}'
    with open(LOG, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
    print(line, flush=True)


def verdict_pass(path):
    try:
        with open(path, errors='replace') as f:
            for line in f:
                if 'FINAL VERDICT' in line:
                    return 'PASS' in line and 'FAIL' not in line
    except OSError:
        pass
    return False


def certified_pages():
    with open(LEDGER_JSON) as f:
        return {p['slide_num'] for p in json.load(f)['pages']
                if p.get('status') == 'certified'}


def qa_dirs_for(n):
    pat = re.compile(rf'slide_?0*{n}$')
    out = []
    if not os.path.isdir(QA):
        return out
    for d in sorted(os.listdir(QA)):
        if pat.fullmatch(d):
            out.append(os.path.join(QA, d))
    return out


def scan_candidate(n):
    """Return (att_path, ver_path, R) if slide n has dual PASS newer than the
    newest render png, else None."""
    dirs = qa_dirs_for(n)
    renders = []
    att = []
    ver = []
    for dd in dirs:
        try:
            files = os.listdir(dd)
        except OSError:
            continue
        for fn in files:
            p = os.path.join(dd, fn)
            try:
                mt = os.path.getmtime(p)
            except OSError:
                continue
            if re.fullmatch(r'render.*\.png', fn):
                renders.append(mt)
            elif re.fullmatch(r'judge_attempt_.*\.txt', fn) and verdict_pass(p):
                att.append((mt, p))
            elif re.fullmatch(r'judge_verify_.*\.txt', fn) and verdict_pass(p):
                ver.append((mt, p))
    if not renders or not att or not ver:
        return None
    r = max(renders)
    att_new = [p for mt, p in att if mt > r]
    ver_new = [p for mt, p in ver if mt > r]
    if not att_new or not ver_new:
        return None
    return max(att_new), max(ver_new), r


def vledger_has_yes(n):
    try:
        with open(VLEDGER, errors='replace') as f:
            for line in f:
                if not line.startswith('|') or line.startswith('| slide') or line.startswith('|---'):
                    continue
                cells = [c.strip() for c in line.split('|')]
                try:
                    s = int(cells[1].lstrip('0') or '0')
                except (ValueError, IndexError):
                    continue
                if s == n and len(cells) > 6 and cells[6].lower() in ('yes', 'certified=yes'):
                    return True
    except OSError:
        pass
    return False


def append_ledger_row(n, att, ver):
    rel = lambda p: os.path.relpath(p, ROOT)
    reanalysis = os.path.join('analysis', 'reanalysis', f'slide_{n:03d}_raw.json')
    if not os.path.exists(os.path.join(ROOT, reanalysis)):
        reanalysis = '-'
    row = (f'| {n} | {rel(att)} | {rel(ver)} | PASS / PASS (dual-read; both transcripts '
           f'mtime newer than newest render) | {reanalysis} | certified=yes | '
           f'appended by certify-merge sweeper {ts()} |')
    with open(VLEDGER, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        if vledger_has_yes(n):
            fcntl.flock(f, fcntl.LOCK_UN)
            return False
        f.write(row + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
        return True


def merge_update(n):
    src_rel = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    r = subprocess.run([sys.executable, os.path.join('pool_run', 'merge_final_deck.py'),
                        'update', str(n), src_rel, DECK_REL],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def db_set_done(n):
    for _ in range(5):
        r = subprocess.run(['sqlite3', DB_REL,
                            f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            return True
        time.sleep(5)
    return False


def one_pass(dry_run):
    cert = certified_pages()
    merged = []
    for n in range(1, N_SLIDES + 1):
        if n in cert:
            continue
        cand = scan_candidate(n)
        if not cand:
            continue
        att, ver, r = cand
        log(f'merge-candidate slide-{n}: attempt={os.path.relpath(att, ROOT)} '
            f'verify={os.path.relpath(ver, ROOT)} render_R={datetime.fromtimestamp(r, timezone.utc).strftime("%FT%TZ")}')
        if dry_run:
            continue
        # re-check certified under fresh read (another sweeper may have merged)
        if n in certified_pages():
            continue
        if append_ledger_row(n, att, ver):
            log(f'merged slide-{n}: ledger row appended (attempt={os.path.relpath(att, ROOT)}, verify={os.path.relpath(ver, ROOT)}, verdict=PASS, certified=yes)')
        else:
            log(f'merged slide-{n}: ledger row already present (certified=yes), skipped append')
        ok, out = merge_update(n)
        log(f'merged slide-{n}: merge_final_deck update {"ok" if ok else "FAILED: " + out}')
        if db_set_done(n):
            log(f'merged slide-{n}: mission.db scope slide-{n} set done')
        else:
            log(f'merged slide-{n}: FAILED to set scope done in mission.db')
        merged.append(n)
    cert2 = certified_pages()
    log(f'scan summary: certified={len(cert2)}/{N_SLIDES} merged_this_pass={merged or "[]"}')
    return len(cert2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--once', action='store_true')
    ap.add_argument('--budget-seconds', type=int, default=2 * 3600)
    ap.add_argument('--interval', type=int, default=90)
    args = ap.parse_args()
    os.chdir(ROOT)
    deadline = time.time() + args.budget_seconds
    log(f'sweeper start: budget={args.budget_seconds}s interval={args.interval}s dry_run={args.dry_run}')
    while True:
        try:
            done = one_pass(args.dry_run)
        except Exception as e:
            log(f'scan error: {e!r}')
            done = len(certified_pages())
        if done >= N_SLIDES:
            log(f'sweeper done: all {N_SLIDES} slides certified')
            return 0
        if args.once or time.time() >= deadline:
            log(f'sweeper stop: once={args.once} budget_end={time.time() >= deadline} certified={done}/{N_SLIDES}')
            return 0
        time.sleep(min(args.interval, max(0, deadline - time.time())))


if __name__ == '__main__':
    sys.exit(main())
