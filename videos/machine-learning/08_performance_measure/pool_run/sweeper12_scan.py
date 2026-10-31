#!/usr/bin/env python3
"""Scan qa/slideNNN/ for dual-PASS uncertified slides and attempt-PASS slides
lacking a verify PASS. Prints machine-readable lines. Run from namespace root."""
import glob
import json
import os
import re

NS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(NS)

PASS = re.compile(r'FINAL VERDICT:\s*\*{0,2}\s*PASS', re.I)


def verdict_pass(path):
    try:
        with open(path, errors='ignore') as f:
            return bool(PASS.search(f.read()))
    except OSError:
        return False


def main():
    with open('final_deck_ledger.json') as f:
        ledger = json.load(f)
    cert = {p['page'] for p in ledger['pages'] if p['status'] == 'certified'}
    dual, need_verify = [], []
    for n in range(1, 38):
        d = f'recreated_pptx/qa/slide{n:03d}'
        if not os.path.isdir(d):
            continue
        att = [p for p in sorted(glob.glob(d + '/judge_attempt_*.txt')) if verdict_pass(p)]
        ver = [p for p in sorted(glob.glob(d + '/judge_verify_*.txt')) if verdict_pass(p)]
        if n in cert:
            continue
        if att and ver:
            dual.append((n, att[-1], ver[-1]))
        elif att and not ver:
            need_verify.append((n, att[-1]))
    for n, a, v in dual:
        print(f'DUAL {n} {a} {v}')
    for n, a in need_verify:
        print(f'NEEDVERIFY {n} {a}')
    print(f'CERTIFIED {len(cert)}/37')


if __name__ == '__main__':
    main()
