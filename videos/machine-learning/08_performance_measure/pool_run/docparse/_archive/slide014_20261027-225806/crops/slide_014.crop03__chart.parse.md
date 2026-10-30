<x_0.0361><y_0.0375><chart type="lollipop">
title: Combine Precision and Recall in one number
bind: Precision ;  ; y

| Position | Treatment | Precision = TP | Recall = TP + FN |
| --- | --- | --- | --- |
| Positive | Positive | 30 | 70 |
| Negative | Negative | 10 | 70 |
| Positive | Positive | 59 | 0 |
| Negative | Positive | 30 | 70 |
| Good Model: Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative | Top FN | 0 | 70 |
| Correctly: This is Not a Model: It classifies ALL Samples as Positive | Precision= 20/(20+11) =64.5% | Precision= 30/(30+70) =30.3% | Precision= 30.3% |
| Recall= 20/(20+10) =66.6% | Recall= 30/(30+0) =100% | Recall= 30/(30+0) =100% | Precision= 65% |
</chart><x_0.9629><y_0.9617><class_Chart>