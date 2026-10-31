#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
PROMPT="$(cat "$NS/judge_template.txt")"
LOG="$NS/_pool/wlogs/b05_judge9_resilient.log"
for cycle in 1 2 3 4 5 6; do
  out="$NS/qa/slide009/b05/judge_attempt_c${cycle}.txt"
  echo "cycle $cycle start $(date +%T)" >> "$LOG"
  timeout 700 env VISION_SLOTS=10 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" comparison \
    "$NS/qa/slide009/b05/render-1.png" "$NS/unique_slides/slide_009.jpg" \
    --view "Slide 009 recreation render vs original lecture frame (b05 attempt)" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 600 --rounds 1 --tries 1 > "$out" 2>&1
  rc=$?
  echo "cycle $cycle rc=$rc bytes=$(wc -c < "$out") $(date +%T)" >> "$LOG"
  if grep -q "FINAL VERDICT" "$out"; then echo "VERDICT FOUND cycle $cycle" >> "$LOG"; exit 0; fi
  sleep 180
done
echo "ALL CYCLES EXHAUSTED $(date +%T)" >> "$LOG"
