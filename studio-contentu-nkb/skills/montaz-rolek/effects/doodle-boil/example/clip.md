# Kredowy kontur: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/doodle-boil.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 3.4 s (102 frames).
Spoken line in the slot: "metodologię, ale całą tą wiedzę trzymasz w Twojej głowie,"

The CLIP block it was built with:
```
# The doodles, one per idea, in the order they are said. cue(word, doodle, ...):
#   word    the spoken word it draws on: first match in words.json after the previous cue ('word#2' = 2nd time),
#           or a time in seconds, or F(frame). build.py snaps Whisper's start to the audio onset and prints it.
#   doodle  a name from the library table in effect.md (heart, clapper, chip, bulb, clock, dollar, check ...)
#   cross='word'   crosses / scribbles it out on that word ("to NIE jest trudne"). hold='word' or seconds: when it rubs out
#           (default: HOLD_MAX after it lands, sooner if the next doodle needs its spot or the finale starts).
#   where   'auto' (most open space near her head) | 'left' | 'right' | 'above' | 'body' (on her torso, under the chin)
#   size    px, None = auto (from her head size, shrunk to fit the space). colour / fill / accent: 'cream' | 'yellow'
#           | 'pink' slot for the main line / scribble fill / other strokes. rot: tilt in degrees.
#   finale=True  the payoff: the outline goes double, rays burst round her, a few small stars sprinkle in (SPARKLE).
DOODLES = [
    cue('wiedzę', 'bulb'),
    cue('głowie,', 'star', finale=True),
]
OUTLINE = 'auto'      # 'auto' = single chalk line from the first doodle, double for the finale | 'single' | 'double' | 'off'
PALETTE = 'classic'   # 'classic' (cream, butter, pink) or 'blush' (cream, lilac, pink)
INK = None            # the buyer's colour for the main line (the cream slot), hex like '#FFF4E8'; None = palette
ACCENT =  '#FFF04A'         # the buyer's second colour (butter / lilac slot), hex; None = palette
ACCENT2 = None        # the third colour (pink slot), hex; None = palette. Avoid orange: it fights with skin tones.
DIM = 'auto'          # room dim behind her while chalk is up: 'auto' (from how bright and busy the room is) or 0 to 1
HOLD_MAX = 2.8        # seconds a doodle stays up when nothing else asks for its space
SPARKLE = 'auto'      # small stars that sprinkle in on the finale: 'auto' (as many as fit, up to 5) or 0 to 6
IN_FRAME = 3          # nothing appears before this frame (frame 0 must stay plain footage)
OUT_FRAME = -4        # everything is rubbed out by this frame (negative = from the end). None = hold to the last frame:
                      # only when the slot ends the reel or ends on a hard cut
SFX_PEAK_DB = -27.0   # chalk scratch peak (her voice peaks near -6 dBFS): -27 sits under her
```
Everything not in the block was left at the effect's default unless the block says otherwise.
