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

// ---------- EQUATION ∂E/∂w_ji ? (measured x830..887, y106..150; red ? at 875..887) ----------
s.addImage({
  path: "eq_s18b.png", x: X(830), y: Y(106), w: EQ.w_in, h: EQ.h_in,
});
s.addText("?", {
  x: X(875), y: Y(110), w: X(14), h: Y(28),
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
});

// ---------- BOTTOM: green up-arrow + "1" (measured x559..569, y189..206) ----------
s.addShape(pres.shapes.UP_ARROW, {
  x: X(559), y: Y(189), w: X(10), h: Y(17),
  fill: { color: "40A020" }, line: { color: "40A020", width: 0.5 },
});
s.addText("1", {
  x: X(555), y: Y(178), w: X(14), h: Y(10),
  align: "center", valign: "middle",
  fontSize: 6, bold: true, color: "208000", fontFace: FONT, margin: 0,
});

// ---------- BOTTOM-LEFT LABEL (measured ink ~x384..420, y195..205) ----------
s.addText("Input Data", {
  x: X(378), y: Y(193), w: X(60), h: Y(12),
  align: "left", valign: "middle",
  fontSize: 6, color: "000000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: process.env.R5_OUT || "slide_018_attempt1.pptx" })
  .then(() => console.log("wrote " + (process.env.R5_OUT || "slide_018_attempt1.pptx")))
  .catch(err => { console.error(err); process.exit(1); });
