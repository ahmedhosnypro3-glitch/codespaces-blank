#!/usr/bin/env python3
"""Inspect slide_031 pptx media: which PNGs are embedded, at what size."""
import zipfile, re
from PIL import Image
import io, os

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
pptx = f"{V}/recreated_pptx/build/slide_031_recreated.pptx"
z = zipfile.ZipFile(pptx)
names = [n for n in z.namelist() if n.startswith("ppt/media/")]
for n in sorted(names):
    data = z.read(n)
    try:
        im = Image.open(io.BytesIO(data))
        print(f"{n:30s} {im.size} {len(data)} bytes")
    except Exception as e:
        print(n, "ERR", e)

print("\n=== slide1.xml rels ===")
rels = z.read("ppt/slides/_rels/slide1.xml.rels").decode()
for m in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels):
    print(m.group(1), m.group(2))

print("\n=== pic elements on slide1 ===")
xml = z.read("ppt/slides/slide1.xml").decode()
for m in re.finditer(r'<p:pic>.*?</p:pic>', xml, re.S):
    s = m.group(0)
    rid = re.search(r'r:embed="([^"]+)"', s)
    ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"', s)
    off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"', s)
    name = re.search(r'name="([^"]*)"', s)
    if ext and off:
        cx, cy = int(ext.group(1)), int(ext.group(2))
        print(f"{name.group(1) if name else '?':24s} rid={rid.group(1) if rid else '?':6s} "
              f"x={int(off.group(1))/914400:.3f} y={int(off.group(2))/914400:.3f} "
              f"w={cx/914400:.3f} h={cy/914400:.3f}")
