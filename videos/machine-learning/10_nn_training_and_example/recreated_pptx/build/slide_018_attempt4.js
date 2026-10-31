// slide_018_attempt4.js — Neural Net ∂E/∂w_ji ?  (slide 18 rebuild, b09 attempt4)
// Patterns: house-chrome, equations-mathtext-png
// Geometry measured from unique_slides/slide_018.jpg (960x540 px; x*13.33/960, y*7.5/540)
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5, FONT = "Arial", NUM = 18;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const X = (px) => px * 13.33 / 960;
const Y = (py) => py * 7.5 / 540;

// ---------- HOUSE CHROME ----------
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

// ---------- DIAGRAM BACKING (measured): cream panel x367..754 y59..207 ----------
s.addShape(pres.shapes.RECTANGLE, {
  x: X(367), y: Y(59), w: X(754 - 367), h: Y(207 - 59),
  fill: { color: "D9CDC1" }, line: { color: "D4A7AC", width: 1.25 },
});
// rose vertical line x899..902 y60..209 (right edge of the grey content area)
s.addShape(pres.shapes.RECTANGLE, {
  x: X(899), y: Y(60), w: X(4), h: Y(149),
  fill: { color: "D4A7AC" }, line: { color: "D4A7AC", width: 0.5 },
});

// ---------- HELPERS ----------
const line = (x1, y1, x2, y2, color, w) => {
  s.addShape(pres.shapes.LINE, {
    x: X(x1), y: Y(y1), w: X(x2 - x1), h: Y(y2 - y1),
    line: { color: color, width: w },
  });
};
const box = (cx, py, w, h, fill, edge, lw, glyph, gsize, gcolor) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(cx - w / 2), y: Y(py - h / 2), w: X(w), h: Y(h),
    fill: { color: fill }, line: { color: edge, width: lw || 0.75 },
  });
  if (glyph) {
    s.addText(glyph, {
      x: X(cx - w / 2), y: Y(py - h / 2), w: X(w), h: Y(h),
      align: "center", valign: "middle",
      fontSize: gsize, bold: true, color: gcolor, fontFace: FONT, margin: 0,
    });
  }
};
const circ = (cx, py, d, fill, edge, lw, glyph, gsize, gcolor) => {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx - d / 2), y: Y(py - d / 2), w: X(d), h: Y(d),
    fill: { color: fill }, line: { color: edge, width: lw || 0.75 },
  });
  if (glyph) {
    s.addText(glyph, {
      x: X(cx - d / 2), y: Y(py - d / 2), w: X(d), h: Y(d),
      align: "center", valign: "middle",
      fontSize: gsize, bold: true, color: gcolor, fontFace: FONT, margin: 0,
    });
  }
};

// ---------- NETWORK: three output rows (measured row centres y84/126/171) ----------
const ROWS = [84, 126, 171];

// faint inter-layer pathways (measured: thin, low-contrast diagonal strokes)
for (const py of ROWS) {
  for (const t of ROWS) {
    if (py !== t) {
      line(476, py, 530, t, "E0C8D0", 0.5);
      line(596, py, 630, t, "E0C8D0", 0.5);
      line(640, py, 672, t, "E0C8D0", 0.5);
    }
  }
}

// node chain per row: measured x-columns, fills sampled from the original
for (const py of ROWS) {
  box(413, py, 11, 11, "F4C8D8", "C060A0", 0.75, "w", 6, "C00000");
  box(425, py, 9, 9, "FFE066", "C8A020", 0.75, "w", 6, "C00000");
  box(433, py, 6, 8, "E8C0E8", "A060A0");
  box(476, py, 5, 8, "FFD0E0", "C060A0", 0.75, "w", 5, "C00000");
  box(483, py, 5, 8, "FFE066", "C8A020", 0.75, "w", 5, "C00000");
  box(493, py, 4, 8, "B8E8A8", "40A020");
  box(514, py, 9, 8, "1A1080", "1A1080");
  box(531, py, 6, 8, "B8E8A8", "40A020");
  box(543, py, 5, 8, "FFE066", "C8A020", 0.75, "w", 5, "C00000");
  // Σ node: light-green circle with red Σ (measured light-green disc x554..572)
  circ(563, py, 21, "B8E8A8", "40A020", 1.25);
  s.addText("Σ", {
    x: X(552.5), y: Y(py - 10), w: X(21), h: Y(20),
    align: "center", valign: "middle",
    fontSize: 10, bold: true, color: "C00000", fontFace: "Cambria Math", margin: 0,
  });
  box(583, py, 4, 8, "B8E8A8", "40A020");
  // activation box: light green with the sigmoid curve image (measured x590..602)
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(590), y: Y(py - 7), w: X(12), h: Y(14),
    fill: { color: "B8E8A8" }, line: { color: "40A020", width: 0.75 },
  });
  s.addImage({
    path: "sig_green.png",
    x: X(591), y: Y(py - 6), w: X(10), h: Y(12),
  });
  box(605, py, 7, 8, "8B0000", "8B0000");
  box(635, py, 6, 6, "800080", "800080", 0.5);
  // output activation box: tan with the sigmoid curve image (measured x646..690)
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(646), y: Y(py - 13), w: X(44), h: Y(27),
    fill: { color: "FBE0C0" }, line: { color: "C09060", width: 1 },
  });
  s.addImage({
    path: "sig_orange.png",
    x: X(651), y: Y(py - 10), w: X(24), h: Y(20),
  });
  s.addText("w", {
    x: X(676), y: Y(py - 13), w: X(14), h: Y(27),
    align: "center", valign: "middle",
    fontSize: 8, bold: true, color: "C00000", fontFace: FONT, margin: 0,
  });
  circ(696, py, 9, "C00000", "C00000", 0.5);
}

// ---------- INPUT COLUMN: three magenta dots (measured x371..375) ----------
for (const dy of [108, 122, 134]) circ(373, dy, 5, "800080", "800080", 0.5);

// ---------- CLASS LABELS (measured green text, ink x776..813) ----------
const CLASSES = ["Class 1", "Class 2", "Class m"];
const CLASS_Y = [85, 125, 171];
for (let r = 0; r < 3; r++) {
  s.addText(CLASSES[r], {
    x: X(776), y: Y(CLASS_Y[r] - 8), w: X(42), h: Y(16),
    align: "left", valign: "middle",
    fontSize: 11, bold: true, color: "3E7A28", fontFace: FONT, margin: 0,
  });
}

// ---------- OUTPUT LABELS (measured navy text, ink x704..743) ----------
const OUTS = ["Output 1", "Output 2", "Output 3"];
for (let r = 0; r < 3; r++) {
  s.addText(OUTS[r], {
    x: X(703), y: Y(CLASS_Y[r] - 8), w: X(48), h: Y(16),
    align: "left", valign: "middle",
    fontSize: 11, bold: true, color: "1A1080", fontFace: FONT, margin: 0,
  });
}

// ---------- ERROR COLUMN (measured red x760..773, y66..187; pink fill) ----------
s.addShape(pres.shapes.RECTANGLE, {
  x: X(761), y: Y(66), w: X(13), h: Y(121),
  fill: { color: "FFBAC3" }, line: { color: "C00000", width: 1 },
});
s.addText("Error Error Error", {
  x: X(760), y: Y(70), w: X(16), h: Y(113),
  align: "center", valign: "middle", rot: 270,
  fontSize: 8, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---------- EQUATION ∂E/∂w_ji ? (measured ink x831..866, y107..149 in orig) ----------
// eq_s18b.png is 199x223 px @600dpi with intrinsic ink bbox (8,8)-(191,215).
const TGT_H_IN = 42 / 540 * 7.5;
const INK_H_IN = 208 / 600;
const EQ_S = TGT_H_IN / INK_H_IN;
s.addImage({
  path: "eq_s18b.png",
  x: 831 / 960 * 13.33 - 8 / 600 * EQ_S,
  y: 107 / 540 * 7.5 - 8 / 600 * EQ_S,
  w: 199 / 600 * EQ_S, h: 223 / 600 * EQ_S,
});
// red "?" — target ink bbox (875,113)-(886,135) in the original
s.addText("?", {
  x: 879.5 / 960 * 13.33 - 0.114, y: 124 / 540 * 7.5 - 0.26, w: 0.34, h: 0.52,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: "C00000", fontFace: "Cambria Math", margin: 0,
});

// ---------- BOTTOM ROW (measured) ----------
// white up-arrow x463..478 y180..206
s.addShape(pres.shapes.UP_ARROW, {
  x: X(463), y: Y(180), w: X(16), h: Y(27),
  fill: { color: "F0F0F0" }, line: { color: "808080", width: 0.75 },
});
s.addText("1", {
  x: X(461), y: Y(194), w: X(20), h: Y(11),
  align: "center", valign: "middle",
  fontSize: 7, bold: true, color: "404040", fontFace: FONT, margin: 0,
});
// magenta circles (measured x499..512 and x590..602, y185..198)
for (const cx of [505.5, 596]) {
  circ(cx, 191.5, 14, "800080", "800080", 0.5, "1", 9, "FFFFFF");
}
// green up-arrow x559..569 y189..207
s.addShape(pres.shapes.UP_ARROW, {
  x: X(559), y: Y(189), w: X(11), h: Y(19),
  fill: { color: "40A020" }, line: { color: "40A020", width: 0.5 },
});
s.addText("1", {
  x: X(556), y: Y(194), w: X(17), h: Y(11),
  align: "center", valign: "middle",
  fontSize: 6, bold: true, color: "206000", fontFace: FONT, margin: 0,
});
// bottom-left: magenta circle + "Input Data" (measured ink x368..405)
circ(373.5, 195.5, 11, "800080", "800080", 0.5);
s.addText("Input Data", {
  x: X(379), y: Y(191), w: X(30), h: Y(10),
  align: "left", valign: "middle",
  fontSize: 8, bold: true, color: "8B007A", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: process.env.R5_OUT || "slide_018_attempt4.pptx" })
  .then(() => console.log("wrote " + (process.env.R5_OUT || "slide_018_attempt4.pptx")))
  .catch(err => { console.error(err); process.exit(1); });
