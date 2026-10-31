#!/usr/bin/env python3
"""Extract all text runs from a single-slide pptx (slide1.xml) for content verification."""
import re
import sys
import zipfile

path = sys.argv[1]
with zipfile.ZipFile(path) as z:
    xml = z.read('ppt/slides/slide1.xml').decode('utf-8')
runs = re.findall(r'<a:t>(.*?)</a:t>', xml, re.S)
media = [n for n in z.namelist() if n.startswith('ppt/media/')]
print(f'--- {path}')
print(f'text runs: {len(runs)}   media parts: {len(media)}')
for i, r in enumerate(runs, 1):
    t = re.sub(r'\s+', ' ', r).strip()
    if t:
        print(f'  {i:2d}: {t[:120]}')
