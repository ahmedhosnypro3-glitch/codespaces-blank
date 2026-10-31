#!/usr/bin/env bash
# b11 audit + judge queue, fully serial so the namespace gate never fights itself.
# Phase 1: audits for 021 and 022. Phase 2: judges for the v3 renders.
# Storm clause: 429/502/504/conn/timeout -> sleep 120, up to 3 retries.
# Audits may be retried beyond that (other scopes are also hitting the gateway);
# judges stop at their per-slide cap of 6 attempts.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
AI=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
LOG=_pool/orphans/b11_queue.out
AP="$(cat _pool/audit_prompt.txt)"
JP="$(cat judge_template.txt)"

audit_ok() { grep -q '\[winner\]' "$1" 2>/dev/null && [ "$(wc -c < "$1" 2>/dev/null || echo 0)" -ge 4000 ]; }
storm() { grep -qiE 'Connection error|Connection aborted|ConnectionReset|HTTP 429|HTTP 502|HTTP 503|HTTP 504|timed out|timeout|HangError|ServiceTimeout' "$1"; }

for s in 021 022; do
  OUT="_pool/audit2/slide_${s}.txt"
  try=0
  while ! audit_ok "$OUT"; do
    try=$((try+1))
    echo "=== AUDIT slide ${s} try ${try} $(date +%F\ %T)" >> "$LOG"
    env VISION_SLOTS=3 bash _pool/vision_gate.sh timeout 1080 python3 "$AI" \
      analysis "unique_slides/slide_${s}.jpg" \
      --view "Slide ${s} — 'Neural Network Training and Example' lecture slide, printed badge ${s}" \
      --capture "960x540 CSS px, 1x scale, lecture video frame" \
      --timeout 900 --rounds 1 --tries 1 -p "$AP" > "$OUT.tmp" 2>&1
    mv "$OUT.tmp" "$OUT"
    echo "    bytes=$(wc -c < "$OUT")" >> "$LOG"
    if audit_ok "$OUT"; then echo "    AUDIT slide ${s} OK $(date +%F\ %T)" >> "$LOG"; break; fi
    echo "    reason: $(grep -iE 'HTTP |Connection|timed out|HangError|degenerate|analyzed successfully' "$OUT" | tail -2 | tr '\n' ' ')" >> "$LOG"
    if storm "$OUT"; then echo "    storm -> sleep 120" >> "$LOG"; sleep 120
    else echo "    non-storm -> sleep 30" >> "$LOG"; sleep 30; fi
    if [ "$try" -ge 10 ]; then echo "    AUDIT slide ${s} GAVE UP after ${try} tries" >> "$LOG"; break; fi
  done
done

for s in 021 022; do
  R="qa/slide${s}/rejudge/v3/render-1.png"
  O="unique_slides/slide_${s}.jpg"
  for a in $(seq 1 6); do
    OUT="qa/slide${s}/rejudge/judge_attempt_${a}.txt"
    echo "=== JUDGE slide ${s} attempt ${a} $(date +%F\ %T)" >> "$LOG"
    env VISION_SLOTS=3 bash _pool/vision_gate.sh timeout 1080 python3 "$AI" \
      comparison "$R" "$O" \
      --view "Slide ${s} recreation render (v3) vs original lecture frame" \
      --capture "IMG1=13.33x7.5in slide 150dpi render (2000x1125px); IMG2=960x540px original frame" \
      -p "$JP" --timeout 900 --rounds 1 --tries 1 > "$OUT.tmp" 2>&1
    mv "$OUT.tmp" "$OUT"
    echo "    bytes=$(wc -c < "$OUT")" >> "$LOG"
    if grep -q 'FINAL VERDICT' "$OUT"; then
      echo "    VERDICT: $(grep 'FINAL VERDICT' "$OUT" | head -1)" >> "$LOG"
      break
    fi
    if storm "$OUT" && [ "$a" -lt 4 ]; then echo "    storm -> sleep 120" >> "$LOG"; sleep 120
    elif [ "$a" -lt 4 ]; then echo "    -> sleep 60" >> "$LOG"; sleep 60; fi
  done
done
echo "=== b11 queue done $(date +%F\ %T) ===" >> "$LOG"
