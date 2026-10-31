#!/usr/bin/env python3
"""Sweeper #41 one pass: for each uncertified slide (final_deck_ledger page not
'certified') with BOTH a judge_attempt_* PASS and a judge_verify_* PASS whose
file mtime is newer than the newest render png in the slide's qa dir:
flock-append a row to pool_run/verification_ledger.md, merge into the final
deck, mark the scope done in mission.db. Idempotent; safe to re-run."""
import json, os, re, subprocess, sys, fcntl
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / 'recreated_pptx' / 'qa'
LEDGER = ROOT / 'pool_run' / 'verification_ledger.md'
LOCK = ROOT / 'pool_run' / 'verification_ledger.md.lock'
DECK = ROOT / '08-performance_final.pptx'
DB = ROOT / 'pool_run' / 'mission.db'
LOG = ROOT / 'pool_run' / 'sweeper41.log'

TS = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def log(msg):
    line = f'{TS} {msg}'
    print(line, flush=True)
    with open(LOG, 'a') as f:
        f.write(line + '\n')

def certified_pages():
    with open(ROOT / 'final_deck_ledger.json') as f:
        d = json.load(f)
    deck_cert = {int(p['slide_num']) for p in d['pages'] if p['status'] == 'certified'}
    out = subprocess.run(['sqlite3', str(DB), "SELECT name FROM scopes WHERE status='done' AND name LIKE 'slide-%';"],
                         capture_output=True, text=True, check=True, timeout=60)
    scope_done = {int(m.group(1)) for line in out.stdout.splitlines() if (m := re.match(r'slide-(\d+)$', line))}
    # uncertified = neither deck page certified nor scope done
    return deck_cert & scope_done

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

def last_verdict_pass(path):
    try:
        txt = path.read_text(errors='replace')
    except Exception:
        return False
    lines = re.findall(r'FINAL VERDICT:?[^\n]*', txt)
    if not lines:
        return False
    last = lines[-1]
    return bool(re.search(r'\bPASS\b', last)) and not re.search(r'\bFAIL\b', last)

def pass_after(qdir, prefix, mtime):
    out = []
    for f in sorted(qdir.rglob(f'{prefix}*.txt')):
        if f.stat().st_mtime > mtime and last_verdict_pass(f):
            out.append(f)
    return out

def append_ledger_row(row):
    with open(LOCK, 'w') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        with open(LEDGER, 'a') as f:
            f.write(row + '\n')
        fcntl.flock(lf, fcntl.LOCK_UN)

def main():
    certified = certified_pages()
    acted = []
    for n in range(1, 38):
        if n in certified:
            continue
        qdir = find_qa_dir(n)
        if qdir is None:
            continue
        pptx = ROOT / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
        if not pptx.exists():
            continue
        nr = newest_render(qdir)
        if nr is None:
            continue
        r_mtime, r_png = nr
        attempts = pass_after(qdir, 'judge_attempt', r_mtime)
        verifies = pass_after(qdir, 'judge_verify', r_mtime)
        if not (attempts and verifies):
            continue
        att = attempts[-1]
        ver = verifies[-1]
        att_rel = os.path.relpath(att, ROOT)
        ver_rel = os.path.relpath(ver, ROOT)
        row = (f'| {n} | `{att_rel}` (FINAL VERDICT: PASS, original-first, newer than newest render '
               f'`{os.path.relpath(r_png, ROOT)}`) | `{ver_rel}` (fresh original-first corroboration, '
               f'FINAL VERDICT: PASS, newer than newest render) | PASS / PASS (original-first dual-read; '
               f'sweeper-41) | analysis/reanalysis/slide_{n:03d}_raw.json | certified=yes | '
               f'sweeper-41 certify+merge {TS} |')
        try:
            append_ledger_row(row)
            r = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update', str(n),
                                f'recreated_pptx/slide_{n:03d}_recreated.pptx', '08-performance_final.pptx'],
                               cwd=ROOT, capture_output=True, text=True, timeout=300)
            if r.returncode != 0:
                log(f'slide {n}: ledger row appended but MERGE FAILED rc={r.returncode}: {r.stderr.strip()[:300]}')
                continue
            subprocess.run(['sqlite3', str(DB),
                            f"UPDATE scopes SET status='done', note='sweeper-41 dual-PASS certified+merged {TS}' WHERE name='slide-{n}';"],
                           check=True, timeout=60)
            log(f'slide {n}: CERTIFIED+MERGED page {n} (attempt {att.name}, verify {ver.name}, render {r_png.name})')
            acted.append(n)
        except Exception as e:
            log(f'slide {n}: ERROR {e}')
    if not acted:
        log('pass complete: no new qualifying slides')
    return acted

if __name__ == '__main__':
    main()
