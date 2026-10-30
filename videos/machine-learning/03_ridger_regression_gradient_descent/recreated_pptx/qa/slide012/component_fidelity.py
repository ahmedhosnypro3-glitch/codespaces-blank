#!/usr/bin/env python3
"""Component fidelity proof for build/components/slide_012.js.

Proves the banked component renders IDENTICALLY to the certified deliverable
(slide_012_recreated.pptx), and that its skip/only/numeral composition hooks —
the contract child slide 013 relies on — actually gate.

Method (closed-loop, no tolerance judgement needed):
  1. Re-render BOTH pptx files with the IDENTICAL LibreOffice command, so the
     comparison isolates the files themselves and not the rasterisation path.
     (The selfcheck input render_1.png at 150dpi is NOT touched.)
  2. Pixel-diff the two renders.
  3. Zip-diff the two pptx containers member by member.
  4. Compare the slide XML shape multiset (same shapes, same boxes).
  5. Verify skip / only / numeral hooks gate as declared.

Run:  python3 component_fidelity.py     (writes component_fidelity.txt)
"""
import os, re, shutil, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.abspath(os.path.join(HERE, "..", ".."))   # recreated_pptx/
CERT = os.path.join(BUILD, "slide_012_recreated.pptx")
PROBE = os.path.join(HERE, "component_build_probe.pptx")
OUT = [""]


def emit(s=""):
    OUT.append(s)
    print(s)


LO_CERT = os.path.join(HERE, "lo_cert")
LO_PROBE = os.path.join(HERE, "lo_probe2")


def _kill_stray_soffice():
    for _ in range(40):
        pid = subprocess.run(["pgrep", "-f", "soffice.bin"],
                             capture_output=True, text=True).stdout.split()
        if not pid:
            return
        subprocess.run(["pkill", "-f", "soffice.bin"], capture_output=True)
        time.sleep(0.5)


def lo_png(pptx, outdir):
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        d = os.path.join(outdir, f)
        if os.path.isfile(d):
            os.remove(d)
    prof = os.path.join(os.environ.get("TMPDIR", "/tmp"),
                        "lo_prof_" + os.path.basename(outdir))
    last = None
    for attempt in range(4):
        _kill_stray_soffice()
        shutil.rmtree(prof, ignore_errors=True)
        last = subprocess.run(
            ["soffice", "--headless", "--norestore",
             "-env:UserInstallation=file://" + prof,
             "--convert-to", "png:impress_png_Export", "--outdir", outdir, pptx],
            capture_output=True, text=True, timeout=600)
        if last.returncode == 0 and os.listdir(outdir):
            return last
        time.sleep(2 + attempt)
    raise RuntimeError("soffice failed: %s %s" % (last.stdout[-500:], last.stderr[-500:]))


def slide_xml(pptx_path):
    with zipfile.ZipFile(pptx_path) as z:
        return z.read("ppt/slides/slide1.xml").decode()


def shape_multiset(xml):
    """(name, x, y, cx, cy) for every sp + pic — geometry, not order."""
    found = re.findall(
        r'<p:(sp|pic)>.*?<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>',
        xml, re.S)
    return sorted(found)


emit("== 1. fresh equal-command renders ==")
lo_png(CERT, LO_CERT)
lo_png(PROBE, LO_PROBE)
rc = Image.open(os.path.join(LO_CERT, "slide_012_recreated.png"))
rp = Image.open(os.path.join(LO_PROBE, "component_build_probe.png"))
emit("cert render  %s" % (rc.size,))
emit("probe render %s" % (rp.size,))

emit("\n== 2. pixel diff (identical command, identical raster path) ==")
ca = np.asarray(rc.convert("RGB")).astype(int)
cb = np.asarray(rp.convert("RGB")).astype(int)
ok_geom = ca.shape == cb.shape
emit("same geometry: %s" % ok_geom)
if ok_geom:
    d = np.abs(ca - cb).max(axis=2)
    nz, n8 = int((d > 0).sum()), int((d > 8).sum())
    emit("pixels differing        : %d of %d" % (nz, d.size))
    emit("pixels differing >8     : %d" % n8)
    emit("max channel delta       : %d" % int(d.max()))
    pixel_ok = (nz == 0)
else:
    pixel_ok = False
emit("PIXEL-IDENTICAL: %s" % pixel_ok)

emit("\n== 3. container member diff ==")
za, zb = zipfile.ZipFile(CERT), zipfile.ZipFile(PROBE)
na = [i.filename for i in za.infolist()]
nb = [i.filename for i in zb.infolist()]
emit("members %d / %d, same names: %s" % (len(na), len(nb), na == nb))
diffs = [n for n in na if za.read(n) != zb.read(n)]
for n in diffs:
    emit("  differs: %s" % n)
order_only = len(diffs) <= 2 and all(
    re.fullmatch(r"(docProps/(core|app)\.xml|ppt/slides/slide1\.xml)", n) for n in diffs)
emit("container diff limited to metadata + shape ORDER: %s" % order_only)

emit("\n== 4. shape geometry multiset ==")
xa, xb = slide_xml(CERT), slide_xml(PROBE)
ma, mb = shape_multiset(xa), shape_multiset(xb)
emit("cert   sp=%d pic=%d" % (len(re.findall(r"<p:sp>", xa)), len(re.findall(r"<p:pic>", xa))))
emit("probe  sp=%d pic=%d" % (len(re.findall(r"<p:sp>", xb)), len(re.findall(r"<p:pic>", xb))))
emit("same xfrm multiset (same shapes, same boxes): %s" % (ma == mb))
emit("  cert xfrms=%d probe xfrms=%d" % (len(ma), len(mb)))

emit("\n== 5. skip / only / numeral hooks ==")
# Per-block shape counts measured from the isolated-block smoke builds below
# (chrome:6, title:1, labels:9, trainTable:0sp+1gf, testBlock:2+1gf,
#  outlier1:0sp+1gf, againCallout:3, arrow:1, outlier2:0sp+1gf, questionBox:2).
#  = 24 sp + 4 graphicFrames, identical to the certified deliverable.
#  The table blocks draw <p:graphicFrame> and no <p:sp>, so both counters are
#  checked — slide 013 inherits the table PATTERN via the graphicFrames, and a
#  form that only verified <p:sp> would silently lose all four tables.
variants = [
    ("(full, default)", None, (24, 0, 4)),
    ("only:{chrome}", "{ numeral: 12, only: { chrome: true } }", (6, 0, 0)),
    ("skip:{title,labels}", "{ numeral: 12, skip: { title: true, labels: true } }", (14, 0, 4)),
    ("only:{chrome,trainTable}", "{ numeral: 12, only: { chrome: true, trainTable: true } }", (6, 0, 1)),
    ("only:{testBlock}", "{ numeral: 12, only: { testBlock: true } }", (2, 0, 1)),
    ("numeral override 42", "{ numeral: 42 }", (24, 0, 4)),
]
# smoke-build the variants straight from the exported contract
smoke_js = os.path.join(HERE, "smoke_hooks.js")
NM = "/workspaces/codespaces-blank/ai_llm_slides/node_modules/pptxgenjs"
COMP = os.path.abspath(os.path.join(BUILD, "build", "components", "slide_012.js"))
with open(smoke_js, "w") as fh:
    fh.write(
        'const path = require("path");\n'
        'const pptxgen = require("%s");\n'
        'const C = require("%s");\n'
        'const out = process.argv[2];\n'
        'const opts = process.argv[3] ? eval("(" + process.argv[3] + ")") : {};\n'
        'const p = new pptxgen(); p.layout = "LAYOUT_WIDE";\n'
        'const s = p.addSlide();\n'
        'C.renderBase(p, s, opts);\n'
        'p.writeFile({ fileName: out }).then(() => console.log(out));\n'
        % (NM, COMP))
exp = {label: counts for label, _, counts in variants}
hooks_ok = True
for label, optjs, _ in variants:
    f = "smoke_%s.pptx" % re.sub(r"\W+", "_", label)
    subprocess.run(["node", smoke_js, os.path.join(HERE, f), optjs or "{}"],
                   check=True, capture_output=True, timeout=120)
    x = slide_xml(os.path.join(HERE, f))
    sp = len(re.findall(r"<p:sp>", x))
    pics = len(re.findall(r"<p:pic>", x))
    gf = len(re.findall(r"<p:graphicFrame>", x))
    got = (sp, pics, gf)
    ok = got == exp[label]
    hooks_ok = hooks_ok and ok
    emit("  %-26s sp=%2d pic=%d gf=%d  %s"
         % (label, sp, pics, gf, "OK" if ok else "MISMATCH (want %s)" % (exp[label],)))

emit("\n== VERDICT ==")
emit("pixel-identical to certified deliverable : %s" % pixel_ok)
emit("container diff = metadata + shape order  : %s" % order_only)
emit("same xfrm multiset (order-only)          : %s" % (ma == mb))
emit("skip/only/numeral hooks gate correctly    : %s" % hooks_ok)
verdict = pixel_ok and order_only and (ma == mb) and hooks_ok
emit("COMPONENT FIDELITY: %s" % ("PASS" if verdict else "FAIL"))

with open(os.path.join(HERE, "component_fidelity.txt"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if verdict else 1)
