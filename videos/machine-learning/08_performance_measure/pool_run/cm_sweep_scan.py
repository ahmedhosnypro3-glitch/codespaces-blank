#!/usr/bin/env python3
"""Certify-and-merge scan for 08_performance_measure (one pass).

For each slide N in 1..37 NOT certified in final_deck_ledger.json:
  - find qa dir(s) matching regex slide_?0*N under recreated_pptx/qa/
  - R = mtime of newest render*.png in the dir
  - look for judge_attempt*.txt and judge_verify*.txt containing
    'FINAL VERDICT: PASS' with mtime > R
  - if BOTH exist (dual PASS newer than newest render) and the slide pptx
    exists, merge:
      1. flock-append one row to pool_run/verification_ledger.md
      2. python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
      3. sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"
Never merges on a single PASS or a PASS older than the newest render.
Logs merges + one scan summary line to pool_run/hygiene2.log (UTC).
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
HLOG = os.path.join(ROOT, 'pool_run', 'hygiene2.log')
DB_REL = os.path.join('pool_run', 'mission.db')
DECK_REL = '08-performance_final.pptx'
N_SLIDES = 37


def utcnow():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def hlog(msg):
    line = f'{utcnow()} {msg}'
    with open(HLOG, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
    print(line, flush=True)


def certified_pages():
    with open(LEDGER_JSON) as f:
        return {p['slide_num'] for p in json.load(f)['pages'] if p['status'] == 'certified'}


def is_pass(path):
    try:
        with open(path, errors='replace') as f:
            return 'FINAL VERDICT: PASS' in f.read()
    except OSError:
        return False


def find_candidates(cert):
    """slide -> (qa_dir, attempt, verify) for uncertified slides with dual PASS newer than newest render."""
    out = {}
    if not os.path.isdir(QA):
        return out
    for n in range(1, N_SLIDES + 1):
        if n in cert:
            continue
        pat = re.compile(r'slide_?0*%d$' % n)
        for d in sorted(os.listdir(QA)):
            if not pat.fullmatch(d):
                continue
            dd = os.path.join(QA, d)
            if not os.path.isdir(dd):
                continue
            renders = [f for f in os.listdir(dd)
                       if f.startswith('render') and f.endswith('.png')]
            if not renders:
                continue
            r_mtime = max(os.path.getmtime(os.path.join(dd, f)) for f in renders)
            att = [f for f in os.listdir(dd)
                   if re.fullmatch(r'judge_attempt.*\.txt', f)
                   and os.path.getmtime(os.path.join(dd, f)) > r_mtime
                   and is_pass(os.path.join(dd, f))]
            ver = [f for f in os.listdir(dd)
                   if re.fullmatch(r'judge_verify.*\.txt', f)
                   and os.path.getmtime(os.path.join(dd, f)) > r_mtime
                   and is_pass(os.path.join(dd, f))]
            if att and ver:
                att.sort(key=lambda f: os.path.getmtime(os.path.join(dd, f)))
                ver.sort(key=lambda f: os.path.getmtime(os.path.join(dd, f)))
                out[n] = (d, att[-1], ver[-1])
    return out


def append_vledger_row(n, qa_dir, att, ver):
    reanalysis = os.path.join('analysis', 'reanalysis', f'slide_{n:03d}_raw.json')
    cell = reanalysis if os.path.exists(os.path.join(ROOT, reanalysis)) else '-'
    row = (f'| {n} | recreated_pptx/qa/{qa_dir}/{att} | '
           f'recreated_pptx/qa/{qa_dir}/{ver} | '
           f'PASS / PASS (dual-read, both newer than newest render) | '
           f'{cell} | certified=yes | certify-merge sweeper {utcnow()} |')
    with open(VLEDGER, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)


def merge_slide(n):
    src_rel = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    r = subprocess.run(['python3', os.path.join('pool_run', 'merge_final_deck.py'),
                        'update', str(n), src_rel, DECK_REL],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def db_set_done(n):
    r = subprocess.run(['sqlite3', DB_REL,
                        f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def scan_once():
    os.chdir(ROOT)
    cert = certified_pages()
    cand = find_candidates(cert)
    merged = []
    for n in sorted(cand):
        qa_dir, att, ver = cand[n]
        src = os.path.join(ROOT, 'recreated_pptx', f'slide_{n:03d}_recreated.pptx')
        if not os.path.exists(src):
            hlog(f'merge SKIP slide-{n}: slide pptx missing (dual PASS in qa/{qa_dir}: {att} + {ver})')
            continue
        try:
            append_vledger_row(n, qa_dir, att, ver)
        except Exception as e:
            hlog(f'merge FAILED slide-{n}: ledger append error {e}')
            continue
        ok, out = merge_slide(n)
        if not ok:
            hlog(f'merge FAILED slide-{n}: merge_final_deck.py: {out}')
            continue
        ok2, out2 = db_set_done(n)
        if not ok2:
            hlog(f'merge slide-{n}: deck updated but DB update failed: {out2}')
        merged.append(n)
        hlog(f'MERGED slide-{n}: attempt=recreated_pptx/qa/{qa_dir}/{att} '
             f'verify=recreated_pptx/qa/{qa_dir}/{ver} verdict=PASS deck=08-performance_final.pptx scope=slide-{n}->done')
    cert_after = certified_pages()
    hlog(f'scan summary: scanned={N_SLIDES - len(cert)} uncertified '
         f'candidates={sorted(cand)} merged={merged if merged else "none"} '
         f'certified={len(cert_after)}/37')
    return len(cert_after)


if __name__ == '__main__':
    c = scan_once()
    print(f'certified={c}/{N_SLIDES}')
    sys.exit(0 if c >= N_SLIDES else 1)
