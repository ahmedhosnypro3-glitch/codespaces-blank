#!/bin/bash
# render_031.sh  <pptx> <out.png>  — LibreOffice -> PDF (300dpi) -> PNG
set -e
IN="$1"; OUT="$2"
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
mkdir -p "$TMPDIR"
WORK="$TMPDIR/render_031_$$"
mkdir -p "$WORK"
timeout 600 soffice --headless --norestore --convert-to pdf --outdir "$WORK" "$IN" >/dev/null 2>&1
PDF=$(ls "$WORK"/*.pdf | head -1)
pdftoppm -r 300 -png -singlefile "$PDF" "$WORK/out"
RESIZE=$(python3 -c "import sys;print(max(1,int(round(300*w/960)))" 2>/dev/null || echo "")
# write 2001x1125 (150dpi-equivalent scale 2.084)
python3 - "$WORK/out.png" "$OUT" <<'PY'
import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('RGB')
print("raw",im.size)
im2=im.resize((2001,1125), Image.LANCZOS)
im2.save(sys.argv[2])
print("wrote",sys.argv[2],im2.size)
PY
