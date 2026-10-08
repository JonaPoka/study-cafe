# Demos

Reference material for building the real game. None of this is production code: it is one
file of plain JavaScript so it is easy to read and borrow from.

## study-cafe-demo.html

Open it in a browser. You start in the central plaza.

**Controls**

| Key | Action |
| --- | --- |
| WASD or arrow keys | Walk |
| Walk into a door, or E | Enter a building |
| E next to a free seat | Sit and start a pomodoro |
| Any movement key, or E | Stand up and get your session summary |
| C | Wardrobe |
| ` (backtick) or F2 | Debug menu |
| Esc | Close panels |

On touch screens an on-screen D-pad and E button appear.

**Scenes**

- **Central Plaza:** three buildings. The left door is your café, the middle one opens the
  café directory, the right one is the weekly café. Two outdoor seats let you study outside.
  Other players walk around, sit and chat.
- **Midnight Study Café:** your café, teal wallpaper and a pink rug, 10 seats.
- **Nordic Nook:** the weekly café, the same room rebuilt with another palette (peach walls,
  light floor, blue rug, yellow sofa) to show how owner palettes change a room.

Walk down onto the door mat to go back to the plaza. You come out in front of the door you
went in through.

**What to look at in the code** (`tools/game.template.html`)

| Feature | Where |
| --- | --- |
| Runtime palette recolor | `recolored()` |
| Character layer stack | `layersFor()`, `buildCharacter()` |
| Y-sorted drawing and lighting | `render()` |
| Collisions | `blocked()` |
| Doors and fade transitions | `useExit()`, `transition()`, `enterScene()` |
| Pomodoro, beans, background-tab timing | `startSession()`, `tickStudy()`, `frame()` |
| Other players | `NPC_DEFS`, `updateWalker()`, `npcStatus()` |
| Wardrobe UI | `buildWardrobe()` |
| Debug menu | `bindToggle()` and the `#debug` panel |
| Scene data (objects, seats, exits, glows) | `tools/bundle.py` |

**Study rules in the demo:** 1 bean per focused minute, +10 per finished pomodoro, focus and
break switch automatically, and the timer keeps going when the tab is in the background. Beans,
study minutes, your look and timer lengths are saved in the browser's localStorage.

**Debug menu:** live stats, toggles for collision boxes, seats, door zones, draw order,
lighting, other players and name tags, time speed (1× to 300×), focus and break length, walk
speed, +100 beans, skip to end of phase, jump to any scene, reset save, and an event log.

## screenshots/ and mockups/

Screens from the demo, plus the first still mockup of the café with the real assets and a
plaza view with collision boxes drawn.

## tools/

| File | What it does |
| --- | --- |
| `build.py` | Runs `bundle.py` and writes `../study-cafe-demo.html` |
| `bundle.py` | Builds the plaza and both cafés: backgrounds, objects with depth and collisions, seats, doors, glows; packs all sprites |
| `parts.py` | The character part catalog used by the demo |
| `game.template.html` | The game: HTML, CSS and JavaScript, with the asset bundle injected at build time |
| `char.py` | Python version of the character compositor, for making stills |
| `compose.py` | Renders the still café mockup in `build/` |
| `sheet.py`, `zoom.py`, `mz.py` | Contact sheets and gridded zooms for finding crop coordinates in sprite sheets |
| `preview_scene.py` | Renders a built scene with collision boxes, seats and doors drawn |

Example: `python3 demos/tools/zoom.py "assets/environment/Objects/Furniture/Shelf.png" 0 0 224 96 3 shelf.png`
