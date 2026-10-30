# Cut leg-B crop pairs at matched effective scale (LANCZOS x H_render/540) from render_18 + original.
import numpy as np
from PIL import Image
B="/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA=B+"/recreated_pptx/qa/slide003"
orig=Image.open(B+"/unique_slides/slide_003.jpg").convert("RGB")
ren=Image.open(QA+"/render_18.png").convert("RGB")
Hr=ren.size[1]; scale=Hr/540.0
# matrix band region (frame coords) with padding; includes y-vec,=, 5-col matrix, w-vec, dim labels
box=(74,320,538,520)
r_crop=ren.crop((int(box[0]*scale),int(box[1]*scale),int(box[2]*scale),int(box[3]*scale)))
o_up=orig.crop(box).resize((r_crop.size[0],r_crop.size[1]),Image.LANCZOS)
r_crop.save(QA+"/crop_18_matrix_render.png")
o_up.save(QA+"/crop_18_matrix_orig.png")
print("crop render px per frame px:",round(scale,4),"| crop size:",r_crop.size)
# also density crop for the equation stack (top box) region — a second leg-B region
box2=(266,105,600,305)
r2=ren.crop((int(box2[0]*scale),int(box2[1]*scale),int(box2[2]*scale),int(box2[3]*scale)))
o2=orig.crop(box2).resize((r2.size[0],r2.size[1]),Image.LANCZOS)
r2.save(QA+"/crop_18_topbox_render.png"); o2.save(QA+"/crop_18_topbox_orig.png")
print("topbox crop size:",r2.size)
