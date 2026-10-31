#!/usr/bin/env python3
"""Closed-loop verification for slide 026 (rebuild vs the original frame).

Runs the SAME predicates on the original frame (unique_slides/slide_026.jpg,
960x540) and on the 150dpi render (build/slide_026_rejudge_rendered-1.png),
so targets are self-derived rather than hardcoded expectations. Render
coordinates are converted back to original-pixel space by dividing by the
render scale.

Checks the seven adjudicated judge findings:
  1 value box clear of the formulas      5 equation accent ink
  2 red 1.0/0.25 peak annotations        6 cream panel + blue chart border
  3 footer 3 lines / right sizes         7 left-chart zero crosshair
  4 footer yellow emphasis marks
"""
import sys
import numpy as np
from PIL import Image

ORIG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "09_introduction_to_neural_networks/unique_slides/slide_026.jpg")
RENDER = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
          "09_introduction_to_neural_networks/recreated_pptx/build/"
          "slide_026_rejudge_rendered-1.png")

TOL = 6          # px tolerance in original-pixel space
results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def runs(prof, minlen=1):
    out, inr = [], False
    for i, v in enumerate(prof):
        if v > 0 and not inr:
            st, inr = i, True
        elif v == 0 and inr:
            out.append((st, i - 1)); inr = False
    if inr:
        out.append((st, len(prof) - 1))
    return [r for r in out if r[1] - r[0] + 1 >= minlen]


class Frame:
    """A frame normalised to original-pixel space (960x540)."""

    def __init__(self, path, is_render):
        im = Image.open(path).convert("RGB")
        self.is_render = is_render
        self.raw_w, self.raw_h = im.size
        if is_render:
            self.scale = self.raw_w / 960.0
            a = np.asarray(im.resize((960, 540), Image.LANCZOS)).astype(int)
        else:
            self.scale = 1.0
            a = np.asarray(im).astype(int)
        self.a = a
        mx = a.max(axis=2); mn = a.min(axis=2)
        self.sat = mx - mn
        self.dark = a.mean(axis=2) < 170

    # --- region helpers -------------------------------------------------
    def band(self, r0, r1, c0, c1):
        return self.a[r0:r1, c0:c1]

    def yellow(self, r0=440, r1=520, c0=50, c1=910):
        reg = self.band(r0, r1, c0, c1)
        return (reg[:, :, 0] > 190) & (reg[:, :, 1] > 190) & \
               (reg[:, :, 2] < 200) & (reg[:, :, 0] - reg[:, :, 2] > 55)

    def redness(self, r0, r1, c0, c1):
        reg = self.band(r0, r1, c0, c1)
        return reg[:, :, 0] - reg[:, :, 2]

    # --- measurements ---------------------------------------------------
    def cream_panel(self):
        """rows/cols of the cream (#feffe8-ish) equation panel."""
        reg = self.band(60, 240, 40, 930)
        m = (np.abs(reg[:, :, 0] - 254) < 8) & (np.abs(reg[:, :, 1] - 255) < 8) & \
            (np.abs(reg[:, :, 2] - 232) < 12)
        ys, xs = np.where(m)
        if not len(ys):
            return None
        return (ys.min() + 60, ys.max() + 60, xs.min() + 40, xs.max() + 40)

    def valuebox_fill(self, r0, r1):
        """cols spanned by the peach (#f6e4cc-ish) value-box fill."""
        reg = self.band(r0, r1, 520, 900)
        m = (reg[:, :, 0] > 225) & (reg[:, :, 1] > 205) & \
            (reg[:, :, 2] > 175) & (reg[:, :, 2] < 225) & \
            (reg[:, :, 0] - reg[:, :, 2] > 25)
        xs = np.where(m.sum(axis=0) > 5)[0]
        return (xs.min() + 520, xs.max() + 520) if len(xs) else None

    def formula_ink_cols(self, r0, r1, c0, c1):
        """ink columns of the formula text between the panel edge and the box."""
        reg = self.band(r0, r1, c0, c1)
        ink = reg.mean(axis=2) < 185
        xs = np.where(ink.sum(axis=0) > 0)[0]
        return (xs.min() + c0, xs.max() + c0) if len(xs) else None

    def red_annotations(self):
        """red ink pixels inside the right subplot (peak reference marks)."""
        m = self.redness(240, 425, 500, 820) > 35
        ys, xs = np.where(m)
        return len(ys), (xs.min() + 500, xs.max() + 500) if len(xs) else None

    def zero_crosshair_rows(self):
        """rows in the LEFT subplot carrying a long horizontal dark line."""
        reg = self.band(235, 430, 145, 495)
        d = reg.mean(axis=2) < 175
        counts = d.sum(axis=1)
        return [i + 235 for i, v in enumerate(counts) if v > 140]

    def blue_border_cols(self):
        reg = self.band(225, 440, 120, 840)
        m = (reg[:, :, 2] - reg[:, :, 0] > 35)
        ys, xs = np.where(m)
        return (xs.min() + 120, xs.max() + 120) if len(xs) else None

    def footer_lines(self):
        """ink bands of the three footer text lines."""
        reg = self.band(448, 512, 65, 895)
        d = reg.mean(axis=2) < 150
        p = d.sum(axis=1)
        rr = runs(p, 1)
        if not rr:
            return []
        lines, cur = [], [rr[0][0], rr[0][1]]
        for s, e in rr[1:]:
            if s - cur[1] <= 2:
                cur[1] = e
            else:
                lines.append(tuple(cur)); cur = [s, e]
        lines.append(tuple(cur))
        out = []
        for s, e in lines:
            xs = np.where(d[s:e + 1].any(axis=0))[0]
            out.append((s + 448, e + 448, xs.min() + 65, xs.max() + 65))
        return out

    def footer_line_hues(self):
        """maroon vs navy share of the dark ink per footer line."""
        reg = self.band(448, 512, 65, 895)
        lum = reg.mean(axis=2)
        d = lum < 135
        lines = self.footer_lines()
        out = []
        for s, e, c0, c1 in lines:
            sub = reg[s - 448:e - 447, c0 - 65:c1 - 64].reshape(-1, 3)
            m = (sub.mean(axis=1) < 135)
            sel = sub[m]
            if not len(sel):
                out.append((0, 0)); continue
            maroon = np.mean(sel[:, 0] > sel[:, 2] + 20)
            navy = np.mean(sel[:, 2] > sel[:, 0] + 20)
            out.append((maroon, navy))
        return out

    def accent_ink(self, r0, r1, c0, c1):
        """maroon vs dark share of the equation ink (definition vs derivative)."""
        reg = self.band(r0, r1, c0, c1)
        sel = reg.reshape(-1, 3)
        sel = sel[sel.mean(axis=1) < 150]
        if not len(sel):
            return 0.0, 0.0
        red = np.mean((sel[:, 0] > sel[:, 2] + 30))
        dark = np.mean((sel[:, 0] <= sel[:, 2] + 30))
        return red, dark


def main():
    o = Frame(ORIG, False)
    r = Frame(RENDER, True)
    print(f"original  : {o.raw_w}x{o.raw_h}")
    print(f"render    : {r.raw_w}x{r.raw_h}  (scale {r.scale:.4f} px/orig-px)")
    print(f"render is 150dpi 2001x1125 expected: "
          f"{'OK' if abs(r.raw_h - 1125) <= 2 and abs(r.raw_w - 2000) <= 3 else 'MISMATCH'}")
    print()

    # ---- finding 6a: cream equation panel -------------------------------
    op, rp = o.cream_panel(), r.cream_panel()
    ok = op and rp and abs(rp[0] - op[0]) <= TOL and abs(rp[1] - op[1]) <= TOL and \
        abs(rp[2] - op[2]) <= TOL and abs(rp[3] - op[3]) <= TOL
    check("finding6 cream equation panel", ok,
          f"orig rows {op[0]}..{op[1]} cols {op[2]}..{op[3]} | "
          f"render rows {rp[0]}..{rp[1]} cols {rp[2]}..{rp[3]}")

    # ---- finding 1: value boxes clear of the formulas -------------------
    for label, rows in (("row1", (100, 158)), ("row2", (168, 224))):
        of = o.formula_ink_cols(rows[0], rows[1], 60, 555)
        rf = r.formula_ink_cols(rows[0], rows[1], 60, 555)
        ob = o.valuebox_fill(rows[0], rows[1])
        rb = r.valuebox_fill(rows[0], rows[1])
        gap_o = ob[0] - of[1] if (ob and of) else -1
        gap_r = rb[0] - rf[1] if (rb and rf) else -1
        ok = gap_o > 0 and gap_r > 0 and abs(gap_r - gap_o) <= TOL + 6
        check(f"finding1 {label} value box clear of formula", ok,
              f"orig formula ends {of[1]}, box starts {ob[0]} (gap {gap_o}px) | "
              f"render formula ends {rf[1]}, box starts {rb[0]} (gap {gap_r}px)")
        okb = ob and rb and abs(rb[0] - ob[0]) <= TOL and abs(rb[1] - ob[1]) <= TOL
        check(f"finding1 {label} value box horizontal extent", bool(okb),
              f"orig cols {ob[0]}..{ob[1]} | render cols {rb[0]}..{rb[1]}")

    # ---- finding 2: red peak annotations --------------------------------
    oc, ocr = o.red_annotations()
    rc, rcr = r.red_annotations()
    check("finding2 red 1.0/0.25 annotations present", rc > 20,
          f"orig {oc} red px cols {ocr} | render {rc} red px cols {rcr}")

    # ---- finding 7: left chart zero crosshair ---------------------------
    oz, rz = o.zero_crosshair_rows(), r.zero_crosshair_rows()
    ok = len(rz) >= 1 and (not oz or min(abs(z - oz[0]) for z in rz) <= TOL)
    check("finding7 left-chart zero crosshair row", ok,
          f"orig rows {oz} | render rows {rz}")

    # ---- finding 6b: blue chart border ----------------------------------
    ob, rb = o.blue_border_cols(), r.blue_border_cols()
    ok = ob and rb and abs(rb[0] - ob[0]) <= TOL and abs(rb[1] - ob[1]) <= TOL
    check("finding6 blue chart-region border", bool(ok),
          f"orig cols {ob[0]}..{ob[1]} | render cols {rb[0]}..{rb[1]}")

    # ---- finding 3: footer 3 lines with the original's break -------------
    ol, rl = o.footer_lines(), r.footer_lines()
    check("finding3 footer has 3 text lines", len(rl) == 3,
          f"orig {len(ol)} lines {[ (s,e) for s,e,_,_ in ol ]} | "
          f"render {len(rl)} lines {[ (s,e) for s,e,_,_ in rl ]}")
    if len(ol) == 3 and len(rl) == 3:
        pitches_o = [ol[1][0] - ol[0][0], ol[2][0] - ol[1][0]]
        pitches_r = [rl[1][0] - rl[0][0], rl[2][0] - rl[1][0]]
        ok = all(abs(pitches_r[i] - pitches_o[i]) <= 3 for i in range(2))
        check("finding3 footer line pitch", ok,
              f"orig {pitches_o} px | render {pitches_r} px")
        # line [2] must wrap: the third line is shorter than the second
        ok = (rl[1][3] - rl[1][2]) > (rl[2][3] - rl[2][2])
        check("finding3 line [2] wraps onto line 3", ok,
              f"orig widths {ol[1][3]-ol[1][2]} / {ol[2][3]-ol[2][2]} | "
              f"render widths {rl[1][3]-rl[1][2]} / {rl[2][3]-rl[2][2]}")
        ok = abs((rl[0][3] - rl[0][2]) - (ol[0][3] - ol[0][2])) <= 40
        check("finding3 footer body size (line 1 ink width)", ok,
              f"orig {ol[0][3]-ol[0][2]} px | render {rl[0][3]-rl[0][2]} px")

    # ---- finding 4: yellow emphasis marks --------------------------------
    om, rm = o.yellow(), r.yellow()
    ocr = runs(om.sum(axis=0), 2)
    rcr = runs(rm.sum(axis=0), 2)
    ok = len(rcr) >= 3 and len(ocr) >= 3
    check("finding4 footer yellow highlights (3 marks)", ok,
          f"orig {len(ocr)} runs {[c for c in ocr]} | "
          f"render {len(rcr)} runs {[c for c in rcr]}")
    if ok:
        err = []
        for a, b in zip(ocr[:3], rcr[:3]):
            err.append(max(abs(a[0] - b[0]), abs(a[1] - b[1])))
        check("finding4 highlight positions within 20px", max(err) <= 20,
              f"per-mark max |delta| = {err} px")

    # ---- footer text colour (maroon line 1, navy lines 2-3) --------------
    oh, rh = o.footer_line_hues(), r.footer_line_hues()
    if len(oh) == 3 and len(rh) == 3:
        ok = rh[0][0] > 0.5 and rh[1][1] > 0.5 and rh[2][1] > 0.5
        check("footer colours: line1 maroon, lines2-3 navy", ok,
              f"orig maroon/navy {[ (round(m,2),round(n,2)) for m,n in oh ]} | "
              f"render {[ (round(m,2),round(n,2)) for m,n in rh ]}")

    # ---- finding 5: equation accent ink -----------------------------------
    for label, (r0, r1, c0, c1), expect in (
            ("row1 definition", (107, 152, 76, 300), "dark"),
            ("row1 derivative", (110, 150, 316, 540), "red"),
            ("row1 values", (115, 145, 660, 875), "red")):
        orr, odd = o.accent_ink(r0, r1, c0, c1)
        rrr, rdd = r.accent_ink(r0, r1, c0, c1)
        if expect == "dark":
            ok = odd > 0.5 and rdd > 0.5
            detail = f"orig dark-share {odd:.2f} | render dark-share {rdd:.2f}"
        else:
            ok = orr > 0.5 and rrr > 0.5
            detail = f"orig red-share {orr:.2f} | render red-share {rrr:.2f}"
        check(f"finding5 {label} ink", ok, detail)

    failed = [n for n, ok, _ in results if not ok]
    print()
    print(f"{len(results) - len(failed)}/{len(results)} checks passed")
    if failed:
        print("FAILED: " + "; ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
