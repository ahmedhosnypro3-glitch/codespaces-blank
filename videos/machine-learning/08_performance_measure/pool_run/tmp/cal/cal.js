const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const FONT = "Arial";
const L1 = "ROC is a graph showing the performance of a classification model at all classification";
const L2 = "thresholds.";
const P2B = "This curve plots two parameters: ";
const P2R = "[1] True Positive Rate [2] False Positive Rate";
const TL = "True Positive Rate (TPR) is a synonym for recall and is therefore defined as:";
const DL = "Correctly Predicted as Positive / ALL Actual Positive Samples";
const CL = "An ROC curve plots TPR vs. FPR at different classification thresholds.";
const lines = [];
function add(label, size, bold) { lines.push({ text: label, options: { fontSize: size, bold: !!bold, fontFace: FONT, color: "000000", breakLine: true } }); }
for (const size of [18, 19, 20]) {
  add(L1, size, false); add(L2, size, false); add(P2B, size, false); add(P2R, size, true);
  add(TL, size, true); add(DL, size, false); add(CL, size, false);
}
let s = pptx.addSlide();
s.addText(lines, { x: 0.2, y: 0.3, w: 12.5, h: 6.5, margin: 0, lineSpacing: 24, fontFace: FONT });
pptx.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/pool_run/tmp/cal/cal.pptx" }).then(() => console.log("done"));
