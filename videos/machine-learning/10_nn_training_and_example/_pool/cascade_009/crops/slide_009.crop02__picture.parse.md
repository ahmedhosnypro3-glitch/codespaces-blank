<x_0.0371><y_0.0375>Gradient Descent
W ji Updated = W ji old - η ∂ E @ W ji
W ji Updated = W ji old + Δ ji
Where Δ ji = −η ∂ E / ∂ W ji 9 Mode Bias
E = 1 2 ∑ (t j − Oj)2 For **Sigmoid** Activation Oj=f(Net j)= 1 Net j= ∑ (w ji Oi)
∂ E ∂ Oj = −(tj−Oj) ∂ Net j = Oj(i−Oj) ∂ W ii i = Oi
∂ EW ji = ∂ E ∂ Oj * ∂ Oj ∂ Net j * ∂ Net j ∂ Wji ∂ E ∂ Oj = −(tj−Oj) ∂ Wji = −(tj−Oj)
= −(tj−Oj) * Oj(1−Oj) * Oi<x_0.999><y_0.9617><class_Picture>