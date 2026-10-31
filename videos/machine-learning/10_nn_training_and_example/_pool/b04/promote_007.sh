#!/usr/bin/env bash
# b04 slide 007 promotion: once attempt-7 carries a banked FINAL VERDICT: PASS,
# promote it to the single-version deliverable name, re-render, prove the render is
# pixel-identical to the judged render, and merge page 7 into the final deck.
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
SRC="recreated_pptx/build/slide_007_attempt7.pptx"
DEST="recreated_pptx/slide_007_recreated.pptx"

# 1) banked PASS check — refuse to promote without it
PASSFILE=$(grep -l "FINAL VERDICT: PASS" qa/slide007/rejudge/judge_r8_attempt_*.txt 2>/dev/null | head -1 || true)
[ -n "$PASSFILE" ] || { echo "ABORT: no banked PASS transcript for slide 7"; exit 3; }
echo "using PASS transcript: $PASSFILE"

# 2) park the superseded deliverable in qa/ (never delete)
mkdir -p qa/slide007/superseded
if [ -f "$DEST" ]; then
  cp -p "$DEST" "qa/slide007/superseded/slide_007_recreated_pre_attempt7_$(date +%Y%m%d_%H%M%S).pptx"
fi

# 3) promote
cp -p "$SRC" "$DEST"
cp -p "$SRC" recreated_pptx/build/slide_007_recreated.pptx
md5sum "$DEST" recreated_pptx/build/slide_007_recreated.pptx

# 4) re-render the promoted deliverable and prove it matches the judged render
export TMPDIR="$NS/_pool/b04"
rm -rf _pool/b04/promo7; mkdir -p _pool/b04/promo7
timeout 240 soffice --headless -env:UserInstallation=file://"$NS/_pool/b04/lo_profile" \
  --convert-to pdf --outdir _pool/b04/promo7 "$DEST" >/dev/null 2>&1
pdftoppm -png -r 150 -f 1 -l 1 _pool/b04/promo7/slide_007_recreated.pdf _pool/b04/promo7/p7
python3 - <<'PY'
from PIL import Image, ImageChops
import sys
a=Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/b04/promo7/p7-1.png').convert('RGB')
b=Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/b04/render2/s7a7-1.png').convert('RGB')
print('promo render', a.size, 'judged render', b.size)
if a.size!=b.size:
    print('SIZE MISMATCH'); sys.exit(4)
n=sum(1 for p in ImageChops.difference(a,b).getdata() if p!=(0,0,0))
print('differing px vs judged render:', n)
if n!=0:
    print('RENDER MISMATCH - abort before merge'); sys.exit(5)
print('RENDER MATCHES JUDGED IMAGE')
PY

# 5) merge page 7 (only via merge_final_deck.py) and verify the ledger
python3 merge_final_deck.py update 7 "$NS/$DEST" 10_nn_training_and_example_final.pptx
python3 - <<'PY'
import json, hashlib
NS='/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example'
led=json.load(open(NS+'/final_deck_ledger.json'))
p7=[p for p in led['pages'] if p['page']==7][0]
src=hashlib.md5(open(NS+'/recreated_pptx/slide_007_recreated.pptx','rb').read()).hexdigest()
print('ledger page7:', p7)
print('deliverable md5:', src)
assert p7['status']=='certified' and p7['source_md5']==src, 'LEDGER MISMATCH'
import zipfile
z=zipfile.ZipFile(NS+'/10_nn_training_and_example_final.pptx')
s=zipfile.ZipFile(NS+'/recreated_pptx/slide_007_recreated.pptx')
assert z.read('ppt/slides/slide7.xml')==s.read('ppt/slides/slide1.xml'), 'DECK XML MISMATCH'
print('deck page 7 XML == deliverable slide1.xml: OK')
print('PAGE 7 CERTIFIED AND MERGED')
PY
