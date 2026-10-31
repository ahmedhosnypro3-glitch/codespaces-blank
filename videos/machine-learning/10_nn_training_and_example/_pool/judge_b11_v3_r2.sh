#!/usr/bin/env bash
# Judge v3 renders for b11 (slides 21, 22) — SEQUENTIAL so they do not compete
# with each other for the 4-slot namespace gate. Wide wall per W4 doctrine:
# --timeout 900 inside timeout 960. Frozen template verbatim, default route.
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example || exit 1
AI=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$(cat judge_template.txt)"
LOG=$PWD/_pool/orphans/judge_b11_v3_r2.out
N=${1:-3}

for s in 21 22; do
  N3=$(printf '%03d' "$s")
  OUT="qa/slide${N3}/rejudge/judge_attempt_${N}.txt"
  echo "=== slide $N3 start $(date +%F\ %T) -> $OUT" >> "$LOG"
  ./_pool/vision_gate.sh timeout 960 python3 "$AI" \
    comparison "qa/slide${N3}/rejudge/v3/render-1.png" "unique_slides/slide_${N3}.jpg" \
    --view "Slide ${N3} recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 900 --rounds 1 --tries 1 > "$OUT" 2>&1
  echo "=== slide $N3 rc=$? bytes=$(wc -c < "$OUT") $(date +%F\ %T)" >> "$LOG"
  grep -h "FINAL VERDICT" "$OUT" >> "$LOG" 2>/dev/null
done
echo "=== b11 judge r2 done $(date +%F\ %T)" >> "$LOG"
