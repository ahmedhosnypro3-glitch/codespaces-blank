#!/usr/bin/env bash
# b16 judge launcher: fresh comparison judge for one slide through the namespace gate.
# Usage: b16_judge.sh <slide-number> <attempt>
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=$(printf '%03d' "$1")
ATT="${2:-1}"
RENDER="${3:-$NS/qa/slide${N}/b16/render-1.png}"
OUT="$NS/qa/slide${N}/b16_judge_attempt_${ATT}.txt"
LOG="$NS/_pool/b16_logs/judge_${N}_${ATT}.log"
PROMPT="$(cat "$NS/judge_template.txt")"

cd "$NS"
echo "start $(date +%F\ %T) render=$RENDER" >> "$LOG"
VISION_SLOTS=2 timeout 3000 bash "$NS/_pool/vision_gate.sh" timeout 2900 \
  python3 "$SKILL/scripts/analyze_image.py" comparison "$RENDER" \
  "$NS/unique_slides/slide_${N}.jpg" \
  --view "Slide $N recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original lecture-video frame" \
  -p "$PROMPT" --timeout 2400 --rounds 1 --tries 1 > "$OUT" 2>&1
rc=$?
echo "done rc=$rc bytes=$(wc -c < "$OUT") $(date +%F\ %T)" >> "$LOG"
