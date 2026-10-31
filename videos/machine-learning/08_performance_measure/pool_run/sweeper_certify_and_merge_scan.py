#!/usr/bin/env python3
"""One sweep pass: find slides 1..37 not yet certified that have a dual PASS
(attempt + verify, both FINAL VERDICT PASS, both postdating the newest render
png in the slide's qa dir). Prints qualifying slides as JSON."""
import json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / 'recreated_pptx' / 'qa'

certified = set()
ledger = json.load(open(ROOT / 'final_deck_ledger.json'))
for p in ledger['pages']:
    if p['status'] == 'certified':
        certified.add(int(p['slide_num']))

def find_qa_dir(n):
    # dirs like slideNNN, slideNN, slide_NNN
    pats = [f'slide{n:03d}', f'slide{n}', f'slide_{n:03d}']
    for pat in pats:
        d = QA / pat
        if d.is_dir():
            return d
    return None

def newest_render_mtime(qdir):
    best = None
    for f in qdir.rglob('*.png'):
        if 'render' in f.name.lower():
            m = f.stat().st_mtime
            if best is None or m > best[0]:
                best = (m, f)
    return best

def pass_transcripts(qdir, prefix):
    """Return list of (mtime, path) for transcripts matching prefix with FINAL VERDICT: PASS."""
    out = []
    for f in sorted(qdir.rglob(f'{prefix}*.txt')):
        try:
            txt = f.read_text(errors='replace')
        except Exception:
            continue
        if re.search(r'FINAL VERDICT:\s*PASS', txt):
            out.append((f.stat().st_mtime, f))
    return out

results = []
for n in range(1, 38):
    if n in certified:
        continue
    qdir = find_qa_dir(n)
    if qdir is None:
        results.append({'slide': n, 'status': 'no_qa_dir'})
        continue
    pptx = ROOT / 'recreated_pptx' / f'slide_{n:03d}_recreated.pptx'
    nr = newest_render_mtime(qdir)
    if nr is None:
        if pptx.exists():
            results.append({'slide': n, 'status': 'no_render_pptx_exists_skip'})
        else:
            results.append({'slide': n, 'status': 'no_render_no_pptx'})
        continue
    r_mtime, r_png = nr
    attempts = [x for x in pass_transcripts(qdir, 'judge_attempt') if x[0] > r_mtime]
    verifies = [x for x in pass_transcripts(qdir, 'judge_verify') if x[0] > r_mtime]
    all_verifies = pass_transcripts(qdir, 'judge_verify')
    newest_verify = max(all_verifies, default=None)
    if newest_verify and not re.search(r'FINAL VERDICT:\s*PASS', newest_verify[1].read_text(errors='replace')):
        results.append({'slide': n, 'status': 'newest_verify_not_pass_skip',
                        'qa': str(qdir), 'render': str(r_png)})
        continue
    if attempts and verifies:
        results.append({'slide': n, 'status': 'qualifies',
                        'qa': str(qdir), 'render': str(r_png), 'render_mtime': r_mtime,
                        'attempt': attempts[-1][1].__str__(), 'attempt_mtime': attempts[-1][0],
                        'verify': verifies[-1][1].__str__(), 'verify_mtime': verifies[-1][0]})
    else:
        results.append({'slide': n, 'status': 'not_yet',
                        'qa': str(qdir), 'render': str(r_png),
                        'n_attempt_pass_after_render': len(attempts),
                        'n_verify_pass_after_render': len(verifies)})

print(json.dumps(results, indent=1))
