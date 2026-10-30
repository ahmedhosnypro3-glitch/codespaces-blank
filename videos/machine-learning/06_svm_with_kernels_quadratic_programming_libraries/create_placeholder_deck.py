#!/usr/bin/env python3
"""Create placeholder final deck: one page per approved frame, original image full-bleed."""

import json
import re
import sys
import zipfile
from pathlib import Path

SLIDE_W = 12192000  # 13.333 in
SLIDE_H = 6858000   # 7.5 in


def slide_xml_with_image():
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld>
<a:spTree>
<a:nvGrpSpPr><a:cNvPr id="1" name=""/><a:cNvGrpSpPr/><a:nvPr/></a:nvGrpSpPr>
<a:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></a:grpSpPr>
<a:pic>
<a:nvPicPr><a:cNvPr id="2" name="Original frame"/><a:cNvPicPr><a:nvPr/></a:cNvPicPr><a:nvPr/></a:nvPicPr>
<a:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></a:blipFill>
<a:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></a:spPr>
</a:pic>
</a:spTree>
</p:cSld>
<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>'''


def slide_rels(img_name):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{img_name}"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>'''


def notes_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><a:spTree><a:nvGrpSpPr><a:cNvPr id="1" name=""/><a:cNvGrpSpPr/><a:nvPr/></a:nvGrpSpPr><a:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></a:grpSpPr></a:spTree></p:cSld>
<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>'''


def notes_rels(n):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{n}.xml"/>
</Relationships>'''


def main():
    slides_index = Path(sys.argv[1])
    frames_dir = Path(sys.argv[2])
    out_pptx = Path(sys.argv[3])
    skeleton_pptx = Path(sys.argv[4])

    with open(slides_index) as f:
        slides = json.load(f)["slides"]
    total = len(slides)

    skel = zipfile.ZipFile(skeleton_pptx)
    out_pptx.parent.mkdir(parents=True, exist_ok=True)
    zf = zipfile.ZipFile(out_pptx, "w", zipfile.ZIP_DEFLATED)

    for name in skel.namelist():
        if name.endswith("/"):
            continue
        if re.match(r"ppt/slides/", name) or re.match(r"ppt/notesSlides/", name):
            continue
        if name in ("ppt/presentation.xml", "ppt/_rels/presentation.xml.rels",
                    "[Content_Types].xml"):
            continue
        zf.writestr(name, skel.read(name))

    media_overrides = []
    for idx, slide_info in enumerate(slides):
        n = idx + 1
        img_path = frames_dir / slide_info["filename"]
        img_bytes = img_path.read_bytes()
        img_name = f"img{n:03d}_{slide_info['filename']}"
        zf.writestr(f"ppt/media/{img_name}", img_bytes)
        media_overrides.append(
            f'<Override PartName="/ppt/media/{img_name}" ContentType="image/jpeg"/>')
        zf.writestr(f"ppt/slides/slide{n}.xml", slide_xml_with_image())
        zf.writestr(f"ppt/slides/_rels/slide{n}.xml.rels", slide_rels(img_name))
        zf.writestr(f"ppt/notesSlides/notesSlide{n}.xml", notes_xml())
        zf.writestr(f"ppt/notesSlides/_rels/notesSlide{n}.xml.rels", notes_rels(n))

    pres = skel.read("ppt/presentation.xml").decode("utf-8")
    sld_ids = "".join(
        f'<p:sldId id="{255 + n}" r:id="rId{n + 1}"/>' for n in range(1, total + 1))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>",
                  f"<p:sldIdLst>{sld_ids}</p:sldIdLst>", pres, flags=re.DOTALL)
    pres = re.sub(r'<p:notesMasterId r:id="[^"]+"/>',
                  '<p:notesMasterId r:id="rId66"/>', pres)
    zf.writestr("ppt/presentation.xml", pres)

    prels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
             + "".join(f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org/officeDocument'
                       f'/2006/relationships/slide" Target="slides/slide{n}.xml"/>'
                       for n in range(1, total + 1))
             + '<Relationship Id="rId66" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>'
             '<Relationship Id="rId67" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/presProps" Target="presProps.xml"/>'
             '<Relationship Id="rId68" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/viewProps" Target="viewProps.xml"/>'
             '<Relationship Id="rId69" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/theme" Target="theme/theme1.xml"/>'
             '<Relationship Id="rId70" Type="http://schemas.openxmlformats.org/officeDocument'
             '/2006/relationships/tableStyles" Target="tableStyles.xml"/>'
             "</Relationships>")
    zf.writestr("ppt/_rels/presentation.xml.rels", prels)

    ct = skel.read("[Content_Types].xml").decode("utf-8")
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType="application/vnd.'
        f'openxmlformats-officedocument.presentationml.slide+xml"/>'
        f'<Override PartName="/ppt/notesSlides/notesSlide{n}.xml" ContentType="application/'
        f'vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        for n in range(1, total + 1))
    overrides += "".join(media_overrides)
    ct = ct.replace("</Types>", overrides + "</Types>")
    zf.writestr("[Content_Types].xml", ct)

    zf.close()
    skel.close()
    print(f"Created placeholder deck: {out_pptx} ({total} slides, original frames full-bleed)")


if __name__ == "__main__":
    main()