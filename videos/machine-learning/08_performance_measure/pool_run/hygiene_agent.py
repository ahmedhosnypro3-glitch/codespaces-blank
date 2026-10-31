#!/usr/bin/env python3
"""Ledger-hygiene agent pass for 08_performance_measure (parent-mandated loop).

Per pass, from the namespace root:
  1. certified = pages with status 'certified' in final_deck_ledger.json
     done      = scopes slide-N with status 'done' in pool_run/mission.db
  2. certified but scope not done -> UPDATE scopes SET status='done' (log fix)
  3. scope done but slide not certified -> look in recreated_pptx/qa/slideN*
     for a judge_attempt PASS and a judge_verify PASS both newer than the
     newest render png; if both exist, flock-append a row to
     pool_run/verification_ledger.md and run
       python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
     otherwise log the inconsistency only (never mark anything ourselves).
  4. append one summary line to pool_run/hygiene2.log:
       <UTC ts> certified=C done=D consistent=T/F fixes=K

Fix/inconsistency diagnostics go to pool_run/hygiene2_detail.log (append-only).
Loop mode: one pass every 30s until the deadline (~40 min).
"""
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
DB_REL = 'pool_run/mission.db'
LEDGER_JSON = 'final_deck_ledger.json'
VLEDGER = 'pool_run/verification_ledger.md'
HLOG = 'pool_run/hygiene2.log'
DLOG = 'pool_run/hygiene2_detail.log'
DECK = '08-performance_final.pptx'
QA = os.path.join('recreated_pptx', 'qa')


def dlog(msg):
    line = f"{datetime.now(timezone.utc).strftime('%FT%TZ')} hygiene-agent {msg}"
    with open(os.path.join(ROOT, DLOG), 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)


def q(sql):
    r = subprocess.run(['sqlite3', DB_REL, sql], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return [l for l in r.stdout.splitlines() if l]


def certified_set():
    with open(os.path.join(ROOT, LEDGER_JSON)) as f:
        pages = json.load(f)['pages']
    return {p['slide_num'] for p in pages if p['status'] == 'certified'}


def done_set():
    rows = q("SELECT name FROM scopes WHERE name LIKE 'slide-%' AND status='done';")
    return {int(r.split('-', 1)[1]) for r in rows}


def verdict_pass(path):
    try:
        with open(path, errors='replace') as f:
            for line in f:
                if 'FINAL VERDICT' in line:
                    return 'PASS' in line and 'FAIL' not in line
    except OSError:
        pass
    return False


def qa_dirs(n):
    pat = re.compile(r'slide0*%d([^0-9].*)?$' % n)
    out = []
    if not os.path.isdir(os.path.join(ROOT, QA)):
        return out
    for d in sorted(os.listdir(os.path.join(ROOT, QA))):
        if pat.match(d) and os.path.isdir(os.path.join(ROOT, QA, d)):
            out.append(d)
    return out


def dual_pass_newer_than_render(n):
    """(attempt, verify) PASS transcripts both newer than the newest render png."""
    for d in qa_dirs(n):
        dd = os.path.join(ROOT, QA, d)
        renders = [f for f in os.listdir(dd)
                   if re.match(r'render.*\.png$', f)]
        if not renders:
            continue
        newest_render = max(os.path.getmtime(os.path.join(dd, f)) for f in renders)
        att = [f for f in os.listdir(dd)
               if re.match(r'judge_attempt.*\.txt$', f)
               and os.path.getmtime(os.path.join(dd, f)) > newest_render
               and verdict_pass(os.path.join(dd, f))]
        ver = [f for f in os.listdir(dd)
               if re.match(r'judge_verify.*\.txt$', f)
               and os.path.getmtime(os.path.join(dd, f)) > newest_render
               and verdict_pass(os.path.join(dd, f))]
        if att and ver:
            return d, sorted(att)[-1], sorted(ver)[-1]
    return None


def vledger_has_row(n):
    pat = re.compile(r'^\|\s*0*%d\s*\|' % n)
    try:
        with open(os.path.join(ROOT, VLEDGER), errors='replace') as f:
            for line in f:
                if pat.match(line):
                    return True
    except OSError:
        pass
    return False


def append_vledger_row(n, d, att, ver):
    reanalysis = f'analysis/reanalysis/slide_{n:03d}_raw.json'
    if not os.path.exists(os.path.join(ROOT, reanalysis)):
        reanalysis = '-'
    row = (f"| {n} | recreated_pptx/qa/{d}/{att} | "
           f"recreated_pptx/qa/{d}/{ver} | PASS / PASS (original-first dual-read, "
           f"both newer than newest render png) | {reanalysis} | yes | "
           f"appended by hygiene-agent (scope done, dual PASS found, slide not certified) |")
    path = os.path.join(ROOT, VLEDGER)
    with open(path, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        if not vledger_has_row(n):
            f.write(row + '\n')
            fcntl.flock(f, fcntl.LOCK_UN)
            return True
        fcntl.flock(f, fcntl.LOCK_UN)
    return False


def merge_update(n):
    src = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    r = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update',
                        str(n), src, DECK], cwd=ROOT,
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def one_pass():
    fixes = 0
    certified = certified_set()
    done = done_set()

    # Fix 2: certified in ledger json but scope not done
    for n in sorted(certified - done):
        q(f"UPDATE scopes SET status='done' WHERE name='slide-{n}';")
        fixes += 1
        dlog(f"FIX scope-done slide-{n} (was certified in final_deck_ledger.json but scope not done)")

    # Fix 3: scope done but slide not certified
    certified = certified_set()
    done = done_set()
    for n in sorted(done - certified):
        found = dual_pass_newer_than_render(n)
        if found:
            d, att, ver = found
            if append_vledger_row(n, d, att, ver):
                fixes += 1
                dlog(f"FIX verification_ledger row appended slide-{n} ({d}/{att} + {d}/{ver})")
            ok, out = merge_update(n)
            fixes += 1
            dlog(f"FIX merge-update slide-{n} {'ok' if ok else 'FAILED: ' + out}")
        else:
            dlog(f"INCONSISTENCY slide-{n}: scope done but not certified and no dual-PASS "
                 f"judge transcripts newer than newest render png (left unmarked)")

    certified = certified_set()
    done = done_set()
    consistent = certified == done
    ts = datetime.now(timezone.utc).strftime('%FT%TZ')
    line = (f"{ts} certified={len(certified)} done={len(done)} "
            f"consistent={'T' if consistent else 'F'} fixes={fixes}")
    with open(os.path.join(ROOT, HLOG), 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
    if not consistent:
        dlog(f"inconsistent after pass: certified={sorted(certified)} done={sorted(done)}")
    return line


def main():
    os.chdir(ROOT)
    if len(sys.argv) > 1 and sys.argv[1] == 'loop':
        deadline = time.time() + 40 * 60
        while time.time() < deadline:
            print(one_pass(), flush=True)
            time.sleep(30)
    else:
        print(one_pass(), flush=True)


if __name__ == '__main__':
    main()
