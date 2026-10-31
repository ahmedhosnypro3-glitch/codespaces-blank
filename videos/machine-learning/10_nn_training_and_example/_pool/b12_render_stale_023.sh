#!/usr/bin/env bash
# Evidence-only render: the stale slide-023 deliverable byte-stream
# (md5 30e1e450) vs the certified bytes (md5 742a2f58, ledger source_md5).
# Writes to a dedicated evidence dir; never touches qa/slide023/rejudge/.
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
Q="$NS/qa/slide023/evidence_stale_deliverable"
PPTX="$NS/recreated_pptx/slide_023_recreated.pptx"
mkdir -p "$Q" "$NS/_pool/lo_b12_stale"
cp "$PPTX" "$NS/_pool/b12_stale_023.pptx"
TMPDIR="$NS/_pool" soffice --headless \
  -env:UserInstallation=file://$NS/_pool/lo_b12_stale \
  --convert-to pdf --outdir "$Q" "$NS/_pool/b12_stale_023.pptx" >/dev/null 2>&1
mv "$Q/b12_stale_023.pdf" "$Q/slide_023_stale_deliverable.pdf" 2>/dev/null || true
pdftoppm -png -r 150 "$Q/slide_023_stale_deliverable.pdf" "$Q/render_stale"
python3 - "$Q" <<'PY'
import sys, glob
from PIL import Image, ImageChops
import numpy as np
q = sys.argv[1]
stale = sorted(glob.glob(q + "/render_stale*.png"))
cert = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/qa/slide023/rejudge/render-1.png"
a = Image.open(stale[0]).convert("RGB")
b = Image.open(cert).convert("RGB")
print("stale render:", a.size, " certified render:", b.size)
if a.size == b.size:
    d = np.array(ImageChops.difference(a, b))
    diff = int((d.sum(axis=2) > 0).sum())
    print("differing pixels:", diff, "of", a.size[0] * a.size[1])
    ys, xs = np.where(d.sum(axis=2) > 0)
    if len(ys):
        print("diff bbox x", xs.min(), "-", xs.max(), " y", ys.min(), "-", ys.max())
else:
    print("SIZE MISMATCH - not directly comparable")
PY
