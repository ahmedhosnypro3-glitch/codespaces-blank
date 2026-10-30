from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'

def exact_rows(label, path, x0, x1, y0, y1):
    im = Image.open(path).convert('RGB')
    px = im.load()
    print(f'== {label} ==')
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if sum(px[x, y][:3]) / 3 < 200]
        if xs:
            # compress into runs
            runs, cur = [], None
            for x in xs:
                if cur and x == cur[1] + 1:
                    cur[1] = x
                else:
                    cur = [x, x]; runs.append(cur)
            print(f'  y{y}: ' + ' '.join(f'{a}-{b}' if a != b else f'{a}' for a, b in runs))

exact_rows('051 aug W exact', f'{deck}/unique_slides/slide_051.jpg', 303, 317, 80, 88)

# 049 aug label: find the W first. "Initial W =" — W is the glyph right before '='.
# From certified comment: Initial underline y71..72 x365..422. Scan x400..440 y58..80.
exact_rows('049 aug W zone x400..440', f'{deck}/unique_slides/slide_049.jpg', 400, 440, 58, 80)
