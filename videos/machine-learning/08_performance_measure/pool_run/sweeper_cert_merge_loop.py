#!/usr/bin/env python3
"""Certify-and-merge sweeper loop for 08_performance_measure.

Each pass: scan slides 1..37 not yet certified in final_deck_ledger.json.
A slide qualifies when its qa dir has a judge_attempt_*.txt and a
judge_verify_*.txt, both with 'FINAL VERDICT: PASS' and both mtime > the
newest render png mtime (i.e. they judged the CURRENT build), and the newest
verify overall is not a FAIL. Qualifying slides get: flock-appended ledger row
in pool_run/verification_ledger.md, merge_final_deck.py update, mission.db
scope done, and a confirmation check. Stops when all 37 certified (runs the
final gate) or after ~40 minutes."""
import json, os, re, subprocess, sys, time, fcntl
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / 'recreated_pptx' / 'qa'
POOL = ROOT / 'pool_run'
LEDGER_JSON = ROOT / 'final_deck_ledger.json'
VER_LEDGER = POOL / 'verification_ledger.md'
LOG = POOL / 'sweeper_cert_merge_loop.log'
DECK = ROOT / '08-performance_final.pptx'
START = time.time()
MAX_SECONDS = 40 * 60

logf = open(LOG, 'a', buffering=1)

def log(msg):
    logf.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

def certified_set():
    d = json.load(open(LEDGER_JSON))
    return {int(p['slide_num']) for p in d['pages'] if p['status'] == 'certified'}

def find_qa_dir(n):
    for pat in (f'slide{n:03d}', f'slide{n}', f'slide_{n:03d}'):
        d = QA / pat
        if d.is_dir():
            return d
    return None

def newest_render(qdir):
    best = None
    for f in qdir.rglob('*.png'):
        if 'render' in f.name.lower():
            m = f.stat().st_mtime
            if best is None or m > best[0]:
                best = (m, f)
    return best

def verdict_passes(path):
    try:
        txt = path.read_text(errors='replace')
    except Exception:
        return False
    return re.search(r'FINAL VERDICT:\s*PASS', txt) is not None

def transcripts(qdir, prefix):
    out = []
    for f in sorted(qdir.rglob(f'{prefix}*.txt')):
        out.append((f.stat().st_mtime, f))
    return out

def scan_pass():
    cert = certified_set()
    log(f"certified now: {' '.join(map(str, sorted(cert))) or '(none)'} ({len(cert)}/37)")
    for n in range(1, 38):
        if n in cert:
            continue
        qdir = find_qa_dir(n)
        if qdir is None:
            continue
        pptx = ROOT / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
        nr = newest_render(qdir)
        if nr is None:
            # no render: skip if pptx exists, per brief
            continue
        r_mtime, r_png = nr
        attempts = [(m, f) for m, f in transcripts(qdir, 'judge_attempt') if m > r_mtime and verdict_passes(f)]
        verifies_all = transcripts(qdir, 'judge_verify')
        verifies = [(m, f) for m, f in verifies_all if m > r_mtime and verdict_passes(f)]
        if verifies_all:
            newest_v = max(verifies_all)
            if not verdict_passes(newest_v[1]):
                continue  # newest verify is FAIL -> skip
        if attempts and verifies:
            merge_slide(n, qdir, r_png, attempts[-1][1], verifies[-1][1])

def source_json(n):
    for cand in (ROOT / 'analysis' / 'reanalysis' / f'slide_{n:03d}_raw.json',
                 ROOT / 'analysis' / f'slide_{n:03d}_raw.json',
                 ROOT / 'analysis' / f'slide_{n:03d}_final.json'):
        if cand.exists():
            return str(cand.relative_to(ROOT))
    return 'analysis/reanalysis/slide_%03d_raw.json (missing)' % n

def merge_slide(n, qdir, r_png, attempt, verify):
    src = source_json(n)
    row = (f"| {n} | {attempt.relative_to(ROOT)} | {verify.relative_to(ROOT)} "
           f"| PASS/PASS (dual-read, original-first, vs {r_png.name}) "
           f"| {src} | certified=yes | appended by certify-merge sweeper {time.strftime('%Y-%m-%d %H:%M:%S')} |\n")
    # flock-append ledger row
    with open(VER_LEDGER, 'a') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        lf.write(row)
        fcntl.flock(lf, fcntl.LOCK_UN)
    log(f"slide {n}: ledger row appended; attempt={attempt.name} verify={verify.name}")
    pptx = ROOT / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
    r = subprocess.run([sys.executable, str(POOL / 'merge_final_deck.py'), 'update',
                        str(n), str(pptx), str(DECK)],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        log(f"slide {n}: MERGE FAILED rc={r.returncode} {r.stdout} {r.stderr}")
        return
    log(f"slide {n}: merge ok: {r.stdout.strip()}")
    subprocess.run(['sqlite3', str(POOL / 'mission.db'),
                    f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                   check=False)
    cert = certified_set()
    if n in cert:
        log(f"slide {n}: CONFIRMED in final_deck_ledger.json certified list")
    else:
        log(f"slide {n}: WARNING not in certified list after merge")

def final_gate():
    log("ALL 37 CERTIFIED -> running final gate")
    r = subprocess.run([sys.executable, str(POOL / 'merge_final_deck.py'), 'gate',
                        str(DECK), str(ROOT / 'recreated_pptx'), '37'],
                       capture_output=True, text=True, cwd=ROOT)
    out = r.stdout + r.stderr
    log(f"gate rc={r.returncode}: {out.strip()}")
    report = ROOT / f'final_deck_gate_{time.strftime("%Y%m%d_%H%M%S")}.txt'
    report.write_text(f"gate run {time.strftime('%Y-%m-%d %H:%M:%S')} rc={r.returncode}\n{out}\n")
    log(f"gate report banked at {report}")

pass_no = 0
while True:
    pass_no += 1
    log(f"--- pass {pass_no} ---")
    try:
        scan_pass()
    except Exception as e:
        log(f"pass error: {e!r}")
    cert = certified_set()
    if len(cert) >= 37:
        final_gate()
        log("DONE: all 37 certified and gate banked; stopping")
        break
    if time.time() - START > MAX_SECONDS:
        log(f"TIME BUDGET EXCEEDED (~40min); stopping with {len(cert)}/37 certified")
        break
    time.sleep(45)
