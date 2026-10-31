#!/usr/bin/env bash
# Detached single-slide parse-verification cross-check runner (retry pass).
# $1 = slide number (e.g. 008), $2 = absolute path to the prompt file.
# Kill-capable outer timeout: `timeout --kill-after` reaps a wedged python child.
set -u
N="$1"; PROMPT="$2"
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/analysis/parse/adjudication/vision
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
if [ -s "$V/slide_$N.vision.txt" ] && grep -q 'result(s) analyzed successfully' "$V/slide_$N.vision.txt"; then
  echo "SKIP_$N ok" >> "$V/run_status2.log"
  exit 0
fi
mv "$V/slide_$N.vision.txt" "$V/prior_attempts/slide_$N.failed1.txt" 2>/dev/null || true
mkdir -p "$V/prior_attempts"
VISION_SLOTS=2 ./_pool/vision_gate.sh timeout --kill-after=45 700 python3 -u \
  /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
  analysis "$V/png/slide_$N.png" \
  --view "Slide $N - original lecture frame, parse-verification cross-check retry" \
  --capture "960x540 px, scale 1, video frame" \
  -p "$(cat "$PROMPT")" \
  --timeout 240 --rounds 3 --tries 3 --max-tokens 24000 \
  > "$V/slide_$N.vision.txt" 2>&1
echo "EXIT2_$N=$?" >> "$V/run_status2.log"
