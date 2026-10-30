// Build slide 031: Example / Better Weights (badge 31)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

// ---- HOUSE CHROME (laws from pattern) ----
// 1. Outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("31", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box
s.addText("Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Subtitle box: "Better Weights" in green box
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.85, w: 3.5, h: 0.5,
  fill: { color: "E0F5E0" },
  line: { color: "008000", width: 1 },
});
s.addText("Better Weights", {
  x: 0.6, y: 0.85, w: 3.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 16, bold: true, color: "008000", fontFace: FONT, margin: 0,
});

// ---- SLIDE CONTENT ----

// Neural network diagram (generated graph from graphgen/)
// The diagram spans top-center to mid-right
// For now, using a placeholder - the graph will be generated via graphgen/
s.addImage({
  path: "slide_031_nn_diagram.png",
  x: 1.5, y: 1.2, w: 7.5, h: 3.5,
});

// "Forward" label (blue, italic) - middle-left
s.addText("Forward", {
  x: 0.8, y: 3.3, w: 1.5, h: 0.5,
  align: "center", fontSize: 16, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0,
});

// Blue-bordered boxes: Net calculations (bottom-left)
// First blue box: Net3, Net4, Net5
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.8, w: 5.5, h: 1.2,
  fill: { color: "FFFFFF" },
  line: { color: "000080", width: 1.5 },
});
s.addImage({ path: "eq_net3.png", x: 0.6, y: 3.85, w: 3.55, h: 0.20 });
s.addImage({ path: "eq_net4.png", x: 0.6, y: 4.15, w: 3.55, h: 0.20 });
s.addImage({ path: "eq_net5.png", x: 0.6, y: 4.45, w: 3.55, h: 0.20 });

// Second blue box: Net6, Net7
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.2, w: 5.5, h: 1.0,
  fill: { color: "FFFFFF" },
  line: { color: "000080", width: 1.5 },
});
s.addImage({ path: "eq_net6.png", x: 0.6, y: 5.25, w: 5.3, h: 0.20 });
s.addImage({ path: "eq_net7.png", x: 0.6, y: 5.55, w: 5.3, h: 0.20 });

// Green-bordered boxes: O (sigmoid output) calculations (bottom-right)
// First green box: O3, O4, O5
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.5, y: 3.8, w: 2.5, h: 1.2,
  fill: { color: "FFFFFF" },
  line: { color: "008000", width: 1.5 },
});
s.addImage({ path: "eq_O3.png", x: 6.6, y: 3.85, w: 1.93, h: 0.29 });
s.addImage({ path: "eq_O4.png", x: 6.6, y: 4.20, w: 1.93, h: 0.29 });
s.addImage({ path: "eq_O5.png", x: 6.6, y: 4.55, w: 1.93, h: 0.29 });

// Second green box: O6, O7
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.5, y: 5.2, w: 2.5, h: 1.0,
  fill: { color: "FFFFFF" },
  line: { color: "008000", width: 1.5 },
});
s.addImage({ path: "eq_O6.png", x: 6.6, y: 5.25, w: 1.88, h: 0.29 });
s.addImage({ path: "eq_O7.png", x: 6.6, y: 5.60, w: 1.93, h: 0.29 });

const outPath = "slide_031_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));