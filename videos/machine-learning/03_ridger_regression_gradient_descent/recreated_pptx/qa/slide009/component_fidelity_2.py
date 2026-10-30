#!/usr/bin/env python3
"""Component fidelity proof, attempt 2 — build/components/slide_009.js (refreshed
2026-10-24) vs the certified slide_009_recreated.pptx.

Mirrors qa/slide009/component_fidelity.py (kept banked, untouched) but builds
the probe variants from the REFRESHED module into scratch/tmp, since the previous
probe files were cut from the pre-attempt-2 component. Method (closed-loop, no
tolerance judgement needed):
  1. build the probe pptx (+ 4 hook variants) from the component;
  2. re-render BOTH pptx files with the IDENTICAL LibreOffice command;
  3. pixel-diff the two renders;
  4. zip-diff the two containers member by member;
  5. count <p:sp>/<p:pic> in the full build vs each hook variant.

Run:  python3 component_fidelity_2.py     (writes component_fidelity_2.txt)
"""
import os, re, shutil, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.abspath(os.path.join(HERE, "..", ".."))   # recreated_pptx/
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", ".."))  # ai_llm_slides/
CERT = os.path.join(BUILD, "slide_009_recreated.pptx")
PROBE = os.path.join(ROOT, "scratch", "tmp", "probe_009_component.pptx")
COMPONENT = os.path.join(BUILD, "build", "components", "slide_009.js")
BUILDER = os.path.join(ROOT, "scratch", "tmp", "probe_build_009.js")
OUT = [""]


def emit(s=""):
    OUT.append(s)
    print(s)


def node(script, *args):
    env = dict(os.environ)
    env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"],
                                      capture_output=True, text=True).stdout.strip()
    r = subprocess.run(["node", script, *args], capture_output=True, text=True,
                       cwd=ROOT, env=env, timeout=300)
    return r


def _kill_stray_soffice():
    for _ in range(40):
        pid = subprocess.run(["pgrep", "-f", "soffice.bin"],
                             capture_output=True, text=True).stdout.split()
        if not pid:
            return
        subprocess.run(["pkill", "-f", "soffice.bin"], capture_output=True)
        time.sleep(0.5)


def lo_png(pptx, outdir):
    """Render via LibreOffice with a FRESH private UserInstallation profile
    (same command as the 150dpi selfcheck path, minus raster resolution)."""
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


emit("== 1. build probe variants from the REFRESHED component ==")
r = node(BUILDER, "full", PROBE)
emit("build: %s%s" % (r.stdout.strip(), r.stderr.strip()[-400:] if r.returncode else ""))
if r.returncode or not os.path.exists(PROBE):
    emit("PROBE BUILD FAILED")
    with open(os.path.join(HERE, "component_fidelity_2.txt"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    sys.exit(1)

VARIANTS = {
    "smoke_only_chrome": ("only:{chrome}", 6, 0),
    "smoke_skip_captions": ("skip:{captions}", 127, 2),
    "smoke_only_chrome_charts": ("only:{chrome,panels,axes}", 82, 0),
    "smoke_numeral_override": ("numeral override 42", 131, 2),
}
smoke = {}
for v, (label, _, _) in VARIANTS.items():
    p = os.path.join(ROOT, "scratch", "tmp", "probe_009_%s.pptx" % v)
    rr = node(BUILDER, v, p)
    emit("build %-28s rc=%d %s" % (v, rr.returncode, rr.stdout.strip()))
    smoke[v] = p

emit("\n== 2. fresh equal-command renders ==")
LO_CERT = os.path.join(HERE, "lo_cert")
LO_PROBE = os.path.join(HERE, "lo_probe2")
lo_png(CERT, LO_CERT)
lo_png(PROBE, LO_PROBE)
rc = Image.open(os.path.join(LO_CERT, "slide_009_recreated.png"))
rp = Image.open(os.path.join(LO_PROBE, "probe_009_component.png"))
emit("cert render  %s" % (rc.size,))
emit("probe render %s" % (rp.size,))

emit("\n== 3. pixel diff (identical command, identical raster path) ==")
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

emit("\n== 4. container member diff ==")
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
order_only = len(diffs) == 2 and all(
    re.fullmatch(r"(docProps/core\.xml|ppt/slides/slide1\.xml)", n) for n in diffs)
emit("container diff limited to metadata + shape ORDER (geometry/content equal): %s"
    % order_only)

emit("\n== 5. shape-order invariant (why order-only is safe) ==")
xa = za.read("ppt/slides/slide1.xml").decode()
xb = zb.read("ppt/slides/slide1.xml").decode()
emit("cert   sp=%d pic=%d" % (len(re.findall(r"<p:sp>", xa)), len(re.findall(r"<p:pic>", xb))))
emit("probe  sp=%d pic=%d" % (len(re.findall(r"<p:sp>", xb)), len(re.findall(r"<p:pic>", xb))))
xf_a = re.findall(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', xa)
xf_b = re.findall(r'<a:off x="(\d+)" y="(\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', xb)
emit("xfrm multiset equal (same shapes, same boxes, only sequence differs): %s"
    % (sorted(xf_a) == sorted(xf_b)))
emit("  cert xfrms=%d probe xfrms=%d" % (len(xf_a), len(xf_b)))

emit("\n== 6. skip / only / numeral hooks (the contract child 010 uses) ==")
hooks_ok = True
for v, (label, sp_want, pic_want) in VARIANTS.items():
    try:
        x = zipfile.ZipFile(smoke[v]).read("ppt/slides/slide1.xml").decode()
    except KeyError:
        emit("  %-30s MISSING" % label)
        hooks_ok = False
        continue
    sp, pics = len(re.findall(r"<p:sp>", x)), len(re.findall(r"<p:pic>", x))
    emit("  %-30s sp=%3d pic=%d  (want %d/%d)" % (label, sp, pics, sp_want, pic_want))
    hooks_ok = hooks_ok and ((sp, pics) == (sp_want, pic_want))

emit("\n== VERDICT ==")
emit("pixel-identical to certified deliverable : %s" % pixel_ok)
emit("container diff = metadata + shape order  : %s" % order_only)
emit("same xfrm multiset (order-only)          : %s" % (sorted(xf_a) == sorted(xf_b)))
emit("skip/only/numeral hooks gate correctly   : %s" % hooks_ok)
verdict = pixel_ok and order_only and (sorted(xf_a) == sorted(xf_b)) and hooks_ok
emit("COMPONENT FIDELITY: %s" % ("PASS" if verdict else "FAIL"))
with open(os.path.join(HERE, "component_fidelity_2.txt"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(0 if verdict else 1)
