const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", BLUE = "00008B", INK = "000000", BADGE = "FFF9C4", NUM = "333333";
const FONT = "Arial";

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
s.addText("37", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("Area Under the Curve (AUC)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0
});

// --- white text panel (original px 98..822 x 94..205; pink borders on left x96 and bottom y206) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 98 / 72, y: 94 / 72, w: (822 - 98) / 72, h: (210 - 94) / 72,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 }
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 95.5 / 72, y: 94 / 72, w: 1.2 / 72, h: (211 - 94) / 72,
  fill: { color: "F3B4C0" }, line: { color: "F3B4C0", width: 0 }
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 96 / 72, y: 210.5 / 72, w: (822 - 96) / 72, h: 1.2 / 72,
  fill: { color: "F3B4C0" }, line: { color: "F3B4C0", width: 0 }
});

// subtitle (blue bold, 'different models' underlined) — px band y100..115, x105..782
s.addText([
  { text: "Compare between ", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "different models", options: { fontSize: 17, bold: true, underline: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: " (at different thresholds for each model)", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT, breakLine: false } }
], {
  x: 105 / 72, y: 100 / 72, w: 9.6, h: 0.3, align: "left", valign: "top",
  margin: 0
});

// body line 1 — px band y154..170, x105..687; "[FBR=0, TPR=1]" is red in the original
s.addText([
  { text: "Best Model is the model trying to reach\u00A0\u00A0the point at ", options: { fontSize: 17, color: INK, fontFace: FONT, breakLine: false } },
  { text: "[FBR=0, TPR=1]", options: { fontSize: 17, bold: true, color: RED, fontFace: FONT, breakLine: false } }
], {
  x: 105 / 72, y: 154 / 72, w: 9.6, h: 0.3, align: "left", valign: "top",
  margin: 0
});

// body line 2 — px band y186..198, x105..787
s.addText("In other words, Best model is the model that has the largest area under the curve", {
  x: 105 / 72, y: 186 / 72, w: 9.6, h: 0.3, align: "left", valign: "top",
  fontSize: 17, color: INK, fontFace: FONT, margin: 0
});

// --- ROC plot (generated matplotlib asset; plot box px 259,217 - 632,512) ---
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/roc_037_v2.png",
  x: 259 / 72, y: 217 / 72, w: 373 / 72, h: 295 / 72
});

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_037_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
