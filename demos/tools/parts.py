# Part catalog for the demo. Paths are relative to ULPC spritesheets/. {F}/{M} = female/male variants.
BODY = {'female': 'body/bodies/female', 'male': 'body/bodies/male'}
HEAD = {'female': 'head/heads/human/female', 'male': 'head/heads/human/male'}
FACE = {'female': 'head/faces/female/neutral', 'male': 'head/faces/male/neutral'}
NOSE = 'head/nose/button/adult'
BROWS = 'eyes/eyebrows/thin/adult'
HAIR = {  # id: (label, fg, bg or None)
 'long': ('Long', 'hair/long/adult', None),
 'long_straight': ('Straight', 'hair/long_straight/adult', None),
 'wavy': ('Wavy', 'hair/wavy/adult/fg', 'hair/wavy/adult/bg'),
 'bangslong': ('Long bangs', 'hair/bangslong/adult', None),
 'curtains_long': ('Curtains', 'hair/curtains_long/adult', None),
 'ponytail': ('Ponytail', 'hair/ponytail2/adult/fg', 'hair/ponytail2/adult/bg'),
 'bunches': ('Bunches', 'hair/bunches/adult/fg', 'hair/bunches/adult/bg'),
 'page': ('Bob', 'hair/page/adult', None),
 'pixie': ('Pixie', 'hair/pixie/adult', None),
 'bangsshort': ('Short bangs', 'hair/bangsshort/adult', None),
 'curtains': ('Middle part', 'hair/curtains/adult', None),
 'parted': ('Side part', 'hair/parted/adult', None),
 'messy1': ('Messy', 'hair/messy1/adult', None),
 'buzzcut': ('Buzz cut', 'hair/buzzcut/adult', None),
}
TOP = {
 'tshirt': ('T-shirt', 'torso/clothes/shortsleeve/tshirt/{b}'),
 'longsleeve': ('Long sleeve', 'torso/clothes/longsleeve/longsleeve/{b}'),
 'cardigan': ('Cardigan', 'torso/clothes/longsleeve/longsleeve2_cardigan/{b}'),
 'polo': ('Polo', 'torso/clothes/longsleeve/longsleeve2_polo/{b}'),
 'sleeveless': ('Tank top', 'torso/clothes/sleeveless/sleeveless2/{b}'),
}
LEGS = {
 'pants': ('Pants', 'legs/pants/{t}'),
 'shorts': ('Shorts', 'legs/shorts/shorts/{t}'),
 'skirt': ('Skirt', 'legs/skirts/plain/{t}'),
}
FEET = {
 'shoes': ('Shoes', 'feet/shoes/basic/{t}', 15),
 'boots': ('Boots', 'feet/boots/basic/{t}', 25),
}
GLASSES = 'facial/glasses/round/adult'
SCARF = 'neck/scarf'
ANIMS = ['walk', 'sit', 'idle']

def all_paths():
    p = set(BODY.values()) | set(HEAD.values()) | set(FACE.values()) | {NOSE, BROWS, GLASSES, SCARF}
    for _, fg, bg in HAIR.values():
        p.add(fg)
        if bg: p.add(bg)
    for b, t in (('female', 'thin'), ('male', 'male')):
        for _, tp in TOP.values(): p.add(tp.format(b=b))
        for _, lp in LEGS.values(): p.add(lp.format(t=t))
        for _, fp, _z in FEET.values(): p.add(fp.format(t=t))
    return sorted(p)
