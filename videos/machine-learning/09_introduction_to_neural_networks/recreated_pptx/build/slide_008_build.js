// Pattern: house-chrome + slide 008 content (Multi-Class One-vs-All classification diagram)
// Build: NODE_PATH=$(npm root -g) node slide_008_build.js
const pptxgen = require("pptxgenjs");

const NUM = 8;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };  // house template background

// ===== HOUSE CHROME (non-negotiable) =====

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge (yellow oval + centered bold numeral) - numeral = printed number (8)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. title - three segments: red, blue, red per validation
s.addText([
  { text: "Multi-Class Classification using ", options: { color: "C0392B", bold: true, fontSize: 28, fontFace: FONT } },
  { text: "[ONE VS ALL] ", options: { color: "21618C", bold: true, fontSize: 28, fontFace: FONT } },
  { text: "Binary Classifiers", options: { color: "C0392B", bold: true, fontSize: 28, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "top", margin: 0,
});

// 4. bottom black bar (video player overlay)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.0, y: H - 0.2, w: W, h: 0.2,
  fill: { color: "000000" },
  line: { type: "none" },
});

// ===== SLIDE 008 CONTENT (coordinates from vision analysis of 960x540 original) =====
// Conversion: 960x540 -> 13.33x7.5, SX=SY=0.01389

// Plot frame: measured from original at x=[175,790], y=[120,510]
// In inches: x=[2.43, 10.97], y=[1.67, 7.08], w=8.54, h=5.41
const plotX = 2.43;
const plotY = 1.67;
const plotW = 8.54;
const plotH = 5.41;

s.addShape(pres.shapes.RECTANGLE, {
  x: plotX, y: plotY, w: plotW, h: plotH,
  fill: { color: "FFFFFF" }, line: { color: "C0392B", width: 2 },
});

// Axes inside plot frame - origin at [315, 420] = 4.38in, 5.83in
// X axis points RIGHT from origin to plot right edge [780, 420] = 10.83in
// Y axis points UP from origin to plot top edge [315, 145] = 2.01in
const axisOriginX = 4.38;
const axisOriginY = 5.83;

// X axis with arrow pointing RIGHT
s.addShape(pres.shapes.LINE, {
  x: axisOriginX, y: axisOriginY, w: plotX + plotW - 0.05 - axisOriginX, h: 0,
  line: { color: "000000", width: 1.5, headEndType: "triangle", headEndSize: 8 },
});

// Y axis with arrow pointing UP (negative h in pptxgen means UP)
s.addShape(pres.shapes.LINE, {
  x: axisOriginX, y: plotY + 0.05, w: 0, h: plotY + 0.05 - axisOriginY,
  line: { color: "000000", width: 1.5, headEndType: "triangle", headEndSize: 8 },
});

// --- Class clusters (dots) ---
// C1: Green center [480,210] = 6.67in, 2.92in
// C2: Blue center [630,360] = 8.75in, 5.00in
// C3: Red center [380,390] = 5.28in, 5.42in

function addDotCluster(slide, cx, cy, radius, color, count, spreadX, spreadY) {
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * 2 * Math.PI;
    const r = Math.sqrt(Math.random()) * radius;
    const x = cx + r * Math.cos(angle) * spreadX;
    const y = cy + r * Math.sin(angle) * spreadY;
    slide.addShape(pres.shapes.OVAL, {
      x: x, y: y, w: 0.07, h: 0.07,
      fill: { color: color }, line: { type: "none" },
    });
  }
}

// C1 cluster: upper area (~9 dots)
addDotCluster(s, 6.67, 2.92, 0.5, "2ECC71", 9, 1.2, 1.0);
// C2 cluster: right area (~11 dots)
addDotCluster(s, 8.75, 5.00, 0.55, "2980B9", 11, 1.0, 1.2);
// C3 cluster: lower-left area (~7 dots)
addDotCluster(s, 5.28, 5.42, 0.45, "C0392B", 7, 1.0, 0.8);

// --- Decision boundaries (arrows) ---
// Red d1(x): [260,180] to [630,500] = 3.61in, 2.50in to 8.75in, 6.94in
s.addShape(pres.shapes.LINE, {
  x: 3.61, y: 2.50, w: 5.14, h: 4.44,
  line: { color: "C0392B", width: 2, headEndType: "triangle", headEndSize: 10 },
});
// label d1(x) at [290,380] = 4.03in, 5.28in
s.addText("d1(x)", {
  x: 4.03, y: 5.28, w: 1.0, h: 0.3,
  align: "center", valign: "top",
  fontSize: 14, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// Blue (unlabeled): [380,500] to [690,130] = 5.28in, 6.94in to 9.58in, 1.81in
s.addShape(pres.shapes.LINE, {
  x: 5.28, y: 6.94, w: 4.30, h: -5.13,
  line: { color: "2980B9", width: 2, headEndType: "triangle", headEndSize: 10 },
});

// Green d3(x): [200,380] to [790,350] = 2.78in, 5.28in to 10.97in, 4.86in
s.addShape(pres.shapes.LINE, {
  x: 2.78, y: 5.28, w: 8.19, h: -0.42,
  line: { color: "2ECC71", width: 2, headEndType: "triangle", headEndSize: 10 },
});
// label d3(x) at [760,390] = 10.56in, 5.42in
s.addText("d3(x)", {
  x: 10.56, y: 5.42, w: 1.0, h: 0.3,
  align: "center", valign: "top",
  fontSize: 14, bold: true, color: "2ECC71", fontFace: FONT, margin: 0,
});

// --- Yellow class label boxes ---
// C1 at [560,185] = 7.78in, 2.57in
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.78 - 0.25, y: 2.57 - 0.15, w: 0.5, h: 0.3,
  fill: { color: "F1C40F" }, line: { color: "000000", width: 1 },
});
s.addText("C1", {
  x: 7.78 - 0.25, y: 2.57 - 0.15, w: 0.5, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// C2 at [650,335] = 9.03in, 4.65in
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.03 - 0.25, y: 4.65 - 0.15, w: 0.5, h: 0.3,
  fill: { color: "F1C40F" }, line: { color: "000000", width: 1 },
});
s.addText("C2", {
  x: 9.03 - 0.25, y: 4.65 - 0.15, w: 0.5, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// C3 at [285,445] = 3.96in, 6.18in
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.96 - 0.25, y: 6.18 - 0.15, w: 0.5, h: 0.3,
  fill: { color: "F1C40F" }, line: { color: "000000", width: 1 },
});
s.addText("C3", {
  x: 3.96 - 0.25, y: 6.18 - 0.15, w: 0.5, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// --- Orange "?" boxes (4 locations) ---
const qBoxes = [
  { x: 3.96, y: 4.44 },   // [285,320]
  { x: 6.60, y: 5.07 },   // [475,365]
  { x: 9.51, y: 3.33 },   // [685,240]
  { x: 6.81, y: 6.81 },   // [490,490]
];

for (const qb of qBoxes) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: qb.x - 0.15, y: qb.y - 0.15, w: 0.3, h: 0.3,
    fill: { color: "E67E22" }, line: { color: "000000", width: 1 },
  });
  s.addText("?", {
    x: qb.x - 0.15, y: qb.y - 0.15, w: 0.3, h: 0.3,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}

// --- "+ve" labels (3) ---
// [300,395] = 4.17in, 5.49in (near green line left)
s.addText("+ve", {
  x: 4.17, y: 5.49, w: 0.6, h: 0.25,
  align: "left", valign: "top",
  fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// [755,265] = 10.49in, 3.68in (near blue line top-right)
s.addText("+ve", {
  x: 10.49, y: 3.68, w: 0.6, h: 0.25,
  align: "left", valign: "top",
  fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// [560,485] = 7.78in, 6.74in (near red line bottom)
s.addText("+ve", {
  x: 7.78, y: 6.74, w: 0.6, h: 0.25,
  align: "left", valign: "top",
  fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// --- Hatched regions (diagonal lines \ top-left to bottom-right) ---
// Simulated with many short diagonal lines across the plot
for (let i = 0; i < 60; i++) {
  const x = plotX + (plotW * i / 60);
  const yStart = plotY + 0.2 + (i % 2) * 0.1;
  const yEnd = yStart + 0.5;
  s.addShape(pres.shapes.LINE, {
    x: x, y: yStart, w: 0.3, h: 0.5,
    line: { color: "999999", width: 0.4 },
  });
}

// --- "Undefined" box at [95,145] = 1.32in, 2.01in (top-left outside plot) ---
const undefX = 1.32;
const undefY = 2.01;
s.addShape(pres.shapes.RECTANGLE, {
  x: undefX, y: undefY, w: 0.83, h: 0.42,
  fill: { color: "D5F5E3" }, line: { color: "000000", width: 1 },
});
s.addText("Undefined", {
  x: undefX, y: undefY, w: 0.83, h: 0.42,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Leader lines from Undefined box into plot (thin red lines)
// Box right edge at undefX+0.83 = 2.15, center y = undefY+0.21 = 2.22
// Point toward left boundary region
s.addShape(pres.shapes.LINE, {
  x: 2.15, y: 2.22, w: 0.3, h: 0.5,
  line: { color: "C0392B", width: 0.75 },
});
s.addShape(pres.shapes.LINE, {
  x: 2.15, y: 2.22, w: 0.5, h: 1.0,
  line: { color: "C0392B", width: 0.75 },
});

// --- "New Class" box at [775,380] = 10.77in, 5.28in (middle-right outside plot) ---
const newClassX = 10.77;
const newClassY = 5.28;
s.addShape(pres.shapes.RECTANGLE, {
  x: newClassX, y: newClassY - 0.15, w: 1.5, h: 0.55,
  fill: { color: "D7BDE2" }, line: { color: "8E44AD", width: 1 },
});
s.addText("New Class", {
  x: newClassX, y: newClassY - 0.15, w: 1.5, h: 0.55,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_008_recreated.pptx" 
}).then(() => console.log("wrote slide_008_recreated.pptx"));