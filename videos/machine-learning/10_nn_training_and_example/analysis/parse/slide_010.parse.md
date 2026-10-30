<x_0.0371><y_0.0781>Gradient Descent
W ji Updated = W ji old - η ∂ EW ji
W ji Updated = W ji old + Δ ji
Where Δ ji = −η ∂ E
∂ W ji
E = 1 2 ∑ j ( tj −Oj)2 For **Sigmoid** Activation Oj=f ( Netj)= 1 −Netj i Netj = ∑i ( wji Oi)
∂ E ∂ Oj = −(tj−Oj) ∂ Oj ∂ Netj = Oj(i−Oj) ∂ Wii = Oi
∂ E ∂ W ji = ∂ E ∂ Oj * ∂ Oj ∂ Netj * ∂ Netj ∂ Wji ∂ E ∂ E ∂ Oj = −(tj−Oj)
= −(tj−Oj) * Oj(1−Oj) * Oi = = δj * Oi
Where δj = − ∂ E ∂ Netj = ( tj−Oj) * Oj(1−Oj) (δj depends on j ONLY ) ∂ Netj ∂ Wji = Oi
Δ ji = −η ∂ E ∂ Wji = η δj * Oi Where δj = ( tj−Oj) * Oj(1−Oj) for output Layer<x_0.9463><y_0.957><class_Picture>