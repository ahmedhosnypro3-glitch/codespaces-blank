// shared.js — common helpers for slide builds in the 06_svm namespace.
// Run: require("./shared.js"); helpers.emitSlide(...)
const pptxgen = require("pptxgenjs");

const W = 13.33, H = 7.5;
const FONT = "Arial";

function newPres() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  return pres;
}

// House chrome: outer red frame + badge + title box (position per house rule)
function addHouseChrome(pres, slide, num, title) {
  slide.background = { color: "E8E8E8" };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
    fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
  });
  slide.addShape(pres.shapes.OVAL, {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
  });
  slide.addText(String(num), {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
  });
  if (title) {
    slide.addText(title, {
      x: 0.6, y: 0.28, w: 12.13, h: 0.55,
      align: "center", valign: "top",
      fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
    });
  }
}

// Plot shell: white panel + axes + ticks + grid. Range is data-space.
function addPlotShell(pres, slide, rx, ry, rw, rh, xMin, xMax, yMin, yMax, xLabel, yLabel) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: rx, y: ry, w: rw, h: rh,
    fill: { color: "FFFFFF" }, line: { color: "999999", width: 0.5 },
  });
  if (xLabel) {
    slide.addText(xLabel, {
      x: rx + rw / 2 - 1.5, y: ry + rh + 0.15, w: 3, h: 0.4,
      align: "center", fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
    });
  }
  if (yLabel) {
    slide.addText(yLabel, {
      x: rx - 1.2, y: ry + rh / 2 - 0.5, w: 2, h: 1,
      align: "center", fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
      rotate: -90,
    });
  }
  const toX = v => rx + ((v - xMin) / (xMax - xMin)) * rw;
  const toY = v => ry + rh - ((v - yMin) / (yMax - yMin)) * rh;

  const xStep = (xMax - xMin) / 5;
  const yStep = (yMax - yMin) / 5;
  const xTicks = [];
  for (let t = 0; t <= 5; t++) xTicks.push(Number((xMin + t * xStep).toFixed(1)));
  const yTicks = [];
  for (let t = 0; t <= 5; t++) yTicks.push(Number((yMin + t * yStep).toFixed(1)));

  xTicks.forEach(tick => {
    const tx = toX(tick);
    slide.addShape(pres.shapes.LINE, { x: tx, y: ry + rh, w: 0, h: 0.15, line: { color: "333333", width: 1 } });
    slide.addText(String(tick), { x: tx - 0.25, y: ry + rh + 0.2, w: 0.5, h: 0.3, align: "center", fontSize: 10, color: "333333", fontFace: FONT, margin: 0 });
  });
  yTicks.forEach(tick => {
    const ty = toY(tick);
    slide.addShape(pres.shapes.LINE, { x: rx - 0.15, y: ty, w: 0.15, h: 0, line: { color: "333333", width: 1 } });
    slide.addText(String(tick), { x: rx - 0.65, y: ty - 0.1, w: 0.5, h: 0.25, align: "right", fontSize: 10, color: "333333", fontFace: FONT, margin: 0 });
  });

  const gridX = xTicks.slice(1, -1);
  const gridY = yTicks.slice(1, -1);
  gridX.forEach(t => slide.addShape(pres.shapes.LINE, { x: toX(t), y: ry, w: 0, h: rh, line: { color: "CCCCCC", width: 0.5, dashType: "dash" } }));
  gridY.forEach(t => slide.addShape(pres.shapes.LINE, { x: rx, y: toY(t), w: rw, h: 0, line: { color: "CCCCCC", width: 0.5, dashType: "dash" } }));

  return { toX, toY, rx, ry, rw, rh };
}

function addDot(pres, slide, mapper, dx, dy, color, radiusIn) {
  const r = radiusIn || 0.05;
  const px = mapper.toX(dx);
  const py = mapper.toY(dy);
  slide.addShape(pres.shapes.OVAL, {
    x: px - r, y: py - r, w: 2 * r, h: 2 * r,
    fill: { color }, line: { color, width: 0 },
  });
}

// Clustered random points around a center (measurement-derived approximations)
function addCluster(pres, slide, mapper, cx, cy, spread, count, color, radiusIn) {
  for (let i = 0; i < count; i++) {
    const x = cx + (Math.random() - 0.5) * spread;
    const y = cy + (Math.random() - 0.5) * spread;
    addDot(pres, slide, mapper, x, y, color, radiusIn);
  }
}

function addRing(pres, slide, mapper, cx, cy, rx, ry, color, radiusIn) {
  const n = Math.max(24, Math.round(Math.sqrt(rx * ry) * 4));
  for (let i = 0; i < n; i++) {
    const a = (i / n) * 2 * Math.PI;
    addDot(pres, slide, mapper, cx + rx * Math.cos(a), cy + ry * Math.sin(a), color, radiusIn);
  }
}

function addSpiral(pres, slide, mapper, cx, cy, rMax, rMin, color, radiusIn, offset) {
  const off = offset || 0;
  const turns = rMax / (rMax - rMin || 1);
  const n = Math.round(rMax * 24);
  for (let i = 0; i < n; i++) {
    const rr = rMax - (i / n) * (rMax - rMin);
    const a = (i / n) * turns * 2 * Math.PI + off;
    addDot(pres, slide, mapper, cx + rr * Math.cos(a), cy + rr * Math.sin(a), color, radiusIn);
  }
}

function addLegend(pres, slide, x, y, entries) {
  entries.forEach((e, i) => {
    slide.addText(e.text, {
      x, y: y + i * 0.3, w: 3.2, h: 0.3,
      fontSize: 11, color: e.color, fontFace: FONT, margin: 0,
    });
  });
}

module.exports = { newPres, addHouseChrome, addPlotShell, addDot, addCluster, addRing, addSpiral, addLegend, W, H, FONT, addDot: addDot };