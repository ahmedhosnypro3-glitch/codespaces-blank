<x_0.0371><y_0.075><chart type="compound_panel">
title: Saturation Problem in Activation Functions
panel: p1 ; line
panel: p2 ; line
axis[p1.x]: t
axis[p1.y]: tatb x
axis[p2.x]: x
bind: t ; p1 ; x
bind: depth = t(1) ; p1 ; y
bind: x ; p2 ; x
bind: tatb x ; p2 ; y

table[p1]:
| t | depth = t(1) |
| --- | --- |
| -3 | 0 |
| -4 | 0 |
| -5 | 0 |
| -6 | 0 |
| -7 | 0.8 |
| -8 | 0.9 |
| -9 | 0.9 |
| 0 | 0.9 |
| 1 | 0.9 |
| 2 | 0.9 |
| 3 | 0.9 |

table[p2]:
| x | tatb x |
| --- | --- |
| -3 | -1 |
| -2 | -1 |
| -1 | -0.5 |
| 0 | 0 |
| 1 | 1 |
| 2 | 1.0 |
| 3 | 1.0 |
</chart><x_0.9609><y_0.957><class_Chart>