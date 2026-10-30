#!/bin/bash
# Slide 014 — attempt-8 legA (Template A full-slide judge). Orchestrator-authorized
# att8 for the parked att7 slide: the three REAL att7 fixes (bold underlined X,
# 14pt labels, Define-Loss underlines) are in the build and verified on render_8.
# Payload = banked payload_A_7.txt, byte-identical to the frozen Template A
# (md5 9387f5fbb94ef05a31db19f1e018dde1, verified against shared_patterns/judge_protocol_03.md).
# Transcript judge_attempt_8.txt; judge_attempt_7.txt is banked evidence, never overwritten.
cd /home/ahmed/Projects/ai_llm_slides || exit 9
LOAD=$(pgrep -c -f analyze_image.py); echo "gate load: $LOAD"
[ "$LOAD" -lt 8 ] || { echo "GATE CLOSED"; exit 7; }
bash scripts/16_vision_gate.sh timeout 1700 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/render_8.png videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg --view "Slide 014 recreation attempt 8 — fidelity check vs original lecture frame" --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/judge_attempt_8.txt -p "$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/payload_A_7.txt)"
echo "LEG A DONE rc=$?"
