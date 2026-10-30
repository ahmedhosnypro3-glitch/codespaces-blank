// kernel_example.js — shared builder for the paired "How to Kernelize SVM"
// example slides (036 quadratic kernel / 037 polynomial kernel).
// Equations are 2D matplotlib-mathtext PNGs; highlight shapes are placed from
// each PNG's .segments.json so they land exactly on the term they mark.

const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { newPres, W, H, FONT } = require("./shared.js");

const DPI = 600;
const MATH = "Times New Roman";

const FRAME = { x: 0.80, y: 0.525, w: 11.73, h: 6.675 };
const KICK = { x: 0.93, y: 0.60, w: 2.95, h: 0.44 };
const UP = { x: 0.93, y: 1.20, w: 11.33, h: 2.15 };
const LO = { x: 0.93, y: 4.58, w: 11.33, h: 2.25 };

function segMeta(eqDir, name) {
  return JSON.parse(fs.readFileSync(`${eqDir}${name}.png.segments.json`, "utf8"));
}

// Bounding box of a labelled segment, in slide inches, for an image at (ix, iy).
function segBox(meta, label, ix, iy, padX, padY) {
  const s = meta.segments[label];
  return {
    x: ix + s.x0 / DPI - padX,
    y: iy + s.y0 / DPI - padY,
    w: (s.x1 - s.x0) / DPI + 2 * padX,
    h: (s.y1 - s.y0) / DPI + 2 * padY,
  };
}

function houseChrome(pres, s, num, title) {
  s.background = { color: "E8E8E8" };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
    fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
  });
  s.addText(String(num), {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
  });
  s.addText(title, {
    x: 0.6, y: 0.28, w: 12.13, h: 0.55,
    align: "center", valign: "top",
    fontSize: 26, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
  });
}

module.exports = function buildKernelExample(cfg) {
  const pres = newPres();
  const s = pres.addSlide();
  houseChrome(pres, s, cfg.num, cfg.title);

  // 1. Red content frame around the whole body
  s.addShape(pres.shapes.RECTANGLE, {
    x: FRAME.x, y: FRAME.y, w: FRAME.w, h: FRAME.h,
    fill: { type: "none" }, line: { color: "E00000", width: 1 },
  });

  // 2. Kicker badge (top-left)
  s.addShape(pres.shapes.RECTANGLE, {
    x: KICK.x, y: KICK.y, w: KICK.w, h: KICK.h,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });
  s.addText([
    { text: "Example:", options: { italic: true } },
    { text: ` ${cfg.kicker}`, options: { italic: true, bold: true } },
  ], {
    x: KICK.x, y: KICK.y, w: KICK.w, h: KICK.h,
    align: "center", valign: "middle", fontSize: 13, color: "0000CC", fontFace: FONT, margin: 0,
  });

  // 3. Upper panel (original SVM formulation)
  s.addShape(pres.shapes.RECTANGLE, {
    x: UP.x, y: UP.y, w: UP.w, h: UP.h,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });

  const lagUpX = 1.55, lagUpY = 1.28;
  s.addImage({ path: cfg.eq + "eq_lag_orig.png", x: lagUpX, y: lagUpY, w: 4.56167, h: 0.83667 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    ...segBox(segMeta(cfg.eq, "eq_lag_orig"), "kern", lagUpX, lagUpY, 0.04, 0.03),
    fill: { color: cfg.hlFill }, line: { color: "00CC00", width: 1.25 },
  });

  const wBoxX = 1.18, wBoxY = 2.18;
  s.addShape(pres.shapes.RECTANGLE, {
    x: wBoxX, y: wBoxY, w: 2.15, h: 0.95,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });
  s.addImage({ path: cfg.eq + "eq_W.png", x: wBoxX + 0.15, y: wBoxY + 0.04, w: 1.65, h: 0.79833 });

  const bBoxX = 4.85, bBoxY = 2.28, bImgX = 5.00, bImgY = 2.34;
  s.addShape(pres.shapes.RECTANGLE, {
    x: bBoxX, y: bBoxY, w: cfg.bOrigW + 0.30, h: 0.65,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });
  s.addImage({ path: cfg.eq + "eq_b_orig.png", x: bImgX, y: bImgY, w: cfg.bOrigW, h: 0.53333 });
  const metaBUp = segMeta(cfg.eq, "eq_b_orig");
  ["t1", "t2"].forEach(k => s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    ...segBox(metaBUp, k, bImgX, bImgY, 0.04, 0.03),
    fill: { color: cfg.hlFill }, line: { color: "00CC00", width: 1.25 },
  }));

  // 4. Class-of-vector strip (upper): peach fill, 3-piece text, green highlight on the math term
  function classStrip(prefixRuns, mathRuns, suffix, mathX, mathW, stripW, stripY) {
    const stripX = 1.73;
    s.addShape(pres.shapes.RECTANGLE, {
      x: stripX, y: stripY, w: stripW, h: 0.44,
      fill: { color: cfg.clsFill },
      line: cfg.clsBorder ? { color: cfg.clsBorder, width: 1 } : { type: "none" },
    });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: mathX, y: stripY + 0.05, w: mathW, h: 0.34,
      fill: { color: cfg.hlFill }, line: { color: "00CC00", width: 1.25 },
    });
    s.addText(prefixRuns, {
      x: stripX, y: stripY, w: mathX - stripX, h: 0.44,
      align: "right", valign: "middle", fontSize: 14, fontFace: MATH, margin: 0,
    });
    s.addText(mathRuns, {
      x: mathX, y: stripY, w: mathW, h: 0.44,
      align: "left", valign: "middle", fontSize: 14, fontFace: MATH, margin: 0,
    });
    s.addText(suffix, {
      x: mathX + mathW, y: stripY, w: 1.2, h: 0.44,
      align: "left", valign: "middle", fontSize: 14, fontFace: MATH, margin: 0,
    });
  }

  classStrip(
    [
      { text: "Class of vector ", options: { color: "000000" } },
      { text: "Z", options: { color: "00A000", bold: true } },
      { text: " \u21d2 sign(", options: { color: "000000" } },
    ],
    cfg.classUpRuns, " + b)", 5.33, 1.07, 6.20, 2.78,
  );

  // 5. Middle connector: "Kernelize using" + the kernel formula
  const connY = 3.72, connH = 0.44;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 4.00, y: connY, w: 1.75, h: connH,
    fill: { color: "FFFFFF" }, line: { color: cfg.connBorder, width: 1 },
  });
  s.addText("Kernelize using", {
    x: 4.00, y: connY, w: 1.75, h: connH,
    align: "center", valign: "middle", italic: true, fontSize: 13, color: "000000", fontFace: FONT, margin: 0,
  });
  if (cfg.kernelImg) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 5.95, y: connY, w: cfg.kernelImg.w + 0.30, h: connH,
      fill: { color: "FFFFFF" }, line: { color: "E00000", width: 1 },
    });
    s.addImage({
      path: cfg.eq + cfg.kernelImg.name,
      x: 5.95 + 0.15, y: connY + (connH - cfg.kernelImg.h) / 2,
      w: cfg.kernelImg.w, h: cfg.kernelImg.h,
    });
  } else {
    s.addImage({ path: cfg.eq + cfg.kernelName, x: 5.95, y: connY + (connH - 0.35833) / 2, w: cfg.kernelW, h: 0.35833 });
  }
  s.addShape(pres.shapes.DOWN_ARROW, {
    x: 5.73, y: 3.53, w: 0.27, h: 0.90,
    fill: { color: "FFFFFF" }, line: { color: "E00000", width: 1 },
  });

  // 6. Lower panel (kernelized SVM formulation)
  s.addShape(pres.shapes.RECTANGLE, {
    x: LO.x, y: LO.y, w: LO.w, h: LO.h,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });

  const lagLoX = 1.28, lagLoY = 4.66;
  s.addImage({ path: cfg.eq + "eq_lag_k.png", x: lagLoX, y: lagLoY, w: cfg.lagKW, h: 0.83667 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    ...segBox(segMeta(cfg.eq, "eq_lag_k"), "kern", lagLoX, lagLoY, 0.04, 0.03),
    fill: { color: cfg.hlFill }, line: { color: "00CC00", width: 1.25 },
  });

  const lwBoxY = 5.56;
  s.addShape(pres.shapes.RECTANGLE, {
    x: wBoxX, y: lwBoxY, w: 2.15, h: 0.95,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });
  s.addImage({ path: cfg.eq + "eq_W.png", x: wBoxX + 0.15, y: lwBoxY + 0.04, w: 1.65, h: 0.79833 });

  const lbBoxX = 4.55, lbBoxY = 5.64, lbImgX = 4.70, lbImgY = 5.70;
  s.addShape(pres.shapes.RECTANGLE, {
    x: lbBoxX, y: lbBoxY, w: cfg.bKW + 0.30, h: 0.65,
    fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
  });
  s.addImage({ path: cfg.eq + "eq_b_k.png", x: lbImgX, y: lbImgY, w: cfg.bKW, h: 0.53333 });
  const metaBkLo = segMeta(cfg.eq, "eq_b_k");
  ["t1", "t2"].forEach(k => s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    ...segBox(metaBkLo, k, lbImgX, lbImgY, 0.04, 0.03),
    fill: { color: cfg.hlFill }, line: { color: "00CC00", width: 1.25 },
  }));

  classStrip(
    [
      { text: "Class of vector ", options: { color: "000000" } },
      { text: "Z", options: { color: "00A000", bold: true } },
      { text: " is sign(", options: { color: "000000" } },
    ],
    cfg.classLoRuns, " + b)", 5.73, 1.20, 6.60, 6.14,
  );

  pres.writeFile({ fileName: cfg.out })
    .then(() => console.log(`wrote ${cfg.out}`))
    .catch(err => console.error(err));
};
