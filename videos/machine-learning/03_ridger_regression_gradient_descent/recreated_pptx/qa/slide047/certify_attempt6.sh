#!/usr/bin/env bash
# Certification sequence for slide 047 (worker w047-root-20261024).
# Run ONLY after both legs PASS (or every finding is PIL-adjudicated with a banked record).
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047
TRANS=$Q/judge_attempt_6.txt

if ! grep -qE "FINAL VERDICT: ?\*{0,2}PASS" "$Q/judge_attempt_6.txt"; then
  echo "REFUSING: full-slide leg not PASS"; exit 1
fi
for n in topband augmatrix calceq calcright button; do
  if ! grep -qE "FINAL VERDICT: ?\*{0,2}PASS" "$Q/crop_6_${n}_judge.txt"; then
    echo "REFUSING: crop $n not PASS"; exit 1
  fi
done

python3 scripts/15_progress.py set 47 visual_check PASS
python3 scripts/15_progress.py set 47 visual_attempts 6
python3 scripts/15_progress.py set 47 visual_transcript "$TRANS"
python3 scripts/15_progress.py set 47 gen_status passed
python3 scripts/15_progress.py set 47 last_error ""
python3 scripts/15_progress.py release 47 w047-root-20261024
echo "=== verify ==="
python3 scripts/15_progress.py get 47
