#!/usr/bin/env bash
# b04 slide 007 re-judge: attempt-7 fix render (JPEG) vs original, frozen template.
# Storm clause: 429/502/504/400-rejected/transport reset/timeout -> sleep 120s, retry up to 3x.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS"
PROMPT="$(cat judge_template.txt)"
IMG1="$NS/_pool/b04/render2/s7a7-1.jpg"
'rm' -f "$NS/qa/slide007/rejudge/judge_r7_attempt_1.txt"
for attempt in 1 2 3 4; do
  OUT="$NS/qa/slide007/rejudge/judge_r7_attempt_${attempt}.txt"
  echo "=== judge slide007 attempt $attempt $(date +%F\ %T) ===" >> "$NS/_pool/b04/judge_007_r7.log"
  env VISION_SLOTS=3 bash _pool/vision_gate.sh python3 "$SKILL" comparison \
    "$IMG1" "$NS/unique_slides/slide_007.jpg" \
    --view "Slide 007 recreation render (attempt-7 fix) vs original lecture frame (fresh audit 2026-10-30, scope b04)" \
    --capture "IMG1=150dpi JPEG render (2001x1125) of slide_007_attempt7.pptx; IMG2=original lecture frame 960x540" \
    --timeout 240 --rounds 1 --tries 1 -p "$PROMPT" > "$OUT" 2>&1
  rc=$?
  if grep -q "FINAL VERDICT: PASS" "$OUT" 2>/dev/null; then
    echo "PASS banked attempt $attempt rc=$rc $(date +%F\ %T)" >> "$NS/_pool/b04/judge_007_r7.log"
    exit 0
  fi
  if grep -qiE "HTTP (429|502|504|400)|timed out|Timeout|deadline|ConnectionResetError|Connection aborted|RemoteDisconnected|rejected the request" "$OUT" 2>/dev/null; then
    echo "storm/transport attempt $attempt rc=$rc; sleep 120 then retry" >> "$NS/_pool/b04/judge_007_r7.log"
    sleep 120
    continue
  fi
  echo "judge verdict attempt $attempt rc=$rc $(date +%F\ %T)" >> "$NS/_pool/b04/judge_007_r7.log"
  exit 1
done
echo "exhausted storm retries $(date +%F\ %T)" >> "$NS/_pool/b04/judge_007_r7.log"
exit 2
