<x_0.8994><y_0.1172>19<x_0.9238><y_0.1484><class_Page-header>

<x_0.4883><y_0.1375>**Kernels**<x_0.6074><y_0.1875><class_Section-header>

<x_0.0869><y_0.2234>• Kernels Represent a **dot product of two vectors** in a higher dimensional feature space<x_0.8164><y_0.2664><class_Text>

<x_0.0859><y_0.3406>• Any Machine Learning Model that contains dot product of input samples can be kernelized<x_0.8438><y_0.3844><class_Text>

<x_0.0879><y_0.4578>• Instead of calculating dot product between input vectors, calculate dot product between input vectors after mapping them to higher dimensional space<x_0.9053><y_0.5602><class_Text>

<x_0.1309><y_0.6023>aTb ⇒ map to φ(a) and φ(b) ⇒ φ(a)T φ(b) ≡ K(a , b)<x_0.8154><y_0.6602><class_Formula>

<x_0.0889><y_0.6937>• Different Kernel functions are based on different mapping functions<x_0.6572><y_0.7367><class_Text>

<x_0.0898><y_0.7516>• **_Calculations of mapping_** and **_calculations of dot product_** _in higher dimensional space are very expensive._<x_0.9062><y_0.8547><class_Text>

<x_0.0879><y_0.8711>• Use **Kernel Trick** to minimize both calculations (at no extra cost)<x_0.6455><y_0.9125><class_Text>