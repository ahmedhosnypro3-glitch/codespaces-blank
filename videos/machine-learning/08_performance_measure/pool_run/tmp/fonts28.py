from PIL import ImageFont

REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# original measurements (960px = 13.333in => 72 px/in => 1 pt = 1 px)
cases = [
    # (label, text, font_path, target_width_px)
    ("para1 line1", "ROC is a graph showing the performance of a classification model at all classification", REG, 800-83),
    ("para2 full", "This curve plots two parameters: ", REG, 355-84),
    ("para2 red", "[1] True Positive Rate [2] False Positive Rate", REG, 752-355),
    ("tpr leadin", "True Positive Rate (TPR) is a synonym for recall and is therefore defined as:", BLD, 739-83),
    ("fpr leadin", "False Positive Rate (FPR) is defined as:", BLD, 428-84),
    ("tpr def L1", "Correctly Predicted as Positive / ALL Actual Positive Samples", REG, 844-336),
    ("tpr def L2", "(Percentage of correctly retrieved Positive samples)", REG, 810-375),
    ("fpr def L1", "Incorrectly Predicted as Positive / ALL Actual Negative Samples", REG, 889-345),
    ("fpr def L2", "(Error percentage in samples Predicted as Positive)", REG, 830-392),
    ("conclusion", "An ROC curve plots TPR vs. FPR at different classification thresholds.", REG, 672-83),
]

for label, text, path, target in cases:
    best = None
    for size in range(8, 26):
        f = ImageFont.truetype(path, size)
        w = f.getlength(text)
        if best is None or abs(w - target) < abs(best[1] - target):
            best = (size, w)
    print(f"{label:14s} target={target:4d}px  best_size={best[0]}pt -> width {best[1]:.0f}px")
    for size in (best[0] - 1, best[0], best[0] + 1):
        f = ImageFont.truetype(path, size)
        print(f"     size {size}: {f.getlength(text):.0f}px")
