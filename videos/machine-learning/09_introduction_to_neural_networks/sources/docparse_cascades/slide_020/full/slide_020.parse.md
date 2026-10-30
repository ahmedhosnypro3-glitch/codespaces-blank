<x_0.0371><y_0.0758><chart type="compound_panel">
title: Saturation Problem in Activation Functions
panel: p1 ; line
panel: p2 ; multi_line
axis[p1.x]: F (x) = Parametric ReLU
axis[p1.y]: f
axis[p2.x]: x
legend[color]: items=x = R.I ; x = R.F ; x = R.B ; x = S.R
bind: f ; p1 ; y
bind: x = R.I ; p1 ; x
bind: x = R.F ; p1 ; x
bind: x = R.B ; p1 ; x
bind: x = S.R ; p1 ; y

table[p1]:
| f | x = R.I | x = R.F | x = R.B | x = S.R |
| --- | --- | --- | --- | --- |
| -3 | 0 | 0 | 0 | 0 |
| -2 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0.5 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 |

table[p2]:
| x | x = R.I | x = R.F | x = R.B | x = S.R |
| --- | --- | --- | --- | --- |
| -3 | -0.2 | 0 | 0 | 0 |
| -2 | 0 | 0 | 0 | 0 |
| -1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 0 | 0 | 0 |
</chart><x_0.9609><y_0.957><class_Chart>