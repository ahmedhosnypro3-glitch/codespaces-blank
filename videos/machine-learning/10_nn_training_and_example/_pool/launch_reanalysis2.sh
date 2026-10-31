#!/usr/bin/env bash
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
nohup bash reanalysis_driver2.sh >> reanalysis2.out 2>&1 &
echo "launched pid $!"
sleep 3
echo "driver alive: $(pgrep -f 'reanalysis_driver2[.]sh' | head -1)"
