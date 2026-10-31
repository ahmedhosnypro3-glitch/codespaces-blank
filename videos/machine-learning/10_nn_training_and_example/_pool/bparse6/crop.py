import sys
from PIL import Image
src, x0, y0, x1, y1, out, scale = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], float(sys.argv[7])
im = Image.open(src).convert('RGB')
W, H = im.size
pad_x = int((x1-x0)*0.04); pad_y = int((y1-y0)*0.04)
bx0 = max(0, x0-pad_x); by0 = max(0, y0-pad_y); bx1 = min(W, x1+pad_x); by1 = min(H, y1+pad_y)
c = im.crop((bx0, by0, bx1, by1))
cw, ch = c.size
s = scale
if cw*s < 480: s = 480.0/cw
if max(cw, ch)*s > 1664: s = 1664.0/max(cw, ch)
c2 = c.resize((int(round(cw*s)), int(round(ch*s))), Image.LANCZOS)
c2.save(out)
print('crop %s box=(%d,%d)-(%d,%d) scale=%.3f size=%s' % (out, bx0, by0, bx1, by1, s, c2.size))
