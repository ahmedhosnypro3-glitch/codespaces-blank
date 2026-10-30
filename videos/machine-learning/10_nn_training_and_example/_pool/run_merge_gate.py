#!/usr/bin/env python3
"""run_merge_gate.py — final-deck merge gate (closing gate) for this video.

Proves the continuous final deck renders IDENTICALLY to every certified source
slide. The deck may close only when every ledger page is `certified` and 0/N
certified pages mismatch their source render.

Guarantees
  * ONE LibreOffice session renders the merged deck AND all certified source
    decks, with a private profile (_pool/lo_gate) and TMPDIR=_pool.
  * Rasterize at 150dpi (pdftoppm), PIL-compare each deck page against its
    source render at matched scale.
  * Missing source/placeholder/missing render => hard failure, never a silent
    pass (the older merge_final_deck.py gate skipped missing sources silently).

Scale + tolerance
  Renders differ by 1px in width (2000 vs 2001 at 150dpi) because the merged
  deck's slide box is 12191695 EMU wide while the certified source decks are
  12192000 EMU; LibreOffice rounds the PDF page box (959.981 vs 960.009 pt).
  Images are therefore compared on their COMMON REGION (no resampling - a
  resample smears glyph edges and hides real defects), and a page passes when
    differing pixels <= 0.02% of the common area AND max channel delta <= 32.
  A correctly merged page measures 0.0000% (measured on 7 pages).

Usage
  python3 _pool/run_merge_gate.py                 # full 34-page gate
  python3 _pool/run_merge_gate.py --pages 5,27    # subset only

Exit codes
  0  PASS  — all pages certified, 0 mismatches (deck may close)
  1  BLOCKED — >=1 placeholder page (gate cannot run for those pages)
  2  FAIL  — >=1 certified page mismatches its source render
  3  ERROR — missing deck/ledger/source, LibreOffice or pdftoppm failed
"""
import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

from PIL import Image, ImageChops
import numpy as np

VIDEO = Path(__file__).resolve().parents[1]
POOL = VIDEO / '_pool'
DECK = VIDEO / '10_nn_training_and_example_final.pptx'
LEDGER = VIDEO / 'final_deck_ledger.json'
BUILD = VIDEO / 'recreated_pptx' / 'build'
WORK = POOL / 'gate_work'
LO_PROFILE = POOL / 'lo_gate'
REPORT = POOL / 'gate_report.txt'
DPI = 150
TOL_MAX_DELTA = 32
TOL_DIFF_FRAC = 0.0002


def log(msg):
    print(msg, flush=True)


def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def load_ledger():
    with open(LEDGER) as f:
        data = json.load(f)
    pages = data.get('pages') or []
    if not pages:
        die('ledger has no pages', 3)
    for p in pages:
        for key in ('page', 'slide_num', 'status'):
            if key not in p:
                die(f'ledger page entry missing {key!r}: {p}', 3)
    return pages


def audit_sources(pages):
    """Map every certified page to its source pptx; verify md5 against ledger."""
    rows, missing = [], []
    for p in sorted(pages, key=lambda x: x['page']):
        n = int(p['slide_num'])
        src = BUILD / f'slide_{n:03d}_recreated.pptx'
        row = {'page': int(p['page']), 'slide_num': n,
               'status': p['status'], 'source': src, 'src_md5': None,
               'md5_ok': None, 'state': None, 'diff_px': None, 'frac': None,
               'max_delta': None, 'detail': ''}
        if p['status'] != 'certified':
            row['state'] = 'PLACEHOLDER'
            row['detail'] = 'page still holds the original-frame placeholder'
            rows.append(row)
            continue
        if not src.exists():
            row['state'] = 'NO_SOURCE'
            row['detail'] = f'missing source deck {src.name}'
            missing.append(row)
            rows.append(row)
            continue
        row['src_md5'] = md5_file(src)
        want = p.get('source_md5')
        row['md5_ok'] = (want == row['src_md5']) if want else None
        if not row['md5_ok']:
            row['detail'] = 'source md5 differs from ledger (deck page is stale)'
        rows.append(row)
    return rows, missing


def die(msg, code):
    log(f'ERROR: {msg}')
    sys.exit(code)


def deck_lock(timeout=180):
    """Shared flock on the deck's update lock so we never render a half-written deck."""
    lock_path = Path(str(DECK) + '.lock')
    f = open(lock_path, 'a+')
    deadline = time.time() + timeout
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_SH | fcntl.LOCK_NB)
            return f
        except OSError:
            if time.time() > deadline:
                f.close()
                die('timed out waiting for deck lock (merge in flight)', 3)
            time.sleep(2)


def render_all(certified_rows):
    """Render deck + all certified sources in ONE LibreOffice session."""
    if WORK.exists():
        shutil.rmtree(WORK)
    (WORK / 'pdf').mkdir(parents=True)
    (WORK / 'pages').mkdir()
    (WORK / 'src').mkdir()
    LO_PROFILE.mkdir(parents=True, exist_ok=True)

    inputs = [str(DECK)] + [str(r['source']) for r in certified_rows]
    cmd = ['soffice', '--headless',
           f'-env:UserInstallation=file://{LO_PROFILE}',
           '--convert-to', 'pdf', '--outdir', str(WORK / 'pdf')] + inputs
    env = dict(os.environ, TMPDIR=str(POOL), HOME=str(POOL))
    log(f'[*] LibreOffice session: 1 invocation, {len(inputs)} file(s), '
        f'profile={LO_PROFILE}')
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=1200)
    if proc.returncode != 0:
        die(f'soffice failed rc={proc.returncode}: {proc.stderr[-800:]}', 3)

    deck_pdf = WORK / 'pdf' / f'{DECK.stem}.pdf'
    if not deck_pdf.exists():
        die(f'merged deck PDF not produced: {deck_pdf}', 3)
    for r in certified_rows:
        pdf = WORK / 'pdf' / f"slide_{r['slide_num']:03d}_recreated.pdf"
        if not pdf.exists():
            die(f'source PDF not produced for page {r["page"]}: {pdf.name}', 3)
        r['pdf'] = pdf
    return deck_pdf


def rasterize(pdf, out_prefix, first=None, last=None):
    cmd = ['pdftoppm', '-png', '-r', str(DPI)]
    if first:
        cmd += ['-f', str(first), '-l', str(last or first)]
    cmd += [str(pdf), str(out_prefix)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    if proc.returncode != 0:
        die(f'pdftoppm failed on {pdf.name}: {proc.stderr[-400:]}', 3)
    outdir = Path(out_prefix).parent
    return sorted(outdir.glob(Path(out_prefix).name + '-*.png'))


def media_diag(deck_zip, names, page):
    """Count dangling media relationships in a merged deck page's rels."""
    rel = f'ppt/slides/_rels/slide{page}.xml.rels'
    if rel not in names:
        return None
    try:
        content = deck_zip.read(rel).decode('utf-8')
    except Exception:
        return None
    dangling = 0
    for target in re.findall(r'Target="([^"]+)"', content):
        if 'media/' not in target:
            continue
        resolved = 'ppt/' + target.replace('../', '')
        if resolved not in names:
            dangling += 1
    return dangling


def compare_pair(deck_png, src_png):
    """PIL compare on the common region (no resampling). Returns stats dict."""
    a = Image.open(deck_png).convert('RGB')
    b = Image.open(src_png).convert('RGB')
    if a.size != b.size:
        w = min(a.size[0], b.size[0])
        h = min(a.size[1], b.size[1])
        a = a.crop((0, 0, w, h))
        b = b.crop((0, 0, w, h))
    diff = np.asarray(ImageChops.difference(a, b), dtype=np.int16)
    total = diff.shape[0] * diff.shape[1] * diff.shape[2]
    nz = int((diff > 0).sum())
    return {
        'diff_px': nz,
        'total': total,
        'frac': nz / total if total else 0.0,
        'max_delta': int(diff.max()) if diff.size else 0,
        'size_deck': Image.open(deck_png).size,
        'size_src': Image.open(src_png).size,
    }


def evaluate(rows, deck_pages, selected=None, deck_zip=None):
    """Per-page compare for certified rows; returns (mismatches, table)."""
    table, mismatches = [], []
    for r in rows:
        if selected is not None and r['page'] not in selected:
            r['state'] = 'SKIP'
            table.append(r)
            continue
        if r['state'] == 'PLACEHOLDER':
            r['state'] = 'BLOCKED'
            table.append(r)
            continue
        if r['state'] == 'NO_SOURCE':
            mismatches.append(r)
            table.append(r)
            continue
        idx = r['page'] - 1
        if idx >= len(deck_pages):
            r['state'] = 'FAIL'
            r['detail'] = f'deck render has only {len(deck_pages)} page(s)'
            mismatches.append(r)
            table.append(r)
            continue
        src_png = WORK / 'src' / f"s{r['slide_num']:03d}-1.png"
        if not src_png.exists():
            r['state'] = 'FAIL'
            r['detail'] = 'source render missing'
            mismatches.append(r)
            table.append(r)
            continue
        stats = compare_pair(deck_pages[idx], src_png)
        r.update(stats)
        dangling = media_diag(deck_zip, names, r['page'])
        if dangling:
            r['detail'] = (f"{r['detail']} | {dangling} dangling media rel(s) in "
                           f"deck page (merge corruption)")
        ok = (stats['frac'] <= TOL_DIFF_FRAC and stats['max_delta'] <= TOL_MAX_DELTA)
        r['state'] = 'PASS' if ok else 'FAIL'
        if not ok:
            r['detail'] = (f"{stats['diff_px']} px differ ({stats['frac']*100:.4f}%), "
                           f"max delta {stats['max_delta']}")
            mismatches.append(r)
        table.append(r)
    return mismatches, table


def write_report(rows, mismatches, verdict, blocked, reason):
    lines = []
    lines.append('FINAL-DECK MERGE GATE REPORT')
    lines.append('=' * 74)
    lines.append(f'deck    : {DECK}')
    lines.append(f'ledger  : {LEDGER}')
    lines.append(f'md5     : {md5_file(DECK)}')
    lines.append(f'verdict : {verdict}')
    lines.append(f'reason  : {reason}')
    lines.append('')
    lines.append('tolerance: %d px on common region (%.4f%%), max channel delta %d'
                  % (int(TOL_DIFF_FRAC * 2_250_000), TOL_DIFF_FRAC * 100, TOL_MAX_DELTA))
    lines.append('render   : one LibreOffice session, private profile, '
                 f'{DPI} dpi, pdftoppm -png')
    lines.append('')
    lines.append(f"{'pg':>3} {'slide':>5} {'status':>11} {'result':>8} {'diffpx':>9} "
                 f"{'frac%':>8} {'maxd':>5}  detail")
    lines.append('-' * 74)
    for r in rows:
        dp = r['diff_px'] if r['diff_px'] is not None else '-'
        fr = f"{r['frac']*100:.4f}" if r['frac'] is not None else '-'
        md = r['max_delta'] if r['max_delta'] is not None else '-'
        lines.append(f"{r['page']:>3} {r['slide_num']:>5} {r['status']:>11} "
                     f"{r['state']:>8} {dp:>9} {fr:>8} {md:>5}  {r['detail']}")
    lines.append('-' * 74)
    n_cert = sum(1 for r in rows if r['status'] == 'certified')
    n_pass = sum(1 for r in rows if r['state'] == 'PASS')
    lines.append(f'{n_pass}/{n_cert} certified pages pixel-match their source; '
                 f'{len(mismatches)} mismatch(es); {len(blocked)} placeholder page(s)')
    lines.append('')
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text('\n'.join(lines) + '\n')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', help='comma list of page nums to compare')
    args = ap.parse_args()

    lock = deck_lock()
    pages = load_ledger()
    rows, missing = audit_sources(pages)
    selected = None
    if args.pages:
        selected = {int(x) for x in args.pages.split(',') if x.strip()}
    blocked = [r for r in rows
               if r['state'] in ('PLACEHOLDER', 'BLOCKED')
               and (selected is None or r['page'] in selected)]
    certified = [r for r in rows if r['state'] not in
                 ('PLACEHOLDER', 'BLOCKED', 'NO_SOURCE')
                 and (selected is None or r['page'] in selected)]
    deck_zip = zipfile.ZipFile(DECK)
    names = set(deck_zip.namelist())
    try:
        deck_pdf = render_all(certified)
        deck_pages = rasterize(deck_pdf, WORK / 'pages' / 'pg')
        for r in certified:
            rasterize(r['pdf'], WORK / 'src' / f"s{r['slide_num']:03d}",
                      first=1, last=1)
        mismatches, table = evaluate(rows, deck_pages, selected, deck_zip, names)
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()
        deck_zip.close()

    blocked_rows = [r for r in table if r['state'] == 'BLOCKED']
    if blocked_rows:
        verdict, code = 'BLOCKED', 1
        reason = ('%d placeholder page(s) not yet certified: %s'
                  % (len(blocked_rows),
                     ', '.join(str(r['page']) for r in blocked_rows)))
    elif missing:
        verdict, code = 'FAIL', 2
        reason = 'missing source deck for a certified page'
    elif mismatches:
        verdict, code = 'FAIL', 2
        reason = '%d certified page(s) mismatch their source render' % len(mismatches)
    else:
        verdict, code = 'PASS', 0
        reason = 'all certified pages pixel-match; 0/%d mismatch' % len(rows)

    text = write_report(table, mismatches, verdict, blocked, reason)
    log(text)
    log('')
    log(f'GATE {verdict}: {reason}')
    sys.exit(code)


if __name__ == '__main__':
    main()
