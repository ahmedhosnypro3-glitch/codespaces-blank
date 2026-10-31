#!/usr/bin/env python3
"""Map slide_005 equation pics (rel id, image, pos, size) to build sidecars."""
import json
import re
import zipfile
from pathlib import Path

NS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example')
PPTX = NS / 'recreated_pptx/slide_005_recreated.pptx'
ASSETS = NS / 'recreated_pptx/build/assets'

with zipfile.ZipFile(PPTX) as z:
    rels = z.read('ppt/slides/_rels/slide1.xml.rels').decode()
    xml = z.read('ppt/slides/slide1.xml').decode()

rel_map = dict(re.findall(r'Id="([^"]+)"[^>]*Target="\.\./media/([^"]+)"', rels))
pics = re.findall(r'<p:pic>.*?</p:pic>', xml, re.S)
print(f'{len(pics)} pics, {len(rel_map)} media rels\n')

sidecars = {}
for p in sorted(ASSETS.glob('eq_*.json')):
    try:
        d = json.loads(p.read_text())
    except Exception:
        continue
    sidecars[p.stem] = d

print('--- pics in document order ---')
for i, s in enumerate(pics, 1):
    rid = re.search(r'r:embed="([^"]+)"', s)
    name = re.search(r'<p:cNvPr id="\d+" name="([^"]*)"', s)
    descr = re.search(r'descr="([^"]*)"', s)
    off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', s)
    ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', s)
    img = rel_map.get(rid.group(1)) if rid else None
    x = int(off.group(1)) / 914400 if off else 0
    y = int(off.group(2)) / 914400 if off else 0
    w = int(ext.group(1)) / 914400 if ext else 0
    h = int(ext.group(2)) / 914400 if ext else 0
    print(f'{i:2d} {rid.group(1) if rid else "?":6s} {str(img):18s} '
          f'x={x:6.3f} y={y:6.3f} w={w:6.3f} h={h:6.3f} name={name.group(1) if name else ""} '
          f'descr={descr.group(1) if descr else ""}')

print('\n--- sidecars (w_in x h_in, font, color) ---')
for k, d in sorted(sidecars.items()):
    print(f'{k:16s} {d.get("w_in"):7.4f} x {d.get("h_in"):7.4f}  '
          f'fs={d.get("fontsize_pt")} color={d.get("color")} '
          f'px={d.get("w_px")}x{d.get("h_px")} path={Path(str(d.get("path"))).name}')
