#!/usr/bin/env bash
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null && [ "$(stat -c %Y "$1")" -gt "$(date -d '2026-10-31 03:00' +%s)" ]; }
verd() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" 2>/dev/null | tail -1 | grep -oE 'PASS|FAIL'; }
ok=0; miss=0
for N in 018 020 021 022 023 024 026 027 028 029 030 031 032 034; do
  D=$RJ/slide$N; line="slide$N"
  for leg in judge_full_r21 crop_dense_judge_r21; do
    T=$D/$leg.txt
    if clean "$T"; then line="$line $leg=$(verd "$T")"; ok=$((ok+1));
    else line="$line $leg=MISSING"; miss=$((miss+1)); fi
  done
  echo "$line"
done
echo "SUMMARY clean=$ok missing=$miss wrappers_alive=$(ps -eo args | grep '[v]ision_leg.sh' | grep -c 'r21') occ=$(ps -eo args | grep -c '[a]nalyze_image[.]py') now=$(date -u +%FT%TZ)"
