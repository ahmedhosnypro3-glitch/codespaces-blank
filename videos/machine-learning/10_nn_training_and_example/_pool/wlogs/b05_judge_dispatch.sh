#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
PROMPT="$(cat "$NS/judge_template.txt")"
run_one() {
  local n="$1" render="$2" out="$3"
  timeout 540 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" comparison "$render" "$NS/unique_slides/slide_0${n}.jpg" \
    --view "Slide 0${n} recreation render vs original lecture frame (b05 attempt)" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  echo "slide $n rc=$? bytes=$(wc -c < "$out") $(date +%T)"
}
run_one 10 "$NS/qa/slide010/b05/render-1.png" "$NS/qa/slide010/b05/judge_attempt_1.txt" &
sleep 15
run_one 9 "$NS/qa/slide009/b05/render-1.png" "$NS/qa/slide009/b05/judge_attempt_1.txt" &
wait
echo "JUDGE DISPATCH DONE $(date +%T)"
