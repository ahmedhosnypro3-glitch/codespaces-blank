#!/usr/bin/env bash
# Slide 015 — attempt-5 legA (Template A full-slide judge) on UNCHANGED bytes.
# Resume of the att4 park (qa/slide_015/worker_report.md appendix 3): the fresh-eyes
# re-dispatch the orchestrator ordered. Payload sourced from the frozen template
# shared_patterns/judge_protocol_03.md (Template A); md5-checked in-run.
# Transcript judge_attempt_5.txt — judge_attempt_4.txt (att4's refuted 3rd verdict)
# is banked evidence and is never overwritten.
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 9
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
PROTO=$DECK/shared_patterns/judge_protocol_03.md
QA=$DECK/recreated_pptx/qa/slide_015

PAYLOAD=$(python3 - <<'PY'
import re, hashlib
p = "videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
txt = open(p, encoding="utf-8").read()
sec = txt.split("## Template A")[1].split("## Procedure B")[0]
line = [l for l in sec.splitlines() if l.lstrip().startswith('-p "GROUND RULES')]
assert len(line) == 1, f"expected 1 payload line, got {len(line)}"
payload = line[0].strip()[len('-p "'):].rstrip()
assert payload.endswith('"'), "payload does not end with quote"
payload = payload[:-1]
assert "NNN" not in payload and "BLOCKER" in payload
h = hashlib.md5(payload.encode()).hexdigest()
print(payload)
import sys
print(f"payload_md5={h} chars={len(payload)}", file=sys.stderr)
assert h == "9387f5fbb94ef05a31db19f1e018dde1", f"payload md5 mismatch: {h}"
PY
) || { echo "PAYLOAD EXTRACTION FAILED"; exit 8; }

LOAD=$(pgrep -c -f analyze_image.py)
echo "gate load pre-probe: $LOAD"
if [ "$LOAD" -ge 8 ]; then echo "GATE CLOSED — do not dispatch"; exit 7; fi

# Probe (opens the window; protocol Template A step 1)
scripts/16_vision_gate.sh timeout 150 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  $DECK/recreated_pptx/qa/slide_015/render_4.png \
  --view "Slide 015 recreation attempt 5 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript $DECK/recreated_pptx/qa/slide_015/probe_5.txt

LOAD=$(pgrep -c -f analyze_image.py)
echo "gate load pre-judge: $LOAD"
if [ "$LOAD" -ge 8 ]; then echo "GATE CLOSED after probe — do not dispatch judge"; exit 7; fi

# Leg A: full-slide comparison judge, frozen Template A payload verbatim
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $DECK/recreated_pptx/qa/slide_015/render_4.png \
  $DECK/unique_slides/slide_015.jpg \
  --view "Slide 015 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript $DECK/recreated_pptx/qa/slide_015/judge_attempt_5.txt \
  -p "$PAYLOAD"
echo "LEG A DONE rc=$?"
