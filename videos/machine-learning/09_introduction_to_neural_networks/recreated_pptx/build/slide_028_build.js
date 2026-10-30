// Build slide 028: Neural Network Model (badge 28)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "F0F0F0" };
const FONT = "Arial";

// ---- HOUSE CHROME ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFD966" }, line: { color: "C0392B", width: 1.5 },
});
s.addText("28", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Title
s.addText("Neural Network Model", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// Input Sample box (top left)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 0.6,
  fill: { color: "9B59B6" }, line: { color: "9B59B6", width: 1 },
});
s.addText("Input\nSample", {
  x: 0.5, y: 0.8, w: 1.5, h: 0.6,
  align: "center", valign: "middle", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Dashed arrow from Input Sample to diagram
s.addShape(pres.shapes.LINE, {
  x: 2.0, y: 1.1, w: 1.5, h: 0,
  line: { color: "9B59B6", width: 1.5, dashType: "dash" },
});

// Target Label box (top right)
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.5, y: 0.8, w: 1.5, h: 0.6,
  fill: { color: "9B59B6" }, line: { color: "9B59B6", width: 1 },
});
s.addText("Target\nLabel", {
  x: 10.5, y: 0.8, w: 1.5, h: 0.6,
  align: "center", valign: "middle", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Dashed arrow from diagram to Target Label
s.addShape(pres.shapes.LINE, {
  x: 9.0, y: 1.1, w: 1.5, h: 0,
  line: { color: "9B59B6", width: 1.5, dashType: "dash" },
});

// Network diagram - simplified representation using shapes
// We'll create a diagram with input nodes, hidden layers, output layer

// Input nodes (purple dots)
for (let i = 0; i < 4; i++) {
  const y = 1.8 + i * 0.4;
  s.addShape(pres.shapes.OVAL, {
    x: 1.0, y: y, w: 0.25, h: 0.25,
    fill: { color: "CC66CC" }, line: { color: "CC66CC", width: 0 },
  });
}

// Layer 1: Neurons with sigma/sigmoid (yellow circles with red borders)
for (let i = 0; i < 3; i++) {
  const y = 2.0 + i * 0.6;
  s.addShape(pres.shapes.OVAL, {
    x: 2.5, y: y, w: 0.5, h: 0.5,
    fill: { color: "FFE699" }, line: { color: "FF0000", width: 1.5 },
  });
  // Net_i label
  s.addText(`Net_${['i','j','k'][i]}`, {
    x: 2.5, y: y - 0.3, w: 0.5, h: 0.3,
    align: "center", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  // O_i label
  s.addText(`O_${['i','j','k'][i]}`, {
    x: 3.0, y: y + 0.1, w: 0.5, h: 0.3,
    align: "left", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
}

// Connection weights (blue labels)
s.addText("w_ji", {
  x: 2.5, y: 1.8, w: 0.8, h: 0.3,
  align: "center", fontSize: 10, bold: true, italic: true, color: "3498DB", fontFace: FONT, margin: 0,
});

// Layer 2: Neurons (blue circles)
for (let i = 0; i < 3; i++) {
  const y = 2.0 + i * 0.6;
  s.addShape(pres.shapes.OVAL, {
    x: 4.5, y: y, w: 0.5, h: 0.5,
    fill: { color: "FFFFFF" }, line: { color: "0070C0", width: 1.5 },
  });
  s.addText(`Net_${['i','j','k'][i]}`, {
    x: 4.5, y: y - 0.3, w: 0.5, h: 0.3,
    align: "center", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  s.addText(`O_${['i','j','k'][i]}`, {
    x: 5.0, y: y + 0.1, w: 0.5, h: 0.3,
    align: "left", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
}

// Layer 3: Neurons (green circles)
for (let i = 0; i < 3; i++) {
  const y = 2.0 + i * 0.6;
  s.addShape(pres.shapes.OVAL, {
    x: 6.5, y: y, w: 0.5, h: 0.5,
    fill: { color: "FFFFFF" }, line: { color: "00B050", width: 1.5 },
  });
  s.addText(`Net_${['i','j','k'][i]}`, {
    x: 6.5, y: y - 0.3, w: 0.5, h: 0.3,
    align: "center", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
  s.addText(`O_${['i','j','k'][i]}`, {
    x: 7.0, y: y + 0.1, w: 0.5, h: 0.3,
    align: "left", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
  });
}

// Weight labels between layer 2 and 3
s.addText("w_kj", {
  x: 4.8, y: 1.8, w: 0.8, h: 0.3,
  align: "center", fontSize: 10, bold: true, italic: true, color: "3498DB", fontFace: FONT, margin: 0,
});

// Output labels
s.addText("Output 1", { x: 7.5, y: 2.0, w: 1.0, h: 0.3, align: "left", fontSize: 10, italic: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Output 2", { x: 7.5, y: 2.6, w: 1.0, h: 0.3, align: "left", fontSize: 10, italic: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Output m", { x: 7.5, y: 3.2, w: 1.0, h: 0.3, align: "left", fontSize: 10, italic: true, color: "000000", fontFace: FONT, margin: 0 });

// Error Error bar (dark red vertical)
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.2, y: 1.8, w: 0.3, h: 2.0,
  fill: { color: "C0392B" }, line: { color: "C0392B", width: 0 },
});
s.addText("Error Error", {
  x: 8.2, y: 1.8, w: 0.3, h: 2.0,
  align: "center", valign: "middle", fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  rotate: 270,
});

// Class boxes
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.6, y: 1.8, w: 1.2, h: 0.5,
  fill: { color: "D9EAD3" }, line: { color: "00B050", width: 1 },
});
s.addText("Class 1", { x: 8.6, y: 1.8, w: 1.2, h: 0.5, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 8.6, y: 2.5, w: 1.2, h: 0.5,
  fill: { color: "D9EAD3" }, line: { color: "00B050", width: 1 },
});
s.addText("Class 2", { x: 8.6, y: 2.5, w: 1.2, h: 0.5, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 8.6, y: 3.2, w: 1.2, h: 0.5,
  fill: { color: "D9EAD3" }, line: { color: "00B050", width: 1 },
});
s.addText("Class m", { x: 8.6, y: 3.2, w: 1.2, h: 0.5, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

// Green arrow from Error bar to middle output
s.addShape(pres.shapes.LINE, {
  x: 8.5, y: 2.75, w: 0.5, h: 0,
  line: { color: "2ECC71", width: 2, endArrow: "triangle" },
});

// Legend box (upper right)
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.5, y: 1.2, w: 2.5, h: 1.5,
  fill: { color: "F2E4D0" }, line: { color: "C00000", width: 1 },
});
s.addText(
  "Net_j ⇒ Summation at Node j\nO_j ⇒ Output at Node j\nw_ji ⇒ Weight from Node i to Node j",
  { x: 9.6, y: 1.3, w: 2.3, h: 1.3, fontSize: 10, color: "000000", fontFace: FONT, margin: 0.1 }
);

// Node count box
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.5, y: 2.8, w: 2.5, h: 0.8,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});
s.addText(
  "Number of I/P Nodes = Input Vector Length\nNumber of O/P Nodes = Number of classes",
  { x: 9.6, y: 2.9, w: 2.3, h: 0.6, fontSize: 10, color: "000000", fontFace: FONT, margin: 0.1 }
);

// Layer callouts (bottom)
s.addShape(pres.shapes.RECTANGLE, {
  x: 2.0, y: 5.5, w: 2.0, h: 0.8,
  fill: { color: "DDEBF7" }, line: { color: "3498DB", width: 1 },
});
s.addText("Previous Layer\nLayer (i)", { x: 2.0, y: 5.5, w: 2.0, h: 0.8, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 4.2, y: 5.5, w: 2.0, h: 0.8,
  fill: { color: "E2EFDA" }, line: { color: "2ECC71", width: 1 },
});
s.addText("Current Layer\n(You are here)", { x: 4.2, y: 5.5, w: 2.0, h: 0.8, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 6.5, y: 5.5, w: 2.0, h: 0.8,
  fill: { color: "FDEBD0" }, line: { color: "E67E22", width: 1 },
});
s.addText("Next Layer\nLayer (K)", { x: 6.5, y: 5.5, w: 2.0, h: 0.8, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

// Hidden Layer bar
s.addShape(pres.shapes.RECTANGLE, {
  x: 2.0, y: 6.5, w: 6.5, h: 0.4,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});
s.addText("Hidden Layer(s)", {
  x: 2.0, y: 6.5, w: 6.5, h: 0.4,
  align: "center", valign: "middle", fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// I/P Layer and O/P Layer boxes
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 6.5, w: 1.3, h: 0.4,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});
s.addText("I/P Layer", { x: 0.5, y: 6.5, w: 1.3, h: 0.4, align: "center", valign: "middle", fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 11.0, y: 6.5, w: 1.3, h: 0.4,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});
s.addText("O/P Layer", { x: 11.0, y: 6.5, w: 1.3, h: 0.4, align: "center", valign: "middle", fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });

const outPath = "slide_028_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));