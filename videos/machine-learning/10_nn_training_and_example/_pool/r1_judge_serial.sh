#!/usr/bin/env bash
# Serial judge retry driver (protocol cap: <=2 concurrent per call; 1 = safest).
# usage: r1_judge_serial.sh <attempt> <NNN> <NNN> ...
set -u
A="$1"; shift
VD=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
for N in "$@"; do
  echo "=== attempt ${A}: slide ${N} start $(date -u +%H:%M:%S) ==="
  R1_ATTEMPT="$A" bash "$VD/_pool/r1_judge.sh" "$N" || echo "driver rc=$? for $N"
  F="$VD/qa/slide${N}/rejudge/judge_attempt_${A}.txt"
  echo "--- slide ${N} ($(stat -c%s "$F" 2>/dev/null || echo 0) bytes) ---"
  tail -3 "$F" 2>/dev/null
  echo "=== attempt ${A}: slide ${N} end $(date -u +%H:%M:%S) ==="
done
echo "=== serial attempt ${A} complete ==="
