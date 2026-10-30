const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", BLUE = "0000CC", INK = "000000", BADGE = "FFF9C4", NUM = "333333";
const FONT = "Arial";
const X0 = 1.15;

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME (root AGENTS.md) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("28", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("Receiver Operating Characteristic (ROC) Curve", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "middle",
  fontSize: 26, bold: true, color: RED, fontFace: FONT, margin: 0
});

// --- INTRO ---
// Original line 1 ends "...at all classification"; line 2 is "thresholds."
s.addText([
  { text: "ROC is a graph showing the performance of a classification model at all classification", options: { fontSize: 19, color: BLUE, fontFace: FONT, breakLine: true } },
  { text: "thresholds.", options: { fontSize: 19, color: BLUE, fontFace: FONT, breakLine: true } }
], {
  x: X0, y: 1.62, w: 10.5, h: 0.62, align: "left", valign: "top",
  margin: 0, lineSpacing: 18
});

// Single line: blue lead-in + red bold parameter names
s.addText([
  { text: "This curve plots two parameters: ", options: { fontSize: 19, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "[1] True Positive Rate [2] False Positive Rate", options: { fontSize: 19, bold: true, color: RED, fontFace: FONT, breakLine: true } }
], {
  x: X0, y: 2.481, w: 10.5, h: 0.4, align: "left", valign: "top",
  margin: 0, lineSpacing: 21
});

// --- TPR SECTION ---
s.addText([
  { text: "True Positive Rate (TPR) is a synonym for ", options: { fontSize: 18, bold: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "recall", options: { fontSize: 18, bold: true, underline: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: " and is therefore defined as:", options: { fontSize: 18, bold: true, color: BLUE, fontFace: FONT, breakLine: true } }
], {
  x: X0, y: 3.093, w: 9.5, h: 0.45, align: "left", valign: "top",
  margin: 0, lineSpacing: 22
});

// TPR formula box + equation image (measured w=2.438in h=0.53in)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.572, y: 3.5, w: 2.639, h: 0.875,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 }
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_tpr.png",
  x: 1.6725, y: 3.6725, w: 2.43833, h: 0.53
});

// TPR definition box (right of formula) + two-line text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.5, y: 3.556, w: 7.486, h: 0.75,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 }
});
s.addText([
  { text: "Correctly Predicted as Positive / ALL Actual Positive Samples", options: { fontSize: 18.5, color: RED, fontFace: FONT, breakLine: true } },
  { text: "(Percentage of correctly retrieved Positive samples)", options: { fontSize: 18.5, color: RED, fontFace: FONT, breakLine: true } }
], {
  x: 4.667, y: 3.556, w: 7.319, h: 0.75, align: "left", valign: "middle",
  margin: 0, lineSpacing: 21
});

s.addText("(Best Value is “1”)", {
  x: 7.85, y: 4.374, w: 2.2, h: 0.3, align: "left", valign: "top",
  fontSize: 16, color: RED, fontFace: FONT, margin: 0, lineSpacing: 19
});

// --- FPR SECTION ---
s.addText("False Positive Rate (FPR) is defined as:", {
  x: X0, y: 4.676, w: 5.0, h: 0.4, align: "left", valign: "top",
  fontSize: 18, bold: true, color: BLUE, fontFace: FONT, margin: 0, lineSpacing: 22
});

// FPR formula box + equation image (measured w=2.43167in h=0.53in)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.572, y: 5.055, w: 2.611, h: 0.861,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 }
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_fpr.png",
  x: 1.6617, y: 5.2205, w: 2.43167, h: 0.53
});

// FPR definition box + two-line text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.611, y: 5.097, w: 7.764, h: 0.764,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 }
});
s.addText([
  { text: "Incorrectly Predicted as Positive / ALL Actual Negative Samples", options: { fontSize: 18.5, color: RED, fontFace: FONT, breakLine: true } },
  { text: "(Error percentage in samples Predicted as Positive)", options: { fontSize: 18.5, color: RED, fontFace: FONT, breakLine: true } }
], {
  x: 4.792, y: 5.097, w: 7.58, h: 0.764, align: "left", valign: "middle",
  margin: 0, lineSpacing: 21
});

s.addText("(Best Value is “0”)", {
  x: 7.85, y: 5.901, w: 2.2, h: 0.3, align: "left", valign: "top",
  fontSize: 16, color: RED, fontFace: FONT, margin: 0, lineSpacing: 19
});

// --- CONCLUSION ---
s.addText([
  { text: "An ROC curve plots TPR vs. FPR ", options: { fontSize: 19, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "at different classification thresholds", options: { fontSize: 19, underline: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: ".", options: { fontSize: 19, color: BLUE, fontFace: FONT, breakLine: true } }
], {
  x: X0, y: 6.328, w: 8.8, h: 0.45, align: "left", valign: "top",
  margin: 0, lineSpacing: 21
});

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_028_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
