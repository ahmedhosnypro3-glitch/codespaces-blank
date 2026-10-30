<x_0.04><y_0.075>25
_Long Chain of Derivatives_
f(x) = ReLU = 0 for x<0 x for x≥0
f'(x)= 1 for x<0 for x≥0
Node Bias
1
1<x_0.96><y_0.9984><class_Picture>

<x_0.3779><y_0.6687><chart type="multi_line">
title: Vanishing Gradients
legend[color]: items=Tanh ; Sigmoid
bind: Tanh ;  ; y
bind: Sigmoid ;  ; y

| column_1 | Tanh | Sigmoid |
| --- | --- | --- |
| -4 | 0.00 | 0.00 |
| -3 | -1.00 | 0.10 |
| -2 | 0.30 | -1.00 |
| -1 | 0.50 | -0.80 |
| 0 | 0.60 | 0.70 |
| 1 | 0.90 | 0.95 |
| 2 | 1.00 | 1.00 |
| 3 | 1.00 | 1.00 |
</chart><x_0.6406><y_0.95><class_Chart>

<x_0.667><y_0.6695><chart type="multi_line">
legend[color]: items=Tanh Derivative ; Sigmoid Derivative
bind: Tanh Derivative ;  ; y
bind: Sigmoid Derivative ;  ; y

| x | Tanh Derivative | Sigmoid Derivative |
| --- | --- | --- |
| -5 | 0.0 | 0.0 |
| -4 | 0.0 | 0.0 |
| -3 | 0.1 | 0.1 |
| -2 | 0.6 | 0.6 |
| -1 | 0.5 | 0.7 |
| 0 | 1.0 | 1.0 |
| 1 | 0.5 | 0.5 |
| 2 | 0.3 | 0.3 |
| 3 | 0.1 | 0.1 |
| 4 | 0.0 | 0.0 |
</chart><x_0.9248><y_0.9547><class_Chart>