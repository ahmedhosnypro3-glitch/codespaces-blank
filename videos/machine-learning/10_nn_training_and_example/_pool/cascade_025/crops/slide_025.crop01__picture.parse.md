<x_0.0342><y_0.0437>**Vanishing and Exploding Gradients** 25
_Long Chain of Derivatives_ **Class 1**
f ( x) = ReLU = 0 for x<0
x for x≥0
f '( x)= 0 for x<0
1 for x≥0<x_0.2861><y_0.5422><class_Picture>

<x_0.9092><y_0.0617>25<x_0.9561><y_0.1359><class_Page-header>

<x_0.3174><y_0.1836><x_0.8672><y_0.5453><class_Picture>

<x_0.8789><y_0.25>**Error Error Error**<x_0.8936><y_0.4633><class_Text>

<x_0.9082><y_0.243>**Class 1**<x_0.9443><y_0.2648><class_Text>

<x_0.9102><y_0.3445>**Class 2**<x_0.9434><y_0.3656><class_Text>

<x_0.9072><y_0.4586>**Class m**<x_0.9453><y_0.4805><class_Text>

<x_0.1016><y_0.5727>**Exploding Gradients**<x_0.2578><y_0.6086><class_Caption>

<x_0.082><y_0.6305><chart type="line">
axis[x]: x
axis[y]: f
bind: x ;  ; x
bind: f ;  ; y

| x | f |
| --- | --- |
| -10 | 0 |
| -5 | 0 |
| 0 | -1 |
| 5 | 4 |
| 10 | 10 |
</chart><x_0.3203><y_0.9484><class_Chart>

<x_0.5693><y_0.6047>**Vanishing Gradients**<x_0.7275><y_0.6391><class_Caption>

<x_0.3799><y_0.6578><chart type="multi_line">
title: Sigmoid vs Tanh
legend[color]: items=Tanh ; Sigmoid
bind: Tanh ;  ; y
bind: Sigmoid ;  ; y
annotation: callout ; label=0.25

| x | Tanh | Sigmoid |
| --- | --- | --- |
| -5 | 0.00 | -1.00 |
| -4 | 0.02 | -1.00 |
| -2 | 0.15 | -1.00 |
| 0 | 0.60 | 0.00 |
| 2 | 0.90 | 0.98 |
| 4 | 1.00 | 1.00 |
</chart><x_0.6416><y_0.9477><class_Chart>

<x_0.6689><y_0.6836><chart type="multi_line">
legend[color]: items=Tanh Derivative ; Sigmoid Derivative
bind: Tanh Derivative ;  ; y
bind: Sigmoid Derivative ;  ; y
annotation: callout ; label=1.0 ; value=0.25

| x | Tanh Derivative | Sigmoid Derivative |
| --- | --- | --- |
| -5 | 0.80 | 0.80 |
| -4 | 0.81 | 0.80 |
| -2 | 0.65 | 0.65 |
| 0 | 1.0 | 0.55 |
| 2 | 0.70 | 0.65 |
| 4 | 0.80 | 0.80 |
</chart><x_0.9258><y_0.9492><class_Chart>