#!/usr/bin/env python3
"""Deck consistency auditor - gateway-free (file + sqlite + PIL/XML only)."""
import os, re, json, glob, zipfile, hashlib, sqlite3, datetime

NS = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.chdir(NS)
EMU = 914400
NOW = datetime.datetime.now().isoformat(timespec='seconds')

MD5_RE = re.compile(r'\b([0-9a-f]{32})\b')
VERD_RE = re.compile(r'FINAL\s+VERDICT\s*:?\s*\**\s*(PASS|FAIL)\b', re.I)
NEG_RE = re.compile(r'\bno\s+FINAL\s+VERDICT|without\s+a\s+FINAL\s+VERDICT|'
                    r'FINAL\s+VERDICT\s*(?:line)?\s*(?:is\s+)?(?:missing|absent|not\s+present)', re.I)
IMG_LINE = re.compile(r'^===\s*(.+?)\s*===\s*$', re.M)
SLIDE_IN_PATH = re.compile(r'slide[_-]?0*(\d{1,2})', re.I)


def md5(path):
    try:
        h = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def slide_num_of(path):
    m = SLIDE_IN_PATH.search(path)
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 34 else None


def canonical_pptx(n):
    return os.path.join('recreated_pptx', 'slide_%03d_recreated.pptx' % n)


def read_text(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return ''


def terminal_verdict(text):
    """Strict parse: returns ('PASS'|'FAIL'|None, note)."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    hits = []
    for i, ln in enumerate(lines):
        if 'FINAL VERDICT' in ln.upper():
            m = VERD_RE.search(ln)
            if m:
                hits.append((i, m.group(1).upper(), ln))
            elif NEG_RE.search(ln):
                hits.append((i, None, ln))
    if not hits:
        return None, 'no FINAL VERDICT line'
    i, v, ln = hits[-1]
    if v is None:
        return None, 'verdict line negated: %s' % ln.strip()[:90]
    # hedge check: verdict token must directly follow the colon (not buried in prose)
    if not re.search(r'FINAL\s+VERDICT\s*:\s*\**\s*(PASS|FAIL)\b', ln, re.I):
        return None, 'hedge verdict line: %s' % ln.strip()[:90]
    tail = '\n'.join(lines[i + 1:]).strip()
    if tail and 'FINAL VERDICT' in tail.upper():
        return None, 'multiple/conflicting verdict lines'
    return v, ln.strip()[:120]


def find_transcripts():
    """All *.txt under the namespace mentioning FINAL VERDICT, keyed by slide num."""
    out = {}
    for root, dirs, files in os.walk(NS):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', '__pycache__')]
        for fn in files:
            if not fn.endswith('.txt'):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, NS)
            if 'deckaudit' in rel:
                continue
            txt = read_text(p)
            if 'FINAL' not in txt.upper() or 'VERDICT' not in txt.upper():
                continue
            if '/judge_template' in ('/' + rel) or rel.startswith('judge_template'):
                continue
            if 'audit_prompt' in rel or 'judge_prompt' in rel:
                continue
            v, vline = terminal_verdict(txt)
            imgs = IMG_LINE.findall(txt)
            first = imgs[0].split(',')[0].strip() if imgs else ''
            n = slide_num_of(first) or slide_num_of(rel)
            rec = {'path': rel, 'verdict': v, 'vline': vline,
                   'render': os.path.relpath(os.path.join(NS, first), NS) if os.path.isabs(first) or True else first,
                   'render_rel': first, 'mtime': os.path.getmtime(p)}
            if n:
                out.setdefault(n, []).append(rec)
    return out


def provenance_md5s(rel_dir):
    """Every md5 attested in prose/notes files inside this dir (bounded to md5-bearing lines)."""
    found = {}
    for fn in sorted(os.listdir(rel_dir or '.')):
        p = os.path.join(rel_dir, fn) if rel_dir else fn
        if not os.path.isfile(p) or not fn.endswith(('.txt', '.md')):
            continue
        for hit in MD5_RE.finditer(read_text(p)):
            found.setdefault(hit.group(1), p)
    return found


def chain_for(rec, cur_md5, pptx_md5s_by_slide):
    """Does the transcript's judged render reach the current deliverable bytes?"""
    render = rec['render_rel']
    rdir = os.path.dirname(render) if render else ''
    if not os.path.isfile(os.path.join(NS, render)):
        return 'NO-RENDER-FILE', 'judged render path missing'
    att = provenance_md5s(rdir)
    render_md5 = md5(os.path.join(NS, render))
    # a pptx sitting in the same dir as the judged render, byte-identical to the deliverable
    for p in sorted(glob.glob(os.path.join(rdir, '*.pptx'))) if rdir else []:
        if md5(p) == cur_md5:
            return 'OK', '%s md5==current deliverable' % os.path.relpath(p, NS)
    # the md5 the render was produced from, attested next to it
    if cur_md5 and cur_md5 in att:
        return 'OK', '%s attests src md5==current' % att[cur_md5]
    # same render file re-judged beside a pptx of identical bytes
    twins = [p for p in pptx_md5s_by_slide if md5(p) == cur_md5]
    if att and twins:
        only = set(att) - {cur_md5}
        return 'STALE', 'render dir attests md5s %s, none == current (%s); current bytes copied to %s' % (
            sorted(only), cur_md5[:8], [os.path.relpath(t, NS) for t in twins])
    if att:
        return 'STALE', 'render dir attests %s, none == current' % sorted(set(att))
    if twins:
        return 'UNVERIFIED', 'no md5 attestation beside judged render; deliverable bytes also at %s' % [
            os.path.relpath(t, NS) for t in twins]
    return 'UNVERIFIED', 'no md5 attestation beside judged render'


import xml.etree.ElementTree as ET
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
FRAME = (0.15, 0.15, 13.03, 7.2)
BADGE = (12.48, 0.30, 0.5, 0.5)
TOL = 27432  # 0.03 in in EMU


def inch(v):
    return round(float(v) / EMU, 4)


def shape_geom(sp):
    xfrm = sp.find('.//' + A + 'xfrm')
    if xfrm is None:
        return None
    off = xfrm.find(A + 'off')
    ext = xfrm.find(A + 'ext')
    if off is None or ext is None:
        return None
    try:
        return (int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy')))
    except (TypeError, ValueError):
        return None


def colors(sp):
    out = set()
    for c in sp.iter(A + 'srgbClr'):
        if c.get('val'):
            out.add(c.get('val').upper())
    return out


def geom_kind(sp):
    for g in sp.iter(A + 'prstGeom'):
        if g.get('prst'):
            return g.get('prst')
    for g in sp.iter(A + 'custGeom'):
        return 'custGeom'
    return None


def text_of(sp):
    return ''.join(t.text or '' for t in sp.iter(A + 't')).strip()


def chrome_check(pptx, n):
    """Static house-chrome check on the canonical pptx XML. Returns list of violations."""
    v = []
    try:
        with zipfile.ZipFile(pptx) as z:
            names = [x for x in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', x)]
            if not names:
                return ['no ppt/slides/slideN.xml found']
            names.sort(key=lambda s: int(re.search(r'(\d+)', s.split('/')[-1]).group(1)))
            for name in names:
                root = ET.fromstring(z.read(name))
                shapes = [e for e in root.iter() if e.tag in (P + 'sp', P + 'pic', P + 'graphicFrame')]
                frames, badges, titles = [], [], []
                for sp in shapes:
                    g = shape_geom(sp)
                    if not g:
                        continue
                    k = geom_kind(sp)
                    cs = colors(sp)
                    txt = text_of(sp)
                    if k == 'rect' and 'C00000' in cs and g[2] > int(12 * EMU):
                        frames.append((g, cs))
                    if k == 'ellipse' and abs(g[0] - BADGE[0] * EMU) < TOL and abs(g[1] - BADGE[1] * EMU) < TOL:
                        badges.append((g, cs, txt))
                    if txt and k in (None, 'rect') and abs(g[0] - 0.6 * EMU) < TOL:
                        titles.append((g, txt))
                if not frames:
                    v.append('%s: outer red frame (C00000, x=0.15 y=0.15 w=13.03 h=7.2) NOT FOUND' % name)
                else:
                    g = frames[0][0]
                    got = (inch(g[0]), inch(g[1]), inch(g[2]), inch(g[3]))
                    if any(abs(got[i] - FRAME[i]) > 0.03 for i in range(4)):
                        v.append('%s: frame geometry %s != %s' % (name, got, FRAME))
                if not badges:
                    v.append('%s: yellow badge ellipse (x=12.48 y=0.30 w=0.5 h=0.5) NOT FOUND' % name)
                else:
                    g, cs, txt = badges[0]
                    got = (inch(g[0]), inch(g[1]), inch(g[2]), inch(g[3]))
                    if any(abs(got[i] - BADGE[i]) > 0.03 for i in range(4)):
                        v.append('%s: badge geometry %s != %s' % (name, got, BADGE))
                    if 'FFF9C4' not in cs:
                        v.append('%s: badge fill %s lacks FFF9C4' % (name, sorted(cs)))
                    if txt != str(n):
                        v.append('%s: badge text %r != printed number %d' % (name, txt, n))
                if not titles:
                    v.append('%s: title text box (x=0.6 y=0.28) NOT FOUND' % name)
                else:
                    g = titles[0][0]
                    if abs(inch(g[1]) - 0.28) > 0.05:
                        v.append('%s: title y=%.3f != 0.28' % (name, inch(g[1])))
    except (zipfile.BadZipFile, ET.ParseError, OSError) as e:
        v.append('XML inspect failed: %s' % e)
    return v


def orphan_scan():
    """Stray parallel deliverables (non-canonical pptx names) for slides that are canonical."""
    found = []
    for root, dirs, files in os.walk(NS):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', '__pycache__')]
        for fn in files:
            if not fn.endswith('.pptx'):
                continue
            p = os.path.join(root, fn)
            m = re.match(r'^slide_(\d{3})_recreated\.pptx$', fn)
            if m:
                continue
            mm = re.search(r'slide[_-]?0*(\d{1,2})', p)
            n = int(mm.group(1)) if mm else None
            if n and 1 <= n <= 34:
                found.append({'slide': n, 'path': os.path.relpath(p, NS),
                              'md5': md5(p), 'size': os.path.getsize(p)})
    return sorted(found, key=lambda d: (d['slide'], d['path']))
