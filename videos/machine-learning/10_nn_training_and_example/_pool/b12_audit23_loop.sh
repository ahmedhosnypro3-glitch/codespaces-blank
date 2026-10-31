#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
LOG=_pool/b12_wave.status
K=1
while [ $K -le 8 ]; do
  bash "$NS/_pool/audit2/run_one.sh" 23
  f=_pool/audit2/slide_023.txt
  if grep -q "\[winner\]" "$f" && [ "$(wc -c < "$f")" -ge 4000 ]; then
    echo "$(date +%T) audit023 OK bytes=$(wc -c < "$f")" >> "$LOG"; exit 0
  fi
  echo "$(date +%T) audit023 try${K} invalid bytes=$(wc -c < "$f")" >> "$LOG"
  K=$((K+1)); sleep 150
done
echo "$(date +%T) audit023 exhausted — certified analysis stands" >> "$LOG"
