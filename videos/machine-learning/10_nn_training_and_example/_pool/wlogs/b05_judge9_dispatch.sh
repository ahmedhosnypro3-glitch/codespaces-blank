#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
PROMPT="$(cat "$NS/judge_template.txt")"
run_one() {
  local out="$1"
  timeout 540 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" comparison "$NS/qa/slide009/b05/render-1.png" "$NS/unique_slides/slide_009.jpg" \
    --view "Slide 009 recreation render vs original lecture frame (b05 attempt)" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  echo "$out rc=$? bytes=$(wc -c < "$out") $(date +%T)"
}
run_one "$NS/qa/slide009/b05/judge_attempt_2.txt" &
sleep 15
run_one "$NS/qa/slide009/b05/judge_attempt_3.txt" &
wait
echo "JUDGE9 DISPATCH DONE $(date +%T)"
