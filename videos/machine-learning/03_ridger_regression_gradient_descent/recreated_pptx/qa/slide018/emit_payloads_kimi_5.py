#!/usr/bin/env python3
"""Bank slide 018's judge payloads extracted PROGRAMMATICALLY from the frozen deck
protocol (byte-for-byte; only NNN/K/NAME/region substitutions) + cut Procedure-B
crop pairs. 2026-10-24 (kimi-slide017).

Convention copied from the certified slide001 bank_prompts.py: the banked
judge_prompt_K.txt / crop_K_NAME_judge_prompt_K.txt files hold ONLY the -p
payload prose; the shell command lines live in judge_commands_K.sh.

Why not a full fenced-block emit: the template's command part carries the
filenames render_K.png / judge_attempt_K.txt / crop_K_NAME_*.png inside -p?? no,
inside the argv; a byte-exact reverse check over the whole block is not possible
for K=5 because "4" already occurs in 13.33x7.5in / 2.083 and in "(4)"-style
prose. Emitting the -p payload only makes the reverse byte-check exact and
unambiguous, which is what the deck convention demands.

K substitution rule: the frozen template writes "attempt K" inside the --view
string, which lives in the command part, not the -p payload; the -p payloads
carry NO K token (verified: zero matches in both payloads). So the only
substitutions inside the emitted payload files are NNN -> 017 and, for Template
B, NAME + the region description -- plus "attempt K" -> "attempt 5" for safety.
"""
import os
import re
import json
import hashlib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PROTO = os.path.join(DECK, "shared_patterns", "judge_protocol_03.md")
RENDER = os.path.join(HERE, "render_5.png")
ORIG = os.path.join(DECK, "unique_slides", "slide_018.jpg")

NNN = "018"
K = "5"

text = open(PROTO, encoding="utf-8").read()

def payload_of(marker, expect_start):
    m = text.split(marker)[1]
    block = m.split("```")[1]
    line = next(l for l in block.splitlines() if l.strip().startswith('-p "'))
    p = line.strip()[len('-p "'):-1]
    assert p.startswith(expect_start), p[:60]
    return p

payloadA = payload_of("Comparison (the real judge", "GROUND RULES")
payloadB = payload_of("## Template B — crop-pair judge", "GROUND RULES")

# zero K tokens in either payload prose -- precondition for the byte-check
for nm, p in [("A", payloadA), ("B", payloadB)]:
    assert re.search(r"\bK\b", p) is None, "payload %s carries a K token" % nm

pA = payloadA.replace("NNN", NNN).replace("attempt K", "attempt " + K)
assert "NNN" not in pA and "attempt K" not in pA
# reverse byte-check (must reproduce the frozen payload exactly)
assert pA.replace("attempt " + K, "attempt K").replace(NNN, "NNN") == payloadA
open(os.path.join(HERE, "judge_prompt_%s.txt" % K), "w", encoding="utf-8").write(pA + "\n")
print("banked judge_prompt_%s.txt (%d chars; reverse byte-check OK)" % (K, len(pA)))
print("  payloadA sha256:", hashlib.sha256(pA.encode()).hexdigest()[:16])

ri = Image.open(RENDER).convert("RGB")
oi = Image.open(ORIG).convert("RGB")
S = ri.height / 540.0
print("render_5.png %dx%d scale %.6f (paren-refit render)"
      % (ri.width, ri.height, S))

# Procedure-B regions picked from the ORIGINAL frame (dense regions, ~8px pad):
#  wbox  = W-box band 1 (red-bordered box: W, =, parenthesised vector, ||W||^2)
#  band1 = full band-1 strip (Train table, arrows, W box, Test table + mint y row)
#  test  = the three Test tables' label column + mint y-rows
REGIONS = [
    ("wbox",  (497, 119, 632, 259)),
    ("band1", (84, 118, 880, 258)),
    ("band2", (84, 255, 880, 395)),
    ("band3", (84, 392, 880, 532)),
    ("test",  (660, 88, 880, 258)),
    ("mark",  (660, 350, 880, 395)),
]
DESCS = json.load(open(os.path.join(HERE, "region_descs_%s.json" % K), encoding="utf-8"))

for name, (x0, y0, x1, y1) in REGIONS:
    desc = DESCS[name]
    # render crop from render_4 at scale S; original crop from the 960x540 frame,
    # LANCZOS-upscaled to the render crop's PIXEL SIZE (equal effective scale)
    rc = ri.crop((int(round(x0 * S)), int(round(y0 * S)), int(round(x1 * S)), int(round(y1 * S))))
    oc = oi.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(os.path.join(HERE, "crop_%s_%s_render.png" % (K, name)))
    oc.save(os.path.join(HERE, "crop_%s_%s_orig.png" % (K, name)))
    sx_r, sy_r = rc.size[0] / (x1 - x0), rc.size[1] / (y1 - y0)
    sx_o, sy_o = oc.size[0] / (x1 - x0), oc.size[1] / (y1 - y0)
    assert abs(sx_r - sx_o) < 1e-9 and abs(sy_r - sy_o) < 1e-9, "crop %s scale mismatch" % name
    print("crop %-5s frame(%d..%d, %d..%d) size=%s effective scale x=%.5f y=%.5f EQUAL"
          % (name, x0, x1, y0, y1, rc.size, sx_r, sy_r))
    p = payloadB.replace("NNN", NNN).replace("NAME", name).replace(
        "<one-line description of what the region contains>", desc)
    assert "NNN" not in p and "NAME" not in p and "<one-line description" not in p
    back = p.replace(desc, "<one-line description of what the region contains>").replace(
        name, "NAME").replace(NNN, "NNN")
    assert back == payloadB, "Template B(%s) reverse byte-check FAILED" % name
    open(os.path.join(HERE, "crop_%s_%s_judge_prompt_%s.txt" % (K, name, K)), "w",
         encoding="utf-8").write(p + "\n")
    print("  banked crop_%s_%s_judge_prompt_%s.txt (%d chars; reverse byte-check OK)" % (K, name, K, len(p)))

print("\nAUDIT: payload A sha256 %s" % hashlib.sha256(pA.encode()).hexdigest()[:16])
print("ALL PAYLOAD FILES EMITTED FOR K=%s (payload-only convention, slide001 parity)" % K)

# Cross-check: the banked shell scripts must use exactly these payload paths.
SH = "\n".join(open(os.path.join(HERE, f), encoding="utf-8").read()
               for f in ("judge_commands_kimi_5.sh", "judge_crops_kimi_5.sh"))
# expand ${NAME} in the crop loop's references before matching
SH_EXPANDED = "\n".join(sh.replace("${NAME}", n).replace("$NAME", n)
                         for sh in SH.splitlines() for n in ("wbox", "band1", "band2", "band3"))
for need in ("judge_prompt_5.txt", "crop_5_wbox_judge_prompt_5.txt",
             "crop_5_band1_judge_prompt_5.txt", "crop_5_band2_judge_prompt_5.txt",
             "crop_5_band3_judge_prompt_5.txt",
             "render_5.png", "crop_5_wbox_render.png", "crop_5_wbox_orig.png",
             "crop_5_band1_render.png", "crop_5_band1_orig.png",
             "crop_5_band2_render.png", "crop_5_band2_orig.png",
             "crop_5_band3_render.png", "crop_5_band3_orig.png"):
    assert need in SH_EXPANDED, "dispatch script does not reference %s" % need
print("CROSS-CHECK OK: banked dispatch scripts reference the emitted payload/crop files")
