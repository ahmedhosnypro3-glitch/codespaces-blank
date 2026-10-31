#!/usr/bin/env bash
# b15: probe-then-fire loop for the high-budget slide_029 audit re-run.
# Storm clause: probe with a short wall, fire only inside an open window; on
# 429/502/504/connection error/timeout sleep 120s and re-probe.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=029
IMG="$NS/unique_slides/slide_${N}.jpg"
OUT="$NS/_pool/audit2/slide_${N}.txt"

probe() {
  timeout 150 env VISION_SLOTS=2 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$NS/qa/slide029/render-1.png" \
    -p "Reply with the single word READY" --timeout 120 --rounds 1 --tries 1 \
    > "$NS/_pool/orphans/b15_probe2.out" 2>&1
  grep -q "READY" "$NS/_pool/orphans/b15_probe2.out"
}

for round in $(seq 1 12); do
  echo "=== probe before audit round $round $(date +%F\ %T) ==="
  if probe; then
    echo "probe OK — firing high-budget audit $(date +%F\ %T)"
    timeout 960 env VISION_SLOTS=2 bash "$NS/_pool/vision_gate.sh" \
      python3 "$SKILL/scripts/analyze_image.py" analysis "$IMG" \
      --timeout 900 --rounds 1 --tries 1 --max-tokens 24000 \
      --view "Slide $N — 'Neural Network Training and Example' lecture slide, printed badge $N" \
      --capture "960x540 CSS px, 1x scale, lecture video frame" \
      -p "$(cat "$NS/_pool/audit_prompt.txt")" > "$OUT.tmp" 2>&1
    mv "$OUT.tmp" "$OUT"
    if grep -q '\[winner\]' "$OUT" && [ "$(wc -c < "$OUT")" -ge 4000 ]; then
      if grep -q '## 1. VERBATIM TEXT' "$OUT"; then
        echo "b15: slide_029 audit OK with structured sections $(wc -c < "$OUT")B"; exit 0
      fi
      cp "$OUT" "$NS/_pool/audit2/slide_029_check_$(date +%s).txt"
      echo "b15: slide_029 audit landed without \`## 1. VERBATIM TEXT\` header — checking"
    else
      echo "attempt invalid ($(wc -c < "$OUT")B) — storm clause sleep 120s"
    fi
  else
    echo "probe failed — storm clause sleep 120s"
  fi
  sleep 120
done
echo "b15: slide_029 audit re-run gave up after 12 probe rounds"
exit 3
