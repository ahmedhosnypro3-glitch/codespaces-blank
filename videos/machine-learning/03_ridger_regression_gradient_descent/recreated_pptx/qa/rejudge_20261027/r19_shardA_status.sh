#!/usr/bin/env bash
# r19 shard A status: per slide/leg clean verdicts + live wrapper count.
set -u
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
cd "$RJ"
echo "=== $(date -u +%FT%TZ) occ=$(ps -eo args | grep -c '[a]nalyze_image[.]py') r19_wrappers=$(ps -eo args | grep '[v]ision_leg.sh' | grep -c r19)"
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 015 016 017 018; do
  D=slide$N
  line="$N:"
  for t in judge_full_r19.txt crop_dense_judge_r19.txt; do
    if [ -f "$D/$t" ] && grep -q 'FINAL VERDICT' "$D/$t" 2>/dev/null && ! grep -qi '429' "$D/$t" 2>/dev/null; then
      v=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$D/$t" | tail -1 | grep -oE '(PASS|FAIL)$')
      line="$line ${t%%_r19*}=$v"
    else
      line="$line ${t%%_r19*}=."
    fi
  done
  echo "$line"
done
