#!/usr/bin/env bash
# b12 slide 24 judge — transport-storm retry (wider wall, 180s backoff).
# Continues the attempt counter; a verdict (FINAL VERDICT line) ends the loop.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
SK=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"
LOG=_pool/b12_wave.status
K="${1:-7}"
MAXK="${MAXK:-14}"

while [ "$K" -le "$MAXK" ]; do
  f="qa/slide024/attempt4/judge_024_try${K}.txt"
  ./_pool/vision_gate.sh timeout 720 python3 "$SK" comparison qa/slide024/attempt4/render-1.png unique_slides/slide_024.jpg \
    --view "Slide 024 recreation render vs original lecture frame" --capture "$CAP" \
    -p "$PROMPT" --timeout 600 --rounds 1 --tries 1 > "$f" 2>&1
  rc=$?
  if grep -qi "FINAL VERDICT" "$f"; then
    echo "$(date +%T) 024 try${K} VERDICT rc=$rc bytes=$(wc -c < "$f"): $(grep -i 'FINAL VERDICT' "$f" | tail -1)" >> "$LOG"
    exit 0
  fi
  echo "$(date +%T) 024 try${K} no-verdict rc=$rc bytes=$(wc -c < "$f") $(grep -oE 'HTTP [0-9]+|Connection reset|Connection aborted' "$f" | head -1)" >> "$LOG"
  K=$((K+1)); sleep 180
done
echo "$(date +%T) 024 judge exhausted tries (no verdict) — PARK" >> "$LOG"
