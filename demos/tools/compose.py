import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import char

HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, '..', '..', 'assets', 'environment')
BUILD = os.path.join(HERE, 'build')
os.makedirs(BUILD, exist_ok=True)
W, H = 640, 400
random.seed(7)

_img = {}
def src(path):
    if path not in _img:
        _img[path] = Image.open(os.path.join(E, path)).convert('RGBA')
    return _img[path]

def crop(path, x, y, w, h):
    return src(path).crop((x, y, x + w, y + h))

scene = Image.new('RGBA', (W, H), (24, 18, 28, 255))
def put(im, x, y):
    scene.alpha_composite(im, (int(x), int(y)))

# ---------- room shell ----------
RX0, RX1 = 24, 616          # room interior
WALL_Y0, WALL_Y1 = 8, 104   # back wall
FLOOR_Y = WALL_Y1

# floor: Wood Floor A, column 1 (warm medium), mixing its three tile variants
for ty in range(FLOOR_Y, H, 32):
    for tx in range(RX0, RX1, 32):
        v = random.choices([0, 32, 64], weights=[6, 2, 2])[0]
        put(crop('Structure/Floor/Wood Floor A.png', 64, v, 32, 32), tx, ty)

# wallpaper: Striped Wallpaper A, teal column (6), second shade, middle tile repeated
WP_X = 96 * 6
for tx in range(RX0, RX1, 32):
    put(crop('Structure/Walls/Striped Wallpaper A.png', WP_X + 32, 128, 32, 96), tx, WALL_Y0)
# wainscot: Half-Wall Paneling A, dark wood, middle tile
for tx in range(RX0, RX1, 32):
    put(crop('Structure/Walls/Half-Wall Paneling A.png', 32, 0, 32, 32), tx, WALL_Y1 - 32)

# shadow along the bottom of the wall onto the floor
sh = Image.new('RGBA', (RX1 - RX0, 6), (0, 0, 0, 70))
put(sh, RX0, FLOOR_Y)

# side walls and ceiling edge
edge = (46, 33, 40, 255); edge_hi = (78, 58, 64, 255)
from PIL import ImageDraw
d = ImageDraw.Draw(scene)
d.rectangle([RX0 - 8, 0, RX0 - 1, H], fill=edge); d.line([(RX0 - 1, 0), (RX0 - 1, H)], fill=edge_hi)
d.rectangle([RX1, 0, RX1 + 7, H], fill=edge); d.line([(RX1, 0), (RX1, H)], fill=edge_hi)
d.rectangle([RX0 - 8, 0, RX1 + 7, WALL_Y0 - 1], fill=edge); d.line([(RX0, WALL_Y0 - 1), (RX1, WALL_Y0 - 1)], fill=edge_hi)

# ---------- wall decor ----------
# window pair (night panes) with a valance curtain
for wx in (96, 128):
    put(crop('Structure/Windows/Ornamental Windows A.png', 0, 18, 32, 92), wx, 10)
put(crop('Objects/Wall Items/Curtains.png', 0, 32, 96, 64), 80, 12)

# wall sconces flanking a painting
put(crop('Objects/Wall Items/Lighting, Wall.png', 0, 0, 32, 30), 184, 30)
put(crop('Objects/Wall Items/Paintings, Landscape.png', 72, 0, 48, 32), 220, 30)
put(crop('Objects/Wall Items/Lighting, Wall.png', 0, 0, 32, 30), 272, 30)
# posters
put(crop('Objects/Wall Items/Posters.png', 128, 64, 32, 32), 318, 32)
put(crop('Objects/Wall Items/Paintings, Landscape.png', 8, 96, 80, 30), 356, 32)

# wall shelf above the counter, with vases and bowls
put(crop('Objects/Furniture/Shelf.png', 0, 8, 96, 24), 464, 46)
put(crop('Objects/Small Items/Flowers.png', 0, 64, 32, 32), 466, 24)     # blue vase
put(crop('Objects/Small Items/Flowers.png', 64, 64, 32, 32), 486, 26)    # small white vase
put(crop('Objects/Small Items/Dishes A.png', 128, 0, 32, 32), 506, 32)   # bowl
put(crop('Objects/Small Items/Dishes A.png', 160, 0, 32, 32), 528, 30)   # bowl
put(crop('Objects/Small Items/Flowers.png', 128, 64, 32, 32), 544, 22)   # potted plant

# back-left tree in a blue vase
put(crop('Objects/Furniture/Planter.png', 64, 0, 32, 86), 36, 36)

# ---------- counter (right) ----------
CX, CY = 432, 98
put(crop('Objects/Furniture/Countertop.png', 96, 136, 32, 52), CX, CY)
for i in range(1, 5):
    put(crop('Objects/Furniture/Countertop.png', 128, 136, 32, 52), CX + 32 * i, CY)
put(crop('Objects/Furniture/Countertop.png', 160, 136, 32, 52), CX + 160, CY)
# on the counter
put(crop('Objects/Small Items/Coffee Maker.png', 0, 0, 32, 32), 444, 82)
put(crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 470, 100)
put(crop('Objects/Small Items/Food/Dessert.png', 0, 0, 32, 32), 500, 92)
put(crop('Objects/Small Items/Food/Dessert.png', 64, 0, 32, 32), 532, 92)
put(crop('Objects/Small Items/Lighting, Table.png', 64, 0, 32, 32), 566, 84)
put(crop('Objects/Small Items/Flowers.png', 0, 32, 32, 32), 594, 92)

chars = {}
def put_char(key, spec, anim, direction, i, x, y):
    put(char.frame(spec, anim, direction, i), x, y)
    chars[key] = {'x': x + 32, 'y': y + 12}

# bar stools with two people facing the counter
put(crop('Objects/Furniture/Seating/Bar Stools.png', 160, 0, 32, 32), 468, 156)
put(crop('Objects/Furniture/Seating/Bar Stools.png', 160, 0, 32, 32), 532, 156)
put_char('stoolA', dict(body='male', skin='taupe', hair='messy1', hairColor='chestnut', top='longsleeve', topColor='slate', legs='pants', legsColor='charcoal', shoes='brown'), 'sit', 'up', 2, 452, 120)
put_char('stoolB', dict(body='female', skin='bronze', hair='ponytail', hairColor='black', top='tshirt', topColor='yellow', legs='skirt', legsColor='forest', shoes='black'), 'sit', 'up', 2, 516, 120)

# ---------- rug + shared desk (center) ----------
put(crop('Objects/Furniture/Rugs/Swirling Vine Rug.png', 0, 64, 160, 64), 228, 200)
# chairs facing down behind the table
put(crop('Objects/Furniture/Seating/Chair, Dining C.png', 0, 96, 32, 32), 260, 178)
put(crop('Objects/Furniture/Seating/Chair, Dining C.png', 0, 96, 32, 32), 324, 178)
put_char('you', dict(body='female', skin='light', hair='long', hairColor='dark_brown', top='cardigan', topColor='red', legs='pants', legsColor='navy', shoes='black'), 'sit', 'down', 2, 244, 146)
put_char('friend', dict(body='male', skin='brown', hair='messy1', hairColor='black', top='tshirt', topColor='green', legs='pants', legsColor='charcoal', shoes='black', glasses=True), 'sit', 'down', 2, 308, 146)
# long table in front of them
put(crop('Objects/Furniture/Table, Rough Wood.png', 8, 148, 80, 44), 268, 186)
put(crop('Objects/Small Items/Laptop.png', 32, 96, 32, 32), 260, 178)
put(crop('Objects/Small Items/Loose Paper.png', 0, 0, 32, 32), 326, 184)
put(crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 314, 190)

# ---------- small round table, side seating (left) ----------
put(crop('Objects/Furniture/Seating/Chair, Dining C.png', 32, 0, 32, 32), 82, 210)
put_char('sideA', dict(body='female', skin='olive', hair='ponytail', hairColor='blonde', top='longsleeve', topColor='teal', legs='skirt', legsColor='maroon', shoes='brown'), 'sit', 'right', 2, 64, 176)
put(crop('Objects/Furniture/Seating/Chair, Dining C.png', 64, 0, 32, 32), 150, 210)
put_char('sideB', dict(body='male', skin='amber', hair='pixie', hairColor='ginger', top='tshirt', topColor='orange', legs='pants', legsColor='navy', shoes='black'), 'sit', 'left', 2, 136, 176)
put(crop('Objects/Furniture/Table, Rough Wood.png', 96, 32, 32, 32), 116, 214)
put(crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 122, 212)
put(crop('Objects/Small Items/Food/Dessert.png', 96, 32, 32, 32), 116, 206)

# ---------- sofa corner (lower right) ----------
put(crop('Objects/Furniture/Planter.png', 128, 32, 32, 54), 368, 262)
put(crop('Objects/Furniture/Seating/Loveseat, Small - Casual Solid A.png', 128, 0, 64, 32), 408, 284)
put_char('sofa', dict(body='female', skin='amber', hair='long', hairColor='rose', top='cardigan', topColor='lavender', legs='pants', legsColor='charcoal', shoes='white', glasses=True), 'sit', 'down', 2, 408, 254)
put(crop('Objects/Furniture/Table, Ornate Wood.png', 8, 32, 48, 30), 416, 322)
put(crop('Objects/Small Items/Food/Dessert.png', 96, 0, 32, 32), 424, 312)
put(crop('Objects/Furniture/Lighting, Floor.png', 0, 0, 32, 56), 474, 258)

# ---------- plants near the front ----------
put(crop('Objects/Furniture/Planter.png', 0, 32, 32, 54), 214, 292)
put(crop('Objects/Furniture/Planter.png', 32, 0, 32, 86), 584, 112)

# ---------- someone walking in ----------
put_char('walker', dict(body='female', skin='black', hair='pixie', hairColor='raven', top='tshirt', topColor='sky', legs='pants', legsColor='tan', shoes='white'), 'walk', 'up', 3, 282, 290)

scene.save(os.path.join(BUILD, 'scene_flat.png'))

# ---------- evening lighting ----------
a = np.asarray(scene).astype(np.float32) / 255.0
rgb = a[..., :3]
night = np.array([0.80, 0.74, 0.88], dtype=np.float32)
rgb = rgb * night
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
light = np.zeros((H, W), np.float32)
def glow(cx, cy, r, s):
    global light
    dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    light += s * np.clip(1 - dd, 0, 1) ** 2
for cx, cy, r, s in [(200, 44, 90, 0.55), (288, 44, 90, 0.55), (582, 96, 70, 0.5), (490, 270, 110, 0.6), (300, 160, 150, 0.25), (460, 100, 120, 0.2)]:
    glow(cx, cy, r, s)
warm = np.array([1.0, 0.72, 0.42], dtype=np.float32)
rgb = 1 - (1 - rgb) * (1 - np.clip(light, 0, 1)[..., None] * warm * 0.55)
rgb = rgb * (1 + np.clip(light, 0, 1)[..., None] * 0.18)
out = np.concatenate([np.clip(rgb, 0, 1), a[..., 3:]], axis=-1)
lit = Image.fromarray((out * 255).astype(np.uint8), 'RGBA')
lit.save(os.path.join(BUILD, 'scene_lit.png'))
lit.resize((W * 2, H * 2), Image.NEAREST).save(os.path.join(BUILD, 'scene_2x.png'))
json.dump(chars, open(os.path.join(BUILD, 'chars.json'), 'w'), indent=1)
print('ok', chars)
