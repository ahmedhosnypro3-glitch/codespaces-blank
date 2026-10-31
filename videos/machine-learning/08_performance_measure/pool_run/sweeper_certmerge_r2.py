#!/usr/bin/env python3
"""Certify-and-merge sweeper: scan qa/slideNNN for fresh dual-PASS transcripts
(newer than newest render png), flock-append verification_ledger.md row,
merge slide into 08-performance_final.pptx, mark scope done in mission.db.
Usage: sweeper_certmerge_r2.py <deadline_epoch>  (loops scan/merge/sleep 45-60s)
"""
import fcntl
import json
import random
import subprocess
import sys
import time
from pathlib import Path

NS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure')
QA = NS / 'recreated_pptx' / 'qa'
LEDGER_JSON = NS / 'final_deck_ledger.json'
VLEDGER = NS / 'pool_run' / 'verification_ledger.md'
VLOCK = NS / 'pool_run' / 'verification_ledger.md.lock'
DB = NS / 'pool_run' / 'mission.db'
LOG = NS / 'pool_run' / 'sweeper_certmerge_r2.log'
PASS = 'FINAL VERDICT: PASS'


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    print(line, flush=True)
    with open(LOG, 'a') as f:
        f.write(line + "\n")


def certified_set():
    with open(LEDGER_JSON) as f:
        data = json.load(f)
    return {p['slide_num'] for p in data['pages'] if p['status'] == 'certified'}


def scan():
    cert = certified_set()
    hits = []
    for n in range(1, 38):
        if n in cert:
            continue
        d = QA / f"slide{n:03d}"
        if not d.is_dir():
            continue
        renders = list(d.glob('render*.png'))
        if not renders:
            continue
        newest_render = max(renders, key=lambda p: p.stat().st_mtime)
        nrt = newest_render.stat().st_mtime
        att = [p for p in d.glob('judge_attempt_*.txt')
               if PASS in p.read_text(errors='ignore') and p.stat().st_mtime > nrt]
        ver = [p for p in d.glob('judge_verify_*.txt')
               if PASS in p.read_text(errors='ignore') and p.stat().st_mtime > nrt]
        if att and ver:
            att.sort(key=lambda p: p.stat().st_mtime)
            ver.sort(key=lambda p: p.stat().st_mtime)
            hits.append((n, att[-1], ver[-1], newest_render.name))
    return hits


def merge(n, att, ver):
    pptx = NS / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
    if not pptx.exists():
        log(f"slide {n}: slide_{n:03d}_recreated.pptx missing — skip merge")
        return False
    row = (f"| {n} | recreated_pptx/qa/slide{n:03d}/{att.name} | "
           f"recreated_pptx/qa/slide{n:03d}/{ver.name} | "
           f"PASS / PASS (original-first dual-read; both PASS transcripts newer than newest render) | — | "
           f"certified=yes | certify-merge sweeper "
           f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} |\n")
    with open(VLOCK, 'a') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            with open(VLEDGER, 'a') as vf:
                vf.write(row)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)
    r = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update', str(n),
                        f'recreated_pptx/slide_{n:03d}_recreated.pptx',
                        '08-performance_final.pptx'],
                       cwd=NS, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"slide {n}: MERGE FAILED rc={r.returncode} stderr={r.stderr[-400:]}")
        return False
    subprocess.run(['sqlite3', str(DB),
                    f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                   check=True)
    log(f"MERGED slide {n}: attempt={att.name} verify={ver.name} | {r.stdout.strip()}")
    return True


def main():
    deadline = float(sys.argv[1])
    log(f"sweep chunk start, deadline {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(deadline))}")
    while True:
        hits = scan()
        if hits:
            for (n, att, ver, rn) in hits:
                log(f"candidate slide {n}: attempt={att.name} verify={ver.name} newest_render={rn}")
                merge(n, att, ver)
        else:
            log("scan: no new dual-PASS candidates beyond certified set")
        remaining = deadline - time.time()
        if remaining <= 0:
            break
        time.sleep(min(random.uniform(45, 60), remaining))
    log("sweep chunk done")


if __name__ == '__main__':
    main()
