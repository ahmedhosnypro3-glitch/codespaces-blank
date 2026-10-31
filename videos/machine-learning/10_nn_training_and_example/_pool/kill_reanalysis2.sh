#!/usr/bin/env bash
# Stop the parallel re-analysis driver and any of its in-flight workers.
# Invoked by name from a parent shell that never mentions the patterns itself.
set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
for p in $(pgrep -f 'reanalysis_driver2[.]sh'; pgrep -f 'run_on[e]'); do
  [ "$p" = "$$" ] && continue
  kill "$p" 2>/dev/null && echo "killed $p"
done
sleep 1
rm -f analysis/reanalysis_skill/slide_*.analysis.txt.b[0-9] 2>/dev/null
echo "cleanup done; remaining run_one procs: $(pgrep -fc 'run_on[e]' || true)"
