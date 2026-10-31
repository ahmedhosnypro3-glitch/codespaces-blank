#!/usr/bin/env bash
# Judge relay lane v6 - fair-slot gate acquisition + VERDICT FRESHNESS.
# A banked verdict only counts if it is at least as new as the promoted pptx
# (mtimes compared), so a slide that was rebuilt after its FAIL gets re-judged
# instead of being skipped on a stale verdict.
# Usage: judge_relay_lane6.sh <lane-id> <slide> [slide ...]
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks
B=$V/recreated_pptx/build
TPL=$B/judge_template_v2.txt
IMG=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
RUN=$V/pooled_missions/runs/run-1793126532
GATE=$RUN/vision_gate_fair.sh
DB=/home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh
MDB=$V/pooled_missions/mission.db
LANE="$1"; shift
LOG=$RUN/judge_relay_${LANE}.log
LOCKS=$RUN/locks
mkdir -p "$LOCKS" "$(dirname "$LOG")"
log(){ echo "$(date +%F\ %T) [$LANE] $*" >> "$LOG"; }
probe(){ curl -s -m 10 -o /dev/null -w '%{http_code}' http://localhost:17844/v1/models 2>/dev/null; }
has_verdict(){ f="$1"; [ -s "$f" ] && grep -q 'FINAL VERDICT' "$f" 2>/dev/null; }

# verdict counts only if no pptx exists yet, or verdict mtime >= pptx mtime
verdict_current(){ f="$1"; p="$2"
  has_verdict "$f" || return 1
  [ -f "$p" ] || return 0
  fm=$(stat -c%Y "$f" 2>/dev/null || echo 0); pm=$(stat -c%Y "$p" 2>/dev/null || echo 0)
  [ "$fm" -ge "$pm" ]
}

pick_render(){
  n="$1"; n3=$(printf '%03d' "$((10#$n))")
  cands=$(ls -t $B/slide_${n3}*rendered*.png 2>/dev/null | grep -v _resized)
  for c in $cands; do
    case "$c" in *_rejudge_rendered*|*_wave4_rendered*) echo "$c"; return 0;; esac
  done
  echo "$cands" | head -1
}

relay_one(){
  n="$1"; n3=$(printf '%03d' "$((10#$n))")
  relay=$V/recreated_pptx/qa/slide$n/judge_re_${n3}_relay.txt
  std=$V/recreated_pptx/qa/slide$n/judge_re_${n3}.txt
  promoted=$V/recreated_pptx/slide_${n3}_recreated.pptx
  verdict_current "$relay" "$promoted" && { log "slide$n SKIP current-verdict"; return 0; }
  verdict_current "$std" "$promoted" && { log "slide$n SKIP current-worker-verdict"; return 0; }
  mark=$V/recreated_pptx/qa/slide$n/.judge_inflight
  if [ -f "$mark" ]; then
    other=$(cat "$mark" 2>/dev/null)
    if [ -n "$other" ] && kill -0 "$other" 2>/dev/null; then
      log "slide$n SKIP in-flight(pid=$other)"; return 0
    fi
  fi
  lock=$LOCKS/slide${n3}.lock
  if ! mkdir "$lock" 2>/dev/null; then
    log "slide$n SKIP locked"; return 0
  fi
  r=$(pick_render "$n")
  case "$(basename "$r")" in slide_${n3}_rendered*|slide_${n3}_rejudge_rendered*|slide_${n3}_wave4_rendered*) ;; *) log "slide$n NO_RENDER/$(basename "${r:-none}")"; rmdir "$lock" 2>/dev/null; return 0;; esac
  [ -s "$r" ] || { log "slide$n NO_RENDER"; rmdir "$lock" 2>/dev/null; return 0; }
  c=$B/judge_${n3}_context.txt
  [ -s "$c" ] || { log "slide$n NO_CONTEXT"; rmdir "$lock" 2>/dev/null; return 0; }
  python3 - "$r" <<'PY'
import sys
from PIL import Image
w,h = Image.open(sys.argv[1]).size
sys.exit(0 if (w>=1500 and h>=800) else 1)
PY
  [ $? -eq 0 ] || { log "slide$n RENDER_BAD dims"; rmdir "$lock" 2>/dev/null; return 0; }
  code=$(probe)
  case "$code" in 2*|3*|4*|5*) ;; *) log "slide$n GW_DOWN($code)"; rmdir "$lock" 2>/dev/null; sleep 90; return 0;; esac
  mkdir -p "$(dirname "$relay")"
  echo $$ > "$mark"
  log "slide$n START $(basename "$r") ctx=$(stat -c%s "$c")"
  tmp=$relay.tmp.$$
  GATE_WAIT=180 timeout 2700 bash "$GATE" python3 "$IMG" comparison "$r" "$V/unique_slides/slide_${n3}.jpg" \
    --timeout 300 --rounds 1 --tries 1 --max-tokens 16000 \
    --view "judge slide $n" --capture "recreated render first, original frame second" \
    -p "$(cat "$TPL"; cat "$c")" > "$tmp" 2>&1
  rc=$?; sz=$(stat -c%s "$tmp" 2>/dev/null || echo 0)
  rm -f "$mark"
  if [ "$rc" -eq 75 ]; then
    rm -f "$tmp"; log "slide$n NO_SLOT (gate saturated)"; rmdir "$lock" 2>/dev/null; sleep 60; return 0
  fi
  if grep -qi '429\|rate limit\|too many requests' "$tmp" 2>/dev/null; then
    cp -f "$tmp" "$relay.lastfail" 2>/dev/null; rm -f "$tmp"
    log "slide$n RATE_LIMITED sz=$sz"; rmdir "$lock" 2>/dev/null; sleep 120; return 0
  fi
  if grep -q 'FINAL VERDICT' "$tmp" 2>/dev/null && [ "$sz" -ge 1500 ]; then
    mv -f "$tmp" "$relay"
    v=$(grep -o 'FINAL VERDICT[^A-Z]*[A-Z]\+' "$relay" | tail -1 | tr -d '*' | sed 's/[[:space:]]*$//')
    log "slide$n VERDICT rc=$rc sz=$sz :: $v"
  else
    cp -f "$tmp" "$relay.lastfail" 2>/dev/null
    log "slide$n FAIL rc=$rc sz=$sz"
    rm -f "$tmp"
  fi
  rmdir "$lock" 2>/dev/null
  sleep 5
}
SLIDES="$*"; log "JUDGE RELAY v6 START: $SLIDES"
todo=""
for pass in $(seq 1 60); do
  todo=""
  for n in $SLIDES; do relay_one "$n"; done
  for n in $SLIDES; do
    rp=$V/recreated_pptx/qa/slide$n/judge_re_$(printf '%03d' "$((10#$n))")_relay.txt
    sp=$V/recreated_pptx/qa/slide$n/judge_re_$(printf '%03d' "$((10#$n))").txt
    pr=$V/recreated_pptx/slide_$(printf '%03d' "$((10#$n))")_recreated.pptx
    verdict_current "$rp" "$pr" || verdict_current "$sp" "$pr" || todo="$todo $n"
  done
  if [ -z "${todo// /}" ]; then log "ALL DONE"; break; fi
  log "pass$pass remaining:$todo - sleeping 60"; sleep 60
done
log "JUDGE RELAY v6 EXIT remaining:$todo"
