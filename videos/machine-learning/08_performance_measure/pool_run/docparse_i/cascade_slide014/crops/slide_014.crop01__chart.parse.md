<x_0.0381><y_0.0375><chart type="lollipop">
title: Combine Precision and Recall in one number
bind: Precision ;  ; y

| Position | Treatment | Precision |
| --- | --- | --- |
| Positive | Positive | 30 |
| Negative | Negative | 70 |
| Positive | Positive | 30 |
| Negative | Negative | 0 |
| Good Model: Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative | Actual: This is Not a Model: It classifies ALL Samples as Positive | 70 |
| Precision= 20/(20+11) =64.5% | Precision= 30/(30+70) =30.3% | 30.3% |
| Recall= 20/(20+10) =66.6% | Recall= 30/(30+0) =100% | 100% |
| Average= 68.7%+60% =65.55% | Average= 30.3%+100% =65% | 65% |
</chart><x_0.9609><y_0.9633><class_Chart>