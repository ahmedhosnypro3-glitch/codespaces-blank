// slide_040.js — 6-panel SVM dataset grid (Aggregation, Compound, Spiral, Pathbased, Flame, Jain)
// House frame + 6 scatter plots from vision analysis + doc-parse data
// Run: NODE_PATH=$(npm root -g) node slide_040.js

const pptxgen = require("pptxgenjs");

const NUM = 40;
const TITLE = "Check class of each background point\nin the following datasets";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House red frame (0.15in inset)
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
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (2 lines)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.75,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
  lineSpacing: 1.0,
});

// 4. Bottom black footer bar (house chrome override: footer is part of original)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: H - 0.15 - 0.35, w: W - 0.3, h: 0.35,
  fill: { color: "000000" }, line: { type: "none" },
});

// 5. Panel layout: 3x2 grid below title
// Title ends at ~y=1.03, start panels at y=1.15
// Each panel: w=4.0, h=2.7, gap=0.2
const panelW = 4.0;
const panelH = 2.7;
const gapX = 0.2;
const gapY = 0.2;
const startX = 0.55;
const startY = 1.15;

const panels = [
  { name: "Aggregation.txt", row: 0, col: 0, clusters: [
    {color: "0000FF", pts: [[10,24],[12,25],[11,23],[9,26]]},  // blue upper-left
    {color: "00FFFF", pts: [[30,25],[28,24],[32,26]]},           // cyan upper-right
    {color: "FF0000", pts: [[15,15],[16,14]]},                    // red small
    {color: "FFFF00", pts: [[20,12],[21,11]]},                    // yellow small
    {color: "FF00FF", pts: [[22,8],[24,7],[23,9],[21,8],[25,7]]}, // magenta large lower-middle
    {color: "000000", pts: [[35,5],[34,6]]},                       // black lower-right
    {color: "00FF00", pts: [[5,5],[6,4]]}                          // green tiny lower-left
  ]},
  { name: "Compound.txt", row: 0, col: 1, clusters: [
    {color: "000000", pts: [[8,20],[10,18],[9,22],[7,19]]},      // black left
    {color: "FF00FF", pts: [[12,15],[13,14],[11,16]]},            // magenta center-left
    {color: "00FF00", pts: [[10,8],[11,9],[12,8],[9,9],[10,10]]}, // green ring lower-left
    {color: "0000FF", pts: [[32,22],[33,23],[31,21]]},            // blue blob upper-right
    {color: "FF0000", pts: [[38,10],[39,12],[37,11]]}             // red dotted right
  ]},
  { name: "Spiral.txt", row: 0, col: 2, clusters: [
    // Spiral pattern - interleaved spirals of blue, red, black
    {color: "0000FF", pts: [[15,25],[16,24],[17,25],[18,24],[19,23]]},
    {color: "FF0000", pts: [[20,22],[21,23],[22,22],[23,21]]},
    {color: "000000", pts: [[24,20],[25,19],[26,20]]},
    {color: "0000FF", pts: [[27,18],[28,19],[29,18]]},
    {color: "FF0000", pts: [[30,17],[31,16]]},
    {color: "000000", pts: [[32,15],[33,14]]}
  ]},
  { name: "Pathbased.txt", row: 1, col: 0, clusters: [
    {color: "FF0000", pts: [[10,25],[12,24],[14,25],[16,24],[18,25]]}, // red spiral/ring
    {color: "0000FF", pts: [[15,15],[16,14]]},                       // blue center-left
    {color: "000000", pts: [[28,15],[29,16]]},                       // black center-right
    {color: "FF0000", pts: [[20,10],[22,9],[24,10]]}                 // red dotted trailing
  ]},
  { name: "Flame.txt", row: 1, col: 1, clusters: [
    {color: "0000FF", pts: [[8,25],[10,23],[12,21],[14,19],[16,17]]}, // blue flame left
    {color: "0000FF", pts: [[32,25],[30,23],[28,21],[26,19]]},       // blue flame right
    {color: "FF0000", pts: [[20,24],[21,23],[22,24]]}                // red top-center
  ]},
  { name: "Jain.txt", row: 1, col: 2, clusters: [
    {color: "0000FF", pts: [[10,22],[11,21],[9,23]]},                // blue upper-left
    {color: "FF0000", pts: [[28,18],[30,16],[32,18],[34,20],[32,22]]} // red C-shape right
  ]}
];

// X and Y scales for all panels (0-40 x, -10 to 40 y based on vision)
const X_MIN = 0, X_MAX = 40;
const Y_MIN = -10, Y_MAX = 40;

panels.forEach(p => {
  const px = startX + p.col * (panelW + gapX);
  const py = startY + p.row * (panelH + gapY);
  
  // Label box (rounded rectangle, light blue fill, blue border, dark blue text)
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: px, y: py - 0.35, w: panelW, h: 0.3,
    fill: { color: "D6E4F0" },  // light blue
    line: { color: "0000FF", width: 0.75 },
  });
  s.addText(p.name, {
    x: px, y: py - 0.35, w: panelW, h: 0.3,
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: "000080", fontFace: FONT, margin: 0,
  });
  
  // Plot area (white square with red border)
  s.addShape(pres.shapes.RECTANGLE, {
    x: px, y: py, w: panelW, h: panelH,
    fill: { color: "FFFFFF" },
    line: { color: "FF0000", width: 1.0 },
  });
  
  // Plot clusters as small ovals
  p.clusters.forEach(cluster => {
    cluster.pts.forEach(pt => {
      const xNorm = (pt[0] - X_MIN) / (X_MAX - X_MIN);
      const yNorm = (pt[1] - Y_MIN) / (Y_MAX - Y_MIN);
      const cx = px + xNorm * panelW;
      const cy = py + panelH - yNorm * panelH;
      s.addShape(pres.shapes.OVAL, {
        x: cx - 0.05, y: cy - 0.05, w: 0.1, h: 0.1,
        fill: { color: cluster.color }, line: { type: "none" },
      });
    });
  });
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_040_recreated.pptx" 
}).then(() => console.log("wrote slide_040_recreated.pptx"))
.catch(err => console.error(err));