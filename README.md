# Study Café

A cozy 2D browser game where time spent studying earns coffee beans. Players spend beans on
decorating their own café and dressing their character, and study together in the central
plaza, in friends' cafés, or in the weekly featured café.

This folder is the project root. It holds the free art the game is built from, a playable
reference demo, the tools that built it, and the game design document.

## Folder layout

```
study-cafe/
├── README.md                  this file
├── CREDITS.md                 artists and licenses (required by the art licenses)
├── docs/
│   └── game-design-document.md
├── assets/
│   ├── environment/           LPC Revised art: floors, walls, windows, doors, buildings,
│   │                          furniture, small items, wall items, terrain, trees
│   ├── characters/            Universal LPC character parts
│   │   ├── spritesheets/      body, head, face, hair, tops, legs, shoes, glasses, scarf
│   │   │                      (walk, sit and idle sheets for each part)
│   │   ├── palette_definitions/   recolor palettes: skin, hair, cloth, eyes
│   │   ├── sheet_definitions/     every part the generator offers, with layer depth
│   │   └── CREDITS.csv            per-file authors and licenses
│   ├── ui/                    icons cut from the packs (coffee bean, chair, mirror, cake, door)
│   └── scenes/                prebuilt backgrounds for the plaza and both cafés (640 × 400)
└── demos/
    ├── study-cafe-demo.html   the playable demo, one self-contained file
    ├── README.md              controls and what the demo shows
    ├── screenshots/           the demo in action
    ├── mockups/               earlier still mockups
    └── tools/                 Python build pipeline for the demo
```

## Running the demo

Open `demos/study-cafe-demo.html` in any modern browser. It needs no server and no install;
all sprites are embedded in the file. Controls are in `demos/README.md`.

## Rebuilding the demo

Needs Python 3 and Pillow (`pip install pillow`).

```
python3 demos/tools/build.py
```

This crops the room and plaza art from `assets/environment/`, builds the scene backgrounds,
packs every character sheet and palette, and writes a fresh `demos/study-cafe-demo.html`.
Intermediate files go to `demos/tools/build/`.

## How the art fits together

- **One style.** Everything is LPC (Liberated Pixel Cup) family art: 32 px tiles in a
  top-down 3/4 view. Characters are drawn on 64 × 64 frames.
- **Characters are layers.** A character is a stack of part sheets drawn in `zPos` order
  (body 10, legs 20, top 35, head 100, face 101, hair 120 and so on; see
  `demos/tools/game.template.html`, function `layersFor`). The layer depth for any part is
  in its `sheet_definitions` JSON.
- **Colors are palette swaps.** Each part sheet is drawn in a base palette (skin `light`,
  hair `orange`, cloth `white`, eyes `blue`). Swapping those exact colors for another palette
  from `palette_definitions` recolors the part, so one sprite gives every color for free.
- **Sheet layout.** Rows are directions: up, left, down, right. `walk` has 9 frames (frame 0
  standing), `sit` has 3 (frame 3, index 2, is sitting on a chair), `idle` has 2.
- **Depth sorting.** Furniture and characters are drawn in order of their bottom edge
  (`sortY`), which is what lets players walk behind and in front of things. Seated
  characters sort just after their chair, so a table in front covers their legs.
- **Adding character parts.** The full generator has hundreds more parts. Pick them from
  `sheet_definitions`, add their paths to `demos/tools/parts.py`, and fetch their sheets from
  https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator (only
  parts with a `sit` animation work for seated players).

## Licenses in one paragraph

Environment art is CC-BY 3.0 / OGA-BY 3.0: credit required. Character parts mix CC0, CC-BY,
OGA-BY, CC-BY-SA and GPL: credit required, and edited CC-BY-SA or GPL sprites must be shared
under the same license. Keep `CREDITS.md` and the per-folder credit files with the game and
show a credits screen. This is a practical summary, not legal advice.
