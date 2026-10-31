#!/usr/bin/env bash
# b17 judge for slides 33/34: comparison mode, frozen template, through the namespace gate.
# Usage: b17_judge.sh <slide-number> <attempt>
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N="$1"; A="$2"
OUT="$NS/qa/slide0${N}/rejudge/judge_attempt_${A}.txt"
PROMPT="$(cat "$NS/judge_template.txt")"
mkdir -p "$NS/qa/slide0${N}/rejudge"
timeout 540 env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
  python3 "$SKILL/scripts/analyze_image.py" comparison \
  "$NS/qa/slide0${N}/rejudge/render-1.png" "$NS/unique_slides/slide_0${N}.jpg" \
  --view "Slide ${N} recreation render vs original lecture frame" \
  --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
  -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$OUT" 2>&1
echo "judge ${N} attempt ${A}: rc=$? bytes=$(wc -c < "$OUT") $(date +%T)"
