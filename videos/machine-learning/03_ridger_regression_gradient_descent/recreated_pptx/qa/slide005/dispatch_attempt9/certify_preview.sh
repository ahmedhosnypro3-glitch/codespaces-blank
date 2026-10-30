#!/usr/bin/env bash
# Certification sequence for slide 005 attempt 9 — run ONLY after real FINAL
# VERDICT bodies exist for Template A and all four crop legs.
#
# The upserts below are NOT run by this script: a certifier must confirm the
# verdicts with check_transcript.py first, then run the listed `set` commands.
set -u
WID="placeholder-worker-id"
cd "/worksp""aces/codespaces-blank/ai_llm_slides" || exit 9
Q="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
T=(
  "$Q/judge_attempt_9.txt"
  "$Q/crop_9_eq_stack_judge.txt"
  "$Q/crop_9_blue_upper_judge.txt"
  "$Q/crop_9_pink_band_judge.txt"
  "$Q/crop_9_lower_eqs_judge.txt"
)
echo "== verdict check (all five must be a real assertion) =="
python3 "$Q/dispatch_attempt9/check_transcript.py" "${T[@]}" || {
  echo "NOT ALL FIVE TRANSCRIPTS CARRY A REAL FINAL VERDICT — do not certify"
  exit 3
}
echo "all five verdicts real"
echo "== proceed =="
cat <<EOF
Run, with the actual worker id substituted for <WID>:

VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py set 5 visual_check PASS --worker <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py set 5 visual_transcript \\
videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/judge_attempt_9.txt --worker <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py set 5 visual_attempts <actual dispatched judge-leg count> --worker <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py set 5 gen_status passed --worker <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py set 5 pptx_path \\
videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_005_recreated.pptx --worker <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py heartbeat 005 <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py release 005 <WID>
VIDEO=machine-learning/03_ridger_regression_gradient_descent \\
python3 scripts/15_progress.py get 005        # verify gen_status=passed, visual_check=PASS, worker_id=""
EOF
