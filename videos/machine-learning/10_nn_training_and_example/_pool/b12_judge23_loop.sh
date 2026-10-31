#!/usr/bin/env bash
# b12 slide 23 judge — transport-storm retry (wide wall, 180s backoff).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
SK=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"
LOG=_pool/b12_wave.status
K="${1:-2}"
MAXK="${MAXK:-10}"

while [ "$K" -le "$MAXK" ]; do
  f="qa/slide023/attempt_r2/judge_023_try${K}.txt"
  ./_pool/vision_gate.sh timeout 720 python3 "$SK" comparison qa/slide023/attempt_r2/render-1.png unique_slides/slide_023.jpg \
    --view "Slide 023 recreation render vs original lecture frame" --capture "$CAP" \
    -p "$PROMPT" --timeout 600 --rounds 1 --tries 1 > "$f" 2>&1
  rc=$?
  if grep -qi "FINAL VERDICT" "$f"; then
    echo "$(date +%T) 023 try${K} VERDICT rc=$rc bytes=$(wc -c < "$f"): $(grep -i 'FINAL VERDICT' "$f" | tail -1)" >> "$LOG"
    exit 0
  fi
  echo "$(date +%T) 023 try${K} no-verdict rc=$rc bytes=$(wc -c < "$f") $(grep -oE 'HTTP [0-9]+|Connection reset|Connection aborted' "$f" | head -1)" >> "$LOG"
  K=$((K+1)); sleep 180
done
echo "$(date +%T) 023 judge exhausted tries (no verdict) — rely on banked PASS (pixel-identical bytes)" >> "$LOG"
