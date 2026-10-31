#!/usr/bin/env bash
# Judge relay lane v2 - parallel-safe: per-lane log, in-flight marker so two
# lanes never burn a call on the same slide, atomic verdict write.
# Usage: judge_relay_lane2.sh <lane-id> <slide> [slide ...]
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks
B=$V/recreated_pptx/build
TPL=$B/judge_template.txt
IMG=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
GATE=/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh
RUN=$V/pooled_missions/runs/run-1793126532
LANE="$1"; shift
LOG=$RUN/judge_relay_${LANE}.log
mkdir -p "$(dirname "$LOG")"
log(){ echo "$(date +%F\ %T) [$LANE] $*" >> "$LOG"; }
probe(){ curl -s -m 10 -o /dev/null -w '%{http_code}' http://localhost:17844/v1/models 2>/dev/null; }
has_verdict(){ f="$1"; [ -s "$f" ] && grep -q 'FINAL VERDICT' "$f" 2>/dev/null; }

pick_render(){
  n3=$(printf "%03d" "$1")
  cands=$(ls -t $B/slide_${n3}*rendered*.png 2>/dev/null | grep -v _resized)
  for c in $cands; do
    case "$c" in *_rejudge_rendered*) echo "$c"; return 0;; esac
  done
  echo "$cands" | head -1
}

relay_one(){
  n="$1"; n3=$(printf "%03d" "$n")
  relay=$V/recreated_pptx/qa/slide$n/judge_re_${n3}_relay.txt
  std=$V/recreated_pptx/qa/slide$n/judge_re_${n3}.txt
  has_verdict "$relay" && { log "slide$n SKIP relay-verdict"; return 0; }
  has_verdict "$std" && { log "slide$n SKIP worker-verdict"; return 0; }
  mark=$V/recreated_pptx/qa/slide$n/.judge_inflight
  if [ -f "$mark" ]; then
    other=$(cat "$mark" 2>/dev/null)
    if [ -n "$other" ] && kill -0 "$other" 2>/dev/null; then
      log "slide$n SKIP in-flight(pid=$other)"; return 0
    fi
  fi
  r=$(pick_render "$n"); [ -n "$r" ] || { log "slide$n NO_RENDER"; return 0; }
  c=$B/judge_${n3}_context.txt
  [ -s "$c" ] || { log "slide$n NO_CONTEXT"; return 0; }
  python3 - "$r" <<'PY'
import sys
from PIL import Image
w,h = Image.open(sys.argv[1]).size
sys.exit(0 if (w>=1500 and h>=800) else 1)
PY
  [ $? -eq 0 ] || { log "slide$n RENDER_BAD dims"; return 0; }
  code=$(probe)
  case "$code" in 2*|3*|4*|5*) ;; *) log "slide$n GW_DOWN($code) backoff"; sleep 120; return 0;; esac
  mkdir -p "$(dirname "$relay")"
  echo $$ > "$mark"
  log "slide$n START $(basename "$r") ctx=$(stat -c%s "$c")"
  tmp=$relay.tmp.$$
  timeout 900 bash "$GATE" python3 "$IMG" comparison "$r" "$V/unique_slides/slide_${n3}.jpg" \
    --timeout 420 --rounds 1 --tries 1 --max-tokens 16000 \
    --view "judge slide $n" --capture "recreated render first, original frame second" \
    -p "$(cat "$TPL"; cat "$c")" > "$tmp" 2>&1
  rc=$?; sz=$(stat -c%s "$tmp" 2>/dev/null || echo 0)
  rm -f "$mark"
  if grep -q 'FINAL VERDICT' "$tmp" 2>/dev/null && [ "$sz" -ge 1500 ]; then
    mv -f "$tmp" "$relay"
    v=$(grep -o 'FINAL VERDICT[:]* *\**[A-Z]*' "$relay" | tail -1 | sed 's/[* ]*$//')
    log "slide$n VERDICT rc=$rc sz=$sz :: $v"
  else
    cp -f "$tmp" "$relay.lastfail" 2>/dev/null
    log "slide$n FAIL rc=$rc sz=$sz"
    rm -f "$tmp"
  fi
  sleep 5
}
SLIDES="$*"; log "JUDGE RELAY v2 START: $SLIDES"
todo="$SLIDES"
for pass in 1 2 3 4 5 6 7 8; do
  todo=""
  for n in $SLIDES; do relay_one "$n"; done
  for n in $SLIDES; do
    rp=$V/recreated_pptx/qa/slide$n/judge_re_$(printf "%03d" "$n")_relay.txt
    sp=$V/recreated_pptx/qa/slide$n/judge_re_$(printf "%03d" "$n").txt
    has_verdict "$rp" || has_verdict "$sp" || todo="$todo $n"
  done
  [ -z "${todo// }" ] && { log "ALL DONE"; break; }
  log "pass$pass remaining:$todo - sleeping 240"; sleep 240
done
log "JUDGE RELAY v2 EXIT remaining:$todo"
