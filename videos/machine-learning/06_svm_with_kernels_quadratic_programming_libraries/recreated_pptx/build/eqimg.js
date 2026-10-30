// eqimg.js — place the 2D math PNG assets rendered by gen_math_assets.py.
// Each asset is already sized to fit its box budget at 600 dpi, so it is
// placed at natural size (w = px/600) and centered unless told otherwise.
const path = require("path");
const manifest = require("./assets/eq/manifest.json");

function addEq(slide, name, box, opts) {
  const m = manifest[name];
  if (!m) throw new Error("unknown math asset: " + name);
  const o = opts || {};
  let w = m.w_in;
  let h = m.h_in;
  if (o.scale) {
    w *= o.scale;
    h *= o.scale;
  }
  if (w > box.w) {
    h *= box.w / w;
    w = box.w;
  }
  const x = o.align === "left" ? box.x : box.x + (box.w - w) / 2;
  const y = box.y + (box.h - h) / 2;
  slide.addImage({ path: m.path, x, y, w, h });
  return { x, y, w, h };
}

module.exports = { addEq };
