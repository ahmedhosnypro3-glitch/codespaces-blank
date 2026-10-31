#!/usr/bin/env bash
# r21 shard C poller — checks 035-049 for clean r21 transcripts; logs status.
set -u
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r21_shardC_poll.log
{
echo "POLL $(date -u +%FT%TZ)"
for N in 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049; do
  D=$RJ/slide$N
  f=$D/judge_full_r21.txt; c=$D/crop_dense_judge_r21.txt
  fs=pending; cs=pending
  if [ -f "$f" ]; then
    if grep -q 'FINAL VERDICT' "$f" 2>/dev/null && ! grep -qi '429' "$f"; then
      fs=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)$')
      fs="$fs($(stat -c %y "$f" | cut -d. -f1))"
    else fs="dirty/429($(stat -c %y "$f" 2>/dev/null | cut -d. -f1))"; fi
  fi
  if [ -f "$c" ]; then
    if grep -q 'FINAL VERDICT' "$c" 2>/dev/null && ! grep -qi '429' "$c"; then
      cs=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$c" | tail -1 | grep -oE '(PASS|FAIL)$')
      cs="$cs($(stat -c %y "$c" | cut -d. -f1))"
    else cs="dirty/429($(stat -c %y "$c" 2>/dev/null | cut -d. -f1))"; fi
  fi
  echo "$N full=$fs crop=$cs"
done
echo "live r21 wrappers: $(ps -eo args | grep '[v]ision_leg.sh' | grep -c 'r21.txt')"
} >> "$LOG"
tail -40 "$LOG"
