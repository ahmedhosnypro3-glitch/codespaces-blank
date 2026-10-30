# OMML prepass note — slide 046 (scope S13, run 299640)

RESULT: OUT OF SCOPE — no wrap. The eq_046_*.json sidecars (final_w / initial_w / step_eta) are
STALE: none of their assets (eq_046_final_w.png 672x367 etc.) is embedded in the current
certified pptx. The 18 embedded pics are m046_* assets (m046_topcol1..6, m046_zcol1..3,
m046_augcol1..6, m046_vec_initial/final, m046_plot) rendered by build/gen_math_046.py via
matplotlib ax.text (plain text + patches) — NOT mathtext equation images, and they carry no
eq_*.json sidecars. Nothing to wrap; no mathtext source exists for the embedded media.
Deliverable untouched.
