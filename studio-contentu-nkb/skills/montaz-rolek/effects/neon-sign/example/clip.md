# Neon: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/neon-sign.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: medium shot, camera still, 1080x1920, 30 fps. Slot: 3.9 s (117 frames).
Spoken line in the slot: "Nagrywanie nigdy nie było dla mnie trudne, gorzej z montażem."

The CLIP block it was built with:
```
LINES = [
    ('gorzej z', 'nigdy'),
    ('*montażem*', 'trudne,'),
]
UNDERLINE = 'auto'        # a swash tube under the last line: 'auto' (strikes 0.4 s after the last line), a word,
                          # seconds, or None
STEP_ON = None            # a word where the whole sign steps brighter with a low thump ('like THAT'), or None
OUT = 'auto'              # 'auto' (switches off, plain footage 3 frames before the end), seconds (switch-off time),
                          # or 'cut' (stays lit to the last frame; only when the reel cuts away right after)
FONT = 'Marck Script'     # any family in assets/fonts/fonts.css. A script face reads as hand-bent neon (the demo);
                          # a sans (Figtree, Montserrat) gives a clean monoline sign. The glyphs are thinned to one tube
WEIGHT = 400              # weight (variable fonts follow it; a static file stays what it is)
CASE = 'as typed'         # 'as typed', 'upper', 'lower', 'title'
INK =  (255, 240, 74)     # tube colour (butter yellow FAE67A, the demo). Pale colours glow best; never orange
ACCENT = 'ink'            # underline and *line* colour: 'ink' (same as INK) or (r, g, b), e.g. the buyer's highlight
ALIGN = 'stagger'         # 'stagger' (each line steps right, sign-painter look), 'left', 'centre'
TILT = 4.0                # degrees the lines climb to the right (0 = level; 4 = the demo)
PLACE = 'auto'            # 'auto' or force 'beside' / 'above' / 'corner'; or (x, y, size): left end of the first
                          # baseline in 1080x1920 px of frame 0 and the letter size in px (read off a preview still)
SIDE = 'auto'             # beside the head: 'auto' (the side with more open wall), 'left', 'right'
SIZE_MAX = 200            # largest letter size in px (the demo: 196)
FLICKER = 'classic'       # 'classic' (irregular strike, the demo) or 'soft' (two quick pulses, then steady)
ROOM_DIM = 'auto'         # room exposure while lit (0.56 = most of a stop); 'auto' sets it from how bright the room is
SPILL = 1.0               # wall glow strength multiplier
CABLE = None              # optional visible flex: list of (x, y) frame-0 px from a tube end to where it hides behind
                          # something (the couch, the speaker). None = wired through the wall (nothing shows)
OCCLUDERS = []            # optional shadows: [([(x, y), ...] polygon in frame-0 px, depth px), ...] for things that
                          # stand proud of the wall right next to the sign (a frame: 18, a wall light: 110). [] = none
BUZZ_DB, THUMP_DB = -33.0, -27.0   # sound peaks (dBFS); the voice peaks around -5
```
Everything not in the block was left at the effect's default unless the block says otherwise.
