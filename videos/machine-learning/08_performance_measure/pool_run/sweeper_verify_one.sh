#!/usr/bin/env bash
# sweeper_verify_one.sh <N> <attempt> <render_relpath> — corroboration (verify) judge
# for one slide whose attempt PASSed on a fresh render. ORIGINAL first (IMG1).
# Sleeps 90-150s before the call; on 429/infra failure sleeps 300s and retries
# (max 8 attempts). Transcript name is unique: judge_verify_<attempt>_sw<epoch>.txt
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
REPO="/home/codespace/ai_llm_slides"
PYBIN="/home/codespace/.pyenv/versions/3.15.2/bin/python3"
N="$1"; ATT="$2"; RENDER="$3"
PAD=$(printf '%03d' "$N")
QA="$NS/recreated_pptx/qa/slide$PAD"
LOG="$NS/pool_run/verify_sw_${N}.log"
log() { echo "[$(date '+%F %T')] slide $N sw-verify: $*" >>"$LOG"; }

ORIG=""
for f in "$NS/unique_slides/slide_${PAD}.jpg" "$NS/unique_slides/slide_${PAD}"-*.jpg; do
  [ -f "$f" ] && { ORIG="$f"; break; }
done
[ -n "$ORIG" ] || { log "FATAL original frame not found"; exit 1; }
[ -f "$NS/$RENDER" ] || { log "FATAL render missing: $RENDER"; exit 1; }

TS=$(date +%s)
VERIFY="$QA/judge_verify_${ATT}_sw${TS}.txt"

s=$((90 + RANDOM % 61))
log "pre-call sleep ${s}s (attempt=$ATT render=$RENDER transcript=$(basename "$VERIFY"))"
sleep "$s"

for i in $(seq 1 8); do
  log "gateway call attempt $i/8 (timeout 540)"
  OUT=$(cd "$REPO" && bash scripts/16_vision_gate.sh timeout 540 "$PYBIN" \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison "$ORIG" "$NS/$RENDER" \
    --view "Slide $N recreation — INDEPENDENT corroboration read vs original lecture frame" \
    --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of a 13.33x7.5in PPTX recreation (read second)" \
    --thinking high --max-tokens 65536 \
    --timeout 420 --rounds 1 --tries 1 \
    --transcript "$VERIFY" \
    -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" 2>&1)
  rc=$?
  echo "$OUT" >>"$LOG"
  if [ -s "$VERIFY" ] && grep -qi 'FINAL VERDICT:' "$VERIFY"; then
    v=$(grep -oi 'FINAL VERDICT: *PASS\|FINAL VERDICT: *FAIL' "$VERIFY" | tail -1)
    log "attempt $i rc=$rc verdict='$v' transcript=$(basename "$VERIFY")"
    exit 0
  fi
  log "attempt $i rc=$rc no verdict (429/infra?) — sleeping 300s before retry"
  sleep 300
done
log "gave up after 8 attempts"
exit 1
