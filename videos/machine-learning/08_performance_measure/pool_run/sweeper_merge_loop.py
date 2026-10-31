#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure.

Each pass: for slides 1..37 not yet certified in final_deck_ledger.json, find the
qa dir, newest render mtime R, then require a judge_attempt_*.txt with
FINAL VERDICT PASS and mtime > R AND the newest judge_verify_*.txt with mtime > R
also FINAL VERDICT PASS. Qualifying slides get: flock-appended ledger row,
merge_final_deck.py update, mission.db scope done, certified confirmation.
"""
import json, os, glob, re, subprocess, sys, time

ROOT = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
os.chdir(ROOT)
LEDGER = 'pool_run/verification_ledger.md'
OUT = '08-performance_final.pptx'
DB = 'pool_run/mission.db'


def verdict(path):
    try:
        with open(path, 'r', errors='replace') as f:
            txt = f.read()
        m = re.findall(r'FINAL VERDICT:\s*(PASS|FAIL)', txt)
        return m[-1] if m else None
    except Exception:
        return None


def certified_set():
    with open('final_deck_ledger.json') as f:
        d = json.load(f)
    return set(p['slide_num'] for p in d['pages'] if p['status'] == 'certified')


def scan():
    cert = certified_set()
    todo = [N for N in range(1, 38) if N not in cert]
    all_dirs = [x for x in glob.glob('recreated_pptx/qa/slide*') if os.path.isdir(x)]
    out = []
    for N in todo:
        dirs = [x for x in all_dirs if re.fullmatch(rf'slide_?0*{N}', os.path.basename(x))]
        if not dirs:
            continue
        dd = dirs[0]
        renders = [r for r in glob.glob(f'{dd}/*.png') if os.path.basename(r).startswith('render')]
        if not renders:
            continue
        R = max(renders, key=os.path.getmtime)
        Rt = os.path.getmtime(R)
        attempts = sorted(glob.glob(f'{dd}/judge_attempt_*.txt'), key=os.path.getmtime)
        verifies = sorted(glob.glob(f'{dd}/judge_verify_*.txt'), key=os.path.getmtime)
        att_pass = [a for a in attempts if os.path.getmtime(a) > Rt and verdict(a) == 'PASS']
        ver = [v for v in verifies if os.path.getmtime(v) > Rt]
        if not att_pass or not ver:
            continue
        newest_ver = ver[-1]
        if verdict(newest_ver) != 'PASS':
            continue  # newest verify is FAIL (or unparseable) -> skip
        ver_pass = [v for v in ver if verdict(v) == 'PASS']
        src = f'analysis/reanalysis/slide_{N:03d}_raw.json'
        if not os.path.exists(src):
            cands = glob.glob(f'analysis/reanalysis/slide_{N:03d}*.json') or glob.glob(f'analysis/slide_{N:03d}*.json')
            src = cands[0] if cands else '—'
        out.append((N, dd, att_pass[-1], ver_pass[-1], newest_ver, src, os.path.basename(R)))
    return out


def merge_one(N, dd, att, ver, src, render):
    pptx = f'recreated_pptx/slide_{N:03d}_recreated.pptx'
    if not os.path.exists(pptx):
        print(f'[slide {N}] no recreated pptx at {pptx}, skipping', flush=True)
        return False
    row = (f"| {N} | `{att}` | `{ver}` | PASS / PASS (original-first dual-read, "
           f"postdate newest render {render}; sweeper-merge) | {src} | yes | "
           f"merged by sweeper {time.strftime('%Y-%m-%d %H:%M:%S')} |\n")
    with open(LEDGER, 'a') as f:
        fcntl = __import__('fcntl')
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(row)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    r = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update', str(N), pptx, OUT],
                       capture_output=True, text=True)
    if r.returncode != 0:
        with open(LEDGER, 'a') as f:
            fcntl = __import__('fcntl')
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(f"| {N} | `{att}` | `{ver}` | MERGE FAILED rc={r.returncode}: {r.stderr.strip()[:200]} | {src} | no | sweeper |\n")
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        print(f'[slide {N}] MERGE FAILED rc={r.returncode}: {r.stderr.strip()[:300]}', flush=True)
        return False
    subprocess.run(['sqlite3', DB, f"UPDATE scopes SET status='done' WHERE name='slide-{N}';"],
                   capture_output=True)
    ok = N in certified_set()
    print(f'[slide {N}] merged: attempt={os.path.basename(att)} verify={os.path.basename(ver)} '
          f'certified_in_ledger={ok}', flush=True)
    return ok


def main():
    deadline = time.time() + 40 * 60
    while time.time() < deadline:
        try:
            qual = scan()
        except Exception as e:
            print(f'scan error: {e}', flush=True)
            qual = []
        if qual:
            print(f'pass {time.strftime("%H:%M:%S")}: {len(qual)} qualifying: {[q[0] for q in qual]}', flush=True)
            for (N, dd, att, ver, nv, src, render) in qual:
                try:
                    merge_one(N, dd, att, ver, src, render)
                except Exception as e:
                    print(f'[slide {N}] merge exception: {e}', flush=True)
        else:
            print(f'pass {time.strftime("%H:%M:%S")}: no qualifying slides; certified={sorted(certified_set())}', flush=True)
        if len(certified_set()) >= 37:
            print('ALL 37 CERTIFIED — running final gate', flush=True)
            r = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'gate', OUT, 'recreated_pptx', '37'],
                               capture_output=True, text=True)
            rep = 'pool_run/final_gate_report_20261031.txt'
            with open(rep, 'w') as f:
                f.write(f'final gate run {time.strftime("%Y-%m-%d %H:%M:%S")} rc={r.returncode}\n')
                f.write(r.stdout)
                f.write(r.stderr)
            print(f'gate rc={r.returncode}, report banked at {rep}', flush=True)
            print(r.stdout[-2000:], flush=True)
            return
        time.sleep(45)
    print('40-minute loop elapsed without all 37 certified', flush=True)


if __name__ == '__main__':
    main()
