#!/usr/bin/env bash
# Backup verify-wing for slide 5 (redundant second leg; agent-196 runs the primary).
# Corroboration judge: original FIRST, newest render SECOND. Banks judge_verify_8.txt.
# Random 90-150s pre-sleep; on 429/empty/HangError/no-verdict sleep 300s, retry up to 8x.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
REPO=/home/codespace/ai_llm_slides
QA=$NS/recreated_pptx/qa/slide005
VERIFY=$QA/judge_verify_8.txt
LOG=$NS/pool_run/verify_wing_s5_backup.log
ORIG=$NS/unique_slides/slide_005.jpg
RENDER=$QA/render_7.png

log() { echo "[$(date '+%F %T')] s5-backup: $*" >>"$LOG"; }

[ -f "$ORIG" ] || { log "FATAL original missing: $ORIG"; exit 1; }
[ -f "$RENDER" ] || { log "FATAL render missing: $RENDER"; exit 1; }

s=$((90 + RANDOM % 61))
log "pre-call sleep ${s}s (verify=judge_verify_8.txt render=render_7.png)"
sleep "$s"

for i in $(seq 1 8); do
  log "=== backup-wing attempt $i/8 start $(date -u '+%FT%TZ') ==="
  echo "=== backup-wing attempt $i/8 start $(date -u '+%FT%TZ'); random pre-sleep ${s}s ===" >>"$VERIFY"
  ( cd "$REPO" && python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$ORIG" "$RENDER" \
      --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
      -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" ) >>"$VERIFY" 2>&1
  rc=$?
  log "attempt $i rc=$rc transcript_bytes=$(wc -c <"$VERIFY")"
  if grep -q 'FINAL VERDICT:' "$VERIFY"; then
    v=$(grep -oi 'FINAL VERDICT: *PASS\|FINAL VERDICT: *FAIL' "$VERIFY" | tail -1)
    log "attempt $i verdict='$v' — done"
    echo "VERDICT=$v" >>"$LOG"
    exit 0
  fi
  if grep -qiE '429|too many requests|rate.?limit|HangError|EmptyStreamError|empty content' "$VERIFY"; then
    log "attempt $i infra (429/empty/hang) — sleep 300s then retry"
  else
    log "attempt $i no verdict rc=$rc — sleep 300s then retry"
  fi
  sleep 300
done
log "exhausted 8 attempts without a verdict"
echo "EXHAUSTED" >>"$LOG"
exit 1
