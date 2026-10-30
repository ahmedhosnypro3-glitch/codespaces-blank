// Pattern: house-chrome + equations-mathtext-png + highlight-box
// Slide 12: "At Output Layer" - Neural network output layer diagram with equations
// Run: NODE_PATH=$(npm root -g) node slide_012.js -> slide_012_recreated.pptx
// FIXES from judge attempt 4:
// 1. w_ji label on EVERY connection line (9 total: 3 inputs × 3 δ_j)
// 2. SINGLE upward arrow (not double-headed) under BOTTOM δ_j circle
// 3. Uppercase O_j in def box: δ_j = O_j(1-O_j)(t_j - O_j)

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const NUM = 12;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. outer red house frame - HOUSE CHROME
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge - HOUSE CHROME
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title at HOUSE CHROME position
s.addText("At Output Layer", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Load equation metadata
const eqF1 = JSON.parse(fs.readFileSync("assets/slide_012/eq_f1.png.meta.json", "utf8"));
const eqF2 = JSON.parse(fs.readFileSync("assets/slide_012/eq_f2.png.meta.json", "utf8"));
const eqF3 = JSON.parse(fs.readFileSync("assets/slide_012/eq_f3.png.meta.json", "utf8"));
const eqF4 = JSON.parse(fs.readFileSync("assets/slide_012/eq_f4.png.meta.json", "utf8"));
const eqDef1 = JSON.parse(fs.readFileSync("assets/slide_012/eq_def_line1.png.meta.json", "utf8"));
const eqDef2 = JSON.parse(fs.readFileSync("assets/slide_012/eq_def_line2.png.meta.json", "utf8"));

// Diagram area
const diagLeft = 1.5;
const diagTop = 1.5;
const diagWidth = 10.0;
const diagHeight = 3.5;

const leftX = diagLeft + 0.8;
const centerX = leftX + 2.5;
const errorX = centerX + 1.5;
const rightX = errorX + 0.8;

const circleY = [diagTop + 0.6, diagTop + 1.55, diagTop + 2.5];
const circleR = 0.35;

// Left column: O_i
circleY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: leftX - circleR, y: y - circleR, w: circleR * 2, h: circleR * 2,
    fill: { color: "90EE90" }, line: { color: "000000", width: 1 },
  });
  s.addText("O_i", {
    x: leftX - 0.6, y: y - 0.5, w: 1.2, h: 0.4,
    align: "center", valign: "bottom",
    fontSize: 12, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
});

// Center column: δ_j circles with O_j label
circleY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: centerX - circleR, y: y - circleR, w: circleR * 2, h: circleR * 2,
    fill: { color: "D2B48C" }, line: { color: "000000", width: 1 },
  });
  s.addText("δ_j", {
    x: centerX - 0.6, y: y - circleR, w: 1.2, h: circleR * 2,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  s.addText("O_j", {
    x: centerX + circleR + 0.1, y: y - 0.2, w: 0.6, h: 0.4,
    align: "left", valign: "middle",
    fontSize: 12, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
});

// Error box
const errorY = diagTop + 0.2;
const errorH = diagHeight - 0.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: errorX, y: errorY, w: 0.5, h: errorH,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});
s.addText("Error", {
  x: errorX + 0.05, y: errorY + errorH/2 - 0.3, w: 0.4, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0,
  rotate: -90,
});

// Right: t_j rectangles
const rectW = 0.6, rectH = 0.5;
circleY.forEach((y, i) => {
  const ry = y - rectH/2;
  s.addShape(pres.shapes.RECTANGLE, {
    x: rightX, y: ry, w: rectW, h: rectH,
    fill: { color: "ADD8E6" }, line: { color: "000000", width: 1 },
  });
  s.addText("t_j", {
    x: rightX + 0.05, y: ry + 0.05, w: rectW - 0.1, h: rectH - 0.1,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0.05,
  });
  s.addShape(pres.shapes.OVAL, {
    x: rightX - 0.1, y: y - 0.05, w: 0.1, h: 0.1,
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  });
});

// FAN-IN connections: ALL O_i to ALL δ_j with w_ji on EACH
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    const x1 = leftX + circleR;
    const y1 = circleY[i];
    const x2 = centerX - circleR;
    const y2 = circleY[j];
    s.addShape(pres.shapes.LINE, {
      x: x1, y: y1, w: x2 - x1, h: y2 - y1,
      line: { color: "0000FF", width: 1, headEndType: "triangle" },
    });
    // w_ji label on EACH connection (near middle)
    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2;
    s.addText("w_ji", {
      x: mx - 0.3, y: my - 0.2, w: 0.6, h: 0.3,
      align: "center", valign: "bottom",
      fontSize: 9, bold: false, color: "0000FF", fontFace: FONT, margin: 0,
    });
  }
}

// δ_j to Error box
for (let i = 0; i < 3; i++) {
  const x1 = centerX + circleR;
  const y1 = circleY[i];
  const x2 = errorX;
  const y2 = circleY[i];
  s.addShape(pres.shapes.LINE, {
    x: x1, y: y1, w: x2 - x1, h: 0,
    line: { color: "FF0000", width: 1.5, headEndType: "triangle" },
  });
}

// Error box to t_j
for (let i = 0; i < 3; i++) {
  const x1 = errorX + 0.5;
  const y1 = circleY[i];
  const x2 = rightX;
  const ry = circleY[i] - rectH/2;
  s.addShape(pres.shapes.LINE, {
    x: x1, y: y1, w: x2 - x1, h: 0,
    line: { color: "FF0000", width: 1.5, headEndType: "triangle" },
  });
}

// SINGLE upward arrow under BOTTOM δ_j circle (third one)
const arrowX = centerX;
const arrowY = circleY[2] + circleR + 0.08;
s.addText("\u2191", {  // single upward arrow
  x: arrowX - 0.1, y: arrowY, w: 0.2, h: 0.2,
  align: "center", valign: "bottom",
  fontSize: 14, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
});

// Diagram frame and column separators
s.addShape(pres.shapes.RECTANGLE, {
  x: diagLeft - 0.1, y: diagTop - 0.1, w: diagWidth + 0.2, h: diagHeight + 0.2,
  fill: { type: "none" }, line: { color: "FF0000", width: 1 },
});
const sep1x = (leftX + centerX)/2;
const sep2x = (centerX + errorX)/2;
const sep3x = (errorX + rightX)/2 + 0.1;
[sep1x, sep2x, sep3x].forEach(sepX => {
  s.addShape(pres.shapes.LINE, {
    x: sepX, y: diagTop - 0.1, w: 0, h: diagHeight + 0.2,
    line: { color: "CCCCCC", width: 0.5, dashType: "dash" },
  });
});

// Formula strip inside diagram frame
const formulaY = diagTop + diagHeight - 0.35;
const formulaH = 0.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: diagLeft, y: formulaY, w: diagWidth, h: formulaH,
  fill: { color: "CCFFCC" }, line: { color: "008000", width: 1 },
});

// Color-coded formula pieces
const formulaX = diagLeft + 0.5;
const formulaGap = 0.05;
let curX = formulaX;
const formulaTop = formulaY + (formulaH - eqF1.h_in) / 2;

s.addImage({ path: "assets/slide_012/eq_f1.png", x: curX, y: formulaTop, w: eqF1.w_in, h: eqF1.h_in });
curX += eqF1.w_in + formulaGap;
s.addImage({ path: "assets/slide_012/eq_f2.png", x: curX, y: formulaTop, w: eqF2.w_in, h: eqF2.h_in });
curX += eqF2.w_in + formulaGap;
s.addImage({ path: "assets/slide_012/eq_f3.png", x: curX, y: formulaTop, w: eqF3.w_in, h: eqF3.h_in });
curX += eqF3.w_in + formulaGap;
s.addImage({ path: "assets/slide_012/eq_f4.png", x: curX, y: formulaTop, w: eqF4.w_in, h: eqF4.h_in });

// Definition box
const defX = diagLeft;
const defY = diagTop + diagHeight + 0.2;
const defW = 5.0;
const defH = 0.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: defX, y: defY, w: defW, h: defH,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});

const def1x = defX + 0.2;
const def1y = defY + 0.1;
s.addImage({ path: "assets/slide_012/eq_def_line1.png", x: def1x, y: def1y, w: eqDef1.w_in, h: eqDef1.h_in });

s.addText("Where:", {
  x: defX + 0.2, y: def1y + eqDef1.h_in + 0.05, w: 0.8, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 14, bold: false, color: "000000", fontFace: FONT, margin: 0,
});
const def2x = defX + 0.2 + 0.9;
const def2y = def1y + eqDef1.h_in + 0.05;
s.addImage({ path: "assets/slide_012/eq_def_line2.png", x: def2x, y: def2y, w: eqDef2.w_in, h: eqDef2.h_in });

pres.writeFile({ fileName: "slide_012_recreated.pptx" })
  .then(() => console.log("wrote slide_012_recreated.pptx"))
  .catch(err => console.error(err));