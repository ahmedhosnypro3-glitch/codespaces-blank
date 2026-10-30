// Build slide 026: Sigmoid vs Tanh (badge 18)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "F5F5F5" };
const FONT = "Arial";

// ---- HOUSE CHROME ----
// 1. Outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("18", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box
s.addText("Sigmoid vs Tanh", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// ---- SLIDE CONTENT ----

// Equation row 1: Sigmoid formula + x=0 values
s.addText("f(x) = Sigmoid(x) = 1/(1+e^-x) ⇒ f'(x) = f(x)(1-f(x))", {
  x: 0.5, y: 1.0, w: 5.5, h: 0.4,
  align: "left", fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
// Cream box with x=0 values
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.5, y: 1.0, w: 4.0, h: 0.4,
  fill: { color: "FDF2E9" }, line: { color: "C00000", width: 1 },
});
s.addText("at x=0   f(0)=0.5   f'(0)=0.25", {
  x: 6.5, y: 1.0, w: 4.0, h: 0.4,
  align: "center", valign: "middle", fontSize: 13, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Equation row 2: Tanh formula + x=0 values
s.addText("f(x) = tanh(x) = sinh x / cosh x ⇒ f'(x) = 1-f(x)^2", {
  x: 0.5, y: 1.6, w: 5.5, h: 0.4,
  align: "left", fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
// Cream box with x=0 values
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.5, y: 1.6, w: 4.0, h: 0.4,
  fill: { color: "FDF2E9" }, line: { color: "C00000", width: 1 },
});
s.addText("at x=0   f(0)=0     f'(0)=1", {
  x: 6.5, y: 1.6, w: 4.0, h: 0.4,
  align: "center", valign: "middle", fontSize: 13, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Shared chart header
s.addText("Sigmoid vs Tanh", {
  x: 0.5, y: 2.3, w: 12.33, h: 0.4,
  align: "center", fontSize: 16, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Left chart: Sigmoid vs Tanh
s.addImage({
  path: "slide_026_sigmoid_tanh.png",
  x: 0.5, y: 2.8, w: 5.5, h: 3.5,
});

// Right chart: Derivatives
s.addImage({
  path: "slide_026_derivatives.png",
  x: 6.5, y: 2.8, w: 5.5, h: 3.5,
});

// Footer box with points [1] and [2]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 6.5, w: 12.33, h: 0.7,
  fill: { color: "FFFFFF" }, line: { color: "E74C3C", width: 2 },
});
s.addText(
  "[1] The range of the sigmoid function is fixed at 0 to 1, whereas the range of the tanh function is fixed at -1 to 1.\n[2] The sigmoid function has a slower rate of change than the tanh function, which means that the derivative of the sigmoid function will be smaller than the derivative of the tanh function for a given input",
  {
    x: 0.6, y: 6.5, w: 12.13, h: 0.7,
    fontSize: 10, color: "333333", fontFace: FONT, margin: 0.1,
  }
);

const outPath = "slide_026_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));