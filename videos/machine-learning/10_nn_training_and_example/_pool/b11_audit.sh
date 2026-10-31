#!/usr/bin/env bash
# b11 wave-2 audits for slides 21 and 22 — sequential, one call each,
# namespace vision gate, storm clause (120s sleep, up to 3 retries).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
LOG=_pool/audit2/run.log

for s in 021 022; do
  OUT="_pool/audit2/slide_${s}.txt"
  for try in 1 2 3 4; do
    if grep -q '\[winner\]' "$OUT" 2>/dev/null && \
       [ "$(wc -c < "$OUT" 2>/dev/null || echo 0)" -ge 4000 ]; then
      echo "slide $s: valid transcript $(wc -c < "$OUT")B — skip" >> "$LOG"
      break
    fi
    echo "slide $s: audit try $try $(date +%F\ %T)" >> "$LOG"
    env VISION_SLOTS=3 bash _pool/vision_gate.sh \
      python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
      analysis "unique_slides/slide_${s}.jpg" \
      --view "Slide ${s} — 'Neural Network Training and Example' lecture slide, printed badge ${s}" \
      --capture "960x540 CSS px, 1x scale, lecture video frame" \
      --timeout 900 --rounds 1 --tries 1 \
      -p "$(cat _pool/audit_prompt.txt)" > "$OUT.tmp" 2>&1
    mv "$OUT.tmp" "$OUT"
    if grep -q '\[winner\]' "$OUT" && [ "$(wc -c < "$OUT")" -ge 4000 ]; then
      echo "slide $s: audit OK $(wc -c < "$OUT")B $(date +%F\ %T)" >> "$LOG"
      break
    fi
    if grep -qiE 'Connection error|HTTP 429|HTTP 502|HTTP 504|timeout|HangError|Connection reset' "$OUT"; then
      echo "slide $s: provider storm on try $try — sleep 120s" >> "$LOG"
      sleep 120
    else
      echo "slide $s: invalid transcript on try $try — sleep 30s" >> "$LOG"
      sleep 30
    fi
  done
done
echo "=== b11 audit done $(date +%F\ %T) ===" >> "$LOG"
