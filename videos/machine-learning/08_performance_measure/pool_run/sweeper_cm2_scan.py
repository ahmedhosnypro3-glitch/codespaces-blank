#!/usr/bin/env python3
"""One certify-and-merge scan over slides 1..37 for 08_performance_measure.

For each slide N not yet 'certified' in final_deck_ledger.json:
  - qa dirs under recreated_pptx/qa/ fullmatching slide_?0*N
  - R = newest mtime of render*.png across those dirs
  - PASS attempt = judge_attempt*.txt containing 'FINAL VERDICT: PASS' with mtime > R
  - PASS verify  = judge_verify*.txt  containing 'FINAL VERDICT: PASS' with mtime > R
  - both exist -> merge (ledger row, deck update, DB scope done)
Logs merges and a scan summary to pool_run/hygiene2.log (UTC).
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

NS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure')
QA = NS / 'recreated_pptx' / 'qa'
PPTX_DIR = NS / 'recreated_pptx'
LEDGER_JSON = NS / 'final_deck_ledger.json'
FINAL_DECK = NS / '08-performance_final.pptx'
VLEDGER = NS / 'pool_run' / 'verification_ledger.md'
VLOCK = NS / 'pool_run' / 'verification_ledger.md.lock'
HLOG = NS / 'pool_run' / 'hygiene2.log'
DB = NS / 'pool_run' / 'mission.db'
REANALYSIS = Path('analysis/reanalysis')

def utcnow():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

def log(msg):
    line = f'{utcnow()} {msg}'
    with open(HLOG, 'a') as f:
        f.write(line + '\n')
    print(line, flush=True)

def certified_set():
    with open(LEDGER_JSON) as f:
        d = json.load(f)
    return {p['slide_num'] for p in d['pages'] if p['status'] == 'certified'}

def qa_dirs(n):
    pat = re.compile(r'slide_?0*%d$' % n)
    return sorted(d for d in QA.iterdir() if d.is_dir() and pat.fullmatch(d.name))

def newest_render_mtime(dirs):
    best = 0.0
    for d in dirs:
        for p in d.glob('render*.png'):
            best = max(best, p.stat().st_mtime)
    return best

def pass_files(dirs, prefix, r):
    out = []
    for d in dirs:
        for p in sorted(d.glob(prefix + '*.txt')):
            try:
                if p.stat().st_mtime > r and 'FINAL VERDICT: PASS' in p.read_text(errors='replace'):
                    out.append(p)
            except OSError:
                pass
    return out

def append_ledger_row(row):
    with open(VLOCK, 'w') as lf:
        import fcntl
        fcntl.flock(lf, fcntl.LOCK_EX)
        with open(VLEDGER, 'a') as f:
            f.write(row + '\n')
        fcntl.flock(lf, fcntl.LOCK_UN)

def merge_slide(n, attempt, verify, r):
    pptx = PPTX_DIR / f'slide_{n:03d}_recreated.pptx'
    if not pptx.exists():
        log(f'slide-{n}: SKIP merge, missing {pptx.name}')
        return False
    rel_attempt = os.path.relpath(attempt, NS)
    rel_verify = os.path.relpath(verify, NS)
    src = REANALYSIS / f'slide_{n:03d}_raw.json'
    src_s = str(src) if src.exists() else '—'
    row = (f'| {n} | {rel_attempt} | {rel_verify} | PASS / PASS (dual-read, both PASS mtime > newest render mtime; '
           f'sweeper-cm2 {utcnow()}) | {src_s} | certified=yes | |')
    append_ledger_row(row)
    log(f'slide-{n}: ledger row appended (attempt={rel_attempt}, verify={rel_verify})')
    r1 = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update', str(n),
                         f'recreated_pptx/slide_{n:03d}_recreated.pptx', '08-performance_final.pptx'],
                        cwd=NS, capture_output=True, text=True)
    if r1.returncode != 0:
        log(f'slide-{n}: MERGE FAILED rc={r1.returncode} err={r1.stderr[-300:]}')
        return False
    log(f'slide-{n}: {r1.stdout.strip()}')
    r2 = subprocess.run(['sqlite3', 'pool_run/mission.db',
                         f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                        cwd=NS, capture_output=True, text=True)
    if r2.returncode != 0:
        log(f'slide-{n}: DB UPDATE FAILED err={r2.stderr[-300:]}')
        return False
    log(f'slide-{n}: scope slide-{n} set done; MERGED')
    return True

def scan():
    certified = certified_set()
    merged = []
    scanned = 0
    for n in range(1, 38):
        if n in certified:
            continue
        scanned += 1
        dirs = qa_dirs(n)
        if not dirs:
            continue
        r = newest_render_mtime(dirs)
        if r == 0.0:
            continue
        attempts = pass_files(dirs, 'judge_attempt', r)
        verifies = pass_files(dirs, 'judge_verify', r)
        if attempts and verifies:
            newest_a = max(attempts, key=lambda p: p.stat().st_mtime)
            newest_v = max(verifies, key=lambda p: p.stat().st_mtime)
            if merge_slide(n, newest_a, newest_v, r):
                merged.append(n)
    now_cert = certified_set()
    log(f'scan summary: scanned={scanned} merged={merged or "none"} certified={len(now_cert)}/37 done-check pending')
    return len(now_cert), merged

if __name__ == '__main__':
    total, merged = scan()
    print(f'RESULT certified={total}/37 merged={merged}', flush=True)
