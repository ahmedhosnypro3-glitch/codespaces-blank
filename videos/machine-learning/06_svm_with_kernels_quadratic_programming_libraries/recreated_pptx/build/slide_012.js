const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_012");
const W = 13.33, H = 7.5;
const SERIF = "Times New Roman";
const RED = "CC0000", BLUE = "0000CC", PINK = "FBEEEE";

const X = v => v * W, Y = v => v * H;
const box = r => ({ x: X(r[0]), y: Y(r[1]), w: (r[2] - r[0]) * W, h: (r[3] - r[1]) * H });

function eqImg(slide, name, r) {
  const meta = JSON.parse(fs.readFileSync(path.join(EQ, name + ".json")));
  const b = box(r);
  slide.addImage({
    path: path.join(EQ, name + ".png"),
    x: b.x + (b.w - meta.w_in) / 2, y: b.y + (b.h - meta.h_in) / 2,
    w: meta.w_in, h: meta.h_in,
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (mandatory, overrides spec)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("12", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
// SLIDE_TITLE: none — no title text added.

// Letterbox black band
s.addShape(pres.shapes.RECTANGLE, {
  ...box([0.039, 0.907, 0.921, 1.000]),
  fill: { color: "000000" }, line: { type: "none" },
});

// Upper and lower pale-pink panels
s.addShape(pres.shapes.RECTANGLE, {
  ...box([0.071, 0.122, 0.849, 0.380]),
  fill: { color: PINK }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  ...box([0.073, 0.463, 0.880, 0.615]),
  fill: { color: PINK }, line: { color: RED, width: 1.5 },
});

// Labels
s.addText("Minimise:", {
  ...box([0.078, 0.143, 0.146, 0.172]),
  fontSize: 13, bold: true, italic: true, color: RED, fontFace: SERIF, margin: 0,
});
s.addText("Subject to:", {
  ...box([0.076, 0.204, 0.146, 0.233]),
  fontSize: 13, bold: true, color: RED, fontFace: SERIF, margin: 0,
});
s.addText("Minimise:", {
  ...box([0.078, 0.500, 0.146, 0.530]),
  fontSize: 13, bold: true, italic: true, color: RED, fontFace: SERIF, margin: 0,
});
// Upper objective (red, two lines — no 1/2 factor in the original)
eqImg(s, "r1", [0.154, 0.141, 0.833, 0.176]);
eqImg(s, "r2", [0.167, 0.183, 0.833, 0.219]);

// Three small white constraint boxes with red borders
const cBoxes = [[0.079, 0.235, 0.120, 0.281], [0.079, 0.291, 0.120, 0.331], [0.079, 0.335, 0.120, 0.376]];
cBoxes.forEach(b => s.addShape(pres.shapes.RECTANGLE, {
  ...box(b), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
}));
eqImg(s, "e3", cBoxes[0]);
eqImg(s, "e5", cBoxes[1]);
eqImg(s, "e7", cBoxes[2]);
eqImg(s, "e4", [0.170, 0.246, 0.300, 0.274]);
eqImg(s, "e6b", [0.172, 0.294, 0.400, 0.319]);
eqImg(s, "e8b", [0.172, 0.343, 0.405, 0.367]);

// Red heading right of constraints
s.addText("Quadratic Equation in \u03b1 with constraints", {
  ...box([0.438, 0.296, 0.802, 0.328]),
  fontSize: 18, bold: true, color: RED, fontFace: SERIF, margin: 0, valign: "middle",
});

// Amber rounded rectangle with compact objective
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  ...box([0.719, 0.380, 0.863, 0.454]),
  fill: { color: "FFFFFF" }, line: { color: "E8A33D", width: 1.5 },
});
eqImg(s, "e9b", [0.717, 0.380, 0.865, 0.454]);

// Lower panel: green stacked 1/2 + red objective in two lines
eqImg(s, "half", [0.149, 0.485, 0.165, 0.541]);
eqImg(s, "r10", [0.172, 0.496, 0.870, 0.533]);
eqImg(s, "r11", [0.175, 0.556, 0.870, 0.593]);

// P matrix box (blue border) + matrix image
s.addShape(pres.shapes.RECTANGLE, {
  ...box([0.100, 0.630, 0.354, 0.815]),
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 },
});
eqImg(s, "p_matrix", [0.111, 0.637, 0.349, 0.807]);

// Light-blue arrow pointing down-left toward the q^T box
s.addShape(pres.shapes.LINE, {
  ...box([0.445, 0.676, 0.461, 0.706]),
  flipHorizontal: true,
  line: { color: "8FB4DE", width: 1.5, endArrowType: "triangle" },
});

// q^T box (blue border) + row vector
s.addShape(pres.shapes.RECTANGLE, {
  ...box([0.461, 0.689, 0.716, 0.769]),
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 },
});
eqImg(s, "e13", [0.490, 0.699, 0.700, 0.750]);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_012_recreated.pptx") })
  .then(() => console.log("wrote slide_012_recreated.pptx"))
  .catch(e => console.error(e));
