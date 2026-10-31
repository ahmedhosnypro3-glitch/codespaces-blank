#!/usr/bin/env bash
# Deck integrity audit (gateway-free, LO-local).
# Renders the current final deck ONCE and verifies every certified page is
# byte-equivalent to its canonical per-slide deliverable, plus confirms every
# placeholder page still shows its original frame full-bleed.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
OUT=_pool/deckaudit
DECK="10_nn_training_and_example_final.pptx"
P="$OUT/lo_profile"
mkdir -p "$OUT"
echo "=== deck integrity audit start $(date '+%F %T') ==="

python3 - <<'PY' > "$OUT/pages.txt"
import json
d = json.load(open("final_deck_ledger.json"))
for p in d["pages"]:
    print(p["slide_num"], p["status"])
PY

echo "--- rendering the full deck (one LO session) ---"
rm -rf "$P"; mkdir -p "$P"
soffice --headless -env:UserInstallation=file://"$P" \
  --convert-to pdf --outdir "$OUT" "$DECK" > "$OUT/lo.log" 2>&1
if [ ! -f "$OUT/10_nn_training_and_example_final.pdf" ]; then
  echo "FAIL: deck did not render"; tail -5 "$OUT/lo.log"; exit 1; fi
pdftoppm -png -r 100 "$OUT/10_nn_training_and_example_final.pdf" "$OUT/deck"
echo "pages rendered: $(ls "$OUT"/deck-*.png 2>/dev/null | wc -l)"
echo "expected pages : $(wc -l < "$OUT/pages.txt")"

python3 - <<'PY' > "$OUT/report.txt"
import json, zipfile, hashlib, re, os
from PIL import Image, ImageChops
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
os.chdir(NS)
deck = "10_nn_training_and_example_final.pptx"
d = json.load(open("final_deck_ledger.json"))
pages = {int(p["slide_num"]): p for p in d["pages"]}
z = zipfile.ZipFile(deck)
names = set(z.namelist())
rows, cert_ok, cert_bad, ph_ok, ph_bad = [], 0, 0, 0, 0
for num, p in sorted(pages.items()):
    try:
        merged = z.read(f"ppt/slides/slide{num}.xml")
    except KeyError:
        rows.append(f"page {num}: MISSING slidе part"); cert_bad += 1; continue
    if p["status"] == "certified":
        src = f"recreated_pptx/slide_{num:03d}_recreated.pptx"
        if not os.path.exists(src):
            rows.append(f"page {num}: canonical pptx MISSING at {src}"); cert_bad += 1; continue
        zs = zipfile.ZipFile(src)
        orig = zs.read("ppt/slides/slide1.xml")
        same = hashlib.md5(merged).hexdigest() == hashlib.md5(orig).hexdigest()
        # media rels resolve?
        rels = z.read(f"ppt/slides/_rels/slide{num}.xml.rels").decode()
        miss = []
        for t in re.findall(r'Target="([^"]+)"', rels):
            if "media/" in t:
                tb = t.split('/')[-1]
                if not any(n.endswith('/' + tb) for n in names): miss.append(tb)
        status = "BYTE-IDENTICAL" if same and not miss else "MISMATCH"
        if same and not miss: cert_ok += 1
        else: cert_bad += 1
        rows.append(f"page {num:>2}: {status} media_missing={miss or 'none'}")
    else:
        img = f"unique_slides/slide_{num:03d}.jpg"
        if not os.path.exists(img):
            rows.append(f"page {num}: ORIGINAL FRAME MISSING {img}"); ph_bad += 1; continue
        pg = f"_pool/deckaudit/deck-{num}.png"
        if not os.path.exists(pg):
            rows.append(f"page {num}: deck render page missing"); ph_bad += 1; continue
        a = Image.open(pg).convert("RGB")
        b = Image.open(img).convert("RGB").resize(a.size, Image.LANCZOS)
        diff = ImageChops.difference(a, b)
        px = list(diff.getdata())
        nz = sum(1 for c in px if sum(c) > 24) / len(px) * 100
        verdict = "PLACEHOLDER-OK" if nz < 6.0 else "PLACEHOLDER-DIFFERS"
        if nz < 6.0: ph_ok += 1
        else: ph_bad += 1
        rows.append(f"page {num:>2}: {verdict} nonbg={nz:.2f}%")
print(f"certified pages byte-verified: {cert_ok}/{len([p for p in pages.values() if p['status']=='certified'])}")
print(f"placeholder pages original-frame-verified: {ph_ok}/{len([p for p in pages.values() if p['status']!='certified'])}")
print(f"ACCEPT: {'YES' if cert_bad==0 and ph_bad==0 else 'NO'}  (cert_bad={cert_bad} ph_bad={ph_bad})")
print()
print("\n".join(rows))
PY
cat "$OUT/report.txt"
echo "=== deck integrity audit end $(date '+%F %T') ==="
