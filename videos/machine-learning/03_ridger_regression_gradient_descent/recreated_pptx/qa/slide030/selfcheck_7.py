"""Title ink left-edge + band across this deck's ORIGINAL frames (convention check)."""
import numpy as np
from PIL import Image
import glob, os

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
for p in sorted(glob.glob(DECK + '/unique_slides/slide_0[0-9][0-9].jpg'))[:51]:
    n = os.path.basename(p)
    im = np.asarray(Image.open(p).convert('RGB')).astype(int)
    R,G,B = im[:,:,0], im[:,:,1], im[:,:,2]
    # title band y55..100, exclude left stroke cols 56..62
    band = np.zeros(im.shape[:2], bool)
    band[55:100, 63:565] = True
    # ink = non-panel (panel is E9E9E7 ~ (233,233,231)); text is dark or colored
    ink = ((R<200)|(G<200)|(B<200)) & band & ~((np.abs(R-233)<16)&(np.abs(G-233)<16)&(np.abs(B-231)<18))
    ys, xs = np.nonzero(ink)
    if len(xs):
        print(f"   {n}: title ink x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
    else:
        print(f"   {n}: no title ink found in band")
