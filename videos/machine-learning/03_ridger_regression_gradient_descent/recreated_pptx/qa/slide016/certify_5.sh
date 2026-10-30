#!/bin/bash
# worker-016-finish-20261024 final certification for slide 016 (run ONLY after BOTH legs
# are PASS or PIL-adjudicated-clean with banked refutations).
# Sequence per scripts/17_worker_instructions.md:329 + caller law:
#   set visual_check PASS, set visual_transcript, set gen_status passed, heartbeat,
#   release, then RE-READ get 16 and RESTORE gen_status=passed if claim()/set() reset it
#   (15_progress.py:337-339 quirk), leaving worker_id="" and gen_status=passed.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 3
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
W=w016-finish-20261024
python3 scripts/15_progress.py set 16 visual_check PASS --worker $W
python3 scripts/15_progress.py set 16 visual_transcript \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016/judge_attempt_5.txt --worker $W
python3 scripts/15_progress.py set 16 gen_status passed --worker $W
python3 scripts/15_progress.py heartbeat 16 $W
python3 scripts/15_progress.py release 16 $W
echo "--- re-read row (must show worker_id=\"\") ---"
python3 scripts/15_progress.py get 16
python3 scripts/15_progress.py set 16 gen_status passed --worker $W
python3 scripts/15_progress.py get 16
