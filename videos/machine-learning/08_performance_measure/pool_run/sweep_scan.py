#!/usr/bin/env python3
"""Sweeper scan: for each slide 1..37 not certified, check qa dir for
newest render R, judge_attempt_*.txt PASS with mtime>R, judge_verify_*.txt
PASS with mtime>R. Prints qualifying slides with details."""
import json, os, re, sys
from pathlib import Path

ROOT = Path('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure')
QA = ROOT / 'recreated_pptx/qa'

def certified():
    d = json.load(open(ROOT / 'final_deck_ledger.json'))
    return set(p['slide_num'] for p in d['pages'] if p['status'] == 'certified')

def has_pass(p):
    try:
        txt = p.read_text(errors='replace')
    except OSError:
        return False
    return 'FINAL VERDICT' in txt and 'PASS' in txt.split('FINAL VERDICT', 1)[1][:200]

def qa_dirs_for(n):
    out = []
    for d in sorted(QA.iterdir()):
        if not d.is_dir():
            continue
        m = re.search(r'(\d+)$', d.name)
        if m and int(m.group(1)) == n:
            out.append(d)
    return out

def scan_slide(n):
    results = []
    for d in qa_dirs_for(n):
        renders = [p for p in d.glob('*.png') if p.name.startswith('render')]
        if not renders:
            results.append((d, None, [], []))
            continue
        newest = max(renders, key=lambda p: p.stat().st_mtime)
        R = newest.stat().st_mtime
        attempts = sorted([p for p in d.glob('judge_attempt_*.txt')
                           if p.stat().st_mtime > R and has_pass(p)],
                          key=lambda p: p.stat().st_mtime)
        verifies = sorted([p for p in d.glob('judge_verify_*.txt')
                           if p.stat().st_mtime > R and has_pass(p)],
                          key=lambda p: p.stat().st_mtime)
        # newest verify overall (to detect FAIL superseding)
        all_verifies = sorted(d.glob('judge_verify_*.txt'), key=lambda p: p.stat().st_mtime)
        newest_verify = all_verifies[-1] if all_verifies else None
        results.append((d, newest, attempts, verifies, newest_verify))
    return results

def main():
    cert = certified()
    print('certified:', ' '.join(map(str, sorted(cert))))
    missing = [n for n in range(1, 38) if n not in cert]
    print('missing:', ' '.join(map(str, missing)))
    print()
    qualifying = []
    for n in missing:
        for res in scan_slide(n):
            d, newest, attempts, verifies = res[0], res[1], res[2], res[3]
            nv = res[4] if len(res) > 4 else None
            status = ''
            if newest is None:
                status = 'NO RENDERS'
            elif attempts and verifies:
                status = 'QUALIFIES'
                qualifying.append((n, d, newest, attempts[-1], verifies[-1]))
            elif not attempts and not verifies:
                status = 'no post-render transcripts'
            else:
                status = f'attempts={len(attempts)} verifies={len(verifies)}'
            print(f'slide {n:2d} dir={d.name} newest_render={newest.name if newest else None} -> {status}')
            if nv is not None and newest is not None and nv.stat().st_mtime > newest.stat().st_mtime and not has_pass(nv):
                print(f'    NOTE: newest verify {nv.name} is FAIL/other -> skip per rule')
    print()
    print('QUALIFYING:', ' '.join(str(q[0]) for q in qualifying))
    for n, d, newest, att, ver in qualifying:
        print(f'  slide {n}: render={newest.name} attempt={att.name} verify={ver.name}')

if __name__ == '__main__':
    main()
