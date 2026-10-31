#!/usr/bin/env bash
# b04 slide 007 persistent judge loop: retries through the provider storm with 120s
# backoff. Banks the first PASS verdict. Exits after STRM retries or on a definite
# non-blocker FAIL verdict.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
LOG="$NS/_pool/b04/judge_007_loop.log"
echo "loop start $(date +%F\ %T)" >> "$LOG"

for attempt in $(seq 1 14); do
  OUT="$NS/qa/slide007/rejudge/judge_r8_attempt_${attempt}.txt"
  echo "=== attempt $attempt $(date +%F\ %T) ===" >> "$LOG"
  env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" python3 "$SKILL" comparison \
    "$NS/_pool/b04/render2/s7a7-1.jpg" "$NS/unique_slides/slide_007.jpg" \
    --view "Slide 007 recreation render (attempt-7 fix) vs original lecture frame (fresh audit 2026-10-30, scope b04)" \
    --capture "IMG1=150dpi JPEG render (2001x1125) of slide_007_attempt7.pptx; IMG2=original lecture frame 960x540" \
    --timeout 240 --rounds 1 --tries 1 -p "$(cat "$NS/judge_template.txt")" > "$OUT" 2>&1
  rc=$?
  if grep -q "FINAL VERDICT: PASS" "$OUT" 2>/dev/null; then
    echo "PASS attempt $attempt rc=$rc $(date +%F\ %T)" >> "$LOG"
    exit 0
  fi
  if grep -qiE "HTTP (429|502|504|400)|timed out|Timeout|deadline|ConnectionResetError|Connection aborted|RemoteDisconnected|rejected the request|HangError|empty content" "$OUT" 2>/dev/null; then
    echo "storm attempt $attempt rc=$rc $(date +%F\ %T); backoff 120s" >> "$LOG"
    sleep 120
    continue
  fi
  echo "VERDICATED attempt $attempt rc=$rc $(date +%F\ %T)" >> "$LOG"
  exit 1
done
echo "loop exhausted $(date +%F\ %T)" >> "$LOG"
exit 2
