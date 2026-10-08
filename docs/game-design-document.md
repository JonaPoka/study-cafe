# Study Café — Game Design Document

Snapshot of October 8, 2026. The living version is the Claude Doc this file was exported from; this copy
adds what the demos settled (art sources, plaza layout).

## Overview

Study Café is a cozy 2D browser game where time spent studying earns coffee beans, which you spend
building your own café and dressing your character. You study alone, with friends in your café, or with
everyone in the weekly featured café.

**Design pillars**

1. **Building and dressing up are the reward.** The café and the character are what players show off, so
   they get the most design and polish.
2. **Studying together is the social core.** Every space is shared: the plaza, public cafés, and friends'
   cafés.
3. **No competition on study time.** No leaderboards and no study verification. Hours are a personal
   record, not a score.
4. **Small, fixed art budget.** Free asset packs plus recolors and layering carry the visuals, so
   development time goes into code.

**Platform:** Browser, desktop first. Top-down 3/4 view, moved with WASD or the arrow keys, interaction
with E.

**Out of scope:** Leaderboards, anti-cheat on study time, paid items that affect anything beyond looks,
mobile-first controls.

## Core loop and player flow

Study time becomes beans, beans become a café and a look worth showing, and that café becomes the place
others come to study.

```
Sit and study ──▶ Earn beans ──▶ Shop ──▶ Show off (café, look, profile)
      ▲                                              │
      └──────── Others visit and study with you ◀────┘
```

**First session**

1. Sign up and create a character from the free starter parts.
2. Arrive in the central plaza and see other players.
3. A short prompt points to your café door; inside, the starter layout already has a table and two chairs.
4. Sit down, start a 25-minute pomodoro, and finish with your first beans.
5. The shop opens with one affordable item highlighted, so the first purchase happens in the first session.

**Returning sessions** start in the plaza, where the player picks: their own café, a friend's café, a
public café from the directory, or the weekly café.

## World, plaza and lobbies

The world has two kinds of space: the central plaza, where everyone arrives, and cafés, which players
enter through doors in the plaza.

**Central plaza** (built in the demo): a paved square with a fountain, street lamps, lawns and trees, and
three building fronts along the top.

- **Your café door** (left building): loads your personal café.
- **Café directory** (middle building): search public cafés and visit one.
- **Weekly café door** (right building): joins a lobby of this week's featured café. A sign names the
  winning café and its creator.
- Planned: a contest board, a wardrobe mirror and a bean shop counter.
- Outdoor tables let players study outside.

Players see each other walk around, chat with speech bubbles, and open a player's profile by walking up
and pressing E. Name tags show who is studying what, or on break.

**Lobbies:** the plaza and the weekly café run as several copies, each with a player cap.

- **Fill-first:** a joining player goes to the fullest lobby still under its cap (start with 30). When all
  are full, a new lobby opens.
- **Join a friend:** joining through a friend's profile or invite puts you in their lobby.
- **Merge:** when two lobbies drop to a few players, new joiners are steered to one of them.

**Cafés:** a personal café is one room. Its capacity is the number of seats the owner has placed, plus
standing space. Visitors can walk, sit, study and chat, but never edit. The door is at the bottom of the
room; walking out returns you to the plaza in front of the door you used.

## Character creation and customization

A character is a stack of sprite layers drawn in a fixed order, so every option is a layer swap or a
recolor rather than a new drawing.

| Layer (bottom to top) | In the demo | How variety is made |
| --- | --- | --- |
| Body | 2 body types | 10 skin palettes |
| Head and face | Matching head, neutral face, nose, eyebrows | Skin palette; 8 eye colors |
| Bottoms and shoes | Pants, shorts, skirt; shoes, boots | 24 cloth colors each |
| Top | T-shirt, long sleeve, cardigan, polo, tank top | 24 cloth colors |
| Hair | 14 styles | 26 hair colors |
| Extras | Glasses, scarf | Scarf in 24 colors |

**Rules**

- Every layer must have the frames the game uses: walk in 4 directions, sit and idle.
- Recoloring is a palette swap done in code, so one hair sprite gives every hair color at no art cost.
- New players get a free starter set. Shop cosmetics add new shapes, rare colors and patterns.

**Creator screen:** a large animated preview, one section per layer, color swatches, and a Randomize
button. The same screen opens later from a wardrobe mirror.

## Studying

Sitting on any seat starts a study session, and standing up ends it. There is no verification: the game
trusts the player.

**Session flow**

1. Walk to a free seat and press E. The character sits and movement locks.
2. A timer panel opens: pomodoro (25 min focus, 5 min break by default, adjustable) or a free timer.
3. Optionally type what you are studying; it shows in your name tag.
4. Focus and break phases switch automatically.
5. Press a movement key or Stand up to end. Beans are paid with a short summary ("42 min · +46 beans").

**Rules**

- Break time earns nothing; focus time earns beans.
- The timer keeps running when the browser tab is in the background.
- Closing the tab ends the session and pays out the time so far.
- A session ends itself after 4 hours, so a forgotten tab doesn't run all night.
- Studying anywhere counts the same.

**Study together:** players at the same table can sync timers so breaks happen together. Status above
each player ("Chemistry · 14 min" or "on break") shows who is free to talk.

## Economy and shop

Coffee beans are the only currency, earned only by studying, at roughly 80 beans per hour of focus.

**Earning:** 1 bean per focused minute; +10 for every full 25 minutes of focus; +20 for the first session
of the day.

| Tier | Price | Study time | Examples |
| --- | --- | --- | --- |
| Small | 40–120 beans | 30 min to 1.5 h | Mug, plant, wall poster, hair color |
| Medium | 200–500 beans | 2.5–6 h | Table set, bookshelf, lamp, outfit |
| Large | 800–1,500 beans | 10–20 h | Counter, sofa, room size upgrade |
| Showpiece | 3,000+ beans | 40 h+ | Espresso machine, aquarium, rare outfit |

**Shop design:** full catalog by category, 3 daily specials at 20% off, themed sets, and a see-through
preview of furniture in your café before buying.

**Rules:** no real-money purchases at launch. Any later paid items are cosmetic only and never sold as
beans.

## Café building

The café is a tile grid with a few placement layers, strict rules, and recolor-based variety, so players
make good-looking cafés without art skill and new items need little drawing.

### Goals

- **Easy to start:** a new café comes pre-furnished.
- **Hard to make ugly:** palettes and matching sets keep combinations coherent.
- **Readable as yours:** layout, palette, lighting and music give each café an identity.
- **Never broken:** placement rules guarantee every seat can be reached from the door.

### Room and grid

- Square 32 px tiles in a top-down 3/4 view. Only the back wall shows decoration; side walls are thin
  edges. The door is fixed at the bottom center.

| Room size | Tiles | Price |
| --- | --- | --- |
| Starter | 10 × 8 | Free |
| Cozy | 12 × 10 | 800 beans |
| Roomy | 14 × 12 | 1,500 beans |
| Grand | 16 × 14 | 3,000 beans |

An upgrade grows the room to the right and down, so placed items keep their positions.

### Placement layers

| Layer | Examples | Placed on | Blocks walking |
| --- | --- | --- | --- |
| Floor style | Wood planks, tiles, herringbone | Whole room | No |
| Wall style | Striped wallpaper, brick, paneling | Whole back wall | No |
| Rugs | Swirl rug, diamond rug | Floor tiles, under furniture | No |
| Furniture | Tables, chairs, sofas, counters, plants, lamps | Floor tiles, by footprint | Yes |
| Tabletop items | Mugs, laptop, cakes, flowers, papers | Slots on tables and counters | No |
| Wall decor | Paintings, posters, shelves, sconces, curtains | Slots on the back wall | No |

### Footprints, rotation and depth

- Every floor item has a footprint in tiles.
- Only seats rotate (4 directions), because facing decides how the character sits.
- Everything is drawn in order of its bottom edge, so characters walk behind and in front of furniture.
  Seated characters sort just after their chair, so a table in front covers their legs.

### Seats

- A chair, stool or sofa has seat points with a facing direction and a stand point next to it. Pressing E
  near the stand point snaps the character onto the seat.
- The number of seats is the café's capacity.

### Placement rules

The client shows the result live; the server checks the same rules on save.

1. The footprint is inside the room and doesn't overlap other blocking furniture. Rugs can sit under
   anything.
2. **Path rule:** every seat and the door stay reachable, checked with a flood fill from the door.
3. A seat needs a free walkable tile next to it.
4. Tabletop items need a free slot on a table or counter.
5. Wall decor needs enough free back-wall width.
6. At most 150 objects per café.

### Edit mode

- **B** or the hammer button in your own café. The view fits the room and shows the grid.
- An inventory bar lists owned items by category, plus a shop tab.
- Place with a snapped see-through ghost (green valid, red not), **R** rotates a seat, **Esc** cancels.
- Click to pick up; **Delete** returns to inventory. Items are never destroyed or sold.
- Undo and redo with Ctrl+Z and Ctrl+Y.
- Visitors stay while you edit; occupied seats can't be moved.
- Autosave, plus three layout slots.

### Making cafés look good with little art

- **Café palette:** recolors floor, walls and recolorable items. The demo's weekly café is the same room
  as your café with another wallpaper, floor, rug and sofa color.
- **Color variants:** one sofa sprite in several colors is several shop items.
- **Sets** with a cosmetic badge for completing one.
- **Lighting presets** (morning to night) tint the room and make lamps glow.
- **Music:** the owner picks the café's lo-fi loop.
- **Starter layout** for new cafés.

### Data format

A café is one JSON document. Contest snapshots are copies of it.

```json
{
  "version": 1,
  "size": { "w": 12, "h": 10 },
  "palette": "warm-wood",
  "floor": "oak-planks",
  "wall": "teal-stripes",
  "lighting": "evening",
  "music": "rainy-lofi",
  "items": [
    { "uid": "a1", "item": "table_round", "x": 3, "y": 4 },
    { "uid": "a2", "item": "chair_dining", "x": 2, "y": 4, "rot": 1, "color": "green" },
    { "uid": "a3", "item": "mug", "on": "a1", "slot": 0 },
    { "uid": "a4", "item": "painting_wave", "wall": 5 }
  ]
}
```

Item definitions:

```json
{
  "id": "chair_dining",
  "layer": "furniture",
  "footprint": [1, 1],
  "blocks": true,
  "rotations": 4,
  "seats": [{ "dx": 0, "dy": 0 }],
  "recolor": true,
  "set": "library",
  "price": 120,
  "sprite": "furniture#chair_dining"
}
```

The placement rules live in one shared TypeScript module that client and server both run.

## Social: visiting, publishing and profiles

| Café privacy | Who can enter | In the directory |
| --- | --- | --- |
| Private | Only the owner | No |
| Friends | Friends and anyone with the invite link | No |
| Public | Anyone | Yes |

- Invite links can be reset. The owner can remove and block visitors.
- **Café directory:** search public cafés by name or owner; sort by visitors now, newest, most liked.
- **Profile:** username, character preview, total hours studied, a free-text personal goal, Visit café
  button, Add friend.
- **Friends list** shows who is online and where, with one-click join.
- **Chat:** speech bubbles plus a log scoped to the room; word filter, report, mute. No voice at launch.

## Weekly café contest

Each week players vote for the best public café; the winner becomes the weekly café for the next week.

1. **Submit, Monday to Wednesday:** a snapshot of your public café.
2. **Vote, Thursday to Saturday:** pick the better of two cafés, as many pairs as you like.
3. **Review, Sunday:** the top few are checked before the winner is confirmed.
4. **Swap, Monday 00:00 UTC:** the winner becomes the weekly café; the previous one moves to a Hall of
   Fame.

Rules: snapshots, not live cafés; only accounts older than a few days vote; no back-to-back wins; rewards
are cosmetic. Ship with a weekly café you design yourself.

## Art direction and assets

Decided by the demos: everything is LPC family art, 32 px tiles, top-down 3/4 view, integer scaling (2×).

| Need | Source (in `assets/`) | License |
| --- | --- | --- |
| Floors, walls, windows, doors, building fronts, furniture, small items, wall items, terrain, trees | LPC Revised by Eliza Wyatt and contributors (`environment/`) | CC-BY 3.0 / OGA-BY 3.0 |
| Character parts and palettes | Universal LPC Spritesheet Character Generator (`characters/`) | CC0 / CC-BY / OGA-BY / CC-BY-SA / GPL per file |
| UI panels | Built in CSS (Kenney UI packs are a CC0 option) | — |
| Fonts | Pixelify Sans, Nunito (Google Fonts) | OFL |
| Music (not yet added) | Not Jam Music Pack (CC0), Cozy cats lo-fi (CC-BY 4.0) | — |

**License checklist:** credits screen listing every artist (see `CREDITS.md`); edited CC-BY-SA or GPL
character sprites shared under the same license; serve plain image files (no DRM); only add clothing
parts that have walk, sit and idle frames.

**Visual rules:** one tile size, integer scaling, a warm limited UI palette, and lighting presets and
palette swaps for atmosphere.

## Tech notes

| Part | Choice |
| --- | --- |
| Rendering | PixiJS or Phaser (the demo uses plain canvas) |
| Real-time rooms | Node.js with Colyseus or plain WebSockets |
| Shared logic | TypeScript module used by client and server |
| Database | PostgreSQL, café layouts in a JSON column |
| Hosting | Home server behind a tunnel; sprites on a static host or CDN |

| Model | Key fields |
| --- | --- |
| Player | id, username, character (parts and palette names), beans, totalStudyMinutes, goalText, cafeId, friends |
| Café | id, ownerId, name, privacy, inviteToken, layout (JSON), likes, layoutSlots |
| Item definition | id, layer, footprint, rotations, seats, surfaceSlots, recolor, set, price, sprite |
| Inventory | playerId, itemId, color, count |
| Study session | playerId, roomId, startedAt, endedAt, focusMinutes, beansEarned |
| Contest entry | week, cafeId, snapshot, score |
| Vote | week, voterId, entryA, entryB, winner |

Store a character as part ids plus palette names (as the demo does), never as a rendered image; the client
composes and recolors at load.

**Network messages:** position and facing about 10 times a second; sit, stand, session start and end;
chat; edit operations validated by the shared rules. The server records session times and pays beans
from them for consistency, not as anti-cheat.

## Build roadmap

1. **Walk and talk:** character creator, plaza, lobbies, chat. *(Demo covers the single-player part.)*
2. **Study loop:** personal café, sitting, timers, beans, invite links. *(Demo covers the single-player
   part.)*
   - Gate: playtest with friends for a week before building further.
3. **Build:** shop, edit mode, placement rules, room upgrades, palettes, lighting, music, cosmetics.
4. **Share:** profiles with goal text, privacy, public café directory, likes, friends.
5. **Contest:** weekly submissions, pairwise voting, global weekly café, Hall of Fame.

## Open questions

- [ ] Weekly café seats: require a minimum seat count, or add seats to small winners?
- [ ] Sign-in: email, Google, Discord, or several?
- [ ] Personal goal text: visible to everyone or only friends?
- [ ] Who reviews contest winners on weeks you can't?
