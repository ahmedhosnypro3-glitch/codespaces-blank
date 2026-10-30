# OMML prepass note — slide 037 (scope S13, run 299640)

RESULT: NOT WRAPPED — blocked on spec fidelity; deliverable untouched (no backup taken, no
manifest written; nothing was mutated). Task-added to mission run 299640.

Why the mechanical sidecar-driven wrap is not safe here:
1. `eq_037_sigma.json` has NO mathtext field (geometry only) — the sigma mathtext was never
   banked, so the OMML Choice content would be a reconstruction, not the certified source.
   (`\Sigma` vs `\sum` unresolved; media ink 228x323px = 38.8pt at 600dpi does not match the
   sidecar's recorded 30pt fontsize either — the sidecar fontsize fields do not describe the
   rendered media.)
2. `eq_037_frac.json` likewise lacks mathtext; the string IS recoverable from banked evidence
   (`\frac{\partial\, Error}{\partial\, W}`, crop_4_eq_stack_adjudication.txt) — but:
3. All 5 equation pics are placed ANISOTROPICALLY RESCALED in the certified pptx
   (sigma 243x338px shown at 0.731x0.671 / 0.987x0.851 / 0.877x0.774 of nominal;
   frac 651x363px at 0.917x1.102) — no single faithful OMML fontsize exists per instance, and
   the noAutofit Choice frame would misrepresent the certified scale in PowerPoint.
The LO/Fallback render is unaffected by these limits (a wrap would still have passed the
pixel gate), but the PowerPoint Choice view would degrade vs the current certified PNG view.
Needs a dedicated re-derivation pass (re-bank mathtext + effective per-instance fontsize, or
re-place at px/600) before wrapping.
