const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "333333", YELLOW = "FFF9C4";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 1.5 } });
s.addText("17", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
s.addText("F-Score for different Precision and Recall values", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Chart image: generated from PIL-measured geometry of the original frame.
// Original px (960x540, 1px=1pt): container x184-766, y104-503 -> inches /72.
s.addImage({
  path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/slide017_f1chart_v2.png",
  x: 184 / 72, y: 104 / 72, w: 582 / 72, h: 399 / 72,
});

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_017_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
