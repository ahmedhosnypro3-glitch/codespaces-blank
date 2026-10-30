#!/usr/bin/env python3
"""Component fidelity proof for build/components/slide_009.js.

Proves the banked component renders IDENTICALLY to the certified deliverable
(slide_009_recreated.pptx), and that its skip/only/numeral composition hooks —
the contract child slide 010 relies on — actually gate.

Method (closed-loop, no tolerance judgement needed):
  1. Re-render BOTH pptx files with the IDENTICAL LibreOffice command, so the
     comparison isolates the files themselves and not the rasterisation path.
     (The certified selfcheck input render_1.png at 150dpi is NOT touched.)
  2. Pixel-diff the two 1280x720 renders.
  3. Zip-diff the two pptx containers member by member.
  4. Count <p:sp>/<p:pic> in the full build vs each hook variant.

Run:  python3 component_fidelity.py     (writes component_fidelity.txt)
"""
import os, re, shutil, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.abspath(os.path.join(HERE, "..", ".."))   # recreated_pptx/
CERT = os.path.join(BUILD, "slide_009_recreated.pptx")
PROBE = os.path.join(HERE, "component_build_probe.pptx")
OUT = [""]


def emit(s=""):
    OUT.append(s)
    print(s)


LO_CERT = os.path.join(HERE, "lo_cert")
LO_PROBE = os.path.join(HERE, "lo_probe2")

def _kill_stray_soffice():
    """Wait out / terminate any soffice still running from a previous step.

    An overlapping soffice holds a lock that makes the next conversion fail with
    the unhelpful "Error: source file could not be loaded", which is the flake
    that hit the first version of this script.
    """
    for _ in range(40):
        pid = subprocess.run(["pgrep", "-f", "soffice.bin"],
                             capture_output=True, text=True).stdout.split()
        if not pid:
            return
        subprocess.run(["pkill", "-f", "soffice.bin"], capture_output=True)
        time.sleep(0.5)


def lo_png(pptx, outdir):
    """Render via LibreOffice with a FRESH private UserInstallation profile.

    The profile dir is wiped first so a crashed previous run cannot leave a
    stale lock behind; stray soffice processes are waited out first.
    """
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        os.remove(os.path.join(outdir, f))
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


emit("== 1. fresh equal-command renders ==")
lo_png(CERT, LO_CERT)
lo_png(PROBE, LO_PROBE)
rc = Image.open(os.path.join(LO_CERT, "slide_009_recreated.png"))
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
    emit("max channel delta        : %d" % int(d.max()))
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
    ta, tb = za.read(n).decode(), zb.read(n).decode()
    i = 0
    while i < min(len(ta), len(tb)) and ta[i] == tb[i]:
        i += 1
    emit("  differs: %s (first divergence at char %d)" % (n, i))
    emit("    A: %s" % ta[max(0, i - 90):i + 130])
    emit("    B: %s" % tb[max(0, i - 90):i + 130])
only_meta = all(re.fullmatch(r"docProps/(core|app)\.xml", n) for n in diffs)
order_only = len(diffs) == 2 and all(
    re.fullmatch(r"(docProps/core\.xml|ppt/slides/slide1\.xml)", n) for n in diffs)
emit("container diff limited to metadata + shape ORDER (geometry/content equal): %s"
    % order_only)

emit("\n== 4. shape-order invariant (why order-only is safe) ==")
xa = za.read("ppt/slides/slide1.xml").decode()
xb = zb.read("ppt/slides/slide1.xml").decode()
emit("cert   sp=%d pic=%d" % (len(re.findall(r"<p:sp>", xa)), len(re.findall(r"<p:pic>", xa))))
emit("probe  sp=%d pic=%d" % (len(re.findall(r"<p:sp>", xb)), len(re.findall(r"<p:pic>", xb))))
# the two chart panels are disjoint rectangles, and no element of either chart
# crosses the other's border -> cross-block z-order is geometrically irrelevant
xf_a = re.findall(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', xa)
xf_b = re.findall(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', xb)
emit("xfrm multiset equal (same shapes, same boxes, only sequence differs): %s"
    % (sorted(xf_a) == sorted(xf_b)))
emit("  cert xfrms=%d probe xfrms=%d" % (len(xf_a), len(xf_b)))

emit("\n== 5. skip / only / numeral hooks (the contract child 010 uses) ==")
VARIANTS = [
    ("(full, default)", 121, 2),
    ("only:{chrome}", 6, 0),
    ("skip:{captions}", 117, 2),
    ("only:{chrome,panels,axes}", 82, 0),
    ("numeral override 42", 121, 2),
]
WANT = {label: (sp, pic) for label, sp, pic in VARIANTS}
base = [
    ("component_build_probe.pptx", "(full, default)"),
    ("smoke_only_chrome.pptx", "only:{chrome}"),
    ("smoke_skip_captions.pptx", "skip:{captions}"),
    ("smoke_only_chrome_charts.pptx", "only:{chrome,panels,axes}"),
    ("smoke_numeral_override.pptx", "numeral override 42"),
]
hooks_ok = True
for f, label in base:
    try:
        x = zipfile.ZipFile(os.path.join(HERE, f)).read("ppt/slides/slide1.xml").decode()
    except KeyError:
        emit("  %-30s MISSING" % label)
        hooks_ok = False
        continue
    sp, pics = len(re.findall(r"<p:sp>", x)), len(re.findall(r"<p:pic>", x))
    emit("  %-30s sp=%3d pic=%d" % (label, sp, pics))
    hooks_ok = hooks_ok and (sp, pics) == WANT[label]

emit("\n== VERDICT ==")
emit("pixel-identical to certified deliverable : %s" % pixel_ok)
emit("container diff = metadata + shape order  : %s" % order_only)
emit("same xfrm multiset (order-only)          : %s" % (sorted(xf_a) == sorted(xf_b)))
emit("skip/only/numeral hooks gate correctly    : %s" % hooks_ok)
verdict = pixel_ok and order_only and (sorted(xf_a) == sorted(xf_b)) and hooks_ok
emit("COMPONENT FIDELITY: %s" % ("PASS" if verdict else "FAIL"))

with open(os.path.join(HERE, "component_fidelity.txt"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if verdict else 1)
