#!/usr/bin/env python3
"""Certify-and-merge sweeper loop for 08_performance_measure (2h budget).

Each scan, for every slide 1..37 NOT certified in final_deck_ledger.json:
  - qa dir(s) under recreated_pptx/qa matching slide_?0*N
  - R = newest render png mtime in the dir (*.png with 'render' in the name)
  - candidate = judge_attempt*.txt AND judge_verify*.txt containing
    'FINAL VERDICT: PASS' with mtime > R (stale-PASS guard)
  - conflict guard: a newer FAIL transcript re-opens the slide (namespace
    AGENTS.md dual-read law) -> skip
On candidate: flock-append row to pool_run/verification_ledger.md, run
merge_final_deck.py update N ... 08-performance_final.pptx from namespace
root, sqlite3 UPDATE scopes SET status='done' WHERE name='slide-N'.
Sleeps 45-60s between scans. Logs to pool_run/sweeper_cm_final_loop.log.
"""
import fcntl
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
QA = os.path.join(ROOT, 'recreated_pptx', 'qa')
LEDGER_JSON = os.path.join(ROOT, 'final_deck_ledger.json')
VLEDGER = os.path.join(ROOT, 'pool_run', 'verification_ledger.md')
VLOCK = VLEDGER + '.lock'
DB = os.path.join(ROOT, 'pool_run', 'mission.db')
LOG = os.path.join(ROOT, 'pool_run', 'sweeper_cm_final_loop.log')
DECK = '08-performance_final.pptx'
N_SLIDES = 37
BUDGET = 7200


def ts():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(msg):
    line = f'{ts()} {msg}'
    with open(LOG, 'a') as f:
        f.write(line + '\n')
    print(line, flush=True)


def verdict_pass(path):
    """True if any line has 'FINAL VERDICT: PASS' (and not FAIL on same line)."""
    try:
        with open(path, errors='replace') as f:
            for line in f:
                if 'FINAL VERDICT' in line and 'PASS' in line and 'FAIL' not in line:
                    return True
    except OSError:
        pass
    return False


def verdict_fail(path):
    try:
        with open(path, errors='replace') as f:
            for line in f:
                if 'FINAL VERDICT' in line and 'FAIL' in line:
                    return True
    except OSError:
        pass
    return False


def certified_pages():
    with open(LEDGER_JSON) as f:
        return {p['slide_num'] for p in json.load(f)['pages'] if p['status'] == 'certified'}


def vledger_has_certified_yes(n):
    pat = re.compile(r'^\|\s*0*%d\s*\|' % n)
    try:
        with open(VLEDGER, errors='replace') as f:
            for line in f:
                if pat.match(line) and 'certified=yes' in line:
                    return True
    except OSError:
        pass
    return False


def append_ledger_row(n, qadir, att, ver):
    reanalysis = f'analysis/reanalysis/slide_{n:03d}_raw.json'
    if not os.path.exists(os.path.join(ROOT, reanalysis)):
        reanalysis = '—'
    row = (f'| {n} | recreated_pptx/qa/{qadir}/{att} | recreated_pptx/qa/{qadir}/{ver} | '
           f'PASS / PASS (dual-read, both PASS transcripts newer than newest render in dir) | '
           f'{reanalysis} | certified=yes | certify-merge sweeper {ts()} |')
    lf = open(VLOCK, 'w')
    try:
        fcntl.flock(lf, fcntl.LOCK_EX)
        if vledger_has_certified_yes(n):
            return False
        with open(VLEDGER, 'a') as f:
            f.write(row + '\n')
        return True
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()


def merge_update(n):
    src = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    if not os.path.exists(os.path.join(ROOT, src)):
        return False, 'source pptx missing: ' + src
    r = subprocess.run([sys.executable, os.path.join('pool_run', 'merge_final_deck.py'),
                        'update', str(n), src, DECK],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    ok = r.returncode == 0 and n in certified_pages()
    return ok, (r.stdout + r.stderr).strip()[:300]


def db_set_done(n):
    for _ in range(5):
        try:
            con = sqlite3.connect(DB, timeout=15)
            con.execute("UPDATE scopes SET status='done' WHERE name=?", (f'slide-{n}',))
            con.commit()
            con.close()
            return True
        except sqlite3.OperationalError:
            time.sleep(5)
    return False


def scan_once():
    cert = certified_pages()
    candidates = []
    skipped = []
    for n in range(1, N_SLIDES + 1):
        if n in cert:
            continue
        dirs = [d for d in os.listdir(QA) if re.fullmatch(r'slide_?0*%d$' % n, d)] if os.path.isdir(QA) else []
        for d in sorted(dirs):
            dd = os.path.join(QA, d)
            renders = [f for f in os.listdir(dd)
                       if f.lower().endswith('.png') and 'render' in f.lower()]
            R = max((os.path.getmtime(os.path.join(dd, f)) for f in renders), default=0.0)
            att_all = sorted(f for f in os.listdir(dd) if re.fullmatch(r'judge_attempt.*\.txt', f))
            ver_all = sorted(f for f in os.listdir(dd) if re.fullmatch(r'judge_verify.*\.txt', f))
            att_pass = [f for f in att_all
                        if verdict_pass(os.path.join(dd, f))
                        and os.path.getmtime(os.path.join(dd, f)) > R]
            ver_pass = [f for f in ver_all
                        if verdict_pass(os.path.join(dd, f))
                        and os.path.getmtime(os.path.join(dd, f)) > R]
            if not (att_pass and ver_pass):
                continue
            att = max(att_pass, key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            ver = max(ver_pass, key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            att_m = os.path.getmtime(os.path.join(dd, att))
            ver_m = os.path.getmtime(os.path.join(dd, ver))
            newer_fail = any(
                verdict_fail(os.path.join(dd, f)) and os.path.getmtime(os.path.join(dd, f)) > m
                for f, m in [(f, att_m) for f in att_all] + [(f, ver_m) for f in ver_all])
            if newer_fail:
                skipped.append(n)
                log(f'conflict-skip slide {n} dir={d}: dual PASS newer than render but a newer FAIL transcript exists (re-opened) att={att} ver={ver}')
                continue
            candidates.append((n, d, att, ver))
    merged = []
    for n, d, att, ver in candidates:
        row_ok = append_ledger_row(n, d, att, ver)
        ok, out = merge_update(n)
        db_ok = db_set_done(n)
        if ok:
            merged.append(n)
            log(f'MERGE slide {n}: row_appended={row_ok} attempt=recreated_pptx/qa/{d}/{att} '
                f'verify=recreated_pptx/qa/{d}/{ver} deck={DECK} scope=slide-{n}->done out={out!r}')
        else:
            log(f'MERGE-FAILED slide {n}: merge_ok={ok} db_ok={db_ok} row_appended={row_ok} out={out!r}')
    cert_now = certified_pages()
    log(f'scan summary: uncertified_at_start={N_SLIDES - len(cert)} candidates={[c[0] for c in candidates]} '
        f'merged={merged} conflict_skipped={sorted(set(skipped))} certified_now={len(cert_now)}/{N_SLIDES}')
    return len(cert_now), merged


def main():
    end = time.time() + BUDGET
    log(f'sweeper start: budget={BUDGET}s deadline={datetime.fromtimestamp(end, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    while time.time() < end:
        t0 = time.time()
        try:
            count, merged = scan_once()
        except Exception as e:
            log(f'scan error: {e!r}')
            count, merged = -1, []
        if count == N_SLIDES:
            log(f'sweeper stop: all {N_SLIDES} certified')
            return 0
        elapsed = time.time() - t0
        time.sleep(max(0, random.uniform(45, 60) - elapsed))
    log(f'sweeper stop: budget ended certified={len(certified_pages())}/{N_SLIDES}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
