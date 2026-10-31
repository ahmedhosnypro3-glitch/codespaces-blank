#!/usr/bin/env bash
# Scoped merge gate for page 8: rebuild a 1-page deck containing ONLY slide 8 by
# rewriting presentation.xml + its rels, then pixel-diff vs the certified source.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
V="_pool/b04/gate_p8"
rm -rf "$V"; mkdir -p "$V/pages" "$V/src"
export TMPDIR="$NS/_pool/b04"
timeout 240 soffice --headless -env:UserInstallation=file://"$NS/_pool/b04/lo_profile" \
  --convert-to pdf --outdir "$V/src" recreated_pptx/slide_008_recreated.pptx >/dev/null 2>&1
pdftoppm -png -r 150 "$V/src/slide_008_recreated.pdf" "$V/src/s008" 2>/dev/null
python3 - "$V" <<'PY'
import sys, os, zipfile, re
V=sys.argv[1]
src='/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/10_nn_training_and_example_final.pptx'
out=os.path.join(V,'deck_p8.pptx')
z=zipfile.ZipFile(src)
names=z.namelist()
# keep only slide8 part; drop other slide parts + their rels + notesSlides
keep_slide='ppt/slides/slide8.xml'
keep_rels='ppt/slides/_rels/slide8.xml.rels'
pres_rels=z.read('ppt/_rels/presentation.xml.rels').decode('utf8')
pres=z.read('ppt/presentation.xml').decode('utf8')
# find rId -> target for slides
rel_map={m.group(1):m.group(2) for m in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', pres_rels)}
sld_ids=re.findall(r'<p:sldId[^>]*r:id="([^"]+)"[^>]*/>', pres)
keep_rid=None
for rid in sld_ids:
    tgt=rel_map.get(rid,'')
    if tgt.endswith('slides/slide8.xml'):
        keep_rid=rid; break
assert keep_rid, 'slide8 rId not found'
# rewrite presentation.xml to a single sldId
new_pres=re.sub(r'(<p:sldIdLst>).*?(</p:sldIdLst>)',
                 r'\1<p:sldId id="256" r:id="%s"/>\2'%keep_rid, pres, flags=re.S)
# rewrite presentation rels: keep only the slide8 rel + layout/master/theme/presProps etc.
out_rels=[]
for m in re.finditer(r'<Relationship\b[^>]*/>', pres_rels):
    tag=m.group(0)
    rid=re.search(r'Id="([^"]+)"', tag).group(1)
    typ=re.search(r'Type="([^"]+)"', tag).group(1)
    if typ.endswith('/slide'):
        if rid==keep_rid: out_rels.append(tag)
        continue
    out_rels.append(tag)
new_rels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(out_rels) + '</Relationships>'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as o:
    for it in z.infolist():
        n=it.filename
        if n=='ppt/presentation.xml': o.writestr(it, new_pres.encode('utf8')); continue
        if n=='ppt/_rels/presentation.xml.rels': o.writestr(it, new_rels.encode('utf8')); continue
        if re.match(r'ppt/slides/slide\d+\.xml$', n) and n!=keep_slide: continue
        if re.match(r'ppt/slides/_rels/slide\d+\.xml\.rels$', n) and n!=keep_rels: continue
        if n.startswith('ppt/notesSlides/'): continue
        if re.match(r'ppt/notesSlides/_rels/', n): continue
        o.writestr(it, z.read(n))
print('wrote 1-page deck')
PY
timeout 240 soffice --headless -env:UserInstallation=file://"$NS/_pool/b04/lo_profile" \
  --convert-to pdf --outdir "$V/pages" "$V/deck_p8.pptx" >/dev/null 2>&1
pdftoppm -png -r 150 "$V/pages/deck_p8.pdf" "$V/pages/pg" 2>/dev/null
python3 - <<'PY'
import glob
from PIL import Image, ImageChops
a=sorted(glob.glob('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/b04/gate_p8/pages/pg-*.png'))
b=sorted(glob.glob('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/b04/gate_p8/src/s008-*.png'))
print('deck pages rendered:', len(a), '| src:', len(b))
if a and b:
    x=Image.open(a[0]).convert('RGB'); y=Image.open(b[0]).convert('RGB')
    print('sizes', x.size, y.size)
    if x.size==y.size:
        diff=ImageChops.difference(x,y); n=sum(1 for p in diff.getdata() if p!=(0,0,0))
        print('differing px:', n)
        print('RESULT:', 'GATE PASS' if n==0 else 'GATE FAIL')
PY
