#!/usr/bin/env bash
# Leg A — full-slide comparison judge for slide 051, attempt 3.
# Payload source: Template A, shared_patterns/judge_protocol_03.md line 71.
# Template A carries no \bK\b or slide NNN placeholder; the payload is byte-identical
# to the protocol block (md5 9387f5fbb94ef05a31db19f1e018dde1, verified against
# qa/slide051/judge_prompt_1.txt which the prior lane extracted from the same line).
#
# Walls (orchestrator override 2026-10-24, supersedes the protocol's 600):
#   analyzer --timeout 1200, inner gate 1650, outer `timeout 1700`.
# Gate check before dispatch: pgrep -c -f analyze_image.py  must be < 8.
set -u
cd "/home/ahmed/Projects/ai_llm_slides"
DECK="videos/machine-learning/03_ridger_regression_gradient_descent"
D="$DECK/recreated_pptx/qa/slide051"

# ---- gate check ----
n=$(pgrep -c -f analyze_image.py || true)
echo "[legA] $(date -u +%H:%M:%S) analyzer procs=$n"
if [ "${n:-0}" -ge 8 ]; then
  echo "[legA] GATE BUSY ($n >= 8) — refusing to dispatch. heartbeat + sleep 240."
  exit 75
fi

exec timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$D/render_3.png" \
  "$DECK/unique_slides/slide_051.jpg" \
  --view "Slide 051 recreation attempt 3 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$D/judge_attempt_3.txt" \
  -p "$(cat "$D/judge_attempt_3_promptA.txt")"
