#!/usr/bin/env python3
"""Safe single-page merge into the final deck (replaces merge_final_deck.py
mode_update, which drops all media and leaves dangling rels).

Keeps every other package part byte-for-byte, renames the merged page's media
and rewrites its rels so they resolve, drops the notesSlide rel (the deck
carries no notesSlides), adds a png content-type default when missing, and
updates final_deck_ledger.json source_md5. Uses the same flock as the stock
script so concurrent merges cannot interleave.

Usage: python3 merge_page_safe.py <deck.pptx> <page> <certified_slide.pptx>
"""
import fcntl, hashlib, json, os, re, shutil, sys, tempfile, zipfile
from pathlib import Path

deck, page, src = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
ledger_path = deck.with_name('final_deck_ledger.json')
lock = open(str(deck) + '.lock', 'w')
fcntl.flock(lock, fcntl.LOCK_EX)
try:
    backup_dir = deck.parent / '_pool' / 'deck_backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f'final_deck_pre_page{page}_merge.pptx'
    if not backup.exists():
        shutil.copy2(deck, backup)
    zsrc = zipfile.ZipFile(src)
    zdeck = zipfile.ZipFile(deck)
    media = {n: f'ppt/media/page{page}_{Path(n).name}'
             for n in zsrc.namelist()
             if n.startswith('ppt/media/') and not n.endswith('/')}
    rels = zsrc.read('ppt/slides/_rels/slide1.xml.rels').decode('utf-8')
    rels = re.sub(r'Target="\.\./media/([^"]+)"',
                  lambda m: f'Target="../media/page{page}_{m.group(1)}"', rels)
    rels = re.sub(r'<Relationship\b[^>]*Type="[^"]*/notesSlide"[^>]*/>', '', rels)
    slide_xml = zsrc.read('ppt/slides/slide1.xml')
    ct = zdeck.read('[Content_Types].xml').decode('utf-8')
    if 'Extension="png"' not in ct:
        ct = re.sub(r'(<Types[^>]*>)',
                    r'\1<Default Extension="png" ContentType="image/png"/>',
                    ct, count=1)
    fd, tmp_name = tempfile.mkstemp(suffix='.pptx', dir=str(deck.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            for item in zdeck.infolist():
                name = item.filename
                if name in (f'ppt/slides/slide{page}.xml',
                            f'ppt/slides/_rels/slide{page}.xml.rels'):
                    continue
                if name == '[Content_Types].xml':
                    z.writestr(name, ct)
                    continue
                z.writestr(item, zdeck.read(name))
            z.writestr(f'ppt/slides/slide{page}.xml', slide_xml)
            z.writestr(f'ppt/slides/_rels/slide{page}.xml.rels', rels)
            for orig, new in media.items():
                z.writestr(new, zsrc.read(orig))
        shutil.move(str(tmp), str(deck))
    finally:
        if tmp.exists():
            tmp.unlink()
    source_md5 = hashlib.md5(src.read_bytes()).hexdigest()
    ledger = json.loads(ledger_path.read_text())
    for p in ledger['pages']:
        if p['page'] == page:
            p['status'] = 'certified'
            p['source_md5'] = source_md5
            break
    ledger_path.write_text(json.dumps(ledger, indent=2))
    print(f'page {page} merged from {src} source_md5={source_md5}')
    print(f'pre-merge backup: {backup}')
finally:
    fcntl.flock(lock, fcntl.LOCK_UN)
    lock.close()
