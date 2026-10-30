const pptxgen = require("pptxgenjs");
const path = require("path");

const ROOT = "/home/codespace/ai_llm_slides";
const VID = ROOT + "/videos/machine-learning/10_nn_training_and_example";
const NUM = 34, FONT = "Arial", S = 13.33 / 960;
const px = (v) => +(v * S).toFixed(4);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText(String(NUM), { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center",
  valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });
