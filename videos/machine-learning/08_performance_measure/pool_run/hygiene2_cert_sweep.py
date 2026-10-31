#!/usr/bin/env python3
"""One certify-and-merge sweep pass over slides 1-37.

For each slide NOT certified in final_deck_ledger.json:
  - pool all qa dirs matching ^slide_?0*N$ under recreated_pptx/qa/
  - R = newest render*.png mtime across those dirs
  - candidate iff exists judge_attempt*.txt containing 'FINAL VERDICT: PASS'
    with mtime > R AND exists judge_verify*.txt containing
    'FINAL VERDICT: PASS' with mtime > R (dual PASS newer than newest render)
  - merge: flock-append row to pool_run/verification_ledger.md, then
    merge_final_deck.py update, then mission.db scope -> done.
Logs scan summary + each merge to pool_run/hygiene2.log (UTC).
"""
import fcntl
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

NS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure')
QA = NS / 'recreated_pptx' / 'qa'
LEDGER_JSON = NS / 'final_deck_ledger.json'
VER_LEDGER = NS / 'pool_run' / 'verification_ledger.md'
VER_LOCK = NS / 'pool_run' / 'verification_ledger.md.lock'
LOG = NS / 'pool_run' / 'hygiene2.log'
OUT_DECK = '08-performance_final.pptx'
TOTAL = 37


def utcnow():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(msg):
    line = f"{utcnow()} {msg}"
    with open(LOG, 'a') as f:
        f.write(line + '\n')
    print(line, flush=True)


def certified_set():
    with open(LEDGER_JSON) as f:
        ledger = json.load(f)
    return {p['slide_num'] for p in ledger['pages'] if p.get('status') == 'certified'}


def qa_dirs(n):
    pat = re.compile(rf'^slide_?0*{n}$')
    return sorted(d for d in QA.iterdir() if d.is_dir() and pat.fullmatch(d.name))


def newest_render(dirs):
    best_m, best_p = None, None
    for d in dirs:
        for p in d.glob('render*.png'):
            m = p.stat().st_mtime
            if best_m is None or m > best_m:
                best_m, best_p = m, p
    return best_m, best_p


def pass_files(dirs, prefix, r_mtime):
    """Files glob prefix*.txt containing FINAL VERDICT: PASS with mtime > r_mtime,
    newest first."""
    out = []
    for d in dirs:
        for p in d.glob(prefix + '*.txt'):
            try:
                txt = p.read_text(errors='replace')
            except OSError:
                continue
            if 'FINAL VERDICT: PASS' not in txt:
                continue
            m = p.stat().st_mtime
            if r_mtime is not None and m > r_mtime:
                out.append((m, p))
    out.sort(reverse=True)
    return out


def rel(p):
    return str(p.relative_to(NS))


def merge_slide(n, dirs, attempt, verify, render_p):
    reanalysis = NS / 'analysis' / 'reanalysis' / f'slide_{n:03d}_raw.json'
    reanalysis_s = rel(reanalysis) if reanalysis.exists() else '—'
    row = (f"| {n} | {rel(attempt)} | {rel(verify)} | "
           f"PASS / PASS (dual PASS newer than newest render {rel(render_p)}) | "
           f"{reanalysis_s} | certified=yes | "
           f"certify-merge sweeper {utcnow()} |\n")
    with open(VER_LOCK, 'w') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        with open(VER_LEDGER, 'a') as f:
            f.write(row)
        fcntl.flock(lf, fcntl.LOCK_UN)
    pptx = NS / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
    r = subprocess.run(
        ['python3', 'pool_run/merge_final_deck.py', 'update', str(n),
         str(pptx.relative_to(NS)), OUT_DECK],
        cwd=NS, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"MERGE-FAIL slide-{n} merge_final_deck rc={r.returncode} err={r.stderr.strip()[:300]}")
        return False
    subprocess.run(
        ['sqlite3', 'pool_run/mission.db',
         f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
        cwd=NS, check=True)
    log(f"MERGE slide-{n} attempt={rel(attempt)} verify={rel(verify)} "
        f"render={rel(render_p)} verdict=PASS/PASS deck={OUT_DECK} db=done")
    return True


def sweep():
    certified = certified_set()
    merged, candidates, pending = [], [], []
    for n in range(1, TOTAL + 1):
        if n in certified:
            continue
        dirs = qa_dirs(n)
        if not dirs:
            pending.append(n)
            continue
        r_m, r_p = newest_render(dirs)
        attempts = pass_files(dirs, 'judge_attempt', r_m)
        verifies = pass_files(dirs, 'judge_verify', r_m)
        if attempts and verifies:
            candidates.append(n)
            # re-check certified right before merging (concurrent sweeper guard)
            if n in certified_set():
                continue
            if merge_slide(n, dirs, attempts[0][1], verifies[0][1], r_p):
                merged.append(n)
                certified.add(n)
        else:
            pending.append(n)
    certified_now = certified_set()
    log(f"scan summary: scanned=37 certified={len(certified_now)}/{TOTAL} "
        f"candidates={candidates} merged_this_pass={merged} "
        f"pending={sorted(set(range(1, TOTAL + 1)) - certified_now)}")
    return len(certified_now), merged


if __name__ == '__main__':
    count, merged = sweep()
    print(f"RESULT certified={count}/{TOTAL} merged={merged}")
    sys.exit(0 if count == TOTAL else 1)
