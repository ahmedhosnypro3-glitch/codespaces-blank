#!/usr/bin/env bash
# Slide 015 — attempt-6 legA (Template A full-slide judge) on render_6.png.
# att5 legA (fresh eyes, unchanged render_4 bytes) adjudicated: 5 MAJORs refuted by
# pixel/doc-parse measurement (qa/slide_015/adjudicate_att5_*.txt), 1 REAL finding
# fixed (W of "Best W" recolored C00000 per the original's red glyph x291..310),
# 1 MINOR refuted (green-box centering margins 4.0/5.0 vs 3.4/4.0).
# Payload sourced from the frozen template shared_patterns/judge_protocol_03.md
# (Template A); md5-checked in-run. Transcript judge_attempt_6.txt (5 is banked).
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 9
DECK=videos/machine-learning/03_ridger_regression_gradient_descent

PAYLOAD=$(python3 - <<'PY'
import hashlib
p = "videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
txt = open(p, encoding="utf-8").read()
sec = txt.split("## Template A")[1].split("## Procedure B")[0]
line = [l for l in sec.splitlines() if l.lstrip().startswith('-p "GROUND RULES')]
assert len(line) == 1, f"expected 1 payload line, got {len(line)}"
payload = line[0].strip()[len('-p "'):].rstrip()
assert payload.endswith('"'), "payload does not end with quote"
payload = payload[:-1]
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
  $DECK/recreated_pptx/qa/slide_015/render_6.png \
  --view "Slide 015 recreation attempt 6 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript $DECK/recreated_pptx/qa/slide_015/probe_6.txt

LOAD=$(pgrep -c -f analyze_image.py)
echo "gate load pre-judge: $LOAD"
if [ "$LOAD" -ge 8 ]; then echo "GATE CLOSED after probe — do not dispatch judge"; exit 7; fi

# Leg A: full-slide comparison judge, frozen Template A payload verbatim
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $DECK/recreated_pptx/qa/slide_015/render_6.png \
  $DECK/unique_slides/slide_015.jpg \
  --view "Slide 015 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript $DECK/recreated_pptx/qa/slide_015/judge_attempt_6.txt \
  -p "$PAYLOAD"
echo "LEG A DONE rc=$?"
