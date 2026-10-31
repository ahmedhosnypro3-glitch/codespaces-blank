// slide_018_attempt1.js — Neural Net: ∂E/∂w_ji ?  (slide 18 rebuild, b09)
// Patterns: house-chrome, equations-mathtext-png, explicit-line-spacing
// Geometry measured from unique_slides/slide_018.jpg (960x540 px; x*13.33/960, y*7.5/540)
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 18;
const BG = "E8E8E8";
const FRAME = "C00000";
const EQ = JSON.parse(fs.readFileSync("eq_s18b.json"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

const PX = 13.33 / 960, PY = 7.5 / 540;
const X = (px) => px * PX;
const Y = (py) => py * PY;

// ---------- HOUSE CHROME ----------
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

// ---------- DIAGRAM PANEL (measured x368..888, y63..205) ----------
s.addShape(pres.shapes.RECTANGLE, {
  x: X(368), y: Y(63), w: X(520), h: Y(142),
  fill: { color: "EFE3D0" }, line: { color: "D8A8A8", width: 1 },
});

// ---------- ROWS ----------
const ROWS = [80, 125, 170];
const line = (x1, y1, x2, y2, color, w, dash, arrow) => {
  s.addShape(pres.shapes.LINE, {
    x: X(x1), y: Y(y1), w: X(x2 - x1), h: Y(y2 - y1),
    line: { color: color, width: w, dashType: dash || "solid",
            endArrowType: arrow || "none" },
  });
};
const dot = (cx, py, d, fill, edge) => {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx - d / 2), y: Y(py - d / 2), w: X(d), h: Y(d),
    fill: { color: fill }, line: { color: edge || fill, width: 0.5 },
  });
};
const sigCircle = (cx, py, edge, glyph) => {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx - 10), y: Y(py - 10), w: X(20), h: Y(20),
    fill: { color: "B8E8A8" }, line: { color: edge, width: 1.25 },
  });
  s.addText("\u03a3", {
    x: X(cx - 10), y: Y(py - 10), w: X(20), h: Y(20),
    align: "center", valign: "middle",
    fontSize: 8, color: glyph, fontFace: "Cambria Math", margin: 0,
  });
};
const sigBox = (cx, py, img, wpx, hpx) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(cx - wpx / 2), y: Y(py - hpx / 2), w: X(wpx), h: Y(hpx),
    fill: { color: "FFF3C4" }, line: { color: "C8A020", width: 1 },
  });
  s.addImage({ path: img, x: X(cx - wpx / 2 + 1), y: Y(py - hpx / 2 + 1),
               w: X(wpx - 2), h: Y(hpx - 2) });
};

// fan-out mesh between stages (drawn under the nodes)
for (const py of ROWS) {
  for (const t of ROWS) {
    line(500, py, 533, t, "F0B8C8", 0.75);
    line(563, py, 596, t, "F0B8C8", 0.75);
  }
}

// per-row node chain (measured colour rhythm: purple dot, red dot, blue sq,
// pink box, Σ circle, sigmoid box, green sq, sigmoid box, Output label)
for (let r = 0; r < ROWS.length; r++) {
  const py = ROWS[r];
  dot(409, py, 7, "9B59B6");
  dot(425, py, 9, "D02020");
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(467), y: Y(py - 3), w: X(7), h: Y(6),
    fill: { color: "2020C0" }, line: { color: "2020C0", width: 0.5 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(481), y: Y(py - 9), w: X(19), h: Y(18),
    fill: { color: "F0C0D8" }, line: { color: "C060A0", width: 0.75 },
  });
  sigCircle(533, py, "40A020", "208000");
  sigBox(563, py, "sig_green.png", 20, 20);
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(590), y: Y(py - 8), w: X(13), h: Y(15),
    fill: { color: "B8E8A8" }, line: { color: "40A020", width: 0.75 },
  });
  sigBox(657, py, "sig_orange.png", 32, 22);
  s.addText("Net", {
    x: X(641), y: Y(py - 21), w: X(32), h: Y(9),
    align: "center", valign: "bottom",
    fontSize: 5, bold: true, color: "208000", fontFace: FONT, margin: 0,
  });
  line(546, py, 553, py, "2040C0", 1, "dash", "triangle");
  line(577, py, 596, py, "2040C0", 1, "dash", "triangle");
  line(600, py, 641, py, "2040C0", 1, "dash", "triangle");
}

// ---------- OUTPUT LABELS (blue, measured ink x704..740, y80..89 -> ~10pt) ----------
const OUTS = ["Output 1", "Output 2", "Output 3"];
for (let r = 0; r < 3; r++) {
  s.addText(OUTS[r], {
    x: X(703), y: Y(ROWS[r] - 8), w: X(46), h: Y(16),
    align: "left", valign: "middle",
    fontSize: 10, bold: true, color: "2020C0", fontFace: FONT, margin: 0,
  });
}

// ---------- ERROR BAR: red OUTLINE + red glyph text (measured x762..772, y69..185) ----------
s.addShape(pres.shapes.RECTANGLE, {
  x: X(762), y: Y(69), w: X(10), h: Y(116),
  fill: { type: "none" }, line: { color: "C00000", width: 0.75 },
});
s.addText("Error Error Error", {
  x: X(760), y: Y(74), w: X(16), h: Y(106),
  align: "center", valign: "middle", rot: 270,
  fontSize: 8, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
// slide_018_attempt1.js — part 2 (appended): class labels, equation, bottom labels
// ---------- CLASS LABELS (x781..798, 3 rows) ----------
const CLASSES = ["Class 1", "Class 2", "Class m"];
for (let r = 0; r < 3; r++) {
  s.addText(CLASSES[r], {
    x: X(779), y: Y(ROWS[r] - 5), w: X(26), h: Y(10),
    align: "left", valign: "middle",
    fontSize: 5, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ---------- EQUATION ∂E/∂w_ji ? (measured ink x831..866, y107..149 in orig) ----------
// eq_s18b.png is 199x223 px @600dpi with intrinsic ink bbox (8,8)-(191,215).
// Target ink box in the 960x540 original: x831..866 (35 px), y107..149 (42 px).
const TGT_W_IN = 35 / 960 * 13.33, TGT_H_IN = 42 / 540 * 7.5;
const INK_W_IN = 184 / 600, INK_H_IN = 208 / 600;
const EQ_S = TGT_H_IN / INK_H_IN;
const eq_img_w = 199 / 600 * EQ_S, eq_img_h = 223 / 600 * EQ_S;
const eq_x = 831 / 960 * 13.33 - 8 / 600 * EQ_S;
const eq_y = 107 / 540 * 7.5 - 8 / 600 * EQ_S;
s.addImage({ path: "eq_s18b.png", x: eq_x, y: eq_y, w: eq_img_w, h: eq_img_h });
// red "?" — target ink bbox (874,114)-(885,134) in the original
s.addText("?", {
  x: 879.5 / 960 * 13.33 - 0.17, y: 124 / 540 * 7.5 - 0.26, w: 0.34, h: 0.52,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
});

// ---------- BOTTOM: white up-arrow + magenta "1" circles (measured x464..479, x499..512, x589..602) ----------
s.addShape(pres.shapes.UP_ARROW, {
  x: X(464), y: Y(188), w: X(15), h: Y(19),
  fill: { color: "F0F0F0" }, line: { color: "808080", width: 0.75 },
});
s.addText("1", {
  x: X(464), y: Y(193), w: X(15), h: Y(11),
  align: "center", valign: "middle",
  fontSize: 7, bold: true, color: "404040", fontFace: FONT, margin: 0,
});
for (const cx of [497, 588]) {
  s.addShape(pres.shapes.OVAL, {
    x: X(cx), y: Y(183), w: X(17), h: Y(17),
    fill: { color: "800080" }, line: { color: "800080", width: 0.5 },
  });
  s.addText("1", {
    x: X(cx), y: Y(183), w: X(17), h: Y(17),
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// ---------- BOTTOM: green up-arrow + "1" (measured x559..569, y189..206) ----------
s.addShape(pres.shapes.UP_ARROW, {
  x: X(559), y: Y(189), w: X(10), h: Y(17),
  fill: { color: "40A020" }, line: { color: "40A020", width: 0.5 },
});
s.addText("1", {
  x: X(556), y: Y(194), w: X(16), h: Y(9),
  align: "center", valign: "middle",
  fontSize: 6, bold: true, color: "208000", fontFace: FONT, margin: 0,
});

// ---------- BOTTOM-LEFT: magenta "1" + Train Data (measured x367..403, y189..200) ----------
s.addShape(pres.shapes.OVAL, {
  x: X(367), y: Y(189), w: X(12), h: X(12),
  fill: { color: "800080" }, line: { color: "800080", width: 0.5 },
});
s.addText("1", {
  x: X(367), y: Y(189), w: X(12), h: Y(12),
  align: "center", valign: "middle",
  fontSize: 7, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("Train Data", {
  x: X(379), y: Y(191), w: X(30), h: Y(10),
  align: "left", valign: "middle",
  fontSize: 6, bold: true, color: "800080", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: process.env.R5_OUT || "slide_018_attempt2.pptx" })
  .then(() => console.log("wrote " + (process.env.R5_OUT || "slide_018_attempt1.pptx")))
  .catch(err => { console.error(err); process.exit(1); });
