#!/usr/bin/env bash
# b15: regenerate the wave-2 audit transcript for ONE slide.
# Storm clause: on Connection error / 429 / 502 / 504 / timeout, sleep 120s
# and retry up to 3x before declaring failure.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=$(printf '%03d' "$((10#$1))")
IMG="$NS/unique_slides/slide_${N}.jpg"
OUT="$NS/_pool/audit2/slide_${N}.txt"
KEEP="$NS/_pool/audit2/slide_${N}.txt"

valid() { grep -q '\[winner\]' "$OUT" 2>/dev/null && [ "$(wc -c < "$OUT" 2>/dev/null || echo 0)" -ge 4000 ]; }

for try in 1 2 3; do
  echo "=== slide $N audit try $try $(date +%F\ %T) ==="
  timeout 960 env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$IMG" \
    --timeout 900 --rounds 1 --tries 1 \
    --view "Slide $N — 'Neural Network Training and Example' lecture slide, printed badge $N" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    -p "$(cat "$NS/_pool/audit_prompt.txt")" > "$OUT.tmp" 2>&1
  rc=$?
  mv "$OUT.tmp" "$OUT"
  if valid; then echo "slide $N audit try $try OK $(wc -c < "$OUT")B"; exit 0; fi
  echo "slide $N audit try $try rc=$rc bytes=$(wc -c < "$OUT") invalid"
  if grep -Eiq "Connection error|ConnectionReset|Connection aborted|HTTP 429|429|502|504|ServiceTimeout|EmptyStreamError|timed out|Timeout" "$OUT"; then
    if [ "$try" -lt 3 ]; then echo "slide $N: provider storm on try $try — sleep 120s"; sleep 120; continue; fi
  fi
  break
done
echo "slide $N audit FINAL bytes=$(wc -c < "$OUT") $(date +%F\ %T)"
exit 3
