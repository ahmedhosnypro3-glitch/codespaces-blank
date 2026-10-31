#!/usr/bin/env bash
# b15: probe-then-fire loop for the slide_030 judge.
# The upstream provider 429s intermittently. A cheap probe (short wall, tiny
# prompt) tells us when a window is open; only then do we spend a judge
# attempt. Storm clause: on 429/502/504/connection error/timeout, sleep 120s.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=030
RENDER="$NS/qa/slide${N}/b15/render-1.png"
ORIG="$NS/unique_slides/slide_${N}.jpg"
PROMPT="$(cat "$NS/judge_template.txt")"
MAX_ATTEMPT=6

probe() {
  timeout 150 env VISION_SLOTS=2 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$NS/qa/slide029/render-1.png" \
    -p "Reply with the single word READY" --timeout 120 --rounds 1 --tries 1 \
    > "$NS/_pool/orphans/b15_probe.out" 2>&1
  grep -q "READY" "$NS/_pool/orphans/b15_probe.out"
}

for attempt in 4 5 6; do
  OUT="$NS/qa/slide_${N}_judge_attempt${attempt}.txt"
  for round in 1 2 3 4 5 6; do
    echo "=== probe before judge attempt $attempt round $round $(date +%F\ %T) ==="
    if probe; then
      echo "probe OK — firing judge attempt $attempt $(date +%F\ %T)"
      timeout 900 env VISION_SLOTS=2 bash "$NS/_pool/vision_gate.sh" \
        python3 "$SKILL/scripts/analyze_image.py" comparison "$RENDER" "$ORIG" \
        --view "Slide 30 recreation render vs original lecture frame" \
        --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
        -p "$PROMPT" --timeout 780 --rounds 1 --tries 1 --max-tokens 12000 > "$OUT.tmp" 2>&1
      rc=$?
      mv "$OUT.tmp" "$OUT"
      echo "judge attempt $attempt round $round rc=$rc bytes=$(wc -c < "$OUT")"
      if grep -q 'FINAL VERDICT: PASS' "$OUT"; then
        echo "b15: slide 030 judge PASS on attempt $attempt"; exit 0
      fi
      if grep -q 'FINAL VERDICT: FAIL' "$OUT"; then
        echo "b15: slide 030 judge FAIL on attempt $attempt"; exit 1
      fi
      echo "invalid transcript — storm clause sleep 120s"
    else
      echo "probe failed — storm clause sleep 120s"
    fi
    sleep 120
  done
done
echo "b15: slide 030 judge exhausted attempts 4-6 without a verdict"
exit 3
