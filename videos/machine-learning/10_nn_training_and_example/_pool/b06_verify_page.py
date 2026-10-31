"""Verify final-deck page N matches the certified single-slide source, at the
OPC level: slide XML (verbatim, modulo relationship-id remap) and media bytes."""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

deck = Path(sys.argv[1])
n = int(sys.argv[2])
src = Path(sys.argv[3])


def md5(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.md5(b).hexdigest()


with zipfile.ZipFile(deck) as dz, zipfile.ZipFile(src) as sz:
    dx = dz.read(f"ppt/slides/slide{n}.xml").decode()
    sx = sz.read("ppt/slides/slide1.xml").decode()
    drels = dz.read(f"ppt/slides/_rels/slide{n}.xml.rels").decode()
    srels = sz.read("ppt/slides/_rels/slide1.xml.rels").decode()

    # media: source media m -> deck media slide{n}_{basename}
    src_media = {m: sz.read(m) for m in sz.namelist() if m.startswith("ppt/media/")}
    missing, mismatched = [], []
    for m, blob in src_media.items():
        target = f"ppt/media/slide{n}_{Path(m).name}"
        try:
            dblob = dz.read(target)
        except KeyError:
            missing.append(target)
            continue
        if md5(dblob) != md5(blob):
            mismatched.append((target, md5(blob), md5(dblob)))
    extra = [z for z in dz.namelist()
             if z.startswith(f"ppt/media/slide{n}_") and
             f"ppt/media/slide{n}_{Path(z).name}" not in src_media]

    # slide XML: strip r:embed ids that were remapped, then compare
    def norm(x, rels):
        r2 = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
        for rid, tgt in r2.items():
            x = x.replace(f'r:embed="{rid}"', f'r:embed="{Path(tgt).name}"')
        return x

    dxml = norm(dx, drels)
    sxml = norm(sx, srels)
    same_xml = dxml == sxml
    print(f"page {n} vs {src.name}")
    print(f"  slide xml identical (after rel-id normalization): {same_xml}")
    if not same_xml:
        print(f"    deck xml md5={md5(dx)} src xml md5={md5(sx)}")
    print(f"  source media: {len(src_media)}  missing in deck: {missing}")
    print(f"  media md5 mismatches: {mismatched}")
    print(f"  extra deck media for this page: {extra}")
    print(f"  VERDICT: {'MATCH' if same_xml and not missing and not mismatched else 'DIFF'}")
