#!/usr/bin/env bash
# b12 judge retry loop: slides 23 and 24, up to MAXA attempts each, 120s apart.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
SK=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"
MAXA="${MAXA:-6}"
S23="${S23:-qa/slide023/attempt_r2}"; S24="${S24:-qa/slide024/attempt4}"
LOG=_pool/b12_retry.status

one() { # $1=tag $2=render $3=orig $4=outdir
  local tag=$1 render=$2 orig=$3 out=$4 k=1
  while [ $k -le $MAXA ]; do
    local f="$out/judge_${tag}_try${k}.txt"
    ./_pool/vision_gate.sh timeout 540 python3 "$SK" comparison "$render" "$orig" \
      --view "Slide ${tag} recreation render vs original lecture frame" --capture "$CAP" \
      -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$f" 2>&1
    local rc=$?
    if grep -qi "FINAL VERDICT" "$f"; then
      echo "$(date +%T) ${tag} try${k} VERDICT rc=$rc bytes=$(wc -c < "$f"): $(grep -i 'FINAL VERDICT' "$f" | tail -1)" >> "$LOG"
      return 0
    fi
    echo "$(date +%T) ${tag} try${k} no-verdict rc=$rc bytes=$(wc -c < "$f")" >> "$LOG"
    k=$((k+1)); [ $k -le $MAXA ] && sleep 120
  done
  return 1
}

echo "=== retry loop start $(date +%T) MAXA=$MAXA ===" >> "$LOG"
one 023 "$S23/render-1.png" unique_slides/slide_023.jpg "$S23" &
sleep 15
one 024 "$S24/render-1.png" unique_slides/slide_024.jpg "$S24" &
wait
echo "=== retry loop done $(date +%T) ===" >> "$LOG"
