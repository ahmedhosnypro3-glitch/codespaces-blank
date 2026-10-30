#!/usr/bin/env bash
# 2D bracketed matrix for slide 049: two stacked rows inside tall L/R brackets.
# Liberation Sans (Arial-metric) so it matches the deck's Arial; 600dpi transparent PNG.
# Args: out.png fontsize_pt color top_row bot_row
set -eu
out="$1"; fs="$2"; color="$3"; top="$4"; bot="$5"
FONT=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf
python3 - "$out" "$fs" "$color" "$top" "$bot" "$FONT" <<'PY'
import sys
from PIL import Image, ImageDraw, ImageFont
out, fs, color, top, bot, font_path = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
fs=int(fs); DPI=600; px=lambda pt: int(round(pt*DPI/72.0))
font_px=px(fs)
font=ImageFont.truetype(font_path, font_px)
col=(int(color[0:2],16),int(color[2:4],16),int(color[4:6],16),255)
# measure
tmp=Image.new("RGBA",(10,10)); d0=ImageDraw.Draw(tmp)
def txtbbox(s):
    b=d0.textbbox((0,0),s,font=font); return b
bb_t=txtbbox(top); bb_b=txtbbox(bot)
wt=bb_t[2]-bb_t[0]; wb=bb_b[2]-bb_b[0]; num_w=max(wt,wb)
line_h=px(fs*1.05); line_gap=px(fs*0.22); pad_v=px(fs*0.10)
stroke=max(3,px(0.9)); serif=px(2.2); margin=px(2.0)
left_w=margin+stroke+serif
top_h=line_h; bot_h=line_h
W=num_w + 2*left_w
H=pad_v + top_h + line_gap + bot_h + pad_v
canvas=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(canvas)
# numbers (baseline-aligned rows), left aligned after left bracket
nx=left_w
y_top=pad_v
y_bot=pad_v+top_h+line_gap
d.text((nx - bb_t[0], y_top - bb_t[1]), top, font=font, fill=col)
d.text((nx - bb_b[0], y_bot - bb_b[1]), bot, font=font, fill=col)
# tall brackets
by0=pad_v - px(0.6); by1=H-pad_v + px(0.6)
# left '['
xb=serif
d.line([(xb,by0),(xb,by1)],fill=col,width=stroke)
d.line([(xb, by0),(xb+serif, by0)],fill=col,width=stroke)
d.line([(xb, by1),(xb+serif, by1)],fill=col,width=stroke)
# right ']'
xr=W-stroke//2-serif*0
d.line([(xr,by0),(xr,by1)],fill=col,width=stroke)
d.line([(xr-serif, by0),(xr, by0)],fill=col,width=stroke)
d.line([(xr-serif, by1),(xr, by1)],fill=col,width=stroke)
canvas.save(out)
import json; print(json.dumps({"w_px":W,"h_px":H,"w_in":round(W/DPI,5),"h_in":round(H/DPI,5)}))
PY
