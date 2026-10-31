<x_0.0371><y_0.0359><chart type="lollipop">
title: Combine Precision and Recall in one number
bind: Precision ;  ; y

| Position | Treatment | Precision = TP | TP + FP |
| --- | --- | --- | --- |
| Positive | Positive | 30 | 70 |
| Negative | Negative | 10 | 59 |
| Positive | Positive | 30 | 0 |
| Negative | Negative | 0 | 70 |
| Good Model: Properly Classifies 20 out of 30 as Positive Properly Classifies 59 out of 70 as Negative | Actualy: This is Not a Model: It classifies ALL Samples as Positive | Procision= 20/(20+11) =64.5% | Precision= 30/(30+70) =30.3% |
| Recall= 20/(20+10) =66.6% | Recall= 30/(30+0) =100% | Average= 68.7%+60% =65.55% | Average= 30.3%+100% =65% |
</chart><x_0.9619><y_0.9984><class_Chart>