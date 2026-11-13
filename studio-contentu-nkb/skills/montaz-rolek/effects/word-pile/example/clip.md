# Spadające klocki: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/word-pile.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: wide shot, camera still, 1080x1920, 30 fps. Slot: 7.2 s (216 frames).
Spoken line in the slot: "Mój branding, a on dobiera napisy, grafiki i efekty pasujące do danej sceny."

The CLIP block it was built with:
```
SLABS = [
    ('NAPISY', 'napisy,', 1.0),
    ('GRAFIKI', 'grafiki', 1.0),
    ('EFEKTY', 'efekty', 2.6),
]
T_SWEEP = 'auto'     # the word the gust blows the pile away on (same forms); 'auto' = 1.7 s after the last drop
SWEEP_DIR = 'auto'   # 'auto' (out on the side the pile is nearest), 'left' or 'right'
FONT = 'Inter Tight'  # slab type: any family in assets/fonts/fonts.css (the buyer's caption font)
WEIGHT = 900         # slab type weight (variable fonts follow it; a static file stays what it is)
CASE = 'upper'       # 'upper', 'lower', 'title' or 'as typed'
TRACK = 0.0          # letter spacing in em (0.02 opens caps up a little)
INK = (255, 248, 239)        # type on the dark slabs (cream)
SLAB = (30, 33, 42)          # dark slab colour (it gets a top-to-bottom shade and an underside)
ACCENT = (255, 240, 74)     # the heavy slab (butter yellow): the buyer's highlight colour
ACCENT_INK = (20, 22, 28)    # type on the heavy slab
LINE = (255, 248, 239)       # the drawn floor line
TYPE_PX = 'auto'     # cap size of the type: 'auto' (66 px, smaller when the pile has little room) or a number
FLOOR_Y = 'auto'     # y of the floor line: 'auto' = 1420 (the safe zone ends at 1470)
SPAWN = 'auto'       # 'auto', 'top' (drop past the head), 'side' (tossed in under the chin, for very tight shots)
CHIN_Y = 'auto'      # lowest chin y over the slot if the printed one is wrong (the pile stays below it)
DROPS = None         # None = search; or a list per slab of dict(x=, ang=, spin=) from a previous printout to pin them
```
Everything not in the block was left at the effect's default unless the block says otherwise.
