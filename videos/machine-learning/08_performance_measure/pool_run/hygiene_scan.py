#!/usr/bin/env python3
"""Ledger/hygiene cross-check for 08_performance_measure.

Compares, per slide N in 1..37:
  - dual-PASS transcripts under recreated_pptx/qa/slideNNN/
  - final_deck_ledger.json page status
  - pool_run/verification_ledger.md certified=yes rows
  - pool_run/mission.db scopes slide-N status
  - merge freshness (ledger source_md5 vs current slide pptx md5)

Fixes (append-only / idempotent only):
  1. dual PASS but no ledger row  -> flock-append row to verification_ledger.md
  2. page certified but scope not done -> UPDATE scopes SET status='done'
  3. scope done but page not merged    -> merge_final_deck.py update N
Prints a one-line summary for hygiene.log.
"""
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
DB = os.path.join(ROOT, 'pool_run', 'mission.db')
DECK = os.path.join(ROOT, '08-performance_final.pptx')
LOCK = DECK + '.lock'
N_SLIDES = 37


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


def certified_pages():
    with open(LEDGER_JSON) as f:
        led = json.load(f)
    return {p['slide_num']: p for p in led['pages'] if p['status'] == 'certified'}


def ledger_yes_rows():
    yes = {}
    with open(VLEDGER) as f:
        for line in f:
            if not line.startswith('|') or line.startswith('| slide') or line.startswith('|---'):
                continue
            cells = [c.strip() for c in line.split('|')]
            try:
                s = int(cells[1].lstrip('0') or '0')
            except (ValueError, IndexError):
                continue
            if len(cells) > 6 and cells[6].lower() in ('yes', 'certified=yes'):
                yes[s] = line.rstrip('\n')
    return yes


def db_done():
    for attempt in range(5):
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
    for attempt in range(5):
        try:
            con = sqlite3.connect(DB, timeout=10)
            con.execute("UPDATE scopes SET status='done' WHERE name=?", (f'slide-{n}',))
            con.commit()
            con.close()
            return True
        except sqlite3.OperationalError:
            time.sleep(5)
    return False


def lock_free():
    try:
        fd = os.open(LOCK, os.O_RDWR)
        try:
            import fcntl
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
           f"{reanalysis_cell} | yes | appended by hygiene agent (dual PASS transcripts found, row was missing) |")
    with open(VLEDGER, 'a') as f:
        import fcntl
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)


def merge_update(n):
    src = os.path.join(ROOT, 'recreated_pptx', f'slide_{n:03d}_recreated.pptx')
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'pool_run', 'merge_final_deck.py'),
                        'update', str(n), src, DECK],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def main():
    fixes = []
    dual = dual_pass_set()
    cert = certified_pages()
    rows = ledger_yes_rows()
    done = db_done()

    # Fix 1: dual PASS but missing verification_ledger row
    for n in sorted(set(dual) - set(rows)):
        append_ledger_row(n, dual[n][0], dual[n][1])
        fixes.append(f'ledger-row-appended slide-{n}')
    # Fix 2: certified in ledger json but scope not done
    for n in sorted(set(cert) - done):
        if db_set_done(n):
            fixes.append(f'scope-done slide-{n}')
    # Fix 3: scope done but page not merged (not certified or md5 stale)
    done = db_done()
    cert = certified_pages()
    if lock_free():
        for n in sorted(done):
            src = os.path.join(ROOT, 'recreated_pptx', f'slide_{n:03d}_recreated.pptx')
            if not os.path.exists(src):
                continue
            p = next((q for q in json.load(open(LEDGER_JSON))['pages'] if q['slide_num'] == n), None)
            merged = p is not None and p['status'] == 'certified' and p['source_md5'] == md5_file(src)
            if not merged:
                ok, out = merge_update(n)
                fixes.append(f'merge-update slide-{n} {"ok" if ok else "FAILED: " + out}')

    dual_s = sorted(dual)
    cert_s = sorted(cert)
    rows_s = sorted(rows)
    done_s = sorted(done)
    consistent = (set(dual_s) == set(cert_s) == set(rows_s) == set(done_s))
    print(f"certified={len(cert_s)}/37 dual={len(dual_s)} ledger_rows={len(rows_s)} "
          f"done={len(done_s)} consistent={consistent} fixes={len(fixes)} "
          f"lock={'free' if lock_free() else 'held'}"
          + (f" | {'; '.join(fixes)}" if fixes else ""))
    return 0


if __name__ == '__main__':
    os.chdir(ROOT)
    sys.exit(main())
