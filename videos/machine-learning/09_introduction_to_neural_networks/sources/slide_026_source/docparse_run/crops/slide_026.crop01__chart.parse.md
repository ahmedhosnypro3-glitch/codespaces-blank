<x_0.0352><y_0.0375><chart type="compound_panel">
title: Sigmoid vs Tanh
panel: p1 ; multi_line ; Sigmoid vs Tanh
panel: p2 ; multi_line ; Tanh Derivative ; Sigmoid Derivative
legend[color]: items=Tanh ; Sigmoid
bind: x ; p1 ; x
bind: Tanh ; p1 ; y
bind: Sigmoid ; p1 ; y
bind: x ; p2 ; x
bind: Tanh Derivative ; p2 ; y
bind: Sigmoid Derivative ; p2 ; y

table[p1]:
| x | Tanh | Sigmoid |
| --- | --- | --- |
| -5 | 0.00 | -1.00 |
| -4 | 0.02 | -1.00 |
| -2 | 0.15 | -1.00 |
| 0 | 0.50 | 0.00 |
| 2 | 0.90 | 1.00 |
| 4 | 1.00 | 1.00 |

table[p2]:
| x | Tanh Derivative | Sigmoid Derivative |
| --- | --- | --- |
| -5 | 0.00 | 0.00 |
| -4 | 0.02 | 0.02 |
| -2 | 0.15 | 0.08 |
| 0 | 1.0 | 0.50 |
| 2 | 0.30 | 0.15 |
| 4 | 0.02 | 0.02 |
</chart><x_0.9639><y_0.9633><class_Chart>