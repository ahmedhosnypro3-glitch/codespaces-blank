#!/usr/bin/env node
// READ-ONLY geometry extractor for pre-judge checks.
//
// Runs a build script under a pptxgenjs prototype patch that neuters
// writeFile/write, so NO pptx (or any work product) is created or modified.
// A Proxy over each slide records every add* call with its resolved options
// (computed values inside loops included), which is then measured by
// tools/measure.py.
//
// Usage: node extract_geom.js <build_script.js> <out.json>
const path = require("path");
const fs = require("fs");

const PPTXGEN = "/home/codespace/ai_llm_slides/node_modules/pptxgenjs";
const pptxgen = require(PPTXGEN);

// ---- neuter all output paths ---------------------------------------------------
const proto = pptxgen.prototype;
proto.writeFile = function () { return Promise.resolve("patched-no-write"); };
if (proto.write) proto.write = function () { return Promise.resolve("patched-no-write"); };

// ---- record every add* call ----------------------------------------------------
const slides = [];
function wrapSlide(slide, index) {
  const proxy = new Proxy(slide, {
    get(target, prop) {
      const v = target[prop];
      if (typeof v === "function" && typeof prop === "string" && prop.startsWith("add")) {
        return (...args) => {
          const rec = { type: prop, args: args.map(serializeArg) };
          slides[index].elements.push(rec);
          const ret = v.apply(target, args);
          return ret === target ? proxy : ret;
        };
      }
      if (typeof v === "function") return v.bind(target);
      return v;
    },
    set(target, prop, value) { target[prop] = value; return true; },
  });
  return proxy;
}

function serializeArg(a) {
  if (a === null || a === undefined) return a;
  if (typeof a === "function") return "[fn]";
  if (Array.isArray(a)) return a.map(serializeArg);
  if (typeof a === "object") {
    const out = {};
    for (const k of Object.keys(a)) {
      const v = a[k];
      if (typeof v === "function") continue;
      out[k] = serializeArg(v);
    }
    return out;
  }
  return a;
}

const origAddSlide = proto.addSlide;
proto.addSlide = function (...args) {
  const slide = origAddSlide.apply(this, args);
  const index = slides.length;
  slides.push({ index, elements: [] });
  return wrapSlide(slide, index);
};

// ---- run the build script ------------------------------------------------------
const target = path.resolve(process.argv[2]);
const outPath = path.resolve(process.argv[3]);

process.on("unhandledRejection", (e) => {
  fs.writeFileSync(outPath, JSON.stringify({ error: String(e), slides }, null, 2));
  process.exit(0);
});

require(target);

// give async build scripts a moment to finish their synchronous geometry work
setTimeout(() => {
  fs.writeFileSync(outPath, JSON.stringify({ build: target, slides }, null, 2));
  process.exit(0);
}, 400);
