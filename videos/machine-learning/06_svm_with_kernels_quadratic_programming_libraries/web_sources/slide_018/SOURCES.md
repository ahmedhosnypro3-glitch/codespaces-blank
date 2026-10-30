# Source verification — slide 018
## Claims checked
- "Z = (x, y) -> (x^2, y^2, sqrt(2)xy)" — CONFIRMED — NUS CS5339 Kernel Notes https://www.comp.nus.edu.sg/~scarlett/CS5339_notes/05-Kernel_Notes.pdf
  Standard degree-2 polynomial feature map is phi(x) = (x1^2, x2^2, sqrt(2)*x1*x2); textbooks commonly list the same three components as (x1^2, sqrt(2)*x1*x2, x2^2) — same map, component order differs. DSC140A Lec10 slides confirm the same map and that <phi(x), phi(y)> = (x . y)^2: https://dsc140a.com/materials/lectures/Lec10/slides.pdf
- "Data is linearly separable In the new representation" — CONFIRMED — DataCamp Kernel Trick tutorial https://www.datacamp.com/tutorial/kernel-trick
  Standard kernel-trick principle: mapping non-linearly separable data into a higher-dimensional feature space (here 2D -> 3D, matching the x/y/z axes on the 3D plot) can make it linearly separable in that space; the linear decision boundary in the mapped space projects back to a non-linear one in the original plane.
- "Mapping Z to phi(Z)" (3D plot with plane + separator) — CONFIRMED — same sources; R^2 -> R^3 degree-2 map yields axes x, y, z.
## Overall
- VERDICT: CONFIRMED
- Tolerance notes for the rebuild: render the mapping in Professional Format as Z = (x, y) to phi(Z) = (x^2, y^2, sqrt(2)*xy) — keep sqrt(2) as a rational multiplier of xy; the implicit kernel is (x . y)^2, so no gamma/constant term belongs in this map. Frame text stays verbatim ("Data is linearly separable In the new representation" keeps its capitalization typo).
