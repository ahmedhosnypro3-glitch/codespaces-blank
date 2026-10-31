#!/usr/bin/env python3
"""Byte-compare final deck page parts against candidate certified pptx files."""
import hashlib
import sys
import zipfile
from pathlib import Path

NS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example')
DECK = NS / '10_nn_training_and_example_final.pptx'


def parts(pptx):
    with zipfile.ZipFile(pptx) as z:
        names = set(z.namelist())
        out = {}
        for n in names:
            if n.startswith('ppt/slides/slide') and n.endswith('.xml'):
                out[n] = hashlib.md5(z.read(n)).hexdigest()
        return out


def page_media(pptx, page):
    """md5 of media referenced by a page's rels."""
    with zipfile.ZipFile(pptx) as z:
        rels = z.read(f'ppt/slides/_rels/slide{page}.xml.rels').decode()
        import re
        tgts = re.findall(r'Target="\.\./media/([^"]+)"', rels)
        return {t: hashlib.md5(z.read(f'ppt/media/{t}')).hexdigest() for t in tgts}


deck_parts = parts(DECK)
print('deck slide parts:', {k: v[:8] for k, v in sorted(deck_parts.items()) if k.endswith('.xml')})

for page, cand in [(5, 'recreated_pptx/build/slide_005_recreated.pptx'),
                   (5, 'recreated_pptx/slide_005_recreated.pptx'),
                   (6, 'recreated_pptx/build/slide_006_recreated.pptx'),
                   (6, 'recreated_pptx/build/slide_006_v3.pptx')]:
    p = NS / cand
    if not p.exists():
        print(f'page {page} <- {cand}: MISSING FILE')
        continue
    cp = parts(p)
    src = cp.get('ppt/slides/slide1.xml')
    dst = deck_parts.get(f'ppt/slides/slide{page}.xml')
    same = src == dst
    print(f'page {page} <- {cand}: slide1.xml={src[:8]} deck={dst[:8]} MATCH={same}')
    if same:
        try:
            dm = page_media(DECK, page)
            sm = page_media(p, 1)
            mm = {k: v for k, v in dm.items() if k.startswith(f'slide{page}_') or k.startswith(f'page{page}_')}
            smapped = {f'slide{page}_' + k: v for k, v in sm.items()}
            print(f'   media match: {mm == smapped} ({len(mm)} media)')
        except Exception as e:
            print('   media compare error:', e)
