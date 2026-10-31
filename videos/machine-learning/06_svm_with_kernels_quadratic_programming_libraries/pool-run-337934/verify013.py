import json, os
from PIL import Image
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
B = NS + "/recreated_pptx/build"
M = json.load(open(B + "/eq_013/manifest.json"))
# render geometry sanity: each PNG's pixel size / 600 must equal manifest w_in
for k, m in M.items():
    im = Image.open(m["path"])
    w, h = im.size[0] / 600, im.size[1] / 600
    ok = abs(w - m["w_in"]) < 0.01 and abs(h - m["h_in"]) < 0.01
    if not ok:
        print("MISMATCH", k, im.size, m["w_in"], m["h_in"])
print("asset size check done over", len(M), "assets")
# check the pptx embeds all images
import zipfile
z = zipfile.ZipFile(NS + "/recreated_pptx/slide_013_recreated.pptx")
media = [n for n in z.namelist() if n.startswith("ppt/media/")]
print("pptx media files:", len(media))
imgs = sum(1 for n in z.namelist() if n.startswith("ppt/slides/slide1.xml"))
xml = z.read("ppt/slides/slide1.xml").decode("utf8", "replace")
print("pic count in slide1:", xml.count("<p:pic>"), "text runs:", xml.count("<a:t>"))
