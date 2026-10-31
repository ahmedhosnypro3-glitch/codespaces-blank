#!/usr/bin/env bash
# Self-healing orchestrator re-analysis lane. Foreign sessions saturate the shared
# gateway, so every call is short-walled with the script's own abort+retry, and the
# lane loops until every target slide has a real transcript.
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks
IMG=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
GATE=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/pooled_missions/runs/run-1793126532/vision_gate_fair.sh
OUT="$V/analysis/reanalysis_v2"
LOG="$V/pooled_missions/runs/run-1793126532/reanalysis_lane.log"
mkdir -p "$OUT"
log(){ echo "$(date +%F\ %T) $*" >> "$LOG"; }
probe(){ curl -s -m 10 -o /dev/null -w '%{http_code}' http://localhost:17844/v1/models 2>/dev/null; }
ok(){
  f="$OUT/slide_${1}_reanalysis.txt"
  [ "$(stat -c%s "$f" 2>/dev/null || echo 0)" -ge 3000 ] && grep -q '^\[winner\]' "$f" 2>/dev/null
}
run_one(){
  n="$1"
  ok "$n" && { log "slide_$n SKIP"; return; }
  [ -f "$V/unique_slides/slide_${n}.jpg" ] || { log "slide_$n NO_IMAGE"; return; }
  c=$(probe)
  case "$c" in 2*|3*|4*|5*) ;; *) log "slide_$n GW_DOWN($c) sleep"; sleep 60 ;; esac
  tmp="$OUT/slide_${n}_reanalysis.tmp.$$"
  timeout 900 env GATE_WAIT=180 bash "$GATE" python3 "$IMG" analysis "$V/unique_slides/slide_${n}.jpg" \
    --timeout 300 --rounds 2 --tries 1 --max-tokens 16000 \
    --view "slide $n — original lecture frame, 09_introduction_to_neural_networks" \
    --capture "960x540 lecture slide frame, original" \
    -p "$(cat "$V/recreated_pptx/build/reanalyze_prompt.md")" > "$tmp" 2>&1
  if [ "$(stat -c%s "$tmp" 2>/dev/null || echo 0)" -ge 3000 ] && grep -q '^\[winner\]' "$tmp"; then
    mv "$tmp" "$OUT/slide_${n}_reanalysis.txt"
    log "slide_$n DONE($(stat -c%s "$OUT/slide_${n}_reanalysis.txt"))"
  else
    cp "$tmp" "$OUT/slide_${n}_reanalysis.lastfail.txt"
    log "slide_$n FAIL(sz=$(stat -c%s "$tmp" 2>/dev/null || echo 0))"
  fi
}
SLIDES="$*"; log "LANE START: $SLIDES"
for pass in 1 2 3 4 5 6 7 8; do
  todo=""
  for n in $SLIDES; do ok "$n" || todo="$todo $n"; done
  [ -z "${todo// }" ] && { log "ALL DONE (pass $pass)"; break; }
  log "pass$pass todo:$todo"
  i=0
  for n in $todo; do run_one "$n" & i=$((i+1)); [ $((i % 3)) -eq 0 ] && wait; done
  wait
  sleep 15
done
log "LANE EXIT"
