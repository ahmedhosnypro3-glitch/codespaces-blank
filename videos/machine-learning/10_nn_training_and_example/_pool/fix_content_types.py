#!/usr/bin/env python3
"""One-time OPC repair for 10_nn_training_and_example_final.pptx:
adds missing Default content-types for media extensions (png measured missing)
and drops unreferenced zero-length media entries. All other parts byte-identical.
Usage: python3 _pool/fix_content_types.py <deck.pptx>
"""
import sys, os, zipfile, shutil, tempfile, fcntl, re
from contextlib import contextmanager
from pathlib import Path

EXT_CT = {
    'png': 'image/png', 'jpeg': 'image/jpeg', 'jpg': 'image/jpeg',
    'gif': 'image/gif', 'emf': 'image/x-emf', 'wmf': 'image/x-wmf',
    'bin': 'application/vnd.openxmlformats-officedocument.presentationml.printerSettings',
    'rels': 'application/vnd.openxmlformats-package.relationships+xml',
    'xml': 'application/xml',
}

@contextmanager
def deck_lock(out_path):
    lock_path = Path(str(out_path) + '.lock')
    lf = open(lock_path, 'w')
    try:
        fcntl.flock(lf, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()

def main(deck):
    out = Path(deck)
    with deck_lock(out):
        with zipfile.ZipFile(out, 'r') as z:
            infos = z.infolist()
            blobs = {i.filename: z.read(i.filename) for i in infos}
            ct = blobs['[Content_Types].xml'].decode('utf-8')
            # all relationship targets across the package
            targets = set()
            for name, blob in blobs.items():
                if name.endswith('.rels'):
                    for t in re.findall(r'Target="([^"]+)"', blob.decode('utf-8')):
                        t = t.lstrip('/')
                        if not t.startswith('http') and 'TargetMode' not in t:
                            base = os.path.dirname(name.replace('/_rels/', '/').replace('.rels', ''))
                            p = os.path.normpath(os.path.join(base, t)) if not t.startswith('..') is False else os.path.normpath(os.path.join(base, t))
                            targets.add(p)
            # media extension inventory
            media_exts = set()
            for name in blobs:
                if '/media/' in name:
                    ext = name.rsplit('.', 1)[-1].lower() if '.' in os.path.basename(name) else ''
                    if ext:
                        media_exts.add(ext)
            has = set(re.findall(r'Extension="([^"]+)"', ct))
            need = sorted(media_exts - has)
            # unreferenced zero-length parts (junk from earlier merges)
            drop = [i.filename for i in infos
                    if i.file_size == 0 and '/media/' in i.filename and i.filename not in targets]
        if not need and not drop:
            print('nothing to repair')
            return
        adds = ''.join(f'<Default Extension="{e}" ContentType="{EXT_CT[e]}"/>' for e in need)
        if adds:
            ct = ct.replace('</Types>', adds + '</Types>')
        fd, tmp = tempfile.mkstemp(suffix='.pptx', dir=str(out.parent), prefix=out.stem + '_repair_')
        os.close(fd)
        try:
            with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as nz:
                for i in infos:
                    if i.filename in drop or i.filename == '[Content_Types].xml':
                        continue
                    nz.writestr(i, blobs[i.filename])
                nz.writestr('[Content_Types].xml', ct.encode('utf-8'))
            with zipfile.ZipFile(out) as z:
                del z
            shutil.move(tmp, str(out))
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        print(f'repaired: added defaults {need}; dropped {len(drop)} unreferenced zero-length parts: {drop}')

if __name__ == '__main__':
    main(sys.argv[1])
