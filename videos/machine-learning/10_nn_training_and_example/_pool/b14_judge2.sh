#!/usr/bin/env bash
# b14 judge runner: protocol recipe (--timeout 420 inside timeout 540) through the
# namespace gate, retried until a real FINAL VERDICT lands (storm clause: sleep 120).
# usage: b14_judge2.sh <first_attempt> N1 [N2 ...]
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
PROMPT="$(cat judge_template.txt)"
A0="${1:-1}"; shift || true
LOG="$NS/_pool/logs_b14/judge_run.log"
mkdir -p "$NS/_pool/logs_b14"

verdict_ok() { [ -f "$1" ] && grep -qaE "FINAL VERDICT: ?\*{0,2}(PASS|FAIL)" "$1"; }

for N in "$@"; do
  PNN=$(printf "%03d" "$N")
  D="$NS/qa/slide${PNN}/b14"
  mkdir -p "$D"
  a="$A0"
  while [ "$a" -le 6 ]; do
    OUT="$D/judge_attempt_${a}.txt"
    if verdict_ok "$OUT"; then
      echo "$(date '+%F %T') slide $PNN attempt $a already banked with verdict" >> "$LOG"
      break
    fi
    echo "$(date '+%F %T') slide $PNN attempt $a start" >> "$LOG"
    TMPDIR="$NS/_pool" timeout 700 bash /home/codespace/ai_llm_slides/scripts/16_vision_gate.sh \
      python3 "$TOOL" comparison "$D/render-1.png" "$NS/unique_slides/slide_${PNN}.jpg" \
      --view "Slide ${PNN} recreation render vs original lecture frame" \
      --capture "13.33x7.5in slide, 150dpi render (2000x1125px) vs 960x540px original frame" \
      -p "$PROMPT" --timeout 620 --rounds 1 --tries 1 > "$OUT" 2>&1
    rc=$?
    echo "$(date '+%F %T') slide $PNN attempt $a exit=$rc bytes=$(wc -c < "$OUT")" >> "$LOG"
    if verdict_ok "$OUT"; then
      echo "$(date '+%F %T') slide $PNN attempt $a VERDICT BANKED" >> "$LOG"
      break
    fi
    a=$((a + 1))
    sleep 120
  done
done
echo "$(date '+%F %T') b14 judge run complete" >> "$LOG"
