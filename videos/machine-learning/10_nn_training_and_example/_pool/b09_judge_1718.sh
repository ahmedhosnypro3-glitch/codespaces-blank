#!/usr/bin/env bash
# b09 fresh judge dispatch: slide 17 (attempt2 render, pixel-identical to the
# previously PASSed attempt1 render) then slide 18 (current deliverable render).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/.agents/skills/image-analysis
cd "$NS" || exit 1
PROMPT="$(cat "$NS/judge_template.txt")"

judge() { # $1=N $2=IMG1 $3=OUT
  local N="$1" IMG1="$2" OUT="$3"
  timeout 600 ./_pool/vision_gate.sh timeout 540 \
    python3 "$SKILL/scripts/analyze_image.py" comparison "$IMG1" "unique_slides/slide_$(printf '%03d' "$N").jpg" \
    --view "Slide $(printf '%03d' "$N") recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$OUT" 2>&1
  echo "judge $N rc=$? bytes=$(wc -c < "$OUT") $(date +%T)"
}

judge 17 "$NS/qa/slide017/rejudge/attempt2/render-1.png" "$NS/qa/slide017/rejudge/judge_attempt_3.txt" &
wait
echo "ALL DONE $(date +%T)"
