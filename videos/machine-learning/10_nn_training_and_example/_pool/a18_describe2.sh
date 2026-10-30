#!/usr/bin/env bash
# scope_a18: describe diagram-region crops for slides 31 and 32 (default route)
set -u
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$SKILL" || exit 1
OUT="$VID/_pool/a18_crops"
mkdir -p "$OUT"

# crop slide 31 network diagram (top-right region)
python3 - "$OUT" <<'PY'
import sys
from PIL import Image
out = sys.argv[1]
base = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
im = Image.open(f"{base}/slide_031.jpg").convert("RGB").crop((430, 45, 850, 205))
im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
im.save(f"{out}/s31_net.png")
im2 = Image.open(f"{base}/slide_032.jpg").convert("RGB").crop((95, 85, 830, 530))
im2 = im2.resize((im2.width * 2, im2.height * 2), Image.LANCZOS)
im2.save(f"{out}/s32_full.png")
print("crops ok")
PY

Q="Report ONLY measured facts. Give me the exact pixel geometry of the neural network diagram: (1) every node circle — its center x,y and radius, its fill color and outline color, and the text inside it; (2) every connecting edge and the weight label text on it; (3) every layer label (Input/Output/Target/Bias) and the eta value with its position; (4) any target vector and its values. Be exhaustive and literal; do not comment on aesthetics."

timeout 540 python3 scripts/analyze_image.py analysis "$OUT/s31_net.png" \
  --timeout 420 --rounds 1 --tries 1 \
  --view "Zoomed crop of a neural-network diagram from a lecture slide" \
  --capture "1260x480 upscaled crop" \
  -p "$Q" > "$VID/qa/slide031/a18_net.txt" 2>&1 &
sleep 15
timeout 540 python3 scripts/analyze_image.py analysis "$OUT/s32_full.png" \
  --timeout 420 --rounds 1 --tries 1 \
  --view "Full-slide crop of a lecture slide with two panels" \
  --capture "1470x890 upscaled crop" \
  -p "$Q" > "$VID/qa/slide032/a18_net.txt" 2>&1 &
wait
echo "CROP DESCRIBE DONE"
