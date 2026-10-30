#!/bin/bash
# wrapper: always run from the video dir with TMPDIR set
cd /workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent || exit 1
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
python3 recreated_pptx/qa/slide004/asciimap.py "$@"
