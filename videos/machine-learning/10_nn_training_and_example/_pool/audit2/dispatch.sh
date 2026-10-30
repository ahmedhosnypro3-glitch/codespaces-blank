#!/usr/bin/env bash
# Audit wave 2 dispatcher: re-analyze all 34 slides with the image-analysis
# script as background bash tasks (xargs pool through the namespace vision
# gate). Unbuilt slides first so builds can start ASAP, then already-built.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
D="$NS/_pool/audit2"
mkdir -p "$D"
LOG="$D/run.log"
ORDER="1 2 3 4 6 9 10 11 12 13 14 15 16 17 18 24 25 26 27 28 30 31 32 33 34 5 7 8 19 20 21 22 23 29"
echo "=== audit wave2 start $(date +%F\ %T) slots=3 xargs=4 ===" >> "$LOG"
echo $ORDER | tr ' ' '\n' | xargs -P 4 -I{} bash "$D/run_one.sh" {}
echo "=== audit wave2 done $(date +%F\ %T) ===" >> "$LOG"
ok=0; bad=0
for f in "$D"/slide_*.txt; do
  if grep -q '\[winner\]' "$f" && [ "$(wc -c < "$f")" -ge 4000 ]; then ok=$((ok+1)); else bad=$((bad+1)); fi
done
echo "=== audit wave2 tally ok=$ok bad=$bad $(date +%F\ %T) ===" >> "$LOG"
