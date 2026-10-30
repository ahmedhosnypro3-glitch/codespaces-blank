// slide_017.js — Neural Network Model (slide 17) — rebuild v2 per judge + precise analysis
// Patterns: house-chrome, equations-mathtext-png, highlight-box
// Equations pre-rendered by render_eq.py (eq1_s17, eq2_s17, eq3_s17); sigmoids: sig_red/green/orange

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 17;
const TITLE = "Neural Network Model";
const SUB = [
  { text: "(Effect of ", color: "0000CC" },
  { text: "Net_k", color: "CC0000" },
  { text: " on Calculated Error is known from O/P Layer)", color: "0000CC" },
];

const BG = "E8E8E8";        // house chrome overrides the original's white page
const PANEL = "F7F1E4";     // pale-cream diagram panel (inner)
const TITLE_COLOR = "CC0000";
const FRAME = "C00000";

const EQ1 = JSON.parse(fs.readFileSync("eq1_s17.json"));
const EQ2 = JSON.parse(fs.readFileSync("eq2_s17.json"));
const EQ3 = JSON.parse(fs.readFileSync("eq3_s17.json"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// HOUSE CHROME
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME, width: 1.5 },
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 26, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});
s.addText(SUB, {
  x: 0.6, y: 0.78, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 16, bold: true, fontFace: FONT, margin: 0,
});

// ========== GEOMETRY (measured from original 960x540 px; in = px * 13.33/960) ======
const PX = 13.33 / 960;
const PY = 7.5 / 540;
const X = (px) => px * PX;
const Y = (py) => py * PY;

// Pale-cream diagram panel (approx 60..840 x, 115..370 y)
s.addShape(pres.shapes.RECTANGLE, {
  x: X(60), y: Y(115), w: X(780), h: Y(255),
  fill: { color: PANEL }, line: { type: "none" },
});

// Magenta 'Input Sample' box (top-left) + 'Target Label' (top-right)
s.addShape(pres.shapes.RECTANGLE, {
  x: X(60), y: Y(90), w: X(62), h: Y(28),
  fill: { color: "FF99FF" }, line: { color: "CC00CC", width: 1 },
});
s.addText([{ text: "Input", options: { breakLine: true } }, { text: "Sample" }], {
  x: X(60), y: Y(90), w: X(62), h: Y(28),
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: X(765), y: Y(90), w: X(62), h: Y(28),
  fill: { color: "FF99FF" }, line: { color: "CC00CC", width: 1 },
});
s.addText([{ text: "Target", options: { breakLine: true } }, { text: "Label" }], {
  x: X(765), y: Y(90), w: X(62), h: Y(28),
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Dotted magenta arrows from the network out toward each box
s.addShape(pres.shapes.LINE, {
  x: X(122), y: Y(104), w: X(52), h: 0,
  line: { color: "CC00CC", width: 1, dashType: "dash", endArrowType: "triangle" },
});
s.addShape(pres.shapes.LINE, {
  x: X(765), y: Y(104), w: X(52), h: 0,
  line: { color: "CC00CC", width: 1, dashType: "dash", endArrowType: "triangle" },
});

// ========== NETWORK ROWS ==========
const ROWS = [170, 235, 310];
const SIG = 22;           // sigmoid square side (px)
const CIR = 24;           // sigma circle diameter (px)
const DOT = 8;            // solid red dot diameter (px)
const YEL = 18;           // yellow annotation circle diameter (px)

// per-row node x positions (px, from analysis)
const NX = {
  sigRed: 137, dot1: 157, sq1: 185, pale1: 200, pale2: 215,
  sigBlue: 240, dot2: 262, sq2: 305, dot3: 320,
  yelWij: 355, sigGreen: 400, yelNet: 430, sq3: 460, dot4: 475,
  yelWjk: 505, sigOrange: 545, yelNet2: 575, sq4: 605, dot5: 620,
};

const line = (x1, y1, x2, y2, color, width, dash, arrow) => {
  s.addShape(pres.shapes.LINE, {
    x: X(x1), y: Y(y1), w: X(x2 - x1), h: Y(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: color, width: width, dashType: dash || "solid",
            endArrowType: arrow || "none" },
  });
};

const sigCircle = (cx, py, edge, glyphColor) => {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx - CIR / 2), y: Y(py - CIR / 2), w: X(CIR), h: Y(CIR),
    fill: { color: "FFFFFF" }, line: { color: edge, width: 1.25 },
  });
  s.addText("Σ", {
    x: X(cx - CIR / 2), y: Y(py - CIR / 2), w: X(CIR), h: Y(CIR),
    align: "center", valign: "middle",
    fontSize: 14, color: glyphColor, fontFace: "Cambria Math", margin: 0,
  });
};

const redDot = (cx, py) => {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx - DOT / 2), y: Y(py - DOT / 2), w: X(DOT), h: Y(DOT),
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 0.5 },
  });
};

const sigBox = (cx, py, img) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(cx - SIG / 2), y: Y(py - SIG / 2), w: X(SIG), h: Y(SIG),
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
  });
  s.addImage({ path: img, x: X(cx - SIG / 2 + 2), y: Y(py - SIG / 2 + 2),
               w: X(SIG - 4), h: Y(SIG - 4) });
};

const yelCircle = (cx, py, txt, txtColor) => {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx - YEL / 2), y: Y(py - YEL / 2), w: X(YEL), h: Y(YEL),
    fill: { color: "FFFF99" }, line: { color: "000000", width: 0.75 },
  });
  s.addText(txt, {
    x: X(cx - YEL / 2), y: Y(py - YEL / 2), w: X(YEL), h: Y(YEL),
    align: "center", valign: "middle",
    fontSize: 7, bold: true, color: txtColor, fontFace: FONT, margin: 0,
  });
};

// ========== FAN-OUT CONNECTION LINES (drawn first, under the nodes) ==========
// Light-pink fully-connected lines from each O_i dot to all green Σ nodes
for (let r = 0; r < ROWS.length; r++) {
  const py = ROWS[r];
  for (let t = 0; t < ROWS.length; t++) {
    line(NX.dot3, py, NX.sigGreen, ROWS[t], "FFB6C1", 0.75);
    line(NX.dot4, py, NX.sigOrange, ROWS[t], "FFB6C1", 0.75);
  }
}
// Magenta input dots at far left with faint fan-out to the first Σ column
const IN_DOTS = [210, 230, 270];
for (const iy of IN_DOTS) {
  s.addShape(pres.shapes.OVAL, {
    x: X(75 - 5), y: Y(iy - 5), w: X(10), h: Y(10),
    fill: { color: "FF00FF" }, line: { color: "FF00FF", width: 0.5 },
  });
  for (const py of ROWS) line(75, iy, NX.sigRed, py, "FFB6C1", 0.75);
}

// ========== BLACK DASHED SKIP-CONNECTION ARCS ==========
const arc = (x1, y1, x2, y2) => {
  s.addShape(pres.shapes.ARC, {
    x: X(Math.min(x1, x2)), y: Y(Math.min(y1, y2)),
    w: X(Math.abs(x2 - x1)), h: Y(Math.abs(y2 - y1)),
    adjustPoint: 0.3,
    fill: { type: "none" },
    line: { color: "000000", width: 1, dashType: "dash" },
    rotate: 0,
  });
};
// Three arcs converging on the top orange Σ (from O_i / O_j of lower rows)
arc(NX.dot3, ROWS[1], NX.sigOrange, ROWS[0]);
arc(NX.dot4, ROWS[1], NX.sigOrange, ROWS[0]);
arc(NX.dot4, ROWS[2], NX.sigOrange, ROWS[0]);
// Arc rising from the bottom-row O_j to the middle orange Σ
arc(NX.dot4, ROWS[2], NX.sigOrange, ROWS[1]);

// ========== PER-ROW NODE CHAIN ==========
for (const py of ROWS) {
  // Previous-layer stage: red Σ circle, red dot, red sigmoid box, two pale circles
  sigCircle(NX.sigRed, py, "FF0000", "FF0000");
  redDot(NX.dot1, py);
  sigBox(NX.sq1, py, "sig_red.png");
  s.addShape(pres.shapes.OVAL, {
    x: X(NX.pale1 - 5), y: Y(py - 5), w: X(10), h: Y(10),
    fill: { color: "FFFFFF" }, line: { color: "C0C0C0", width: 0.75 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: X(NX.pale2 - 5), y: Y(py - 5), w: X(10), h: Y(10),
    fill: { color: "FFFFFF" }, line: { color: "C0C0C0", width: 0.75 },
  });
  // Blue Σ (previous layer i)
  sigCircle(NX.sigBlue, py, "0000CC", "0000CC");
  redDot(NX.dot2, py);
  // Red sigmoid with 'Net_i' label above, red dot with 'O_i' label above
  sigBox(NX.sq2, py, "sig_red.png");
  s.addText("Net_i", {
    x: X(NX.sq2 - 20), y: Y(py - 26), w: X(40), h: Y(12),
    align: "center", valign: "bottom",
    fontSize: 8, italic: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  redDot(NX.dot3, py);
  s.addText("O_i", {
    x: X(NX.dot3 - 15), y: Y(py - 26), w: X(30), h: Y(12),
    align: "center", valign: "bottom",
    fontSize: 8, italic: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  // Current layer j: yellow W_ij, green Σ, yellow Net, green sigmoid, red dot O_j
  yelCircle(NX.yelWij, py, "W_ij", "0000CC");
  sigCircle(NX.sigGreen, py, "00CC00", "00CC00");
  yelCircle(NX.yelNet, py, "Net", "FF0000");
  sigBox(NX.sq3, py, "sig_green.png");
  redDot(NX.dot4, py);
  s.addText("O_j", {
    x: X(NX.dot4 - 15), y: Y(py - 26), w: X(30), h: Y(12),
    align: "center", valign: "bottom",
    fontSize: 8, italic: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  // Next layer k: yellow W_jk, orange Σ, yellow Net, orange sigmoid, red dot O_k
  yelCircle(NX.yelWjk, py, "W_jk", "0000CC");
  sigCircle(NX.sigOrange, py, "FF6600", "FF6600");
  yelCircle(NX.yelNet2, py, "Net", "FF0000");
  sigBox(NX.sq4, py, "sig_orange.png");
  redDot(NX.dot5, py);
  s.addText("O_k", {
    x: X(NX.dot5 - 15), y: Y(py - 26), w: X(30), h: Y(12),
    align: "center", valign: "bottom",
    fontSize: 8, italic: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  // Blue dashed weight arrows (same row): O_i -> green Σ, O_j -> orange Σ
  line(NX.dot3 + 6, py, NX.sigGreen - CIR / 2 - 2, py, "0000FF", 1, "dash", "triangle");
  line(NX.dot4 + 6, py, NX.sigOrange - CIR / 2 - 2, py, "0000FF", 1, "dash", "triangle");
}

// Rotated blue weight labels along the dashed arrows (top row only, as in original)
s.addText("W_ij", {
  x: X(NX.dot3 + 6), y: Y(ROWS[0] - 26), w: X(38), h: Y(12),
  align: "center", valign: "middle", rot: 330,
  fontSize: 8, bold: true, color: "0000CC", fontFace: FONT, margin: 0,
});
s.addText("W_jk", {
  x: X(NX.dot4 + 6), y: Y(ROWS[0] - 26), w: X(38), h: Y(12),
  align: "center", valign: "middle", rot: 330,
  fontSize: 8, bold: true, color: "0000CC", fontFace: FONT, margin: 0,
});

// ========== OUTPUT BOXES (blue-outlined white boxes, one per row) ==========
for (let r = 0; r < ROWS.length; r++) {
  const labels = ["Output 1", "Output 2", "Output m"];
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(660), y: Y(ROWS[r] - 12), w: X(66), h: Y(24),
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1.25 },
  });
  s.addText(labels[r], {
    x: X(660), y: Y(ROWS[r] - 12), w: X(66), h: Y(24),
    align: "center", valign: "middle",
    fontSize: 10, bold: true, italic: true, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ========== ERROR BAR (tall dark-red bar, rotated white text) ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: X(735), y: Y(140), w: X(20), h: Y(200),
  fill: { color: "CC0000" }, line: { color: "CC0000", width: 1 },
});
s.addText("Error Error Error", {
  x: X(735 - 6), y: Y(155), w: X(32), h: Y(170),
  align: "center", valign: "middle", rot: 270,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Blue dashed arrows from each O_k dot to the error bar (per analysis)
for (const py of ROWS) {
  line(NX.dot5 + 6, py, 733, 240, "0000FF", 1, "dash", "triangle");
}

// ========== CLASS BOXES (light-green, aligned with rows) ==========
const CLASSES = ["Class 1", "Class 2", "Class m"];
for (let r = 0; r < ROWS.length; r++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(790), y: Y(ROWS[r] - 11), w: X(66), h: Y(22),
    fill: { color: "CCFFCC" }, line: { color: "000000", width: 0.75 },
  });
  s.addText(CLASSES[r], {
    x: X(790), y: Y(ROWS[r] - 11), w: X(66), h: Y(22),
    align: "center", valign: "middle",
    fontSize: 10, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ========== LAYER-POINTER BAND (bias circles, up-arrows, layer-name boxes) ==========
// Magenta bias circles with white '1' + 'Node Bias' italic label
s.addShape(pres.shapes.OVAL, {
  x: X(75 - 5), y: Y(352 - 5), w: X(10), h: Y(10),
  fill: { color: "CC00CC" }, line: { color: "CC00CC", width: 0.5 },
});
s.addText("1", {
  x: X(75 - 5), y: Y(352 - 5), w: X(10), h: Y(10),
  align: "center", valign: "middle",
  fontSize: 7, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("Node Bias", {
  x: X(86), y: Y(344), w: X(56), h: Y(16),
  align: "left", valign: "middle",
  fontSize: 9, italic: true, color: "CC00CC", fontFace: FONT, margin: 0,
});
// Two larger bias circles
s.addShape(pres.shapes.OVAL, {
  x: X(300 - 7), y: Y(345 - 7), w: X(14), h: Y(14),
  fill: { color: "CC00CC" }, line: { color: "CC00CC", width: 0.5 },
});
s.addText("1", {
  x: X(300 - 7), y: Y(345 - 7), w: X(14), h: Y(14),
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.OVAL, {
  x: X(455 - 7), y: Y(345 - 7), w: X(14), h: Y(14),
  fill: { color: "CC00CC" }, line: { color: "CC00CC", width: 0.5 },
});
s.addText("1", {
  x: X(455 - 7), y: Y(345 - 7), w: X(14), h: Y(14),
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
// Small orange circle 'k'
s.addShape(pres.shapes.OVAL, {
  x: X(550 - 5), y: Y(355 - 5), w: X(10), h: Y(10),
  fill: { color: "FFDAB9" }, line: { color: "000000", width: 0.5 },
});
s.addText("k", {
  x: X(550 - 5), y: Y(355 - 5), w: X(10), h: Y(10),
  align: "center", valign: "middle",
  fontSize: 7, color: "000000", fontFace: FONT, margin: 0,
});

// Hollow outlined up-arrows pointing to the layer Σ columns
const upArrow = (cx, color, yTop, yBottom) => {
  s.addShape(pres.shapes.UP_ARROW, {
    x: X(cx - 7), y: Y(yTop), w: X(14), h: Y(yBottom - yTop),
    fill: { type: "none" }, line: { color: color, width: 1.25 },
  });
};
upArrow(NX.sigBlue, "8ECAE6", 355, 400);
upArrow(NX.sigGreen, "00CC00", 355, 400);
upArrow(NX.sigOrange, "FF6600", 355, 400);

// Layer-name boxes beneath the arrows (two-line, colored)
const layerBox = (cx, fill, l1, l2) => {
  const bw = 78;
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(cx - bw / 2), y: Y(400), w: X(bw), h: Y(24),
    fill: { color: fill }, line: { color: "000000", width: 0.75 },
  });
  s.addText([
    { text: l1, options: { breakLine: true } },
    { text: l2, options: { breakLine: true } },
  ], {
    x: X(cx - bw / 2), y: Y(400), w: X(bw), h: Y(24),
    align: "center", valign: "middle",
    fontSize: 8, color: "000000", fontFace: FONT, margin: 0,
  });
};
layerBox(NX.sigBlue, "ADD8E6", "Previous Layer", "Layer (i)");
layerBox(NX.sigGreen, "90EE90", "Current Layer", "(You are here)");
layerBox(NX.sigOrange, "FFDAB9", "Next Layer", "Layer (K)");

// Red italic notes (far left and far right of the bottom band)
s.addText('For Layer "j"', {
  x: X(60), y: Y(390), w: X(140), h: Y(20),
  align: "left", valign: "middle",
  fontSize: 12, italic: true, color: "CC0000", fontFace: FONT, margin: 0,
});
s.addText('Note: Layer "j" is NOT Output Layer', {
  x: X(600), y: Y(392), w: X(240), h: Y(20),
  align: "right", valign: "middle",
  fontSize: 12, italic: true, color: "CC0000", fontFace: FONT, margin: 0,
});

// ========== BOTTOM EQUATION BOXES (pale yellow, olive border) ==========
// Left box: Net_j and O_j formulas
s.addShape(pres.shapes.RECTANGLE, {
  x: X(65), y: Y(412), w: X(175), h: Y(70),
  fill: { color: "FFFFE0" }, line: { color: "808000", width: 1 },
});
const eq1t = Y(412 + 22) + EQ1.h_in;   // text-line target baselines inside the box
const eq1y = eq1t - EQ1.baseline_frac * EQ1.h_in;
s.addImage({ path: "eq1_s17.png", x: X(72), y: eq1y, w: EQ1.w_in, h: EQ1.h_in });
const eq2t = Y(412 + 48) + EQ2.h_in;
const eq2y = eq2t - EQ2.baseline_frac * EQ2.h_in;
s.addImage({ path: "eq2_s17.png", x: X(72), y: eq2y, w: EQ2.w_in, h: EQ2.h_in });

// Right box: E formula + three red X marks on the same line to the right
s.addShape(pres.shapes.RECTANGLE, {
  x: X(590), y: Y(412), w: X(240), h: Y(70),
  fill: { color: "FFFFE0" }, line: { color: "808000", width: 1 },
});
const eq3t = Y(412 + 42) + EQ3.h_in;
const eq3y = eq3t - EQ3.baseline_frac * EQ3.h_in;
s.addImage({ path: "eq3_s17.png", x: X(598), y: eq3y, w: EQ3.w_in, h: EQ3.h_in });
s.addText("X  X  X", {
  x: X(598 + EQ3.w_in * 60 + 10), y: Y(438), w: X(70), h: Y(28),
  align: "left", valign: "middle",
  fontSize: 16, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "slide_017_recreated.pptx" })
  .then(() => console.log("wrote slide_017_recreated.pptx (v2)"))
  .catch(err => { console.error(err); process.exit(1); });




