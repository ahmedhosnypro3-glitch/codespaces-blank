# Verification ledger — dual-read certification + re-analysis

| slide | first PASS transcript | corroboration transcript | verify verdict | reanalysis | certified |
|---|---|---|---|---|---|
| 1 | recreated_pptx/qa/slide001/judge_attempt_5.txt | recreated_pptx/qa/slide001/judge_verify_5.txt | PASS | analysis/reanalysis/slide_001_raw.json (gap fixed: Arabic label جامعة العلوم والتكنولوجيا, rtlMode) | yes |
| 28 | recreated_pptx/qa/slide28/judge_attempt_4.txt | recreated_pptx/qa/slide28/judge_verify_4c.txt | PASS (dual-read, original-first) | analysis/reanalysis/slide_028_raw.json | yes |
| 009 | recreated_pptx/qa/slide009/judge_attempt_1.txt | recreated_pptx/qa/slide009/judge_verify_1.txt | PASS/PASS | reanalysis/slide_009_raw.json | certified=yes |
| 23 | recreated_pptx/qa/slide023/judge_attempt_2.txt | recreated_pptx/qa/slide023//judge_verify_2.txt | FAIL | analysis/reanalysis/slide_023_raw.json | no |
