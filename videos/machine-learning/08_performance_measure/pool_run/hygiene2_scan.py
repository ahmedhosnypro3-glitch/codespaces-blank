#!/usr/bin/env python3
"""Deeper ledger/hygiene cross-check for 08_performance_measure (120s lane).

Per slide N in 1..37 compares:
  - dual-PASS transcripts under recreated_pptx/qa/slideNNN/
  - final_deck_ledger.json page status + source_md5 vs md5 of the slide pptx
  - pool_run/verification_ledger.md rows (any row / certified=yes row)
  - pool_run/mission.db scopes slide-N status

Sanctioned fixes only (append-only / idempotent):
  1. dual PASS but no ledger row for the slide -> flock-append row (skip if a
     row exists for the slide)
  2. certified (json or ledger row) but scope not done ->
     sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"
  3. scope done but page not certified or source_md5 stale ->
     python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx
     (run from namespace root, only when the deck lock is free)

stdout: one summary line "certified=N/37 consistent=T/F fixes=K"
stderr: fix diagnostics (loop appends these to hygiene2_detail.log)
"""
import fcntl
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(ROOT, 'recreated_pptx', 'qa')
LEDGER_JSON = os.path.join(ROOT, 'final_deck_ledger.json')
VLEDGER = os.path.join(ROOT, 'pool_run', 'verification_ledger.md')
DB_REL = os.path.join('pool_run', 'mission.db')
DB = os.path.join(ROOT, DB_REL)
DECK_REL = '08-performance_final.pptx'
LOCK = os.path.join(ROOT, DECK_REL + '.lock')
N_SLIDES = 37


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def verdict_pass(path):
    try:
        with open(path, errors='replace') as f:
            for line in f:
                if 'FINAL VERDICT' in line:
                    return 'PASS' in line and 'FAIL' not in line
    except OSError:
        pass
    return False


def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def dual_pass_set():
    dual = {}
    if not os.path.isdir(QA):
        return dual
    for d in sorted(os.listdir(QA)):
        m = re.fullmatch(r'slide0*(\d+)', d)
        if not m:
            continue
        n = int(m.group(1))
        dd = os.path.join(QA, d)
        att = sorted(f for f in os.listdir(dd)
                     if re.fullmatch(r'judge_attempt_.*\.txt', f)
                     and verdict_pass(os.path.join(dd, f)))
        ver = sorted(f for f in os.listdir(dd)
                     if re.fullmatch(r'judge_verify_.*\.txt', f)
                     and verdict_pass(os.path.join(dd, f)))
        if att and ver:
            dual[n] = (att[0], ver[0])
    return dual


def load_ledger_json():
    with open(LEDGER_JSON) as f:
        return json.load(f)['pages']


def certified_pages():
    return {p['slide_num']: p for p in load_ledger_json() if p['status'] == 'certified'}


def vledger_rows():
    """All table rows keyed by slide number; value = (certified_yes, raw line)."""
    any_row = {}
    yes_row = {}
    with open(VLEDGER, errors='replace') as f:
        for line in f:
            if not line.startswith('|') or line.startswith('| slide') or line.startswith('|---'):
                continue
            cells = [c.strip() for c in line.split('|')]
            try:
                s = int(cells[1].lstrip('0') or '0')
            except (ValueError, IndexError):
                continue
            any_row.setdefault(s, []).append(line.rstrip('\n'))
            if len(cells) > 6 and cells[6].lower() in ('yes', 'certified=yes'):
                yes_row[s] = line.rstrip('\n')
    return any_row, yes_row


def db_done():
    for _ in range(5):
        try:
            con = sqlite3.connect(DB, timeout=10)
            rows = con.execute(
                "SELECT name FROM scopes WHERE status='done' AND name LIKE 'slide-%'").fetchall()
            con.close()
            return {int(r[0].split('-')[1]) for r in rows}
        except sqlite3.OperationalError:
            time.sleep(5)
    return set()


def db_set_done(n):
    for _ in range(5):
        r = subprocess.run(
            ['sqlite3', DB_REL,
             f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
            cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            return True
        time.sleep(5)
    return False


def lock_free():
    try:
        fd = os.open(LOCK, os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(fd, fcntl.LOCK_UN)
            return True
        finally:
            os.close(fd)
    except OSError:
        return False


def append_ledger_row(n, att, ver):
    reanalysis = os.path.join('analysis', 'reanalysis', f'slide_{n:03d}_raw.json')
    reanalysis_cell = reanalysis if os.path.exists(os.path.join(ROOT, reanalysis)) else '-'
    row = (f"| {n} | recreated_pptx/qa/slide{n:03d}/{att} | "
           f"recreated_pptx/qa/slide{n:03d}/{ver} | PASS / PASS (original-first dual-read) | "
           f"{reanalysis_cell} | yes | appended by hygiene2 agent (dual PASS transcripts found, no row existed) |")
    with open(VLEDGER, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        any_row, _ = vledger_rows()
        if n not in any_row:
            f.write(row + '\n')
            fcntl.flock(f, fcntl.LOCK_UN)
            return True
        fcntl.flock(f, fcntl.LOCK_UN)
    return False


def merge_update(n):
    src_rel = f'recreated_pptx/slide_{n:03d}_recreated.pptx'
    r = subprocess.run([sys.executable, os.path.join('pool_run', 'merge_final_deck.py'),
                        'update', str(n), src_rel, DECK_REL],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def fresh(cert):
    """Certified pages whose ledger source_md5 matches the current slide pptx."""
    out = {}
    for n, p in cert.items():
        src = os.path.join(ROOT, 'recreated_pptx', f'slide_{n:03d}_recreated.pptx')
        out[n] = os.path.exists(src) and p.get('source_md5') == md5_file(src)
    return out


def main():
    os.chdir(ROOT)
    fixes = 0

    dual = dual_pass_set()
    cert = certified_pages()
    any_row, yes_row = vledger_rows()
    done = db_done()

    # Fix 1: dual PASS but no ledger row at all for the slide
    for n in sorted(set(dual) - set(any_row)):
        if append_ledger_row(n, dual[n][0], dual[n][1]):
            fixes += 1
            log(f'fix1 ledger-row-appended slide-{n}')
        else:
            log(f'fix1 skipped slide-{n} (row appeared under lock)')

    # Fix 2: certified in json or ledger row, but scope not done in mission.db
    for n in sorted((set(cert) | set(yes_row)) - done):
        if db_set_done(n):
            fixes += 1
            log(f'fix2 scope-done slide-{n}')
        else:
            log(f'fix2 FAILED slide-{n}')

    # Fix 3: scope done but page not certified or source_md5 stale
    if lock_free():
        done = db_done()
        cert = certified_pages()
        pages = {p['slide_num']: p for p in load_ledger_json()}
        for n in sorted(done):
            src = os.path.join(ROOT, 'recreated_pptx', f'slide_{n:03d}_recreated.pptx')
            if not os.path.exists(src):
                continue
            p = pages.get(n)
            merged = p is not None and p['status'] == 'certified' and p['source_md5'] == md5_file(src)
            if not merged:
                ok, out = merge_update(n)
                fixes += 1
                log(f'fix3 merge-update slide-{n} {"ok" if ok else "FAILED: " + out}')
    else:
        log('fix3 skipped: deck lock held')

    # Re-read state after fixes for the summary line
    dual = dual_pass_set()
    cert = certified_pages()
    any_row, yes_row = vledger_rows()
    done = db_done()
    fr = fresh(cert)
    consistent = (set(dual) == set(cert) == set(yes_row) == set(done)
                  and all(fr.values()) and len(fr) == len(cert))
    print(f"certified={len(cert)}/{N_SLIDES} "
          f"consistent={'T' if consistent else 'F'} fixes={fixes}")
    if not consistent:
        log(f"inconsistent: dual={sorted(dual)} cert={sorted(cert)} "
            f"yes_rows={sorted(yes_row)} done={sorted(done)} stale_md5={sorted(n for n, v in fr.items() if not v)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
