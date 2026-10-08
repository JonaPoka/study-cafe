import json, base64, io, sys, os
BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build')
from PIL import Image, ImageDraw
A = json.load(open(os.path.join(BUILD, 'assets.json')))
def img(u): return Image.open(io.BytesIO(base64.b64decode(u.split(',', 1)[1]))).convert('RGBA')
name = sys.argv[1]; coll = len(sys.argv) > 2
s = A['scenes'][name]
c = img(s['bg'])
for o in sorted(s['objects'], key=lambda o: o['sortY']):
    c.alpha_composite(img(o['img']), (o['x'], o['y']))
d = ImageDraw.Draw(c)
if coll:
    for r in s['collisions']: d.rectangle([r['x'], r['y'], r['x'] + r['w'] - 1, r['y'] + r['h'] - 1], outline=(255, 60, 60, 255))
    for e in s['exits']: x, y, w, h = e['rect']; d.rectangle([x, y, x + w - 1, y + h - 1], outline=(80, 200, 255, 255))
    for st in s['seats']: d.ellipse([st['stand'][0]-3, st['stand'][1]-3, st['stand'][0]+3, st['stand'][1]+3], outline=(120,255,120,255))
c.resize((1280, 800), Image.NEAREST).save(os.path.join(BUILD, 'prev_%s.png' % name))
