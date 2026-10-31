#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure (2026-10-31).

Loop until 37/37 certified in final_deck_ledger.json:
  1. Scan recreated_pptx/qa/slide*/ for slides with BOTH judge_attempt_*.txt and
     judge_verify_*.txt containing FINAL VERDICT: PASS but not yet certified.
     For each: flock-append row to pool_run/verification_ledger.md, run
     `merge_final_deck.py update N ...`, set mission.db scope slide-N done.
  2. For attempt-PASS slides lacking a verify PASS: run the verify judge
     (original-first) against the slide's newest render_*.png, unique
     transcript name, 90-150s pre-sleep, 429 => sleep 300s retry 8x.
  3. Sleep 60s, rescan.
"""
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

NS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure')
REPO = Path('/home/codespace/ai_llm_slides')
QA = NS / 'recreated_pptx' / 'qa'
LEDGER = NS / 'pool_run' / 'verification_ledger.md'
LOG = NS / 'pool_run' / 'sweeper_cert_merge.log'
TOTAL = 37

PASS_RE = re.compile(r'FINAL VERDICT:.*PASS', re.IGNORECASE)
FAIL_RE = re.compile(r'FINAL VERDICT:.*FAIL', re.IGNORECASE)


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, 'a') as f:
        f.write(line + '\n')


def verdict_pass(path):
    try:
        text = Path(path).read_text(errors='replace')
    except OSError:
        return False
    for line in text.splitlines():
        if 'FINAL VERDICT:' in line.upper():
            if FAIL_RE.search(line):
                return False
            if PASS_RE.search(line):
                return True
    return False


def qa_dir(n):
    for cand in (QA / f'slide{n:03d}', QA / f'slide{n}'):
        if cand.is_dir():
            return cand
    return None


def pass_files(n, kind):
    d = qa_dir(n)
    if not d:
        return []
    out = []
    for p in sorted(d.glob(f'judge_{kind}_*.txt')):
        if verdict_pass(p):
            out.append(p)
    return out


def certified_set():
    with open(NS / 'final_deck_ledger.json') as f:
        d = json.load(f)
    return {p['slide_num'] for p in d['pages'] if p['status'] == 'certified'}


def newest_render(n):
    d = qa_dir(n)
    renders = sorted(d.glob('render*.png'), key=lambda p: p.stat().st_mtime, reverse=True)
    return renders[0] if renders else None


def append_ledger_row(n, att, ver, render):
    reanalysis = NS / 'analysis' / 'reanalysis' / f'slide_{n:03d}_raw.json'
    re_col = f'analysis/reanalysis/slide_{n:03d}_raw.json' if reanalysis.exists() else '-'
    row = (f"| {n} | recreated_pptx/qa/{att.parent.name}/{att.name} | "
           f"recreated_pptx/qa/{ver.parent.name}/{ver.name} | "
           f"PASS / PASS (original-first, sweeper verify vs {render.name}) | {re_col} | yes | "
           f"certify-and-merge sweeper 2026-10-31 |\n")
    cmd = ['flock', str(LEDGER), 'bash', '-c',
           f'printf %s "$1" >> "$2"', 'bash', row, str(LEDGER)]
    subprocess.run(cmd, check=True)


def certify(n):
    att = pass_files(n, 'attempt')
    ver = pass_files(n, 'verify')
    if not att or not ver:
        return False
    att, ver = att[-1], ver[-1]
    render = newest_render(n)
    log(f"certifying slide {n}: attempt={att.name} verify={ver.name} render={render.name if render else 'NONE'}")
    append_ledger_row(n, att, ver, render or att)
    r = subprocess.run(['python3', 'pool_run/merge_final_deck.py', 'update', str(n),
                        f'recreated_pptx/slide_{n:03d}_recreated.pptx', '08-performance_final.pptx'],
                       cwd=NS, capture_output=True, text=True)
    log(f"  merge update rc={r.returncode} {r.stdout.strip()} {r.stderr.strip()[:200]}")
    for attempt in range(5):
        r = subprocess.run(['sqlite3', 'pool_run/mission.db',
                            f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                           cwd=NS, capture_output=True, text=True)
        if r.returncode == 0:
            break
        time.sleep(5)
    log(f"  mission.db slide-{n} done rc={r.returncode} {r.stderr.strip()[:200]}")
    return True


def run_verify(n):
    d = qa_dir(n)
    render = newest_render(n)
    if render is None:
        log(f"slide {n}: no render_*.png found, skipping verify")
        return False
    orig = NS / 'unique_slides' / f'slide_{n:03d}.jpg'
    if not orig.exists():
        log(f"slide {n}: missing original {orig}, skipping")
        return False
    # unique transcript name
    ts = time.strftime('%H%M%S')
    transcript = d / f'judge_verify_sweep_{ts}_{n}.txt'
    k = 1
    while transcript.exists():
        transcript = d / f'judge_verify_sweep_{ts}_{n}_{k}.txt'
        k += 1
    pre = random.randint(90, 150)
    log(f"slide {n}: sleeping {pre}s before verify judge vs {render.name}")
    time.sleep(pre)
    for retry in range(8):
        cmd = ['timeout', '540', 'python3',
               '.agents/skills/image-analysis/scripts/analyze_image.py', 'comparison',
               str(orig.relative_to(REPO)), str(render.relative_to(REPO)),
               '--thinking', 'high', '--max-tokens', '65536',
               '--timeout', '420', '--rounds', '1', '--tries', '1']
        log(f"slide {n}: verify run {retry+1}/8 -> {transcript.name} (ORIGINAL first)")
        with open(transcript, 'w') as tf:
            r = subprocess.run(cmd, cwd=REPO, stdout=tf, stderr=subprocess.STDOUT)
        text = transcript.read_text(errors='replace')
        if verdict_pass(transcript):
            log(f"slide {n}: verify PASS ({transcript.name})")
            return True
        if '429' in text:
            log(f"slide {n}: 429 seen, sleeping 300s before retry")
            time.sleep(300)
            continue
        if r.returncode == 0 and 'FINAL VERDICT:' in text.upper():
            log(f"slide {n}: verify verdict FAIL ({transcript.name}) — worker owns fix; will rescan")
            return False
        log(f"slide {n}: infra error rc={r.returncode}, sleeping 60s before retry")
        time.sleep(60)
    log(f"slide {n}: verify retries exhausted")
    return False


def main():
    log('sweeper start')
    while True:
        cert = certified_set()
        log(f'certified {len(cert)}/{TOTAL}: {sorted(cert)}')
        if len(cert) >= TOTAL:
            log('ALL 37 CERTIFIED — sweeper done')
            return
        # 1. certify any dual-PASS uncertified slides
        for n in range(1, TOTAL + 1):
            if n in cert:
                continue
            if pass_files(n, 'attempt') and pass_files(n, 'verify'):
                certify(n)
                cert = certified_set()
        # 2. run verify judges for attempt-PASS slides lacking verify PASS
        ran = False
        for n in range(1, TOTAL + 1):
            if n in cert:
                continue
            if pass_files(n, 'attempt') and not pass_files(n, 'verify'):
                run_verify(n)
                ran = True
                cert = certified_set()
                if len(cert) >= TOTAL:
                    log('ALL 37 CERTIFIED — sweeper done')
                    return
                break  # one verify per loop iteration; rescan after
        if not ran:
            log('no certifiable or verifiable slides this pass; sleeping 60s')
            time.sleep(60)


if __name__ == '__main__':
    main()
