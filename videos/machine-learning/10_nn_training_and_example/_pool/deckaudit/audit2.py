#!/usr/bin/env python3
"""Deck audit v2 — corrected slide association, chain resolution, chrome check."""
import os, re, json, hashlib, zipfile, sqlite3, datetime
import xml.etree.ElementTree as ET

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example'
os.chdir(NS)
EMU = 914400.0
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
MD5_RE = re.compile(r'\b([0-9a-f]{32})\b')
PROV = ('render_meta', 'render_check', 'pil_check', 'closed_loop', 'measurement',
        'adjudication', 'report', 'certif', 'deckcheck', 'rejudge_report')
SLIDE_RE = re.compile(r'slide[_-]?(\d{1,3})', re.I)
SNAP = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def md5(p):
    try:
        h = hashlib.md5()
        with open(p, 'rb') as f:
            for c in iter(lambda: f.read(1 << 20), b''):
                h.update(c)
        return h.hexdigest()
    except OSError:
        return None


def read(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        return ''


def slide_of(s):
    m = SLIDE_RE.search(s or '')
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 34 else None


def prov_md5s(d, up=3):
    """md5 -> provenance file, searching curated evidence files up the tree."""
    att = {}
    base = os.path.abspath(d or '.')
    for _ in range(up + 1):
        if not os.path.isdir(base):
            break
        try:
            names = sorted(os.listdir(base))
        except OSError:
            break
        for fn in names:
            p = os.path.join(base, fn)
            low = fn.lower()
            if not os.path.isfile(p) or not low.endswith(('.txt', '.md')):
                continue
            if any(k in low for k in PROV):
                for m in MD5_RE.finditer(read(p)):
                    att.setdefault(m.group(1), os.path.relpath(p, NS))
        base = os.path.dirname(base)
    return att


def verdict_of(text):
    """Strict terminal-verdict parse -> (PASS|FAIL|None, verdict_line)."""
    lines = [l.rstrip() for l in text.splitlines()]
    hits = []
    for l in lines:
        if 'FINAL' not in l.upper() or 'VERDICT' not in l.upper():
            continue
        m = re.search(r'FINAL\s+VERDICT\s*:\s*\**\s*(PASS|FAIL)\b', l, re.I)
        if m:
            hits.append((m.group(1).upper(), l.strip()[:110]))
        elif re.search(r'\bno\s+FINAL\s+VERDICT|FINAL\s+VERDICT\s+(?:is\s+)?(?:missing|absent|not\s+present)',
                       l, re.I):
            hits.append((None, l.strip()[:110]))
    if not hits:
        return None, 'no terminal FINAL VERDICT line'
    return hits[-1]


def transcripts():
    out = {}
    for root, dirs, files in os.walk(NS):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', '__pycache__', 'deckaudit')]
        for fn in files:
            if not fn.endswith('.txt'):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, NS)
            if any(k in rel for k in ('judge_prompt', 'judge_template', 'audit_prompt')):
                continue
            t = read(p)
            if 'FINAL VERDICT' not in t.upper():
                continue
            v, vline = verdict_of(t)
            imgs = re.findall(r'^===\s*(.+?)\s*===\s*$', t, re.M)
            first = imgs[0].split(',')[0].strip() if imgs else ''
            n = slide_of(rel) or slide_of(first)
            if not n:
                continue
            out.setdefault(n, []).append({'rel': rel, 'verdict': v, 'vline': vline,
                                          'render': first, 'mtime': os.path.getmtime(p)})
    return out


def chrome_violations(pptx, n):
    v = []
    try:
        z = zipfile.ZipFile(pptx)
        names = sorted([x for x in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', x)],
                       key=lambda s: int(re.search(r'(\d+)', s.split('/')[-1]).group(1)))
        root = ET.fromstring(z.read(names[0]))
    except Exception as e:
        return ['open/parse failed: %s: %s' % (type(e).__name__, e)]
    FR = (0.15, 0.15, 13.03, 7.2)
    BD = (12.48, 0.30, 0.5, 0.5)
    frame_ok = badge_geo = False
    badge_fill = set()
    numeral = None
    title_ok = False
    badge_circles = []
    for sp in root.iter():
        if sp.tag not in (P + 'sp', P + 'pic'):
            continue
        xfrm = sp.find('.//' + A + 'xfrm')
        if xfrm is None:
            continue
        off, ext = xfrm.find(A + 'off'), xfrm.find(A + 'ext')
        if off is None or ext is None:
            continue
        try:
            g = (float(off.get('x')) / EMU, float(off.get('y')) / EMU,
                 float(ext.get('cx')) / EMU, float(ext.get('cy')) / EMU)
        except (TypeError, ValueError):
            continue
        kind = next((gg.get('prst') for gg in sp.iter(A + 'prstGeom') if gg.get('prst')), None)
        cols = {c.get('val').upper() for c in sp.iter(A + 'srgbClr') if c.get('val')}
        lnz = {c.get('val').upper() for c in (sp.find('.//' + A + 'ln').iter(A + 'srgbClr')
                                              if sp.find('.//' + A + 'ln') is not None else [])
               if c.get('val')}
        txt = ''.join(t.text or '' for t in sp.iter(A + 't')).strip()
        # house frame: rect, red line, exact geometry
        if kind == 'rect' and 'C00000' in lnz and all(abs(g[i] - FR[i]) < 0.06 for i in range(4)):
            frame_ok = True
        # badge geometry (any shape at badge position)
        if all(abs(g[i] - BD[i]) < 0.06 for i in range(4)):
            badge_circles.append((kind, cols, txt))
            if len(badge_circles) == 1:
                badge_geo = True
        # badge ellipse fill
        if kind == 'ellipse' and all(abs(g[i] - BD[i]) < 0.06 for i in range(4)):
            badge_fill = cols
            # numeral may live in the ellipse itself
        if txt and all(abs(g[i] - BD[i]) < 0.06 for i in range(4)):
            numeral = txt
        # title box: text shape at x=0.6, y=0.28
        if txt and abs(g[0] - 0.6) < 0.06 and abs(g[1] - 0.28) < 0.06:
            title_ok = True
    if not frame_ok:
        v.append('outer red frame at (0.15,0.15,13.03,7.2) with C00000 line NOT FOUND')
    if not badge_geo:
        v.append('badge shape at (12.48,0.30,0.5,0.5) NOT FOUND')
    if badge_fill and 'FFF9C4' not in badge_fill:
        v.append('badge fill %s != FFF9C4' % sorted(badge_fill))
    if numeral != str(n):
        v.append('badge numeral %r != %d' % (numeral, n))
    if not title_ok:
        v.append('no title text box at x=0.6 y=0.28')
    return v


def orphan_pptx():
    out = []
    for root, dirs, files in os.walk(NS):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', '__pycache__')]
        for fn in files:
            if not fn.endswith('.pptx') or SLIDE_RE.search(fn) is None:
                continue
            p = os.path.join(root, fn)
            if os.path.basename(p) == os.path.basename(
                    os.path.join('recreated_pptx', 'slide_%03d_recreated.pptx' % slide_of(fn))):
                if os.path.relpath(p, NS) == os.path.join(
                        'recreated_pptx', 'slide_%03d_recreated.pptx' % slide_of(fn)):
                    continue
            out.append({'path': os.path.relpath(p, NS), 'slide': slide_of(fn),
                        'md5': md5(p), 'size': os.path.getsize(p)})
    return sorted(out, key=lambda d: (d['slide'] or 0, d['path']))


def classify(n, e, tx):
    pptx = os.path.join('recreated_pptx', 'slide_%03d_recreated.pptx' % n)
    if not os.path.isfile(pptx):
        return 'MISSING', 'no recreated_pptx/slide_%03d_recreated.pptx' % n
    cur = md5(pptx)
    recs = []
    for r in tx:
        rec = dict(r)
        rp = r['render'] if (r['render'] and os.path.isabs(r['render'])
                             and os.path.isfile(r['render'])) else os.path.join(NS, r['render'])
        if os.path.isfile(rp):
            att = prov_md5s(os.path.dirname(rp))
            if cur in att:
                rec['chain'], rec['src'] = 'OK', att[cur]
            else:
                others = sorted(k[:8] for k in att if k != cur)
                rec['chain'] = 'STALE' if att else 'UNVERIFIED'
                rec['src'] = ('md5s attested near judged render: %s (current %s not among them)'
                              % (', '.join(others), cur[:8])) if att else \
                             ('no md5 attestation near judged render %s' % os.path.relpath(rp, NS))
        else:
            rec['chain'], rec['src'] = 'NO-RENDER', 'judged render file missing'
        recs.append(rec)
    e['cur_md5'] = cur
    pass_ok = [r for r in recs if r['verdict'] == 'PASS' and r['chain'] == 'OK']
    pass_any = [r for r in recs if r['verdict'] == 'PASS']
    fail_ok = [r for r in recs if r['verdict'] == 'FAIL' and r['chain'] == 'OK']
    fail_any = [r for r in recs if r['verdict'] == 'FAIL']
    e['pass_tx'] = [{'path': r['rel'], 'render': os.path.relpath(rp, NS), 'chain': r['chain'],
                     'src': r['src']} for r in pass_any]
    e['fail_tx'] = [{'path': r['rel'], 'chain': r['chain']} for r in fail_any]
    if pass_ok:
        best = max(pass_ok, key=lambda r: r['mtime'])
        return 'CERTIFIED-SOUND', 'PASS %s bound to current md5 via %s' % (best['rel'], best['src'])
    if fail_ok:
        best = max(fail_ok, key=lambda r: r['mtime'])
        return 'FAIL', 'chain-verified FAIL on current bytes: %s (%s)' % (best['rel'], best['src'])
    if pass_any:
        best = max(pass_any, key=lambda r: r['mtime'])
        return 'CERTIFIED-UNVERIFIED', 'PASS %s exists but chain=%s (%s)' % (
            best['rel'], best['chain'], best['src'])
    if fail_any:
        best = max(fail_any, key=lambda r: r['mtime'])
        return 'FAIL', 'only FAIL verdicts, newest %s (chain=%s)' % (best['rel'], best['chain'])
    return 'NO-VERDICT', 'no transcript with a terminal FINAL VERDICT line'


def main():
    tx = transcripts()
    led = json.load(open(os.path.join(NS, 'final_deck_ledger.json')))['pages']
    L = {p['slide_num']: p for p in led}
    db = sqlite3.connect(os.path.join(NS, 'slides_progress.db'))
    D = {r[0]: {'gen': r[1], 'vis': r[2], 'vt': r[3], 'err': r[4]}
         for r in db.execute('SELECT slide_id,gen_status,visual_check,visual_transcript,last_error FROM slides')}
    orphan = orphan_pptx()
    zf = zipfile.ZipFile(os.path.join(NS, '10_nn_training_and_example_final.pptx'))
    deck = {'final_md5': md5('10_nn_training_and_example_final.pptx'),
            'final_slides': len([x for x in zf.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', x)]),
            'final_zip_ok': zf.testzip() is None}
    out = {}
    for n in range(1, 35):
        pptx = os.path.join('recreated_pptx', 'slide_%03d_recreated.pptx' % n)
        e = {'pptx': os.path.isfile(pptx), 'size': None, 'md5': None, 'zip_ok': None,
             'slide_xml': None, 'has_presentation': None, 'chrome': [], 'class': None,
             'why': None, 'pass_tx': [], 'fail_tx': [], 'cur_md5': None}
        if e['pptx']:
            e['size'] = os.path.getsize(pptx)
            e['md5'] = md5(pptx)
            try:
                z = zipfile.ZipFile(pptx)
                e['zip_ok'] = z.testzip() is None
                e['slide_xml'] = len([x for x in z.namelist()
                                      if re.match(r'ppt/slides/slide\d+\.xml$', x)])
                e['has_presentation'] = 'ppt/presentation.xml' in z.namelist()
                if e['zip_ok'] and e['has_presentation']:
                    e['chrome'] = chrome_violations(pptx, n)
            except Exception as ex:
                e['zip_ok'] = False
                e['chrome'] = ['pptx unreadable: %s' % type(ex).__name__]
        cls, why = classify(n, e, tx.get(n, []))
        e['class'], e['why'] = cls, why
        e['ledger_status'] = L[n]['status'] if n in L else 'ABSENT'
        e['ledger_md5'] = L[n]['source_md5'] if n in L else None
        e['ledger_mismatch'] = bool(e['ledger_status'] == 'certified'
                                    and (e['md5'] is None or e['md5'] != e['ledger_md5']))
        e['db_gen'] = D[n]['gen'] if n in D else 'NO-ROW'
        e['db_vis'] = D[n]['vis'] if n in D else None
        e['db_vt'] = D[n]['vt'] if n in D else None
        e['orphans'] = [o['path'] for o in orphan if o['slide'] == n]
        out[str(n)] = e
    json.dump({'snapshot': SNAP, 'slides': out, 'orphans': orphan, 'deck': deck},
              open(os.path.join(NS, '_pool/deckaudit/consistency.json'), 'w'), indent=1)
    for n in range(1, 35):
        e = out[str(n)]
        print('%03d %-21s pptx=%s md5=%s led=%-11s db=%-9s vis=%-5s chrome=%d' % (
            n, e['class'], 'Y' if e['pptx'] else 'N', (e['md5'] or '-')[:8],
            e['ledger_status'], e['db_gen'], e['db_vis'] or '-', len(e['chrome'])))
    from collections import Counter
    print('COUNTS', dict(Counter(out[str(n)]['class'] for n in range(1, 35))))


main()
