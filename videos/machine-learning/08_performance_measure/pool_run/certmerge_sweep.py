#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure.

Every ~90s, for each slide 1..37 NOT certified in final_deck_ledger.json:
  - qa dir matching slide_?0*N under recreated_pptx/qa/
  - R = newest render png mtime in that dir
  - need judge_attempt*.txt AND judge_verify*.txt containing
    'FINAL VERDICT: PASS' with mtime > R (dual PASS newer than newest render)
  - skip if a newer FAIL transcript of the same kind exists (re-opened slide)
On dual PASS: flock-append row to pool_run/verification_ledger.md, run
merge_final_deck.py update N ..., set mission.db scope slide-N done.
Logs merges + scan summaries to pool_run/hygiene2.log (UTC timestamps).
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
QA = os.path.join(ROOT, 'recreated_pptx', 'qa')
LEDGER_JSON = os.path.join(ROOT, 'final_deck_ledger.json')
VLEDGER = os.path.join(ROOT, 'pool_run', 'verification_ledger.md')
DB = os.path.join(ROOT, 'pool_run', 'mission.db')
LOG = os.path.join(ROOT, 'pool_run', 'hygiene2.log')
DECK = '08-performance_final.pptx'
N_SLIDES = 37
INTERVAL = 90
BUDGET = 7200


def ts():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(msg):
    with open(LOG, 'a') as f:
        f.write(f'{ts()} {msg}\n')


def has_verdict(path, word):
    try:
        with open(path, errors='replace') as f:
            for line in f:
                if 'FINAL VERDICT' not in line:
                    continue
                if word == 'PASS':
                    if 'FINAL VERDICT: PASS' in line and 'FAIL' not in line:
                        return True
                else:
                    if 'FAIL' in line:
                        return True
    except OSError:
        pass
    return False


def certified_pages():
    with open(LEDGER_JSON) as f:
        return {p['slide_num'] for p in json.load(f)['pages'] if p['status'] == 'certified'}


def vledger_certified_yes(n):
    if not os.path.exists(VLEDGER):
        return False
    pat = re.compile(r'^\|\s*0*%d\s*\|' % n)
    with open(VLEDGER, errors='replace') as f:
        for line in f:
            if pat.match(line) and 'certified=yes' in line:
                return True
    return False


def append_ledger_row(n, qadir, att, ver):
    reanalysis = f'analysis/reanalysis/slide_{n:03d}_raw.json'
    if not os.path.exists(os.path.join(ROOT, reanalysis)):
        reanalysis = '-'
    row = (f'| {n} | recreated_pptx/qa/{qadir}/{att} | recreated_pptx/qa/{qadir}/{ver} | '
           f'PASS / PASS (original-first dual-read, both newer than newest render) | '
           f'{reanalysis} | certified=yes | certify-merge sweeper {ts()} |')
    with open(VLEDGER, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            if vledger_certified_yes(n):
                return False
            f.write(row + '\n')
            return True
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


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


def scan_pass():
    cert = certified_pages()
    merged = []
    skipped = []
    candidates = []
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
                        if has_verdict(os.path.join(dd, f), 'PASS')
                        and os.path.getmtime(os.path.join(dd, f)) > R]
            ver_pass = [f for f in ver_all
                        if has_verdict(os.path.join(dd, f), 'PASS')
                        and os.path.getmtime(os.path.join(dd, f)) > R]
            if not (att_pass and ver_pass):
                continue
            att = max(att_pass, key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            ver = max(ver_pass, key=lambda f: os.path.getmtime(os.path.join(dd, f)))
            att_m = os.path.getmtime(os.path.join(dd, att))
            ver_m = os.path.getmtime(os.path.join(dd, ver))
            newer_fail = any(
                has_verdict(os.path.join(dd, f), 'FAIL')
                and os.path.getmtime(os.path.join(dd, f)) > m
                for f, m in [(f, att_m) for f in att_all] + [(f, ver_m) for f in ver_all])
            if newer_fail:
                skipped.append(n)
                log(f'conflict-skip slide {n} dir={d}: dual PASS newer than render but a newer FAIL transcript exists (re-opened per namespace AGENTS.md) att={att} ver={ver}')
                continue
            candidates.append((n, d, att, ver))
    for n, d, att, ver in candidates:
        row_appended = append_ledger_row(n, d, att, ver)
        ok, out = merge_update(n)
        db_ok = db_set_done(n)
        if ok and db_ok:
            merged.append(n)
            log(f'MERGE slide {n}: row_appended={row_appended} attempt=recreated_pptx/qa/{d}/{att} '
                f'verify=recreated_pptx/qa/{d}/{ver} verdict=PASS reanalysis=analysis/reanalysis/slide_{n:03d}_raw.json '
                f'certified=yes deck={DECK} scope=slide-{n}->done out={out!r}')
        else:
            log(f'MERGE-FAILED slide {n}: merge_ok={ok} db_ok={db_ok} out={out!r}')
    cert_now = certified_pages()
    log(f'scan summary: scanned={N_SLIDES} uncertified={N_SLIDES - len(cert)} '
        f'candidates={sorted(n for n, *_ in candidates)} merged={sorted(merged)} '
        f'conflict_skipped={sorted(set(skipped))} certified={len(cert_now)}/{N_SLIDES}')
    return len(cert_now), sorted(merged)


def main():
    end = time.time() + BUDGET
    log(f'certmerge sweeper start: budget={BUDGET}s interval={INTERVAL}s deadline={datetime.fromtimestamp(end, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}')
    while time.time() < end:
        t0 = time.time()
        try:
            count, merged = scan_pass()
        except Exception as e:
            log(f'scan error: {e!r}')
            count, merged = -1, []
        if count == N_SLIDES:
            log(f'certmerge sweeper stop: all {N_SLIDES} certified')
            return 0
        elapsed = time.time() - t0
        time.sleep(max(0, INTERVAL - elapsed))
    log(f'certmerge sweeper stop: budget ended certified={len(certified_pages())}/{N_SLIDES}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
