#!/usr/bin/env bash
# r20 shard C status scan — read-only. Snapshots ps once, then checks all legs fast.
set -u
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
PSOUT=$(ps -eo args)
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
for N in 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051; do
  D=$RJ/slide$N
  for leg in full crop; do
    if [ "$leg" = full ]; then T=$D/judge_full_r20.txt; else T=$D/crop_dense_judge_r20.txt; fi
    if clean "$T"; then
      v=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$T" | tail -1 | grep -oE 'PASS|FAIL')
      echo "$N $leg: CLEAN_$v"
    elif [ -f "$T" ]; then
      if echo "$PSOUT" | grep '[v]ision_leg.sh' | grep -q "slide$N/$(basename "$T")"; then o=OWNED; else o=unowned; fi
      echo "$N $leg: unclean($(wc -c < "$T")B) $o"
    else
      if echo "$PSOUT" | grep '[v]ision_leg.sh' | grep -q "slide$N/$(basename "$T")"; then
        echo "$N $leg: in-flight"
      else
        echo "$N $leg: NO_TRANSCRIPT_NO_WRAPPER"
      fi
    fi
  done
done
echo "occ=$(echo "$PSOUT" | grep -c '[a]nalyze_image[.]py') wrappers=$(echo "$PSOUT" | grep -c '[v]ision_leg.sh') ts=$(date -u +%FT%TZ)"
