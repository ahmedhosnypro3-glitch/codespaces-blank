#!/usr/bin/env bash
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide025
LOG=$D/watch_k15.log
verdict() {
  local f newest=""
  for f in $(ls -t $D/$1 2>/dev/null | grep -v -E '\.(bak|log|wrapper\.out)$'); do newest=$f; break; done
  [ -z "$newest" ] && return
  local v c429
  v=$(grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$newest" 2>/dev/null | tail -1 | grep -oE '(PASS|FAIL)$')
  c429=$(grep -ci 429 "$newest" 2>/dev/null); c429=${c429:-0}
  echo "$(stat -c %Y "$newest")|$v|$c429|$(basename $newest)"
}
echo "watch3 start $(date -u +%FT%TZ)" >> $LOG
for i in $(seq 1 55); do
  sleep 60
  RM=$(md5sum $D/render.png 2>/dev/null | cut -d' ' -f1); RMT=$(stat -c %Y $D/render.png 2>/dev/null)
  F=$(verdict 'judge_full_k*.txt'); C=$(verdict 'crop_dense_judge_k*.txt')
  OCC=$(ps -eo args | grep -c '[a]nalyze_image[.]py')
  echo "$(date -u +%FT%TZ) render=$RM mtime=$RMT full=[$F] crop=[$C] occ=$OCC" >> $LOG
  FMT=$(echo "$F" | cut -d'|' -f1); FV=$(echo "$F" | cut -d'|' -f2); F429=$(echo "$F" | cut -d'|' -f3)
  CMT=$(echo "$C" | cut -d'|' -f1); CV=$(echo "$C" | cut -d'|' -f2); C429=$(echo "$C" | cut -d'|' -f3)
  if [ "$FV" = PASS ] && [ "$CV" = PASS ] && [ "$F429" = 0 ] && [ "$C429" = 0 ] && [ "$FMT" -ge "$RMT" ] && [ "$CMT" -ge "$RMT" ]; then
    echo "$(date -u +%FT%TZ) CERTIFIABLE render=$RM full=$F crop=$C" >> $LOG; exit 0
  fi
done
echo "$(date -u +%FT%TZ) WATCH3_TIMEOUT" >> $LOG; exit 1
