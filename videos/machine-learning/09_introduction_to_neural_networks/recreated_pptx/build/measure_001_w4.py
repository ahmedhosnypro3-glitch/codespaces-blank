import numpy as np
from PIL import Image

orig = np.asarray(Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_001.jpg').convert('RGB')).astype(int)
H, W, _ = orig.shape
print('orig', W, H)

def dark_rows(a, thresh=60):
    return [y for y in range(a.shape[0]) if a[y].mean() < thresh]

d = dark_rows(orig)
print('very dark rows (mean<60):', d[:5], '...', d[-5:], 'count', len(d))

# black band: rows with low mean
low = [y for y in range(H) if orig[y].mean() < 80]
print('rows mean<80:', low[:3], low[-3:], 'count', len(low))

# background sample (corner area inside frame)
print('bg samples:', orig[20,20], orig[520,480], orig[30,500])

# red border scan: find reddish pixels
r, g, b = orig[:,:,0], orig[:,:,1], orig[:,:,2]
redmask = (r > 100) & (r - g > 60) & (r - b > 60)
ys, xs = np.where(redmask)
if len(ys):
    print('red px count', len(ys), 'x range', xs.min(), xs.max(), 'y range', ys.min(), ys.max())
    print('topmost red rows sample y:', sorted(set(ys.tolist()))[:12])
    print('leftmost red cols sample x:', sorted(set(xs.tolist()))[:12])

# yellow badge region: yellowish bright pixels
ymask = (r > 200) & (g > 200) & (b < 150)
ys, xs = np.where(ymask)
if len(ys):
    print('yellow px count', len(ys), 'x range', xs.min(), xs.max(), 'y range', ys.min(), ys.max())

# blue text pixels (navy)
bmask = (b > 80) & (b - r > 40)
ys, xs = np.where(bmask)
if len(ys):
    print('blue px count', len(ys), 'x range', xs.min(), xs.max(), 'y range', ys.min(), ys.max())
    # cluster by row bands
    rows = np.where(bmask.any(axis=1))[0]
    if len(rows):
        groups = []
        start = rows[0]; prev = rows[0]
        for y in rows[1:]:
            if y - prev > 4:
                groups.append((start, prev)); start = y
            prev = y
        groups.append((start, prev))
        for gp in groups:
            print('  blue band rows', gp, 'x', xs[(ys>=gp[0])&(ys<=gp[1])].min(), xs[(ys>=gp[0])&(ys<=gp[1])].max())

# teal logo panel
tmask = (g > 100) & (b > 100) & (r < 100)
ys, xs = np.where(tmask)
if len(ys):
    print('teal px count', len(ys), 'x range', xs.min(), xs.max(), 'y range', ys.min(), ys.max())

# white logo panel bottom-right
sub = orig[400:540, 560:940]
whitemask = (sub[:,:,0] > 220) & (sub[:,:,1] > 220) & (sub[:,:,2] > 220)
ys, xs = np.where(whitemask)
if len(ys):
    print('white-in-lr px count', len(ys), 'x range', xs.min()+560, xs.max()+560, 'y range', ys.min()+400, ys.max()+400)

# title red row bands
ys, xs = np.where(redmask)
rows = np.where(redmask.any(axis=1))[0]
if len(rows):
    groups = []
    start = rows[0]; prev = rows[0]
    for y in rows[1:]:
        if y - prev > 6:
            groups.append((start, prev)); start = y
        prev = y
    groups.append((start, prev))
    for gp in groups:
        m = redmask[gp[0]:gp[1]+1]
        yy, xx = np.where(m)
        print('red band rows', gp, 'x', xx.min(), xx.max(), 'count', m.sum())
