<x_0.0371><y_0.0375><chart type="compound_panel">
title: Saturation Problem in Activation Functions
panel: p1 ; line
panel: p2 ; multi_line
axis[p1.x]: x
axis[p1.y]: f
axis[p2.x]: x
legend[color]: items=z = 0.1 ; z = 0.2 ; z = 0.3 ; z = 1.0
bind: x ; p1 ; x
bind: z = 0.1 ; p1 ; y
bind: z = 0.2 ; p1 ; y
bind: z = 0.3 ; p1 ; y
bind: z = 1.0 ; p1 ; y

table[p1]:
| x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 |
| --- | --- | --- | --- | --- |
| -4 | -0.1 | 0.0 | 0.0 | 0.0 |
| -2 | 0.1 | 0.1 | 0.1 | 0.1 |
| 0 | 0.1 | 0.1 | 0.1 | 0.1 |
| 2 | 2.0 | 2.0 | 2.0 | 2.0 |

table[p2]:
| x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 |
| --- | --- | --- | --- | --- |
| -3 | -0.2 | -0.3 | -0.3 | -1.0 |
| -2 | -0.1 | -0.2 | -0.2 | -0.8 |
| -1 | 0.0 | 0.0 | 0.0 | 0.0 |
| 0 | 0.1 | 0.1 | 0.1 | 0.1 |
| 1 | 1.0 | 1.5 | 1.9 | 1.7 |
| 2 | 3.1 | 3.2 | 3.1 | 3.1 |
</chart><x_0.9629><y_0.9633><class_Chart>