#!/usr/bin/env bash
# r21 shard A status: freshness of the 6 r21 targets + live wrapper ownership.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
THRESH=1793415600
for spec in 009:crop 010:full 010:crop 011:full 016:full 016:crop; do
  N=${spec%%:*}; kind=${spec##*:}
  D=$RJ/slide$N
  if [ "$kind" = full ]; then T=$D/judge_full_r21.txt; else T=$D/crop_dense_judge_r21.txt; fi
  if [ -f "$T" ]; then
    mt=$(stat -c %Y "$T")
    verdict=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$T" | tail -1)
    n429=$(grep -ci '429' "$T" || true)
    fresh=no; [ "$mt" -gt "$THRESH" ] && [ -n "$verdict" ] && [ "$n429" -eq 0 ] && fresh=YES
    echo "$N $kind: $fresh mt=$(date -u -d @$mt +%FT%TZ) 429=$n429 verdict='$verdict'"
  else
    echo "$N $kind: NO FILE"
  fi
done
echo "live r21 wrappers: $(ps -eo args | grep '[v]ision_leg.sh' | grep -c 'r21')"
echo "occ analyze_image.py: $(ps -eo args | grep -c '[a]nalyze_image[.]py')"
date -u +%FT%TZ
