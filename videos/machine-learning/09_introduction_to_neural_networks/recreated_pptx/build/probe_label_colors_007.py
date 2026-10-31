from PIL import Image
import numpy as np
SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
im = Image.open(SRC).convert('RGB')
a = np.asarray(im).astype(int)
def region(name, x0, x1, y0, y1):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    m = ~(((reg > 230).all(1)) | ((reg[:, 0] > 220) & (reg[:, 1] > 220) & (reg[:, 2] < 120)))
    reg = reg[m]
    if len(reg) == 0:
        print(name, 'none')
        return
    q = (reg // 48 * 48)
    uniq, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:6]
    print(name, [(tuple(int(v) for v in uniq[i]), int(counts[i])) for i in order])
region('C1', 524, 568, 152, 189)
region('C2', 594, 637, 295, 330)
region('C3', 259, 303, 394, 431)
region('d1', 245, 292, 174, 206)
region('d2', 660, 712, 192, 224)
region('d3', 566, 610, 128, 176)
region('+ve-green', 250, 290, 302, 330)
region('+ve-blue', 636, 674, 120, 146)
region('+ve-red', 490, 536, 442, 470)
region('badge', 805, 850, 45, 90)
region('title-line1', 330, 630, 40, 80)
region('title-blue-span', 470, 600, 80, 110)
