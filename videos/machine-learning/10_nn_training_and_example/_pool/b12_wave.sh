#!/usr/bin/env bash
# b12: fresh audit for slide 23 (wave-2 left a 429 stub), then judge 23 and 24 attempt4.
# Retry policy: storm clause — sleep 120s between attempts, MAXA tries each phase.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
SK=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"
LOG=_pool/b12_wave.status
MAXA="${MAXA:-6}"

judge() { # $1=tag $2=render $3=orig $4=outdir
  local tag=$1 render=$2 orig=$3 out=$4 k=1
  while [ $k -le $MAXA ]; do
    local f="$out/judge_${tag}_try${k}.txt"
    ./_pool/vision_gate.sh timeout 540 python3 "$SK" comparison "$render" "$orig" \
      --view "Slide ${tag} recreation render vs original lecture frame" --capture "$CAP" \
      -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$f" 2>&1
    local rc=$?
    if grep -qi "FINAL VERDICT" "$f"; then
      echo "$(date +%T) ${tag} try${k} VERDICT rc=$rc bytes=$(wc -c < "$f"): $(grep -i 'FINAL VERDICT' "$f" | tail -1)" >> "$LOG"; return 0
    fi
    echo "$(date +%T) ${tag} try${k} no-verdict rc=$rc bytes=$(wc -c < "$f") $(grep -o 'HTTP 4[0-9][0-9]' "$f" | head -1)" >> "$LOG"
    k=$((k+1)); [ $k -le $MAXA ] && sleep 120
  done
  return 1
}

echo "=== b12 wave start $(date +%T) MAXA=$MAXA ===" >> "$LOG"
bash "$NS/_pool/audit2/run_one.sh" 23
judge 023 qa/slide023/attempt_r2/render-1.png unique_slides/slide_023.jpg qa/slide023/attempt_r2 &
sleep 15
judge 024 qa/slide024/attempt4/render-1.png unique_slides/slide_024.jpg qa/slide024/attempt4 &
wait
echo "=== b12 wave done $(date +%T) ===" >> "$LOG"
