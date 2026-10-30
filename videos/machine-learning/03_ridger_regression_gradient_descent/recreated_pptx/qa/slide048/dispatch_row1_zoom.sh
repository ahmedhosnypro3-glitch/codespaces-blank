#!/usr/bin/env bash
# 048 row-1 right-side structure inspection — analysis mode, single zoomed image.
# Resolves the dashed-vertical role + bracket-pair structure handoff left open.
set -u
cd "/home/ahmed/Projects/ai_llm_slides"
DECK="videos/machine-learning/03_ridger_regression_gradient_descent"
D="$DECK/recreated_pptx/qa/slide048"

n=$(pgrep -c -f analyze_image.py || true)
echo "[row1zoom] $(date -u +%H:%M:%S) analyzer procs=$n"
if [ "${n:-0}" -ge 8 ]; then echo "[row1zoom] GATE BUSY"; exit 75; fi

PROMPT='You are inspecting a 5x Lanczos upscale of region x600..815 y140..200 (original slide space) from a lecture frame. The region contains the right side of one calculation row of a perceptron-update table. Prior evidence: a wide glyph at x618..627 (word), "=" bars at x631..636, a tall solid stroke x666 y163..183, a red plus at x676, small glyphs x687..701, dashed verticals at x713..715 (y152..192, dashed ~9-on/7-off), strokes at x707..708 and x720..721, "=" bars at x729..733, small strokes x749..757, a red leftwards double-arrow at x785..799. Prior transcription attempt read the row as: W = (4;-2;-2) + 1*(1;1;1) = (5;-1;-1) followed by a red left arrow.

Answer these EXACTLY:
1. Read the full expression left to right, verbatim, with every glyph you can see (operators, digits, signs, subscripts).
2. How many bracket/parenthesis pairs are visible? For each: x-position (approx), whether it is ( ), [ ], or { }, its height (tall multi-row vs small), and whether the stroke is SOLID or DASHED/DOTTED.
3. The dashed vertical line(s): exactly where, and what role — separator between table cells? part of a tall bracket? a dotted rule? nothing but a glyph edge artifact?
4. Which glyphs are RED, and what is each red glyph?
5. Any horizontal bars/underlines or semicolons: list them with positions.
6. End with a line: ROW1 EXPRESSION: <verbatim read>'

timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  "$D/zoom_row1_right_5x.png" \
  --view "Slide 048 original frame, 5x zoom of calc row 1 right side — structure inspection (dashed verticals + bracket pairs)" \
  --capture "single zoomed crop of the ORIGINAL lecture frame (no render in this call); region: right side of calculation row 1" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$D/row1_zoom_inspect.txt" \
  -p "$PROMPT"
rc=$?
echo "### row1zoom EXIT=$rc"
