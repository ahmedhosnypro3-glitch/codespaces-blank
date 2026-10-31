// Slide 25: Vanishing and Exploding Gradients (house-chrome ML family)
const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const NUM = 25;
const FONT = "Arial";
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/qa/slide025/assets";

let s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Vanishing and Exploding Gradients", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Blue section header
s.addText("Long Chain of Derivatives", {
  x: 0.87, y: 1.72, w: 3.4, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 18, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// Equation boxes (peach + cream) with 2D mathtext PNGs
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.66, y: 2.25, w: 3.34, h: 0.95,
  fill: { color: "FFE6CC" }, line: { color: "E8C9A0", width: 0.75 },
});
s.addImage({ path: `${ASSETS}/eq25_1.png`, x: 0.74, y: 2.35, w: 3.15 });
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.66, y: 3.30, w: 3.01, h: 0.87,
  fill: { color: "FFF2CC" }, line: { color: "E8DFA0", width: 0.75 },
});
s.addImage({ path: `${ASSETS}/eq25_2.png`, x: 0.74, y: 3.39, w: 2.85 });

// ---- Neural network diagram ----
const ROWY = [2.06, 2.78, 3.61];       // node row centers (in)
const IN_X = 4.70, H1_X = 6.90, AC_X = 8.30, H2_X = 9.70, OUT_X = 10.75;
const YEL = "FFD966", GRN = "00AA00", PUR = "800080", BLU = "0000FF";

function circle(cx, cy, d, fill, lineColor) {
  s.addShape(pres.shapes.OVAL, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d,
    fill: { color: fill }, line: { color: lineColor || "000000", width: 1 },
  });
}
function link(x1, y1, x2, y2) {
  // pptxgenjs LINE draws a diagonal across its bounding box
  s.addShape(pres.shapes.LINE, {
    x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color: "9A9A9A", width: 0.75 },
  });
}

// input dots (purple), hidden layer 1 (yellow Sigma), activations (green),
// hidden layer 2 (yellow Sigma), outputs (blue) + labels
for (const y of ROWY) {
  circle(IN_X, y, 0.18, PUR);
  circle(H1_X, y, 0.45, YEL);
  circle(AC_X, y, 0.35, GRN, "006600");
  circle(H2_X, y, 0.45, YEL);
  circle(OUT_X, y, 0.32, BLU, "000066");
}
for (const y of ROWY) {
  s.addText("Σ", {
    x: H1_X - 0.2, y: y - 0.16, w: 0.4, h: 0.32, align: "center", valign: "middle",
    fontSize: 16, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  s.addText("Σ", {
    x: H2_X - 0.2, y: y - 0.16, w: 0.4, h: 0.32, align: "center", valign: "middle",
    fontSize: 16, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    link(IN_X + 0.09, ROWY[i], H1_X - 0.225, ROWY[j]);
    link(H1_X + 0.225, ROWY[i], AC_X - 0.175, ROWY[j]);
    link(AC_X + 0.175, ROWY[i], H2_X - 0.225, ROWY[j]);
    link(H2_X + 0.225, ROWY[i], OUT_X - 0.16, ROWY[j]);
  }
}
const OUTL = ["Output 1", "Output 2", "Output m"];
ROWY.forEach((y, i) => {
  s.addText(OUTL[i], {
    x: OUT_X + 0.18, y: y - 0.1, w: 0.85, h: 0.22,
    align: "left", valign: "middle",
    fontSize: 10, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
});

// vertical red Error bar + Class labels
s.addShape(pres.shapes.RECTANGLE, {
  x: 11.68, y: 1.78, w: 0.22, h: 2.17, fill: { color: "C00000" }, line: { color: "C00000", width: 0.5 },
});
s.addText("Error\nError\nError", {
  x: 11.60, y: 1.85, w: 0.42, h: 2.0,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
const CLS = ["Class 1", "Class 2", "Class m"];
ROWY.forEach((y, i) => {
  s.addText(CLS[i], {
    x: 12.07, y: y - 0.1, w: 0.6, h: 0.22,
    align: "left", valign: "middle",
    fontSize: 10, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
});

// Node Bias icon + label; red 1.0 annotation
circle(4.73, 3.90, 0.42, PUR);
s.addText("Node Bias", {
  x: 5.02, y: 3.80, w: 1.0, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 10, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
s.addText("1.0", {
  x: 7.68, y: 3.82, w: 0.5, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- Bottom charts ----
s.addText("Exploding Gradients", {
  x: 1.43, y: 4.46, w: 2.2, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: `${ASSETS}/chart25_relu.png`, x: 0.75, y: 4.83, w: 3.6, h: 2.4 });

s.addText("Vanishing Gradients", {
  x: 7.65, y: 4.68, w: 2.2, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: `${ASSETS}/chart25_sigtanh.png`, x: 5.10, y: 5.05, w: 7.26, h: 2.04 });

pres.writeFile({ fileName: "slide_025_recreated.pptx" })
  .then(() => console.log("wrote slide_025_recreated.pptx"));
