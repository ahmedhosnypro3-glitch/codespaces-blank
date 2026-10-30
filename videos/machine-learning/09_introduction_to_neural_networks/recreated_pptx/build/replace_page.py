#!/usr/bin/env python3
"""Replace a single page in the final deck at OPC level (byte-verbatim)."""
import zipfile
from pathlib import Path
import re
import sys

def replace_page(deck_path, slide_num, source_pptx):
    """Replace slide N in deck with content from source_pptx."""
    deck = zipfile.ZipFile(deck_path, 'r')
    source = zipfile.ZipFile(source_pptx, 'r')
    
    out_path = deck_path.with_suffix('.tmp.pptx')
    zf = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)
    
    # Copy everything from deck except the slide we're replacing
    for name in deck.namelist():
        if name.endswith('/'):
            continue
        # Skip the target slide parts
        if name == f"ppt/slides/slide{slide_num}.xml":
            continue
        if name == f"ppt/slides/_rels/slide{slide_num}.xml.rels":
            continue
        if name == f"ppt/notesSlides/notesSlide{slide_num}.xml":
            continue
        if name == f"ppt/notesSlides/_rels/notesSlide{slide_num}.xml.rels":
            continue
        # Skip media files for this slide
        if name.startswith(f"ppt/media/img{slide_num:03d}_"):
            continue
        zf.writestr(name, deck.read(name))
    
    # Copy the target slide from source (source uses slide1.xml)
    zf.writestr(f"ppt/slides/slide{slide_num}.xml", source.read("ppt/slides/slide1.xml"))
    zf.writestr(f"ppt/notesSlides/notesSlide{slide_num}.xml", 
                source.read("ppt/notesSlides/notesSlide1.xml"))
    
    # Copy and retarget media
    media_names = [m for m in source.namelist() 
                   if m.startswith("ppt/media/") and not m.endswith("/")]
    for m in sorted(media_names):
        base = Path(m).name
        zf.writestr(f"ppt/media/img{slide_num:03d}_{base}", source.read(m))
    
    # Retarget rels
    def retarget(mo):
        rid, rtype, target = mo.groups()
        t = rtype.rsplit("/", 1)[-1]
        if t == "slideLayout":
            new = "../slideLayouts/slideLayout1.xml"
        elif t == "notesSlide":
            new = f"../notesSlides/notesSlide{slide_num}.xml"
        elif t == "image":
            new = f"../media/img{slide_num:03d}_{Path(target).name}"
        else:
            raise SystemExit(f"FATAL: unhandled rel type {rtype}")
        return f'<Relationship Id="{rid}" Type="{rtype}" Target="{new}"/>'
    
    rels = source.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8")
    rels = re.sub(r'<Relationship Id="([^"]+)" Type="([^"]+)" Target="([^"]+)"/>',
                  retarget, rels)
    zf.writestr(f"ppt/slides/_rels/slide{slide_num}.xml.rels", rels)
    
    nrels = source.read("ppt/notesSlides/_rels/notesSlide1.xml.rels").decode("utf-8")
    nrels = nrels.replace("../slides/slide1.xml", f"../slides/slide{slide_num}.xml")
    zf.writestr(f"ppt/notesSlides/_rels/notesSlide{slide_num}.xml.rels", nrels)
    
    zf.close()
    deck.close()
    source.close()
    
    # Atomic replace
    out_path.replace(deck_path)
    print(f"Replaced slide {slide_num} in {deck_path}")

if __name__ == "__main__":
    deck_path = Path(sys.argv[1])
    slide_num = int(sys.argv[2])
    source_pptx = Path(sys.argv[3])
    replace_page(deck_path, slide_num, source_pptx)
