"""Builds assets.json for the Study Café demo.

Scenes: the central plaza, your café, and the weekly café (same room, different palette).
Each scene has a static background, y-sorted objects with collision boxes, seats, exits,
light glows and NPCs. Character parts, palettes and credits are shared."""
import os, sys, json, base64, io, csv, random, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import parts

HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, '..', '..', 'assets', 'environment')
U = os.path.join(HERE, '..', '..', 'assets', 'characters')
BUILD = os.path.join(HERE, 'build')
os.makedirs(BUILD, exist_ok=True)
W, H = 640, 400

_img = {}
used_eliza = set()
def src(path):
    used_eliza.add(path)
    if path not in _img:
        _img[path] = Image.open(os.path.join(E, path)).convert('RGBA')
    return _img[path]
def crop(path, x, y, w, h):
    return src(path).crop((x, y, x + w, y + h))
def uri(im):
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

class Scene:
    def __init__(self, bgcolor=(24, 18, 28, 255)):
        self.bg = Image.new('RGBA', (W, H), bgcolor)
        self.objects, self.collisions = [], []
    def put(self, im, x, y):
        self.bg.alpha_composite(im, (int(x), int(y)))
    def obj(self, name, pieces, sortY, coll=None):
        x0 = min(p[1] for p in pieces); y0 = min(p[2] for p in pieces)
        x1 = max(p[1] + p[0].size[0] for p in pieces); y1 = max(p[2] + p[0].size[1] for p in pieces)
        im = Image.new('RGBA', (x1 - x0, y1 - y0))
        for p, x, y in pieces: im.alpha_composite(p, (x - x0, y - y0))
        bb = im.getbbox(); im2 = im.crop(bb)
        self.objects.append({'name': name, 'x': x0 + bb[0], 'y': y0 + bb[1], 'sortY': sortY, 'img': uri(im2)})
        for c in (coll or []): self.collisions.append({'name': name, 'x': c[0], 'y': c[1], 'w': c[2], 'h': c[3]})

# =====================================================================
# Café room (used twice with different palettes)
# =====================================================================
def cafe_background(seed, wall_col, wall_shade, floor_col, rug_row, panel_row):
    random.seed(seed)
    s = Scene()
    RX0, RX1, WY0, WY1 = 24, 616, 8, 104
    for ty in range(WY1, H, 32):
        for tx in range(RX0, RX1, 32):
            v = random.choices([0, 32, 64], weights=[6, 2, 2])[0]
            s.put(crop('Structure/Floor/Wood Floor A.png', 32 * floor_col, v, 32, 32), tx, ty)
    for tx in range(RX0, RX1, 32):
        s.put(crop('Structure/Walls/Striped Wallpaper A.png', 96 * wall_col + 32, 128 * wall_shade, 32, 96), tx, WY0)
        s.put(crop('Structure/Walls/Half-Wall Paneling A.png', 32, 32 * panel_row, 32, 32), tx, WY1 - 32)
    s.put(Image.new('RGBA', (RX1 - RX0, 6), (0, 0, 0, 70)), RX0, WY1)
    d = ImageDraw.Draw(s.bg)
    edge = (46, 33, 40, 255); hi = (78, 58, 64, 255)
    d.rectangle([RX0 - 8, 0, RX0 - 1, H], fill=edge); d.line([(RX0 - 1, 0), (RX0 - 1, H)], fill=hi)
    d.rectangle([RX1, 0, RX1 + 7, H], fill=edge); d.line([(RX1, 0), (RX1, H)], fill=hi)
    d.rectangle([RX0 - 8, 0, RX1 + 7, WY0 - 1], fill=edge); d.line([(RX0, WY0 - 1), (RX1, WY0 - 1)], fill=hi)
    # doorway at the bottom: a mat and a gap in the shadow
    d.rectangle([292, 384, 347, 399], fill=(70, 46, 34, 255)); d.rectangle([296, 387, 343, 396], fill=(122, 86, 58, 255))
    for wx in (96, 128):
        s.put(crop('Structure/Windows/Ornamental Windows A.png', 0, 18, 32, 92), wx, 10)
    s.put(crop('Objects/Wall Items/Curtains.png', 0, 32, 96, 64), 80, 12)
    s.put(crop('Objects/Wall Items/Lighting, Wall.png', 0, 0, 32, 30), 184, 30)
    s.put(crop('Objects/Wall Items/Paintings, Landscape.png', 72, 0, 48, 32), 220, 30)
    s.put(crop('Objects/Wall Items/Lighting, Wall.png', 0, 0, 32, 30), 272, 30)
    s.put(crop('Objects/Wall Items/Posters.png', 128, 64, 32, 32), 318, 32)
    s.put(crop('Objects/Wall Items/Paintings, Landscape.png', 8, 96, 80, 30), 356, 32)
    s.put(crop('Objects/Furniture/Shelf.png', 0, 8, 96, 24), 464, 46)
    s.put(crop('Objects/Small Items/Flowers.png', 0, 64, 32, 32), 466, 24)
    s.put(crop('Objects/Small Items/Flowers.png', 64, 64, 32, 32), 486, 26)
    s.put(crop('Objects/Small Items/Dishes A.png', 128, 0, 32, 32), 506, 32)
    s.put(crop('Objects/Small Items/Dishes A.png', 160, 0, 32, 32), 528, 30)
    s.put(crop('Objects/Small Items/Flowers.png', 128, 64, 32, 32), 544, 22)
    s.put(crop('Objects/Furniture/Rugs/Swirling Vine Rug.png', 0, 64 * rug_row, 160, 64), 228, 200)
    return s

def cafe_objects(s, sofa_col):
    P = 'Objects/Furniture/Planter.png'
    s.obj('tree in vase', [(crop(P, 64, 0, 32, 86), 36, 36)], 122, [(40, 112, 24, 10)])
    CX, CY = 432, 98
    cp = [(crop('Objects/Furniture/Countertop.png', 96, 136, 32, 52), CX, CY)]
    cp += [(crop('Objects/Furniture/Countertop.png', 128, 136, 32, 52), CX + 32 * i, CY) for i in range(1, 5)]
    cp += [(crop('Objects/Furniture/Countertop.png', 160, 136, 32, 52), CX + 160, CY)]
    cp += [(crop('Objects/Small Items/Coffee Maker.png', 0, 0, 32, 32), 444, 82),
           (crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 470, 100),
           (crop('Objects/Small Items/Food/Dessert.png', 0, 0, 32, 32), 500, 92),
           (crop('Objects/Small Items/Food/Dessert.png', 64, 0, 32, 32), 532, 92),
           (crop('Objects/Small Items/Lighting, Table.png', 64, 0, 32, 32), 566, 84),
           (crop('Objects/Small Items/Flowers.png', 0, 32, 32, 32), 594, 92)]
    s.obj('counter', cp, 150, [(432, 108, 184, 42)])
    stool = crop('Objects/Furniture/Seating/Bar Stools.png', 160, 0, 32, 32)
    s.obj('bar stool A', [(stool, 468, 156)], 186, [(476, 178, 16, 8)])
    s.obj('bar stool B', [(stool, 532, 156)], 186, [(540, 178, 16, 8)])
    s.obj('tree in planter', [(crop(P, 32, 0, 32, 86), 584, 112)], 198, [(588, 186, 24, 12)])
    C = 'Objects/Furniture/Seating/Chair, Dining C.png'
    chair_down, chair_r, chair_l = crop(C, 0, 96, 32, 32), crop(C, 32, 0, 32, 32), crop(C, 64, 0, 32, 32)
    s.obj('desk chair L', [(chair_down, 260, 178)], 208, [(264, 198, 24, 10)])
    s.obj('desk chair R', [(chair_down, 324, 178)], 208, [(328, 198, 24, 10)])
    s.obj('desk', [(crop('Objects/Furniture/Table, Rough Wood.png', 8, 148, 80, 44), 268, 186),
                   (crop('Objects/Small Items/Laptop.png', 32, 96, 32, 32), 260, 178),
                   (crop('Objects/Small Items/Loose Paper.png', 0, 0, 32, 32), 326, 184),
                   (crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 314, 190)], 230, [(270, 210, 76, 20)])
    s.obj('round table A chair L', [(chair_r, 82, 210)], 242, [(86, 228, 24, 12)])
    s.obj('round table A chair R', [(chair_l, 150, 210)], 242, [(154, 228, 24, 12)])
    s.obj('round table A', [(crop('Objects/Furniture/Table, Rough Wood.png', 96, 32, 32, 32), 116, 214),
                            (crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 122, 212),
                            (crop('Objects/Small Items/Food/Dessert.png', 96, 32, 32, 32), 116, 206)], 246, [(120, 232, 24, 14)])
    s.obj('round table B chair L', [(chair_r, 82, 312)], 344, [(86, 330, 24, 12)])
    s.obj('round table B chair R', [(chair_l, 150, 312)], 344, [(154, 330, 24, 12)])
    s.obj('round table B', [(crop('Objects/Furniture/Table, Rough Wood.png', 160, 32, 32, 32), 116, 316),
                            (crop('Objects/Small Items/Flowers.png', 32, 32, 32, 32), 116, 302)], 348, [(120, 334, 24, 14)])
    s.obj('fern box', [(crop(P, 0, 32, 32, 54), 214, 292)], 346, [(216, 334, 28, 12)])
    s.obj('fern pot', [(crop(P, 128, 32, 32, 54), 368, 262)], 316, [(372, 304, 24, 12)])
    s.obj('loveseat', [(crop('Objects/Furniture/Seating/Loveseat, Small - Casual Solid A.png', 64 * sofa_col, 0, 64, 32), 408, 284)], 314, [(410, 300, 60, 14)])
    s.obj('coffee table', [(crop('Objects/Furniture/Table, Ornate Wood.png', 8, 32, 48, 30), 416, 322),
                           (crop('Objects/Small Items/Food/Dessert.png', 96, 0, 32, 32), 424, 312)], 352, [(418, 338, 44, 14)])
    s.obj('floor lamp', [(crop('Objects/Furniture/Lighting, Floor.png', 0, 0, 32, 56), 474, 258)], 314, [(484, 304, 12, 10)])

CAFE_SEATS = [
 {'id': 'deskL', 'label': 'Shared desk', 'frame': [244, 146], 'dir': 'down', 'sortY': 209, 'stand': [276, 190]},
 {'id': 'deskR', 'label': 'Shared desk', 'frame': [308, 146], 'dir': 'down', 'sortY': 209, 'stand': [340, 190]},
 {'id': 'roundAL', 'label': 'Round table', 'frame': [64, 176], 'dir': 'right', 'sortY': 243, 'stand': [70, 252]},
 {'id': 'roundAR', 'label': 'Round table', 'frame': [136, 176], 'dir': 'left', 'sortY': 243, 'stand': [192, 240]},
 {'id': 'roundBL', 'label': 'Corner table', 'frame': [64, 278], 'dir': 'right', 'sortY': 345, 'stand': [70, 354]},
 {'id': 'roundBR', 'label': 'Corner table', 'frame': [136, 278], 'dir': 'left', 'sortY': 345, 'stand': [192, 344]},
 {'id': 'stoolA', 'label': 'Counter', 'frame': [452, 120], 'dir': 'up', 'sortY': 187, 'stand': [484, 198]},
 {'id': 'stoolB', 'label': 'Counter', 'frame': [516, 120], 'dir': 'up', 'sortY': 187, 'stand': [548, 198]},
 {'id': 'sofaL', 'label': 'Sofa', 'frame': [392, 254], 'dir': 'down', 'sortY': 315, 'stand': [424, 326]},
 {'id': 'sofaR', 'label': 'Sofa', 'frame': [424, 254], 'dir': 'down', 'sortY': 315, 'stand': [456, 326]},
]
CAFE_GLOWS = [[200, 44, 90, 0.55], [288, 44, 90, 0.55], [582, 96, 70, 0.5], [490, 270, 110, 0.6], [300, 170, 150, 0.22], [460, 110, 120, 0.2], [134, 230, 60, 0.15]]
CAFE_EXIT = {'id': 'toPlaza', 'rect': [292, 378, 56, 18], 'to': 'plaza', 'label': 'Back to the plaza', 'auto': 'down'}

def build_cafe(seed, wall_col, wall_shade, floor_col, rug_row, panel_row, sofa_col):
    s = cafe_background(seed, wall_col, wall_shade, floor_col, rug_row, panel_row)
    cafe_objects(s, sofa_col)
    return s

cafe = build_cafe(7, 6, 1, 2, 1, 0, 2)      # teal wallpaper, warm floor, pink rug, blue sofa
weekly = build_cafe(11, 10, 0, 4, 0, 2, 0)  # peach wallpaper, light floor, blue rug, yellow sofa

# =====================================================================
# Plaza
# =====================================================================
random.seed(3)
pz = Scene((50, 92, 40, 255))
T = 'Terrain/terrain_summer.png'
for ty in range(0, H, 32):
    for tx in range(0, W, 32):
        pz.put(crop(T, random.choice([96, 128, 160]), 64, 32, 32), tx, ty)
# stone paving for the square (Tile C, warm slabs), from just under the houses to the bottom
for ty in range(172, H, 32):
    for tx in range(0, W, 32):
        pz.put(crop('Structure/Floor/Tile C.png', random.choice([0, 32]), random.choice([0, 32]), 32, 32), tx, ty)
d = ImageDraw.Draw(pz.bg)
d.line([(0, 171), (W, 171)], fill=(96, 78, 70, 255)); d.line([(0, 172), (W, 172)], fill=(150, 128, 112, 255))
def grass_island(x, y, w, h):
    # 9-slice the grass island tiles (terrain 0..96) over the paving
    for ty in range(y, y + h, 32):
        for tx in range(x, x + w, 32):
            cx = 0 if tx == x else (64 if tx + 32 >= x + w else 32)
            cy = 0 if ty == y else (64 if ty + 32 >= y + h else 32)
            pz.put(crop(T, cx, cy, 32, 32), tx, ty)
grass_island(-32, 300, 192, 160)
grass_island(480, 300, 192, 160)
grass_island(256, 236, 128, 96)       # lawn ring around the fountain
# flowers along the house fronts and lawns (background layer)
FL = 'Terrain/flowers.png'
for x, col in ((36, 1), (124, 4), (156, 6), (268, 7), (396, 2), (468, 5), (500, 1), (604, 3)):
    pz.put(crop(FL, 32 * col, 0, 32, 32), x, 170)
for x, y, col in ((8, 330, 0), (40, 352, 5), (96, 332, 3), (520, 336, 6), (560, 354, 1), (600, 330, 4)):
    pz.put(crop(FL, 32 * col, 32, 32, 32), x, y)

TREES = 'Terrain/trees_summer.png'
tree_a = crop(TREES, 128, 8, 96, 104)
tree_b = crop(TREES, 224, 8, 96, 104)
tree_c = crop(TREES, 320, 176, 96, 88)
# trees behind and between the buildings
pz.obj('tree back L', [(tree_b, -40, 30)], 128, [])
pz.obj('tree back gap', [(tree_a, 384, 40)], 140, [(416, 132, 24, 10)])
pz.obj('tree back R', [(tree_c, 588, 50)], 132, [])
# buildings, doors on the street side
pz.obj('your cafe building', [(crop('Structure/Structures/Brick House A.png', 0, 0, 256, 224), 8, 0)], 176, [(32, 60, 208, 116)])
pz.obj('directory building', [(crop('Structure/Structures/Brick House B.png', 0, 0, 192, 192), 236, 4)], 190, [(260, 60, 144, 128)])
pz.obj('weekly cafe building', [(crop('Structure/Structures/Paneled House A.png', 0, 0, 160, 160), 452, 20)], 178, [(452, 60, 160, 102), (452, 162, 112, 16)])
# fountain
pz.obj('fountain', [(crop('Structure/Misc/Fountain A.png', 0, 0, 64, 82), 288, 232)], 312, [(292, 286, 56, 24)])
# street lamps
lamp = crop('Objects/Furniture/Lighting, Outdoors.png', 0, 0, 32, 86)
for i, (x, y) in enumerate(((240, 200), (368, 200), (148, 300), (460, 300))):
    pz.obj('lamp %d' % i, [(lamp, x, y)], y + 84, [(x + 10, y + 78, 12, 8)])
# outdoor café tables in front of your café
C = 'Objects/Furniture/Seating/Chair, Dining C.png'
pz.obj('outdoor chair L', [(crop(C, 32, 32, 32, 32), 124, 218)], 250, [(128, 236, 24, 12)])
pz.obj('outdoor chair R', [(crop(C, 64, 32, 32, 32), 192, 218)], 250, [(196, 236, 24, 12)])
pz.obj('outdoor table', [(crop('Objects/Furniture/Table, Rough Wood.png', 160, 32, 32, 32), 158, 222),
                         (crop('Objects/Small Items/Coffee Maker.png', 64, 16, 16, 16), 166, 220)], 254, [(162, 240, 24, 14)])
# bushes and topiaries
PL = 'Terrain/plants_summer.png'
for x, y in ((420, 152), (520, 150)):
    pz.obj('topiary', [(crop(PL, 32, 64, 32, 64), x, y)], y + 62, [(x + 8, y + 52, 16, 10)])
pz.obj('tree front L', [(tree_a, -20, 290)], 392, [(16, 380, 24, 12)])
pz.obj('tree front R', [(tree_b, 556, 292)], 394, [(592, 382, 24, 12)])

PLAZA_SEATS = [
 {'id': 'outL', 'label': 'Outdoor table', 'frame': [106, 184], 'dir': 'right', 'sortY': 251, 'stand': [138, 262]},
 {'id': 'outR', 'label': 'Outdoor table', 'frame': [174, 184], 'dir': 'left', 'sortY': 251, 'stand': [208, 262]},
]
PLAZA_EXITS = [
 {'id': 'yourCafe', 'rect': [72, 172, 32, 26], 'to': 'cafe', 'label': 'Enter your café', 'auto': 'up', 'spawn': [88, 210, 'down']},
 {'id': 'directory', 'rect': [332, 186, 32, 20], 'to': 'directory', 'label': 'Open the café directory', 'auto': 'up', 'spawn': [348, 214, 'down']},
 {'id': 'weekly', 'rect': [564, 172, 32, 26], 'to': 'weekly', 'label': 'Enter the weekly café', 'auto': 'up', 'spawn': [580, 210, 'down']},
]
PLAZA_SIGNS = [
 {'x': 88, 'y': 138, 'title': 'Your café', 'sub': 'Midnight Study Café'},
 {'x': 348, 'y': 148, 'title': 'Café directory', 'sub': 'Find public cafés'},
 {'x': 580, 'y': 120, 'title': 'Weekly café', 'sub': 'Nordic Nook by mira'},
]
PLAZA_GLOWS = [[256, 214, 90, 0.7], [384, 214, 90, 0.7], [164, 314, 90, 0.7], [476, 314, 90, 0.7],
               [210, 140, 40, 0.45], [100, 140, 36, 0.4], [300, 170, 36, 0.35], [540, 110, 40, 0.4], [320, 280, 80, 0.2]]

# =====================================================================
# character parts, palettes, credits
# =====================================================================
sheets = {}
for p in parts.all_paths():
    for a in parts.ANIMS:
        im = Image.open(os.path.join(U, 'spritesheets', p, a + '.png')).convert('RGBA')
        sheets[p + '|' + a] = uri(im)
def pal(name): return json.load(open(os.path.join(U, 'palette_definitions', name)))
palettes = {'body': pal('body/body_ulpc.json'), 'hair': pal('hair/hair_ulpc.json'),
            'cloth': pal('cloth/cloth_ulpc.json'), 'eye': pal('eye/eye_ulpc.json'),
            'base': {'body': 'light', 'hair': 'orange', 'cloth': 'white', 'eye': 'blue'}}
catalog = {
 'body': parts.BODY, 'head': parts.HEAD, 'face': parts.FACE, 'nose': parts.NOSE, 'brows': parts.BROWS,
 'hair': {k: {'label': v[0], 'fg': v[1], 'bg': v[2]} for k, v in parts.HAIR.items()},
 'top': {k: {'label': v[0], 'path': v[1]} for k, v in parts.TOP.items()},
 'legs': {k: {'label': v[0], 'path': v[1]} for k, v in parts.LEGS.items()},
 'feet': {k: {'label': v[0], 'path': v[1], 'z': v[2]} for k, v in parts.FEET.items()},
 'glasses': parts.GLASSES, 'scarf': parts.SCARF,
}
cred_people, cred_lic = set(), set()
used_files = {p + '/' + a + '.png' for p in parts.all_paths() for a in parts.ANIMS}
with open(os.path.join(U, 'CREDITS.csv'), newline='') as f:
    for row in csv.DictReader(f):
        if row['filename'].strip() in used_files:
            cred_people.update(a.strip() for a in row['authors'].split(',') if a.strip())
            cred_lic.update(l.strip() for l in row['licenses'].split(',') if l.strip())
eliza_people = set()
for path in used_eliza:
    cf = os.path.join(os.path.dirname(os.path.join(E, path)), 'Credits.txt')
    if os.path.exists(cf):
        txt = open(cf, encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'ARTIST\(S\):\s*(.+)', txt):
            eliza_people.update(a.strip() for a in m.group(1).split(',') if a.strip())
credits = {
 'characters': {'source': 'Universal LPC Spritesheet Character Generator', 'url': 'https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator',
                'licenses': sorted(cred_lic), 'authors': sorted(cred_people)},
 'room': {'source': 'LPC Revised (Eliza Wyatt and contributors)', 'url': 'https://github.com/ElizaWy/LPC',
          'licenses': ['CC-BY 3.0', 'OGA-BY 3.0'], 'authors': sorted(eliza_people)},
}

def scene_json(s, **extra):
    d = {'bg': uri(s.bg), 'objects': s.objects, 'collisions': s.collisions}
    d.update(extra); return d

out = {
 'size': [W, H],
 'scenes': {
  'plaza': scene_json(pz, name='Central Plaza', sub='Pick a café, or sit outside', bounds={'x0': 8, 'x1': 632, 'y0': 150, 'y1': 396},
                      seats=PLAZA_SEATS, exits=PLAZA_EXITS, signs=PLAZA_SIGNS, glows=PLAZA_GLOWS, tint='#A79CC8', spawn=[320, 380, 'up']),
  'cafe': scene_json(cafe, name='Midnight Study Café', sub='your café', bounds={'x0': 32, 'x1': 608, 'y0': 116, 'y1': 396},
                     seats=CAFE_SEATS, exits=[CAFE_EXIT], signs=[], glows=CAFE_GLOWS, tint='#CCBDE0', spawn=[320, 376, 'up']),
  'weekly': scene_json(weekly, name='Nordic Nook', sub='weekly café · built by mira', bounds={'x0': 32, 'x1': 608, 'y0': 116, 'y1': 396},
                       seats=CAFE_SEATS, exits=[CAFE_EXIT], signs=[], glows=CAFE_GLOWS, tint='#D6C8DE', spawn=[320, 376, 'up']),
 },
 'sheets': sheets, 'palettes': palettes, 'catalog': catalog, 'credits': credits,
 'icons': {'bean': uri(Image.open(os.path.join(HERE, '..', '..', 'assets', 'ui', 'icon-bean.png')))},
}
json.dump(out, open(os.path.join(BUILD, 'assets.json'), 'w'))
for name, s in (('plaza', pz), ('cafe', cafe), ('weekly', weekly)):
    s.bg.save(os.path.join(BUILD, 'bg_%s.png' % name))
print('ok', {k: len(v['objects']) for k, v in out['scenes'].items()}, os.path.getsize(os.path.join(BUILD, 'assets.json')) // 1024, 'KB')
