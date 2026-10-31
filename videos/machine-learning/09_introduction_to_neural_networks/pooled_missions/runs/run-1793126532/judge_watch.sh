#!/usr/bin/env bash
# Judge watcher v7 - ONE slide, runs FOREVER, re-judges automatically whenever
# the promoted pptx is newer than the banked verdict. This closes the
# fix -> re-judge loop without orchestrator intervention.
# Usage: judge_watch_NNN.sh <slide>
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks
B=$V/recreated_pptx/build
TPL=$B/judge_template_v2.txt
IMG=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
RUN=$V/pooled_missions/runs/run-1793126532
GATE=$RUN/vision_gate_fair.sh
export TMPDIR=/home/codespace/ai_llm_slides/scratch/tmp
mkdir -p "$TMPDIR"
n="$1"; n3=$(printf '%03d' "$((10#$n))")
LANE=w$n3
LOG=$RUN/judge_watch_${n3}.log
LOCKS=$RUN/locks
mkdir -p "$LOCKS"
log(){ echo "$(date +%F\ %T) [$LANE] $*" >> "$LOG"; }
probe(){ curl -s -m 10 -o /dev/null -w '%{http_code}' http://localhost:17844/v1/models 2>/dev/null; }
has_verdict(){ f="$1"; [ -s "$f" ] && grep -q 'FINAL VERDICT' "$f" 2>/dev/null; }
verdict_current(){ f="$1"; p="$2"
  has_verdict "$f" || return 1
  [ -f "$p" ] || return 0
  fm=$(stat -c%Y "$f" 2>/dev/null || echo 0); pm=$(stat -c%Y "$p" 2>/dev/null || echo 0)
  [ "$fm" -ge "$pm" ]
}
pick_render(){
  cands=$(ls -t $B/slide_${n3}*rendered*.png 2>/dev/null | grep -v _resized)
  for c in $cands; do case "$c" in *_rejudge_rendered*|*_wave4_rendered*) echo "$c"; return 0;; esac; done
  echo "$cands" | head -1
}
relay=$V/recreated_pptx/qa/slide$n3/judge_re_${n3}_relay.txt
std=$V/recreated_pptx/qa/slide$n3/judge_re_${n3}.txt
promoted=$V/recreated_pptx/slide_${n3}_recreated.pptx
log "WATCH START slide$n3"
while true; do
  if verdict_current "$relay" "$promoted" || verdict_current "$std" "$promoted"; then
    sleep 45; continue
  fi
  lock=$LOCKS/slide${n3}.lock
  mkdir "$lock" 2>/dev/null || { sleep 30; continue; }
  r=$(pick_render)
  case "$(basename "${r:-none}")" in
    slide_${n3}_rendered*|slide_${n3}_rejudge_rendered*|slide_${n3}_wave4_rendered*) ;;
    *) log "slide$n3 NO_RENDER"; rmdir "$lock" 2>/dev/null; sleep 60; continue;;
  esac
  c=$B/judge_${n3}_context.txt
  [ -s "$c" ] || { log "slide$n3 NO_CONTEXT"; rmdir "$lock" 2>/dev/null; sleep 60; continue; }
  python3 - "$r" <<'PY'
import sys
from PIL import Image
w,h = Image.open(sys.argv[1]).size
sys.exit(0 if (w>=1500 and h>=800) else 1)
PY
  [ $? -eq 0 ] || { log "slide$n3 RENDER_BAD"; rmdir "$lock" 2>/dev/null; sleep 60; continue; }
  code=$(probe)
  case "$code" in 2*|3*|4*|5*) ;; *) log "slide$n3 GW_DOWN($code)"; rmdir "$lock" 2>/dev/null; sleep 90; continue;; esac
  mkdir -p "$(dirname "$relay")"
  mark=$V/recreated_pptx/qa/slide$n3/.judge_inflight
  echo $$ > "$mark"
  log "slide$n3 START $(basename "$r")"
  tmp=$relay.tmp.$$
  GATE_WAIT=180 timeout 2700 bash "$GATE" python3 "$IMG" comparison "$r" "$V/unique_slides/slide_${n3}.jpg" \
    --timeout 300 --rounds 1 --tries 1 --max-tokens 16000 \
    --view "judge slide $n" --capture "recreated render first, original frame second" \
    -p "$(cat "$TPL"; cat "$c")" > "$tmp" 2>&1
  rc=$?; sz=$(stat -c%s "$tmp" 2>/dev/null || echo 0)
  rm -f "$mark"
  if [ "$rc" -eq 75 ]; then
    rm -f "$tmp"; log "slide$n3 NO_SLOT"; rmdir "$lock" 2>/dev/null; sleep 45; continue
  fi
  if grep -qi '429\|rate limit\|too many requests' "$tmp" 2>/dev/null; then
    cp -f "$tmp" "$relay.lastfail" 2>/dev/null; rm -f "$tmp"
    log "slide$n3 RATE_LIMITED sz=$sz"; rmdir "$lock" 2>/dev/null; sleep 60; continue
  fi
  if grep -q 'FINAL VERDICT' "$tmp" 2>/dev/null && [ "$sz" -ge 1500 ]; then
    mv -f "$tmp" "$relay"
    v=$(grep -ao 'FINAL VERDICT[^A-Z]\{0,4\}[A-Z]\+' "$relay" | tail -1 | tr -d '*' | sed 's/.*VERDICT//;s/^[[:space:]]*//')
    log "slide$n3 VERDICT sz=$sz :: $v"
  else
    cp -f "$tmp" "$relay.lastfail" 2>/dev/null; rm -f "$tmp"
    log "slide$n3 FAIL rc=$rc sz=$sz"
  fi
  rmdir "$lock" 2>/dev/null
  sleep 20
done
