from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
im = Image.open(f'{deck}/unique_slides/slide_049.jpg').convert('RGB')
px = im.load()

print('== 049 orig: W zone x694..712, y per-row ink (thr<200) ==')
for y in range(155, 190):
    cnt = [(x) for x in range(694, 712) if sum(px[x, y][:3]) / 3 < 200]
    if cnt:
        print(f'  y{y}: n={len(cnt)} x{cnt[0]}..{cnt[-1]}')

print('== 049 render (certified render_15?) W zone — use latest certified render ==')
import glob, os
renders = sorted(glob.glob(f'{deck}/recreated_pptx/qa/slide049/render_*.png'))
print('renders:', [os.path.basename(r) for r in renders[-3:]])
r = Image.open(renders[-1]).convert('RGB')
rp = r.load()
S = 2001 / 960
print('== 049 certified render W zone (orig-space) ==')
for oy in range(155, 190):
    y = int(oy * S)
    cnt = [int(x / S) for x in range(int(694 * S), int(712 * S))
           if sum(rp[x, y][:3]) / 3 < 200]
    if cnt:
        print(f'  y{oy}: n={len(cnt)} x{cnt[0]}..{cnt[-1]}')
