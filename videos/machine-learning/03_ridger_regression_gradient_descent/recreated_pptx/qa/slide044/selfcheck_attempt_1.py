#!/usr/bin/env python3
"""Pre-judge self-check for slide 044: PIL assertions against render_1.png."""
import numpy as np
from PIL import Image

RENDER = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
          "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/render_1.png")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg")

im = Image.open(RENDER).convert("RGB")
W, H = im.size
S = W / 960.0
IM = np.asarray(im).astype(int)
LUM = 0.299 * IM[:, :, 0] + 0.587 * IM[:, :, 1] + 0.114 * IM[:, :, 2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

fails = []
def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + ("  " + detail if detail else ""))
    if not ok:
        fails.append(name)

def box(x0, y0, x1, y1):
    return (int(y0 * S), int(y1 * S) + 1, int(x0 * S), int(x1 * S) + 1)

def ink_count(x0, y0, x1, y1, thr=200):
    sl = LUM[box(x0, y0, x1, y1)[0]:box(x0, y0, x1, y1)[1],
             box(x0, y0, x1, y1)[2]:box(x0, y0, x1, y1)[3]]
    return int((sl < thr).sum())

def colored(x0, y0, x1, y1, kind):
    ys, ye, xs, xe = box(x0, y0, x1, y1)
    rr, gg, bb = r[ys:ye, xs:xe], g[ys:ye, xs:xe], b[ys:ye, xs:xe]
    if kind == "red":
        m = (rr > 110) & (rr - gg > 40) & (rr - bb > 40)
    else:
        m = (bb > 100) & (bb - rr > 25) & (bb - gg > 15)
    return int(m.sum())

print("render %dx%d  scale=%.4f  (render px per frame px)" % (W, H, S))

# --- frame / chrome (house_chrome_check already PASSed; re-assert the top-stroke ban)
check("no top stroke (top band red px == 0)",
      int(((r[0:int(45 * S), :] > 110) & (r[0:int(45 * S), :] - g[0:int(45 * S)] > 40)).sum()) == 0)
badge = LUM[int(50 * S):int(96 * S), int(858 * S):int(895 * S)]
check("badge yellow present around (876,73)",
      int(((r[int(60*S):int(86*S), int(862*S):int(890*S)] > 200) &
           (r[int(60*S):int(86*S), int(862*S):int(890*S)] < 255)).sum()) > 50)

# --- panel containment: no ink in the white margin left of the left stroke
left_margin = LUM[:, 0:int(56 * S)]
check("nothing drawn left of the panel (cols 0..56)",
      int((left_margin < 200).sum()) == 0)

# --- table ink present at the measured glyph rows (frame coords)
check("T1 header ink (x88..216 y64..73)", ink_count(88, 62, 216, 75) > 60)
check("T1 data row 1 ink (y78..91)", ink_count(88, 78, 216, 91) > 80)
check("T1 data row 2 ink (y94..107)", ink_count(88, 94, 216, 107) > 80)
check("T1 class row ink (y113..125)", ink_count(88, 113, 216, 125) > 60)
check("T2 box ink (top rule y140)", ink_count(72, 139, 245, 142) > 100)
check("T2 caption ink (y148..159)", ink_count(84, 147, 224, 160) > 40)
check("T2 header ink (y166..176)", ink_count(92, 164, 218, 178) > 40)
check("T2 row1 ink (y182..195)", ink_count(92, 181, 218, 196) > 40)
check("T2 row2 ink (y197..210)", ink_count(92, 196, 218, 211) > 40)
check("T2 row3 ink (y212..225)", ink_count(92, 211, 218, 225) > 40)
check("T2 class row ink (y232..244)", ink_count(92, 230, 218, 245) > 50)

# --- class-row colour split: 3 red + 3 blue in BOTH tables
check("T1 class row RED ink (cells 1-3)", colored(90, 110, 160, 126, "red") > 25,
      "red px=%d" % colored(90, 110, 160, 126, "red"))
check("T1 class row BLUE ink (cells 4-6)", colored(170, 110, 218, 126, "blue") > 25,
      "blue px=%d" % colored(170, 110, 218, 126, "blue"))
check("T2 class row RED ink (cells 1-3)", colored(90, 230, 165, 246, "red") > 25,
      "red px=%d" % colored(90, 230, 165, 246, "red"))
check("T2 class row BLUE ink (cells 4-6)", colored(175, 230, 220, 246, "blue") > 25,
      "blue px=%d" % colored(175, 230, 220, 246, "blue"))

# --- centre block
check("Initial W bracket strokes (x331/x353 y55..103)",
      ink_count(329, 55, 334, 105) > 30 and ink_count(351, 55, 355, 105) > 30)
check("Initial W glyph stack (3 entries)", ink_count(334, 60, 350, 103) > 60,
      "px=%d" % ink_count(334, 60, 350, 103))
check("'Initial W =' text ink (x266..322 y74..85)", ink_count(264, 73, 324, 86) > 40)
check("RED 'Step' ink (x365..435 y66..77)", colored(363, 64, 437, 80, "red") > 60,
      "red px=%d" % colored(363, 64, 437, 80, "red"))
check("'Check classes of' ink (x499..582 y82..89)", ink_count(497, 80, 584, 91) > 40)
check("Z-matrix header ink (y64..76)", ink_count(594, 63, 658, 77) > 40)
check("Z-matrix row ink (y83..108)", ink_count(594, 82, 658, 109) > 80)
check("rule line: red C1 ink", colored(238, 109, 266, 126, "red") > 12,
      "red px=%d" % colored(238, 109, 266, 126, "red"))
check("rule line: blue C2 ink", colored(310, 109, 330, 126, "blue") > 12,
      "blue px=%d" % colored(310, 109, 330, 126, "blue"))
check("rule line: trailing text ink", ink_count(330, 109, 510, 126) > 80)

# --- equation stack
for i, (y0, y1) in enumerate([(149, 196), (219, 262), (279, 322), (342, 394),
                              (411, 460), (478, 527)], 1):
    check("equation band %d ink" % i, ink_count(280, y0, 850, y1) > 400,
          "px=%d" % ink_count(280, y0, 850, y1))
for i in (1, 2, 3):
    check("band %d RED decision ink" % i,
          colored(330, {1: 160, 2: 228, 3: 288}[i], 850, {1: 178, 2: 246, 3: 306}[i], "red") > 100)
for i in (4, 5, 6):
    check("band %d has NO red (black decision)" % i,
          colored(280, {4: 342, 5: 411, 6: 478}[i], 850, {4: 394, 5: 460, 6: 527}[i], "red") < 40)

# --- red Iteration 3 badge
check("Iteration 3 badge RED fill (x84..214 y277..305)", colored(86, 278, 212, 304, "red") > 3000,
      "red px=%d" % colored(86, 278, 212, 304, "red"))
check("Iteration 3 badge WHITE text", ink_count(90, 283, 210, 300, thr=235) > 100,
      "px=%d" % ink_count(90, 283, 210, 300, thr=235))

# --- no content outside the panel
right_margin = LUM[:, int(906 * S):]
check("nothing drawn right of the panel (cols 906..end)", int((right_margin < 200).sum()) == 0)
bottom_margin = LUM[int(542 * S):, :]
check("nothing drawn below the bottom stroke (rows 542..end)",
      int((bottom_margin < 200).sum()) == 0)

print()
print("SELF-CHECK: %s  (%d failures)" % ("PASS" if not fails else "FAIL", len(fails)))
if fails:
    print("FAILED: " + ", ".join(fails))
