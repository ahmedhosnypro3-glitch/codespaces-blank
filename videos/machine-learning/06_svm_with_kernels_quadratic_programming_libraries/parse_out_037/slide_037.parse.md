<x_0.04><y_0.075>_Example: Polynomial Kernel_ **How to Kernelize SVM**
LD (α) = ∑ i=1 N αi - 1/2 ∑ j=1 n ai αj yiy yj XTi XI W = ∑ i=1 αi yi Xi b = - 1/2 [max i:y,=-1 WT Xi + mini:y,=+1 WT Xi] Class of vector Z ⇒ sign (W T Z + b)
Kernelize using K(a,b)=[aT b+ 1]d
LD (α) = ∑ i=1 αi - 1/2 ∑ j=1 n ai αj yiy yj [XTi Xj + 1 ]d
W = ∑ i=1 αi yiXi b = - 1/2 [max i:y,=-1 [WTi Xj + 1 ]d + mini:y,=+1 [WTi Xj + 1 ]d] Class of vector Z is sign( [WT Z + 1 ]d + b)<x_0.9326><y_0.957><class_Picture>