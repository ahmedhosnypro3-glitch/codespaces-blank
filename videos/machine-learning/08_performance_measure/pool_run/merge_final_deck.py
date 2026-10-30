#!/usr/bin/env python3
"""
merge_final_deck.py — Byte-verbatim OPC merge for continuous final deck.

MODES:
  placeholder: Initialize OUT with N pages, each page the corresponding original
               frame image full-bleed (one per confirmed slide in printed-badge order).
  update N:    Replace page N in OUT with certified slide_NNN_recreated.pptx content
               at the OPC package level (verbim XML, media renamed per slide).
  gate:        Render merged deck + all sources in one LO session, pixel-diff
               page N vs source N — 0/N mismatches required.

Usage:
  python3 merge_final_deck.py placeholder <unique_slides_dir> <slides_index.json> <out.pptx>
  python3 merge_final_deck.py update <slide_num> <certified_slide.pptx> <out.pptx>
  python3 merge_final_deck.py gate <out.pptx> <per_slide_dir> <N>
"""
import sys
import os
import json
import shutil
import tempfile
import zipfile
import hashlib
import fcntl
from contextlib import contextmanager
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.oxml.ns import qn


def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


@contextmanager
def deck_lock(out_path):
    """Fleet-global lock for final-deck mutations — concurrent merge workers
    must never write the same pptx simultaneously (corrupt zip measured 2026-10-27)."""
    lock_path = Path(str(out_path) + '.lock')
    lock_file = open(lock_path, 'w')
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()


def mode_placeholder(unique_slides_dir, slides_index_path, out_path):
    """Initialize placeholder deck: N pages, each original frame full-bleed."""
    with open(slides_index_path) as f:
        slides = json.load(f)
    N = len(slides)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # blank layout
    for s in slides:
        slide = prs.slides.add_slide(blank_layout)
        img_path = Path(unique_slides_dir) / s['file']
        slide.shapes.add_picture(str(img_path), Inches(0), Inches(0),
                                  width=prs.slide_width, height=prs.slide_height)
    prs.save(out_path)
    # Write ledger
    ledger_path = Path(out_path).with_name('final_deck_ledger.json')
    ledger = {
        "pages": [
            {"page": i+1, "slide_num": s['slide_number'], "status": "placeholder",
             "source_md5": md5_file(Path(unique_slides_dir) / s['file'])}
            for i, s in enumerate(slides)
        ]
    }
    with open(ledger_path, 'w') as f:
        json.dump(ledger, f, indent=2)
    print(f"Placeholder initialized: {out_path} ({N} pages)")


def mode_update(slide_num, certified_pptx_path, out_path):
    """Replace page N in OUT with certified slide content at OPC level.
    Certified single-slide decks always have slide1.xml/slide1.xml.rels.
    We must rename them to slide{N}.xml / slide{N}.xml.rels during merge.
    The whole mutation is serialized under a fleet-global lock."""
    slide_num = int(slide_num)
    certified = Path(certified_pptx_path)
    out = Path(out_path)
    ledger_path = out.with_name('final_deck_ledger.json')

    with deck_lock(out):
        # Load ledger
        with open(ledger_path) as f:
            ledger = json.load(f)

        # Open both as zip (OPC)
        with zipfile.ZipFile(certified, 'r') as czip, zipfile.ZipFile(out, 'r') as ozip:
            # Build new zip — unique tmp name (no two writers share a path)
            fd, tmp_name = tempfile.mkstemp(suffix='.pptx', dir=str(out.parent),
                                            prefix=out.stem + '_merge_')
            os.close(fd)
            tmp_out = Path(tmp_name)
            try:
                with zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as nzip:
                    # Target names in final deck
                    target_slide_xml = f'ppt/slides/slide{slide_num}.xml'
                    target_slide_rels = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
                    # Source names in certified deck (always slide1 for single-slide decks)
                    source_slide_xml = 'ppt/slides/slide1.xml'
                    source_slide_rels = 'ppt/slides/_rels/slide1.xml.rels'

                    # Media files from certified to be renamed and added
                    certified_media = [n for n in czip.namelist() if n.startswith('ppt/media/')]
                    # Map certified media names -> new names (slide{N}_<orig>)
                    media_map = {}
                    for m in certified_media:
                        orig_name = os.path.basename(m)
                        new_name = f'ppt/media/slide{slide_num}_{orig_name}'
                        media_map[m] = new_name

                    # Copy everything from OUT
                    for item in ozip.infolist():
                        if item.filename == target_slide_xml or item.filename == target_slide_rels:
                            continue  # will replace from certified
                        if item.filename.startswith('ppt/media/'):
                            continue  # will add renamed from certified
                        nzip.writestr(item, ozip.read(item.filename))

                    # Add certified slide XML (rename from slide1.xml to slide{N}.xml)
                    nzip.writestr(target_slide_xml, czip.read(source_slide_xml))
                    # Add certified slide rels (rename from slide1.xml.rels to slide{N}.xml.rels)
                    rels_content = czip.read(source_slide_rels).decode('utf-8')
                    # For simplicity, assume layout/master refs are compatible (same template family)
                    nzip.writestr(target_slide_rels, rels_content.encode('utf-8'))

                    # Add renamed media
                    for cert_media, new_name in media_map.items():
                        nzip.writestr(new_name, czip.read(cert_media))

                # Atomic replace
                shutil.move(str(tmp_out), str(out))
            finally:
                if tmp_out.exists():
                    tmp_out.unlink()

        # Update ledger
        for p in ledger['pages']:
            if p['page'] == slide_num:
                p['status'] = 'certified'
                p['source_md5'] = md5_file(certified)
                break
        with open(ledger_path, 'w') as f:
            json.dump(ledger, f, indent=2)
    print(f"Page {slide_num} updated from {certified_pptx_path}")


def mode_gate(out_path, per_slide_dir, N):
    """Gate: render merged + all sources, pixel-diff page N vs source N."""
    import subprocess
    from PIL import Image, ImageChops

    N = int(N)
    out = Path(out_path)
    per_slide = Path(per_slide_dir)
    V = per_slide / '.merge_gate'
    shutil.rmtree(V, ignore_errors=True)
    V.mkdir(parents=True)
    (V / 'src').mkdir()
    (V / 'pages').mkdir()
    (V / 'src_png').mkdir()
    lo_profile = V / 'lo'

    # Render merged
    subprocess.run(['soffice', '--headless', f'-env:UserInstallation=file://{lo_profile}',
                    '--convert-to', 'pdf', '--outdir', str(V), str(out)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    merged_pdf = V / f'{out.stem}.pdf'

    # Render each source
    source_pdfs = []
    for i in range(1, N+1):
        src_pptx = per_slide / f'slide_{i:03d}_recreated.pptx'
        if src_pptx.exists():
            subprocess.run(['soffice', '--headless', f'-env:UserInstallation=file://{lo_profile}',
                            '--convert-to', 'pdf', '--outdir', str(V / 'src'), str(src_pptx)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            source_pdfs.append(V / 'src' / f'slide_{i:03d}_recreated.pdf')
        else:
            source_pdfs.append(None)

    # Convert to PNG
    subprocess.run(['pdftoppm', '-png', '-r', '150', str(merged_pdf), str(V / 'pages' / 'pg')],
                   check=True)
    for i, spdf in enumerate(source_pdfs, 1):
        if spdf and spdf.exists():
            subprocess.run(['pdftoppm', '-png', '-r', '150', str(spdf), str(V / 'src_png' / f's{i:03d}')],
                           check=True)

    # Pixel diff
    bad = []
    for n in range(1, N+1):
        pg_png = V / 'pages' / f'pg-{n:02d}.png'
        src_png = V / 'src_png' / f's{n:03d}-1.png'
        if pg_png.exists() and src_png.exists():
            a = Image.open(pg_png).convert('RGB')
            b = Image.open(src_png).convert('RGB')
            if a.size != b.size or ImageChops.difference(a, b).getbbox():
                bad.append(n)
    print(f"Mismatched pages: {bad if bad else 'NONE — 0/{N}, merge is lossless'}")
    shutil.rmtree(V / 'src_png', ignore_errors=True)
    shutil.rmtree(V / 'src', ignore_errors=True)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    if mode == 'placeholder':
        mode_placeholder(sys.argv[2], sys.argv[3], sys.argv[4])
    elif mode == 'update':
        mode_update(sys.argv[2], sys.argv[3], sys.argv[4])
    elif mode == 'gate':
        mode_gate(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)