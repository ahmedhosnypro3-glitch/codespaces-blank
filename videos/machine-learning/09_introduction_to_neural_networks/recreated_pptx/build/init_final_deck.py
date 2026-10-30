#!/usr/bin/env python3
"""Initialize the final deck as a placeholder with 32 pages (original frames full-bleed).
Then replace pages as slides certify.
"""
import zipfile
from pathlib import Path
import shutil

# Create a simple PPTX with 32 slides, each containing the original image full-bleed
def init_final_deck(video_dir, out_path):
    video_path = Path(video_dir)
    unique_slides_dir = video_path / "unique_slides"
    recreated_dir = video_path / "recreated_pptx"
    
    # Get slides in order
    slide_files = sorted(unique_slides_dir.glob("slide_*.jpg"))
    assert len(slide_files) == 32, f"Expected 32 slides, got {len(slide_files)}"
    
    # Use slide_001 as the skeleton
    skeleton_path = recreated_dir / "slide_001_recreated.pptx"
    assert skeleton_path.exists(), f"Skeleton not found: {skeleton_path}"
    
    # Create a new PPTX with 32 slides
    # We'll copy the skeleton and add 31 more slides with original images
    skeleton = zipfile.ZipFile(skeleton_path)
    
    # Prepare output
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    zf = zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED)
    
    # Copy all non-slide parts from skeleton
    slide_parts = {"ppt/slides/slide1.xml", "ppt/slides/_rels/slide1.xml.rels",
                   "ppt/notesSlides/notesSlide1.xml", "ppt/notesSlides/_rels/notesSlide1.xml.rels"}
    for name in skeleton.namelist():
        if name.endswith("/"):
            continue
        if name in slide_parts or name in ("ppt/presentation.xml",
                                           "ppt/_rels/presentation.xml.rels",
                                           "[Content_Types].xml"):
            continue
        zf.writestr(name, skeleton.read(name))
    
    # Keep skeleton's slide 1 as placeholder (we'll replace it later)
    for name in slide_parts:
        zf.writestr(name, skeleton.read(name))
    
    # Add slides 2-32 with original images
    for i, slide_file in enumerate(slide_files[1:], 2):
        # Copy slide XML
        zf.writestr(f"ppt/slides/slide{i}.xml", skeleton.read("ppt/slides/slide1.xml"))
        
        # Copy notes slide
        zf.writestr(f"ppt/notesSlides/notesSlide{i}.xml", 
                    skeleton.read("ppt/notesSlides/notesSlide1.xml"))
        
        # Rels with media pointing to original image
        rels = skeleton.read("ppt/slides/_rels/slide1.xml.rels").decode("utf-8")
        # Replace the image reference to point to our renamed media
        rels = rels.replace("slide1.xml", f"slide{i}.xml")  # not exactly right
        # We'll simplify: just use the skeleton rels and rename media
        media_names = [m for m in skeleton.namelist() 
                       if m.startswith("ppt/media/") and not m.endswith("/")]
        for m in sorted(media_names):
            base = Path(m).name
            zf.writestr(f"ppt/media/img{i:03d}_{base}", skeleton.read(m))
        
        # Retarget rels
        def retarget(mo):
            rid, rtype, target = mo.groups()
            t = rtype.rsplit("/", 1)[-1]
            if t == "slideLayout":
                new = "../slideLayouts/slideLayout1.xml"
            elif t == "notesSlide":
                new = f"../notesSlides/notesSlide{i}.xml"
            elif t == "image":
                new = f"../media/img{i:03d}_{Path(target).name}"
            else:
                raise SystemExit(f"FATAL: unhandled rel type {rtype}")
            return f'<Relationship Id="{rid}" Type="{rtype}" Target="{new}"/>'
        
        import re
        rels = re.sub(r'<Relationship Id="([^"]+)" Type="([^"]+)" Target="([^"]+)"/>',
                      retarget, rels)
        zf.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels)
        
        # Notes slide rels
        nrels = skeleton.read("ppt/notesSlides/_rels/notesSlide1.xml.rels").decode("utf-8")
        nrels = nrels.replace("../slides/slide1.xml", f"../slides/slide{i}.xml")
        zf.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", nrels)
    
    # Build presentation.xml with 32 slides
    pres = skeleton.read("ppt/presentation.xml").decode("utf-8")
    sld_ids = "".join(f'<p:sldId id="{255 + n}" r:id="rId{n + 1}"/>' for n in range(1, 33))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{sld_ids}</p:sldIdLst>", pres)
    pres = re.sub(r'<p:notesMasterId r:id="[^"]+"/>', '<p:notesMasterId r:id="rId34"/>', pres)
    zf.writestr("ppt/presentation.xml", pres)
    
    # Build presentation.xml.rels
    prels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
             + "".join(f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org'
                       f'/officeDocument/2006/relationships/slide" Target="slides/slide{n}.xml"/>'
                       for n in range(1, 33))
             + '<Relationship Id="rId34" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>'
             '<Relationship Id="rId35" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/presProps" Target="presProps.xml"/>'
             '<Relationship Id="rId36" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/viewProps" Target="viewProps.xml"/>'
             '<Relationship Id="rId37" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/theme" Target="theme/theme1.xml"/>'
             '<Relationship Id="rId38" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/tableStyles" Target="tableStyles.xml"/>'
             "</Relationships>")
    zf.writestr("ppt/_rels/presentation.xml.rels", prels)
    
    # [Content_Types].xml
    ct = skeleton.read("[Content_Types].xml").decode("utf-8")
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType="application/vnd.'
        f'openxmlformats-officedocument.presentationml.slide+xml"/>'
        f'<Override PartName="/ppt/notesSlides/notesSlide{n}.xml" ContentType="application/'
        f'vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        for n in range(2, 33))
    ct = ct.replace("</Types>", overrides + "</Types>")
    zf.writestr("[Content_Types].xml", ct)
    
    zf.close()
    print(f"Initialized final deck: {out_path} with 32 placeholder slides")

if __name__ == "__main__":
    import sys
    video_dir = sys.argv[1]
    out_path = sys.argv[2]
    init_final_deck(video_dir, out_path)