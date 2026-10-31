#!/usr/bin/env python3
"""Sweeper pass: scan uncertified slides for dual-PASS evidence postdating the
newest render, merge qualifying slides into the final deck, ledger + DB.
When all 37 certified, run the merge gate and bank the report."""
import fcntl, json, os, re, sqlite3, subprocess, sys, time
from pathlib import Path

ROOT = Path('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure')
QA = ROOT / 'recreated_pptx/qa'
LEDGER = ROOT / 'pool_run/verification_ledger.md'
DB = ROOT / 'pool_run/mission.db'
DECK = ROOT / '08-performance_final.pptx'
FINAL_LEDGER = ROOT / 'final_deck_ledger.json'
GATE_REPORT = ROOT / 'pool_run/final_gate_report.txt'
DONE_SENTINEL = ROOT / 'pool_run/SWEEP_DONE'

def certified():
    d = json.load(open(FINAL_LEDGER))
    return set(p['slide_num'] for p in d['pages'] if p['status'] == 'certified')

def verdict_pass(p):
    try:
        txt = p.read_text(errors='replace')
    except OSError:
        return False
    if 'FINAL VERDICT' not in txt:
        return False
    tail = txt.split('FINAL VERDICT', 1)[1][:200]
    return 'PASS' in tail and 'FAIL' not in tail

def qa_dirs_for(n):
    out = []
    for d in sorted(QA.iterdir()):
        if d.is_dir():
            m = re.search(r'(\d+)$', d.name)
            if m and int(m.group(1)) == n:
                out.append(d)
    return out

def scan_slide(n):
    """Return (qa_dir, newest_render, best_attempt, best_verify) if qualifies else None."""
    for d in qa_dirs_for(n):
        renders = [p for p in d.glob('*.png') if p.name.startswith('render')]
        if not renders:
            continue
        newest = max(renders, key=lambda p: p.stat().st_mtime)
        R = newest.stat().st_mtime
        attempts = [p for p in d.glob('judge_attempt_*.txt') if p.stat().st_mtime > R]
        verifies = [p for p in d.glob('judge_verify_*.txt') if p.stat().st_mtime > R]
        if not attempts or not verifies:
            continue
        newest_verify = max(verifies, key=lambda p: p.stat().st_mtime)
        if not verdict_pass(newest_verify):
            continue  # newest verify is FAIL -> skip slide
        pass_attempts = [p for p in attempts if verdict_pass(p)]
        pass_verifies = [p for p in verifies if verdict_pass(p)]
        if not pass_attempts or not pass_verifies:
            continue
        att = max(pass_attempts, key=lambda p: p.stat().st_mtime)
        ver = max(pass_verifies, key=lambda p: p.stat().st_mtime)
        return d, newest, att, ver
    return None

def source_for(n):
    r = ROOT / 'analysis/reanalysis' / f'slide_{n:03d}_raw.json'
    if r.exists():
        return f'analysis/reanalysis/slide_{n:03d}_raw.json'
    r2 = ROOT / 'analysis' / f'slide_{n:03d}_raw.json'
    if r2.exists():
        return f'analysis/slide_{n:03d}_raw.json'
    return '—'

def append_ledger(n, att, ver, ok, note=''):
    row = (f'| {n} | `{att.relative_to(ROOT)}` | `{ver.relative_to(ROOT)}` '
           f'| PASS / PASS (original-first dual-read) | `{source_for(n)}` '
           f'| {"yes" if ok else "no"} | {note} |\n')
    with open(LEDGER, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row)
        fcntl.flock(f, fcntl.LOCK_UN)

def merge_slide(n):
    src = ROOT / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
    r = subprocess.run([sys.executable, 'pool_run/merge_final_deck.py', 'update',
                        str(n), str(src.relative_to(ROOT)), '08-performance_final.pptx'],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()

def db_done(n):
    for _ in range(5):
        try:
            con = sqlite3.connect(DB, timeout=10)
            con.execute("UPDATE scopes SET status='done', updated_at=datetime('now') WHERE name=?", (f'slide-{n}',))
            con.commit(); con.close()
            return True
        except sqlite3.OperationalError:
            time.sleep(5)
    return False

def run_gate():
    r = subprocess.run([sys.executable, 'pool_run/merge_final_deck.py', 'gate',
                        '08-performance_final.pptx', 'recreated_pptx', '37'],
                       cwd=ROOT, capture_output=True, text=True)
    out = r.stdout + r.stderr
    md5 = subprocess.run(['md5sum', '08-performance_final.pptx'], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    with open(GATE_REPORT, 'a') as f:
        f.write(f'=== final gate run {time.strftime("%Y-%m-%d %H:%M:%S")} exit={r.returncode} ===\n')
        f.write(out.strip() + '\n')
        f.write(md5 + '\n\n')
    return r.returncode == 0, out.strip()

def main():
    ts = time.strftime('%H:%M:%S')
    cert = certified()
    missing = [n for n in range(1, 38) if n not in cert]
    print(f'[{ts}] certified={len(cert)}/37 missing={missing}')
    if not missing:
        if DONE_SENTINEL.exists():
            print('already done, sentinel present')
            return
        ok, out = run_gate()
        print('GATE:', 'PASS' if ok else 'FAIL')
        print(out)
        if ok:
            DONE_SENTINEL.write_text(f'gate PASS {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
        return
    for n in missing:
        res = scan_slide(n)
        if not res:
            continue
        d, newest, att, ver = res
        ok, msg = merge_slide(n)
        now_cert = n in certified()
        dbok = db_done(n) if ok and now_cert else False
        note = f'sweeper {ts}; render={newest.name}'
        if ok and now_cert:
            note += f'; merged, db_done={dbok}, ledger confirmed'
        else:
            note += f'; MERGE FAILED: {msg[:200]}'
        append_ledger(n, att, ver, ok and now_cert, note)
        print(f'  slide {n}: att={att.name} ver={ver.name} merge_ok={ok} certified_now={now_cert} :: {msg[:120]}')

if __name__ == '__main__':
    main()
