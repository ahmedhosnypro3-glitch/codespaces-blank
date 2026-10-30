<x_0.04><y_0.0781>**How to Kernelize SVM**
35
L D (α) = ∑ N αi - 1 2 ∑ N ∑ N αi αj yiy yj XTi Xj
W = ∑ i=1 αi yi Xi b = - 1 2 [maxi;y,=-1 WT Xi + mini;y,=+1 WT Xi]
Class of vector Z ⇒ sign( W T Z + b)
**_Remember_** :
**_Mapping_** Instead of using Xi _(of dimension d_) use φ(Xi) (_with higher dimension_ )
X Ti X j ⇒ φ(Xi)T φ(Xj)
**_Kernelization_** Instead of using φ(Xi)T φ(Xj) use K(XTi , Xj) _(Where K is one of kernel functions)_
L D (α) = ∑ n ai - 1 2 ∑ N ∑ n ai aj yiy yj XTi Xi
W = ∑ n ai yi Xi b = - 1 2 [maxi;y,=-1 WT Xi + mini;y,=+1 WT Xi]
Class of vector Z ⇒ sign( W T Z + b)<x_0.9326><y_0.9586><class_Picture>