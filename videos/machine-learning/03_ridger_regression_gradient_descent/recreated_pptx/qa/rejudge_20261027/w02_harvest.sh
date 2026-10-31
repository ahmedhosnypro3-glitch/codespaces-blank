#!/usr/bin/env bash
# w02_harvest.sh — snapshot any W02-scope transcript that has a FINAL VERDICT before a
# vision_leg.sh retry can rm -f it. Banks to <name>.W02bank (first writer wins per mtime check).
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT"
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/driver_W02_harvest.log
SLIDES="018 019 023 024 026 029 030 031 032 033 034"
while true; do
  for s in $SLIDES; do
    D=$RJ/slide$s
    for f in judge_full.txt crop_dense_judge.txt; do
      p=$D/$f; b=$D/$f.W02bank
      if [ -f "$p" ] && grep -q 'FINAL VERDICT' "$p" 2>/dev/null; then
        if [ ! -f "$b" ] || [ "$p" -nt "$b" ]; then
          cp "$p" "$b"
          v=$(grep -oE 'FINAL VERDICT: *\** *(PASS|FAIL)' "$b" | tail -1)
          has429=$(grep -ci 429 "$b" || true)
          echo "$(date -u +%FT%TZ) banked slide$s/$f -> W02bank: $v 429lines=$has429" >> "$LOG"
        fi
      fi
    done
  done
  sleep 15
done
