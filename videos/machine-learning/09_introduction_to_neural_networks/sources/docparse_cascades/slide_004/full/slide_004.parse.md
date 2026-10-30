<x_0.3643><y_0.1062>**Problem Formulation**<x_0.6592><y_0.1602><class_Section-header>

<x_0.9023><y_0.1172>4<x_0.918><y_0.15><class_Text>

<x_0.0752><y_0.2016>**Define** δi as :<x_0.1953><y_0.2461><class_Text>

<x_0.0762><y_0.2484>_If_ X ∈ **_class I_** and _misclassified_ as **_Class II_** then d(X) will be <0 ⇒ δi = -1 ⇒ d(X) δi >0
_If_ X ∈ **_class II_** and misclassified as **_Class I_** then d(X) will be **>**0** ⇒ δi = +1 ⇒ d(X) δi >0<x_0.8877><y_0.3445><class_Text>

<x_0.0742><y_0.4234>**Redefine Error function as:**<x_0.3154><y_0.4648><class_Section-header>

<x_0.0771><y_0.4656>**Error**= ∑ δi W T Xi i ⇒ (W T Xi ) takes positive and negative values and δi has the same sign
_all mislassified vectors_(i)<x_0.9082><y_0.543><class_Text>

<x_0.0732><y_0.5437>_Summation is always positive_<x_0.3105><y_0.5852><class_Text>

<x_0.082><y_0.6359>_Minimize the Error using Gradient Descent with step_ η<x_0.5674><y_0.6813><class_Text>

<x_0.0801><y_0.7125>W (updated)= Wold - η Θ **Error** ∂ W where **where** σ Error ∂ W = ∑ mislcassed vectors δi Xi
W (updated)= Wold - η ∑ mislcassed vectors ONLY (i)<x_0.8008><y_0.9234><class_Picture>

<x_0.6807><y_0.832>W (updated)= Wold - η δi Xi<x_0.916><y_0.8922><class_Formula>