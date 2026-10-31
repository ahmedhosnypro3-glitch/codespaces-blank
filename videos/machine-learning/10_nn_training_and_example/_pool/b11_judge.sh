#!/usr/bin/env bash
# b11 judge of v3 renders (slides 21, 22) — frozen template verbatim.
# Arg order per frozen template: image1 = recreation render, image2 = original.
# Sequential (not parallel) so the two do not compete for gate slots.
# Storm clause: Connection error / 429 / 502 / 504 / timeout -> sleep 120, retry 3x.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
AI=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
LOG=_pool/orphans/b11_judge_v3.out

storm() {
  grep -qiE 'Connection error|Connection aborted|ConnectionReset|HTTP 429|HTTP 502|HTTP 503|HTTP 504|timed out|timeout|HangError' "$1"
}
valid() { grep -q 'FINAL VERDICT' "$1" 2>/dev/null; }

for s in 021 022; do
  R="qa/slide${s}/rejudge/v3/render-1.png"
  O="unique_slides/slide_${s}.jpg"
  MAXA=6
  for a in $(seq 1 $MAXA); do
    OUT="qa/slide${s}/rejudge/judge_attempt_${a}.txt"
    echo "=== slide ${s} attempt ${a} $(date +%F\ %T)" >> "$LOG"
    env VISION_SLOTS=3 bash _pool/vision_gate.sh timeout 960 python3 "$AI" \
      comparison "$R" "$O" \
      --view "Slide ${s} recreation render (v3) vs original lecture frame" \
      --capture "IMG1=13.33x7.5in slide 150dpi render (2000x1125px); IMG2=960x540px original frame" \
      -p "$PROMPT" --timeout 900 --rounds 1 --tries 1 > "$OUT.tmp" 2>&1
    mv "$OUT.tmp" "$OUT"
    echo "    rc done bytes=$(wc -c < "$OUT")" >> "$LOG"
    if valid "$OUT"; then
      grep -h "FINAL VERDICT" "$OUT" >> "$LOG"
      echo "=== slide ${s} VERDICT banked on attempt ${a}" >> "$LOG"
      break
    fi
    if storm "$OUT" && [ "$a" -lt 4 ]; then
      echo "    storm -> sleep 120" >> "$LOG"
      sleep 120
    elif [ "$a" -lt 4 ]; then
      echo "    no verdict -> sleep 60" >> "$LOG"
      sleep 60
    else
      echo "=== slide ${s} NO VERDICT after ${a} attempts" >> "$LOG"
    fi
  done
done
