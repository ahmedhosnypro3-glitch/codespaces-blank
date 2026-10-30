<x_0.0391><y_0.0773><chart type="compound_panel">
title: Sigmoid vs Tanh
panel: p1 ; multi_line ; Sigmoid vs Tanh
panel: p2 ; multi_line ; Tanh Derivative ; Sigmoid Derivative
legend[color]: items=Tanh ; Sigmoid
bind: Tanh ; p1 ; y
bind: Sigmoid ; p1 ; y
bind: Tanh Derivative ; p2 ; y
bind: Sigmoid Derivative ; p2 ; y

table[p1]:
| x | Tanh | Sigmoid |
| --- | --- | --- |
| -5 | 0.00 | -0.40 |
| -4 | 0.00 | -1.00 |
| -2 | 0.10 | -1.00 |
| 0 | 0.50 | 0.00 |
| 2 | 0.95 | 0.85 |
| 4 | 1.00 | 1.00 |

table[p2]:
| x | Tanh Derivative | Sigmoid Derivative |
| --- | --- | --- |
| -5 | 0.00 | 0.00 |
| -4 | 0.02 | 0.00 |
| -2 | 0.10 | 0.10 |
| 0 | 1.0 | 1.0 |
| 2 | 0.20 | 0.20 |
| 4 | 0.02 | 0.02 |
</chart><x_0.959><y_0.9555><class_Chart>